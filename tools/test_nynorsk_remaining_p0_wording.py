"""72 exact NN P0 values; no whole-locale, native-human or runtime certification."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import memory_warning_source_review as warnings
from memory_warning_successors import accepted_warning, successors
import translation_catalogues as catalogues

KEYS = frozenset(['formats22_animation_message', 'formats22_animation_poster', 'formats22_animation_still', 'formats22_animation_title', 'formats22_animation_unknown', 'formats22_ascii_description', 'formats22_open_still', 'formats22_pdf_raster_hint', 'gallery_credit_could_not_save', 'gallery_credit_too_large', 'legacy_credits_unreadable', 'save20_destination_error', 'save20_encoding_budget', 'save20_file_format', 'save20_gif_description', 'save20_invalid_name', 'save20_lossy_quality_description', 'save20_unsupported_image_colour', 'ui_a_separate_recovery_copy_has_been_kept_use', 'ui_an_assembly_source_image_is_missing', 'ui_assembly_saved', 'ui_assembly_source_memory_floor', 'ui_autosave_failed_use_save', 'ui_autosave_image_encoding_failed', 'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_autosave_metadata_is_missing', 'ui_autosave_paused_use_save', 'ui_autosave_pixels_are_missing', 'ui_autosave_pixels_could_not_be_read', 'ui_autosave_selection_encoding_failed', 'ui_cannot_create_the_undo_cache_free_some_device', 'ui_clear_all', 'ui_clear_image', 'ui_could_not_export_the_recovery_copy', 'ui_could_not_open_image', 'ui_could_not_save_the_assembly', 'ui_could_not_store_the_assembly', 'ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_draft_not_saved_yet', 'ui_draft_restored', 'ui_draft_saved', 'ui_export_recovery_copy', 'ui_export_recovery_copy_144b8a', 'ui_higher_quality_usually_makes_a_larger_file_lossless', 'ui_history_unavailable34', 'ui_invalid_autosave_metadata', 'ui_keeps_pixels_at_the_top_left_smaller_canvas', 'ui_not_enough_memory_for_this_operation_the_assembly', 'ui_not_enough_memory_to_save_in_this_format', 'ui_png_encoding_failed', 'ui_previous_draft_kept_for_recovery', 'ui_recovered_image', 'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_resize_large_image', 'ui_sampled_resize_memory_explanation', 'ui_save_and_share', 'ui_save_and_share_41edb4', 'ui_save_png', 'ui_the_draft_is_saving_try_again_shortly', 'ui_the_encoder_did_not_finish', 'ui_the_image_was_saved_but_android_could_not', 'ui_the_previous_draft_could_not_be_moved_to', 'ui_the_previous_draft_could_not_be_preserved_separately', 'ui_the_previous_draft_could_not_be_restored', 'ui_the_previous_draft_needs_more_memory_to_reopen', 'ui_the_saved_assembly_could_not_be_opened', 'ui_the_selected_location_is_not_writable', 'ui_the_trim_would_remove_the_entire_image', 'ui_the_undo_cache_is_damaged', 'ui_there_is_not_enough_memory_for_this_operation', 'ui_this_location_is_not_writable', 'ui_unexpected_data_in_the_undo_cache'])


class NynorskRemainingP0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('nynorsk_p0_remaining_wording.json'), KEYS, {'default', 'nn'})
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('nn', 'values-b+nn')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}

    def test_all_complete_reviewed_values_and_source_contracts(self):
        self.assertEqual(72, len(KEYS))
        p0 = next(x['keys'] for x in json.loads((catalogues.DATA / 'string-importance.json').read_text())['tiers'] if x['id'] == 'P0')
        self.assertTrue({'string/' + k for k in KEYS}.issubset(p0))
        for key in KEYS:
            for tag in ('default', 'nn'):
                with self.subTest(key=key, tag=tag):
                    require_string(self.xml[tag], key, self.data['values'][key][tag], self.data['constraints'][key][tag])
        self.assertEqual('false', self.roots['nn'].find("./string[@name='ui_history_unavailable34']").get('formatted'))

    def test_each_value_rejects_missing_duplicate_truncation_markup_attributes_types_and_placeholders(self):
        for key in KEYS:
            original = self.roots['nn'].find(f"./string[@name='{key}']")
            for mutation in ('missing', 'duplicate', 'truncate', 'markup', 'attribute', 'wrong-type', 'placeholder'):
                root = ET.Element('resources');node = deepcopy(original)
                if mutation != 'missing':root.append(node)
                if mutation == 'duplicate':root.append(deepcopy(node))
                elif mutation == 'truncate':node.text = node.text[:-1]
                elif mutation == 'markup':ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'attribute':node.set('translatable', 'false')
                elif mutation == 'wrong-type':node.tag = 'plurals'
                elif mutation == 'placeholder':node.text += ' %9$s'
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, self.data['values'][key]['nn'], self.data['constraints'][key]['nn'])

    def test_prior_118_values_aliases_attributes_and_global_scope_stay_exact(self):
        preserved = self.data['preserved_values']
        self.assertEqual(118, len(preserved));self.assertFalse(set(preserved) & KEYS)
        for key, expected in preserved.items():
            with self.subTest(key=key):
                require_string(self.xml['nn'], key, expected['value'], {'attributes': expected['attributes']})
        self.assertEqual(190, len(self.roots['nn']))
        from test_translations import SCOPED_TAGS
        self.assertNotIn('nn', SCOPED_TAGS)

    def test_five_holds_and_unreviewed_neighbor_fallbacks_remain_absent(self):
        holds = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg', 'ui_save_as_jpeg_xl', 'ui_save_as_png'}
        self.assertEqual(holds, set(self.data['held_absent']))
        for key in holds | {'ui_no_resize_fits_decoder_memory', 'formats22_at_least_frames', 'ui_load_image', 'ui_choose_location', 'ui_image_assembly'}:
            self.assertIsNone(self.roots['nn'].find(f"./string[@name='{key}']"), key)

    def test_recovery_and_animation_compositions_keep_actual_commands_and_quantity(self):
        value = lambda key: self.data['values'][key]['nn'].strip('"')
        recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
        self.assertIn('Fil > Load image…', recovery)
        self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery)
        self.assertIn('eit eventuelt flytande utval.', recovery)
        paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
        self.assertIn(value('ui_export_recovery_copy'), paused)
        self.assertIn(value('save20_file_format') + ': PNG / JPEG', paused)
        for key in ('formats22_animation_poster', 'formats22_animation_still'):
            self.assertTrue(value(key).endswith('Ved lagring vert det laga eit stillbilete.'))
        self.assertEqual({'%1$d':1, '%2$d':1, '%3$.2f':1, '%4$.2f':1}, catalogues.placeholders(value('ui_d_d_pixels_2f_mp_exceeds_the_current')))

    def test_single_warning_has_no_paired_acceptance_or_rewritten_history(self):
        key = 'ui_assembly_source_memory_floor';other = 'ui_no_resize_fits_decoder_memory'
        self.assertEqual({('nn', key)}, warnings.SINGLE_KEY_EXPECTATIONS)
        self.assertEqual(120, len(successors()));self.assertEqual(60, len({t for t,k in successors()}))
        queue = warnings.review_record();old = next(x for x in queue['options'] if x['tag'] == 'nn')
        for k in (key, other):
            self.assertIsNone(old['terms'][k]['value'])
            with self.assertRaises(ValueError):accepted_warning(k, 'nn')
        self.assertEqual(self.data['values'][key]['nn'], warnings.current_source_expectation(key, 'nn', None))
        self.assertIsNone(warnings.current_source_expectation(other, 'nn', None))
        with self.assertRaises(ValueError):warnings.current_source_expectation(key, 'nn', 'invented old value')
        changed = deepcopy(queue);next(x for x in changed['options'] if x['tag']=='nn')['terms'][key]['value'] = 'invented history'
        with patch.object(warnings, 'review_record', return_value=changed), self.assertRaises(ValueError):
            warnings.current_source_expectation(key, 'nn', None)
        changed = deepcopy(self.data);changed['values'][key]['default'] += ' changed'
        with patch.object(warnings, 'fixture', return_value=changed), self.assertRaises(ValueError):
            warnings.current_source_expectation(key, 'nn', None)

    def test_scope_corruption_and_current_catalogue_validation(self):
        for mutation in ('missing', 'extra', 'wrong-locale'):
            data = deepcopy(self.data);key = next(iter(KEYS))
            if mutation == 'missing':data['values'].pop(key)
            elif mutation == 'extra':data['values']['not_reviewed'] = data['values'][key]
            else:data['values'][key]['unreviewed'] = 'arbitrary'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):require_wording_shape(data, KEYS, {'default', 'nn'})
        self.assertEqual([], catalogues.validate_catalogue('nn', require_complete=False))
        names = [(n.tag, n.get('name')) for n in self.roots['nn']]
        self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':unittest.main()
