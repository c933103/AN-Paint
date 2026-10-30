import csv,json,re,sys,xml.etree.ElementTree as E
sys.path.insert(0,'tools')
from translation_catalogues import android_string_errors, FORMAT_TOKEN
from pathlib import Path
p=Path('records/localization-review/2026-10-30/qug-quh-quz-priority'); m=json.load(open('translations/string-importance.json')); tiers={k.split('/')[1]:t['id'] for t in m['tiers'][:2] for k in t['keys']}; source={e.get('name'):''.join(e.itertext()) for e in E.parse('Paintroid/src/main/res/values/strings.xml').getroot()}
authored=list(csv.DictReader((p/'candidates.tsv').open(),delimiter='\t'))
rows={r['key']:r for r in authored}
assert len(rows)==len(authored), 'Duplicate candidate key'
assert not (rows.keys()-tiers.keys()),rows.keys()-tiers.keys()
pattern=re.compile(r'%(?:\d+\$)[-+# 0,(<]*(?:\d+)?(?:\.\d+)?[bBhHsScCdoxXeEfgGaAtT%n]')
invariant={'ui_0f_0f_px_1f','ui_100','ui_1_px','ui_1f_s','ui_hex_rrggbb','ui_numeric_slider_value','ui_px','ui_px_724eb3'}
summary={}
for l in ('qug','quh','quz'):
 root=E.Element('resources'); review=[]
 for k in tiers:
  if k in rows:
   v=rows[k][l]; assert sorted(pattern.findall(v))==sorted(pattern.findall(source[k])),(l,k,v)
   E.SubElement(root,'string',{'name':k}).text=v.replace("'",r"\'")
   review.append({'key':k,'tier':tiers[k],'source':source[k],'candidate':v,'literal_backtranslation':rows[k]['backtranslation'],'status':'unreviewed-regional-candidate','review_note':'Confirm local UI usage; see locale-specific terminology review in README.'})
  else: review.append({'key':k,'tier':tiers[k],'source':source[k],'candidate':None,'status':'unresolved-not-translated','review_note':'No defensible complete regional wording supplied yet. Do not fill from another Quechua catalogue.'})
 E.indent(root); (p/(l+'.xml')).write_text('<?xml version="1.0" encoding="utf-8"?>\n<!-- Candidate only. NOT production acceptance. Missing keys are not translated. -->\n'+E.tostring(root,encoding='unicode')+'\n')
 (p/(l+'-review.json')).write_text(json.dumps({'locale':l,'status':'unreviewed-partial-candidate','backtranslations':'candidates.tsv','unresolved_keys':[r['key'] for r in review if r['candidate'] is None]},ensure_ascii=False,indent=2)+'\n')
 summary[l]={t:sum(k in rows and tiers[k]==t for k in tiers) for t in ['P0','P1']}; summary[l]['unresolved']=len(tiers)-len(rows)
 summary[l]['invariant_notation_not_translated_prose']=len(invariant)
 summary[l]['prose_candidates']=len(rows)-len(invariant)
 parsed=E.parse(p/(l+'.xml')).getroot()
 assert len(parsed)==len(rows)
 for e in parsed:
  v=''.join(e.itertext())
  assert not android_string_errors(v),(l,e.get('name'),android_string_errors(v))
  assert sorted(FORMAT_TOKEN.findall(v))==sorted(FORMAT_TOKEN.findall(source[e.get('name')]))
(p/'validation.json').write_text(json.dumps({'base':'420cb76fb1fc02a53a5b6296505be193eaa3bb2f','required_per_locale':{'P0':92,'P1':249},'candidate_counts':summary,'xml_parse':'pass','android_quoting':'pass','placeholder_identity':'pass','production_changes':False,'linguistic_acceptance':False,'full_tests':'not-run-as-instructed'},indent=2)+'\n')
print(json.dumps(summary))

with (p/'scope.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['key','tier','English_source','candidate_status'])
 for k,t in tiers.items():w.writerow([k,t,source[k],'unreviewed-candidate' if k in rows else 'unresolved-not-translated'])
with (p/'regional-comparison.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['key','comparison','rationale'])
 for k,r in rows.items():
  vals=[r[l] for l in ('qug','quh','quz')]
  if len(set(vals))==1:
   reason='Shared technical notation; no prose translation claim' if k in invariant else 'Shared candidate vocabulary; independently subject to regional review, not transferred acceptance'
   comp='all-identical'
  elif vals[1]==vals[2]:comp='quh-quz-identical';reason='Shared Southern candidate morphology/vocabulary; Ecuadorian wording differs. Neither Southern entry validates the other.'
  else:comp='regional-difference';reason='Explicit regional vocabulary, morphology or action-label convention; see three authored values and README terminology choices.'
  w.writerow([k,comp,reason])
