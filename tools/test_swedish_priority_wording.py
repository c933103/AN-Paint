"""Bounded complete Swedish statements; actual consumers also have JVM tests."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues
# Frozen pairs stay historical; exact current warning successors are separately receipt-bound.
from memory_warning_source_review import current_source_expectation

KEYS = {
    'formats22_animation_message',
    'formats22_animation_poster',
    'formats22_animation_still',
    'formats22_animation_title',
    'formats22_animation_unknown',
    'formats22_ascii_description',
    'formats22_at_least_frames',
    'formats22_derived_exported',
    'formats22_open_still',
    'formats22_pdf_raster_hint',
    'gallery_credit_could_not_save',
    'gallery_credit_too_large',
    'language20_app_language',
    'language20_current',
    'language20_device_default',
    'language20_translation_note',
    'legacy_credits_unreadable',
    'save20_destination_error',
    'save20_encoding_budget',
    'save20_file_format',
    'save20_gif_description',
    'save20_invalid_name',
    'save20_lossy_quality_description',
    'save20_unsupported_image_colour',
    'ui_a_separate_recovery_copy_has_been_kept_use',
    'ui_an_assembly_source_image_is_missing',
    'ui_assembly_saved',
    'ui_assembly_source_memory_floor',
    'ui_autosave_failed_use_save',
    'ui_autosave_image_encoding_failed',
    'ui_autosave_is_paused_to_protect_that_draft_use',
    'ui_autosave_metadata_is_missing',
    'ui_autosave_paused_use_save',
    'ui_autosave_pixels_are_missing',
    'ui_autosave_pixels_could_not_be_read',
    'ui_autosave_selection_encoding_failed',
    'ui_bottom',
    'ui_cannot_create_the_undo_cache_free_some_device',
    'ui_clear_all',
    'ui_clear_image',
    'ui_collapse_tool_category',
    'ui_could_not_export_the_recovery_copy',
    'ui_could_not_open_image',
    'ui_could_not_save_image',
    'ui_could_not_save_the_assembly',
    'ui_could_not_store_the_assembly',
    'ui_d_d_pixels_2f_mp_exceeds_the_current',
    'ui_draft_not_saved_yet',
    'ui_draft_restored',
    'ui_draft_saved',
    'ui_drawing23',
    'ui_expand_tool_category',
    'ui_export_did_not_save23',
    'ui_export_explanation23',
    'ui_export_recovery_copy',
    'ui_export_recovery_copy_144b8a',
    'ui_fit',
    'ui_fit_entire_canvas_in_view',
    'ui_fit_image',
    'ui_higher_quality_usually_makes_a_larger_file_lossless',
    'ui_history_unavailable34',
    'ui_invalid_autosave_metadata',
    'ui_keep_editing23',
    'ui_keeps_pixels_at_the_top_left_smaller_canvas',
    'ui_line',
    'ui_load_image',
    'ui_menu',
    'ui_not_enough_memory_for_this_operation_the_assembly',
    'ui_not_enough_memory_to_save_in_this_format',
    'ui_outline',
    'ui_percent',
    'ui_pixels_6ec9c2',
    'ui_png_encoding_failed',
    'ui_previous_draft_kept_for_recovery',
    'ui_recovered_image',
    'ui_recovery_copy_exported_extract_canvas_png_from_the',
    'ui_resize_large_image',
    'ui_sampled_resize_memory_explanation',
    'ui_save_and_share',
    'ui_save_and_share_41edb4',
    'ui_save_as',
    'ui_save_as_jpeg',
    'ui_save_as_jpeg_xl',
    'ui_save_as_png',
    'ui_save_explanation23',
    'ui_save_png',
    'ui_saved',
    'ui_share_explanation34',
    'ui_share_saved_image',
    'ui_solid_fill',
    'ui_swap23',
    'ui_swap_foreground_background',
    'ui_the_draft_is_saving_try_again_shortly',
    'ui_the_encoder_did_not_finish',
    'ui_the_image_was_saved_but_android_could_not',
    'ui_the_previous_draft_could_not_be_moved_to',
    'ui_the_previous_draft_could_not_be_preserved_separately',
    'ui_the_previous_draft_could_not_be_restored',
    'ui_the_previous_draft_needs_more_memory_to_reopen',
    'ui_the_saved_assembly_could_not_be_opened',
    'ui_the_selected_location_is_not_writable',
    'ui_the_trim_would_remove_the_entire_image',
    'ui_the_undo_cache_is_damaged',
    'ui_there_is_not_enough_memory_for_this_operation',
    'ui_this_location_is_not_writable',
    'ui_unexpected_data_in_the_undo_cache',
    'ui_watercolor',
    'ui_your_current_image_has_unsaved_changes',
}

class SwedishPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture('swedish_priority_current_wording.json')
        cls.keys = KEYS
        require_wording_shape(cls.data, cls.keys, {'default', 'sv'})
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text() for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.strings = {n.get('name'): n.text.strip('"') for n in ET.fromstring(cls.xml['sv']) if n.tag == 'string'}

    def test_complete_values_attributes_formats_and_newlines(self):
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, current_source_expectation(key, tag, expected), self.data['constraints'][key])
        self.assertEqual([], catalogues.validate_catalogue('sv'))

    def test_current_fixture_is_nonempty_and_has_all_safety_keys(self):
        self.assertGreater(len(self.keys), 100)
        manifest = json.loads((catalogues.ROOT / 'translations/string-importance.json').read_text())
        safety = next(t['keys'] for t in manifest['tiers'] if t['id'] == 'P0')
        self.assertTrue(all(k.removeprefix('string/') in self.strings for k in safety))
        self.assertIn('formats22_at_least_frames', self.keys)
        self.assertIn('ui_load_image', self.keys)

    def test_missing_empty_or_duplicate_value_and_markup_fail(self):
        for key in self.keys:
            for mutation in ('missing', 'duplicate', 'truncated', 'markup', 'format-flag'):
                root = ET.fromstring(self.xml['sv']); node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                else: node.set('formatted', 'true' if node.get('formatted') == 'false' else 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, current_source_expectation(key, 'sv', self.data['values'][key]['sv']), self.data['constraints'][key])

    def test_missing_fixture_locale_or_constraint_fails(self):
        for mutation in ('key', 'locale', 'constraint', 'empty'):
            changed = deepcopy(self.data); key = 'ui_keep_editing23'
            if mutation == 'key': del changed['values'][key]
            elif mutation == 'locale': del changed['values'][key]['sv']
            elif mutation == 'constraint': del changed['constraints'][key]
            else: changed['values'][key]['sv'] = ''
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_wording_shape(changed, self.keys, {'default', 'sv'})

    def test_actual_command_names_in_recovery_and_export_guidance(self):
        s = self.strings
        self.assertEqual(('Arkiv', 'Spara', 'Spara som…', 'Öppna bild…'), tuple(s[k] for k in ('ui_menu_file', 'ui_save', 'save20_title', 'ui_load_image')))
        for key in ('ui_a_separate_recovery_copy_has_been_kept_use', 'ui_autosave_is_paused_to_protect_that_draft_use'):
            self.assertIn(s['ui_export_recovery_copy'].removesuffix('…'), s[key])
        self.assertIn('Arkiv > Öppna bild', s['ui_recovery_copy_exported_extract_canvas_png_from_the'])
        self.assertIn('canvas.png', s['ui_recovery_copy_exported_extract_canvas_png_from_the'])
        self.assertIn('Spara eller Spara som', s['ui_export_did_not_save23'])
        self.assertIn('Filformat: PNG / JPEG', s['ui_autosave_is_paused_to_protect_that_draft_use'])

    def test_frame_counts_include_the_localized_lower_bound(self):
        for count in (2, 21, 101):
            exact = self.strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', str(count))
            lower = self.strings['formats22_at_least_frames'].replace('%1$d', str(count))
            inexact = self.strings['formats22_animation_message'].replace('%1$s', 'GIF').replace('%2$s', lower)
            self.assertIn(f'innehåller {count} bildrutor.', exact)
            self.assertIn(f'innehåller minst {count} bildrutor.', inexact)
            self.assertIn('bevarar inte animeringar.', exact)
        self.assertIn('om den innehåller flera bildrutor', self.strings['formats22_animation_unknown'])

    def test_fixed_tool_and_action_meanings_are_distinct(self):
        expected = {'ui_line': 'Linje', 'ui_watercolor': 'Akvarell', 'ui_outline': 'Kontur', 'ui_solid_fill': 'Enfärgad fyllning', 'ui_keep_editing23': 'Fortsätt redigera', 'ui_swap23': 'Byt plats på färgerna'}
        for key, value in expected.items(): self.assertEqual(value, self.strings[key])
        self.assertNotEqual(self.strings['ui_keep_editing23'], self.strings['ui_cancel'])
        self.assertIn('osparade ändringar', self.strings['ui_your_current_image_has_unsaved_changes'])

    def test_conditional_safety_and_retained_data_are_explicit(self):
        s = self.strings
        for key in ('ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_there_is_not_enough_memory_for_this_operation'):
            self.assertIn('Ingen automatisk storleksändring gjordes.', s[key])
        self.assertIn('Originalfilen förblir oförändrad.', s['ui_sampled_resize_memory_explanation'])
        self.assertIn('Bildmontaget är oförändrat.', s['ui_assembly_source_memory_floor'])
        self.assertIn('har behållits', s['ui_history_unavailable34'])
        self.assertIn('visas på engelska.', s['language20_translation_note'])

if __name__ == '__main__': unittest.main()
