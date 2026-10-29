"""110 bounded CA/RO P0 recovery/memory/encoding values, not whole-locale acceptance."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape, require_string_root
from test_danish_norwegian_p0_wording import full_format_tokens, require_reviewed_string
import memory_warning_source_review as warnings
from memory_warning_successors import accepted_warning, successors
import translation_catalogues as catalogues
from sk_sl_ca_priority_successors import current_fixture, added_keys, catalogue_count, current_display

KEYS = frozenset({
    'gallery_credit_could_not_save', 'gallery_credit_too_large', 'legacy_credits_unreadable',
    'save20_destination_error', 'save20_encoding_budget',
    'ui_a_separate_recovery_copy_has_been_kept_use', 'ui_an_assembly_source_image_is_missing',
    'ui_assembly_saved', 'ui_assembly_source_memory_floor', 'ui_autosave_failed_use_save',
    'ui_autosave_image_encoding_failed', 'ui_autosave_is_paused_to_protect_that_draft_use',
    'ui_autosave_metadata_is_missing', 'ui_autosave_paused_use_save', 'ui_autosave_pixels_are_missing',
    'ui_autosave_pixels_could_not_be_read', 'ui_autosave_selection_encoding_failed',
    'ui_cannot_create_the_undo_cache_free_some_device', 'ui_clear_all', 'ui_clear_image',
    'ui_could_not_export_the_recovery_copy', 'ui_could_not_open_image',
    'ui_could_not_save_the_assembly', 'ui_could_not_store_the_assembly',
    'ui_d_d_pixels_2f_mp_exceeds_the_current', 'ui_draft_not_saved_yet', 'ui_draft_restored',
    'ui_draft_saved', 'ui_export_recovery_copy', 'ui_export_recovery_copy_144b8a',
    'ui_history_unavailable34', 'ui_invalid_autosave_metadata',
    'ui_keeps_pixels_at_the_top_left_smaller_canvas',
    'ui_not_enough_memory_for_this_operation_the_assembly',
    'ui_not_enough_memory_to_save_in_this_format', 'ui_png_encoding_failed',
    'ui_previous_draft_kept_for_recovery', 'ui_recovered_image',
    'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_resize_large_image',
    'ui_sampled_resize_memory_explanation', 'ui_save_png',
    'ui_the_draft_is_saving_try_again_shortly', 'ui_the_encoder_did_not_finish',
    'ui_the_previous_draft_could_not_be_moved_to',
    'ui_the_previous_draft_could_not_be_preserved_separately',
    'ui_the_previous_draft_could_not_be_restored', 'ui_the_previous_draft_needs_more_memory_to_reopen',
    'ui_the_saved_assembly_could_not_be_opened', 'ui_the_selected_location_is_not_writable',
    'ui_the_trim_would_remove_the_entire_image', 'ui_the_undo_cache_is_damaged',
    'ui_there_is_not_enough_memory_for_this_operation', 'ui_this_location_is_not_writable',
    'ui_unexpected_data_in_the_undo_cache',
})
TAGS = {'default', 'ca', 'ro'}
HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
         'ui_save_as_jpeg_xl', 'ui_save_as_png'}


class CatalanRomanianCompletionWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(current_fixture('catalan_romanian_completion_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('ca', 'values-ca'), ('ro', 'values-ro')]}
        cls.roots = {tag: ET.fromstring(value) for tag, value in cls.xml.items()}

    def test_exact_55_P0_values_attributes_and_complete_format_inventory(self):
        self.assertEqual(55, len(KEYS))
        tiers = json.loads((catalogues.DATA / 'string-importance.json').read_text())['tiers']
        p0 = set(next(t['keys'] for t in tiers if t['id'] == 'P0'))
        self.assertEqual(92, len(p0))
        self.assertTrue({'string/' + key for key in KEYS}.issubset(p0))
        for key in KEYS:
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            for tag in TAGS:
                with self.subTest(key=key, tag=tag):
                    require_reviewed_string(self.xml[tag], key, self.data['values'][key][tag],
                                            self.data['constraints'][key][tag], self.data['values'][key]['default'])
                    self.assertEqual(self.roots['default'].find(f"./string[@name='{key}']").attrib,
                                     self.roots[tag].find(f"./string[@name='{key}']").attrib)
        for tag in ('ca', 'ro'):
            actual = {node.tag + '/' + node.get('name') for node in self.roots[tag]}
            self.assertEqual(87, len(actual & p0))
            self.assertEqual({'string/' + key for key in HOLDS}, p0 - actual)
            formatted_false = {key for key in KEYS if self.data['constraints'][key][tag]['attributes'].get('formatted') == 'false'}
            self.assertEqual({'ui_history_unavailable34'}, formatted_false)
        self.assertEqual({
            'ui_a_separate_recovery_copy_has_been_kept_use',
            'ui_autosave_is_paused_to_protect_that_draft_use',
            'ui_could_not_save_the_assembly', 'ui_d_d_pixels_2f_mp_exceeds_the_current',
            'ui_the_saved_assembly_could_not_be_opened',
        }, {key for key in KEYS if full_format_tokens(self.data['values'][key]['default'])})

    def test_every_value_rejects_missing_duplicate_empty_truncation_markup_attributes_type_and_tokens(self):
        for tag in ('ca', 'ro'):
            for key in KEYS:
                original = self.roots[tag].find(f"./string[@name='{key}']")
                for mutation in ('missing', 'duplicate', 'empty', 'truncate', 'markup', 'attribute', 'wrong-type', 'placeholder'):
                    root = ET.Element('resources');node = deepcopy(original)
                    if mutation != 'missing':root.append(node)
                    if mutation == 'duplicate':root.append(deepcopy(node))
                    elif mutation == 'empty':node.text = ''
                    elif mutation == 'truncate':node.text = node.text[:-1]
                    elif mutation == 'markup':ET.SubElement(node, 'b').text, node.text = node.text, None
                    elif mutation == 'attribute':node.set('translatable', 'false')
                    elif mutation == 'wrong-type':node.tag = 'plurals'
                    elif mutation == 'placeholder':node.text += ' %9$s'
                    with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                        require_reviewed_string(ET.tostring(root, encoding='unicode'), key,
                            self.data['values'][key][tag], self.data['constraints'][key][tag],
                            self.data['values'][key]['default'])

    def test_actual_formatted_false_values_reject_refreshed_unindexed_nonargument_and_malformed_tokens(self):
        key = 'ui_history_unavailable34'
        for tag in ('ca', 'ro'):
            constraints = self.data['constraints'][key][tag]
            self.assertEqual('false', constraints['attributes']['formatted'])
            source = self.data['values'][key]['default']
            self.assertFalse(full_format_tokens(source))
            # These are mutations of two real reviewed values, not synthetic resources.
            for suffix in (' %s', ' %d', ' %.2f', ' %1$s', ' %%', ' %n',
                           ' %', ' %q', ' %1$', ' %.', ' %3$.', ' %3$.f', ' %t'):
                changed = self.data['values'][key][tag] + suffix
                root = ET.Element('resources');ET.SubElement(root, 'string', constraints['attributes']).text = changed
                with self.subTest(tag=tag, suffix=suffix), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key, changed, constraints, source)

    def test_four_argument_memory_format_rejects_changed_index_type_precision_width_flags(self):
        key = 'ui_d_d_pixels_2f_mp_exceeds_the_current'
        tokens = {'%1$d': 1, '%2$d': 1, '%3$.2f': 1, '%4$.2f': 1}
        for tag in TAGS:
            self.assertEqual(tokens, full_format_tokens(self.data['values'][key][tag]))
        for tag in ('ca', 'ro'):
            for original, replacement in [('%1$d', '%2$d'), ('%1$d', '%1$s'), ('%3$.2f', '%3$.1f'),
                                          ('%1$d', '%1$4d'), ('%1$d', '%1$+d'), ('%1$d', '%d')]:
                changed = self.data['values'][key][tag].replace(original, replacement)
                root = ET.Element('resources')
                ET.SubElement(root, 'string', self.data['constraints'][key][tag]['attributes']).text = changed
                with self.subTest(tag=tag, replacement=replacement), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key, changed,
                                            self.data['constraints'][key][tag], self.data['values'][key]['default'])

    def test_inherited_values_attributes_with_only_exact_reviewed_priority_successors(self):
        from test_translations import SCOPED_TAGS
        self.assertEqual({'ca', 'ro'}, set(self.data['preserved_values']))
        for tag in ('ca', 'ro'):
            preserved = self.data['preserved_values'][tag]
            self.assertEqual(150, len(preserved));self.assertFalse(set(preserved) & KEYS)
            for key, expected in preserved.items():
                with self.subTest(tag=tag, key=key):
                    require_string_root(self.roots[tag], key, expected['value'], {'attributes': expected['attributes']})
            names = [(node.tag, node.get('name')) for node in self.roots[tag]]
            self.assertEqual(catalogue_count(tag,205), len(names));self.assertEqual(len(names), len(set(names)))
            self.assertEqual({('string', key) for key in set(preserved) | KEYS | added_keys(tag)}, set(names))
            self.assertNotIn(tag, SCOPED_TAGS)
            self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=False))
        self.assertEqual(59, len(SCOPED_TAGS))
        self.assertEqual(112, len(set(catalogues.offered_tags()) - SCOPED_TAGS))

    def test_five_holds_remain_while_explicit_reviewed_neighbors_advance(self):
        self.assertEqual(HOLDS, set(self.data['held_absent']))
        for tag in ('ca', 'ro'):
            for key in HOLDS | {'formats22_at_least_frames', 'ui_no_resize_fits_decoder_memory',
                                'ui_load_image', 'ui_choose_location', 'ui_share_saved_image'}:
                if key not in HOLDS:
                    successor = fixture('slovak_slovenian_catalan_priority_wording.json' if tag == 'ca' else 'ukrainian_lithuanian_romanian_priority_wording.json')['locales'][tag]['values'][key]
                    self.assertIsNone(successor['previous_target'])
                    require_string_root(self.roots[tag], key, successor['target'], {'attributes': successor['attributes']})
                else:
                    self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"), (tag, key))
            self.assertEqual('"' + current_display(tag,'save20_file_format') + '"', self.roots[tag].find("./string[@name='save20_file_format']").text)
        self.assertEqual('at least %1$d', self.roots['default'].find("./string[@name='formats22_at_least_frames']").text)
        self.assertEqual('Load image…', self.roots['default'].find("./string[@name='ui_load_image']").text)

    def test_recovery_compositions_keep_existing_actions_product_syntax_and_prefix_punctuation(self):
        for tag, menu, save, save_as in [('ca', 'Fitxer', 'Desa', 'Anomena i desa…'),
                                        ('ro', 'Fișier', 'Salvează', 'Salvează ca…')]:
            value = lambda key: self.data['values'][key][tag][1:-1]
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            self.assertIn(menu, paused);self.assertIn(save_as, paused)
            self.assertIn(value('ui_export_recovery_copy'), paused)
            self.assertIn(current_display(tag,'save20_file_format') + ': PNG / JPEG', paused)
            for key in ('ui_autosave_failed_use_save', 'ui_autosave_paused_use_save'):
                self.assertIn(save, value(key))
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            self.assertIn(menu + ' > ' + current_display(tag,'ui_load_image'), recovery)
            self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery)
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', value('ui_export_recovery_copy'))
            for key in ('ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy',
                        'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            for literal in ('AN Paint', '×', 'MP'):
                self.assertIn(literal, value('ui_d_d_pixels_2f_mp_exceeds_the_current'))

    def test_single_P0_warning_has_no_paired_acceptance_or_rewritten_history(self):
        key = 'ui_assembly_source_memory_floor';other = 'ui_no_resize_fits_decoder_memory'
        self.assertEqual({(tag, key) for tag in ('nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl', 'sr-Cyrl', 'sr-Latn', 'hr', 'bs')}, warnings.SINGLE_KEY_EXPECTATIONS)
        self.assertEqual(120, len(successors()));self.assertEqual(60, len({tag for tag, _ in successors()}))
        queue = warnings.review_record()
        for tag in ('ca', 'ro'):
            self.assertEqual('catalan_romanian_completion_wording.json', warnings.SINGLE_KEY_FIXTURES[tag])
            old = next(row for row in queue['options'] if row['tag'] == tag)
            for term in (key, other):
                self.assertIsNone(old['terms'][term]['value'])
                with self.assertRaises(ValueError):accepted_warning(term, tag)
            self.assertEqual(self.data['values'][key][tag], warnings.current_source_expectation(key, tag, None))
            addition = fixture('slovak_slovenian_catalan_priority_wording.json' if tag == 'ca' else 'ukrainian_lithuanian_romanian_priority_wording.json')['locales'][tag]['values'][other]
            self.assertIsNone(addition['previous_target'])
            self.assertEqual(addition['target'], warnings.current_source_expectation(other, tag, None))
            with self.assertRaises(ValueError):warnings.current_source_expectation(other, tag, addition['target'])
            with self.assertRaises(ValueError):warnings.current_source_expectation(key, tag, 'invented history')
            changed = deepcopy(queue);next(row for row in changed['options'] if row['tag'] == tag)['terms'][key]['value'] = 'invented history'
            with patch.object(warnings, 'review_record', return_value=changed), self.assertRaises(ValueError):
                warnings.current_source_expectation(key, tag, None)
            changed = deepcopy(self.data);changed['values'][key]['default'] += ' changed'
            with patch.object(warnings, 'fixture', return_value=changed), self.assertRaises(ValueError):
                warnings.current_source_expectation(key, tag, None)

    def test_fixture_scope_rejects_missing_extra_empty_or_wrong_locale(self):
        mutations = []
        d = deepcopy(self.data);d['values'].pop(next(iter(KEYS)));mutations.append(d)
        d = deepcopy(self.data);d['constraints'].pop(next(iter(KEYS)));mutations.append(d)
        d = deepcopy(self.data);d['values'][next(iter(KEYS))]['ca'] = '';mutations.append(d)
        d = deepcopy(self.data);d['values'][next(iter(KEYS))]['fr'] = 'unexpected';mutations.append(d)
        d = deepcopy(self.data);d['values']['save20_file_format'] = dict(d['values'][next(iter(KEYS))]);mutations.append(d)
        for data in mutations:
            with self.assertRaises(ValueError):require_wording_shape(data, KEYS, TAGS)


if __name__ == '__main__':
    unittest.main()
