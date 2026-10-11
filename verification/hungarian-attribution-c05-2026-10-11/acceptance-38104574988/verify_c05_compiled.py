import pathlib,json,re,xml.etree.ElementTree as E,argparse
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--dump',type=pathlib.Path,required=True);a=p.parse_args()
src=a.source;raw=a.dump.read_text();resources={};key=config=None
wanted_keys={'string/'+r['key'] for r in json.loads((src/'tools/fixtures/hungarian_attribution_c05_scope.json').read_text())['entries']}
for line in raw.splitlines():
 m=re.match(r'^    resource \S+ (\S+)',line)
 if m:
  key=m[1];resources[key]={};config=None;continue
 m=re.match(r'^      \(([^)]*)\) (.*)',line)
 if m and key:
  config=m[1];resources[key][config]=m[2];continue
 if key in wanted_keys and config == 'hu':
  if line and not line.startswith('      '):raise ValueError('Unexpected AAPT continuation indentation')
  resources[key][config]+='\n'+(line[6:] if line else '')
f=json.loads((src/'tools/fixtures/hungarian_attribution_c05_scope.json').read_text());observed=[]
for row in f['entries']:
 expected=E.fromstring(row['after']).text.replace('\\n','\n')
 actual=resources['string/'+row['key']]['hu']
 if actual != '"'+expected+'"':print('DIFF',row['key'],repr(actual[:90]),repr(('"'+expected+'"')[:90]))
 observed.append({'id':row['id'],'key':row['key'],'compiled_hu_present':True,'no_financial_credit_root':'jóváírás' not in actual.lower(),'exact_dump_matches_source':actual=='"'+expected+'"'})
if not all(x['compiled_hu_present'] and x['no_financial_credit_root'] and x['exact_dump_matches_source'] for x in observed):raise ValueError('Compiled C05 mismatch')
pathlib.Path('c05-compiled-resource-receipt.json').write_text(json.dumps({'head':'826eeaa9f4c2960eca3958ae63d673e4d87fe05a','observed':observed,'limits':'Exact compiled resource check only; no text-fit or linguistic acceptance.'},ensure_ascii=False,indent=2)+'\n')
print('Verified all 17 exact compiled Hungarian replacements')
