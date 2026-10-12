if not __debug__:
 raise RuntimeError('Acceptance verification requires ordinary Python; optimized mode is rejected')
import hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).parent; C=R/'checkout'; sys.path.insert(0,str(C/'tools'))
import translation_catalogues as t
(R/'candidate-resources-verification.json').unlink(missing_ok=True)
text=(R/'candidate-resources.txt').read_text(); resources={}
for header,block in re.findall(r'^    resource \S+ (\S+)\n(.*?)(?=^    resource |^  type |\Z)',text,re.M|re.S):
 if not header.startswith('string/'):continue
 key=header.removeprefix('string/');resources[key]={}
 for qualifier,value in re.findall(r'^      \(([^)]*)\) (.*?)(?=^      \(|\Z)',block,re.M|re.S):
  value=value.rstrip('\n')
  if not(value.startswith('"') and value.endswith('"')):
   if re.fullmatch(r'@string/[A-Za-z0-9_]+',value):resources[key][qualifier]=value;continue
   raise ValueError((key,qualifier,value))
  assert qualifier not in resources[key],(key,qualifier)
  resources[key][qualifier]=value[1:-1].replace('\n      ','\n')
def android(s):
 if s.startswith('"') and s.endswith('"'):s=s[1:-1]
 return re.sub(r'\\([\\\'"@?nt])',lambda m:{'n':'\n','t':'\t'}.get(m[1],m[1]),s)
normalized={k:{t.resource_configuration('values'+('-'+q if q else '')):v for q,v in configs.items()} for k,configs in resources.items()}
metadata=[]
for path in sorted((C/'Paintroid/src/main/res').glob('values*/strings.xml')):
 values=t.read_strings(path); qualifier=t.resource_configuration(path.parent.name)
 if all(k in values for k in ['commons_metadata_http_error','commons_metadata_response_too_large']):
  for k in ['commons_metadata_http_error','commons_metadata_response_too_large']:
   assert normalized[k][qualifier]==android(values[k]),(path,k,normalized[k].get(qualifier),android(values[k]));metadata.append([qualifier,k])
assert len(metadata)==120
fixture=json.loads((C/'tools/fixtures/hungarian_attribution_c05_scope.json').read_text());keys=[x['key'] for x in fixture['entries']]+['commons_metadata_http_error','commons_metadata_response_too_large'];hu=t.read_strings(C/'Paintroid/src/main/res/values-hu/strings.xml')
assert len(keys)==len(set(keys))==19
for k in keys:
 assert 'hu' in resources[k],(k,resources[k])
 assert resources[k]['hu']==android(hu[k]),(k,resources[k]['hu'],android(hu[k]))
canonical={k:v['b+ko+Kore+KR'] for k,v in resources.items() if 'b+ko+Kore+KR' in v};generated={k:v['b+ko+Kore+KR+anpaint'] for k,v in resources.items() if 'b+ko+Kore+KR+anpaint' in v};assert canonical==generated;assert len(canonical)==len(t.read_strings(C/"Paintroid/src/main/res/values-b+ko+Kore+KR/strings.xml")),len(canonical)
out=dict(success=True,apk_sha256=hashlib.sha256((R/'candidate-app-debug.apk').read_bytes()).hexdigest(),dump_sha256=hashlib.sha256((R/'candidate-resources.txt').read_bytes()).hexdigest(),metadata_compiled_value_matches=len(metadata),catalogues=60,hungarian_scoped_value_matches=19,hungarian_keys=keys,mixed_korean_compiled_string_pairs=len(canonical),scope='Literal compiled APK strings vs exact source for two metadata keys and C05; full mixed Korean canonical/generated string equality. No independent linguistic acceptance.')
(R/'candidate-resources-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
