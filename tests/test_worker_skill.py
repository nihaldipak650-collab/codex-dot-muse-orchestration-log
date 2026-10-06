"""Alias/session wrapper integration over the same synthetic MCP server as runtime tests."""
import json, subprocess, tempfile, threading, unittest
from pathlib import Path
from test_runtime import FakeMCP, ThreadingHTTPServer, ROOT, URL

SCRIPT=ROOT/'skills/browser-worker/scripts/worker.py'
class WorkerSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.dir=Path(self.tmp.name)
        self.server=ThreadingHTTPServer(('127.0.0.1',0),FakeMCP)
        self.server.state={'scenario':'success','run_id':'SYNTHETIC','sent':False,'sends':0,'observations':0}
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.aliases=self.dir/'workers.local.json'
        self.aliases.write_text(json.dumps({'endpoint':f'http://127.0.0.1:{self.server.server_port}/mcp','workers':{'dot':{'url':URL}}}))
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.tmp.cleanup()
    def call(self,action,**kw):
        import sys
        cmd=[sys.executable,str(SCRIPT),action,'--worker',kw.get('worker','dot'),'--workers',str(self.aliases),'--state-dir',str(self.dir/'state'),'--timeout','3','--allow-example']
        if kw.get('message'):cmd+=['--message',kw['message']]
        if kw.get('max_turns'):cmd+=['--max-turns',str(kw['max_turns'])]
        if kw.get('transport'):cmd+=['--transport',kw['transport']]
        p=subprocess.run(cmd,capture_output=True,encoding='utf-8',errors='replace',timeout=45)
        self.assertTrue(p.stdout.strip(),p.stderr)
        data=json.loads(p.stdout);return data
    def test_alias_resolution_and_inspect_no_send(self):
        self.assertEqual('ALIAS_NOT_CONFIGURED',self.call('inspect',worker='absent')['status'])
        self.assertEqual('INSPECT_READY',self.call('inspect')['status'])
        self.assertEqual(0,self.server.state['sends'])
    def test_continue_same_thread_and_persistence(self):
        first=self.call('ask',message='Reply exactly: ACK {RUN_ID}')
        self.assertEqual('SUCCESS',first['status']);self.assertEqual(1,first['session']['turn_count'])
        second=self.call('continue',message='Reply exactly: ACK {RUN_ID}')
        self.assertEqual('SUCCESS',second['status'])
        self.assertEqual(first['session']['thread_binding'],second['session']['thread_binding'])
        self.assertEqual(2,self.server.state['sends']);self.assertEqual(2,second['session']['turn_count'])
        saved=json.loads((self.dir/'state/dot.json').read_text())
        self.assertEqual(second['session'],saved);self.assertNotIn(URL,json.dumps(saved))
        self.assertIsNotNone(saved['last_confirmed_user_message_hash']);self.assertIsNotNone(saved['last_correlated_reply_hash'])
    def test_collect_no_resend_and_pending_resume(self):
        self.server.state['scenario']='no_reply'
        first=self.call('ask',message='Reply exactly: ACK {RUN_ID}')
        self.assertEqual('REPLY_TIMEOUT',first['status']);self.assertTrue(first['session']['pending'])
        context=self.dir/'state/runs'/(first['session']['last_run_id']+'.context.json')
        self.assertNotIn(URL,context.read_text());self.assertNotIn('old prompt',context.read_text())
        self.server.state['scenario']='success'
        collected=self.call('collect')
        self.assertEqual('SUCCESS',collected['status']);self.assertFalse(collected['session']['pending'])
        self.assertEqual(1,self.server.state['sends'])
        self.assertEqual(first['session']['last_run_id'],collected['session']['last_run_id'])
        self.assertEqual('NOT_PENDING',self.call('collect')['status']);self.assertEqual(1,self.server.state['sends'])
    def test_unknown_delivery_cannot_replay(self):
        self.server.state['scenario']='uncertain_send'
        first=self.call('ask',message='Reply exactly: ACK {RUN_ID}')
        self.assertEqual('DELIVERY_UNKNOWN',first['status']);self.assertTrue(first['session']['pending'])
        self.assertEqual('PENDING_OR_DELIVERY_UNKNOWN_NO_RESEND',self.call('continue',message='retry')['status'])
        self.assertEqual('PENDING_OR_DELIVERY_UNKNOWN_NO_RESEND',self.call('ask',message='retry')['status'])
        self.assertEqual(1,self.server.state['sends'])
    def test_max_turns(self):
        self.assertEqual('SUCCESS',self.call('ask',message='Reply exactly: ACK {RUN_ID}',max_turns=1)['status'])
        self.assertEqual('MAX_TURNS',self.call('continue',message='one more',max_turns=1)['status'])
        self.assertEqual(1,self.server.state['sends'])
    def test_collect_reconciles_uncertain_enter_from_real_receipt(self):
        self.server.state['scenario']='uncertain_send'
        first=self.call('ask',message='Reply exactly: ACK {RUN_ID}')
        self.assertEqual('DELIVERY_UNKNOWN',first['status'])
        self.assertFalse(first['result']['submitted'])
        self.server.state['scenario']='success'
        recovered=self.call('collect')
        self.assertEqual('SUCCESS',recovered['status'])
        for key in ['filled','submitted','visible_as_user_message','submit_confirmed','reply_received']:
            self.assertTrue(recovered['result'][key])
        self.assertEqual(1,self.server.state['sends'])
    def test_thread_binding_mismatch(self):
        self.call('ask',message='Reply exactly: ACK {RUN_ID}')
        changed=json.loads(self.aliases.read_text());changed['workers']['dot']['url']='https://worker.example/conversation/other';self.aliases.write_text(json.dumps(changed))
        self.assertEqual('THREAD_BINDING_MISMATCH',self.call('continue',message='next')['status'])
        self.assertEqual(1,self.server.state['sends'])

    def test_registered_to_standalone_pending_and_late_artifact_receipt(self):
        import sys
        sys.path.insert(0,str(ROOT/'runtime'))
        from workflow import Workflow
        self.call('ask',message='Reply exactly: ACK {RUN_ID}')
        statepath=self.dir/'state/dot.json'
        state=json.loads(statepath.read_text());state['transport']='registered';statepath.write_text(json.dumps(state))
        self.server.state['scenario']='no_reply'
        pending=self.call('continue',message='Reply exactly: ACK {RUN_ID}')
        self.assertEqual('REPLY_TIMEOUT',pending['status'])
        self.assertEqual('standalone',pending['session']['transport'])
        self.assertEqual('STANDALONE_PENDING_USE_STANDALONE_COLLECT',self.call('collect',transport='registered')['status'])
        self.server.state['scenario']='success'
        resolved=self.call('collect')
        self.assertEqual('SUCCESS',resolved['status'])
        original=pending['session']['last_run_id']
        flow=Workflow(self.dir/'state','dot',{'url':URL})
        self.assertTrue(flow.receipt(original)['reply_received'])
        self.assertNotEqual(original,resolved['session']['receipt_runs'][original])
        self.assertEqual(2,self.server.state['sends'])

if __name__=='__main__':unittest.main()
