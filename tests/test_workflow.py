"""Full local workflows: registered observations, bundle bytes and inline recovery."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
import subprocess
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("workflow", Path(__file__).resolve().parents[1] / "runtime/workflow.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.flow = w.Workflow(self.root, "dot", {"url": "https://worker.example/thread/a"})

    def tearDown(self):
        self.tmp.cleanup()

    def obs(self, users=None, replies=None, **extra):
        return {"url_sha256": self.flow.binding, "observed_at": w.stamp(),
                "users": users or [], "assistants": replies or [], "generating": False, **extra}

    def deliver(self, flow=None, continuation=False):
        flow = flow or self.flow
        base = {"url_sha256": flow.binding, "observed_at": w.stamp(), "users": [], "assistants": [], "generating": False}
        prepared = flow.prepare("Give two structured rows for {RUN_ID}", base, continuation)
        raw = json.dumps({"run_id": prepared["run_id"], "state": "DONE", "results": [{"id": 1}, {"id": 2}]})
        for _ in range(2):
            receipt = flow.reconcile({**base, "observed_at": w.stamp(), "users": [prepared["message"]], "assistants": [raw]})
        self.assertEqual("SUCCESS", receipt["status"])
        return prepared, raw

    def bundle(self, run, bad=False, traversal=False):
        result = json.dumps({"results": [{"id": 1}, {"id": 2}, {"id": 2}]}).encode()
        manifest = {"run_id": run, "files": {"results.json": w.digest(result), "summary.md": w.digest(b"Summary")}}
        if bad:
            manifest["files"]["results.json"] = "bad"
        path = self.root / "bundle.zip"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("manifest.json", json.dumps(manifest))
            z.writestr("results.json", result)
            z.writestr("summary.md", b"Summary")
            if traversal:
                z.writestr("../escape.json", b"[]")
        return path

    def test_dot_bundle_then_continue_and_dedupe(self):
        prepared, _ = self.deliver()
        path = self.bundle(prepared["run_id"])
        first = self.flow.ingest(path, prepared["run_id"])
        self.assertEqual("VALIDATED", first["state"])
        self.assertEqual((3, 2, 1), (first["row_count"], first["new_row_count"], first["duplicate_row_count"]))
        second = self.flow.ingest(path, prepared["run_id"])
        self.assertTrue(second["duplicate_bundle"])
        self.assertEqual(0, second["new_row_count"])
        self.deliver(continuation=True)
        self.assertEqual(2, self.flow.state["turn_count"])

    def test_muse_inline_fallback_then_continue(self):
        muse = w.Workflow(self.root, "muse", {"url": "https://worker.example/thread/m"})
        prepared, raw = self.deliver(muse)
        source = self.root / "inline.json"
        source.write_text(raw)
        record = muse.ingest(source, prepared["run_id"], inline=True)
        self.assertEqual("INLINE", record["delivery"])
        self.assertEqual("VALIDATED", record["state"])
        self.deliver(muse, continuation=True)

    def test_b06_and_delivery_unknown_no_replay(self):
        prepared = self.flow.prepare("go", self.obs())
        reply = json.dumps({"run_id": prepared["run_id"], "state": "DONE", "results": []})
        self.assertEqual("DELIVERY_UNKNOWN", self.flow.reconcile(self.obs(replies=[reply]))["status"])
        with self.assertRaisesRegex(ValueError, "NO_RESEND"):
            self.flow.prepare("retry", self.obs())
        self.assertEqual("REPLY_TIMEOUT", self.flow.reconcile(self.obs(users=[prepared["message"]], replies=[reply]))["status"])
        self.assertEqual("SUCCESS", self.flow.reconcile(self.obs(users=[prepared["message"]], replies=[reply]))["status"])

    def test_stale_wrong_thread_and_replayed_observation(self):
        with self.assertRaisesRegex(ValueError, "STALE"):
            self.flow.prepare("go", self.obs(observed_at="2000-01-01T00:00:00Z"))
        with self.assertRaisesRegex(ValueError, "WRONG_THREAD"):
            self.flow.prepare("go", self.obs(url_sha256="wrong"))
        self.flow.prepare("go", self.obs())
        obs = self.obs()
        self.flow.reconcile(obs)
        with self.assertRaisesRegex(ValueError, "NON_NEW"):
            self.flow.reconcile(obs)

    def test_malformed_preserved_partial_not_validated(self):
        prepared, _ = self.deliver()
        source = self.root / "bad.json"
        raw = '{"results":[{"id":1},{"id":2},'
        source.write_text(raw)
        record = self.flow.ingest(source, prepared["run_id"], inline=True)
        self.assertEqual("READ", record["state"])
        self.assertEqual(2, record["row_count"])
        saved = self.root / "artifacts" / prepared["run_id"] / record["sha256"] / "source.json"
        self.assertEqual(raw, saved.read_text())
        self.assertFalse((self.root / "artifact-index.json").exists())

    def test_manifest_mismatch_and_unsafe_zip_not_validated(self):
        prepared, _ = self.deliver()
        self.assertEqual("READ", self.flow.ingest(self.bundle(prepared["run_id"], bad=True), prepared["run_id"])["state"])
        record = self.flow.ingest(self.bundle(prepared["run_id"], traversal=True), prepared["run_id"])
        self.assertEqual("DOWNLOADED", record["state"])
        self.assertFalse((self.root / "escape.json").exists())

    def test_generating_resets_stability_and_empty_not_validated(self):
        prepared = self.flow.prepare("go", self.obs())
        raw = json.dumps({"run_id": prepared["run_id"], "state": "DONE", "results": []})
        self.flow.reconcile(self.obs(users=[prepared["message"]], replies=[raw]))
        self.flow.reconcile(self.obs(users=[prepared["message"]], replies=[raw], generating=True))
        self.assertEqual("REPLY_TIMEOUT", self.flow.reconcile(self.obs(users=[prepared["message"]], replies=[raw]))["status"])
        self.assertEqual("SUCCESS", self.flow.reconcile(self.obs(users=[prepared["message"]], replies=[raw]))["status"])
        source = self.root / "empty.json"
        source.write_text(raw)
        self.assertEqual("READ", self.flow.ingest(source, prepared["run_id"], inline=True)["state"])

    def test_discovery_is_correlated_and_not_download(self):
        prepared, raw = self.deliver()
        obs = self.obs(reply_sha256=w.digest(raw), artifacts=[{"name": "bundle.zip", "target": "a >> nth=0"}])
        record = self.flow.discover(obs)
        self.assertEqual("VISIBLE", record["primary"]["state"])
        self.assertFalse((self.root / "artifact-index.json").exists())
        with self.assertRaisesRegex(ValueError, "BINDING"):
            self.flow.discover({**obs, "reply_sha256": "old"})

    def test_registered_wrapper_uses_same_durable_budget(self):
        aliases = self.root / "workers.json"
        aliases.write_text(json.dumps({"workers": {"dot": self.flow.worker}}))
        observation = self.root / "observation.json"
        w.write(observation, self.obs())
        script = w.ROOT / "skills/browser-worker/scripts/worker.py"
        cmd = [sys.executable, str(script), "ask", "--transport", "registered", "--worker", "dot", "--workers", str(aliases), "--state-dir", str(self.root), "--observation", str(observation), "--allow-example", "--message", "structured task"]
        first = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(0, first.returncode, first.stdout)
        self.assertEqual("PREPARED", json.loads(first.stdout)["status"])
        second = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual("PENDING_OR_DELIVERY_UNKNOWN_NO_RESEND", json.loads(second.stdout)["status"])

    def test_turn_budget_and_partial_csv(self):
        self.deliver()
        with self.assertRaisesRegex(ValueError, "MAX_TURNS"):
            self.flow.prepare("extra", self.obs(), True, 1)
        parsed = w.parse_result("id,name\n1,good\n2,\n3,extra,column\n", ".csv")
        self.assertEqual("PARTIAL", parsed["parse_status"])
        self.assertEqual(2, len(parsed["rows"]))


if __name__ == "__main__":
    unittest.main()
