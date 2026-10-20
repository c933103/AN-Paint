import json, collections, re, pathlib, xml.etree.ElementTree as ET, hashlib
root=pathlib.Path('/tmp/swedish-independent-full-review');receipt=json.loads((root/'independent-review.json').read_text())
base=pathlib.Path('/tmp/an-audit-release039/AN-Paint/Paintroid/src/main/res');work=pathlib.Path('/tmp/an-swedish-complete/Paintroid/src/main/res')
def catalogue(path):
 out={}
 for e in ET.parse(path).getroot():
  if e.tag not in ['string','plurals'] or e.get('translatable')=='false':continue
  key=e.tag+'/'+e.attrib['name'];assert key not in out,key
  value={q.attrib['quantity']:q.text or '' for q in e} if e.tag=='plurals' else ''.join(e.itertext())
  out[key]=(value,e.attrib)
 return out
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
en=catalogue(base/'values/strings.xml');old=catalogue(base/'values-sv/strings.xml');sv=catalogue(work/'values-sv/strings.xml')
assert len(receipt['entries'])==717 and set(en)=={r['identity'] for r in receipt['entries']}
pattern=re.compile(r'%\d+\$[-+ #0,(]*\d*(?:\.\d+)?[a-zA-Z]')
accepted=0;retained=0;nonheld=0
for r in receipt['entries']:
 key=r['identity'];assert r['english']==en[key][0] and r['source_attributes']==en[key][1],key
 assert r['english_sha256']==digest(r['english']) and r['swedish_sha256']==digest(r['swedish']),key
 if r['decision'].startswith('held_'):continue
 nonheld+=1;assert sv[key][0]==r['swedish'],key
 if r['decision']=='retained_prior_exact_not_rereviewed':
  retained+=1;assert sv[key]==old[key],key;continue
 accepted+=1
 assert sv[key][1]==en[key][1],(key,sv[key][1],en[key][1])
 a,b=r['english'],r['swedish'];pairs=[(a[q],b[q]) for q in a] if isinstance(a,dict) else [(a,b)]
 if isinstance(a,dict):assert set(a)==set(b)=={'one','other'}
 for source,target in pairs:
  assert collections.Counter(pattern.findall(source))==collections.Counter(pattern.findall(target)),key
  assert source.count(r'\n')==target.count(r'\n'),key
  if source.startswith('@string/'):assert target==source,key
assert (accepted,retained,nonheld)==(373,340,713)
print('PASS: all 717 typed identities and full English values bound to released e50de18d.')
print('PASS: 373 newly accepted full targets and 340 retained prior targets exactly match application snapshot.')
print('PASS: newly accepted attributes, positional format contracts, plural quantities, newlines and aliases.')
print('PASS: all 340 prior pairs and resource attributes remain unchanged.')
print('NOT TESTED: build, CI, installed layout, clipping, TalkBack, device/runtime behavior or native-speaker fluency.')
