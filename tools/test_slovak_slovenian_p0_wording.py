"""156 bounded SK/SL P0 whole values; not native, complete-locale or runtime acceptance."""
from collections import Counter
from copy import deepcopy
import json
import re
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import memory_warning_source_review as warnings
from memory_warning_successors import accepted_warning, successors
import translation_catalogues as catalogues

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
TAGS = {'default', 'sk', 'sl'}
HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
         'ui_save_as_jpeg_xl', 'ui_save_as_png'}


# Keep this stricter parser local to the reviewed family. Generic catalogue
# accounting permits literal percent signs in formatted=false resources and
# deliberately excludes non-argument tokens; neither rule can hide added tokens
# in these exact, source-bound values.
FULL_FORMAT_TOKEN = re.compile(
    r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?'
    r'(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')


def full_format_tokens(value):
    """Parse indexed/unindexed and non-argument tokens; reject any leftover %."""
    if '%' in FULL_FORMAT_TOKEN.sub('', value):
        raise ValueError('Invalid or unescaped format token')
    return Counter(FULL_FORMAT_TOKEN.findall(value))


def display_value(value):
    return value[1:-1] if value.startswith('"') and value.endswith('"') else value


def require_reviewed_string(xml, key, expected, constraints, source):
    """Keep complete text and full token inventory, even with formatted=false."""
    value = require_string(xml, key, expected, constraints)
    if full_format_tokens(value) != full_format_tokens(source):
        raise ValueError(key + ': complete format-token inventory differs')
    return value


