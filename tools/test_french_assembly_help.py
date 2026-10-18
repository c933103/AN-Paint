"""Complete French assembly Help contract; not whole-catalogue acceptance."""
from copy import deepcopy
from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / 'Paintroid/src/main/res/values-fr/strings.xml'
FIXTURE = ROOT / 'Paintroid/src/test/resources/french-assembly-help/expected.txt'
HELP = 'ui_add_up_to_20_images_with_android_s'


def decoded(text):
    return text.replace(r"\'", "'").replace(r'\"', '"').replace(r'\n', '\n')


def require_complete(root, expected):
    nodes = root.findall(f"./string[@name='{HELP}']")
    if len(nodes) != 1:
        raise ValueError('Missing or duplicated Help')
    node = nodes[0]
    if node.attrib != {'name': HELP} or len(node):
        raise ValueError('Help attributes or markup changed')
    if decoded(node.text or '') != expected:
        raise ValueError('Complete French Help differs')


class FrenchAssemblyHelpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ET.parse(RESOURCE).getroot()
        cls.expected = FIXTURE.read_text(encoding='utf-8').removesuffix('\n')
        cls.paragraphs = cls.expected.split('\n\n')

    def test_complete_eight_paragraph_entry(self):
        require_complete(self.root, self.expected)
        self.assertEqual(8, len(self.paragraphs))
        self.assertFalse(re.search(r'%\d+\$', self.expected))

    def test_complete_oracle_rejects_every_missing_paragraph_and_structural_change(self):
        for index in range(8):
            broken = deepcopy(self.root)
            broken.find(f"./string[@name='{HELP}']").text = '\n\n'.join(
                p for i, p in enumerate(self.paragraphs) if i != index)
            with self.subTest(paragraph=index), self.assertRaises(ValueError):
                require_complete(broken, self.expected)
        for mutation in ('missing', 'duplicate', 'attribute', 'markup', 'truncated'):
            broken = deepcopy(self.root)
            node = broken.find(f"./string[@name='{HELP}']")
            if mutation == 'missing': broken.remove(node)
            elif mutation == 'duplicate': broken.append(deepcopy(node))
            elif mutation == 'attribute': node.set('formatted', 'false')
            elif mutation == 'markup': ET.SubElement(node, 'b').text = 'Unexpected'
            elif mutation == 'truncated': node.text = node.text[:-1]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_complete(broken, self.expected)

    def test_snapping_and_exact_position_are_distinct(self):
        self.assertIn('Lors de l’alignement sur une cible, la première image commence à l’origine.', self.paragraphs[2])
        self.assertIn('Les chevauchements sont refusés lors de l’alignement sur une cible.', self.paragraphs[2])
        label = decoded(self.root.find("./string[@name='ui_assembly_exact_position']").text)
        self.assertEqual(
            'Sélectionnez une image et utilisez ' + label + ' pour définir les coordonnées X/Y de son '
            'coin supérieur gauche en nombres entiers de pixels, à partir de zéro. '
            'Les autres images conservent leur position et les chevauchements sont autorisés.', self.paragraphs[3])

    def test_conditional_movement_and_complete_undo_redo_statement(self):
        self.assertIn('Les images rattachées peuvent se déplacer lorsque leur image parente est recadrée.', self.paragraphs[2])
        self.assertIn('Les autres images restent placées ; les images rattachées peuvent se déplacer '
                      'pour combler l’espace libéré.', self.paragraphs[5])
        self.assertIn('Annuler et Rétablir permettent d’annuler ou de rétablir ces modifications.', self.paragraphs[5])
        self.assertNotIn('Les images suivantes comblent l’espace', self.expected)
        self.assertNotIn('Annuler/Rétablir restaure', self.expected)

    def test_actual_control_labels_and_help_priority(self):
        for key in ('ui_assembly_exact_position', 'ui_same_width', 'ui_same_height'):
            with self.subTest(key=key):
                label = decoded(self.root.find(f"./string[@name='{key}']").text)
                self.assertIn(label, self.expected)
        tiers = json.loads((ROOT / 'translations/string-importance.json').read_text())['tiers']
        actual = {key: tier['id'] for tier in tiers for key in tier['keys']}
        self.assertEqual('P3', actual['string/' + HELP])


if __name__ == '__main__':
    unittest.main()
