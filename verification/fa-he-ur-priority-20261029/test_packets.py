from pathlib import Path
import sys,json,re,copy,unittest,xml.etree.ElementTree as E
P=Path(__file__).parent;R=P/'repo';sys.path.insert(0,str(R/'tools'));import translation_catalogues as cat

def nodevalue(n):return {'attributes':dict(n.attrib),'value':n.text if n.tag=='string'else {c.get('quantity'):c.text for c in n}}
def nodes(path):return {n.tag+'/'+n.get('name'):n for n in E.parse(path).getroot() if n.get('name')}
def validate(d):
 tag=d['locale']; paths={'fa':'values-fa','he':'values-iw','ur':'values-ur'}
 if d['catalogue_path']!=f'Paintroid/src/main/res/{paths[tag]}/strings.xml':raise ValueError('canonical locale/path')
 en=nodes(R/'Paintroid/src/main/res/values/strings.xml');cur=nodes(R/d['catalogue_path'])
 tiers=json.loads((R/'translations/string-importance.json').read_text())['tiers'];scope={k:t['id']for t in tiers if t['id']in('P0','P1')for k in t['keys']}
 rows=d['priority_rows'];ids=[r['identity']for r in rows]
 if len(set(ids))!=len(ids)or set(ids)!=set(scope):raise ValueError('full typed priority scope')
 allids=ids+[r['identity']for r in d['companions']]
 if len(set(allids))!=len(allids):raise ValueError('duplicate companion')
 for r in rows+d['companions']:
  k=r['identity'];typ,name=k.split('/');src=en[k]
  if r['english']!=nodevalue(src):raise ValueError('source binding')
  n=cur.get(k)
  if r['current']!=(None if n is None else nodevalue(n)):raise ValueError('current complete value binding')
  if k in scope and r['tier']!=scope[k]:raise ValueError('tier')
  for c in r['direct_consumers']:
   lines=(R/c['path']).read_text().splitlines();actual='\n'.join(lines[c['start_line']-1:c['end_line']])
   if actual!=c['text']:raise ValueError('consumer source moved')
  if r['decision'].startswith('hold'):
   if r['candidate']is not None:raise ValueError('hold promoted')
   continue
  if r['candidate']is None:raise ValueError('missing proposed complete value')
  v=r['candidate'];a=r['candidate_attributes']
  if a.get('name')!=name:raise ValueError('typed identity')
  source_values=r['english']['value'];source_text=next(iter(source_values.values()))if isinstance(source_values,dict)else source_values
  if typ=='plurals':
   if not isinstance(v,dict)or'other'not in v or set(v)-{'zero','one','two','few','many','other'}:raise ValueError('plural quantities')
  for s in v.values()if isinstance(v,dict)else[v]:
   if cat.placeholders(s)!=cat.placeholders(source_text):raise ValueError('placeholder contract')
   if cat.android_string_errors(s)or cat.format_string_errors(s,a.get('formatted')!='false'):raise ValueError('Android syntax')
   if cat.literal_token_errors(name,s,source_text):raise ValueError('technical literal contract')
   for token in ('sRGB','RGB','ICC','canvas.png','AN Paint','Android','512 MiB','144 dpi','#RRGGBB'):
    if token in source_text and token not in s:raise ValueError('required operational literal')
   if s.startswith('@string/')and not(k=='string/ui_save_a5d0d9'and s=='@string/ui_save'):raise ValueError('unexpected alias')
 return True

class CompletePackets(unittest.TestCase):
 def setUp(self):self.data={t:json.loads((P/'packets'/f'{t}-complete-packet.json').read_text())for t in('fa','he','ur')}
 def test_complete_current_source_consumer_syntax(self):
  for d in self.data.values():self.assertTrue(validate(d))
 def rejected(self,mutate):
  for d in self.data.values():
   x=copy.deepcopy(d);mutate(x)
   with self.assertRaises((ValueError,KeyError)):validate(x)
 def test_missing_or_duplicate_priority_fails(self):
  self.rejected(lambda d:d['priority_rows'].pop());self.rejected(lambda d:d['priority_rows'].append(d['priority_rows'][0]))
 def test_full_source_and_predecessor_binding(self):
  self.rejected(lambda d:d['priority_rows'][0]['english'].update(value='changed source'))
  self.rejected(lambda d:d['priority_rows'][14]['current'].update(value='changed predecessor'))
 def test_placeholder_deletion_or_duplication_fails(self):
  self.rejected(lambda d:d['priority_rows'][0].update(candidate=d['priority_rows'][0]['candidate'].replace('%2$s','')))
  self.rejected(lambda d:d['priority_rows'][0].update(candidate=d['priority_rows'][0]['candidate']+' %1$s'))
 def test_hold_cannot_be_silently_promoted(self):self.rejected(lambda d:d['priority_rows'][6].update(candidate='invented'))
 def test_wrong_type_identity_or_canonical_path_fails(self):
  self.rejected(lambda d:d.update(catalogue_path='Paintroid/src/main/res/values-fa-rIR/strings.xml'))
  self.rejected(lambda d:d['priority_rows'][0]['candidate_attributes'].update(name='wrong_key'))
 def test_consumer_change_fails(self):self.rejected(lambda d:d['priority_rows'][0]['direct_consumers'][0].update(text='different consumer'))
 def test_plural_other_deletion_fails(self):self.rejected(lambda d:next(r for r in d['companions']if r['identity']=='plurals/ui_crop_preview_images')['candidate'].pop('other'))
 def test_technical_literal_removal_fails(self):self.rejected(lambda d:d['priority_rows'][20].update(candidate=d['priority_rows'][20]['candidate'].replace('sRGB','RGB')))
 def test_unescaped_apostrophe_fails(self):self.rejected(lambda d:d['priority_rows'][0].update(candidate=d['priority_rows'][0]['candidate'].strip('"')+"'"))
if __name__=='__main__':unittest.main()
