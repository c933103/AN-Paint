"""Complete resource/composition regressions; not fluency or installed UI certification."""
from collections import Counter
from copy import deepcopy
import json
import re
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from current_localization_contracts import fixture, require_string, require_string_root
import hr_bs_mk_priority_expectations as current
import translation_catalogues as catalogues

HOLDS=frozenset({'formats22_derived_exported','ui_save_as','ui_save_as_jpeg',
                'ui_save_as_jpeg_xl','ui_save_as_png','ui_foreground_background_colour_palette','ui_pinch_and_pan_mode'})
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')

class CroatianBosnianMacedonianPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=fixture(current.FIXTURE)['locales']
        cls.xml={t:(catalogues.RES/('values' if t=='default' else 'values-'+t)/'strings.xml').read_text() for t in ['default','hr','bs','mk']}
        cls.roots={t:ET.fromstring(v) for t,v in cls.xml.items()}
        cls.tiers={t['id']:t['keys'] for t in json.loads((catalogues.DATA/'string-importance.json').read_text())['tiers'] if t['id'] in ['P0','P1']}

    def test_complete_priority_accounting_and_explicit_unapplied_holds(self):
        self.assertEqual({'P0':92,'P1':249},{k:len(v) for k,v in self.tiers.items()})
        keys={k.split('/',1)[1] for tier in self.tiers.values() for k in tier}
        self.assertEqual(current.TAGS,set(self.data))
        self.assertTrue(current.TAGS <= set(catalogues.offered_tags()))
        for tag,d in self.data.items():
            self.assertEqual(keys,set(d['priority_status']))
            self.assertEqual(HOLDS,set(d['held_absent']))
            self.assertEqual(keys-HOLDS,set(d['values'])-set(d['dependencies']))
            self.assertEqual(HOLDS,{k for k,s in d['priority_status'].items() if s=='hold'})
            for key in HOLDS:self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"))

    def test_every_complete_value_attributes_tokens_and_newlines(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                with self.subTest(tag=tag,key=key):
                    self.assertEqual(row['source'],self.roots['default'].find(f"./string[@name='{key}']").text)
                    self.assertEqual(row['attributes'],self.roots['default'].find(f"./string[@name='{key}']").attrib)
                    require_string_root(self.roots[tag],key,row['target'],{'attributes':row['attributes'],'child_elements':0})
                    self.assertEqual(Counter(TOKEN.findall(row['source'])),Counter(TOKEN.findall(row['target'])))
                    self.assertEqual(row['source'].count('\\n'),row['target'].count('\\n'))
                    self.assertEqual(row['source'].count('\n'),row['target'].count('\n'))
                    self.assertEqual(row['changed'],row['target']!=row['previous'])

    def test_changed_values_reject_missing_duplicate_truncated_markup_attributes_and_wrong_type(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                if not row['changed']:continue
                for mode in ['missing','duplicate','truncated','markup','attribute','type','argument']:
                    root=ET.Element('resources');n=ET.SubElement(root,'string',row['attributes']);n.text=row['target']
                    if mode=='missing':root.remove(n)
                    elif mode=='duplicate':root.append(deepcopy(n))
                    elif mode=='truncated':n.text=n.text[:-2]
                    elif mode=='markup':ET.SubElement(n,'b').text,n.text=n.text,None
                    elif mode=='attribute':n.set('translatable','false')
                    elif mode=='type':n.tag='plurals'
                    else:n.text+=' %9$s'
                    with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):
                        require_string(ET.tostring(root,encoding='unicode'),key,row['target'],{'attributes':row['attributes'],'child_elements':0})

    def test_forward_bindings_reject_forged_prior_source_attributes_and_unbound_locales(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                if not row['changed']:continue
                self.assertEqual(row['target'],current.current_value(tag,key,row['previous'],row['attributes'],row['source']))
                for previous,attrs,source in [('forged',row['attributes'],row['source']),
                    (row['previous'],{'name':key,'formatted':'forged'},row['source']),
                    (row['previous'],row['attributes'],row['source']+' changed')]:
                    with self.subTest(tag=tag,key=key),self.assertRaises(ValueError):current.current_value(tag,key,previous,attrs,source)
                self.assertEqual(row['previous'],current.current_value('unbound',key,row['previous']))
        for tag in current.TAGS:
            for key in current.added_keys(tag):self.assertIsNone(self.data[tag]['values'][key]['previous'])

    def test_atomic_save_recovery_and_paste_navigation_use_actual_complete_labels(self):
        for tag,d in self.data.items():
            v=lambda key:(d['values'].get(key) or d.get('context',{})[key])['display']
            for key in ['ui_autosave_failed_use_save','ui_autosave_paused_use_save','ui_export_did_not_save23','ui_export_explanation23','ui_save_explanation23','ui_share_explanation34']:
                self.assertIn(v('ui_save'),v(key))
            for key in ['ui_autosave_is_paused_to_protect_that_draft_use','ui_export_did_not_save23']:self.assertIn(v('save20_title'),v(key))
            for key in ['ui_a_separate_recovery_copy_has_been_kept_use','ui_autosave_is_paused_to_protect_that_draft_use']:
                self.assertIn(v('ui_export_recovery_copy'),v(key));self.assertIn(v('ui_menu_file'),v(key))
            recovery=v('ui_recovery_copy_exported_extract_canvas_png_from_the')
            for literal in [v('ui_menu_file'),v('ui_load_image'),'canvas.png','ZIP']:self.assertIn(literal,recovery)
            for key in ['ui_draw26','ui_category_insert','ui_other_images34']:self.assertIn(v(key),v('ui_paste_hint34'))
            self.assertEqual(3,len({v('ui_save'),v('ui_discard_changes23'),v('ui_keep_editing23')}))
            self.assertIn(v('ui_undo'),v('ui_keeps_pixels_at_the_top_left_smaller_canvas'))

    def test_unit_and_edge_compositions_keep_complete_argument_slots(self):
        for tag,d in self.data.items():
            v=lambda key:(d['values'].get(key) or d.get('context',{})[key])['display']
            for key in ['ui_width_in','ui_height_in','ui_trim_in_pixels','ui_trim_in_percent']:
                self.assertEqual(['%1$s'],TOKEN.findall(v(key)))
            for unit in ['ui_pixels_6ec9c2','ui_percent_fd8671']:
                for key in ['ui_width_in','ui_height_in']:
                    self.assertIn(v(unit),v(key).replace('%1$s',v(unit)))
            for edge in ['ui_left','ui_top','ui_right','ui_bottom']:
                for key in ['ui_trim_in_pixels','ui_trim_in_percent']:
                    self.assertEqual(1,v(key).replace('%1$s',v(edge)).count(v(edge)))
            self.assertEqual({'%1$s':1,'%2$s':1},Counter(TOKEN.findall(v('ui_expand_tool_category'))))
            self.assertEqual({'%1$s':1,'%2$s':1},Counter(TOKEN.findall(v('ui_collapse_tool_category'))))

    def test_demonstrated_mistranslations_cannot_return(self):
        expected={'hr':{'ui_font':'Font','ui_underline':'Podcrtano'},
                  'bs':{'ui_rectangle_select':'Pravougaoni izbor','ui_pixels':'Pikseli','ui_pixels_6ec9c2':'pikseli'},
                  'mk':{'ui_save':'Зачувај','ui_undo':'Поништи','ui_done':'Готово','save20_file_format':'Формат на датотека'}}
        for tag,values in expected.items():
            for key,value in values.items():self.assertEqual(value,current.current_display(tag,key))

if __name__=='__main__':unittest.main()
