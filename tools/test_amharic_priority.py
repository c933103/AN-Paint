"""Exact reviewed Amharic priority wording; no native-reader/runtime certification."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
from current_localization_contracts import fixture, require_string
import translation_catalogues as catalogues


class AmharicPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture('amharic_priority.json')['values']
        cls.xml = (catalogues.RES / 'values-b+am/strings.xml').read_text()
        cls.english = (catalogues.RES / 'values/strings.xml').read_text()

    def test_complete_reviewed_wording_and_source_binding(self):
        self.assertEqual(255, len(self.data))
        for key, term in self.data.items():
            with self.subTest(key=key):
                constraints = {'attributes': term['attributes'],
                               'placeholders': catalogues.placeholders(term['source']),
                               'escaped_newline_count': term['source'].count('\\n')}
                require_string(self.english, key, term['source'], constraints)
                require_string(self.xml, key, term['expected'], constraints)

    def test_every_reviewed_value_rejects_corruption(self):
        for key, term in self.data.items():
            node = ET.fromstring(self.xml).find(f"./string[@name='{key}']")
            for mutation in ('missing', 'duplicate', 'truncate', 'changed', 'markup', 'placeholder', 'attribute'):
                root = ET.Element('resources'); changed = deepcopy(node)
                if mutation != 'missing': root.append(changed)
                if mutation == 'duplicate': root.append(deepcopy(changed))
                elif mutation == 'truncate': changed.text = term['expected'][:-1]
                elif mutation == 'changed': changed.text += ' changed'
                elif mutation == 'markup': ET.SubElement(changed, 'b').text, changed.text = term['expected'], None
                elif mutation == 'placeholder': changed.text += ' %1$s'
                elif mutation == 'attribute': changed.set('translatable', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, term['expected'], {'attributes': term['attributes']})

    def test_frozen_plural_remains_unchanged(self):
        require_string(self.xml, 'ui_pixels_6ec9c2', '"ፒክሰሎች"', {'attributes': {'name': 'ui_pixels_6ec9c2'}})


if __name__ == '__main__':
    unittest.main()
