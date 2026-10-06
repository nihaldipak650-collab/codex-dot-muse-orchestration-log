"""Stdlib fake MCP end-to-end tests. No worker accounts or Playwright installation needed."""
import json, os, shutil, subprocess, tempfile, threading, unittest
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PS=os.environ.get('RUNTIME_POWERSHELL') or shutil.which('pwsh') or shutil.which('powershell')
URL='https://worker.example/conversation/demo'

class FakeMCP(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_POST(self):
        rpc=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        method=rpc['method']; state=self.server.state
        if method=='notifications/initialized':
            self.send_response(202);self.end_headers();return
        result={}
        if method=='initialize':result={'protocolVersion':'2025-03-26','serverInfo':{'name':'synthetic-test','version':'1'}}
        elif method=='tools/list':
            ref=state['scenario'] in ('ref_success','ref_opened')
            key='ref' if ref else 'target'
            tabprops={'action':{'type':'string'},'index':{'type':'number'}}
            if not ref:tabprops['url']={'type':'string'}
            typeprops={key:{'type':'string'},'text':{'type':'string'},'submit':{'type':'boolean'},'element':{'type':'string'}}
            result={'tools':[
                {'name':'browser_type','inputSchema':{'properties':typeprops}},
                {'name':'browser_tabs','inputSchema':{'properties':tabprops}},
            ]}
        elif method=='tools/call':
            name=rpc['params']['name'];args=rpc['params']['arguments'];scenario=state['scenario']
            text='OK'
            if scenario=='control_down':
                self.send_response(503);self.end_headers();return
            if name=='browser_tabs':
                if scenario=='approval':result={'isError':True,'content':[{'type':'text','text':'Welcome: approval required'}]}
                elif args['action']=='new':
                    if scenario=='ref_opened' and 'url' in args:result={'isError':True,'content':[{'type':'text','text':'url not allowed'}]}
                    else:state['opened']=True
                elif args['action']=='list':
                    text='### Open tabs\n- 0: Worker ('+URL+')' if scenario not in ('tab_opened','ref_opened') or state.get('opened') else '### Open tabs\nNo open tabs'
            elif name=='browser_snapshot':text='### Snapshot\n- textbox "Message" [ref=e12]'
            elif name=='browser_type':
                expected='ref' if scenario in ('ref_success','ref_opened') else 'target'
                if expected not in args:
                    result={'isError':True,'content':[{'type':'text','text':'required composer argument absent'}]}
                else:state['message']=args['text'];state['filled']=True
            elif name=='browser_press_key':
                state['sends']+=1
                if scenario!='draft':state['sent']=True
                if scenario=='uncertain_send':
                    self.send_response(503);self.end_headers();return
            elif name=='browser_evaluate':
                state['observations']+=1
                run=state.get('message','').split('RUN_ID=')[-1].splitlines()[0] if state.get('message') else 'OLD'
                old='ACK '+state['run_id'] if scenario=='old_reply' else 'ACK OLD'
                users=['old prompt'];assistants=[old]
                if state['sent']:users.append(state['message'])
                if state['sent'] and scenario not in ('no_reply','old_reply','draft'):
                    reply=('Completed '+run+'\n'+URL+'\nAuthorization: Bearer synthetic-secret') if scenario=='redaction' else 'ACK '+run
                    assistants.append(reply)
                ob={'users':users,'assistants':assistants,'generating':False,'completion':scenario=='redaction','observed_at':datetime.now(timezone.utc).isoformat()}
                text='### Result\n'+json.dumps(ob)+'\n### Ran Playwright code\n(synthetic)'
            if not result:result={'content':[{'type':'text','text':text}]}
        wire={'jsonrpc':'2.0','id':rpc.get('id'),'result':result}
        if state['scenario']=='progress_on_fill' and method=='tools/call' and rpc['params']['name']=='browser_type':
            wire={'jsonrpc':'2.0','method':'notifications/progress','params':{'progress':1}}
        payload=json.dumps(wire).encode()
        sse=state['scenario']=='sse_success'
        if sse:payload=b': heartbeat\n\nevent: message\ndata: '+payload+b'\n\n'
        self.send_response(200);self.send_header('Content-Type','text/event-stream' if sse else 'application/json');self.send_header('Mcp-Session-Id','synthetic-only');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)

