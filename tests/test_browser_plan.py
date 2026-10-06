"""Registered snippet contracts against a synthetic Playwright-shaped surface."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from browser_plan import download_code, observation_code


@unittest.skipUnless(shutil.which('node'),'Node needed only to verify generated JavaScript')
class BrowserPlanTests(unittest.TestCase):
    def execute(self, source):
        return subprocess.run(['node','-e',source],capture_output=True,text=True,timeout=10)

    def test_download_event_saves_real_local_bytes_to_fixed_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            destination=Path(directory)/'fixed.zip'
            worker={'url':'https://worker.example/thread/a'}
            code=download_code(worker,'a >> nth=0',destination)
            source="""const fs=require('fs'); let clicked=0,events=0;
            const page={url:()=>URL, locator:()=>({count:async()=>1,click:async()=>{clicked++;}}),
            waitForEvent:async name=>{events++;return {saveAs:async p=>fs.writeFileSync(p,'bundle-bytes'),failure:async()=>null};}};
            (FUNCTION)(page).then(r=>{if(clicked!==1||events!==1||!r.save_completed)process.exit(2);}).catch(e=>{console.error(e);process.exit(1)});
            """.replace('URL',json.dumps(worker['url'])).replace('FUNCTION',code)
            proc=self.execute(source)
            self.assertEqual(0,proc.returncode,proc.stderr)
            self.assertEqual(b'bundle-bytes',destination.read_bytes())

    def test_wrong_thread_and_ambiguous_target_never_click(self):
        code=download_code({'url':'https://worker.example/a'},'a',Path('fixed.zip'))
        for url,count in [('https://worker.example/b',1),('https://worker.example/a',2)]:
            source="""let clicked=0; const page={url:()=>URL,locator:()=>({count:async()=>COUNT,click:async()=>{clicked++}})};
            (FUNCTION)(page).then(()=>process.exit(2)).catch(()=>{if(clicked)process.exit(3)});
            """.replace('URL',json.dumps(url)).replace('COUNT',str(count)).replace('FUNCTION',code)
            self.assertEqual(0,self.execute(source).returncode)

    def test_observation_requires_validated_selector_contract_and_exact_url(self):
        with self.assertRaisesRegex(ValueError,'SELECTORS_REQUIRED'):
            observation_code({'url':'https://worker.example/a'})
        code=observation_code({'url':'https://worker.example/a','selectors':{'users':'.user','assistants':'.reply','generating':'.stop'}})
        source="const location={href:'https://worker.example/wrong'}; (FUNCTION)().then(()=>process.exit(2)).catch(()=>{});".replace('FUNCTION',code)
        self.assertEqual(0,self.execute(source).returncode)


if __name__=='__main__':unittest.main()
