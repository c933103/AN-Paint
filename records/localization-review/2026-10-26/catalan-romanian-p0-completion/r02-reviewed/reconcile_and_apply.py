#!/usr/bin/env python3
"""Reconcile exact independent complete-value receipts and apply missing-only resources."""
import argparse,collections,hashlib,json,pathlib,sys,xml.etree.ElementTree as ET
from xml.sax.saxutils import escape,quoteattr
PIN='ce796879f4568a27b9d905a8e8db639dd0a93a30'
TREE='f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
MANIFESTS={'ca':'27105ba12a3b5424b52ac0cd2abd251b79d364779ac8e51b2b0057e111d17bec','ro':'67e57079828e04a3c166b8d5c7e6ae78831134675af8b97cad4a7597a9970cde'}
HOLDS=['formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png']
def require(x,msg):
 if not x:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:require(k not in d,'duplicate JSON key '+k);d[k]=v
 return d
def read(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def run(a):
 packet,review,base,out=map(pathlib.Path,[a.packet,a.review,a.base_source,a.output])
 sys.path.insert(0,str(base/'tools'))
 from test_danish_norwegian_p0_wording import full_format_tokens,require_reviewed_string
 scope=read(packet/'scope-and-source-context.json'); foundation=read(packet/'terminology-foundations.json')
 require(scope['source_commit']==PIN and scope['source_tree']==TREE,'source pin')
 english=ET.parse(base/'Paintroid/src/main/res/values/strings.xml').getroot()
 englishmap={x.attrib['name']:x for x in english if x.tag=='string'}
 selected={x['identity'].split('/',1)[1] for x in scope['entries']};require(len(selected)==55,'55 keys')
 fixture={'schema_version':1,'note':'Exactly 55 independently reviewed missing P0 complete values per Catalan/Romanian catalogue: 107 unchanged candidates and 3 exact revisions. Bounded AI linguistic/source-static acceptance with source/author qualifications retained in review receipts; not native-human, runtime, layout or whole-language certification. All 300 inherited values, five holds each, English composition labels, Valencian inheritance distinction, P1/paired frozen history and global 59/112 remain unchanged.','values':{},'constraints':{},'preserved_values':{},'held_absent':HOLDS}
 approved={'schema_version':1,'record_kind':'Exact reviewed missing-only implementation manifest','source_commit':PIN,'source_tree':TREE,'review_manifests':MANIFESTS,'scope':'Independent AI complete-value linguistic and source-static acceptance, qualified; not native-human/runtime/layout/whole-locale acceptance','historical_author_context':'Original pending-review wording is preserved in candidate and reviewer evidence as historical proposal context. Explicit independent verdicts and final strings determine current bounded status; original semantic caveats remain applicable.','values':[],'source_semantic_revision_reconciliation':['AutosaveStore.preserveForRecovery uses a distinct recovery ZIP target and throws on missing source or failed rename. CA and RO negative revisions describe the intended move without promising successful preservation.','TextImageCodec.replace is called by decodeToFile, encodeBase64 and encodeAscii. CA fitxer resultant names completed temporary output without restricting it to encoding or artwork.'],'preserved_holds':HOLDS,'acceptance_counts':{},'limits':['No native-human, device, layout, whole-language or release certification.','Paired memory-warning oracle stays 120 entries/60 tags; only separate exact-key P0 expectations may be added. P1 remains absent.','Valencian parent inheritance remains distinct from direct reviewed values; existing labels and mixed English dynamic reasons remain unchanged.']}
 changes=[]
 for tag in ('ca','ro'):
  mp=review/tag/f'{tag}-review-manifest.json';require(digest(mp.read_bytes())==MANIFESTS[tag],tag+' manifest hash');m=read(mp)
  require(m['source_commit']==PIN and m['source_tree']==TREE,'review source')
  files=m.get('files',m.get('group_receipts',[]))
  if tag=='ro':files=files+[m['source_input_verification']]
  for f in files:
   fp=review/tag/f.get('path',f.get('file'));require(digest(fp.read_bytes())==f['sha256'],'receipt hash '+fp.name)
  finals={}; counts=collections.Counter()
  for cp in sorted(packet.glob(tag+'-group-*-candidates.json')):
   c=read(cp);g=c['group'];require(c['source_commit']==PIN,'candidate pin')
   rp=next((review/tag).glob(f'{tag}-group-{g:02d}-*-independent-review.json'));r=read(rp)
   bound=r['candidate_packet'];rh=r.get('candidate_packet_sha256',bound.get('sha256') if isinstance(bound,dict) else None)
   require(rh==digest(cp.read_bytes()),'candidate receipt binding '+rp.name)
   rows=r.get('entries',r.get('verdicts')); require(len(rows)==len(c['candidates']),'review count')
   cm={x['identity']:x for x in c['candidates']}
   require(len(cm)==len(rows) and set(cm)=={x['identity'] for x in rows},'exact review join')
   for v in rows:
    k=v['identity'].split('/',1)[1];require(k not in finals,'duplicate final');cv=cm[v['identity']]
    require(v['verdict'] in ('accept','revise'),'held value cannot apply')
    for f in ['source','source_value_sha256_utf8','candidate_display_text','candidate_value_sha256_utf8','attributes','placeholder_tokens','consumer_context_ids']:require(v[f]==cv[f],'candidate field differs '+k+'/'+f)
    require(v['source']==''.join(englishmap[k].itertext()) and v['attributes']==englishmap[k].attrib,'exact English binding '+k)
    for f,h in [('source','source_value_sha256_utf8'),('candidate_display_text','candidate_value_sha256_utf8'),('final_display_text','final_value_sha256_utf8'),('final_xml_text','final_xml_text_sha256_utf8')]:require(digest(v[f].encode())==v[h],'value hash '+k+'/'+f)
    require(v['final_xml_text']=='"'+v['final_display_text']+'"','Android quote representation')
    require(full_format_tokens(v['final_xml_text'])==full_format_tokens(v['source']),'full token inventory')
    require(v['verdict']!='accept' or v['final_display_text']==cv['candidate_display_text'],'accept changed value')
    if tag=='ca':
     require(v['retained_author_uncertainties']==cv['author_uncertainties'],'author caveats')
     require(v['retained_source_semantic_notes']==cv['source_semantic_notes'],'source notes')
     require(v['retained_author_semantic_qualifications']==cv['author_semantic_qualifications'],'author qualifications')
    else:require(v['original_author_uncertainties_preserved_as_context']==cv['author_uncertainties'],'author caveats')
    finals[k]=v;counts[v['verdict']]+=1
    approved['values'].append({'locale':tag,'identity':v['identity'],'group':g,'verdict':v['verdict'],'source':v['source'],'source_value_sha256_utf8':v['source_value_sha256_utf8'],'attributes':v['attributes'],'final_display_text':v['final_display_text'],'final_value_sha256_utf8':v['final_value_sha256_utf8'],'final_xml_text':v['final_xml_text'],'final_xml_text_sha256_utf8':v['final_xml_text_sha256_utf8'],'receipt':f'{tag}/{rp.name}','receipt_sha256':digest(rp.read_bytes()),'qualifications':'All complete-value qualifications and historical author caveats in the exact referenced receipt remain applicable; no scope elevation.'})
  require(set(finals)==selected,'selected identities differ')
  target=pathlib.Path(f'Paintroid/src/main/res/values-{tag}/strings.xml');raw=(base/target).read_bytes();root=ET.fromstring(raw);require(len(root)==150,'baseline count')
  require(digest(raw)==foundation['locales'][tag]['sha256'],'baseline foundation hash')
  existing={x.attrib['name']:{'value':''.join(x.itertext()),'attributes':x.attrib} for x in root};require(len(existing)==150 and not set(existing)&selected,'missing-only')
  fixture['preserved_values'][tag]=existing
  require(not (set(HOLDS)|{'ui_no_resize_fits_decoder_memory'})&set(existing),'held/P1 absent')
  additions=[]
  for k,v in sorted(finals.items()):
   fixture['values'].setdefault(k,{'default':v['source']})[tag]=v['final_xml_text']
   fixture['constraints'].setdefault(k,{'default':{'attributes':v['attributes'],'placeholders':full_format_tokens(v['source'])}})[tag]={'attributes':v['attributes'],'placeholders':full_format_tokens(v['source'])}
   attr=' '.join(n+'='+quoteattr(val) for n,val in v['attributes'].items());additions.append('    <string '+attr+'>'+escape(v['final_xml_text'])+'</string>')
  require(raw.count(b'</resources>')==1,'resources closing boundary')
  updated=raw.replace(b'</resources>', ('\n    <!-- Bounded independently reviewed P0 completion values. -->\n'+'\n'.join(additions)+'\n</resources>').encode())
  parsed=ET.fromstring(updated);require(len(parsed)==205,'result count')
  for k,v in existing.items():
   node=parsed.find(f"./string[@name='{k}']");require(node is not None and ''.join(node.itertext())==v['value'] and node.attrib==v['attributes'],'inherited value changed')
  for k,v in finals.items():require_reviewed_string(updated.decode(),k,v['final_xml_text'],fixture['constraints'][k][tag],v['source'])
  dest=out/target;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(updated)
  approved['acceptance_counts'][tag]=dict(counts)
  changes.append({'path':str(target),'before_sha256':digest(raw),'after_sha256':digest(updated),'added_values':55,'inherited_values_unchanged':150,'final_containers':205,'P0_present':87,'P0_missing_held':5})
 fixturepath=out/'tools/fixtures/current_localization/catalan_romanian_completion_wording.json';dump(fixturepath,fixture)
 approved['implementation_resource_changes']=changes;approved['fixture_sha256']=digest(fixturepath.read_bytes());approved['final_values']=110
 dump(pathlib.Path(a.receipt),approved)
 print(json.dumps({'applied_values':110,'counts':approved['acceptance_counts'],'fixture_sha256':approved['fixture_sha256'],'approved_manifest_sha256':digest(pathlib.Path(a.receipt).read_bytes())}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',required=True);p.add_argument('--review',required=True);p.add_argument('--base-source',required=True);p.add_argument('--output',required=True);p.add_argument('--receipt',required=True);run(p.parse_args())
