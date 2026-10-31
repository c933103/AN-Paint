"""Exact independently reviewed BO/DZ/Valencian resources; not fluency or device certification."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as E
import translation_catalogues as c
from current_localization_contracts import fixture, RESIDUAL_KEYS
from tibetan_dzongkha_valencian_priority_expectations import require_fixture_binding, require_edited_resource as bound_require_edited_resource
from tibetan_dzongkha_valencian_priority_expectations import inherited_held_display
from test_slovak_slovenian_catalan_priority_wording import token_contract

ROOT=Path(__file__).resolve().parents[1]
TAGS=('bo', 'dz', 'ca-ES-valencia')
DATA={tag:fixture('tibetan_dzongkha_valencian_priority_wording/'+tag+'.json') for tag in TAGS}
REVIEW_METADATA_SHA256={'bo': '80168ffc78a88fb3de1ac1a9b0753bfca01bef916633827e88398231c76acd27', 'dz': '031887b9934680ba595fea935ec9aaf89e35bab92e9d66a837d031b78c6e25ed', 'ca-ES-valencia': 'ae8d8cee0386817fcc6a52b0b00abc1abcb720ce288217273243803671310b6d'}
EDIT_COUNTS={'bo': 30, 'dz': 14, 'ca-ES-valencia': 270}
HOLD_COUNTS={'bo': 7, 'dz': 7, 'ca-ES-valencia': 8}

def resource(e):
 d={'value':e.text if e.tag=='string' else {x.get('quantity'):x.text for x in e},'attributes':dict(e.attrib)}
 if e.tag!='string':d['children_attributes']={x.get('quantity'):dict(x.attrib) for x in e}
 return d

def require_review_metadata(tag,data):
 return require_fixture_binding(tag,data)

def require_edited_resource(tag,key,element):
 return bound_require_edited_resource(tag,key,element,DATA[tag])

class TibetanDzongkhaValencianPriorityWordingTest(unittest.TestCase):
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
    else:
     from current_localization_contracts import require_residual_or_previous
     require_residual_or_previous(E.parse(ROOT/data['catalogue_path']).getroot(),tag,key)

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
   self.assertEqual(set(self.local[tag]),set(data['original_catalogue'])|set(data['values'])|RESIDUAL_KEYS.get(tag,set()))

 def test_full_tokens_newlines_and_android_syntax(self):
  for tag,data in DATA.items():
   for key,row in data['values'].items():
    pairs=[(row['source']['value'],row['reviewed_value'])] if row['type']=='string' else [(row['source']['value'].get(q,row['source']['value']['other']),v) for q,v in row['reviewed_value'].items()]
    for en,value in pairs:
     self.assertEqual(token_contract(en),token_contract(value),(tag,key))
     self.assertEqual(en.count('\\n'),value.count('\\n'))
     self.assertEqual([],c.android_string_errors(value))
     self.assertEqual([],c.format_string_errors(value,row['reviewed_attributes'].get('formatted')!='false'))

 def test_plural_quantities_and_all_three_crop_arguments(self):
  for tag in TAGS:
   e=self.local[tag]['ui_crop_preview_images'];self.assertEqual({'one','many','other'} if tag=='ca-ES-valencia' else {'other'},{x.get('quantity') for x in e})
   for child in e:
    self.assertIn('%1$d × %2$d',child.text);self.assertIn('%3$d',child.text);self.assertIn('\\n',child.text)

 def test_no_duplicate_identities(self):
  for tag,data in DATA.items():
   root=E.parse(ROOT/data['catalogue_path']).getroot();self.assertEqual(len(root),len(self.local[tag]))

 def test_exact_shared_warning_svg_and_tagged_colour_successor_guards(self):
  import memory_warning_source_review as memory
  import test_current_localization_contracts as current
  probes=0
  for tag in ('ca-ES-valencia',):
   name='tibetan_dzongkha_valencian_priority_wording/'+tag+'.json'
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
  self.assertEqual(17,probes)

 def test_finite_tagged_colour_addition_rejects_source_attributes_history_display_and_overwrite(self):
  import test_current_localization_contracts as current
  key=current.TAGGED_COLOUR_KEY
  for tag in ('ca-ES-valencia',):
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
    with self.subTest(tag=tag,mutation=mutation),self.assertRaises(ValueError):current.add_bo_dz_val_tagged_colour(expected,data)

 def test_warning_and_svg_additions_reject_source_attributes_and_omitted_predecessors(self):
  import memory_warning_source_review as memory
  import test_current_localization_contracts as current
  for tag in ('ca-ES-valencia',):
   name='tibetan_dzongkha_valencian_priority_wording/'+tag+'.json'
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

 def test_actual_accessors_reject_coordinated_fixture_and_target_mutation(self):
  from tibetan_dzongkha_valencian_priority_expectations import require_shared_row
  for tag,data in ((t,DATA[t]) for t in ('ca-ES-valencia',)):
   key=next(k for k,r in data['values'].items() if r['type']=='string')
   changed=deepcopy(data);changed['values'][key]['reviewed_value']+=' forged'
   element=deepcopy(self.local[tag][key]);element.text=changed['values'][key]['reviewed_value']
   with patch.dict(DATA,{tag:changed}):
    with self.subTest(tag=tag),self.assertRaises(ValueError):require_edited_resource(tag,key,element)
   for key in ('ui_assembly_source_memory_floor','ui_no_resize_fits_decoder_memory','commons_svg_original_size_too_large','commons_svg_original_size_unavailable','save20_unsupported_image_colour'):
    for mutation in ('type','value','coordinated','missingPrevious','previous','source','sourceAttributes','attributes'):
     changed=deepcopy(data);row=changed['values'][key]
     if mutation=='type':row['type']='plurals'
     elif mutation=='value':row['reviewed_value']='forged'
     elif mutation=='coordinated':row['reviewed_value']='"forged"';row['display']='forged'
     elif mutation=='missingPrevious':del row['previous_target']
     elif mutation=='previous':row['previous_target']='forged'
     elif mutation=='source':row['source']['value']='forged'
     elif mutation=='sourceAttributes':row['source']['attributes']['formatted']='false'
     else:row['reviewed_attributes']['formatted']='false'
     with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):require_shared_row(tag,key,changed)
    with self.assertRaises(ValueError):require_shared_row(tag,key,data,historical_value='forged')
    with self.assertRaises(ValueError):require_shared_row(tag,key,data,already_present=True)
   with self.assertRaises(ValueError):require_shared_row(tag,'ui_save',data)

 def test_strict_resource_and_catalogue_shape_rejects_unreviewed_text_and_children(self):
  from tibetan_dzongkha_valencian_priority_expectations import require_catalogue
  for tag,data in DATA.items():
   original=E.parse(ROOT/data['catalogue_path']).getroot();require_catalogue(tag,original,data)
   string_key=next(k for k,r in data['values'].items() if r['type']=='string')
   for mode in ('resource-tail','string-child','plural-parent','plural-tail','plural-child','plural-item-tag','plural-duplicate'):
    key=string_key if mode in ('resource-tail','string-child') else 'ui_crop_preview_images'
    element=deepcopy(self.local[tag][key])
    if mode=='resource-tail':element.tail='unreviewed'
    elif mode=='string-child':E.SubElement(element,'b').text='unreviewed'
    elif mode=='plural-parent':element.text='unreviewed'
    elif mode=='plural-tail':element[0].tail='unreviewed'
    elif mode=='plural-child':E.SubElement(element[0],'b').text='unreviewed'
    elif mode=='plural-item-tag':element[0].tag='string'
    else:element.append(deepcopy(element[0]))
    with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_edited_resource(tag,key,element)
   for mode in ('root-tag','root-attributes','root-text','root-tail','duplicate','extra','missing','resource-tail','nested-string','plural-parent','plural-tail'):
    root=deepcopy(original)
    if mode=='root-tag':root.tag='unreviewed'
    elif mode=='root-attributes':root.set('unreviewed','true')
    elif mode=='root-text':root.text='unreviewed'
    elif mode=='root-tail':root.tail='unreviewed'
    elif mode=='duplicate':root.append(deepcopy(root[0]))
    elif mode=='extra':E.SubElement(root,'string',name='unreviewed').text='unreviewed'
    elif mode=='missing':root.remove(root[0])
    elif mode=='resource-tail':root[0].tail='unreviewed'
    elif mode=='nested-string':E.SubElement(root.find('./string'),'b').text='unreviewed'
    elif mode=='plural-parent':root.find('./plurals').text='unreviewed'
    else:root.find('./plurals')[0].tail='unreviewed'
    with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_catalogue(tag,root,data)

 def test_display_and_all_hold_oracles_are_derived_from_raw_reviewed_resources(self):
  import re
  def decode(raw,resources,seen=()):
   if isinstance(raw,dict):return {q:decode(text,resources,seen) for q,text in raw.items()}
   if raw.startswith('@string/'):
    key=raw.split('/',1)[1]
    if key in seen:raise ValueError('Alias cycle')
    return decode(resources[key],resources,seen+(key,))
   if raw.startswith('"') and raw.endswith('"'):raw=raw[1:-1]
   else:raw=re.sub(r'\s+',' ',raw).strip()
   return re.sub(r'\\(.)',lambda m:{'n':'\n','r':'\r','t':'\t'}.get(m[1],m[1]),raw)
  english={key:resource(node)['value'] for key,node in self.en.items()}
  for tag,data in DATA.items():
   resources={key:row['value'] for key,row in data['original_catalogue'].items()}
   resources.update({key:row['reviewed_value'] for key,row in data['values'].items()})
   for key,row in {**data['context'],**data['values']}.items():
    self.assertEqual(decode(resources[key],resources),row['display'],(tag,key))
   self.assertEqual(set(data['holds']),{row['type']+'/'+key for key,row in data['held_display'].items()})
   fallback=dict(english)
   if tag=='ca-ES-valencia':fallback.update({node.get('name'):resource(node)['value'] for node in E.parse(ROOT/'Paintroid/src/main/res/values-ca/strings.xml').getroot()})
   for key,row in data['held_display'].items():
    prior=data['original_catalogue'].get(key)
    self.assertEqual(decode(prior['value'],resources) if prior else decode(self.local[tag][key].text,resources) if key in self.local[tag] else decode(fallback[key],fallback),inherited_held_display(tag,key,row['display']),(tag,key))

 def test_downstream_tagged_projection_rejects_coordinated_fixture_and_expected_value(self):
  import test_current_localization_contracts as current
  for tag in ('ca-ES-valencia',):
   data=current.current_tagged_colour_data();changed=deepcopy(DATA[tag]);key=current.TAGGED_COLOUR_KEY
   changed['values'][key]['reviewed_value']='"forged"';changed['values'][key]['display']='forged';data[tag]='forged'
   original=current.fixture;name='tibetan_dzongkha_valencian_priority_wording/'+tag+'.json'
   with patch.object(current,'fixture',side_effect=lambda n:changed if n==name else original(n)):
    with self.subTest(tag=tag),self.assertRaises(ValueError):current.tagged_colour_expectations(data)

 def test_every_retained_accepted_value_remains_source_bound_with_exact_attributes(self):
  for tag,data in DATA.items():
   for key,row in data['context'].items():
    with self.subTest(tag=tag,key=key):
     self.assertEqual(resource(self.en[key]),row['source'])
     self.assertEqual(row['reviewed_value'],resource(self.local[tag][key])['value'])
     self.assertEqual(row['reviewed_attributes'],self.local[tag][key].attrib)
     if row['type']=='plurals':self.assertEqual(row['reviewed_children_attributes'],resource(self.local[tag][key])['children_attributes'])
   self.assertEqual({'bo':349,'dz':349,'ca-ES-valencia':348}[tag],len(data['context'])+len(data['values']))

 def test_all_held_display_oracles_follow_direct_parent_and_default_resolution(self):
  from tibetan_dzongkha_valencian_priority_expectations import decode_android
  for tag,data in DATA.items():
   parent={e.get('name'):e for e in E.parse(ROOT/'Paintroid/src/main/res/values-ca/strings.xml').getroot()} if tag=='ca-ES-valencia' else {}
   resolved=dict(self.en);resolved.update(parent);resolved.update(self.local[tag])
   for identity in data['holds']:
    key=identity.split('/')[1];node=resolved[key];raw=node.text;seen=set()
    while raw.startswith('@string/'):
     target=raw.split('/',1)[1]
     self.assertNotIn(target,seen);seen.add(target);raw=resolved[target].text
    self.assertEqual('string',node.tag)
    self.assertEqual(decode_android(raw),inherited_held_display(tag,key,data['held_display'][key]['display']),(tag,key))
    changed=deepcopy(data);changed['held_display'][key]['display']+=' forged'
    with self.assertRaises(ValueError):require_review_metadata(tag,changed)
   if tag=='ca-ES-valencia':
    self.assertEqual('Principal',self.local[tag]['ui_main23'].text)
    self.assertEqual('Principal',data['held_display']['ui_main23']['display'])

 def test_exact_direct_valencian_successors_and_unchanged_catalan_parent(self):
  from current_localization_contracts import RESIDUAL_KEYS, residual_rows, require_residual_or_previous
  from tibetan_dzongkha_valencian_priority_expectations import decode_android
  tag='ca-ES-valencia';data=DATA[tag];rows=residual_rows()
  keys=set(RESIDUAL_KEYS[tag])
  self.assertEqual(8,len(keys))
  self.assertEqual(keys,set(data['held_display']))
  parent=E.parse(ROOT/'Paintroid/src/main/res/values-ca/strings.xml').getroot()
  direct=E.parse(ROOT/data['catalogue_path']).getroot()
  for key in keys:
   previous=data['held_display'][key]['display']
   self.assertEqual(decode_android(rows[(tag,key)]['target']),inherited_held_display(tag,key,previous,parent,direct))
   if key in RESIDUAL_KEYS['ca']:require_residual_or_previous(parent,'ca',key)
   for mutation in ('missing','duplicate','type','value','attribute','child','tail','previous'):
    local=deepcopy(direct);node=local.find(f"./string[@name='{key}']");old=previous
    if mutation=='missing':local.remove(node)
    elif mutation=='duplicate':local.append(deepcopy(node))
    elif mutation=='type':node.tag='plurals'
    elif mutation=='value':node.text+=' forged'
    elif mutation=='attribute':node.set('formatted','false')
    elif mutation=='child':E.SubElement(node,'b')
    elif mutation=='tail':node.tail='unreviewed'
    else:old+=' forged'
    with self.subTest(key=key,mutation=mutation),self.assertRaises(ValueError):
     inherited_held_display(tag,key,old,parent,local)
   for mutation in ('source','previous_target'):
    changed=deepcopy(rows);changed[(tag,key)][mutation]='forged'
    with patch('current_localization_contracts.residual_rows',return_value=changed):
     with self.subTest(key=key,mutation=mutation),self.assertRaises(ValueError):
      inherited_held_display(tag,key,previous,parent,direct)
  for other in ('bo','dz'):
   for key,row in DATA[other]['held_display'].items():
    self.assertEqual(row['display'],inherited_held_display(other,key,row['display']))

if __name__=='__main__':unittest.main()
