"""Exact independently reviewed KK/TG/PS resources; not fluency or device certification."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as E
import translation_catalogues as c
from current_localization_contracts import fixture
from test_slovak_slovenian_catalan_priority_wording import token_contract

ROOT=Path(__file__).resolve().parents[1]
TAGS=('kk','tg','ps')
DATA={tag:fixture('kazakh_tajik_pashto_priority_wording/'+tag+'.json') for tag in TAGS}
REVIEW_METADATA_SHA256={'kk': '395d99d0493d3d0439b6c30875576c1ed12c77541c2ca362ea2c85ed4b62d33b', 'tg': '9ea992815f0ac7eab22218f4cf452e4e5139e63b67924cbde7e0176c4d3ccaf6', 'ps': '28041fb4935b7a990691d1e8f0a00ea417d5ca00f62b63d0ce514c0c0a5da39f'}
EDIT_COUNTS={'kk': 260, 'tg': 346, 'ps': 324}
HOLD_COUNTS={'kk': 8, 'tg': 10, 'ps': 10}

def resource(e):
 d={'value':e.text if e.tag=='string' else {x.get('quantity'):x.text for x in e},'attributes':dict(e.attrib)}
 if e.tag!='string':d['children_attributes']={x.get('quantity'):dict(x.attrib) for x in e}
 return d

def require_review_metadata(tag,data):
 # Complete compact review contract, including predecessor history and JVM display/context fields.
 actual=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 if actual!=REVIEW_METADATA_SHA256[tag]:raise ValueError('Reviewed disposition/context differs: '+tag)

def require_edited_resource(tag,key,element):
 row=DATA[tag]['values'][key]
 if element is None or element.tag!=row['type'] or element.attrib!=row['reviewed_attributes']:
  raise ValueError('Reviewed resource type/attributes differ: '+tag+'/'+key)
 if resource(element)['value']!=row['reviewed_value']:raise ValueError('Complete reviewed text differs: '+tag+'/'+key)
 if element.tag=='plurals' and resource(element)['children_attributes']!=row['reviewed_children_attributes']:
  raise ValueError('Reviewed plural quantities/attributes differ: '+tag+'/'+key)

class KazakhTajikPashtoPriorityWordingTest(unittest.TestCase):
 def setUp(self):
  self.en={e.get('name'):e for e in E.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()}
  self.local={tag:{e.get('name'):e for e in E.parse(ROOT/data['catalogue_path']).getroot()} for tag,data in DATA.items()}

 def test_complete_priority_accounting_and_context_holds(self):
  tiers={key:tier['id'] for tier in json.loads((ROOT/'translations/string-importance.json').read_text())['tiers'] if tier['id'] in ('P0','P1') for key in tier['keys']}
  for tag,data in DATA.items():
   self.assertEqual({key:row['tier'] for key,row in data['priority_rows'].items()},tiers)
   require_review_metadata(tag,data)
   self.assertEqual(HOLD_COUNTS[tag],len(data['holds']))
   for identity in data['holds']:
    key=identity.split('/')[1];self.assertNotIn(key,data['values'])
    if key in data['original_catalogue']:self.assertEqual(resource(self.local[tag][key]),data['original_catalogue'][key])
    else:self.assertNotIn(key,self.local[tag])

 def test_disposition_contract_rejects_status_value_attributes_and_context_mutations(self):
  for tag,data in DATA.items():
   identity=next(iter(data['priority_rows']))
   for field in ('decision','reviewed_value','reviewed_attributes'):
    changed=deepcopy(data);changed['priority_rows'][identity][field]='unreviewed mutation'
    with self.assertRaises(ValueError):require_review_metadata(tag,changed)
   for field in ('holds','context_limited'):
    changed=deepcopy(data);changed[field]=[]
    with self.assertRaises(ValueError):require_review_metadata(tag,changed)
   key=next(iter(data['values']))
   for field in ('previous_target','display'):
    changed=deepcopy(data);changed['values'][key][field]='forged history/display'
    with self.assertRaises(ValueError):require_review_metadata(tag,changed)
   for field in ('original_catalogue','context'):
    changed=deepcopy(data);changed[field]['forged_identity']={'value':'forged'}
    with self.assertRaises(ValueError):require_review_metadata(tag,changed)

 def test_exact_source_and_typed_reviewed_edits(self):
  for tag,data in DATA.items():
   self.assertEqual(EDIT_COUNTS[tag],len(data['values']))
   for key,row in data['values'].items():
    with self.subTest(tag=tag,key=key):
     self.assertEqual(resource(self.en[key]),row['source'])
     require_edited_resource(tag,key,self.local[tag].get(key))

 def test_every_edited_target_rejects_complete_text_corruption_and_missing_resource(self):
  for tag,data in DATA.items():
   for key,row in data['values'].items():
    with self.subTest(tag=tag,key=key):
     changed=deepcopy(self.local[tag][key])
     if changed.tag=='string':changed.text=(changed.text or '')+' unreviewed mutation'
     else:changed[0].text=(changed[0].text or '')+' unreviewed mutation'
     with self.assertRaises(ValueError):require_edited_resource(tag,key,changed)
     with self.assertRaises(ValueError):require_edited_resource(tag,key,None)

 def test_every_edited_target_rejects_attribute_corruption(self):
  for tag,data in DATA.items():
   for key in data['values']:
    changed=deepcopy(self.local[tag][key]);changed.set('formatted','false' if changed.get('formatted')!='false' else 'true')
    with self.subTest(tag=tag,key=key),self.assertRaises(ValueError):require_edited_resource(tag,key,changed)

 def test_unrelated_resources_and_attributes_remain_exact(self):
  for tag,data in DATA.items():
   for key,row in data['original_catalogue'].items():
    if key not in data['values']:self.assertEqual(resource(self.local[tag][key]),row)
   self.assertEqual(set(self.local[tag]),set(data['original_catalogue'])|set(data['values']))

 def test_full_tokens_newlines_and_android_syntax(self):
  for tag,data in DATA.items():
   for key,row in data['values'].items():
    pairs=[(row['source']['value'],row['reviewed_value'])] if row['type']=='string' else [(row['source']['value'][q],v) for q,v in row['reviewed_value'].items()]
    for en,value in pairs:
     self.assertEqual(token_contract(en),token_contract(value),(tag,key))
     self.assertEqual(en.count('\\n'),value.count('\\n'))
     self.assertEqual([],c.android_string_errors(value))
     self.assertEqual([],c.format_string_errors(value,row['reviewed_attributes'].get('formatted')!='false'))

 def test_plural_quantities_and_all_three_crop_arguments(self):
  for tag in TAGS:
   e=self.local[tag]['ui_crop_preview_images'];self.assertEqual({'other'} if tag=='tg' else {'one','other'},{x.get('quantity') for x in e})
   for child in e:
    self.assertIn('%1$d × %2$d',child.text);self.assertIn('%3$d',child.text);self.assertIn('\\n',child.text)

 def test_no_duplicate_identities(self):
  for tag,data in DATA.items():
   root=E.parse(ROOT/data['catalogue_path']).getroot();self.assertEqual(len(root),len(self.local[tag]))

 def test_exact_shared_warning_svg_and_tagged_colour_successor_guards(self):
  import memory_warning_source_review as memory
  import test_current_localization_contracts as current
  probes=0
  for tag in TAGS:
   name='kazakh_tajik_pashto_priority_wording/'+tag+'.json'
   for key in memory.KEYS:
    with self.assertRaises(ValueError):memory.current_source_expectation(key,tag,'invented prior target')
    probes+=1
    for mutation in ('previous','source','attributes'):
     changed=deepcopy(DATA[tag]);row=changed['values'][key]
     if mutation=='previous':row['previous_target']={'value':'invented prior target','attributes':{'name':key}}
     elif mutation=='source':row['source']['value']+=' source corruption'
     else:row['reviewed_attributes']['formatted']='false'
     original=memory.fixture
     with patch.object(memory,'fixture',side_effect=lambda n:changed if n==name else original(n)):
      with self.assertRaises(ValueError):memory.current_source_expectation(key,tag,None)
     probes+=1
   for key in current.EXPECTED_KEYS[current.FAMILIES[2]]:
    for mutation in ('previous','source','attributes'):
     changed=deepcopy(DATA[tag]);row=changed['values'][key]
     if mutation=='previous':row['previous_target']={'value':'invented prior target','attributes':{'name':key}}
     elif mutation=='source':row['source']['value']+=' source corruption'
     else:row['reviewed_attributes']['formatted']='false'
     original=current.fixture
     with patch.object(current,'fixture',side_effect=lambda n:changed if n==name else original(n)):
      with self.assertRaises(ValueError):current.wording_fixture(current.FAMILIES[2])
     probes+=1
   changed=deepcopy(DATA[tag]);changed['values'][current.TAGGED_COLOUR_KEY]['previous_target']={'value':'forged'}
   original=current.fixture
   with patch.object(current,'fixture',side_effect=lambda n:changed if n==name else original(n)):
    with self.assertRaises(ValueError):current.current_tagged_colour_data()
   probes+=1
   for mutation in ('missing','wrong'):
    data=current.current_tagged_colour_data()
    if mutation=='missing':del data[tag]
    else:data[tag]='unreviewed replacement'
    with self.assertRaises(ValueError):current.tagged_colour_expectations(data)
    probes+=1
  self.assertEqual(51,probes)

 def test_finite_tagged_colour_addition_rejects_source_attributes_history_display_and_overwrite(self):
  import test_current_localization_contracts as current
  key=current.TAGGED_COLOUR_KEY
  for tag in TAGS:
   for mutation in ('source','sourceAttributes','missingPrevious','previous','attributes','display','raw','alreadyPresent'):
    data=deepcopy(DATA);row=data[tag]['values'][key];expected={}
    if mutation=='source':row['source']['value']='forged'
    elif mutation=='sourceAttributes':row['source']['attributes']['formatted']='false'
    elif mutation=='missingPrevious':del row['previous_target']
    elif mutation=='previous':row['previous_target']='forged'
    elif mutation=='attributes':row['reviewed_attributes']['formatted']='false'
    elif mutation=='display':row['display']='forged'
    elif mutation=='raw':row['reviewed_value']='forged'
    elif mutation=='alreadyPresent':expected[tag]='forged'
    with self.subTest(tag=tag,mutation=mutation),self.assertRaises(ValueError):current.add_kk_tg_ps_tagged_colour(expected,data)

 def test_warning_and_svg_additions_reject_source_attributes_and_omitted_predecessors(self):
  import memory_warning_source_review as memory
  import test_current_localization_contracts as current
  for tag in TAGS:
   name='kazakh_tajik_pashto_priority_wording/'+tag+'.json'
   for module,keys in ((memory,memory.KEYS),(current,current.EXPECTED_KEYS[current.FAMILIES[2]])):
    for key in keys:
     for mutation in ('sourceAttributes','missingPrevious'):
      changed=deepcopy(DATA[tag]);row=changed['values'][key]
      if mutation=='sourceAttributes':row['source']['attributes']['formatted']='false'
      else:del row['previous_target']
      original=module.fixture
      with patch.object(module,'fixture',side_effect=lambda n:changed if n==name else original(n)):
       with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):
        if module is memory:memory.current_source_expectation(key,tag,None)
        else:current.wording_fixture(current.FAMILIES[2])

if __name__=='__main__':unittest.main()
