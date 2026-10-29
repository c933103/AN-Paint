"""Full-value Thai replacement evidence; no new programme-wide review credit."""
from pathlib import Path
from copy import deepcopy
import unittest,json,xml.etree.ElementTree as E
from thai_priority_expectations import reviewed_fixture,require_reviewed_fixture,validated_fixture_text,current_row,display,NAME
import translation_catalogues as catalogues
ROOT=Path(__file__).resolve().parents[1]
def value(n):
 return {'attributes':dict(n.attrib),'value':{x.attrib['quantity']:x.text for x in n} if n.tag=='plurals' else n.text}
class ThaiReplacementTests(unittest.TestCase):
 def test_complete_priority_and_dependency_partition(self):
  d=reviewed_fixture();loc=d['locales']['th'];tiers=json.loads((ROOT/'translations/string-importance.json').read_text())['tiers']
  keys={k.split('/',1)[1] for t in tiers if t['id'] in ('P0','P1') for k in t['keys']}
  self.assertEqual(keys,set(loc['priority']));self.assertEqual(8,len(loc['holds']));self.assertEqual(15,len(loc['dependencies']));self.assertEqual(238,len(loc['changed']))
  self.assertEqual(keys-set(loc['holds'])|set(loc['dependencies']),set(loc['accepted']))
  self.assertEqual({'th'},set(d['locales']));self.assertEqual(set(loc['changed']),set(loc['predecessors']))
 def test_every_source_and_full_target_attributes_and_arguments(self):
  d=reviewed_fixture();loc=d['locales']['th'];source={n.attrib['name']:n for n in E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot() if 'name'in n.attrib};actual={n.attrib['name']:n for n in E.parse(ROOT/loc['catalogue_path']).getroot() if 'name'in n.attrib}
  for key,row in d['sources'].items():self.assertEqual({'attributes':row['attributes'],'value':row['value']},value(source[key]));self.assertEqual(row['type'],source[key].tag)
  for key,expected in loc['accepted'].items():
   self.assertEqual({'attributes':loc['attributes'][key],'value':expected},value(actual[key]),key)
   src=d['sources'][key]['value']
   if isinstance(expected,dict):
    self.assertEqual({'other'},set(expected))
    for v in expected.values():self.assertEqual(catalogues.placeholders(src['other']),catalogues.placeholders(v))
   else:self.assertEqual(catalogues.placeholders(src),catalogues.placeholders(expected))
  for key,row in loc['holds'].items():self.assertEqual(row,value(actual[key]) if key in actual else None)
 def test_every_target_and_coordinated_metadata_mutant_rejected(self):
  d=reviewed_fixture();require_reviewed_fixture(d)
  for key,v in d['locales']['th']['accepted'].items():
   bad=deepcopy(d);bad['locales']['th']['accepted'][key]= {'other':'forged'} if isinstance(v,dict) else v+' forged';bad['locales']['th']['display']={key:'forged'}
   with self.subTest(key=key),self.assertRaises(ValueError):require_reviewed_fixture(bad)
  for key in ('holds','attributes','changed','priority','dependencies','predecessors'):
   bad=deepcopy(d);bad['locales']['th'][key]={}
   with self.assertRaises(ValueError):require_reviewed_fixture(bad)
 def test_retained_alias_resolves_without_changing_raw_resource(self):
  self.assertEqual('@string/ui_save',current_row('th','ui_save_a5d0d9')['target'])
  self.assertEqual(display('th','ui_save'),display('th','ui_save_a5d0d9'))
  with self.assertRaises(ValueError):display('th','ui_crop_preview_images')
  from unittest.mock import patch
  for replacement in ('@string/ui_save_a5d0d9','@string/missing_alias_target'):
   def changed(tag,key):
    row=current_row(tag,key)
    if key=='ui_save':row['target']=replacement
    return row
   with patch('thai_priority_expectations.current_row',side_effect=changed):
    with self.assertRaises(ValueError):display('th','ui_save_a5d0d9')
  self.assertEqual(display('th','ui_save'),display('th','ui_save_a5d0d9'))
 def test_raw_coordinated_fixture_and_mutable_cache_poison_rejected(self):
  text=(ROOT/'tools/fixtures/current_localization'/NAME).read_text();validated_fixture_text(text)
  d=json.loads(text);d['locales']['th']['accepted']['ui_undo']='forged'
  with self.assertRaises(ValueError):validated_fixture_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  original=current_row('th','ui_undo');copy=current_row('th','ui_undo');copy['attributes']['name']='forged';self.assertEqual(original,current_row('th','ui_undo'))
  plural=current_row('th','ui_crop_preview_images');copy=current_row('th','ui_crop_preview_images');copy['target']['other']='forged';copy['source']['other']='forged';self.assertEqual(plural,current_row('th','ui_crop_preview_images'))
  for tag,key in [('hi','ui_undo'),('th','ui_discard'),('th','unknown')]:
   with self.assertRaises(ValueError):current_row(tag,key)
if __name__=='__main__':unittest.main()