class SlovakSlovenianP0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('slovak_slovenian_p0_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('sk', 'values-sk'), ('sl', 'values-sl')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}

    def test_exact_78_key_P0_family_and_complete_values_attributes_and_tokens(self):
        self.assertEqual(78, len(KEYS))
        self.assertTrue({'save20_file_format', 'ui_save_your_changes'}.isdisjoint(KEYS))
        tiers = json.loads((catalogues.DATA / 'string-importance.json').read_text())['tiers']
        self.assertTrue({'string/' + k for k in KEYS}.issubset(next(t['keys'] for t in tiers if t['id'] == 'P0')))
        for key in KEYS:
            self.assertEqual(TAGS, set(self.data['constraints'][key]))
            source = self.data['values'][key]['default']
            for tag in TAGS:
                with self.subTest(key=key, tag=tag):
                    require_reviewed_string(self.xml[tag], key, self.data['values'][key][tag],
                                            self.data['constraints'][key][tag], source)
                    self.assertEqual(self.roots['default'].find(f"./string[@name='{key}']").attrib,
                                     self.roots[tag].find(f"./string[@name='{key}']").attrib)
        for tag in ('sk', 'sl'):
            for key in ('ui_history_unavailable34', 'ui_share_explanation34'):
                self.assertEqual('false', self.roots[tag].find(f"./string[@name='{key}']").get('formatted'))

    def test_every_value_rejects_missing_duplicate_empty_truncated_markup_attributes_type_and_placeholder(self):
        for tag in ('sk', 'sl'):
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

    def test_full_format_tokens_reject_changed_index_type_precision_width_flags_and_literals(self):
        key = 'ui_d_d_pixels_2f_mp_exceeds_the_current'
        tokens = {'%1$d': 1, '%2$d': 1, '%3$.2f': 1, '%4$.2f': 1}
        for tag in TAGS:
            expected = self.data['values'][key][tag]
            self.assertEqual(tokens, catalogues.placeholders(expected))
            self.assertEqual(tokens, full_format_tokens(expected))
            mutations = [expected.replace('%3$.2f', replacement) for replacement in
                         ('%3$.3f', '%9$.2f', '%3$.2d', '%.2f', '%3$f', '%3$2f', '%3$-10.2f', '%3$', '%3$.f', '%q')]
            mutations += [expected + token for token in (' %9$s', ' %n', ' %%', ' %')]
            for changed in mutations:
                node = ET.Element('string', self.data['constraints'][key][tag]['attributes']);node.text = changed
                root = ET.Element('resources');root.append(node)
                # Use changed as the expected text so rejection exercises the
                # independent token/syntax guard, not just full-text inequality.
                with self.subTest(tag=tag, value=changed), self.assertRaises(ValueError):
                    require_reviewed_string(ET.tostring(root, encoding='unicode'), key, changed,
                        self.data['constraints'][key][tag], self.data['values'][key]['default'])

    def test_formatted_false_rejects_unindexed_non_argument_and_malformed_tokens_with_refreshed_expected(self):
        # Recognize both indexed and unindexed syntax, with precision, width,
        # flags, date/time and non-argument tokens; do not silently skip any %.
        recognized = ('%s', '%1$s', '%.2f', '%3$-10.2f', '%tY', '%1$tY', '%%', '%n')
        self.assertEqual(Counter(recognized), full_format_tokens(' '.join(recognized)))
        suffixes = (' %s', ' %d', ' %.2f', ' %1$s', ' %%', ' %n',
                    ' %', ' %q', ' %1$', ' %.', ' %3$.', ' %3$.f', ' %t')
        for tag in ('sk', 'sl'):
            for key in ('ui_history_unavailable34', 'ui_share_explanation34'):
                constraints = self.data['constraints'][key][tag]
                self.assertEqual('false', constraints['attributes']['formatted'])
                source = self.data['values'][key]['default']
                self.assertEqual(Counter(), full_format_tokens(source))
                for suffix in suffixes:
                    changed = self.data['values'][key][tag] + suffix
                    node = ET.Element('string', constraints['attributes']);node.text = changed
                    root = ET.Element('resources');root.append(node)
                    # A matching changed expectation must not bypass the
                    # source token contract, even when Android formatting is off.
                    with self.subTest(tag=tag, key=key, suffix=suffix), self.assertRaises(ValueError):
                        require_reviewed_string(ET.tostring(root, encoding='unicode'),
                            key, changed, constraints, source)

    def test_all_127_per_locale_prior_values_and_catalogue_identity_stay_unchanged(self):
        self.assertEqual({'sk', 'sl'}, set(self.data['preserved_values']))
        from test_translations import SCOPED_TAGS
        for tag, count in [('sk', 127), ('sl', 127)]:
            preserved = self.data['preserved_values'][tag]
            self.assertEqual(count, len(preserved));self.assertFalse(set(preserved) & KEYS)
            for key, expected in preserved.items():
                with self.subTest(tag=tag, key=key):
                    require_string(self.xml[tag], key, expected['value'], {'attributes': expected['attributes']})
            self.assertEqual(count + 78, len(self.roots[tag]))
            self.assertNotIn(tag, SCOPED_TAGS)
            self.assertEqual('Image format', self.roots[tag].find("./string[@name='save20_file_format']").text)
        self.assertTrue({'sk', 'sl'} <= set(catalogues.offered_tags()))
        self.assertEqual(59, len(SCOPED_TAGS))
        self.assertEqual(112, len(set(catalogues.offered_tags()) - SCOPED_TAGS))

    def test_five_holds_each_and_unreviewed_neighbor_fallbacks_remain_absent(self):
        self.assertEqual(HOLDS, set(self.data['held_absent']))
        neighbors = {'ui_no_resize_fits_decoder_memory', 'formats22_at_least_frames',
                     'ui_load_image', 'ui_choose_location', 'ui_image_assembly'}
        for tag in ('sk', 'sl'):
            for key in HOLDS | neighbors:
                self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"), (tag, key))
        self.assertEqual('at least %1$d', self.roots['default'].find("./string[@name='formats22_at_least_frames']").text)
        self.assertEqual('Load image…', self.roots['default'].find("./string[@name='ui_load_image']").text)

    def test_recovery_compositions_retain_actual_labels_and_literal_filenames(self):
        for tag, menu in [('sk', 'Súbor'), ('sl', 'Datoteka')]:
            value = lambda key: display_value(self.data['values'][key][tag])
            prior = self.data['preserved_values'][tag]
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            self.assertIn(menu + (' > ' if tag == 'sk' else ' → ') + 'Load image…', recovery)
            self.assertIn('canvas.png', recovery);self.assertIn('ZIP', recovery)
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            self.assertIn(menu + ' → ' + value('ui_export_recovery_copy'), paused)
            self.assertIn(menu + ' → ' + prior['save20_title']['value'][1:-1], paused)
            self.assertIn(prior['save20_file_format']['value'] + ': PNG / JPEG', paused)
            kept = value('ui_a_separate_recovery_copy_has_been_kept_use')
            self.assertIn(menu + (' > ' if tag == 'sk' else ' → ') + value('ui_export_recovery_copy'), kept)
            self.assertIn('canvas.png', kept);self.assertIn('ZIP', kept)

    def test_save_share_and_error_composition_keeps_command_and_punctuation_contracts(self):
        for tag in ('sk', 'sl'):
            value = lambda key: display_value(self.data['values'][key][tag])
            save = self.data['preserved_values'][tag]['ui_save']['value'][1:-1]
            save_as = self.data['preserved_values'][tag]['save20_title']['value'][1:-1]
            for key in ('ui_export_did_not_save23', 'ui_export_explanation23', 'ui_save_explanation23', 'ui_share_explanation34'):
                self.assertIn(save, value(key))
            self.assertIn(save_as, value('ui_export_did_not_save23'))
            self.assertEqual(value('ui_save_and_share_41edb4') + '…', value('ui_save_and_share'))
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', value('ui_export_recovery_copy'))
            for key in ('ui_could_not_save_image', 'ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy',
                        'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_saved')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_the_image_was_saved_but_android_could_not')))

    def test_single_P0_warnings_have_no_paired_acceptance_or_rewritten_history(self):
        key = 'ui_assembly_source_memory_floor';other = 'ui_no_resize_fits_decoder_memory'
        self.assertEqual({(tag, key) for tag in ('nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl', 'sr-Cyrl', 'sr-Latn')}, warnings.SINGLE_KEY_EXPECTATIONS)
        self.assertEqual({'tags': ['sk', 'sl'], 'key': key, 'historical_value': None,
                          'unreviewed_companion': other}, self.data['single_warning_scope'])
        self.assertEqual(120, len(successors()));self.assertEqual(60, len({tag for tag,k in successors()}))
        queue = warnings.review_record()
        for tag in ('sk', 'sl'):
            old = next(row for row in queue['options'] if row['tag'] == tag)
            for term in (key, other):
                self.assertIsNone(old['terms'][term]['value'])
                with self.assertRaises(ValueError):accepted_warning(term, tag)
            self.assertEqual(self.data['values'][key][tag], warnings.current_source_expectation(key, tag, None))
            self.assertIsNone(warnings.current_source_expectation(other, tag, None))
            with self.assertRaises(ValueError):warnings.current_source_expectation(key, tag, 'invented history')
            changed = deepcopy(queue);next(row for row in changed['options'] if row['tag'] == tag)['terms'][key]['value'] = 'invented history'
            with patch.object(warnings, 'review_record', return_value=changed), self.assertRaises(ValueError):
                warnings.current_source_expectation(key, tag, None)
            changed = deepcopy(self.data);changed['values'][key]['default'] += ' changed'
            with patch.object(warnings, 'fixture', return_value=changed), self.assertRaises(ValueError):
                warnings.current_source_expectation(key, tag, None)

    def test_family_scope_corruption_and_current_catalogue_validation(self):
        for mutation in ('missing-key', 'extra-key', 'wrong-locale', 'empty-value', 'missing-constraint'):
            data = deepcopy(self.data);key = next(iter(KEYS))
            if mutation == 'missing-key':data['values'].pop(key)
            elif mutation == 'extra-key':data['values']['not_reviewed'] = data['values'][key]
            elif mutation == 'wrong-locale':data['values'][key]['unreviewed'] = 'arbitrary'
            elif mutation == 'empty-value':data['values'][key]['sk'] = ''
            else:data['constraints'].pop(key)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):require_wording_shape(data, KEYS, TAGS)
        for tag in ('sk', 'sl'):
            self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=False))
            names = [(node.tag, node.get('name')) for node in self.roots[tag]]
            self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':unittest.main()
