#!/usr/bin/env python3
"""Compare input bytes only to the preceding tree; never inherit its results."""
import argparse,json,pathlib,subprocess
from audit_natural_artifacts import TREE,HEAD,require
PREVIOUS_TREE='d2379b932cc976bb5347515887ecdfc4729ee70d'
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def entries(tree):
 out={}
 for item in subprocess.check_output(['git','ls-tree','-rz',tree],cwd=a.repo).split(b'\0'):
  if item:
   head,name=item.split(b'\t');out[name.decode()]=head.decode()
 return out
old,new=entries(PREVIOUS_TREE),entries(TREE);core=json.loads((pathlib.Path(__file__).parent/'source-input-result.json').read_bytes())
paths={x['path'] for x in core['inputs']}
paths.update(n for n in new if n.startswith(('app/src/main/','Paintroid/src/main/','colorpicker/src/main/')) and pathlib.PurePosixPath(n).suffix in ('.kt','.java','.c','.h','.cpp','.hpp'))
require(paths,'no compared source');require(all(new[n]==old.get(n) for n in paths),'installed/production input changed')
a.output.write_text(json.dumps({'status':'PASS_UNCHANGED_BYTES_ONLY','head':HEAD,'tree':TREE,'comparison_tree':PREVIOUS_TREE,'compared_paths':len(paths),'paths':sorted(paths),'limit':'Only confirms these input bytes/modes are unchanged. No result or acceptance from the previous tree is inherited; all current-source schedules, payload bindings and installed evidence must be independently recomputed.'},indent=2)+'\n');print('PASS',len(paths),'unchanged installed/production-code input blobs')
