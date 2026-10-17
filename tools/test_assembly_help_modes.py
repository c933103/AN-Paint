"""Complete English assembly Help regressions; no whole-language acceptance."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
KEY = 'ui_add_up_to_20_images_with_android_s'
PATHS = {'en': 'values', 'en-001': 'values-b+en+001',
         **{f'en-{region}': f'values-en-r{region}' for region in ('AU', 'CA', 'GB', 'IN', 'SG', 'US')},
         'en-XV': 'values-b+en+XV', 'qaa-Zsye-XV': 'values-b+qaa+Zsye+XV'}
POSITION = ('Select an image and use Exact position to set its top-left X/Y coordinates in whole pixels, '
            'starting at zero. Other images keep their positions, and overlaps are allowed.')
GAP = 'Other images stay placed; attached images may move to fill the gap.'


def decoded(value):
    return value.replace(r"\'", "'").replace(r'\"', '"').replace(r'\n', '\n')


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {'name': KEY} or len(nodes[0]):
        raise ValueError('Help key, attributes or markup changed')
    if decoded(nodes[0].text or '') != expected:
        raise ValueError('Complete Help differs')


class AssemblyHelpModesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((ROOT / 'Paintroid/src/test/resources/assembly-help-modes/expected.json')
                                  .read_text(encoding='utf-8'))['locales']
        cls.roots = {tag: ET.parse(RES / directory / 'strings.xml').getroot()
                     for tag, directory in PATHS.items()}

    def test_exact_english_inventory_and_all_complete_values(self):
        # Include the plain-English vertical test and the separately routed emoji
        # catalogue; neither is one of the six regional English catalogues.
        found = {p.parent.name for p in RES.glob('values*/strings.xml')
                 if (node := ET.parse(p).find(f"./string[@name='{KEY}']")) is not None
                 and 'Add up to 20 images' in (node.text or '')}
        self.assertEqual(set(PATHS.values()), found)
        self.assertEqual(set(PATHS), set(self.expected))
        for tag, root in self.roots.items():
            with self.subTest(tag=tag):
                self.assertEqual(PATHS[tag], self.expected[tag]['directory'])
                require_complete(root, self.expected[tag]['help'])

    def test_separate_snap_and_exact_position_paragraphs_and_qualified_removal(self):
        for tag, expected in self.expected.items():
            with self.subTest(tag=tag):
                paragraphs = expected['help'].split('\n\n')
                self.assertEqual(8, len(paragraphs))
                self.assertIn('highlighted edge', paragraphs[2])
                self.assertIn('When snapping, the first image starts at the origin.', paragraphs[2])
                self.assertTrue(paragraphs[2].endswith('Overlaps are rejected when snapping.'))
                position = POSITION.replace('Exact position', '«📍 Exact position»') if tag == 'qaa-Zsye-XV' else POSITION
                self.assertEqual(position, paragraphs[3])
                self.assertIn('returns only the selected image to the tray. ' + GAP, paragraphs[5])
                self.assertNotIn('Following images fill its gap', expected['help'])
                self.assertIn('Attached images may move when their parent is cropped.', paragraphs[2])

    def test_actual_control_names_dimensions_and_conditional_memory_guidance(self):
        for tag, root in self.roots.items():
            values = {node.get('name'): decoded(node.text or '') for node in root if node.tag == 'string'}
            help_text = self.expected[tag]['help']
            with self.subTest(tag=tag):
                self.assertEqual(values['ui_assembly_exact_position'], self.expected[tag]['positionLabel'])
                for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                            'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest',
                            'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                            'ui_save_png', 'ui_edit_in_paint'):
                    self.assertIn(values[key], help_text, key)
                self.assertIn('image dimensions after cropping and any ' +
                              ('«↔️ Same width» or «↕️ Same height»' if tag == 'qaa-Zsye-XV'
                               else 'Same width or Same height') + ' adjustment', help_text)
                self.assertIn('choose a smaller output copy if offered.', help_text)
                self.assertIn('If even a tiny output exceeds the budget, the app shows a memory warning instead of a size chooser.', help_text)

    def test_oracle_rejects_old_mode_claims_omissions_truncation_and_resource_corruption(self):
        for tag, root in self.roots.items():
            expected = self.expected[tag]['help']
            position = expected.split('\n\n')[3]
            for mutation in ('missing-position', 'guaranteed-gap', 'unscoped-origin', 'unscoped-overlap', 'wrong-label', 'wrong-origin',
                             'reject-overlap', 'moves-others', 'truncated', 'duplicate', 'missing', 'attribute'):
                broken = deepcopy(root)
                node = broken.find(f"./string[@name='{KEY}']")
                if mutation == 'missing-position': node.text = node.text.replace(position + r'\n\n', '')
                elif mutation == 'guaranteed-gap': node.text = node.text.replace(GAP, 'Following images fill its gap; they stay placed.')
                elif mutation == 'unscoped-origin': node.text = node.text.replace('When snapping, the first image', 'The first image')
                elif mutation == 'unscoped-overlap': node.text = node.text.replace('Overlaps are rejected when snapping.', 'Overlaps are rejected.')
                elif mutation == 'wrong-label': node.text = node.text.replace('Exact position', 'Exact placement')
                elif mutation == 'wrong-origin': node.text = node.text.replace('starting at zero', 'starting at one')
                elif mutation == 'reject-overlap': node.text = node.text.replace('overlaps are allowed', 'overlaps are rejected')
                elif mutation == 'moves-others': node.text = node.text.replace('Other images keep their positions', 'Other images move with it')
                elif mutation == 'truncated': node.text = node.text[:-1]
                elif mutation == 'duplicate': broken.append(deepcopy(node))
                elif mutation == 'missing': broken.remove(node)
                elif mutation == 'attribute': node.set('formatted', 'false')
                with self.subTest(tag=tag, mutation=mutation), self.assertRaises(ValueError):
                    require_complete(broken, expected)

    def test_help_remains_p3(self):
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text())['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + KEY])


if __name__ == '__main__':
    unittest.main()
