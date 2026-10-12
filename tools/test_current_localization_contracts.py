"""Current wording, syntax, fallback and Unicode contracts, not linguistic certification."""
from pathlib import Path
import unittest
import unicodedata
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape
import translation_catalogues as catalogues
from test_translations import SCOPED_TAGS

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


def wording_fixture(name):
    return require_wording_shape(fixture(name), EXPECTED_KEYS[name],
        {'hu'} if name==FAMILIES[3] else {'default'}|SCOPED_TAGS)


def paths():
    return {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}


class CurrentLocalizationContracts(unittest.TestCase):
    def test_message_family_keys_and_nonempty_locale_contracts_are_required(self):
        from copy import deepcopy
        for name in FAMILIES:
            original=wording_fixture(name)
            tags={'hu'} if name==FAMILIES[3] else {'default'}|SCOPED_TAGS
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

    def test_explicit_scope_and_open_fallbacks_match_current_picker(self):
        scope = fixture('locale_contract_scope.json')
        self.assertEqual(SCOPED_TAGS, set(scope['scoped_tags']))
        self.assertEqual(59, len(scope['scoped_tags']))
        self.assertEqual(81, len(scope['fallback_tags']))
        self.assertFalse(set(scope['scoped_tags']) & set(scope['fallback_tags']))
        self.assertEqual(set(catalogues.offered_tags()), set(scope['scoped_tags'] + scope['fallback_tags']))

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
                self.assertEqual({'default'} | SCOPED_TAGS, set(values))
                for tag, root in xml.items():
                    with self.subTest(key=key, tag=tag):
                        self.assertEqual(int(tag in values), len(root.findall(f"./string[@name='{key}']")))

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


if __name__ == '__main__': unittest.main()
