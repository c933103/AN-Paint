"""Independent current legal, protocol, formatting and Unicode constraints.

No copied locale values or historical approval/fallback partition is an oracle.
"""
import unittest
import unicodedata
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from current_localization_contracts import fixture, require_string, current_display

FAMILIES = ('commons_metadata_current_wording.json', 'commons_copy_credit_current_wording.json',
            'commons_svg_current_wording.json', 'commons_import_failures_current_wording.json',
            'hungarian_attribution_current_wording.json')

class CurrentLocalizationContracts(unittest.TestCase):
    def test_current_resources_keep_protocol_legal_and_format_requirements(self):
        paths = {'default': catalogues.RES / 'values/strings.xml', **catalogues.catalogue_paths()}
        for name in FAMILIES:
            data = fixture(name)
            selected = {'hu': paths['hu']} if name.startswith('hungarian') else paths
            for tag, path in selected.items():
                root = ET.parse(path).getroot()
                for key, constraint in data['constraints'].items():
                    nodes = root.findall(f"./string[@name='{key}']")
                    if not nodes:
                        continue  # Real runtime fallback checks do not forbid new translations.
                    with self.subTest(family=name, tag=tag, key=key):
                        self.assertEqual(1, len(nodes))
                        node = nodes[0]; value = ''.join(node.itertext())
                        self.assertEqual(constraint.get('child_elements', 0), len(node))
                        if 'attributes' in constraint:
                            self.assertEqual(constraint['attributes'], node.attrib)
                        if 'formatted' in constraint:
                            self.assertEqual(constraint['formatted'], node.get('formatted') != 'false')
                        self.assertEqual(constraint['placeholders'], catalogues.placeholders(value))
                        self.assertEqual([], catalogues.android_string_errors(value))
                        self.assertEqual([], catalogues.format_string_errors(value, node.get('formatted') != 'false'))
                        for literal in constraint.get('required_literals', ()):
                            self.assertIn(literal, value)
                        for literal, count in constraint.get('legal_identifier_counts', {}).items():
                            self.assertEqual(count, value.count(literal))
                        for forbidden in constraint.get('forbidden_casefold_substrings', ()):
                            self.assertNotIn(forbidden, value.casefold())

    def test_script_controls_variation_selectors_and_normalization(self):
        paths = catalogues.catalogue_paths()
        for name in FAMILIES:
            data = fixture(name)
            for key, tags in data.get('special_codepoint_counts', {}).items():
                for tag, codepoints in tags.items():
                    value = catalogues.read_strings(paths[tag])[key]
                    for codepoint, count in codepoints.items():
                        with self.subTest(tag=tag, key=key, codepoint=codepoint):
                            self.assertEqual(count, value.count(chr(int(codepoint[2:], 16))))
            for key, tags in data.get('nfc_and_no_category_C_required', {}).items():
                for tag in tags:
                    value = catalogues.read_strings(paths[tag])[key]
                    self.assertEqual(value, unicodedata.normalize('NFC', value))
                    self.assertFalse(any(unicodedata.category(c).startswith('C') for c in value))

    def test_hungarian_attribution_references_live_labels(self):
        references = fixture('hungarian_attribution_current_wording.json')['label_references']
        for key, labels in references.items():
            value = current_display('hu', key)
            for label in labels:
                with self.subTest(key=key, label=label):
                    self.assertIn(current_display('hu', label), value)

    def test_full_string_validator_rejects_real_structure_and_argument_damage(self):
        for xml in ('<resources/>', '<resources><string name="target">Commons %1$s</string><string name="target">Commons %1$s</string></resources>',
                    '<resources><string name="target"><b>Commons %1$s</b></string></resources>',
                    '<resources><string name="target">Commons %2$d</string></resources>'):
            with self.subTest(xml=xml), self.assertRaises(ValueError):
                require_string(xml, 'target', 'Commons %1$s', {'placeholders': {'%1$s': 1}})

if __name__ == '__main__':
    unittest.main()
