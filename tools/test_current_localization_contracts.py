"""Bounded product fixtures and current resource structure; no catalogue approval mirrors."""
from pathlib import Path
import json
import re
import unittest
import unicodedata
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from current_localization_contracts import fixture, require_string, require_wording_shape, require_locale_scope, CURRENT_CATALOGUE_TAGS
from exact_script_priority_expectations import require_addition as exact_script_addition, decode_display
from test_translations import SCOPED_TAGS
from language_option_additions import ADDED_TAGS
ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ('commons_metadata_current_wording.json', 'commons_copy_credit_current_wording.json',
            'commons_svg_current_wording.json', 'hungarian_attribution_current_wording.json')
EXPECTED_KEYS = {
    FAMILIES[0]: {'commons_metadata_http_error','commons_metadata_response_too_large','commons_metadata_query_failed'},
    FAMILIES[1]: {'commons_credit_copy_failed','commons_credit_copy_failed_reason','commons_credit_copy_out_of_memory'},
    FAMILIES[2]: {'commons_svg_original_size_unavailable','commons_svg_original_size_too_large'},
    FAMILIES[3]: {'gallery_copy_credit','gallery_description','gallery_edit_credits','gallery_credit_copied',
        'gallery_credit_saved','ui_image_credits','ui_about_credits23','ui_credits_terms','ui_icons_fonts_artwork_credits',
        'ui_open_source_credits_and_notices','ui_gimp_translations31','ui_catrobat_s_own_artwork_uses_cc_by_sa',
        'ui_irasutoya_help34','ui_openclipart_help34','ui_help23','ui_add_up_to_20_images_with_android_s',
        'ui_the_arrow_on_the_left_directly_below_the'},
}

FAMILY_EXTRA_TAGS = {FAMILIES[0]: {'cs', 'sv'}, FAMILIES[1]: {'cs', 'sv'}, FAMILIES[2]: {'am', 'cs', 'pl', 'sv', 'bg', 'bn', 'tt-Latn'}}

def wording_tags(name):
    tags = {'hu'} if name == FAMILIES[3] else {'default'} | SCOPED_TAGS | FAMILY_EXTRA_TAGS.get(name, set())
    return tags - CURRENT_CATALOGUE_TAGS if name == FAMILIES[2] else tags

def wording_fixture(name):
    data = fixture(name)
    if name == FAMILIES[2]:
        for key in EXPECTED_KEYS[name]:
            row = exact_script_addition('tt-Latn', key, None, data['values'][key]['default'], already_present='tt-Latn' in data['values'][key])
            data['values'][key]['tt-Latn'] = row['reviewed_value']
    if name == FAMILIES[2]:
        for values in data['values'].values():
            for tag in CURRENT_CATALOGUE_TAGS:
                values.pop(tag, None)
    return require_wording_shape(data, EXPECTED_KEYS[name], wording_tags(name))

TAGGED_COLOUR_KEY = 'save20_unsupported_image_colour'
TAGGED_COLOUR_EXTRA_TAGS = {'am', 'cs', 'pl', 'sv', 'bg', 'bn', 'tt-Latn'}

def current_tagged_colour_data():
    data = json.loads((ROOT / 'Paintroid/src/test/resources/tagged-colour/expected.json').read_text())
    english = catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    data['tt-Latn'] = exact_script_addition('tt-Latn', TAGGED_COLOUR_KEY, None, english, already_present='tt-Latn' in data)['compiled_display']
    return {tag: value for tag, value in data.items() if tag not in CURRENT_CATALOGUE_TAGS}

