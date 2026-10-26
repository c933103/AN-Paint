"""Current wording, syntax, fallback and Unicode contracts, not linguistic certification."""
from pathlib import Path
import json
import re
import unittest
import unicodedata
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string, require_wording_shape, require_locale_scope
import translation_catalogues as catalogues
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


# Additions are message-family-specific. Czech and Swedish have independently reviewed metadata/copy-credit values.
FAMILY_EXTRA_TAGS = {FAMILIES[0]: {'cs', 'sv'}, FAMILIES[1]: {'cs', 'sv'}, FAMILIES[2]: {'am', 'cs', 'pl', 'sv', 'bg', 'bn'}}


def wording_tags(name):
    return {'hu'} if name == FAMILIES[3] else {'default'} | SCOPED_TAGS | FAMILY_EXTRA_TAGS.get(name, set())


def wording_fixture(name):
    return require_wording_shape(fixture(name), EXPECTED_KEYS[name], wording_tags(name))


TAGGED_COLOUR_KEY = 'save20_unsupported_image_colour'
TAGGED_COLOUR_EXTRA_TAGS = {'am', 'cs', 'pl', 'sv', 'bg', 'bn', 'nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl'}
# Explicit runtime parent inheritance, not an additional reviewed catalogue.
TAGGED_COLOUR_INHERITED_CATALOGUES = {'ca-ES-valencia': 'ca'}


