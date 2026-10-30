"""Complete SI/MY replacement and bounded ZA acceptance; not fluency certification."""
from pathlib import Path
from copy import deepcopy
import json,unittest,xml.etree.ElementTree as E
from sinhala_burmese_zhuang_priority_expectations import reviewed_fixture,require_reviewed_fixture,validated_fixture_text,current_row,display,NAME
import translation_catalogues as c
ROOT=Path(__file__).resolve().parents[1]
def value(n):return {'attributes':dict(n.attrib),'value':{x.attrib['quantity']:x.text for x in n} if n.tag=='plurals' else n.text}
class SinhalaBurmeseZhuangTests(unittest.TestCase):
 def test_complete_priority_and_companion_partition_and_real_edits(self):
  d=reviewed_fixture();scope=json.loads((ROOT/'translations/string-importance.json').read_text())['tiers'];keys={k.split('/',1)[1] for t in scope if t['id'] in ('P0','P1') for k in t['keys']}
  self.assertEqual({'si','my','za'},set(d['locales']))
  for tag,loc in d['locales'].items():
   self.assertEqual(keys,set(loc['priority']));self.assertEqual(15,len(loc['dependencies']))
   self.assertEqual(set(loc['priority'])|set(loc['dependencies']),set(loc['accepted'])|set(loc['holds']))
   self.assertTrue(set(loc['accepted']).isdisjoint(loc['holds']))
   self.assertEqual({'si':7,'my':7,'za':312}[tag],len(loc['holds']))
   self.assertEqual({'si':335,'my':301,'za':2}[tag],len(loc['changed']))
   self.assertEqual(set(loc['changed']),set(loc['predecessors']))
   for key in loc['changed']:self.assertNotEqual(loc['predecessors'][key],{'attributes':loc['attributes'][key],'value':loc['accepted'][key]})
 def test_all_complete_source_target_attributes_holds_syntax_and_placeholders(self):
  d=reviewed_fixture();en={n.attrib['name']:n for n in E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot() if 'name'in n.attrib}
  for key,row in d['sources'].items():self.assertEqual({'attributes':row['attributes'],'value':row['value']},value(en[key]));self.assertEqual(row['type'],en[key].tag)
  for tag,loc in d['locales'].items():
   actual={n.attrib['name']:n for n in E.parse(ROOT/loc['catalogue_path']).getroot() if 'name'in n.attrib}
   for key,v in loc['accepted'].items():
    self.assertEqual({'attributes':loc['attributes'][key],'value':v},value(actual[key]),tag+'/'+key)
    src=d['sources'][key]['value'];src=src['other'] if isinstance(src,dict) else src
    for text in v.values() if isinstance(v,dict) else [v]:
     self.assertEqual(c.placeholders(src),c.placeholders(text));self.assertEqual([],c.android_string_errors(text));self.assertEqual([],c.format_string_errors(text,loc['attributes'][key].get('formatted')!='false'))
   for key,v in loc['holds'].items():self.assertEqual(v,value(actual[key]) if key in actual else None,tag+'/'+key)
   if tag!='za':self.assertEqual({'one','other'} if tag=='si' else {'other'},set(loc['accepted']['ui_crop_preview_images']))
 def test_every_target_and_finite_metadata_mutation_rejected(self):
  data=reviewed_fixture();require_reviewed_fixture(data)
  for tag,loc in data['locales'].items():
   for key,v in loc['accepted'].items():
    bad=deepcopy(data);bad['locales'][tag]['accepted'][key]={'other':'forged'} if isinstance(v,dict) else v+' forged'
    with self.subTest(tag=tag,key=key),self.assertRaises(ValueError):require_reviewed_fixture(bad)
   for key in ('holds','attributes','changed','priority','dependencies','predecessors'):
    bad=deepcopy(data);bad['locales'][tag][key]={}
    with self.assertRaises(ValueError):require_reviewed_fixture(bad)
 def test_raw_alias_and_deep_mutability_boundaries(self):
  self.assertEqual('@string/ui_save',current_row('my','ui_save_a5d0d9')['target']);self.assertEqual(display('my','ui_save'),display('my','ui_save_a5d0d9'))
  from unittest.mock import patch
  for replacement in ('@string/ui_save_a5d0d9','@string/missing','@string/ui_crop_preview_images'):
   def altered(tag,key):
    row=current_row(tag,key)
    if key=='ui_save':row['target']=replacement
    return row
   with patch('sinhala_burmese_zhuang_priority_expectations.current_row',side_effect=altered):
    with self.assertRaises(ValueError):display('my','ui_save_a5d0d9')
  baseline=current_row('si','ui_crop_preview_images');copy=current_row('si','ui_crop_preview_images');copy['source']['other']='forged';copy['target']['one']='forged';self.assertEqual(baseline,current_row('si','ui_crop_preview_images'))
  self.assertEqual(display('my','ui_save'),display('my','ui_save_a5d0d9'))
  for tag,key in [('th','ui_undo'),('za','ui_save'),('si','ui_save_as_png')]:
   with self.assertRaises(ValueError):current_row(tag,key)
 def test_reviewed_sinhala_composition_and_exact_fixture_binding(self):
  self.assertNotEqual(display('si','ui_undo'),display('si','ui_cancel'))
  self.assertEqual('false',current_row('si','ui_quality')['attributes']['formatted'])
  for key in ('ui_width_in','ui_height_in'):
   self.assertIn('පික්සලවලින්',display('si',key).replace('%1$s',display('si','ui_pixels_6ec9c2')))
   self.assertIn('ප්‍රතිශතවලින්',display('si',key).replace('%1$s',display('si','ui_percent_fd8671')))
  text=(ROOT/'tools/fixtures/current_localization'/NAME).read_text();validated_fixture_text(text)
  bad=json.loads(text);bad['locales']['za']['accepted']['ui_all']='forged'
  with self.assertRaises(ValueError):validated_fixture_text(json.dumps(bad,ensure_ascii=False))
if __name__=='__main__':unittest.main()