class RuntimeTests(unittest.TestCase):
    def run_case(self,scenario,expected):
        server=ThreadingHTTPServer(('127.0.0.1',0),FakeMCP)
        run='TEST-'+scenario.replace('_','-')
        server.state={'scenario':scenario,'run_id':run,'sent':False,'sends':0,'observations':0}
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as out:
                command=[PS,'-NoProfile','-File',str(ROOT/'runtime/single_worker_v0.ps1'),'-Endpoint',f'http://127.0.0.1:{server.server_port}/mcp','-WorkerUrl',URL,'-RunId',run,'-Message',f'RUN_ID={run}\nReply exactly:\nACK {run}','-Timeout','3','-OutputDirectory',out]
                if scenario=='sse_success':
                    aliases={'-Endpoint':'--endpoint','-WorkerUrl':'--worker-url','-Message':'--message','-Timeout':'--timeout'}
                    command=[aliases.get(x,x) for x in command]
                if scenario=='redaction':
                    cfg=Path(out)/'worker.local.json';cfg.write_text(json.dumps({'completion':'#done'}))
                    command+=['-Config',str(cfg)]
                proc=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=40)
                path=Path(out)/(run+'.json')
                self.assertTrue(path.exists(),proc.stderr)
                data=json.loads(path.read_text(encoding='utf-8-sig'))
                self.assertEqual(expected,data['final_status'],proc.stderr)
                summary=json.loads(proc.stdout.strip())
                self.assertEqual(expected,summary['final_status'])
                self.assertEqual(run,summary['run_id'])
                self.assertEqual(proc.returncode,0 if expected=='SUCCESS' else 1,proc.stderr)
                self.assertNotIn(URL,path.read_text())
                for key in ['run_id','started_at','finished_at','endpoint','preflight_status','tab_status','message_sha256','filled','submit_confirmed','reply_received','reply_text','timestamps','errors']:
                    self.assertIn(key,data)
                schema=json.loads((ROOT/'schemas/runtime-result.schema.json').read_text())
                self.assertEqual(set(schema['required']),set(data))
                self.assertIn(data['final_status'],schema['properties']['final_status']['enum'])
                if expected=='SUCCESS':
                    for key in ['filled','submitted','visible_as_user_message','submit_confirmed','reply_received']:self.assertIs(data[key],True)
                    if scenario=='redaction':
                        self.assertIn('[REDACTED_WORKER_URL]',data['reply_text'])
                        self.assertNotIn('synthetic-secret',data['reply_text'])
                    else:self.assertEqual('ACK '+run,data['reply_text'])
                if scenario in ('tab_opened','ref_opened'):self.assertEqual('TAB_OPENED',data['tab_status'])
                sends=server.state['sends']
                self.assertLessEqual(sends,1)
                if scenario=='progress_on_fill':self.assertEqual(0,sends)
                again=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=10)
                self.assertNotEqual(again.returncode,0)
                self.assertEqual(sends,server.state['sends'])
                self.assertEqual(data,json.loads(path.read_text(encoding='utf-8-sig')))
        finally:server.shutdown();server.server_close();thread.join()
    def test_success(self):self.run_case('success','SUCCESS')
    def test_control_down(self):self.run_case('control_down','CONTROL_DOWN')
    def test_draft_b06(self):self.run_case('draft','DELIVERY_UNKNOWN')
    def test_submitted_timeout(self):self.run_case('no_reply','REPLY_TIMEOUT')
    def test_old_reply_correlation(self):self.run_case('old_reply','REPLY_TIMEOUT')
    def test_uncertain_send_not_replayed(self):self.run_case('uncertain_send','DELIVERY_UNKNOWN')
    def test_human_approval(self):self.run_case('approval','HUMAN_APPROVAL_REQUIRED')
    def test_sse_transport(self):self.run_case('sse_success','SUCCESS')
    def test_open_missing_tab(self):self.run_case('tab_opened','SUCCESS')
    def test_standard_snapshot_ref(self):self.run_case('ref_success','SUCCESS')
    def test_standard_open_tab(self):self.run_case('ref_opened','SUCCESS')
    def test_private_url_reply_redaction(self):self.run_case('redaction','SUCCESS')
    def test_progress_notification_is_not_fill_receipt(self):self.run_case('progress_on_fill','DELIVERY_UNKNOWN')

if __name__=='__main__':
    if not PS:raise SystemExit('Install PowerShell or set RUNTIME_POWERSHELL')
    unittest.main()
