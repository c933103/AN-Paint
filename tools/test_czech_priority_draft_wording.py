"""Bounded Czech candidate contracts; these tests do not accept draft translations."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues

FIXTURE='czech_priority_draft_wording.json'
CORRECTIONS={
    'save20_file_format':'Formát souboru',
    'ui_keep_editing23':'Pokračovat v úpravách',
    'ui_apply':'Použít',
    'ui_background_colour':'Barva pozadí',
    'ui_brush':'Štětec',
    'ui_foreground_colour':'Barva popředí',
    'ui_line':'Čára',
    'ui_pixels':'Pixely',
    'ui_pixels_6ec9c2':'pixelech',
    'ui_solid_fill':'Plná výplň',
    'ui_watercolor':'Akvarel',
    'ui_rectangle_select':'Obdélníkový výběr',
}
MEMORY='ui_d_d_pixels_2f_mp_exceeds_the_current'
COUNT='ui_d_d_px_d_pixels_2f_mp'

class CzechPriorityDraftWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=fixture(FIXTURE)
        cls.xml={tag:(catalogues.RES / folder / 'strings.xml').read_text()
                 for tag,folder in [('default','values'),('cs','values-cs')]}
        cls.strings={tag:catalogues.read_strings(catalogues.RES / folder / 'strings.xml')
                     for tag,folder in [('default','values'),('cs','values-cs')]}
        cls.priority=json.loads((catalogues.ROOT/'translations/string-importance.json').read_text())
        cls.selected={k.split('/')[1] for tier in cls.priority['tiers'][:2] for k in tier['keys']}

    def test_complete_priority_presence_without_claiming_whole_language_acceptance(self):
        self.assertEqual(341,len(self.selected))
        self.assertLessEqual(self.selected,self.strings['cs'].keys())
        self.assertEqual('independent_static_review_with_holds',self.data['review_status'])
        self.assertEqual('cs',self.data['locale'])
        scope=fixture('locale_contract_scope.json')
        self.assertIn('cs',scope['fallback_tags'])
        self.assertNotIn('cs',scope['scoped_tags'])
        self.assertNotIn('commons_import_svg_changes',self.strings['cs'])
        self.assertNotIn('commons_import_raster_changes',self.strings['cs'])

    def test_full_candidate_values_attributes_placeholders_and_syntax(self):
        keys=set(self.data['values'])
        self.assertEqual(255,len(keys))
        self.assertEqual({'ui_width_in','formats22_at_least_frames'},keys-self.selected)
        self.assertLessEqual(CORRECTIONS.keys(),keys)
        require_wording_shape(self.data,keys,{'default','cs'})
        for key,values in self.data['values'].items():
            constraints=self.data['constraints'][key]
            self.assertEqual(catalogues.placeholders(values['default']),Counter(constraints['placeholders']))
            for tag,expected in values.items():
                with self.subTest(key=key,tag=tag):
                    require_string(self.xml[tag],key,expected,constraints)
        self.assertEqual([],catalogues.validate_catalogue('cs',require_complete=False))

    def test_selected_entries_preserve_argument_type_index_precision_and_multiplicity(self):
        for key in self.selected | {'ui_width_in','formats22_at_least_frames'}:
            with self.subTest(key=key):
                self.assertEqual(catalogues.placeholders(self.strings['default'][key]),
                                 catalogues.placeholders(self.strings['cs'][key]))
        self.assertEqual('%1$d × %2$d px · Počet pixelů: %3$,d (%4$.2f MP)',self.strings['cs'][COUNT])

    def test_missing_duplicate_truncated_and_markup_values_fail_closed(self):
        for key in (MEMORY,'formats22_animation_poster','ui_sampled_resize_memory_explanation','ui_width_in','ui_background_colour'):
            for mutation in ('missing','duplicate','truncated','markup','attributes'):
                root=ET.fromstring(self.xml['cs']);node=root.find(f"./string[@name='{key}']")
                if mutation=='missing':root.remove(node)
                elif mutation=='duplicate':root.append(deepcopy(node))
                elif mutation=='truncated':node.text=node.text[:-1]
                elif mutation=='attributes':node.set('formatted','false')
                else:
                    child=ET.SubElement(node,'b');child.text,node.text=node.text,None
                with self.subTest(key=key,mutation=mutation),self.assertRaises(ValueError):
                    require_string(ET.tostring(root,encoding='unicode'),key,self.data['values'][key]['cs'],self.data['constraints'][key])

    def test_argument_mutations_fail_even_if_mutated_text_is_given_as_expected(self):
        for key in (MEMORY,COUNT):
            original=self.strings['cs'][key]
            for value in (original.replace('%1$d','%1$s'),original.replace('%1$d',''),original.replace('$.2f','$f'),original+" '"):
                root=ET.fromstring(self.xml['cs']);root.find(f"./string[@name='{key}']").text=value
                with self.subTest(key=key,value=value),self.assertRaises(ValueError):
                    require_string(ET.tostring(root,encoding='unicode'),key,value,self.data['constraints'][key])

    def test_supported_present_entry_corrections_and_unchanged_uncertainties(self):
        for key,value in CORRECTIONS.items():self.assertEqual(value,self.strings['cs'][key])
        for key,value in {'ui_discard':'Zahodit změny','ui_category_brush':'"Stopa"','ui_fit_image':'"Přizpůsobit obrázek oknu"','ui_main23':'Hlavní','ui_swap_foreground_background':'"Prohodit barvy"'}.items():
            self.assertEqual(value,self.strings['cs'][key])

    def test_independently_reviewed_crop_and_selection_corrections_reject_old_text(self):
        for key,expected,old in (
            ('ui_reset_crop','Zrušit ořez','Obnovit původní ořez'),
            ('ui_rectangle_select','Obdélníkový výběr','"Výběr obdélníku"'),
        ):
            self.assertEqual(expected,self.strings['cs'][key])
            root=ET.fromstring(self.xml['cs']);root.find(f"./string[@name='{key}']").text=old
            with self.subTest(key=key),self.assertRaises(ValueError):
                require_string(ET.tostring(root,encoding='unicode'),key,expected,self.data['constraints'][key])

    def test_locative_units_compose_with_both_dimension_descriptions(self):
        strings=self.strings['cs']
        self.assertEqual(('Pixely','Procenta'),(strings['ui_pixels'],strings['ui_percent']))
        for key,noun in [('ui_width_in','Šířka'),('ui_height_in','Výška')]:
            for unit_key,unit in [('ui_pixels_6ec9c2','pixelech'),('ui_percent_fd8671','procentech')]:
                self.assertEqual(noun+' v '+unit,strings[key].replace('%1$s',strings[unit_key]))

    def test_category_description_does_not_inflect_dynamic_tool_names(self):
        for key,action in [('ui_collapse_tool_category','Sbalit'),('ui_expand_tool_category','Rozbalit')]:
            self.assertEqual('%1$s: vybraný nástroj: %2$s. '+action+' nástroje a možnosti',self.strings['cs'][key])
            for tool in ('Štětec','Tužka','Kreslení','Volný výběr'):
                self.assertIn('vybraný nástroj: '+tool,self.strings['cs'][key].replace('%1$s','Kreslení').replace('%2$s',tool))

    def test_memory_safety_clauses_cannot_be_lost(self):
        clauses=(
            '%1$d × %2$d pixelů (%3$.2f MP) překračuje aktuální bezpečný limit pro úpravy %4$.2f MP.',
            'AN Paint uchovává v paměti celý obrázek a vyhrazuje místo pro transformace a výběry.',
            'Tento limit závisí na dostupné paměti.',
            'Operace byla zastavena před vyhrazením paměti pro příliš velkou bitmapu.',
            'K automatické změně velikosti nedošlo.',
        )
        value=self.strings['cs'][MEMORY];self.assertEqual(' '.join(clauses),value)
        for clause in clauses:
            root=ET.fromstring(self.xml['cs']);root.find(f"./string[@name='{MEMORY}']").text=value.replace(clause,'')
            with self.subTest(clause=clause),self.assertRaises(ValueError):
                require_string(ET.tostring(root,encoding='unicode'),MEMORY,value,self.data['constraints'][MEMORY])
        for key,required in {
            'ui_sampled_resize_memory_explanation':['Skutečná spotřeba paměti se může lišit.','Menší kopie ztrácí detaily.','Původní soubor zůstane beze změny.'],
            'ui_assembly_source_memory_floor':['i pro velmi malý výstup.','Zmenšení rozměrů sestavy tento problém nevyřeší.','Sestava zůstala beze změny.'],
            'ui_the_full_image_and_working_buffers_exceed_the':['nebo jim Android nemohl vyhradit paměť.','změňte velikost kopie.','Původní soubor zůstane beze změny.'],
        }.items():
            for clause in required:self.assertIn(clause,self.strings['cs'][key])

    def test_recovery_save_export_and_sharing_remain_distinct(self):
        strings=self.strings['cs']
        for key in ('ui_a_separate_recovery_copy_has_been_kept_use','ui_recovery_copy_exported_extract_canvas_png_from_the'):
            self.assertIn('canvas.png',strings[key]);self.assertIn('ZIP',strings[key]);self.assertIn('Soubor >',strings[key])
        self.assertIn('Formát souboru: PNG / JPEG',strings['ui_autosave_is_paused_to_protect_that_draft_use'])
        self.assertIn('„Soubor → '+strings['ui_export_recovery_copy']+'“',strings['ui_autosave_is_paused_to_protect_that_draft_use'])
        self.assertIn('aktuální obrázek i cíl příkazu Uložit beze změny',strings['ui_export_explanation23'])
        self.assertIn('Aktuální cíl příkazu Uložit zůstane beze změny.',strings['ui_share_explanation34'])
        self.assertIn('Obrázek byl uložen, ale Android nemohl otevřít sdílení:',strings['ui_the_image_was_saved_but_android_could_not'])

    def test_inexact_frame_count_composes_without_english_or_count_inflection(self):
        s=self.strings['cs']
        self.assertEqual('alespoň %1$d',s['formats22_at_least_frames'])
        for count in (2,5,21,1001):
            frames=s['formats22_at_least_frames'].replace('%1$d',str(count))
            value=s['formats22_animation_message'].replace('%1$s','GIF').replace('%2$s',frames)
            self.assertTrue(value.startswith('Počet snímků v souboru GIF: alespoň '+str(count)+'.'))
            self.assertIn('nezachovává animaci.',value)
            self.assertNotIn('at least',value)

    def test_animation_colour_and_import_contracts_preserve_key_limits(self):
        s=self.strings['cs']
        self.assertIn('nezachovává animaci.',s['formats22_animation_message'])
        self.assertIn('místo snímků animace.',s['formats22_animation_poster'])
        self.assertIn('pouze první snímek.',s['formats22_animation_still'])
        self.assertIn('zda obsahuje více snímků.',s['formats22_animation_unknown'])
        self.assertIn('144 dpi',s['formats22_pdf_raster_hint'])
        self.assertIn('512 MiB',s['formats22_import_limit'])
        self.assertIn('PNG v barevném prostoru sRGB',s['save20_unsupported_image_colour'])
        self.assertIn('Obrázek nebyl importován.',s['colour_converter_unavailable'])
        self.assertIn('Nebyla nahrazena velikostí podle plátna.',s['commons_svg_original_size_unavailable'])
        self.assertEqual(2,s['language20_translation_note'].count('\\n'))
        self.assertIn('Nový nebo nepřeložený text se zobrazuje anglicky.',s['language20_translation_note'])

if __name__=='__main__':unittest.main()
