"""Exact accepted delta and mutation tests; retained context is not linguistic acceptance."""
from collections import Counter
from copy import deepcopy
import json,re,unittest,xml.etree.ElementTree as ET
from current_localization_contracts import fixture,require_string
import serbian_priority_delta_expectations as current
import translation_catalogues as cat
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png','ui_foreground_background_colour_palette','ui_pinch_and_pan_mode'}
class SerbianPriorityDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=fixture(current.FIXTURE)['locales']
        cls.xml={t:(cat.RES/('values' if t=='default' else 'values-b+'+t.replace('-','+'))/'strings.xml').read_text() for t in ['default','sr-Cyrl','sr-Latn']}
        cls.roots={t:ET.fromstring(v) for t,v in cls.xml.items()}
    def test_scope_separates_changed_values_context_holds_and_pending_retained_rows(self):
        tiers=json.loads((cat.DATA/'string-importance.json').read_text())['tiers']
        keys={k.split('/',1)[1] for tier in tiers if tier['id'] in ('P0','P1') for k in tier['keys']}
        self.assertEqual(341,len(keys));self.assertEqual(current.TAGS,set(self.data));self.assertTrue(current.TAGS<=set(cat.offered_tags()))
        for tag,d in self.data.items():
            self.assertEqual(keys,set(d['priority_status']));self.assertEqual(HOLDS,set(d['held_absent']));self.assertEqual(['ui_discard'],d['held_existing'])
            self.assertEqual(144 if tag=='sr-Cyrl' else 146,len(d['values']));self.assertEqual(4,len(d['dependencies']))
            self.assertEqual(118 if tag=='sr-Cyrl' else 117,Counter(d['priority_status'].values())['retain_pending_prior_binding'])
            self.assertEqual(75 if tag=='sr-Cyrl' else 74,sum(s.startswith('prior_exact_P0_carry') for s in d['priority_status'].values()))
            for key in HOLDS:self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"))
            for row in d['context'].values():self.assertFalse(row['changed']);self.assertNotEqual('accepted_delta',row['review_status'])
    def test_complete_targets_and_source_attributes_slots_newlines(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                with self.subTest(tag=tag,key=key):
                    s=self.roots['default'].find(f"./string[@name='{key}']")
                    self.assertEqual((s.text,s.attrib),(row['source'],row['attributes']))
                    require_string(self.xml[tag],key,row['target'],{'attributes':row['attributes'],'child_elements':0})
                    self.assertEqual(Counter(TOKEN.findall(row['source'])),Counter(TOKEN.findall(row['target'])))
                    for newline in ('\n','\\n'):self.assertEqual(row['source'].count(newline),row['target'].count(newline))
                    self.assertTrue(row['changed']);self.assertNotEqual(row['previous'],row['target'])
    def test_missing_duplicate_truncated_markup_attributes_type_and_slot_corruption_fail(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                for mode in ['missing','duplicate','truncated','markup','attribute','type','argument']:
                    root=ET.Element('resources');n=ET.SubElement(root,'string',row['attributes']);n.text=row['target']
                    if mode=='missing':root.remove(n)
                    elif mode=='duplicate':root.append(deepcopy(n))
                    elif mode=='truncated':n.text=n.text[:-2]
                    elif mode=='markup':ET.SubElement(n,'b').text,n.text=n.text,None
                    elif mode=='attribute':n.set('translatable','false')
                    elif mode=='type':n.tag='plurals'
                    else:n.text+=' %9$s'
                    with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):require_string(ET.tostring(root,encoding='unicode'),key,row['target'],{'attributes':row['attributes'],'child_elements':0})
    def test_finite_forward_binding_rejects_forged_previous_source_and_attributes(self):
        for tag,d in self.data.items():
            for key,r in d['values'].items():
                self.assertEqual(r['target'],current.current_value(tag,key,r['previous'],r['attributes'],r['source']))
                for old,attrs,source in [('forged',r['attributes'],r['source']),(r['previous'],{'name':key,'formatted':'forged'},r['source']),(r['previous'],r['attributes'],r['source']+' forged')]:
                    with self.subTest(tag=tag,key=key),self.assertRaises(ValueError):current.current_value(tag,key,old,attrs,source)
            self.assertIsNone(current.current_value('unbound','ui_no_resize_fits_decoder_memory',None,{},''))
    def test_independently_revised_svg_and_demonstrated_action_defects(self):
        exact={'sr-Cyrl':{'ui_crop_image':'Исеци слику','ui_rectangle_select':'Правоугаони избор','ui_keep_editing23':'Настави уређивање','commons_svg_original_size_too_large':'Изворне димензије SVG-а премашују ограничења система Android за димензије битмапе. Величина није промењена.'},'sr-Latn':{'ui_crop_image':'Iseci sliku','ui_rectangle_select':'Pravougaoni izbor','ui_keep_editing23':'Nastavi uređivanje'}}
        for tag,rows in exact.items():
            for key,text in rows.items():self.assertEqual(text,current.row(tag,key)['display'])
    def test_paste_hint_and_dirty_confirmation_keep_distinct_actual_labels(self):
        for tag in current.TAGS:
            v=lambda k:current.row(tag,k)['display']
            for key in ['ui_draw26','ui_category_insert','ui_other_images34']:self.assertIn(v(key),v('ui_paste_hint34'))
            self.assertEqual(3,len({v('ui_save'),v('ui_discard_changes23'),v('ui_keep_editing23')}))
    def test_dependencies_are_exact_absent_to_target_additions(self):
        for tag,d in self.data.items():
            self.assertEqual({'ui_width_in','ui_trim_in_pixels','ui_trim_in_percent','formats22_at_least_frames'},set(d['dependencies']))
            for key in d['dependencies']:
                r=d['values'][key];self.assertIsNone(r['previous']);self.assertEqual(r['target'],current.addition(tag,key,r['source'],None))
                with self.assertRaises(ValueError):current.addition(tag,key,r['source'],'forged')
if __name__=='__main__':unittest.main()
