"""Complete reviewed pairs plus concrete grammar, fixture and resource rejection checks."""
import copy,json,tempfile,unittest,xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
import translation_catalogues as catalogues
import north_korean_australian_priority_expectations as contracts

class NorthKoreanAustralianPriorityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=contracts.bind_fixture();cls.source=(catalogues.RES/'values/strings.xml').read_text();cls.paths=catalogues.catalogue_paths();cls.targets={tag:cls.paths[tag].read_text()for tag in cls.data['locales']}
 def test_complete_accepted_values_and_existing_holds(self):
  for tag in self.targets:
   self.assertEqual({'accepted':348,'existing_holds':11},contracts.validate_catalogue(tag,self.source,self.targets[tag]))
 def test_priority_and_companion_inventory_is_exact(self):
  tiers=json.loads((catalogues.DATA/'string-importance.json').read_text())['tiers'];priority={key for t in tiers if t['id']in('P0','P1')for key in t['keys']}
  self.assertEqual(341,len(priority));self.assertEqual(359,len(self.data['sources']));self.assertTrue(priority<set(self.data['sources']))
  for loc in self.data['locales'].values():self.assertFalse(set(loc['accepted'])&set(loc['held']));self.assertEqual(set(self.data['sources']),set(loc['accepted'])|set(loc['held']))
 def test_every_standalone_complete_row_rejects_target_and_source_replacements(self):
  for tag,loc in self.data['locales'].items():
   for ident,row in loc['accepted'].items():
    source=self.data['sources'][ident];contracts.require_complete(tag,ident,source,row)
    for which in ('source','target'):
     a,b=copy.deepcopy(source),copy.deepcopy(row);x=a if which=='source'else b
     if isinstance(x['value'],dict):x['value']['other']+=' CHANGED'
     else:x['value']+=' CHANGED'
     with self.assertRaises(ValueError,msg=(tag,ident,which)):contracts.require_complete(tag,ident,a,b)
 def test_complete_supplied_fixture_rejects_unrelated_and_coordinated_changes(self):
  for tag in self.data['locales']:
   for field in ('accepted','held'):
    bad=copy.deepcopy(self.data);key=next(iter(bad['locales'][tag][field]));bad['locales'][tag][field][key]['value']='replacement'
    with self.assertRaises(ValueError):contracts.bind_fixture(bad)
   bad=copy.deepcopy(self.data);key='string/ui_save';bad['sources'][key]['value']='Changed';bad['locales'][tag]['accepted'][key]['value']='Changed'
   with self.assertRaises(ValueError):contracts.bind_fixture(bad)
  for value in (None,False,[],{},1):
   if value is None:continue
   with self.assertRaises(ValueError):contracts.bind_fixture(value)
 def test_raw_disk_fixture_binding_is_fresh(self):
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'fixture.json';p.write_bytes(contracts.FIXTURE.read_bytes())
   with patch.object(contracts,'FIXTURE',p):
    contracts.bind_fixture();p.write_text(p.read_text()+' ')
    with self.assertRaises(ValueError):contracts.bind_fixture()
 def test_strings_reject_wrong_type_duplicate_markup_attributes_and_tails(self):
  for tag,loc in self.data['locales'].items():
   ident='string/ui_save';row=loc['accepted'][ident]
   for mode in ('type','duplicate','child','attribute','tail','text'):
    root=ET.fromstring(self.targets[tag]);n=root.find("string[@name='ui_save']")
    if mode=='type':n.tag='plurals'
    elif mode=='duplicate':root.append(copy.deepcopy(n))
    elif mode=='child':ET.SubElement(n,'b').text='hidden'
    elif mode=='attribute':n.set('formatted','true'if n.get('formatted')=='false'else'false')
    elif mode=='tail':n.tail='hidden'
    else:n.text+='different'
    with self.assertRaises(ValueError,msg=(tag,mode)):contracts.require_resource(root,ident,row)
 def test_plurals_reject_parent_resource_item_tail_and_quantity_mutations(self):
  ident='plurals/ui_crop_preview_images'
  for tag,loc in self.data['locales'].items():
   for mode in ('parenttext','resourcetail','itemtail','duplicate','attribute','quantity','nested','missing'):
    root=ET.fromstring(self.targets[tag]);n=root.find("plurals[@name='ui_crop_preview_images']");child=n[0]
    if mode=='parenttext':n.text='hidden'
    elif mode=='resourcetail':n.tail='hidden'
    elif mode=='itemtail':child.tail='hidden'
    elif mode=='duplicate':n.append(copy.deepcopy(child))
    elif mode=='attribute':child.set('formatted','false')
    elif mode=='quantity':child.set('quantity','few')
    elif mode=='nested':ET.SubElement(child,'b').text='hidden'
    else:n.remove(child)
    with self.assertRaises(ValueError,msg=(tag,mode)):contracts.require_resource(root,ident,loc['accepted'][ident])
 def test_actual_corrections_preserve_complete_actions_and_units(self):
  au=self.data['locales']['en-AU']['accepted'];kp=self.data['locales']['ko-KP']['accepted']
  for key,value in {'ui_save_a5d0d9':'Save…','ui_draw_again':'Resume drawing','ui_colour_tab23':'Colour','ui_percent':'Per cent','ui_percent_fd8671':'per cent','ui_trim_in_percent':'%1$s trim in per cent','ui_quality':'Quality (%)'}.items():self.assertEqual(value,au['string/'+key]['value'])
  self.assertEqual({'name':'ui_quality','formatted':'false'},au['string/ui_quality']['attributes']);self.assertEqual('보관…',kp['string/ui_save_a5d0d9']['value']);self.assertEqual('계속 그리기',kp['string/ui_draw_again']['value']);self.assertEqual('모두 선택 해제',kp['string/ui_none']['value'])
  self.assertIn('「이동 및 확대·축소」',kp['string/ui_drawing_canvas_pinch_and_move_two_fingers_to']['value'])
  for key in ('gallery_credit_could_not_save','gallery_credit_too_large','legacy_credits_unreadable'):self.assertIn('저작자·출처·리용허가',kp['string/'+key]['value'])
 def test_existing_hold_replacement_is_rejected_without_acceptance_credit(self):
  for tag,loc in self.data['locales'].items():
   ident=next(iter(loc['held']));typ,key=ident.split('/');root=ET.fromstring(self.targets[tag]);root.find(f"{typ}[@name='{key}']").text='new guessed wording'
   with self.assertRaises(ValueError):contracts.validate_catalogue(tag,self.source,ET.tostring(root,encoding='unicode'))
if __name__=='__main__':unittest.main()

class NorthKoreanHistoricalSuccessorTests(unittest.TestCase):
 def test_exact_three_historical_warning_successors_and_corruption_rejection(self):
  original=json.loads((catalogues.ROOT/'tools/fixtures/current_localization/korean_image_attribution.json').read_text())['entries'];current=contracts.current_kp_attribution_entries(original)
  changed=[a['key']for a,b in zip(original,current)if a!=b]
  self.assertEqual({'gallery_credit_could_not_save','gallery_credit_too_large','legacy_credits_unreadable'},set(changed));self.assertEqual(3,len(changed))
  for index in range(len(original)):
   bad=copy.deepcopy(original);bad[index]['value']+=' mutation'
   with self.assertRaises(ValueError):contracts.current_kp_attribution_entries(bad)
  for bad in (original[:-1],original+[original[0]],list(reversed(original))):
   with self.assertRaises(ValueError):contracts.current_kp_attribution_entries(bad)
