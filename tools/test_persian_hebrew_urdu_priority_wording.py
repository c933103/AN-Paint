"""Complete independently reviewed FA/HE/UR inventories, typed resources and fail-closed successors."""
from collections import Counter
from copy import deepcopy
import json
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import translation_catalogues as cat
from current_localization_contracts import fixture,require_string as scalar
from persian_hebrew_urdu_priority_expectations import NAME,TAGS,require_reviewed_fixture,reviewed_fixture,validated_fixture_text,current_row,current_value,display,compiled_display,require_addition,MEMORY_ADDITIONS
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png','ui_foreground_background_colour_palette','ui_main23','ui_pinch_and_pan_mode'}
def require_resource(xml,identity,target,attrs):
    root=ET.fromstring(xml);kind,key=identity.split('/')
    if root.tag!='resources'or root.attrib or(root.text or '').strip()or any((n.tail or '').strip()for n in root):raise ValueError('Root/tail shape')
    matches=[n for n in root if n.get('name')==key]
    if len(matches)!=1 or matches[0].tag!=kind:raise ValueError('Typed identity')
    n=matches[0]
    if n.attrib!=attrs:raise ValueError('Attributes')
    if kind=='string':return scalar(xml,key,target,{'attributes':attrs})
    if kind!='plurals'or(n.text or '').strip():raise ValueError('Plural parent')
    if len(n)!=len(target)or {c.get('quantity')for c in n}!=set(target):raise ValueError('Plural quantities')
    for c in n:
        if c.tag!='item'or c.attrib!={'quantity':c.get('quantity')}or len(c)or(c.tail or '').strip()or c.text!=target[c.get('quantity')]:raise ValueError('Complete plural child')
def resource(identity,target,attrs):
    root=ET.Element('resources');n=ET.SubElement(root,identity.split('/')[0],attrs)
    if isinstance(target,dict):
        for q,v in target.items():ET.SubElement(n,'item',{'quantity':q}).text=v
    else:n.text=target
    return root,n
class PersianHebrewUrduTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=require_reviewed_fixture(fixture(NAME));cls.xml={t:(cat.ROOT/l['path']).read_text()for t,l in cls.data['locales'].items()};cls.english=(cat.RES/'values/strings.xml').read_text()
    def test_three_complete_priority_inventories_and_explicit_unaccepted_limits(self):
        expected={k.split('/')[1]:t['id']for t in json.loads((cat.DATA/'string-importance.json').read_text())['tiers']if t['id']in ('P0','P1')for k in t['keys']}
        self.assertEqual(TAGS,set(self.data['locales']))
        for t,l in self.data['locales'].items():
            self.assertEqual(expected,{k:r['tier']for k,r in l['priority_dispositions'].items()})
            self.assertEqual(Counter({'P0':92,'P1':249}),Counter(r['tier']for r in l['priority_dispositions'].values()))
            self.assertEqual(HOLDS,set(l['held_absent'])|set(l['held_present']))
            self.assertEqual({'fa':262,'he':266,'ur':322}[t],len(l['changed']))
            self.assertEqual(set(expected)-HOLDS,set(expected)&set(l['accepted']))
            for k in l['held_absent']:self.assertIsNone(ET.fromstring(self.xml[t]).find(f"./*[@name='{k}']"))
            for i,r in l['preserved_unreviewed'].items():require_resource(self.xml[t],i,r['target'],r['attributes'])
            self.assertEqual([],cat.validate_catalogue(t,require_complete=False))
    def test_all_complete_scalar_plural_values_attributes_and_placeholder_contracts(self):
        for t,l in self.data['locales'].items():
            entries={"string/"+k:{'target':v,'attributes':l['target_attribute_exceptions'].get(k,{'name':k})}for k,v in l['accepted'].items()}
            entries.update({'plurals/'+k:v for k,v in l['plurals'].items()})
            for identity,r in entries.items():
                src=self.data['sources'][identity]
                with self.subTest(t=t,identity=identity):
                    require_resource(self.english,identity,src['source'],src['attributes']);require_resource(self.xml[t],identity,r['target'],r['attributes'])
                    texts=list(r['target'].values())if isinstance(r['target'],dict)else[r['target']]
                    source=src['source']['other']if isinstance(src['source'],dict)else src['source']
                    for text in texts:self.assertEqual(cat.placeholders(source),cat.placeholders(text));self.assertEqual([],cat.android_string_errors(text))
    def test_every_change_rejects_old_missing_duplicate_wrong_type_markup_and_shape(self):
        for t,l in self.data['locales'].items():
            for identity in l['changed']:
                kind,k=identity.split('/');r=current_row(t,k)if kind=='string'else l['plurals'][k]
                for mutation in ('old','missing','duplicate','wrong-type','markup','attribute','root-text','root-attribute','tail','truncated'):
                    root,n=resource(identity,r['target'],r['attributes'])
                    if mutation=='old':
                        old=l['predecessors'].get(identity);root,n=resource(identity,''if old is None else old['target'],r['attributes'])
                    elif mutation=='missing':root.remove(n)
                    elif mutation=='duplicate':root.append(deepcopy(n))
                    elif mutation=='wrong-type':ET.SubElement(root,'plurals'if kind=='string'else'string',{'name':k})
                    elif mutation=='markup':ET.SubElement(n if kind=='string'else n[0],'b').text='extra'
                    elif mutation=='attribute':n.set('translatable','false')
                    elif mutation=='root-text':root.text='extra'
                    elif mutation=='root-attribute':root.set('extra','true')
                    elif mutation=='tail':n.tail='extra'
                    elif kind=='string':n.text=n.text[:-1]
                    else:n[0].text=n[0].text[:-1]
                    with self.subTest(t=t,key=k,mutation=mutation),self.assertRaises(ValueError):require_resource(ET.tostring(root,encoding='unicode'),identity,r['target'],r['attributes'])
    def test_plural_quantity_and_child_attribute_mutations_reject(self):
        for t in TAGS:
            r=self.data['locales'][t]['plurals']['ui_crop_preview_images']
            for mutation in ('missing','extra','duplicate','attribute','parent-text','child-tail'):
                root,n=resource('plurals/ui_crop_preview_images',r['target'],r['attributes'])
                if mutation=='missing':n.remove(n[0])
                elif mutation=='extra':ET.SubElement(n,'item',{'quantity':'zero'}).text='extra'
                elif mutation=='duplicate':n.append(deepcopy(n[0]))
                elif mutation=='attribute':n[0].set('formatted','false')
                elif mutation=='parent-text':n.text='extra'
                else:n[0].tail='extra'
                with self.subTest(t=t,mutation=mutation),self.assertRaises(ValueError):require_resource(ET.tostring(root,encoding='unicode'),'plurals/ui_crop_preview_images',r['target'],r['attributes'])
    def test_exact_previous_value_guards_and_historical_scope(self):
        for t,l in self.data['locales'].items():
            for i in set(l['changed'])&set(l['predecessors']):
                kind,k=i.split('/');old=l['predecessors'][i]
                if kind!='string':continue
                self.assertEqual(l['accepted'][k],current_value(t,k,old['target'],old['attributes']))
                with self.assertRaises(ValueError):current_value(t,k,old['target']+' forged')
                with self.assertRaises(ValueError):current_value(t,k,old['target'],{'name':'wrong'})
        self.assertEqual('untouched',current_value('mk','ui_save','untouched'))
    def test_shared_additions_reject_invented_history_and_changed_source(self):
        import persian_hebrew_urdu_priority_expectations as current
        import memory_warning_source_review as warnings
        from test_current_localization_contracts import FAMILIES,wording_fixture,current_tagged_colour_data
        for t,k in MEMORY_ADDITIONS:
            r=require_addition(t,k);self.assertEqual(r['target'],warnings.current_source_expectation(k,t,None))
            with self.assertRaises(ValueError):warnings.current_source_expectation(k,t,'invented')
            bad=deepcopy(self.data);bad['sources']['string/'+k]['source']+=' altered'
            with patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):warnings.current_source_expectation(k,t,None)
        for t in TAGS:
            k='commons_svg_original_size_too_large';bad=deepcopy(self.data);bad['locales'][t]['predecessors']['string/'+k]={'target':'invented','attributes':{'name':k}}
            with patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):wording_fixture(FAMILIES[2])
        for t in TAGS:self.assertEqual(display(t,'save20_unsupported_image_colour'),current_tagged_colour_data()[t])
    def test_composed_units_and_edges_preserve_each_argument(self):
        for t in TAGS:
            for k in ('ui_width_in','ui_height_in'):
                for u in ('ui_pixels_6ec9c2','ui_percent_fd8671'):
                    self.assertEqual({'%1$s':1},cat.placeholders(display(t,k)))
                    self.assertNotIn('%1$s',display(t,k).replace('%1$s',display(t,u)))
            for k in ('ui_trim_in_pixels','ui_trim_in_percent'):
                for edge in ('ui_left','ui_top','ui_right','ui_bottom'):self.assertNotIn('%1$s',display(t,k).replace('%1$s',display(t,edge)))
    def test_coordinated_targets_xml_display_and_metadata_cannot_replace_accepted_values(self):
        import persian_hebrew_urdu_priority_expectations as current
        for tag,locale in self.data['locales'].items():
            for key in locale['accepted']:
                bad=deepcopy(self.data);bad['locales'][tag]['accepted'][key]+=' forged'
                # Matching altered XML is insufficient: independent accepted row refuses it.
                with self.subTest(tag=tag,key=key),patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):current.current_row(tag,key)
            for field in ('predecessors','changed','held_absent','held_present','target_attribute_exceptions','priority_dispositions','preserved_unreviewed','review_receipt_sha256'):
                bad=deepcopy(self.data);del bad['locales'][tag][field]
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):require_reviewed_fixture(bad)
            bad=deepcopy(self.data);del bad['locales'][tag]['predecessors']['string/ui_apply']
            with self.assertRaises(ValueError):require_reviewed_fixture(bad)
            bad=deepcopy(self.data);bad['locales'][tag]['display']={'save20_unsupported_image_colour':'forged'}
            with self.assertRaises(ValueError):require_reviewed_fixture(bad)
        raw=(cat.ROOT/'tools/fixtures/current_localization'/NAME).read_text()
        self.assertEqual(self.data,validated_fixture_text(raw))
        for corrupted in (raw+' ',raw.replace('sRGB','forgedRGB',1)):
            with self.assertRaises(ValueError):validated_fixture_text(corrupted)
        copy=reviewed_fixture();copy['locales']['fa']['accepted']['ui_apply']='forged'
        self.assertNotEqual(copy,reviewed_fixture())
if __name__=='__main__':unittest.main()
