"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import translation_catalogues as catalogues

MEMORY='ui_d_d_pixels_2f_mp_exceeds_the_current'

class CzechPriorityDraftWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strings={tag:catalogues.read_strings(catalogues.RES / folder / 'strings.xml')
                     for tag,folder in [('default','values'),('cs','values-cs')]}

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

    def test_memory_modality_and_original_ownership_distinctions(self):
        strings = self.strings['cs']
        self.assertIn('K automatické změně velikosti nedošlo', strings[MEMORY])
        sampled = strings['ui_sampled_resize_memory_explanation']
        for distinction in ('může lišit', 'kopie ztrácí detaily', 'Původní soubor zůstane beze změny'):
            self.assertIn(distinction, sampled)
        self.assertIn('Samotné zmenšení', strings['ui_assembly_source_memory_floor'])
        self.assertIn('Sestava zůstala beze změny', strings['ui_assembly_source_memory_floor'])
        self.assertIn('nebo jim Android', strings['ui_the_full_image_and_working_buffers_exceed_the'])

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
