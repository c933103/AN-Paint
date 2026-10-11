#!/usr/bin/env python3
"""Check canonical/private compiled parity and every bounded F01/C023 description."""
import argparse,hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--dump',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
def need(x,m):
 if not x:raise ValueError(m)
resources={};key=config=None
for line in a.dump.read_text().splitlines():
 m=re.match(r'^    resource \S+ (\S+)',line)
 if m:
  key=m[1];resources[key]={};config=None;continue
 m=re.match(r'^      \(([^)]*)\) (.*)',line)
 if m and key:
  config=m[1];need(config not in resources[key],f'Duplicate {key} {config}');resources[key][config]=m[2];continue
 if config is not None and key:
  resources[key][config]+='\n'+line
root=ET.parse(a.source/'Paintroid/src/main/res/values-b+ko+Kore+KR/strings.xml').getroot()
expected={n.tag+'/'+n.attrib['name'] for n in root}
canonical={k for k,v in resources.items() if 'b+ko+Kore+KR' in v}
private={k for k,v in resources.items() if 'b+ko+Kore+KR+anpaint' in v}
need(canonical==private==expected, 'Canonical/private compiled resource key union differs from XML')
for k in sorted(expected):need(resources[k]['b+ko+Kore+KR']==resources[k]['b+ko+Kore+KR+anpaint'], 'Compiled value mismatch '+k)
entries=json.loads((a.source/'tools/fixtures/tiff_size_wording_scope.json').read_text())['entries']
c023=json.loads((a.source/'tools/fixtures/tiff_c023_wording_scope.json').read_text())
entries+=c023['entries']
need(len(entries)==38,'Wrong original-plus-C023 entry count')
def config_for(folder):
 q=folder.removeprefix('values').lstrip('-')
 if q.startswith('b+'):
  parts=q[2:].split('+')
  if len(parts)==1:return parts[0]
  if len(parts)==2 and (len(parts[1])==2 or parts[1].isdigit()):return parts[0]+'-r'+parts[1]
 return q
observed=[]
for row in entries:
 folder=Path(row['path']).parent.name;config=config_for(folder)
 wanted=ET.fromstring(row['after']).text
 actual=resources['string/formats22_tiff_description'][config]
 need(actual=='"'+wanted+'"',f'Compiled TIFF mismatch {config}: {actual!r}')
 observed.append({'source':row['path'],'configuration':config,'value':wanted})
result={'dump_sha256':hashlib.sha256(a.dump.read_bytes()).hexdigest(),'canonical_private_resources':len(expected),'compiled_resource_keys':sorted(expected),'bounded_tiff_descriptions':observed,'tiff_count':len(observed),'result':'pass','limits':'Compiled resource identity only; not runtime layout, accessibility or linguistic acceptance.'}
a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('PASS:',len(expected),'canonical/private resources;',len(observed),'bounded TIFF descriptions')
