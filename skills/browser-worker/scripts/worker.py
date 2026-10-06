"""Four bounded actions over the existing PowerShell runtime; no transport implementation."""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def now():return datetime.now(timezone.utc).isoformat()
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def save(path,data):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');os.replace(tmp,path)
def worker_next(text):
    try:
        data=json.loads(text.strip().removeprefix('```json').removesuffix('```').strip())
        return data.get('state') if data.get('state') in ('CONTINUE','NEED_CONTEXT','BLOCKED','DONE') else 'UNSTRUCTURED'
    except (ValueError,AttributeError):return 'UNSTRUCTURED'
def invoke(args):
    aliases=json.loads(args.workers.read_text(encoding='utf-8-sig'))
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,40}',args.worker):raise ValueError('INVALID_ALIAS')
    worker=aliases['workers'].get(args.worker)
    if not worker or not worker.get('url') or '.example' in worker['url'] and not args.allow_example:raise ValueError('ALIAS_NOT_CONFIGURED')
    binding=sha(worker['url'])
    args.state_dir.mkdir(parents=True,exist_ok=True)
    path=args.state_dir/(args.worker+'.json');lock=path.with_suffix('.lock')
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.close(fd)
    try:
        state=json.loads(path.read_text()) if path.exists() else {'worker_alias':args.worker,'safe_worker_id':binding,'thread_binding':binding,'last_run_id':None,'last_confirmed_user_message_hash':None,'last_correlated_reply_hash':None,'pending':False,'last_status':'NEW','updated_at':now(),'turn_count':0,'next_state':'UNSTRUCTURED'}
        if state['thread_binding']!=binding:raise ValueError('THREAD_BINDING_MISMATCH')
        if args.action in ('ask','continue'):
            if state['pending']:raise ValueError('PENDING_OR_DELIVERY_UNKNOWN_NO_RESEND')
            if state['turn_count']>=args.max_turns:raise ValueError('MAX_TURNS')
            if args.action=='continue' and (not state['last_run_id'] or state['last_status']!='SUCCESS'):raise ValueError('NO_CONFIRMED_PREVIOUS_TURN')
            if not args.message:raise ValueError('MESSAGE_REQUIRED')
        if args.action=='collect' and not state['pending']:
            return {'action':'collect','status':'NOT_PENDING','session':state}
        if args.action=='collect' and not state['last_run_id']:raise ValueError('NO_PENDING_RUN')
        ps=os.environ.get('RUNTIME_POWERSHELL') or shutil.which('pwsh')
        if not ps:raise ValueError('POWERSHELL_REQUIRED')
        run='BW-'+uuid.uuid4().hex
        runs=args.state_dir/'runs';runs.mkdir(exist_ok=True)
        cmd=[ps,'-NoProfile','-File',str(ROOT/'runtime/single_worker_v0.ps1'),'-WorkerUrl',worker['url'],'-Endpoint',worker.get('endpoint',aliases.get('endpoint','http://localhost:8931/mcp')),'-RunId',run,'-OutputDirectory',str(runs),'-Timeout',str(args.timeout)]
        if worker.get('config'):
            cfg=Path(worker['config']);cfg=cfg if cfg.is_absolute() else args.workers.parent/cfg
            cmd+=['-Config',str(cfg)]
        if args.action=='inspect':cmd+=['-Inspect']
        elif args.action=='collect':
            context=runs/(state['last_run_id']+'.context.json')
            if not context.exists():raise ValueError('NO_COLLECTION_CONTEXT_RECONCILE_MANUALLY')
            cmd+=['-Collect','-ContextFile',str(context)]
        else:
            message='RUN_ID='+run+'\nInclude this RUN_ID in your reply.\n'+args.message.replace('{RUN_ID}',run)
            cmd+=['-Message',message]
            state.update(last_run_id=run,pending=True,last_status='IN_FLIGHT',turn_count=state['turn_count']+1,updated_at=now())
            save(path,state) # Durable reservation before any possible send.
        try:
            proc=subprocess.run(cmd,capture_output=True,encoding='utf-8',errors='replace',timeout=args.timeout+120)
            result_path=runs/(run+'.json')
            if not result_path.exists():raise ValueError('RUNTIME_RESULT_MISSING')
            result=json.loads(result_path.read_text(encoding='utf-8-sig'))
        except subprocess.TimeoutExpired:
            # Never replay: invocation may have crossed the submission boundary.
            if args.action!='inspect':state.update(last_status='UNKNOWN',updated_at=now());save(path,state)
            raise ValueError('UNKNOWN_RUNTIME_TIMEOUT_NO_REPLAY')
        status=result['final_status']
        if args.action!='inspect':
            state['last_status']=status
            state['pending']=status!='SUCCESS' and (result['filled'] or result['submitted'] or status in ('DELIVERY_UNKNOWN','REPLY_TIMEOUT') or args.action=='collect')
            if result['submit_confirmed']:state['last_confirmed_user_message_hash']=result['message_sha256']
            if result['reply_received']:
                state['last_correlated_reply_hash']=sha(result['reply_text']);state['next_state']=worker_next(result['reply_text'])
            state['updated_at']=now();save(path,state)
        return {'action':args.action,'status':status,'session':state,'result':result,'runtime_exit':proc.returncode}
    finally:lock.unlink()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['inspect','ask','continue','collect']);p.add_argument('--worker',required=True)
    p.add_argument('--workers',type=Path,default=ROOT/'workers.local.json')
    p.add_argument('--state-dir',type=Path,default=ROOT/'sessions.local')
    p.add_argument('--message');p.add_argument('--timeout',type=int,default=10);p.add_argument('--max-turns',type=int,default=6)
    p.add_argument('--allow-example',action='store_true',help='permit synthetic example host for local tests only')
    args=p.parse_args()
    if not 1<=args.max_turns<=20 or not 1<=args.timeout<=300:p.error('bounds: max-turns 1..20; timeout 1..300')
    try:
        result=invoke(args);print(json.dumps(result,ensure_ascii=False));return 0 if result['status'] in ('SUCCESS','INSPECT_READY','NOT_PENDING') else 1
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as error:
        # Error code only, never raw exception text containing worker paths/URLs.
        code=str(error) if isinstance(error,ValueError) and re.fullmatch('[A-Z_]+',str(error)) else 'LOCAL_STATE_OR_CONFIG_ERROR'
        print(json.dumps({'status':code}));return 1
if __name__=='__main__':sys.exit(main())
