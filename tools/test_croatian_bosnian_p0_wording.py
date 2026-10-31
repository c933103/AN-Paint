"""Current action, format, script and numeric-locale regressions; approval history is archived."""
import re
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import current_display


KEYS = frozenset({
    'formats22_animation_message', 'formats22_animation_poster', 'formats22_animation_still',
    'formats22_animation_title', 'formats22_animation_unknown', 'formats22_ascii_description',
    'formats22_open_still', 'formats22_pdf_raster_hint', 'gallery_credit_could_not_save',
    'gallery_credit_too_large', 'legacy_credits_unreadable', 'save20_destination_error',
    'save20_encoding_budget', 'save20_gif_description', 'save20_invalid_name',
    'save20_lossy_quality_description', 'save20_unsupported_image_colour',
    'ui_a_separate_recovery_copy_has_been_kept_use', 'ui_an_assembly_source_image_is_missing',
    'ui_assembly_saved', 'ui_assembly_source_memory_floor', 'ui_autosave_failed_use_save',
    'ui_autosave_image_encoding_failed', 'ui_autosave_is_paused_to_protect_that_draft_use',
    'ui_autosave_metadata_is_missing', 'ui_autosave_paused_use_save',
    'ui_autosave_pixels_are_missing', 'ui_autosave_pixels_could_not_be_read',
    'ui_autosave_selection_encoding_failed', 'ui_cannot_create_the_undo_cache_free_some_device',
    'ui_clear_all', 'ui_clear_image', 'ui_could_not_export_the_recovery_copy',
    'ui_could_not_open_image', 'ui_could_not_save_image', 'ui_could_not_save_the_assembly',
    'ui_could_not_store_the_assembly', 'ui_d_d_pixels_2f_mp_exceeds_the_current',
    'ui_draft_not_saved_yet', 'ui_draft_restored', 'ui_draft_saved', 'ui_export_did_not_save23',
    'ui_export_explanation23', 'ui_export_recovery_copy', 'ui_export_recovery_copy_144b8a',
    'ui_higher_quality_usually_makes_a_larger_file_lossless', 'ui_history_unavailable34',
    'ui_invalid_autosave_metadata', 'ui_keeps_pixels_at_the_top_left_smaller_canvas',
    'ui_not_enough_memory_for_this_operation_the_assembly',
    'ui_not_enough_memory_to_save_in_this_format', 'ui_png_encoding_failed',
    'ui_previous_draft_kept_for_recovery', 'ui_recovered_image',
    'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_resize_large_image',
    'ui_sampled_resize_memory_explanation', 'ui_save_and_share', 'ui_save_and_share_41edb4',
    'ui_save_explanation23', 'ui_save_png', 'ui_saved', 'ui_share_explanation34',
    'ui_the_draft_is_saving_try_again_shortly', 'ui_the_encoder_did_not_finish',
    'ui_the_image_was_saved_but_android_could_not', 'ui_the_previous_draft_could_not_be_moved_to',
    'ui_the_previous_draft_could_not_be_preserved_separately',
    'ui_the_previous_draft_could_not_be_restored',
    'ui_the_previous_draft_needs_more_memory_to_reopen',
    'ui_the_saved_assembly_could_not_be_opened', 'ui_the_selected_location_is_not_writable',
    'ui_the_trim_would_remove_the_entire_image', 'ui_the_undo_cache_is_damaged',
    'ui_there_is_not_enough_memory_for_this_operation', 'ui_this_location_is_not_writable',
    'ui_unexpected_data_in_the_undo_cache', 'ui_your_current_image_has_unsaved_changes'
})

class CroatianBosnianP0Tests(unittest.TestCase):

    def test_recovery_compositions_retain_actual_labels_and_literal_filenames(self):
        for tag in ('hr', 'bs'):
            value = lambda key: current_display(tag,key)
            prior = lambda key: current_display(tag,key)
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            for literal in (prior('ui_menu_file'), prior('ui_load_image'), 'canvas.png', 'ZIP'):
                self.assertIn(literal, recovery)
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            for literal in (prior('ui_menu_file'), value('ui_export_recovery_copy'), prior('save20_title'), prior('save20_file_format'), 'PNG', 'JPEG'):
                self.assertIn(literal, paused)
            kept = value('ui_a_separate_recovery_copy_has_been_kept_use')
            for literal in (prior('ui_menu_file'), value('ui_export_recovery_copy'), 'canvas.png', 'ZIP'):
                self.assertIn(literal, kept)

    def test_save_share_and_error_composition_keeps_command_and_punctuation_contracts(self):
        for tag in ('hr', 'bs'):
            value = lambda key: current_display(tag,key)
            prior = lambda key: current_display(tag,key)
            for key in ('ui_export_did_not_save23', 'ui_export_explanation23', 'ui_save_explanation23', 'ui_share_explanation34'):
                self.assertIn(prior('ui_save'), value(key))
            self.assertIn(prior('save20_title'), value('ui_export_did_not_save23'))
            self.assertEqual(value('ui_save_and_share_41edb4') + '…', value('ui_save_and_share'))
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', value('ui_export_recovery_copy'))
            for key in ('ui_could_not_save_image', 'ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy', 'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            for key in KEYS:self.assertNotRegex(value(key), r'[\u0400-\u04ff]')

    def test_numeric_locale_caption_table_covers_entire_runtime_loop(self):
        source = (catalogues.ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt').read_text()
        tags = re.findall(r'"([A-Za-z0-9-]+)"', source.split('private val tags=listOf(',1)[1].split(')',1)[0])
        table = source.split('val captions=mapOf(',1)[1].split('for(tag in tags)',1)[0]
        captions = re.findall(r'"([A-Za-z0-9-]+)"\s+to\s+\(',table)
        self.assertEqual(len(captions),len(set(captions)));self.assertEqual(set(tags),set(captions))
        self.assertTrue({'hr','bs'} <= set(tags))

    def test_dither_description_names_the_actual_operation_not_blurring(self):
        for tag, operation in (('hr', 'Dithering'), ('bs', 'Miješanje boja')):
            self.assertIn(operation.lower(), current_display(tag, 'save20_dither').lower())
            self.assertIn(operation.lower(), current_display(tag, 'save20_gif_description').lower())
        self.assertNotIn('Zamućivanje', current_display('hr', 'save20_gif_description'))


if __name__ == '__main__':
    unittest.main()
