#!/usr/bin/env python3
"""Compare fresh native captures with the separately accepted e19 originals.

Byte equality permits reuse only of the recorded prior visual scope. It does
not turn all captures into individually inspected images or certify language.
"""
import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--fresh',type=pathlib.Path,required=True);p.add_argument('--prior',type=pathlib.Path,required=True);p.add_argument('--prior-review',type=pathlib.Path,required=True);p.add_argument('--binding',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def collect(root):
 paths=[]
 for name in ('commons-metadata-m04','commons-metadata-m04-diagnostic','commons-metadata-m04-painted-ink'):
  paths.extend((root/name).glob('*.png'))
 paths.extend((root/'localized-dialog-layout').glob('*retained-vertical*.png'))
 return {str(p.relative_to(root)):p for p in paths}
fresh,prior=collect(a.fresh),collect(a.prior)
if fresh.keys()!=prior.keys():raise ValueError('fresh image inventory differs: '+str(sorted(fresh.keys()^prior.keys())))
rows=[];different=[]
for name,p in sorted(fresh.items()):
 b=p.read_bytes();old=prior[name].read_bytes();row={'path':name,'bytes':len(b),'sha256':sha(b),'prior_sha256':sha(old),'identical':b==old};rows.append(row)
 if b!=old:different.append(row)
fringe=json.loads((a.prior_review/'fresh-fringe-disposition.json').read_text());target=[]
for item in fringe['inspected_images']:
 name=str(pathlib.PurePosixPath(item['path']).relative_to('Paintroid/build/reports'))
 row=next(r for r in rows if r['path']==name)
 if row['prior_sha256']!=item['sha256']:raise ValueError('prior inspected input changed')
 target.append(row)
notices=json.loads((a.prior_review/'notice-visual-byte-comparison.json').read_text());notice=[]
for item in notices['images']:
 row=next(r for r in rows if r['path']==item['path'])
 if row['prior_sha256']!=item['sha256']:raise ValueError('prior notice visual input changed')
 notice.append(row)
b=json.loads(a.binding.read_text());r={'current_run':b['run_id'],'current_head':b['head'],'current_tree':b['tree'],'prior_run':38299305241,'prior_head':'e19c766eb3eaedc1b3cd3657bb92864f81a9498a','compared_pngs':len(rows),'identical_pngs':len(rows)-len(different),'changed_images':different,'ordered_comparison_rows_sha256':sha(json.dumps(rows,sort_keys=True).encode()),'prior_inspected_fringe_images':target,'prior_notice_visual_scope':notices['scope'],'notice_images':notice,'scope_limits':['Comparison is of original PNG bytes, no resize/crop/normalization.','Only documented prior visual conclusions are reused; all-image equality does not claim all images were individually viewed.','Fresh JSON, pixel metrics, JUnit identities and phase bindings are independently checked.','Retained-notice oversized captions establish programmatic reader retention, not simultaneous full caption visibility or installed reachability.']}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('compared_pngs','identical_pngs','changed_images')},indent=2));raise SystemExit(0 if not different else 1)