def tagged_colour_expectations(data):
    if set(data) != (SCOPED_TAGS | TAGGED_COLOUR_EXTRA_TAGS) - CURRENT_CATALOGUE_TAGS:
        raise ValueError('Bounded tagged-colour fixture locale inventory differs')
    if not all(isinstance(value, str) and value for value in data.values()):
        raise ValueError('Tagged-colour expectations must be nonempty strings')
    for tag, name in [('cs', 'czech'), ('pl', 'polish'), ('sv', 'swedish')]:
        suffix = '_priority_current_wording.json' if tag == 'sv' else '_priority_draft_wording.json'
        if data[tag] != fixture(name + suffix)['values'][TAGGED_COLOUR_KEY][tag]:
            raise ValueError('Bounded tagged-colour value differs: ' + tag)
    for tag in ('bg', 'bn'):
        if data[tag] != fixture('bulgarian_bengali_priority_wording.json')['values'][TAGGED_COLOUR_KEY][tag].replace("\\'", "'"):
            raise ValueError('Bounded tagged-colour value differs: ' + tag)
    if data['am'] != decode_display(fixture('amharic_priority.json')['values'][TAGGED_COLOUR_KEY]['expected']):
        raise ValueError('Amharic tagged-colour value differs')
    english = catalogues.read_strings(catalogues.RES/'values/strings.xml')[TAGGED_COLOUR_KEY]
    if data['tt-Latn'] != exact_script_addition('tt-Latn', TAGGED_COLOUR_KEY, None, english)['compiled_display']:
        raise ValueError('Exact-script tagged-colour value differs')
    return data

def require_tagged_colour_resolution(data, strings, offered, english):
    data = tagged_colour_expectations(data)
    for tag in set(offered) - CURRENT_CATALOGUE_TAGS:
        expected = data.get(tag, english)
        actual = decode_display(strings[tag].get(TAGGED_COLOUR_KEY, english))
        if actual != expected:
            raise ValueError('Bounded tagged-colour value or English fallback differs: ' + tag)

def paths():
    return {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}

