"""Opt-in anonymous online checks against the newest published Skill snapshot.

Run with Python 3.9+; optionally pass a complete release checkout directory.
All fixture installations and notification state are temporary. The 0.0.0
version is simulated; no historical release or real user choice is implied.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/agent-bridge-integration'
INSTALLED=(SKILL/'VERSION').read_text().strip()
SOURCE=json.loads((SKILL/'update-source.json').read_text())
EXPECTED=f"https://github.com/{SOURCE['repository']}/releases/tag/{SOURCE['tag_prefix']}{INSTALLED}"
checks=[]

def cli(script,state,*args):
    run=subprocess.run([sys.executable,'-B',str(script),'--state-dir',str(state),*args],capture_output=True,text=True,timeout=25)
    assert run.returncode==0, run.stderr
    return json.loads(run.stdout)

def summary(name,result):
    entry={'case':name,**{key:result[key] for key in ('status','notify','cached','installed_version','suppressed_by','reason') if key in result}}
    if 'latest' in result:
        entry['latest_version']=result['latest']['version']
        entry['release_url']=result['latest']['url']
        entry['release_notes_characters']=len(result['latest']['notes'])
    checks.append(entry)
    print(json.dumps(entry,ensure_ascii=False),flush=True)

with tempfile.TemporaryDirectory(prefix='agent-bridge-online-validation-') as directory:
    base=Path(directory)
    installation=base/'installation'
    shutil.copytree(ROOT,installation,ignore=shutil.ignore_patterns('.git','__pycache__'))
    skill=installation/'skills/agent-bridge-integration'
    script=skill/'scripts/check_updates.py'
    assert hashlib.sha256(script.read_bytes()).digest()==hashlib.sha256((ROOT/'skills/agent-bridge-integration/scripts/check_updates.py').read_bytes()).digest()
    current=cli(script,base/'current-state','check','--force')
    summary(f'installed_{INSTALLED}_live',current)
    assert current['status']=='up_to_date' and current['notify'] is False and current['cached'] is False
    again=cli(script,base/'current-state','check')
    summary(f'installed_{INSTALLED}_cached',again)
    assert again['status']=='up_to_date' and again['notify'] is False and again['cached'] is True
    # Only a disposable installation's version is changed. No historical 0.0.0 release is claimed.
    (skill/'VERSION').write_text('0.0.0\n')
    older=cli(script,base/'older-state','check','--force')
    summary('simulated_0.0.0_live',older)
    assert older['status']=='update_available' and older['notify'] is True and older['cached'] is False
    assert older['latest']['version']==INSTALLED and older['latest']['url']==EXPECTED
    assert '## 中文' in older['latest']['notes'] and '## English' in older['latest']['notes']
    assert older['latest']['notes_truncated'] is False
    acknowledgement=cli(script,base/'older-state','record','--version',INSTALLED,'--decision','notified','--notice-id',older['notice_id'])
    assert acknowledgement['status']=='recorded'
    repeated=cli(script,base/'older-state','check')
    summary('simulated_0.0.0_after_test_ack_cached',repeated)
    assert repeated['notify'] is False and repeated['suppressed_by']=='notified' and repeated['cached'] is True
    forced=cli(script,base/'older-state','check','--force')
    summary('simulated_0.0.0_after_test_ack_live',forced)
    assert forced['notify'] is False and forced['suppressed_by']=='notified' and forced['cached'] is False
    report={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'release_url':EXPECTED,'authentication':'none in checker','production_files_changed':False,
            'state':'temporary isolated directories; cleaned after test','old_installation':'0.0.0 is a disposable version fixture, not a published historical release',
            'checks':checks}
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
print('Online CLI verification passed; all isolated test installations and state directories were removed.',flush=True)