def tagged_colour_expectations(data):
    if set(data) != SCOPED_TAGS | TAGGED_COLOUR_EXTRA_TAGS:
        raise ValueError('Tagged-colour family locale inventory differs')
    if not all(isinstance(value, str) and value for value in data.values()):
        raise ValueError('Tagged-colour expectations must be complete nonempty strings')
    for tag, name in [('cs', 'czech'), ('pl', 'polish'), ('sv', 'swedish')]:
        suffix = '_priority_current_wording.json' if tag == 'sv' else '_priority_draft_wording.json'
        reviewed = fixture(name + suffix)['values'][TAGGED_COLOUR_KEY][tag]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed complete pair: ' + tag)
    for tag in ('bg', 'bn'):
        reviewed = fixture('bulgarian_bengali_priority_wording.json')['values'][TAGGED_COLOUR_KEY][tag]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour priority expectation differs: ' + tag)
    reviewed_am = fixture('amharic_priority.json')['values'][TAGGED_COLOUR_KEY]['expected'][1:-1]
    if data['am'] != reviewed_am:
        raise ValueError('Tagged-colour expectation differs from reviewed Amharic value')
    reviewed_nn = fixture('nynorsk_p0_remaining_wording.json')['values'][TAGGED_COLOUR_KEY]['nn'][1:-1]
    if data['nn'] != reviewed_nn:
        raise ValueError('Tagged-colour expectation differs from reviewed Nynorsk value')
    for tag in ('da', 'no'):
        reviewed = fixture('danish_norwegian_p0_wording.json')['values'][TAGGED_COLOUR_KEY][tag][1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed DA/NO value: ' + tag)
    for tag in ('ca', 'ro'):
        reviewed = fixture('catalan_romanian_import_wording.json')['values'][TAGGED_COLOUR_KEY][tag][1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed CA/RO value: ' + tag)
    for tag in ('sk', 'sl'):
        reviewed = fixture('slovak_slovenian_p0_wording.json')['values'][TAGGED_COLOUR_KEY][tag]
        if reviewed.startswith('"') and reviewed.endswith('"'):
            reviewed = reviewed[1:-1]
        if data[tag] != reviewed:
            raise ValueError('Tagged-colour expectation differs from reviewed SK/SL value: ' + tag)
    return data


def require_tagged_colour_resolution(data, strings, offered, english):
    """Model direct values and the one explicit parent fallback, checked by Android too."""
    data = tagged_colour_expectations(data)
    if not (set(TAGGED_COLOUR_INHERITED_CATALOGUES) |
            set(TAGGED_COLOUR_INHERITED_CATALOGUES.values())) <= set(offered):
        raise ValueError('Tagged-colour inheritance uses an unoffered catalogue')
    for tag in offered:
        parent = TAGGED_COLOUR_INHERITED_CATALOGUES.get(tag)
        if parent is not None and (tag in data or parent not in data or
                                   TAGGED_COLOUR_KEY in strings[tag]):
            raise ValueError('Explicit tagged-colour parent inheritance differs: ' + tag)
        catalogue = parent or tag
        expected = data[catalogue] if catalogue in data else english
        # Catalogue values retain Android apostrophe escapes; this family uses no other escapes.
        actual = strings[catalogue].get(TAGGED_COLOUR_KEY, english).replace("\\'", "'")
        if catalogue in ('am', 'nn', 'da', 'no', 'ca', 'ro', 'sk', 'sl') and actual.startswith('"') and actual.endswith('"'):
            actual = actual[1:-1]  # Android removes the reviewed outer quoting.
        if actual != expected:
            raise ValueError('Tagged-colour message or explicit English fallback differs: ' + tag)


def paths():
    return {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}


class CurrentLocalizationContracts(unittest.TestCase):
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

    def test_each_message_family_has_only_its_explicitly_reviewed_additions(self):
        svg = wording_fixture(FAMILIES[2])
        extra_tags = {'am', 'cs', 'pl', 'sv', 'bg', 'bn'}
        self.assertEqual({'cs', 'pl'}, set(svg['additional_draft_tags']))
        self.assertEqual({'am', 'sv', 'bg', 'bn'}, set(svg['additional_reviewed_tags']))
        self.assertEqual(extra_tags, FAMILY_EXTRA_TAGS[FAMILIES[2]])
        self.assertEqual(extra_tags, set(svg['additional_locale_review_status']))
        self.assertTrue(extra_tags.isdisjoint(SCOPED_TAGS))
        for name in FAMILIES[:2]:
            self.assertTrue({'pl'}.isdisjoint(wording_tags(name)))
            self.assertEqual({'default'} | SCOPED_TAGS | {'cs', 'sv'}, wording_tags(name))
            self.assertEqual(['cs', 'sv'], wording_fixture(name)['additional_reviewed_tags'])
        self.assertEqual({'hu'}, wording_tags(FAMILIES[3]))
        self.assertEqual({'default'} | SCOPED_TAGS | extra_tags, wording_tags(FAMILIES[2]))
        amharic = fixture('amharic_priority.json')
        for key, values in svg['values'].items():
            self.assertEqual(amharic['values'][key]['expected'], values['am'])
        swedish = fixture('swedish_remaining_p1_wording.json')
        for key, values in svg['values'].items():
            self.assertEqual(swedish['values'][key]['sv'], values['sv'])
            for tag in ('bg', 'bn'):
                self.assertEqual(fixture('bulgarian_bengali_priority_wording.json')['values'][key][tag], values[tag])

    def test_tagged_colour_family_resolves_complete_extra_values_and_exact_english_fallbacks(self):
        data = json.loads((ROOT / 'Paintroid/src/test/resources/tagged-colour/expected.json').read_text())
        strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
        offered = set(catalogues.offered_tags())
        english = strings['default'][TAGGED_COLOUR_KEY]
        self.assertEqual(72, len(data))
        self.assertEqual(99, len(offered - set(data)))  # Missing direct values, not all English at runtime.
        self.assertEqual({'ca-ES-valencia': 'ca'}, TAGGED_COLOUR_INHERITED_CATALOGUES)
        self.assertEqual(98, len(offered - set(data) - set(TAGGED_COLOUR_INHERITED_CATALOGUES)))
        self.assertTrue(TAGGED_COLOUR_EXTRA_TAGS.isdisjoint(SCOPED_TAGS))
        require_tagged_colour_resolution(data, strings, offered, english)
        for tag in TAGGED_COLOUR_EXTRA_TAGS:
            self.assertNotEqual(english, data[tag])

    def test_tagged_colour_oracle_rejects_missing_localization_and_arbitrary_defaults(self):
        data = json.loads((ROOT / 'Paintroid/src/test/resources/tagged-colour/expected.json').read_text())
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
        fallback = sorted(offered - set(data) - set(TAGGED_COLOUR_INHERITED_CATALOGUES))[0]
        changed_strings = dict(strings)
        changed_strings[fallback] = dict(strings[fallback])
        changed_strings[fallback][TAGGED_COLOUR_KEY] = english
        require_tagged_colour_resolution(data, changed_strings, offered, english)
        changed_strings[fallback][TAGGED_COLOUR_KEY] = 'arbitrary default'
        with self.assertRaises(ValueError):
            require_tagged_colour_resolution(data, changed_strings, offered, english)

    def test_tagged_colour_parent_inheritance_stays_separate_and_rejects_overrides(self):
        data = json.loads((ROOT / 'Paintroid/src/test/resources/tagged-colour/expected.json').read_text())
        strings = {tag: catalogues.read_strings(path) for tag, path in paths().items()}
        offered = set(catalogues.offered_tags())
        english = strings['default'][TAGGED_COLOUR_KEY]
        child, parent = 'ca-ES-valencia', 'ca'
        self.assertNotIn(child, data)
        self.assertNotIn(TAGGED_COLOUR_KEY, strings[child])
        self.assertEqual(data[parent], fixture('catalan_romanian_import_wording.json')['values'][TAGGED_COLOUR_KEY][parent][1:-1])
        require_tagged_colour_resolution(data, strings, offered, english)
        for value in (english, 'arbitrary override', strings[parent][TAGGED_COLOUR_KEY]):
            changed = dict(strings)
            changed[child] = dict(strings[child], **{TAGGED_COLOUR_KEY: value})
            with self.subTest(override=value), self.assertRaises(ValueError):
                require_tagged_colour_resolution(data, changed, offered, english)
        for missing in (child, parent):
            with self.subTest(unoffered=missing), self.assertRaises(ValueError):
                require_tagged_colour_resolution(data, strings, offered - {missing}, english)
        changed_data = dict(data, **{child: data[parent]})
        with self.assertRaises(ValueError):
            require_tagged_colour_resolution(changed_data, strings, offered, english)

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
