"""Complete resource/composition regressions for recovered HI/GU wording."""
from current_localization_contracts import require_residual_or_previous
from copy import deepcopy
from pathlib import Path
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture,require_string, require_string_root
from hindi_gujarati_priority_expectations import NAME,TAGS,current_row,display,require_reviewed_fixture,validated_fixture_text,reviewed_fixture
import translation_catalogues as catalogues
ROOT=Path(__file__).resolve().parents[1]
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png','ui_foreground_background_colour_palette','ui_pinch_and_pan_mode'}
class HindiGujaratiPriorityWordingTests(unittest.TestCase):
 def test_full_priority_and_dependency_partition(self):
  data=fixture(NAME);tiers=json.loads((ROOT/'translations/string-importance.json').read_text())['tiers'];keys={k.split('/',1)[1] for t in tiers if t['id'] in ('P0','P1') for k in t['keys']}
  self.assertEqual(TAGS,set(data['locales']))
  for tag,loc in data['locales'].items():
   self.assertEqual(keys,set(loc['priority']));self.assertEqual(HOLDS,set(loc['holds']));self.assertEqual(7,len(loc['dependencies']))
   self.assertEqual(keys-HOLDS|set(loc['dependencies']),set(loc['accepted']));self.assertEqual(308 if tag=='hi' else 309,len(loc['changed']))
   self.assertEqual(set(loc['changed']),set(loc['predecessors']));self.assertLessEqual(set(loc['wording_only']),set(loc['accepted']))
 def test_complete_values_and_source_attributes(self):
  data=fixture(NAME);source=(ROOT/'Paintroid/src/main/res/values/strings.xml').read_text()
  for key,row in data['sources'].items():require_string(source,key,row['value'],{'attributes':row['attributes']})
  for tag,loc in data['locales'].items():
   xml=(ROOT/loc['catalogue_path']).read_text();root=ET.fromstring(xml)
   for key,value in loc['accepted'].items():
    require_string_root(root,key,value,{'attributes':loc['attributes'][key]})
    self.assertEqual(catalogues.placeholders(data['sources'][key]['value']),catalogues.placeholders(value))
   for key in loc['holds']:require_residual_or_previous(root,tag,key)
 def test_every_value_and_coordinated_metadata_mutation_rejected(self):
  data=fixture(NAME);require_reviewed_fixture(data)
  for tag,loc in data['locales'].items():
   for key in loc['accepted']:
    bad=deepcopy(data);bad['locales'][tag]['accepted'][key]+=' forged';bad['locales'][tag]['display']={key:'forged'}
    with self.assertRaises(ValueError):require_reviewed_fixture(bad)
   for field in ('changed','holds','wording_only','priority','dependencies'):
    bad=deepcopy(data);bad['locales'][tag][field].append('forged')
    with self.assertRaises(ValueError):require_reviewed_fixture(bad)
 def test_raw_complete_fixture_rejects_coordinated_rewrite(self):
  text=(ROOT/'tools/fixtures/current_localization'/NAME).read_text();validated_fixture_text(text)
  bad=json.loads(text);bad['locales']['hi']['accepted']['colour_converter_unavailable']='forged'
  with self.assertRaises(ValueError):validated_fixture_text(json.dumps(bad,ensure_ascii=False,indent=2)+'\n')
 def test_mutable_returns_cannot_poison_cached_accepted_baseline(self):
  original=current_row('hi','ui_undo');copy=current_row('hi','ui_undo')
  copy['attributes']['name']='forged';copy['previous_attributes']['name']='forged'
  self.assertEqual(original,current_row('hi','ui_undo'))
  copy=reviewed_fixture();copy['locales']['hi']['accepted']['ui_undo']='forged'
  self.assertEqual(original,current_row('hi','ui_undo'))
  with self.assertRaises(ValueError):require_reviewed_fixture(copy)
 def test_wrong_scope_and_unaccepted_keys_rejected(self):
  for tag,key in [('ms','ui_save'),('hi','ui_save_as'),('gu','not_a_key')]:
   with self.assertRaises(ValueError):current_row(tag,key)
 def test_each_actual_xml_rejects_truncation_placeholder_markup_and_attributes(self):
  for tag,loc in fixture(NAME)['locales'].items():
   for key,value in loc['accepted'].items():
    node=ET.Element('string',loc['attributes'][key]);node.text=value
    for kind in ('truncated','placeholder','attribute','markup'):
     bad=deepcopy(node)
     if kind=='truncated':bad.text=value[:-1]
     elif kind=='placeholder':bad.text=value+' %9$s'
     elif kind=='attribute':bad.set('translatable','false')
     else:ET.SubElement(bad,'b').text='extra'
     with self.assertRaises(ValueError):require_string('<resources>'+ET.tostring(bad,encoding='unicode')+'</resources>',key,value,{'attributes':loc['attributes'][key]})
 def test_preserved_conditional_crop_and_real_compositions(self):
  # Complete source clauses, not isolated keyword approval; Android tests execute formatting.
  for tag in TAGS:
   self.assertIn('%1$s',display(tag,'ui_trim_in_pixels'));self.assertIn('%1$s',display(tag,'ui_trim_in_percent'))
   self.assertIn('%1$s',display(tag,'formats22_animation_message'));self.assertIn('%2$s',display(tag,'formats22_animation_message'))
   self.assertIn('%1$d',display(tag,'formats22_at_least_frames'))
   self.assertNotIn('"',display(tag,'ui_undo'))
if __name__=='__main__':unittest.main()
