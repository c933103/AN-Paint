import hashlib,json,pathlib,sys
sys.path.insert(0,'tools')
import translation_catalogues as c
ROOT=pathlib.Path.cwd(); out=ROOT/'verification/attribution-terminology-2026-10-09'
history=ROOT/'verification/help-commons-provider-2026-10-09'; original=json.loads((history/'translations.json').read_text())
proposal=json.loads((out/'proposal.json').read_text()); item=next(i for i in proposal['items'] if i['key']=='ui_help23')
def digest(s):return hashlib.sha256(s.encode('utf8')).hexdigest()
row=original['translations']['hu']; before=item['current'];after=item['proposed'];replacement=item['replacements'][0]
assert digest(before)==row['after_help_sha256']
successor={'task':'AN-W05-C05-HU-15','status':'proposed_not_applied','historical_manifest':'verification/help-commons-provider-2026-10-09/translations.json','historical_manifest_sha256':digest((history/'translations.json').read_text()),'transitions':{'hu':{'resource':'ui_help23','catalogue':item['path'],'historical_after_help_sha256':digest(before),'successor_after_help_sha256':digest(after),**replacement}}}
(out/'help-successor-proposal.json').write_text(json.dumps(successor,ensure_ascii=False,indent=2)+'\n')
def verify(tag,current):
 oldrow=original['translations'][tag]
 historical=current
 if tag=='hu':
  s=successor['transitions'][tag]
  assert digest(current)==s['successor_after_help_sha256']
  assert s['occurrences']==1
  assert current.count(s['proposed_phrase'])==1
  assert s['current_phrase'] not in current
  historical=current.replace(s['proposed_phrase'],s['current_phrase'],1)
  assert digest(historical)==s['historical_after_help_sha256']==oldrow['after_help_sha256']
 assert current.count(oldrow['caption'])==1
 assert current.count(oldrow['after_segment'])==1
 assert digest(historical)==oldrow['after_help_sha256']
 old=historical.replace(oldrow['after_segment'],oldrow['before_segment'],1)
 assert digest(old)==oldrow['before_help_sha256']
 assert 'Wikimedia Commons' not in old
 assert oldrow['before_context'] in old
 assert oldrow['after_context'] in current
 assert c.placeholders(old)==c.placeholders(current)
 assert not c.android_string_errors(current)
 assert not c.format_string_errors(current,False)
 for provider in ['Catrobat','Openclipart','Irasutoya','いらすとや']:
  assert old.count(provider)==current.count(provider)
for tag,row in original['translations'].items():
 value=after if tag=='hu' else c.read_strings(ROOT/row['catalogue'])['ui_help23']
 verify(tag,value)
mutations={
 'hu-unrelated-opening':('hu',after.replace('Válasszon','Választhat',1)),
 'hu-unrelated-ending':('hu',after+' '),
 'hu-commons-removed':('hu',after.replace('Wikimedia Commons · Vaktérképek…','',1)),
 'hu-provider-changed':('hu',after.replace('Openclipartot','Openclipart',1)),
 'hu-terminology-reverted':('hu',before),
 'hu-terminology-duplicated':('hu',after+replacement['proposed_phrase']),
 'non-hu-unrelated-change':('fr',c.read_strings(ROOT/original['translations']['fr']['catalogue'])['ui_help23']+' '),
}
rejected=[]
for name,(tag,value) in mutations.items():
 try:verify(tag,value)
 except AssertionError:rejected.append(name)
 else:raise AssertionError('Mutation accepted: '+name)
result={'status':'in_memory_successor_design_check_only','application_resources_changed':False,'historical_files_changed':False,'positive_default_plus_scoped_cases':60,'negative_mutations_rejected':rejected,'new_hungarian_help_sha256':digest(after),'reconstructed_pr32_hungarian_help_sha256':digest(before),'reconstructed_pre_pr32_hungarian_help_sha256':original['translations']['hu']['before_help_sha256'],'limits':'This checks the proposed hash-transition logic against extracted text; the repository test has not been changed, and Android/runtime evidence is not established.'}
(out/'help-successor-design-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