class CurrentLocalizationContracts(unittest.TestCase):
    def test_current_svg_resources_preserve_independent_format_and_literal_constraints(self):
        data = fixture(FAMILIES[2])
        for tag in CURRENT_CATALOGUE_TAGS:
            strings = catalogues.read_strings(catalogues.catalogue_paths()[tag])
            for key in EXPECTED_KEYS[FAMILIES[2]]:
                if key not in strings:
                    continue  # Presence/fallback routing is a separate product contract.
                value = strings[key]
                source = data['values'][key]['default']
                with self.subTest(tag=tag, key=key):
                    self.assertEqual(catalogues.placeholders(source), catalogues.placeholders(value))
                    self.assertEqual([], catalogues.literal_token_errors(key, value, source))
                    for literal in data['constraints'][key].get('required_literals', []):
                        self.assertIn(literal, value)

    def test_message_family_keys_and_nonempty_locale_contracts_are_required(self):
            from copy import deepcopy
            for name in FAMILIES:
                original=wording_fixture(name)
                tags=wording_tags(name)
                for key in EXPECTED_KEYS[name]:
                    for mutation in ('missing-key','empty-values','missing-locale','empty-text','missing-constraint'):
                        data=deepcopy(original)
                        if mutation=='missing-key': del data['values'][key]
                        if mutation=='empty-values': data['values'][key]={}
                        if mutation=='missing-locale': data['values'][key].pop(next(iter(tags)))
                        if mutation=='empty-text': data['values'][key][next(iter(tags))]=''
                        if mutation=='missing-constraint': del data['constraints'][key]
                        with self.subTest(name=name,key=key,mutation=mutation),self.assertRaises(ValueError):
                            require_wording_shape(data,EXPECTED_KEYS[name],tags)
                data=deepcopy(original);data['values']={}
                with self.assertRaises(ValueError): require_wording_shape(data,EXPECTED_KEYS[name],tags)

    def test_bounded_tagged_colour_values_and_fallbacks(self):
        data = current_tagged_colour_data()
        strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
        require_tagged_colour_resolution(data, strings, set(catalogues.offered_tags()), strings['default'][TAGGED_COLOUR_KEY])

    def test_tagged_colour_oracle_rejects_missing_localization_and_arbitrary_defaults(self):
            data = current_tagged_colour_data()
            strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
            offered = set(catalogues.offered_tags())
            english = strings['default'][TAGGED_COLOUR_KEY]
            for tag in TAGGED_COLOUR_EXTRA_TAGS:
                for mutation in ('missing-resource', 'english-resource', 'arbitrary-resource',
                                 'missing-oracle', 'english-oracle', 'arbitrary-oracle'):
                    changed_data = dict(data)
                    changed_strings = dict(strings)
                    changed_strings[tag] = dict(strings[tag])
                    if mutation == 'missing-resource': changed_strings[tag].pop(TAGGED_COLOUR_KEY)
                    elif mutation == 'english-resource': changed_strings[tag][TAGGED_COLOUR_KEY] = english
                    elif mutation == 'arbitrary-resource': changed_strings[tag][TAGGED_COLOUR_KEY] = 'arbitrary default'
                    elif mutation == 'missing-oracle': changed_data.pop(tag)
                    elif mutation == 'english-oracle': changed_data[tag] = english
                    else: changed_data[tag] = 'arbitrary default'
                    with self.subTest(tag=tag, mutation=mutation), self.assertRaises(ValueError):
                        require_tagged_colour_resolution(changed_data, changed_strings, offered, english)
            fallback = sorted(offered - set(data) - CURRENT_CATALOGUE_TAGS)[0]
            changed_strings = dict(strings)
            changed_strings[fallback] = dict(strings[fallback])
            changed_strings[fallback][TAGGED_COLOUR_KEY] = english
            require_tagged_colour_resolution(data, changed_strings, offered, english)
            changed_strings[fallback][TAGGED_COLOUR_KEY] = 'arbitrary default'
            with self.assertRaises(ValueError):
                require_tagged_colour_resolution(data, changed_strings, offered, english)

    def test_explicit_scope_and_open_fallbacks_match_current_picker(self):
            scope = fixture('locale_contract_scope.json')
            scoped, fallback = require_locale_scope(scope, SCOPED_TAGS, catalogues.offered_tags())
            self.assertEqual(59, len(scoped))
            self.assertEqual(112, len(fallback))
            self.assertEqual(27, len(ADDED_TAGS))
            self.assertLessEqual(ADDED_TAGS, fallback)
            self.assertEqual(fallback - {'cs', 'sv'}, set(fixture('commons_import_current_wording.json')['remaining_other_offered_locales']))
            source = (ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsCopyCreditTranslationTest.kt').read_text()
            declaration = re.search(r'private val fallbackTags=setOf\((.*?)\n    \)', source, re.S)
            self.assertIsNotNone(declaration)
            runtime_fallbacks = re.findall(r'"([\w-]+)"', declaration.group(1))
            self.assertEqual(len(fallback - {'cs', 'sv'}), len(runtime_fallbacks))
            self.assertEqual(fallback - {'cs', 'sv'}, set(runtime_fallbacks))

    def test_missing_duplicate_overlapping_or_unknown_scope_tags_are_rejected(self):
            from copy import deepcopy
            original = fixture('locale_contract_scope.json')
            offered = catalogues.offered_tags()
            for field in ('scoped_tags', 'fallback_tags'):
                for mutation in ('missing-group', 'empty-group', 'missing-tag', 'duplicate-tag', 'unknown-tag'):
                    data = deepcopy(original)
                    if mutation == 'missing-group': del data[field]
                    if mutation == 'empty-group': data[field] = []
                    if mutation == 'missing-tag': data[field].pop()
                    if mutation == 'duplicate-tag': data[field].append(data[field][0])
                    if mutation == 'unknown-tag': data[field][0] = 'zz-unknown'
                    with self.subTest(field=field, mutation=mutation), self.assertRaises(ValueError):
                        require_locale_scope(data, SCOPED_TAGS, offered)
            data = deepcopy(original)
            data['fallback_tags'].append(data['scoped_tags'][0])
            with self.assertRaises(ValueError): require_locale_scope(data, SCOPED_TAGS, offered)
            for tag in ADDED_TAGS:
                data = deepcopy(original); data['fallback_tags'].remove(tag)
                with self.subTest(missing_added=tag), self.assertRaises(ValueError):
                    require_locale_scope(data, SCOPED_TAGS, offered)
            with self.assertRaises(ValueError): require_locale_scope(original, SCOPED_TAGS, offered + [offered[0]])

    def test_all_current_values_attributes_placeholders_and_legal_literals(self):
            xml = {tag: path.read_text() for tag, path in paths().items()}
            for name in FAMILIES:
                data = wording_fixture(name)
                for key, values in data['values'].items():
                    for tag, expected in values.items():
                        with self.subTest(family=name, key=key, tag=tag):
                            require_string(xml[tag], key, expected, data['constraints'][key])

    def test_whole_message_families_have_exact_localized_scope_and_no_english_filled_fallbacks(self):
            xml = {tag: ET.parse(path).getroot() for tag, path in paths().items()}
            for name in FAMILIES[:3]:
                data = wording_fixture(name)
                for key, values in data['values'].items():
                    self.assertEqual(wording_tags(name), set(values))
                    for tag, root in xml.items():
                        if name == FAMILIES[2] and tag in CURRENT_CATALOGUE_TAGS: continue
                        with self.subTest(key=key, tag=tag):
                            from current_localization_contracts import residual_rows, require_residual_or_previous
                            if tag not in values and (tag,key) in residual_rows():
                                require_residual_or_previous(root,tag,key)
                            else:self.assertEqual(int(tag in values), len(root.findall(f"./string[@name='{key}']")))

    def test_metadata_english_identity_and_language_specific_normalization(self):
            data = wording_fixture(FAMILIES[0])
            for key, expected in data['values'].items():
                equal = set(data['constraints'][key]['default_equal_tags']) | {'default'}
                for tag, value in expected.items():
                    self.assertEqual(tag in equal, value == expected['default'], (key, tag))
            for key, tags in data['nfc_and_no_category_C_required'].items():
                for tag in tags:
                    value = catalogues.read_strings(paths()[tag])[key]
                    self.assertEqual(value, unicodedata.normalize('NFC', value))
                    self.assertFalse(any(unicodedata.category(c).startswith('C') for c in value))

    def test_script_controls_and_variation_selectors_are_retained(self):
            for name in FAMILIES[:3]:
                for key, tags in wording_fixture(name).get('special_codepoint_counts', {}).items():
                    for tag, counts in tags.items():
                        value = catalogues.read_strings(paths()[tag])[key]
                        for point, count in counts.items():
                            self.assertEqual(count, value.count(chr(int(point[2:], 16))), (key, tag, point))

    def test_hungarian_instructions_reference_current_labels(self):
            data = wording_fixture('hungarian_attribution_current_wording.json')
            values = catalogues.read_strings(paths()['hu'])
            for key, labels in data['label_references'].items():
                for label in labels:
                    self.assertIn(values[label], values[key], (key, label))

    def test_missing_duplicate_changed_and_wrong_format_resources_fail(self):
            for name in FAMILIES:
                data = wording_fixture(name)
                for key, values in data['values'].items():
                    for tag, expected in values.items():
                        node = ET.parse(paths()[tag]).getroot().find(f"./string[@name='{key}']")
                        line = ET.tostring(node, encoding='unicode')
                        constraints = data['constraints'][key]
                        require_string('<resources>'+line+'</resources>', key, expected, constraints)
                        for broken in ('', line+line, line.replace('</string>', '? </string>'), line.replace('</string>', '%1$d</string>')):
                            with self.subTest(key=key, tag=tag), self.assertRaises(ValueError):
                                require_string('<resources>'+broken+'</resources>', key, expected, constraints)

    def test_independent_unrelated_resource_or_formatting_edits_are_allowed(self):
            xml = '<resources>\n<!-- ordinary refactor -->\n<string name="target">Commons</string><string name="other">New</string></resources>'
            self.assertEqual('Commons', require_string(xml, 'target', 'Commons'))

    def test_unicode_control_removal_is_rejected(self):
            data = wording_fixture(FAMILIES[0]); key = 'commons_metadata_query_failed'
            for tag, control in [('mn-Mong', '\u202f'), ('mnc-Mong', '\u180e')]:
                expected = data['values'][key][tag]
                self.assertIn(control, expected)
                xml = '<resources><string name="'+key+'">'+expected.replace(control, '')+'</string></resources>'
                with self.assertRaises(ValueError):
                    require_string(xml, key, expected, data['constraints'][key])

class ReviewedResidualSuccessorTests(unittest.TestCase):
    def test_complete_reviewed_successors_and_predecessors(self):
            from current_localization_contracts import residual_rows, require_residual_or_previous
            rows = residual_rows()
            english = ET.parse(catalogues.RES/'values/strings.xml').getroot()
            roots = {tag: ET.parse(catalogues.catalogue_paths()[tag]).getroot() for tag, _ in rows}
            self.assertEqual(1485, sum(r['previous_target'] is None for r in rows.values()))
            self.assertEqual({('gl','ui_discard'),('gl','ui_bg'),('gl','ui_fg'), ('xh','ui_free_form_select'),('xh','ui_palette'),('xh','ui_preview'),('xh','ui_rotate'),('sr-Cyrl','ui_discard'),('sr-Latn','ui_discard')} | {('csb', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('mww', 'ui_zoom_out'), ('yi', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('wa', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('se', 'ui_your_current_image_has_unsaved_changes'), ('sa', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('se', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('se', 'ui_ellipse'), ('mww', 'ui_drawing_canvas_pinch_and_move_two_fingers_to')},
                             {identity for identity,r in rows.items() if r['previous_target'] is not None} - {('br', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('shn', 'ui_brush')} - {('tok', 'save20_destination_error'), ('tok', 'ui_share_explanation34'), ('tok', 'ui_colour_palette_tap_for_foreground_hold_for_background'), ('tok', 'formats22_ascii_description'), ('tok', 'ui_autosave_is_paused_to_protect_that_draft_use'), ('tok', 'ui_not_enough_memory_to_finish_opening_this_image'), ('tok', 'commons_svg_original_size_unavailable'), ('tok', 'ui_tool_categories'), ('tok', 'ui_crop_preview_drag_an_edge_or_corner_drag'), ('ps', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('tok', 'ui_not_enough_memory_to_inspect_this_image'), ('nds', 'ui_save_a5d0d9'), ('tok', 'ui_a_separate_recovery_copy_has_been_kept_use'), ('nds', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'), ('tok', 'ui_tap_to_type_a_number')})
            for (tag,key),row in rows.items():
                with self.subTest(tag=tag,key=key):
                    require_string(ET.tostring(english,encoding='unicode'),key,row['source'],{'attributes':row['attributes']})
                    require_residual_or_previous(roots[tag],tag,key,row['previous_target'])
                    self.assertEqual([],catalogues.android_string_errors(row['target']))

    def test_new_kinyarwanda_gesture_hold_remains_absent_and_unaccepted(self):
            from current_localization_contracts import residual_rows, require_residual_or_previous
            held = fixture('reviewed_residuals_20261030.json')['new_holds']
            self.assertEqual(1, len(held))
            row = held[0]
            self.assertEqual(('rw', 'ui_pinch_and_pan_mode', 'hold_absent', None),
                             (row['locale'], row['key'], row['disposition'], row['target']))
            self.assertEqual('Pinch and pan mode', row['source'])
            self.assertTrue(row['reason'])
            self.assertNotIn((row['locale'], row['key']), residual_rows())
            root = ET.parse(catalogues.catalogue_paths()['rw']).getroot()
            require_residual_or_previous(root, row['locale'], row['key'])
            ET.SubElement(root, 'string', name=row['key']).text = 'unaccepted gesture'
            with self.assertRaises(ValueError):
                require_residual_or_previous(root, row['locale'], row['key'])

    def test_each_successor_rejects_missing_duplicate_wrong_type_and_full_message_corruption(self):
            from current_localization_contracts import residual_rows, require_residual_or_previous
            from copy import deepcopy
            for (tag,key),row in residual_rows().items():
                for mutation in ('missing','duplicate','type','truncate','argument','markup','attribute','predecessor'):
                    root=ET.Element('resources');node=ET.SubElement(root,'string',row['attributes']);node.text=row['target']
                    if mutation=='missing':root.remove(node)
                    elif mutation=='duplicate':root.append(deepcopy(node))
                    elif mutation=='type':node.tag='plurals'
                    elif mutation=='truncate':node.text=node.text[:-1]
                    elif mutation=='argument':node.text+=' %9$s'
                    elif mutation=='markup':ET.SubElement(node,'b').text='extra'
                    elif mutation=='attribute':node.set('translatable','false')
                    elif row['previous_target'] is None:root.remove(node)
                    else:node.text=row['previous_target']
                    with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):
                        require_residual_or_previous(root,tag,key,row['previous_target'])
            with self.assertRaises(ValueError):
                require_residual_or_previous(ET.fromstring('<resources><string name="ui_save_as">unreviewed</string></resources>'),'eu-ES','ui_save_as')

if __name__ == '__main__': unittest.main()
