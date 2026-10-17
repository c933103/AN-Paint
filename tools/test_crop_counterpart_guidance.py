"""Complete four-locale crop guidance contracts, not whole-language acceptance."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'Paintroid/src/test/resources/crop-counterparts/expected.json'
PATHS = {'de': 'values-de', 'es-ES': 'values-b+es+ES',
         'it': 'values-it', 'pt-PT': 'values-b+pt+PT'}
HELP = 'ui_add_up_to_20_images_with_android_s'
CROP = 'ui_crop_preview_images'


def decoded(text):
    return text.replace(r"\'", "'").replace(r'\"', '"').replace(r'\n', '\n')


def require_complete(root, expected):
    help_nodes = root.findall(f"./string[@name='{HELP}']")
    plural_nodes = root.findall(f"./plurals[@name='{CROP}']")
    if len(help_nodes) != 1 or len(plural_nodes) != 1:
        raise ValueError('Missing or duplicated guidance resource')
    help_node, plural = help_nodes[0], plural_nodes[0]
    if help_node.attrib != {'name': HELP} or len(help_node):
        raise ValueError('Help attributes or markup changed')
    if plural.attrib != {'name': CROP}:
        raise ValueError('Plural attributes changed')
    if decoded(help_node.text or '') != expected['help']:
        raise ValueError('Complete Help differs')
    if len(plural) != 2 or {x.get('quantity') for x in plural} != {'one', 'other'}:
        raise ValueError('Plural categories changed')
    for item in plural:
        quantity = item.get('quantity')
        if item.tag != 'item' or item.attrib != {'quantity': quantity} or len(item):
            raise ValueError('Plural form attributes or markup changed')
        if decoded(item.text or '') != expected['crop'][quantity]:
            raise ValueError('Complete crop quantity differs')


class CropCounterpartGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads(FIXTURE.read_text(encoding='utf-8'))['locales']
        cls.roots = {tag: ET.parse(ROOT / 'Paintroid/src/main/res' / qualifier / 'strings.xml').getroot()
                     for tag, qualifier in PATHS.items()}

    def test_exact_four_locales_all_help_paragraphs_and_every_plural_form(self):
        self.assertEqual(set(PATHS), set(self.expected))
        for tag, expected in self.expected.items():
            with self.subTest(tag=tag):
                self.assertEqual({'help', 'crop'}, set(expected))
                self.assertEqual({'one', 'other'}, set(expected['crop']))
                self.assertEqual(7, len(expected['help'].split('\n\n')))
                self.assertFalse(re.search(r'%\d+\$', expected['help']))
                require_complete(self.roots[tag], expected)
                for quantity, value in expected['crop'].items():
                    self.assertEqual(['%1$d', '%2$d', '%3$d'], re.findall(r'%[1-9]\d*\$d', value))
                    self.assertEqual(1, value.count('\n'))
                    self.assertIn(' × ', value)

    def test_full_value_oracles_reject_truncated_help_and_warning_or_wrong_argument_types(self):
        for tag, root in self.roots.items():
            mutations = ['help-truncated', 'help-duplicated', 'help-missing', 'help-wrong-attribute',
                         'one-truncated', 'other-truncated', 'one-missing', 'other-missing',
                         'one-duplicated', 'other-duplicated', 'one-wrong-type', 'other-wrong-type']
            for mutation in mutations:
                broken = deepcopy(root)
                kind, change = mutation.split('-', 1)
                node = broken.find(f"./string[@name='{HELP}']") if kind == 'help' else \
                    broken.find(f"./plurals[@name='{CROP}']/item[@quantity='{kind}']")
                parent = broken if kind == 'help' else broken.find(f"./plurals[@name='{CROP}']")
                if change == 'truncated': node.text = (node.text or '')[:-1]
                elif change == 'missing': parent.remove(node)
                elif change == 'duplicated': parent.append(deepcopy(node))
                elif change == 'wrong-type': node.text = node.text.replace('%3$d', '%3$s')
                elif change == 'wrong-attribute': node.set('formatted', 'false')
                with self.subTest(tag=tag, mutation=mutation), self.assertRaises(ValueError):
                    require_complete(broken, self.expected[tag])

    def test_movement_is_conditional_and_names_images_in_both_consumers(self):
        phrases = {
            'de': ('Verbundene Bilder können sich verschieben', 'kann die mit ihnen verbundenen Bilder verschieben'),
            'es-ES': ('Las imágenes unidas pueden desplazarse', 'puede desplazar las imágenes unidas a ellas'),
            'it': ('Le immagini collegate possono spostarsi', 'può spostare anche le immagini ad essa collegate'),
            'pt-PT': ('As imagens ligadas podem deslocar-se', 'pode deslocar as imagens que lhes estão ligadas'),
        }
        for tag, (help_phrase, crop_phrase) in phrases.items():
            with self.subTest(tag=tag):
                self.assertIn(help_phrase, self.expected[tag]['help'])
                for value in self.expected[tag]['crop'].values():
                    self.assertIn(crop_phrase, value)

    def test_same_entry_clarifications_retain_exact_current_control_names(self):
        # Names come from the production button resources, not a translated guess.
        controls = {'es-ES': ['ui_crop_image', 'ui_remove'],
                    'it': ['ui_same_width', 'ui_same_height', 'ui_pixels', 'ui_percent'],
                    'pt-PT': ['ui_same_width', 'ui_same_height']}
        for tag, keys in controls.items():
            for key in keys:
                node = self.roots[tag].find(f"./string[@name='{key}']")
                with self.subTest(tag=tag, key=key):
                    self.assertIsNotNone(node)
                    self.assertIn(decoded(node.text), self.expected[tag]['help'])
        self.assertIn('halbtransparente Vorschau', self.expected['de']['help'])
        self.assertIn('ampliar o reducir', self.expected['es-ES']['help'])

    def test_help_and_plural_priority_remain_p3_and_p2(self):
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text())['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + HELP])
        self.assertEqual('P2', actual['plurals/' + CROP])


if __name__ == '__main__':
    unittest.main()
