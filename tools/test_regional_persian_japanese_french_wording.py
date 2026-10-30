import unittest,json,tempfile,xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
import regional_persian_japanese_french_expectations as e
import translation_catalogues as cat
ROOT=Path(__file__).resolve().parents[1]
class RegionalPersianJapaneseFrench(unittest.TestCase):
 def setUp(self):
  self.data=e.reviewed_fixture();self.catalogues={t:e.typed_catalogue(ROOT/l['catalogue_path'])for t,l in self.data['locales'].items()};self.english=e.typed_catalogue(cat.RES/'values/strings.xml');self.fa=e.typed_catalogue(cat.RES/'values-fa/strings.xml')
 def check(self):return e.check_catalogues(self.data,self.catalogues,self.english,self.fa)
 def test_all_complete_values_attributes_and_inheritance(self):self.assertTrue(self.check())
 def test_scope_holds_and_only_seven_existing_revisions(self):
  priority={k for tier in json.loads((cat.DATA/'string-importance.json').read_text())['tiers']if tier['id']in('P0','P1')for k in tier['keys']}
  self.assertEqual(341,len(priority))
  for tag,loc in self.data['locales'].items():
   self.assertTrue(priority.issubset(loc['rows']));self.assertEqual(16,len(set(loc['rows'])-priority))
   rows=loc['rows'];self.assertEqual(357,len(rows));self.assertEqual(8,sum(r['disposition']=='hold_preserved'for r in rows.values()));self.assertEqual(30,sum(r['consumer_binding']=='no_direct_consumer_in_packet'for r in rows.values()))
   changed=[r for r in rows.values()if r['direct']!=r['previous_direct']];self.assertEqual({'fa-IR':5,'ja':0,'fr':2}[tag],len(changed));self.assertTrue(all(r['previous_direct']is not None for r in changed))
  self.assertEqual(303,sum(r['disposition']=='carry_generic_no_duplicate_credit'for r in self.data['locales']['fa-IR']['rows'].values()))
 def test_seven_base_persian_successors_are_inherited_not_direct_or_main_credit(self):
  from current_localization_contracts import RESIDUAL_KEYS
  self.assertEqual(7,len(RESIDUAL_KEYS['fa']))
  for key in RESIDUAL_KEYS['fa']:
   identity='string/'+key
   self.assertNotIn(identity,self.catalogues['fa-IR'])
   for mutation in ('missing','value','attributes','direct'):
    parent=deepcopy(self.fa);cats=deepcopy(self.catalogues)
    if mutation=='missing':del parent[identity]
    elif mutation=='value':parent[identity]['value']+=' forged'
    elif mutation=='attributes':parent[identity]['attributes']['formatted']='false'
    else:cats['fa-IR'][identity]=deepcopy(parent[identity])
    with self.subTest(key=key,mutation=mutation),self.assertRaises(ValueError):e.check_catalogues(self.data,cats,self.english,parent)
  main=self.data['locales']['fa-IR']['rows']['string/ui_main23']
  self.assertEqual('hold_preserved',main['disposition']);self.assertIsNone(main['effective'])
  self.assertEqual(main['previous_direct'],self.catalogues['fa-IR']['string/ui_main23'])
 def test_every_coordinated_target_and_resource_corruption_rejected(self):
  for tag,loc in e.reviewed_fixture()['locales'].items():
   for identity,row in loc['rows'].items():
    if row['effective']is None:continue
    bad=e.reviewed_fixture();r=bad['locales'][tag]['rows'][identity];r['effective']['value']='forged'
    cats=deepcopy(self.catalogues);parent=deepcopy(self.fa)
    if r['direct']is not None:r['direct']['value']='forged';cats[tag][identity]=deepcopy(r['direct'])
    else:parent[identity]=deepcopy(r['effective'])
    with self.assertRaises(ValueError,msg=tag+'/'+identity):e.check_catalogues(bad,cats,self.english,parent)
 def test_metadata_display_and_missing_predecessor_rejected(self):
  for key in ['previous_direct','source','origin','disposition','consumer_binding','direct','effective']:
   bad=e.reviewed_fixture();del bad['locales']['fa-IR']['rows']['string/ui_airbrush'][key]
   with self.assertRaises(ValueError):e.require_reviewed_fixture(bad)
  for key in ['display','review_receipt_sha256','source_base','limit']:
   bad=e.reviewed_fixture();bad[key]='forged'
   with self.assertRaises(ValueError):e.require_reviewed_fixture(bad)
  altered=e.reviewed_fixture();altered['locales']['fr']['rows'].clear();self.assertEqual(357,len(e.reviewed_fixture()['locales']['fr']['rows']))
 def test_wrong_parent_and_direct_override_rejected(self):
  k='string/save20_unsupported_image_colour';self.assertNotIn(k,self.catalogues['fa-IR']);self.fa[k]['value']='wrong parent'
  with self.assertRaises(ValueError):self.check()
  self.fa=e.typed_catalogue(cat.RES/'values-fa/strings.xml');self.catalogues['fa-IR'][k]=deepcopy(self.fa[k])
  with self.assertRaises(ValueError):self.check()
 def test_every_placeholder_and_android_syntax(self):
  for tag,l in self.data['locales'].items():
   for identity,r in l['rows'].items():
    if r['effective']is None:continue
    v=r['effective']['value'];s=r['source']['value'];s=s['other']if isinstance(s,dict)else s
    for text in v.values()if isinstance(v,dict)else[v]:
     if text.startswith('@string/'):continue
     self.assertEqual(cat.placeholders(s),cat.placeholders(text),(tag,identity));self.assertEqual([],cat.android_string_errors(text),(tag,identity))
 def test_changed_resources_reject_old_missing_duplicate_markup_wrong_type(self):
  for tag,l in self.data['locales'].items():
   for identity,row in l['rows'].items():
    if row['direct']==row['previous_direct']:continue
    key=identity.split('/')[1]
    for mutation in ['old','missing','duplicate','markup','type','attribute','tail']:
     root=ET.parse(ROOT/l['catalogue_path']).getroot();n=root.find("./string[@name='%s']"%key)
     if mutation=='old':n.text=row['previous_direct']['value'];n.attrib=row['previous_direct']['attributes'].copy()
     elif mutation=='missing':root.remove(n)
     elif mutation=='duplicate':root.append(deepcopy(n))
     elif mutation=='markup':ET.SubElement(n,'b').text='forged'
     elif mutation=='type':n.tag='plurals'
     elif mutation=='attribute':n.set('translatable','false')
     elif mutation=='tail':n.tail='forged'
     with tempfile.TemporaryDirectory()as tmp:
      path=Path(tmp)/'strings.xml';ET.ElementTree(root).write(path,encoding='unicode')
      with self.assertRaises(ValueError,msg=tag+'/'+identity+'/'+mutation):
       cats=deepcopy(self.catalogues);cats[tag]=e.typed_catalogue(path);e.check_catalogues(self.data,cats,self.english,self.fa)
 def test_finite_fixture_bytes_reject_even_coordinated_fixture_rewrite(self):
  with self.assertRaises(ValueError):e.validated_fixture_text(json.dumps(self.data,ensure_ascii=False))
 def test_quality_and_all_eight_french_compositions(self):
  r=self.data['locales']['fa-IR']['rows']['string/ui_quality']['effective'];self.assertEqual('false',r['attributes']['formatted']);self.assertEqual('"کیفیت (%)"',r['value'])
  rows=self.data['locales']['fr']['rows']
  for key,unit in [('ui_trim_in_pixels','pixels'),('ui_trim_in_percent','pourcentage')]:
   template=rows['string/'+key]['effective']['value'].strip('"')
   for edge in ['ui_left','ui_top','ui_right','ui_bottom']:
    label=rows['string/'+edge]['effective']['value'];self.assertEqual(label+' : rognage en '+unit,template.replace('%1$s',label))
if __name__=='__main__':unittest.main()
