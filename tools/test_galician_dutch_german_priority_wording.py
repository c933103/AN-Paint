"""Bounded complete-value and real-consumer guards for accepted GL/NL/DE changes."""
from copy import deepcopy
import json,re,unittest,xml.etree.ElementTree as E
import translation_catalogues as c
from current_localization_contracts import fixture,require_string
from gl_nl_de_priority_scope import SCOPE,PREVIOUS,HELD
FIXTURE='galician_dutch_german_priority_wording.json'
CLASSIC=c.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'
def display(v):
 if isinstance(v,dict):return {q:display(s) for q,s in v.items()}
 if v.startswith('"') and v.endswith('"'):v=v[1:-1]
 return re.sub(r'\\([\x27"])',r'\1',v).replace(r'\n','\n')
def shape(identity,v):
 kind,key=identity.split('/')
 if kind=='string':return isinstance(v,str) and bool(v)
 return kind=='plurals' and isinstance(v,dict) and set(v)=={'one','other'} and all(isinstance(s,str) and s for s in v.values())
def checked(data):
 if data.get('schema_version')!=1 or set(data.get('locales',{}))!=set(SCOPE):raise ValueError('Locale scope differs')
 for tag,groups in SCOPE.items():
  loc=data['locales'][tag]
  if set(loc)!=set(groups):raise ValueError('Group scope differs')
  for group,keys in groups.items():
   if set(loc[group])!=set(keys):raise ValueError('Typed scope differs')
   for identity,row in loc[group].items():
    key=identity.split('/')[1]
    if not shape(identity,row.get('source')) or row.get('source_attributes',{}).get('name')!=key:raise ValueError('Source shape differs')
    if row.get('attributes',{}).get('name')!=key:raise ValueError('Target identity differs')
    if row.get('target') is not None and not shape(identity,row['target']):raise ValueError('Target shape differs')
    if group=='held':
     if row.get('decision')!=HELD[tag][identity]:raise ValueError('Hold disposition differs')
    else:
     if row['target'] is None or row.get('display')!=display(row['target']):raise ValueError('Display differs')
     if group=='values':
      if not {'previous_target','previous_attributes'} <= set(row):raise ValueError('Required predecessor field absent')
      if (row.get('previous_target'),row.get('previous_attributes'))!=PREVIOUS[tag][identity]:raise ValueError('Predecessor differs')
      if row['target']==row['previous_target'] and row['attributes']==row['previous_attributes']:raise ValueError('Not a change')
      if row['attributes']!=row['source_attributes']:raise ValueError('Changed attributes differ from source')
 return data['locales']
def require_entry(xml,identity,row,field='target'):
 kind,key=identity.split('/');target=row[field];attrs=row['source_attributes'] if field=='source' else row['attributes']
 if target is None:
  if E.fromstring(xml).findall(f"./{kind}[@name='{key}']"):raise ValueError('Expected exact absence')
  return
 if kind=='string':return require_string(xml,key,target,{'attributes':attrs,'formatted':attrs.get('formatted')!='false','placeholders':c.placeholders(row['source']),'escaped_newline_count':target.count(r'\n')})
 nodes=E.fromstring(xml).findall(f"./plurals[@name='{key}']")
 if len(nodes)!=1:raise ValueError('Plural count differs')
 n=nodes[0]
 if n.attrib!=attrs or len(n)!=len(target) or {x.get('quantity') for x in n}!=set(target):raise ValueError('Plural scope differs')
 for child in n:
  q=child.get('quantity');value=child.text or ''
  if child.tag!='item' or child.attrib!={'quantity':q} or len(child) or value!=target[q]:raise ValueError('Plural child differs')
  if c.placeholders(value)!=c.placeholders(row['source'][q]) or value.count(r'\n')!=row['source'][q].count(r'\n'):raise ValueError('Plural arguments/newlines differ')
  if c.android_string_errors(value) or c.format_string_errors(value,True):raise ValueError('Plural syntax differs')
class GalicianDutchGermanPriorityWordingTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=fixture(FIXTURE);cls.locales=checked(cls.data);cls.xml={t:c.catalogue_paths()[t].read_text() for t in SCOPE};cls.en=(c.RES/'values/strings.xml').read_text()
 def test_complete_changed_and_reviewed_context_values_bind_current_english(self):
  self.assertEqual(281,sum(len(v['values']) for v in self.locales.values()))
  for tag,loc in self.locales.items():
   for group in ['values','context']:
    for identity,row in loc[group].items():
     with self.subTest(tag=tag,identity=identity):require_entry(self.xml[tag],identity,row);require_entry(self.en,identity,row,'source')
 def test_each_precise_present_or_absent_hold_remains_exact(self):
  for tag,loc in self.locales.items():
   for identity,row in loc['held'].items():
    with self.subTest(tag=tag,identity=identity):require_entry(self.xml[tag],identity,row);require_entry(self.en,identity,row,'source')
 def test_every_changed_scalar_and_plural_child_rejects_corruption(self):
  for tag,loc in self.locales.items():
   for identity,row in loc['values'].items():
    kind,key=identity.split('/')
    for q in list(row['target']) if kind=='plurals' else [None]:
     for mutation in ['truncate','argument','markup','attribute']:
      root=E.fromstring(self.xml[tag]);node=root.find(f"./{kind}[@name='{key}']");child=node if q is None else node.find(f"./item[@quantity='{q}']")
      if mutation=='truncate':child.text=(child.text or '')[:-1]
      elif mutation=='argument':child.text=(child.text or '')+' %9$s'
      elif mutation=='markup':E.SubElement(child,'b').text='unexpected'
      else:child.set('unexpected','true')
      with self.subTest(tag=tag,identity=identity,q=q,mutation=mutation),self.assertRaises(ValueError):require_entry(E.tostring(root,encoding='unicode'),identity,row)
 def test_each_changed_resource_rejects_absence_duplication_and_wrong_type(self):
  for tag,loc in self.locales.items():
   for identity,row in loc['values'].items():
    kind,key=identity.split('/')
    for mutation in ['missing','duplicate','wrong-type']:
     root=E.fromstring(self.xml[tag]);node=root.find(f"./{kind}[@name='{key}']")
     if mutation=='missing':root.remove(node)
     elif mutation=='duplicate':root.append(deepcopy(node))
     else:node.tag='plurals' if kind=='string' else 'string'
     with self.subTest(tag=tag,identity=identity,mutation=mutation),self.assertRaises(ValueError):require_entry(E.tostring(root,encoding='unicode'),identity,row)
 def test_every_changed_predecessor_is_exact_and_cannot_replace_current_value(self):
  for tag,loc in self.locales.items():
   for identity,row in loc['values'].items():
    kind,key=identity.split('/');root=E.fromstring(self.xml[tag]);node=root.find(f"./{kind}[@name='{key}']")
    if row['previous_target'] is None:root.remove(node)
    else:
     node.attrib=dict(row['previous_attributes'])
     if kind=='string':node.text=row['previous_target']
     else:
      for child in node:child.text=row['previous_target'][child.get('quantity')]
    with self.subTest(tag=tag,identity=identity),self.assertRaises(ValueError):require_entry(E.tostring(root,encoding='unicode'),identity,row)
 def test_fixture_cannot_shrink_or_expand_typed_groups_or_relabel_holds(self):
  for tag in SCOPE:
   for group in SCOPE[tag]:
    for mutation in ['remove','add']:
     data=deepcopy(self.data);rows=data['locales'][tag][group];key=next(iter(rows))
     if mutation=='remove':rows.pop(key)
     else:rows['string/unreviewed']=deepcopy(rows[key])
     with self.subTest(tag=tag,group=group,mutation=mutation),self.assertRaises(ValueError):checked(data)
  data=deepcopy(self.data);row=next(iter(data['locales']['gl']['held'].values()));row['decision']='accept';self.assertRaises(ValueError,checked,data)
 def test_display_predecessor_and_full_plural_shape_are_not_optional(self):
  for mutation in ['display','previous','quantity','attributes','locale']:
   data=deepcopy(self.data);row=data['locales']['gl']['values']['string/formats22_animation_message']
   if mutation=='display':row['display']+=' wrong'
   elif mutation=='previous':row['previous_target']='fabricated predecessor'
   elif mutation=='quantity':data['locales']['nl']['values']['plurals/ui_crop_preview_images']['target'].pop('other')
   elif mutation=='attributes':row['attributes']['formatted']='false'
   else:data['locales']['gl-ES']=data['locales'].pop('gl')
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):checked(data)
 def test_catalogues_keep_unique_typed_entries_and_manifest_priority_counts(self):
  manifest=json.loads((c.ROOT/'translations/string-importance.json').read_text());tiers={t['id']:set(t['keys']) for t in manifest['tiers']}
  self.assertEqual(92,len(tiers['P0']));self.assertEqual(249,len(tiers['P1']))
  for tag,xml in self.xml.items():
   typed=[n.tag+'/'+n.get('name') for n in E.fromstring(xml)];self.assertEqual(len(typed),len(set(typed)))
   self.assertEqual([],c.validate_catalogue(tag,require_complete=tag!='gl'))
 def test_real_callers_retain_atomic_replacement_and_bidirectional_scaling(self):
  for name in ['BitmapFileCodec.kt','DibCodec.kt','IcoCodec.kt','TextImageCodec.kt']:
   source=(CLASSIC/name).read_text();self.assertRegex(source,r'if \(!temporary.renameTo\((?:file|destination)\)\) throw IOException\(ui\(R.string.save20_destination_error\)\)')
  source=(CLASSIC/'ClassicPaintActivity.kt').read_text()
  for token in ['locked = stretch','document.resize(size.width,size.height,stretch)','R.string.ui_scales_the_image_unlock_the_ratio_to_stretch','R.string.ui_keeps_pixels_at_the_top_left_smaller_canvas','chooseTool(drawingTool)']:self.assertIn(token,source)
 def test_jvm_draft_exercises_compiled_values_and_real_state_changes(self):
  source=(c.ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/GalicianDutchGermanPriorityWordingTest.kt').read_text()
  self.assertEqual(14,len(re.findall(r'@Test\s+fun\s+',source)))
  for token in ['for(identity in values.keys())','for(count in 0..125)','ImageDimensions(4,9)','ImageDimensions(12,3)','controls.aspectLock.performClick()','assertSame(bitmap,activity.document.bitmap)','assertArrayEquals(original,restored)','ImageCropDialog(','ImportSelection(','ImageResizeDialog(','SaveOptionsDialog(','recoverEditor(context,store)','ToolCategoryButton(']:self.assertIn(token,source)
 def test_finite_prior_corrections_reject_changed_sources_predecessors_and_attributes(self):
  from unittest.mock import patch
  import galician_priority_expectations as successors
  for tag,key in successors.WORDING_CORRECTIONS:
   original=self.data['locales'][tag]['values']['string/'+key]
   self.assertEqual(original['target'],successors.wording_successor(tag,key,original['previous_target']))
   for field in ['source','source_attributes','previous_target','previous_attributes','attributes','display','target']:
    changed=deepcopy(self.data);row=changed['locales'][tag]['values']['string/'+key]
    row[field]={'name':'unreviewed'} if field.endswith('attributes') else 'corrupted full value'
    with self.subTest(tag=tag,key=key,field=field),patch.object(successors,'fixture',return_value=changed),self.assertRaises(ValueError):
     successors.wording_successor(tag,key,original['previous_target'])
  self.assertRaises(ValueError,successors.wording_successor,'gl','ui_swap_foreground_background','old')

 def test_finite_additions_and_corrections_reject_missing_reviewed_fields(self):
  from unittest.mock import patch
  import galician_priority_expectations as successors
  for tag,key in successors.ADDITIONS | successors.WORDING_CORRECTIONS:
   original=self.data['locales'][tag]['values']['string/'+key]
   for field in ['source','source_attributes','previous_target','previous_attributes','attributes','display','target']:
    changed=deepcopy(self.data);changed['locales'][tag]['values']['string/'+key].pop(field)
    with self.subTest(tag=tag,key=key,missing=field),patch.object(successors,'fixture',return_value=changed),self.assertRaises(ValueError):
     if (tag,key) in successors.ADDITIONS:successors.current_row(tag,key)
     else:successors.wording_successor(tag,key,original['previous_target'])

 def test_all_changed_values_require_explicit_predecessor_fields_even_for_null(self):
  checked_fields=0
  for tag,loc in self.locales.items():
   for identity in loc['values']:
    for field in ['previous_target','previous_attributes']:
     data=deepcopy(self.data);data['locales'][tag]['values'][identity].pop(field)
     with self.subTest(tag=tag,identity=identity,missing=field),self.assertRaises(ValueError):checked(data)
     checked_fields+=1
  self.assertEqual(562,checked_fields)

if __name__=='__main__':unittest.main()
