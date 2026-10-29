"""Full Nordic priority scope, typed text, compositions and negative controls."""
from collections import Counter
from copy import deepcopy
import json
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string as require_scalar
import translation_catalogues as cat
from nordic_priority_expectations import NAME, TAGS, current_row, current_value, added_keys, display

def require_string(xml,key,value,rule):
    root=ET.fromstring(xml)
    if root.tag!='resources' or root.attrib or (root.text or '').strip():
        raise ValueError('Unexpected resources shape')
    if any((node.tail or '').strip() for node in root):
        raise ValueError('Unexpected resource tail')
    named=[node for node in root if node.get('name')==key]
    if len(named)!=1 or named[0].tag!='string':
        raise ValueError('Ambiguous scalar identity')
    return require_scalar(xml,key,value,rule)

HOLDS = {'formats22_derived_exported','ui_foreground_background_colour_palette','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png','ui_pinch_and_pan_mode'}
COMPANIONS={'da':{'ui_top','ui_width_in','ui_trim_in_pixels','ui_trim_in_percent','formats22_at_least_frames'},'is':{'ui_top','ui_width_in','ui_trim_in_pixels','ui_trim_in_percent','formats22_at_least_frames','save20_dither'},'no':{'ui_top','ui_width_in','ui_trim_in_pixels','ui_trim_in_percent','formats22_at_least_frames'}}

class NordicPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=fixture(NAME)
        cls.xml={t:(cat.ROOT/cls.data['locales'][t]['path']).read_text() for t in TAGS}
        cls.source=(cat.RES/'values/strings.xml').read_text()

    def test_full_typed_priority_partitions_and_explicit_no_not_nb(self):
        tiers=json.loads((cat.DATA/'string-importance.json').read_text())['tiers']
        expected={k.split('/')[1]:t['id'] for t in tiers if t['id'] in ('P0','P1') for k in t['keys']}
        self.assertEqual({'da','is','no'},set(self.data['locales']))
        for tag,loc in self.data['locales'].items():
            self.assertEqual(expected,{k:r['tier'] for k,r in loc['priority_dispositions'].items()})
            self.assertEqual(Counter({'P0':92,'P1':249}),Counter(r['tier'] for r in loc['priority_dispositions'].values()))
            holds=HOLDS|({'ui_main23'} if tag=='is' else set())
            self.assertEqual(holds,set(loc['held_absent']))
            self.assertEqual(set(expected)-holds|COMPANIONS[tag],set(loc['accepted']))
            self.assertEqual(22 if tag=='is' else 23,sum(r['status']=='bounded-wording-only' for r in loc['priority_dispositions'].values()))
            for key in holds:self.assertIsNone(ET.fromstring(self.xml[tag]).find(f"./string[@name='{key}']"))
        self.assertIn('no',cat.offered_tags());self.assertIn('nn',cat.offered_tags());self.assertNotIn('nb',cat.offered_tags())

    def test_every_full_source_target_attributes_alias_and_placeholder(self):
        for tag,loc in self.data['locales'].items():
            for key,value in loc['accepted'].items():
                row=current_row(tag,key)
                with self.subTest(tag=tag,key=key):
                    require_string(self.source,key,row['source'],{'attributes':self.data['sources'][key]['attributes']})
                    require_string(self.xml[tag],key,value,{'attributes':row['attributes'],'placeholders':cat.placeholders(row['source'])})
                    self.assertEqual([],cat.android_string_errors(value))
            self.assertEqual([],cat.validate_catalogue(tag,require_complete=False))
        self.assertEqual('Vista',display('is','ui_save_a5d0d9'))

    def test_changed_values_reject_old_missing_truncated_duplicate_markup_and_attributes(self):
        for tag,loc in self.data['locales'].items():
            for key in loc['changed']:
                row=current_row(tag,key)
                for mutation in ('old','missing','truncated','duplicate','markup','attributes','root-text','root-attribute','tail','wrong-type'):
                    root=ET.Element('resources');node=ET.SubElement(root,'string',row['attributes']);node.text=row['target']
                    if mutation=='old':node.text=row['previous_target'] or ''
                    elif mutation=='missing':root.remove(node)
                    elif mutation=='truncated':node.text=node.text[:-2]
                    elif mutation=='duplicate':root.append(deepcopy(node))
                    elif mutation=='markup':ET.SubElement(node,'b').text='extra'
                    elif mutation=='attributes':node.set('translatable','false')
                    elif mutation=='root-text':root.text='unexpected'
                    elif mutation=='root-attribute':root.set('unexpected','true')
                    elif mutation=='tail':node.tail='unexpected'
                    else:ET.SubElement(root,'plurals',{'name':key})
                    with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):
                        require_string(ET.tostring(root,encoding='unicode'),key,row['target'],{'attributes':row['attributes']})

    def test_forward_bindings_reject_forged_previous_and_keep_unrelated_values(self):
        for tag,loc in self.data['locales'].items():
            for key in set(loc['changed'])&set(loc['predecessors']):
                old=loc['predecessors'][key]
                self.assertEqual(loc['accepted'][key],current_value(tag,key,old['target'],old['attributes']))
                with self.assertRaises(ValueError):current_value(tag,key,old['target']+' changed')
                with self.assertRaises(ValueError):current_value(tag,key,old['target'],{'name':'wrong'})
        self.assertEqual('untouched',current_value('nn','ui_save','untouched'))

    def test_icelandic_standalone_and_composed_units_use_distinct_cases(self):
        self.assertEqual(('Mynddílar','prósent'),(display('is','ui_pixels'),display('is','ui_percent')))
        for key,noun in [('ui_width_in','Breidd'),('ui_height_in','Hæð')]:
            for unit,word in [('ui_pixels_6ec9c2','mynddílum'),('ui_percent_fd8671','prósentum')]:
                self.assertEqual(noun+' í '+word,display('is',key).replace('%1$s',display('is',unit)))
        source=(cat.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt').read_text()
        self.assertIn('listOf(ui(R.string.ui_pixels), ui(R.string.ui_percent))',source)
        self.assertIn('ui(R.string.ui_percent_fd8671) else ui(R.string.ui_pixels_6ec9c2)',source)

    def test_actual_recovery_menu_commands_gif_and_crop_compositions(self):
        for tag in TAGS:
            recovery=display(tag,'ui_recovery_copy_exported_extract_canvas_png_from_the')
            self.assertIn(display(tag,'ui_menu_file')+' > '+display(tag,'ui_load_image'),recovery)
            paused=display(tag,'ui_autosave_is_paused_to_protect_that_draft_use')
            for token in [display(tag,'ui_menu_file')+' → '+display(tag,'save20_title'),display(tag,'save20_file_format')+': PNG / JPEG','%1$s']:self.assertIn(token,paused)
            for unit in ['ui_trim_in_pixels','ui_trim_in_percent']:
                for edge in ['ui_left','ui_right','ui_bottom']:
                    composed=display(tag,unit).replace('%1$s',display(tag,edge))
                    self.assertTrue(composed.startswith(display(tag,edge)+': '));self.assertNotIn('%',composed)
        self.assertIn(display('is','save20_dither'),display('is','save20_gif_description'))
        self.assertEqual('Fjöldi ramma í þessari GIF-mynd: að minnsta kosti 2. AN Paint breytir kyrrmyndum og varðveitir ekki hreyfimyndir.',display('is','formats22_animation_message').replace('%1$s','GIF').replace('%2$s',display('is','formats22_at_least_frames').replace('%1$d','2')))

    def test_shared_additions_reject_changed_english_and_forged_history(self):
        import memory_warning_source_review as warnings
        import nordic_priority_expectations as current
        from test_current_localization_contracts import wording_fixture,FAMILIES,current_tagged_colour_data
        for tag,key in current.MEMORY_ADDITIONS:
            self.assertEqual(current_row(tag,key)['target'],warnings.current_source_expectation(key,tag,None))
            with self.assertRaises(ValueError):warnings.current_source_expectation(key,tag,'invented')
            bad=deepcopy(self.data);bad['sources'][key]['source']+=' changed'
            with patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):warnings.current_source_expectation(key,tag,None)
        for tag in TAGS:
            key='commons_svg_original_size_too_large';bad=deepcopy(self.data);bad['sources'][key]['source']+=' changed'
            with patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):wording_fixture(FAMILIES[2])
        self.assertEqual(display('is','save20_unsupported_image_colour'),current_tagged_colour_data()['is'])

if __name__=='__main__':unittest.main()
