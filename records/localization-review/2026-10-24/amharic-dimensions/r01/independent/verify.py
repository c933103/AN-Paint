#!/usr/bin/env python3
"""Independent read-only checks of the sealed dimension translation dossier."""
import ast, hashlib, json, pathlib, re, sys, xml.etree.ElementTree as ET
ROOT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/scratch/bbca2890f602/amharic-dimensions-draft-20261024')
OUT=pathlib.Path(__file__).parent
EXPECTED='830cf544de5bd76f85e4117484a2f9d97b18f8a92d36a0a0078cc706d894de3e'
def sha(x): return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def read(p): return json.loads((ROOT/p).read_text())
def display(s): return s[1:-1] if s.startswith('"') and s.endswith('"') else s
checks=[]
def check(name,condition,detail=None):
 checks.append({'check':name,'pass':bool(condition),**({'detail':detail} if detail is not None else {})})
check('input MANIFEST.json seal',sha((ROOT/'MANIFEST.json').read_bytes())==EXPECTED)
man=read('MANIFEST.json'); bindings=read('source-bindings.json'); prov=read('fresh-production-provenance.json')
for p,h in man['files'].items(): check('manifest file '+p,sha((ROOT/p).read_bytes())==h)
check('manifest covers all nonmanifest input files',set(man['files'])=={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'})
check('production and tree agree',prov['commit']==man['production']==read('draft-review.json')['production'] and prov['tree']==read('draft-review.json')['tree'])
check('fresh binding records agree',bindings==prov['paths'])
source_results=[]
for p,r in bindings.items():
 b=(ROOT/r['local_complete_copy']).read_bytes()
 result={'path':p,'bytes':len(b),'sha256':sha(b),'git_blob':blob(b),'source_url':r['immutable_url']}
 check('source binding '+p,sha(b)==r['sha256'] and blob(b)==r['git_blob']); source_results.append(result)
for line in (ROOT/'lexical-evidence/SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1); p=p.lstrip('*'); check('lexical seal '+p,sha((ROOT/'lexical-evidence'/p).read_bytes())==h)
for s in read('lexical-evidence/sources.json'):
 b=(ROOT/'lexical-evidence'/s['file']).read_bytes()
 check('lexical snapshot '+s['file'],sha(b)==s['sha256'] and len(b)==s['bytes'])
 if s.get('git_blob'): check('lexical Git blob '+s['file'],blob(b)==s['git_blob'])
fragment_count=0
record_results=[]
for r in read('lexical-evidence/exact-records.json'):
 pieces=[r['english_record'],r['amharic_record']] if 'english_record' in r else [r]
 for f in pieces:
  fragment_count+=1
  lines=(ROOT/'lexical-evidence'/f['source_file']).read_text().splitlines()
  got='\n'.join(lines[f['start_line']-1:f['end_line']]).strip()
  expected=f.get('raw_xml_record',f.get('raw_po_record'))
  check('exact fragment '+r['id']+'/'+f['source_file'],got==expected)
  if 'raw_xml_record' in f:
   node=ET.fromstring('<root xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">'+got+'</root>')[0]
   check('XML attributes '+r['id']+'/'+f['source_file'],node.attrib==f['attributes'] and node.attrib['name']==f['key'])
   check('XML display '+r['id']+'/'+f['source_file'],display(''.join(node.itertext()))==f['display_text'])
  else:
   fields={}; active=None; flags=[]
   for line in got.splitlines():
    if line.startswith('#,'): flags.extend(x.strip() for x in line[2:].split(','))
    m=re.match(r'^(msgctxt|msgid|msgstr) (".*")$',line)
    if m: active=m[1]; fields[active]=ast.literal_eval(m[2])
    elif line.startswith('"') and active: fields[active]+=ast.literal_eval(line)
   check('PO fields '+r['id'],all(fields.get(k)==f[k] for k in ['msgctxt','msgid','msgstr']) and flags==f['flags'] and ('fuzzy' in flags)==f['fuzzy'] and bool(fields['msgstr']))
 record_results.append({'id':r['id'],'fragments':len(pieces),'role':r['evidence_role']})
eng=ET.parse(ROOT/'source/Paintroid/src/main/res/values/strings.xml').getroot()
am=ET.parse(ROOT/'source/Paintroid/src/main/res/values-b+am/strings.xml').getroot()
engmap={e.attrib['name']:e for e in eng if 'name' in e.attrib}; ammap={e.attrib['name']:e for e in am if 'name' in e.attrib}
rows=read('draft-review.json')['rows']; lexical={r['key']:r for r in read('lexical-evidence/draft-candidates.json')}; engrecords={r['key']:r for r in read('lexical-evidence/english-source-records.json')}
key_results=[]
for r in rows:
 k=r['key'].split('/')[1]; e=engmap[k]; l=lexical[r['key']]; er=engrecords[r['key']]
 check('unique English exact key '+k,len([x for x in eng if x.attrib.get('name')==k])==1)
 check('English exact source '+k,''.join(e.itertext())==r['English']==l['english']==er['english'] and e.attrib==r['source_attributes']==l['source_attributes']==er['source_attributes'])
 check('English value hash '+k,sha(r['English'])==r['source_sha256']==er['source_value_sha256'])
 check('English record lines '+k,'\n'.join((ROOT/'lexical-evidence/project-en-strings.xml').read_text().splitlines()[er['start_line']-1:er['end_line']]).strip()==er['raw_xml_record'])
 check('Amharic exact key absent '+k,k not in ammap)
 ce=ET.fromstring(r['proposed_XML_element']); c=r['proposed_XML_text']; disp=display(c)
 check('candidate XML and hash '+k,ce.tag=='string' and ce.attrib==e.attrib and ce.text==c and sha(c)==r['proposed_XML_text_sha256'] and disp==l['draft'])
 expected=1 if '%1$s' in r['English'] else 0
 check('placeholder contract '+k,c.count('%1$s')==expected and c.count('%')==expected and r['English'].count('%1$s')==expected)
 if k in ['ui_width','ui_height']: check('parenthesized unit '+k,disp.endswith(' (%1$s)'))
 if k.endswith('_in'): check('single attached preposition '+k,disp.endswith(' በ%1$s') and disp.count('በ')==1)
 key_results.append({'key':r['key'],'English':r['English'],'English_sha256':sha(r['English']),'candidate_XML_text':c,'candidate_XML_text_sha256':sha(c),'candidate_display_text':disp,'candidate_display_sha256':sha(disp),'candidate_element_sha256':sha(r['proposed_XML_element']),'placeholder_count':expected,'English_source_url':er['pinned_source_url']+'#L'+str(er['start_line'])})
expanded=[]
outer=read('interpolated-review-examples.json')
for i,c in enumerate(read('lexical-evidence/interpolation-cases.json')):
 candidate=lexical[c['key']]['draft']; got=candidate.replace('%1$s',c['argument'])
 check('expanded example '+str(i+1),candidate==c['draft_template'] and got==c['substituted_text']==outer[i]['expanded_candidate'] and outer[i]['key']==c['key'].split('/')[1] and outer[i]['unit']==c['argument'])
 if c['argument_source_key']: check('translated argument '+str(i+1),lexical[c['argument_source_key']]['draft']==c['argument'])
 expanded.append({'key':c['key'],'argument':c['argument'],'expanded':got,'expanded_sha256':sha(got)})
check('canonical translatable coverage',len([x for x in eng if x.get('name') and x.get('translatable')!='false'])==717 and len(ammap)==12 and len(set(x.attrib['name'] for x in eng if x.get('name') and x.get('translatable')!='false')-set(ammap))==705)
check('eight distinct candidate keys',len(rows)==len({r['key'] for r in rows})==8)
check('evidence cardinalities',len(bindings)==18 and len(read('lexical-evidence/sources.json'))==9 and len(record_results)==16 and fragment_count==24 and len(expanded)==8)
# Independent bounded literal source-reference inventory, not a whole-repository scan.
pat=re.compile(r'R\.string\.('+'|'.join(sorted([r['key'].split('/')[1] for r in rows],key=len,reverse=True))+r')\b')
refs=[]
for p in (ROOT/'source').rglob('*.kt'):
 for n,line in enumerate(p.read_text().splitlines(),1):
  matches=pat.findall(line)
  if matches: refs.append({'file':str(p.relative_to(ROOT/'source')),'line':n,'keys':matches,'source_line':line.strip()})
report={'status':'pass' if all(x['pass'] for x in checks) else 'fail','check_count':len(checks),'failed_checks':[x for x in checks if not x['pass']],'input_manifest_sha256':EXPECTED,'production':man['production'],'tree':prov['tree'],'manifest_file_count':len(man['files']),'source_file_count':len(source_results),'lexical_snapshot_count':len(read('lexical-evidence/sources.json')),'lexical_record_count':len(record_results),'lexical_fragment_count':fragment_count,'English_named_containers':len(engmap),'Amharic_named_containers':len(ammap),'canonical_translatable_containers':717,'canonical_present':12,'canonical_missing':705,'keys':key_results,'expansions':expanded,'bounded_consumer_references':refs,'source_files':source_results,'exact_records':record_results,'checks':checks,'limits':['No production head fetch was performed by this reviewer. Byte/blob bindings were recomputed against the supplied parent provenance.','No Kotlin/Java or Android runtime, build, rendering, accessibility speech, UI fit, or native speaker test was run.','Static Python string substitution validates supplied examples, not formatter execution.']}
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','check_count','failed_checks','manifest_file_count','source_file_count','lexical_snapshot_count','lexical_record_count','lexical_fragment_count','English_named_containers','Amharic_named_containers']},ensure_ascii=False,indent=2))
