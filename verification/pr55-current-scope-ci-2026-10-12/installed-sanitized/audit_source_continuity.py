#!/usr/bin/env python3
"""Bound the successor's deliberate changes; no previous acceptance carries forward."""
import argparse,json,pathlib,subprocess
from audit_natural_artifacts import TREE,HEAD,require
PREVIOUS_TREE='dc1ba97dacc573ead73729297eb739ecb244dcf5'
EXPECTED_CHANGED={'AGENTS.md','README.md','TRANSLATING.md'}
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def entries(tree):
 out={}
 for item in subprocess.check_output(['git','ls-tree','-rz',tree],cwd=a.repo).split(b'\0'):
  if item:
   head,name=item.split(b'\t');out[name.decode()]=head.decode()
 return out
old,new=entries(PREVIOUS_TREE),entries(TREE);require(set(old)==set(new),'successor source leaf inventory changed')
changed={n for n in new if new[n]!=old[n]};require(changed==EXPECTED_CHANGED,'successor source change scope differs')
core=json.loads((pathlib.Path(__file__).parent/'source-input-result.json').read_bytes());paths={x['path'] for x in core['inputs']}
paths.update(n for n in new if n.startswith(('app/src/main/','Paintroid/src/main/','colorpicker/src/main/')) and pathlib.PurePosixPath(n).suffix in ('.kt','.java','.c','.h','.cpp','.hpp'))
require(paths,'no compared source')
a.output.write_text(json.dumps({'status':'PASS_EXACT_THREE_PATH_SUCCESSOR_CHANGE_SCOPE','head':HEAD,'tree':TREE,'comparison_tree':PREVIOUS_TREE,'changed_paths':sorted(changed),'compared_paths':len(paths),'unchanged_review_input_paths':sorted(paths-changed),'changed_review_input_paths':sorted(paths&changed),'limit':'Only records exact source changes and unchanged bytes/modes. No result or acceptance from the previous tree is inherited; all current-source schedules, payload bindings and installed evidence must be independently recomputed.'},indent=2)+'\n');print('PASS',len(changed),'deliberate changed source paths;',len(paths-changed),'unchanged review inputs')
