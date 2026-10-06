"""Generate private registered-tool snippets; this script does not control a browser."""
import argparse
import json
import uuid
from pathlib import Path
from workflow import ROOT, digest, load, write


def observation_code(worker, run=None):
    selectors = worker.get("selectors")
    required = {"users", "assistants", "generating"}
    if not isinstance(selectors, dict) or not required <= selectors.keys() or not all(selectors[k] for k in required):
        raise ValueError("VALIDATED_PROVIDER_SELECTORS_REQUIRED")
    config = json.dumps({"url": worker["url"], "selectors": selectors, "run": run})
    return """async () => {
      const c=CONFIG;
      if(location.href !== c.url) throw new Error('WRONG_THREAD');
      const hash=async t=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t)))).map(v=>v.toString(16).padStart(2,'0')).join('');
      const read=s=>Array.from(document.querySelectorAll(s)).map(n=>n.innerText||n.textContent||'');
      const users=read(c.selectors.users), assistants=read(c.selectors.assistants);
      const nodes=Array.from(document.querySelectorAll(c.selectors.assistants));
      const correlated=c.run ? nodes.filter(n=>(n.innerText||n.textContent||'').includes(c.run)) : [];
      const reply=correlated.length===1 ? correlated[0] : null;
      const artifacts=reply ? Array.from(reply.querySelectorAll(c.selectors.artifacts||'a[download]')).map((n,i)=>({name:n.getAttribute('download')||n.textContent.trim(),target:c.selectors.assistants+' >> nth='+nodes.indexOf(reply)+' >> '+(c.selectors.artifacts||'a[download]')+' >> nth='+i})) : [];
      return {url_sha256:await hash(location.href),observed_at:new Date().toISOString(),users,assistants,generating:!!document.querySelector(c.selectors.generating),completion:c.selectors.completion?!!document.querySelector(c.selectors.completion):false,reply_sha256:reply?await hash(reply.innerText||reply.textContent||''):null,artifacts};
    }""".replace("CONFIG", config)


def download_code(worker, target, destination):
    # Fixed destination supplied by coordinator, never download.suggestedFilename().
    return """async (page) => {
      if(page.url() !== URL) throw new Error('WRONG_THREAD');
      const locator=page.locator(TARGET);
      if(await locator.count() !== 1) throw new Error('ARTIFACT_AMBIGUOUS');
      const waiting=page.waitForEvent('download',{timeout:20000});
      const [download]=await Promise.all([waiting,locator.click({timeout:10000})]);
      await download.saveAs(DESTINATION);
      const failure=await download.failure();
      return {download_event:true,save_completed:!failure,local_path:DESTINATION};
    }""".replace("URL", json.dumps(worker["url"])).replace("TARGET", json.dumps(target)).replace("DESTINATION", json.dumps(str(destination)))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--worker',required=True)
    p.add_argument('--workers',type=Path,default=ROOT/'workers.local.json')
    p.add_argument('--state-dir',type=Path,default=ROOT/'sessions.local')
    p.add_argument('--run-id')
    p.add_argument('--target',help='Fresh verified unique selector from correlated artifact discovery')
    p.add_argument('--extension',choices=['zip','json','csv','md'],default='zip')
    a=p.parse_args()
    worker=load(a.workers)['workers'][a.worker]
    output={'observation_function':observation_code(worker,a.run_id),'thread_binding':digest(worker['url'])}
    if a.target:
        dest=(a.state_dir/'downloads'/('download-'+uuid.uuid4().hex+'.'+a.extension)).resolve()
        dest.parent.mkdir(parents=True,exist_ok=True)
        output['download_code']=download_code(worker,a.target,dest)
        output['destination']=str(dest)
    path=a.state_dir/'browser-plan.local.json'
    write(path,output)
    print(json.dumps({'status':'PLAN_SAVED','path':str(path)}))


if __name__=='__main__':main()
