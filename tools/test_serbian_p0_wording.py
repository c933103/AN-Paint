"""149 current reviewed Serbian values; not native, complete-locale or runtime acceptance."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import re
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string, require_wording_shape
import memory_warning_source_review as warnings
from memory_warning_successors import accepted_warning, successors
import translation_catalogues as catalogues
import serbian_priority_delta_expectations as delta

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
    'ui_clear_all', 'ui_could_not_export_the_recovery_copy',
    'ui_could_not_open_image', 'ui_could_not_save_image', 'ui_could_not_save_the_assembly',
    'ui_could_not_store_the_assembly', 'ui_d_d_pixels_2f_mp_exceeds_the_current',
    'ui_draft_not_saved_yet', 'ui_draft_restored', 'ui_draft_saved', 'ui_export_did_not_save23',
    'ui_export_explanation23', 'ui_export_recovery_copy_144b8a',
    'ui_higher_quality_usually_makes_a_larger_file_lossless', 'ui_history_unavailable34',
    'ui_invalid_autosave_metadata', 'ui_keeps_pixels_at_the_top_left_smaller_canvas',
    'ui_not_enough_memory_for_this_operation_the_assembly',
    'ui_not_enough_memory_to_save_in_this_format', 'ui_png_encoding_failed',
    'ui_previous_draft_kept_for_recovery', 'ui_recovered_image',
    'ui_recovery_copy_exported_extract_canvas_png_from_the', 'ui_resize_large_image',
    'ui_sampled_resize_memory_explanation', 'ui_save_and_share_41edb4',
    'ui_save_explanation23', 'ui_save_png', 'ui_saved',
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
TAGS = {'default', 'sr-Cyrl', 'sr-Latn'}
HOLDS = {'formats22_derived_exported', 'ui_save_as', 'ui_save_as_jpeg',
         'ui_save_as_jpeg_xl', 'ui_save_as_png'}
FORMAT_KEY = 'save20_file_format'
PAUSED_KEY = 'ui_autosave_is_paused_to_protect_that_draft_use'
SUCCESSOR_LOCALE = 'sr-Cyrl'
# This is a compact, two-value current contract, not a whole-source hash or a
# reconstruction of historical snapshots. The separate immutable receipt binds
# the newly reviewed label and replacement warning atomically. The replaced
# warning remains one unique current value, not an additional accepted value.
FORMAT_LABEL_REVIEW = {
    'review_commit': '747437e11d94a88aeacc826cc8f2f7f227bc9a14',
    'review_path': 'records/localization-review/2026-10-26/serbian-p0/r04-format-label-review/review.json',
    'review_sha256': 'a2e91394fd6fcbbeaefafe4ee879df23fd4791a33dba565b0a31bfbc2f78b164',
    'locale': SUCCESSOR_LOCALE,
    'superseded_warning': PAUSED_KEY,
    'newly_reviewed_label': FORMAT_KEY,
    'unchanged_inherited_values': 337,
    'unchanged_prior_reviewed_values': 147,
    'current_unique_reviewed_values': 149,
    'accepted_pair_sha256': 'c84e7335b4bea3a9d2dc4d7857f8fdb9ea662d63d1c7368373dc7505df892511',
}


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


def require_format_label_successor(data, xml):
    """Validate both complete current values against one immutable pair receipt."""
    require_wording_shape(data, KEYS, TAGS)
    if data.get('review_successors') != FORMAT_LABEL_REVIEW:
        raise ValueError('Format-label review binding or accounting differs')
    label = data.get('format_label_successor')
    if (not isinstance(label, dict) or
            set(label) != {'locale', 'key', 'value', 'attributes'} or
            label['locale'] != SUCCESSOR_LOCALE or label['key'] != FORMAT_KEY or
            not isinstance(label['value'], str) or not label['value'] or
            label['attributes'] != {'name': FORMAT_KEY}):
        raise ValueError('Format-label successor scope or attributes differ')
    warning_by_tag = data['constraints'][PAUSED_KEY]
    if not isinstance(warning_by_tag, dict) or set(warning_by_tag) != TAGS:
        raise ValueError('Recovery successor constraint locale inventory differs')
    warning_constraints = warning_by_tag[SUCCESSOR_LOCALE]
    if warning_constraints != {
            'attributes': {'name': PAUSED_KEY}, 'placeholders': {'%1$s': 1},
            'child_elements': 0, 'formatted': True, 'escaped_newline_count': 0}:
        raise ValueError('Recovery successor constraints differ')
    pair = {
        FORMAT_KEY: {'value': label['value'], 'attributes': label['attributes']},
        PAUSED_KEY: {'value': data['values'][PAUSED_KEY][SUCCESSOR_LOCALE],
                     'attributes': warning_constraints['attributes']},
    }
    encoded = json.dumps(pair, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode('utf-8')
    if hashlib.sha256(encoded).hexdigest() != FORMAT_LABEL_REVIEW['accepted_pair_sha256']:
        raise ValueError('Complete format-label/recovery pair differs from reviewed receipt')
    # Token expectations are independent of any refreshed fixture expectation.
    if (full_format_tokens(label['value']) != Counter() or
            full_format_tokens(pair[PAUSED_KEY]['value']) != Counter({'%1$s': 1})):
        raise ValueError('Atomic pair format-token inventory differs')
    label_constraints = {'attributes': {'name': FORMAT_KEY}, 'placeholders': {},
                         'child_elements': 0, 'formatted': True, 'escaped_newline_count': 0}
    require_reviewed_string(xml['default'], FORMAT_KEY, 'File format',
                            label_constraints, 'File format')
    require_reviewed_string(xml[SUCCESSOR_LOCALE], FORMAT_KEY, label['value'],
                            label_constraints, 'File format')
    require_reviewed_string(xml[SUCCESSOR_LOCALE], PAUSED_KEY, pair[PAUSED_KEY]['value'],
                            warning_constraints, data['values'][PAUSED_KEY]['default'])
    return pair


class SerbianP0Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = require_wording_shape(fixture('serbian_p0_wording.json'), KEYS, TAGS)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('sr-Cyrl', 'values-b+sr+Cyrl'), ('sr-Latn', 'values-b+sr+Latn')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}

    def test_exact_74_key_P0_family_and_complete_values_attributes_and_tokens(self):
        self.assertEqual(74, len(KEYS))
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
        for tag in ('sr-Cyrl', 'sr-Latn'):
            for key in ('ui_history_unavailable34',):
                self.assertEqual('false', self.roots[tag].find(f"./string[@name='{key}']").get('formatted'))

    def test_every_value_rejects_missing_duplicate_empty_truncated_markup_attributes_type_and_placeholder(self):
        for tag in ('sr-Cyrl', 'sr-Latn'):
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
        for tag in ('sr-Cyrl', 'sr-Latn'):
            for key in ('ui_history_unavailable34',):
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

    def test_historical_337_values_keep_only_exact_bound_delta_and_catalogue_identity(self):
        self.assertEqual({'sr-Cyrl', 'sr-Latn'}, set(self.data['preserved_values']))
        self.assertEqual(337, sum(len(values) for values in self.data['preserved_values'].values()))
        from test_translations import SCOPED_TAGS
        for tag, count, total in [('sr-Cyrl', 169, 244), ('sr-Latn', 168, 242)]:
            preserved = self.data['preserved_values'][tag]
            self.assertEqual(count, len(preserved));self.assertFalse(set(preserved) & KEYS)
            for key, expected in preserved.items():
                with self.subTest(tag=tag, key=key):
                    source=self.roots['default'].find(f"./string[@name='{key}']").text
                    target=delta.current_value(tag,key,expected['value'],expected['attributes'],source)
                    require_string(self.xml[tag], key, target, {'attributes': expected['attributes']})
            added=sum(r['previous'] is None for r in delta.cohort()[tag]['values'].values())
            self.assertEqual(total+added, len(self.roots[tag]))
            self.assertEqual(total, count + 74 + (tag == SUCCESSOR_LOCALE))
            self.assertNotIn(tag, SCOPED_TAGS)
            self.assertEqual('"Формат датотеке"' if tag == SUCCESSOR_LOCALE else 'Format slike',
                             self.roots[tag].find(f"./string[@name='{FORMAT_KEY}']").text)
            self.assertEqual(tag != SUCCESSOR_LOCALE, FORMAT_KEY in preserved)
        self.assertTrue({'sr-Cyrl', 'sr-Latn'} <= set(catalogues.offered_tags()))
        self.assertEqual(59, len(SCOPED_TAGS))
        self.assertEqual(112, len(set(catalogues.offered_tags()) - SCOPED_TAGS))

    def test_atomic_format_label_pair_binds_full_values_attributes_tokens_and_unique_scope(self):
        pair = require_format_label_successor(self.data, self.xml)
        self.assertEqual({FORMAT_KEY, PAUSED_KEY}, set(pair))
        family = {(tag, key) for tag in ('sr-Cyrl', 'sr-Latn') for key in KEYS}
        unchanged = family - {(SUCCESSOR_LOCALE, PAUSED_KEY)}
        replacement = {(SUCCESSOR_LOCALE, key) for key in pair}
        self.assertEqual(148, len(family))
        self.assertEqual(147, len(unchanged))
        self.assertEqual(2, len(replacement))
        self.assertFalse(unchanged & replacement)
        current = unchanged | replacement
        self.assertEqual(family | {(SUCCESSOR_LOCALE, FORMAT_KEY)}, current)
        self.assertEqual(149, len(current))
        self.assertEqual(self.data['review_successors']['unchanged_prior_reviewed_values'], len(unchanged))
        self.assertEqual(self.data['review_successors']['current_unique_reviewed_values'], len(current))
        # The existing filename fields are distinct, unchanged full values, not
        # alternatives that may be used to label the format selection control.
        for tag in ('sr-Cyrl', 'sr-Latn'):
            filename = self.data['preserved_values'][tag]['save20_file_name']
            actual = require_string(self.xml[tag], 'save20_file_name', filename['value'],
                                    {'attributes': filename['attributes']})
            self.assertNotEqual(display_value(actual), display_value(
                self.roots[tag].find(f"./string[@name='{FORMAT_KEY}']").text))
        self.assertEqual('Format slike', self.data['preserved_values']['sr-Latn'][FORMAT_KEY]['value'])

    def test_atomic_pair_rejects_half_updates_and_xml_corruption(self):
        for key in (FORMAT_KEY, PAUSED_KEY):
            for mutation in ('missing', 'duplicate', 'empty', 'truncate', 'markup',
                             'attribute', 'wrong-type', 'placeholder', 'old-label',
                             'filename', 'newline', 'unquoted'):
                root = deepcopy(self.roots[SUCCESSOR_LOCALE])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing':root.remove(node)
                elif mutation == 'duplicate':root.append(deepcopy(node))
                elif mutation == 'empty':node.text = ''
                elif mutation == 'truncate':node.text = node.text[:-1]
                elif mutation == 'markup':ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'attribute':node.set('formatted', 'false')
                elif mutation == 'wrong-type':node.tag = 'plurals'
                elif mutation == 'placeholder':node.text += ' %2$s'
                elif mutation == 'old-label':node.text = node.text.replace('Формат датотеке', 'Име слике')
                elif mutation == 'filename':node.text = node.text.replace('Формат датотеке', 'Назив датотеке')
                elif mutation == 'newline':node.text += '\\n'
                else:node.text = display_value(node.text)
                changed = dict(self.xml);changed[SUCCESSOR_LOCALE] = ET.tostring(root, encoding='unicode')
                # Only one resource is changed in each case: neither the label
                # alone nor the warning alone may leave the accepted pair.
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_format_label_successor(self.data, changed)

    def test_matching_fixture_and_xml_edits_cannot_refresh_atomic_pair_acceptance(self):
        for key in (FORMAT_KEY, PAUSED_KEY):
            for mutation in ('wording', 'old-label', 'filename', 'placeholder', 'attribute', 'polarity'):
                data = deepcopy(self.data);root = deepcopy(self.roots[SUCCESSOR_LOCALE])
                node = root.find(f"./string[@name='{key}']")
                if mutation == 'wording':node.text += ' changed'
                elif mutation == 'old-label':node.text = node.text.replace('Формат датотеке', 'Име слике')
                elif mutation == 'filename':node.text = node.text.replace('Формат датотеке', 'Назив датотеке')
                elif mutation == 'placeholder':node.text += ' %9$s'
                elif mutation == 'attribute':node.set('translatable', 'false')
                elif key == PAUSED_KEY:node.text = node.text.replace('је паузирано', 'није паузирано')
                else:node.text = '"Није формат датотеке"'
                if key == FORMAT_KEY:
                    data['format_label_successor']['value'] = node.text
                    data['format_label_successor']['attributes'] = dict(node.attrib)
                else:
                    data['values'][key][SUCCESSOR_LOCALE] = node.text
                    data['constraints'][key][SUCCESSOR_LOCALE]['attributes'] = dict(node.attrib)
                changed = dict(self.xml);changed[SUCCESSOR_LOCALE] = ET.tostring(root, encoding='unicode')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_format_label_successor(data, changed)
        # Updating the expected digest as well cannot manufacture a new review.
        data = deepcopy(self.data);data['format_label_successor']['value'] += ' changed'
        pair = {FORMAT_KEY: {'value': data['format_label_successor']['value'],
                             'attributes': data['format_label_successor']['attributes']},
                PAUSED_KEY: {'value': data['values'][PAUSED_KEY][SUCCESSOR_LOCALE],
                             'attributes': data['constraints'][PAUSED_KEY][SUCCESSOR_LOCALE]['attributes']}}
        data['review_successors']['accepted_pair_sha256'] = hashlib.sha256(json.dumps(
            pair, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
        root = deepcopy(self.roots[SUCCESSOR_LOCALE])
        root.find(f"./string[@name='{FORMAT_KEY}']").text = data['format_label_successor']['value']
        changed = dict(self.xml);changed[SUCCESSOR_LOCALE] = ET.tostring(root, encoding='unicode')
        with self.assertRaises(ValueError):require_format_label_successor(data, changed)

    def test_atomic_pair_rejects_scope_receipt_accounting_and_constraint_corruption(self):
        for field, expected in FORMAT_LABEL_REVIEW.items():
            for mutation in ('missing', 'changed'):
                data = deepcopy(self.data)
                if mutation == 'missing':data['review_successors'].pop(field)
                else:data['review_successors'][field] = expected + 1 if type(expected) is int else expected + ' changed'
                with self.subTest(field=field, mutation=mutation), self.assertRaises(ValueError):
                    require_format_label_successor(data, self.xml)
        for field in ('locale', 'key', 'value', 'attributes'):
            data = deepcopy(self.data);data['format_label_successor'].pop(field)
            with self.subTest(missing=field), self.assertRaises(ValueError):
                require_format_label_successor(data, self.xml)
        for field, value in [('locale', 'sr-Latn'), ('key', 'save20_file_name'),
                             ('value', ''), ('attributes', {'name': FORMAT_KEY, 'formatted': 'false'})]:
            data = deepcopy(self.data);data['format_label_successor'][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                require_format_label_successor(data, self.xml)
        for field in self.data['constraints'][PAUSED_KEY][SUCCESSOR_LOCALE]:
            data = deepcopy(self.data);data['constraints'][PAUSED_KEY][SUCCESSOR_LOCALE].pop(field)
            with self.subTest(constraint=field), self.assertRaises(ValueError):
                require_format_label_successor(data, self.xml)
        for mutation in ('extra-receipt-field', 'extra-label-field', 'missing-constraint-locale',
                         'extra-constraint-locale'):
            data = deepcopy(self.data)
            if mutation == 'extra-receipt-field':data['review_successors']['extra'] = 'unreviewed'
            elif mutation == 'extra-label-field':data['format_label_successor']['extra'] = 'unreviewed'
            elif mutation == 'missing-constraint-locale':data['constraints'][PAUSED_KEY].pop(SUCCESSOR_LOCALE)
            else:data['constraints'][PAUSED_KEY]['unreviewed'] = data['constraints'][PAUSED_KEY][SUCCESSOR_LOCALE]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_format_label_successor(data, self.xml)

    def test_five_historical_holds_and_three_exact_reviewed_neighbor_additions(self):
        self.assertEqual(HOLDS, set(self.data['held_absent']))
        neighbors = {'ui_no_resize_fits_decoder_memory', 'formats22_at_least_frames',
                     'ui_choose_location'}
        for tag in ('sr-Cyrl', 'sr-Latn'):
            for key in HOLDS:
                self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"), (tag, key))
            for key in neighbors:
                source=self.roots['default'].find(f"./string[@name='{key}']").text
                target=delta.addition(tag,key,source,None)
                require_string(self.xml[tag],key,target,{'attributes':{'name':key},'child_elements':0})
        self.assertEqual('at least %1$d', self.roots['default'].find("./string[@name='formats22_at_least_frames']").text)
        self.assertEqual('Load image…', self.roots['default'].find("./string[@name='ui_load_image']").text)

    def test_recovery_compositions_retain_actual_labels_and_literal_filenames(self):
        for tag in ('sr-Cyrl', 'sr-Latn'):
            value = lambda key: display_value(self.data['values'][key][tag])
            prior = lambda key: display_value(self.data['preserved_values'][tag][key]['value'])
            recovery = value('ui_recovery_copy_exported_extract_canvas_png_from_the')
            for literal in (prior('ui_menu_file'), prior('ui_load_image'), 'canvas.png', 'ZIP'):
                self.assertIn(literal, recovery)
            paused = value('ui_autosave_is_paused_to_protect_that_draft_use')
            format_label = (display_value(self.data['format_label_successor']['value'])
                            if tag == SUCCESSOR_LOCALE else prior(FORMAT_KEY))
            for literal in (prior('ui_menu_file'), prior('ui_export_recovery_copy'), prior('save20_title'), format_label, 'PNG', 'JPEG'):
                self.assertIn(literal, paused)
            kept = value('ui_a_separate_recovery_copy_has_been_kept_use')
            for literal in (prior('ui_menu_file'), prior('ui_export_recovery_copy'), 'canvas.png', 'ZIP'):
                self.assertIn(literal, kept)

    def test_save_share_and_error_composition_keeps_command_and_punctuation_contracts(self):
        for tag in ('sr-Cyrl', 'sr-Latn'):
            value = lambda key: display_value(self.data['values'][key][tag])
            prior = lambda key: display_value(self.data['preserved_values'][tag][key]['value'])
            for key in ('ui_export_did_not_save23', 'ui_export_explanation23', 'ui_save_explanation23'):
                self.assertIn(prior('ui_save'), value(key))
            self.assertIn(prior('save20_title'), value('ui_export_did_not_save23'))
            self.assertEqual(value('ui_save_and_share_41edb4') + '…', prior('ui_save_and_share'))
            self.assertEqual(value('ui_export_recovery_copy_144b8a') + '…', prior('ui_export_recovery_copy'))
            for key in ('ui_could_not_save_image', 'ui_could_not_open_image', 'ui_could_not_export_the_recovery_copy', 'ui_not_enough_memory_to_save_in_this_format'):
                self.assertFalse(value(key).endswith(('.', ':', '…')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_saved')))
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(value('ui_the_image_was_saved_but_android_could_not')))
            # New script values are checked separately; preserved catalogue quirks are not repaired here.
            for key in KEYS:
                if tag == 'sr-Latn':self.assertNotRegex(value(key), r'[\u0400-\u04ff]')
                else:self.assertRegex(value(key), r'[\u0400-\u04ff]')

    def test_numeric_locale_caption_table_covers_the_entire_runtime_loop(self):
        source = (catalogues.ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/NumericDisplayLocaleTest.kt').read_text()
        loop = source.split('private val tags=listOf(', 1)[1].split(')', 1)[0]
        tags = re.findall(r'"([^"\n]+)"', loop)
        table = source.split('val captions=mapOf(', 1)[1].split('for(tag in tags)', 1)[0]
        caption_tags = re.findall(r'"([A-Za-z0-9-]+)"\s+to\s+\(', table)
        self.assertEqual(len(tags), len(set(tags)))
        self.assertEqual(len(caption_tags), len(set(caption_tags)))
        self.assertEqual(set(tags), set(caption_tags))
        for tag in ('sr-Cyrl', 'sr-Latn'):
            expected = ('"' + tag + '" to ("Current safe editing budget: 25,7 MiB · up to 2,25 MP before decoder overhead" to')
            self.assertIn(expected, table)
        # The unchanged P1 text falls back to English, but numeric formatting uses Serbian.
        self.assertIn('Current safe editing budget: 17,2 MiB · up to 1,50 MP before decoder overhead', table)

    def test_single_P0_warnings_have_no_paired_acceptance_or_rewritten_history(self):
        key = 'ui_assembly_source_memory_floor';other = 'ui_no_resize_fits_decoder_memory'
        self.assertEqual({(tag, key) for tag in ('nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl', 'sr-Cyrl', 'sr-Latn', 'hr', 'bs')}, warnings.SINGLE_KEY_EXPECTATIONS)
        self.assertEqual({'tags': ['sr-Cyrl', 'sr-Latn'], 'key': key, 'historical_value': None,
                          'unreviewed_companion': other}, self.data['single_warning_scope'])
        self.assertEqual(120, len(successors()));self.assertEqual(60, len({tag for tag,k in successors()}))
        queue = warnings.review_record()
        for tag in ('sr-Cyrl', 'sr-Latn'):
            old = next(row for row in queue['options'] if row['tag'] == tag)
            for term in (key, other):
                self.assertIsNone(old['terms'][term]['value'])
                with self.assertRaises(ValueError):accepted_warning(term, tag)
            self.assertEqual(self.data['values'][key][tag], warnings.current_source_expectation(key, tag, None))
            self.assertEqual(delta.addition(tag,other,queue['keys'][other]['corrected_english'],None),
                             warnings.current_source_expectation(other,tag,None))
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
            elif mutation == 'empty-value':data['values'][key]['sr-Cyrl'] = ''
            else:data['constraints'].pop(key)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):require_wording_shape(data, KEYS, TAGS)
        for tag in ('sr-Cyrl', 'sr-Latn'):
            self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=False))
            names = [(node.tag, node.get('name')) for node in self.roots[tag]]
            self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':unittest.main()
