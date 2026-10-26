"""Three qualified crop whole-value guards; no runtime or native-language proof."""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture
import translation_catalogues as catalogues

KEY = 'ui_crop_preview_images'
FOLDERS = {'values-b+hak+Hant+TW', 'values-b+hak+Latn+TW', 'values-b+wuu+Hans'}


def require_crop(root, expected):
    nodes = root.findall(f"./plurals[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY}:
        raise ValueError('Missing, duplicate or changed plural resource')
    items = list(nodes[0])
    if len(items) != 1 or items[0].tag != 'item' or items[0].attrib != {'quantity': 'other'} or len(items[0]):
        raise ValueError('Exactly one unmarked other-form is required')
    if items[0].text != expected:
        raise ValueError('Complete crop warning changed')
    if catalogues.android_string_errors(expected) or catalogues.format_string_errors(expected):
        raise ValueError('Invalid Android formatting')


class HakkaWuCropTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture('hakka_wu_crop_wording.json')
        cls.roots = {folder: ET.parse(catalogues.RES / folder / 'strings.xml').getroot() for folder in FOLDERS}

    def test_exact_qualified_scope_and_complete_values(self):
        self.assertEqual(1, self.data['schema_version'])
        self.assertEqual(KEY, self.data['key'])
        self.assertEqual(FOLDERS, set(self.data['locales']))
        for folder, entry in self.data['locales'].items():
            with self.subTest(folder=folder):
                self.assertEqual('qualified', entry['disposition'])
                self.assertEqual(['other'], entry['quantities'])
                require_crop(self.roots[folder], entry['value'])
                self.assertTrue(entry['value'].startswith(entry['retained_prefix']))
                self.assertTrue(entry['original'].startswith(entry['retained_prefix']))

    def test_reference_dimensions_selection_count_and_newline_preserved(self):
        source = ET.parse(catalogues.RES / 'values/strings.xml').find(f"plurals[@name='{KEY}']/item[@quantity='other']").text
        for folder, entry in self.data['locales'].items():
            value = entry['value']
            with self.subTest(folder=folder):
                self.assertEqual(catalogues.placeholders(source), catalogues.placeholders(value))
                self.assertEqual(['%1$d', '%2$d', '%3$d'], catalogues.FORMAT_TOKEN.findall(value))
                self.assertEqual(1, value.count(r'\n'))
                self.assertNotIn('\n', value)
                self.assertEqual(1, value.count(' × '))
                self.assertEqual(1, value.count('px'))

    def test_complete_guard_rejects_old_wording_corruption_and_unreviewed_forms(self):
        for folder, entry in self.data['locales'].items():
            for mutation in ('old', 'truncate', 'placeholder', 'newline', 'markup', 'attribute', 'missing', 'duplicate', 'extra-form'):
                root = deepcopy(self.roots[folder]);plural = root.find(f"plurals[@name='{KEY}']");item = plural[0]
                if mutation == 'old': item.text = entry['original']
                elif mutation == 'truncate': item.text = item.text[:-1]
                elif mutation == 'placeholder': item.text = item.text.replace('%3$d', '%3$s')
                elif mutation == 'newline': item.text = item.text.replace(r'\n', '\n')
                elif mutation == 'markup': ET.SubElement(item, 'b').text, item.text = item.text, None
                elif mutation == 'attribute': plural.set('formatted', 'false')
                elif mutation == 'missing': plural.remove(item)
                elif mutation == 'duplicate': root.append(deepcopy(plural))
                else: ET.SubElement(plural, 'item', quantity='one').text = item.text
                with self.subTest(folder=folder, mutation=mutation), self.assertRaises(ValueError):
                    require_crop(root, entry['value'])

    def test_actual_consumer_passes_reference_crop_dimensions_and_selected_image_count(self):
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        dialog = (classic / 'ImageCropDialog.kt').read_text()
        self.assertIn('val count = images.count { it.id in selected }', dialog)
        self.assertIn('uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,crop.width(),crop.height(),count)', dialog)
        model = (classic / 'ImageAssembly.kt').read_text()
        self.assertIn('val parent = resolve(byId[a.anchor]', model)
        self.assertIn('x = if (a.edge == SnapEdge.RIGHT) parent.right else parent.left', model)
        self.assertIn('y = if (a.edge == SnapEdge.BOTTOM) parent.bottom else parent.top', model)


if __name__ == '__main__':
    unittest.main()
