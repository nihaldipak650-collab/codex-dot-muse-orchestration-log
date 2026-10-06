"""Transport-neutral persistent worker and artifact workflow (stdlib only).

Registered browser tools remain owned by Codex. This CLI prepares durable turns
and reconciles their observations; it never pretends Python can invoke those tools.
All observations and downloads are private inputs supplied by the coordinator.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

VERSION = "3.0.0"
ROOT = Path(__file__).resolve().parents[1]
STATES = {"CONTINUE", "NEED_CONTEXT", "BLOCKED", "DONE"}
MAX_BYTES = 32 * 1024 * 1024


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode("utf-8")).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def instant(value):
    parsed=datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("TIMEZONE_REQUIRED")
    return parsed.astimezone(timezone.utc)


def parse_result(text, suffix=".json"):
    """Preserve raw separately. Recover complete JSON objects, never invent rows."""
    cleaned = text.strip()
    fenced = re.fullmatch(r"```(?:json|csv)?\s*\n(.*?)\n```", cleaned, re.S)
    if fenced:
        cleaned = fenced[1]
    errors, rows, data = [], [], None
    try:
        if suffix == ".csv":
            reader = csv.DictReader(io.StringIO(cleaned), strict=True)
            if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
                raise ValueError("INVALID_CSV_HEADER")
            for number, row in enumerate(reader, 2):
                if None in row or any(v is None for v in row.values()):
                    errors.append({"row": number, "code": "CSV_COLUMN_MISMATCH"})
                else:
                    rows.append(row)
            data = rows
        elif suffix in (".md", ".txt"):
            return {"parse_status": "READ", "rows": [], "data": None, "errors": []}
        else:
            data = json.loads(cleaned)
            candidates = data.get("results", []) if isinstance(data, dict) else data
            if not isinstance(candidates, list):
                raise ValueError("RESULTS_NOT_ARRAY")
            for number, row in enumerate(candidates):
                if isinstance(row, dict):
                    rows.append(row)
                else:
                    errors.append({"row": number, "code": "ROW_NOT_OBJECT"})
    except (ValueError, csv.Error):
        errors.append({"code": "MALFORMED_RESULT"})
        if suffix == ".json":
            # Recover only complete top-level objects in the results array.
            match = re.search(r'"results"\s*:\s*\[', cleaned)
            offset = match.end() if match else 0
            decoder = json.JSONDecoder()
            while match and offset < len(cleaned):
                offset += len(cleaned[offset:]) - len(cleaned[offset:].lstrip(" \r\n\t,"))
                try:
                    row, length = decoder.raw_decode(cleaned[offset:])
                except ValueError:
                    break
                if isinstance(row, dict):
                    rows.append(row)
                offset += length
    return {"parse_status": "PARTIAL" if errors and rows else "MALFORMED" if errors else "PARSED",
            "rows": rows, "data": data, "errors": errors}


class Workflow:
    def __init__(self, directory, alias, worker):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", alias):
            raise ValueError("INVALID_ALIAS")
        self.base, self.alias, self.worker = Path(directory), alias, worker
        self.path = self.base / (alias + ".json")
        self.binding = digest(worker["url"])
        self.base.mkdir(parents=True, exist_ok=True)
        self.state = load(self.path) if self.path.exists() else {
            "worker_alias": alias, "thread_binding": self.binding, "turn_count": 0,
            "pending": False, "last_status": "NEW", "last_run_id": None}
        if self.state["thread_binding"] != self.binding:
            raise ValueError("THREAD_BINDING_MISMATCH")

    def save(self):
        self.state["updated_at"] = stamp()
        write(self.path, self.state)

    def receipt(self, run):
        if not re.fullmatch(r"BW-[a-f0-9]{32}", run):
            raise ValueError("INVALID_RUN_ID")
        path=self.base / "turns" / (run + ".json")
        if path.exists():
            return load(path)
        resolved=self.state.get('receipt_runs',{}).get(run,run)
        if not re.fullmatch(r"BW-[a-f0-9]{32}", resolved):
            raise ValueError("INVALID_RECEIPT_POINTER")
        receipt=load(self.base / "runs" / (resolved + ".json"))
        if receipt.get('worker_identifier_safe',{}).get('url_sha256') != self.binding:
            raise ValueError("RECEIPT_THREAD_MISMATCH")
        return receipt

    def observation(self, observed):
        if observed.get("url_sha256") != self.binding:
            raise ValueError("WRONG_THREAD_OBSERVATION")
        age = (datetime.now(timezone.utc) - instant(observed["observed_at"])).total_seconds()
        if not 0 <= age <= 120:
            raise ValueError("STALE_OBSERVATION")
        if not all(isinstance(observed.get(k), list) and all(isinstance(v, str) for v in observed[k]) for k in ("users", "assistants")):
            raise ValueError("INVALID_OBSERVATION")
        if not isinstance(observed.get("generating"), bool):
            raise ValueError("GENERATION_SIGNAL_REQUIRED")

    def prepare(self, message, observed, continuation=False, max_turns=6):
        self.observation(observed)
        if self.state["pending"]:
            raise ValueError("PENDING_OR_DELIVERY_UNKNOWN_NO_RESEND")
        if self.state["turn_count"] >= max_turns:
            raise ValueError("MAX_TURNS")
        if continuation and self.state["last_status"] != "SUCCESS":
            raise ValueError("NO_CONFIRMED_PREVIOUS_TURN")
        run = "BW-" + uuid.uuid4().hex
        text = "RUN_ID=" + run + "\nInclude this RUN_ID in your reply.\n" + message.replace("{RUN_ID}", run)
        turn = {"run_id": run, "thread_binding": self.binding, "prepared_at": stamp(),
                "message_sha256": digest(text.strip()), "baseline_users": [digest(v) for v in observed["users"]],
                "baseline_assistants": [digest(v) for v in observed["assistants"]], "last_observed_at": observed["observed_at"],
                "submit_confirmed": False, "reply_received": False, "stable_reply": None,
                "final_status": "DELIVERY_UNKNOWN"}
        write(self.base / "turns" / (run + ".json"), turn)
        self.state.update(last_run_id=run, pending=True, last_status="IN_FLIGHT",
                          turn_count=self.state["turn_count"] + 1, transport="registered")
        self.save()  # Before returning text that could be sent.
        return {"status": "PREPARED", "run_id": run, "message": text, "thread_binding": self.binding}

    def reconcile(self, observed):
        self.observation(observed)
        if not self.state["pending"]:
            return {"status": "NOT_PENDING"}
        path = self.base / "turns" / (self.state["last_run_id"] + ".json")
        turn = load(path)
        if instant(observed["observed_at"]) <= instant(turn["last_observed_at"]) or instant(observed["observed_at"]) < instant(turn["prepared_at"]):
            raise ValueError("NON_NEW_OBSERVATION")
        users = [v for v in observed["users"] if digest(v) not in turn["baseline_users"] and digest(v.strip()) == turn["message_sha256"]]
        replies = [v for v in observed["assistants"] if digest(v) not in turn["baseline_assistants"] and turn["run_id"] in v]
        confirmed = len(users) == 1
        turn["submit_confirmed"] = confirmed
        turn["last_observed_at"] = observed["observed_at"]
        status = "REPLY_TIMEOUT" if confirmed else "DELIVERY_UNKNOWN"
        if confirmed and len(replies) == 1:
            raw = replies[0]
            folder = self.base / "artifacts" / turn["run_id"]
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "reply.raw.txt").write_text(raw, encoding="utf-8")
            parsed = parse_result(raw)
            write(folder / "reply.parsed.json", parsed)
            data = parsed["data"]
            structured = isinstance(data, dict) and data.get("run_id") == turn["run_id"] and data.get("state") in STATES
            complete = not observed["generating"] and (structured or observed.get("completion") is True or raw.strip() == "ACK " + turn["run_id"])
            if complete and turn["stable_reply"] == digest(raw):
                status = "SUCCESS"
                turn.update(reply_received=True, reply_sha256=digest(raw))
                self.state.update(last_correlated_reply_hash=digest(raw), next_state=data.get("state") if structured else "UNSTRUCTURED")
            turn["stable_reply"] = digest(raw) if complete else None
        else:
            turn["stable_reply"] = None
        turn["final_status"] = status
        write(path, turn)
        self.state.update(last_status=status, pending=status != "SUCCESS")
        if confirmed:
            self.state["last_confirmed_user_message_hash"] = turn["message_sha256"]
        self.save()
        return {"status": status, "turn": turn, "session": self.state}

    def ingest(self, source, run, inline=False):
        if not re.fullmatch(r"BW-[a-f0-9]{32}", run):
            raise ValueError("INVALID_RUN_ID")
        turn = self.receipt(run)
        if not turn.get("reply_received"):
            raise ValueError("NO_CORRELATED_REPLY")
        source = Path(source)
        if source.stat().st_size > MAX_BYTES:
            raise ValueError("ARTIFACT_SIZE_LIMIT")
        raw = source.read_bytes()
        if not raw or len(raw) > MAX_BYTES:
            raise ValueError("ARTIFACT_SIZE_LIMIT")
        sha = digest(raw)
        folder = self.base / "artifacts" / run / sha
        folder.mkdir(parents=True, exist_ok=True)
        suffix = source.suffix.lower()
        saved = folder / ("source" + suffix)
        saved.write_bytes(raw)
        record = {"run_id": run, "sha256": sha, "size_bytes": len(raw), "received_at": stamp(),
                  "delivery": "INLINE" if inline else "LOCAL_FILE", "state": "DOWNLOADED", "errors": [], "files": []}
        rows = []
        files = [(saved, suffix)]
        if suffix == ".zip":
            files = []
            try:
                with zipfile.ZipFile(saved) as archive:
                    members = archive.infolist()
                    names = [item.filename for item in members]
                    if len(members) > 100 or sum(i.file_size for i in members) > MAX_BYTES or len(set(n.lower() for n in names)) != len(names):
                        raise ValueError("ZIP_LIMIT_OR_DUPLICATE_NAMES")
                    for item in members:
                        name = PurePosixPath(item.filename)
                        if name.as_posix() != item.filename.rstrip('/') or re.search(r'[<>"|?*\x00-\x1f]',item.filename):
                            raise ValueError("NON_CANONICAL_ZIP_MEMBER")
                        if name.is_absolute() or ".." in name.parts or "\\" in item.filename or ":" in item.filename or (item.external_attr >> 16) & 0o170000 == 0o120000:
                            raise ValueError("UNSAFE_ZIP_MEMBER")
                        if any(part.endswith((".", " ")) or re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?",part) for part in name.parts):
                            raise ValueError("UNSAFE_WINDOWS_ZIP_MEMBER")
                    for item in members:
                        if item.is_dir():
                            continue
                        dest = folder / "unpacked" / item.filename
                        dest.resolve().relative_to((folder / "unpacked").resolve())
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(archive.read(item))
                        files.append((dest, dest.suffix.lower()))
            except (ValueError, zipfile.BadZipFile, RuntimeError, OSError):
                record["errors"].append({"code": "ZIP_REJECTED"})
                files = []
        manifest = None
        for file, ext in files:
            entry = {"name": file.relative_to(folder).as_posix(), "sha256": digest(file.read_bytes())}
            try:
                text = file.read_text(encoding="utf-8-sig")
                parsed = parse_result(text, ext)
                if file.name == "manifest.json":
                    manifest = parsed["data"]
                else:
                    rows.extend(parsed["rows"])
                entry["parse_status"] = parsed["parse_status"]
                record["errors"].extend(parsed["errors"])
            except UnicodeError:
                entry["parse_status"] = "UNSUPPORTED_BINARY"
                record["errors"].append({"code": "UNSUPPORTED_BINARY"})
            record["files"].append(entry)
        record["state"] = "READ" if files else "DOWNLOADED"
        if suffix == ".zip":
            if not isinstance(manifest, dict) or manifest.get("run_id") != run:
                record["errors"].append({"code": "MANIFEST_BINDING_REQUIRED"})
            else:
                declarations = manifest.get("files")
                actual = {e["name"].removeprefix("unpacked/"): e["sha256"] for e in record["files"] if e["name"] != "unpacked/manifest.json"}
                if not isinstance(declarations, dict) or declarations != actual:
                    record["errors"].append({"code": "MANIFEST_FILE_HASH_MISMATCH"})
                if not {"summary.md"} <= actual.keys() or not ({"results.json", "results.csv"} & actual.keys()):
                    record["errors"].append({"code": "BUNDLE_REQUIRED_FILES_MISSING"})
        elif suffix == ".json":
            try:
                decoded=raw.decode("utf-8-sig")
                parsed = parse_result(decoded)
                if not isinstance(parsed["data"], dict) or parsed["data"].get("run_id") != run:
                    record["errors"].append({"code": "INLINE_BINDING_REQUIRED"})
                if inline and digest(decoded) != (turn.get("reply_sha256") or digest(turn.get("reply_text", ""))):
                    record["errors"].append({"code": "INLINE_REPLY_HASH_MISMATCH"})
            except UnicodeError:
                record["errors"].append({"code": "INLINE_ENCODING_INVALID"})
        else:
            record["errors"].append({"code": "UNBOUND_RESULT"})
        indexpath = self.base / "artifact-index.json"
        index = load(indexpath) if indexpath.exists() else {"bundles": [], "rows": []}
        record["duplicate_bundle"] = sha in index["bundles"]
        seen = set(index["rows"])
        unique = []
        for row in rows:
            key = digest(json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":")))
            if key not in seen:
                unique.append(row)
                seen.add(key)
        record.update(row_count=len(rows), new_row_count=len(unique), duplicate_row_count=len(rows)-len(unique))
        if not rows:
            record["errors"].append({"code": "NO_RESULT_ROWS"})
        if not record["errors"] and rows:
            record["state"] = "VALIDATED"
            index["bundles"] = sorted(set(index["bundles"] + [sha]))
            index["rows"] = sorted(seen)
            write(indexpath, index)
        write(folder / "rows.json", rows)
        write(folder / "new-rows.json", unique)
        write(folder / "receipt.json", record)
        return record

    def discover(self, observed):
        self.observation(observed)
        run = self.state["last_run_id"]
        turn = self.receipt(run)
        if not turn.get("reply_received"):
            raise ValueError("NO_CORRELATED_REPLY")
        reply_hash = turn.get("reply_sha256") or digest(turn["reply_text"])
        if observed.get("reply_sha256") != reply_hash:
            raise ValueError("ARTIFACT_REPLY_BINDING_REQUIRED")
        candidates = observed.get("artifacts", [])
        if not isinstance(candidates, list) or len(candidates) > 30:
            raise ValueError("ARTIFACT_DISCOVERY_LIMIT")
        entries = []
        rawpath = self.base / "artifacts" / run / "reply.raw.txt"
        parsed = parse_result(rawpath.read_text(encoding="utf-8")) if rawpath.exists() else parse_result(turn.get("reply_text", ""))
        declarations = parsed["data"].get("artifacts", []) if isinstance(parsed["data"], dict) else []
        if isinstance(declarations, list):
            entries = [{"name": v["name"], "state": "DECLARED"} for v in declarations if isinstance(v, dict) and isinstance(v.get("name"), str)]
        for item in candidates:
            if not isinstance(item, dict) or not item.get("name") or not item.get("target"):
                raise ValueError("ARTIFACT_LOCATOR_REQUIRED")
            entries = [v for v in entries if v["name"] != item["name"]]
            entries.append({"name": item["name"], "target": item["target"], "state": "VISIBLE",
                            "observed_at": observed["observed_at"], "reply_sha256": reply_hash})
        result = {"run_id": run, "provider": self.worker.get("provider", self.alias),
                  "policy": "INLINE_FALLBACK" if self.worker.get("provider", self.alias) == "muse" else "BUNDLE_FIRST",
                  "artifacts": entries, "primary": next((v for v in entries if v["state"] == "VISIBLE" and v["name"].lower().endswith(".zip")), next((v for v in entries if v["state"] == "VISIBLE"), None))}
        write(self.base / "artifacts" / run / "discovery.json", result)
        return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["prepare", "reconcile", "discover", "ingest", "capsule"])
    p.add_argument("--worker", required=True)
    p.add_argument("--workers", type=Path, default=ROOT / "workers.local.json")
    p.add_argument("--state-dir", type=Path, default=ROOT / "sessions.local")
    p.add_argument("--observation", type=Path)
    p.add_argument("--message")
    p.add_argument("--continue", dest="continuation", action="store_true")
    p.add_argument("--max-turns", type=int, choices=range(1, 21), default=6)
    p.add_argument("--source", type=Path)
    p.add_argument("--run-id")
    p.add_argument("--inline", action="store_true")
    args = p.parse_args()
    lock = None
    indexlock = None
    try:
        worker = load(args.workers)["workers"][args.worker]
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", args.worker):
            raise ValueError("INVALID_ALIAS")
        args.state_dir.mkdir(parents=True, exist_ok=True)
        lockpath = args.state_dir / (args.worker + ".lock")
        lock = os.open(lockpath, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        flow = Workflow(args.state_dir, args.worker, worker)
        if args.action == "prepare":
            if not args.message:
                raise ValueError("MESSAGE_REQUIRED")
            result = flow.prepare(args.message, load(args.observation), args.continuation, args.max_turns)
        elif args.action == "reconcile":
            result = flow.reconcile(load(args.observation))
        elif args.action == "ingest":
            indexpath=args.state_dir/'artifact-index.lock'
            indexlock=os.open(indexpath,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
            result = flow.ingest(args.source, args.run_id, args.inline)
        elif args.action == "discover":
            result = flow.discover(load(args.observation))
        else:
            capsule = load(args.source)
            if set(capsule) != {"goal", "constraints", "accepted_facts", "artifact_refs"}:
                raise ValueError("INVALID_CAPSULE")
            if len(json.dumps(capsule)) > 12000:
                raise ValueError("CAPSULE_TOO_LARGE")
            write(args.state_dir / (args.worker + ".capsule.json"), capsule)
            result = {"status": "CAPSULE_SAVED", "provenance": "COORDINATOR_SUPPLIED_REQUIRES_REVIEW"}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        code=str(error) if isinstance(error, ValueError) and re.fullmatch("[A-Z_]+",str(error)) else "WORKFLOW_INPUT_OR_STATE_ERROR"
        print(json.dumps({"status": code}))
        return 1
    finally:
        if indexlock is not None:
            os.close(indexlock)
            indexpath.unlink()
        if lock is not None:
            os.close(lock)
            lockpath.unlink()


if __name__ == "__main__":
    sys.exit(main())
