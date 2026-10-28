"""Compact complete-message fixtures; no historical snapshot or source hash guard."""
import copy
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tools/fixtures/finnish_estonian_latvian_crop_companions.json'
TOKENS = re.compile(r'%\d+\$[ds]')


def read_nodes(path):
    root = ET.parse(path).getroot()
    keys = [(node.tag, node.attrib.get('name')) for node in root]
    if len(keys) != len(set(keys)):
        raise ValueError('duplicate resource identity')
    return {(node.tag, node.attrib.get('name')): node for node in root}


def validate(nodes, locale):
    for name, expected in locale['strings'].items():
        node = nodes['string', name]
        if node.attrib != {'name': name} or list(node) or node.text != expected:
            raise ValueError(name)
        if TOKENS.findall(node.text) != ['%1$s']:
            raise ValueError('edge argument')
    for name, expected in locale['plurals'].items():
        node = nodes['plurals', name]
        if node.attrib != {'name': name} or len(node) != len(expected):
            raise ValueError('plural container')
        forms = {}
        for item in node:
            quantity = item.attrib.get('quantity')
            if item.tag != 'item' or item.attrib != {'quantity': quantity} or quantity in forms or list(item):
                raise ValueError('plural quantity')
            forms[quantity] = item.text
        if forms != expected:
            raise ValueError('complete plural text')
        for text in forms.values():
            if TOKENS.findall(text) != ['%1$d', '%2$d', '%3$d'] or text.count(r'\n') != 1:
                raise ValueError('plural formatting')


class FinnishEstonianLatvianCropCompanionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locales = json.loads(FIXTURE.read_text(encoding='utf-8'))['locales']

    def test_complete_values_attributes_quantities_and_format_tokens(self):
        self.assertEqual({'fi', 'et', 'lv'}, set(self.locales))
        for tag, locale in self.locales.items():
            self.assertEqual({'ui_trim_in_pixels', 'ui_trim_in_percent'}, set(locale['strings']), tag)
            self.assertEqual({'left', 'top', 'right', 'bottom'}, set(locale['edge_compositions']), tag)
            for outputs in locale['edge_compositions'].values():
                self.assertEqual({'pixels', 'percent'}, set(outputs), tag)
            self.assertEqual({'ui_crop_preview_images'} if tag in ('fi', 'lv') else set(), set(locale['plurals']), tag)
        for tag, locale in self.locales.items():
            with self.subTest(tag=tag):
                validate(read_nodes(ROOT / locale['path']), locale)

    def test_all_twenty_four_complete_crop_side_compositions(self):
        for tag, locale in self.locales.items():
            nodes = read_nodes(ROOT / locale['path'])
            for edge, expected in locale['edge_compositions'].items():
                label = nodes['string', 'ui_' + edge].text
                for unit in ('pixels', 'percent'):
                    actual = nodes['string', 'ui_trim_in_' + unit].text.replace('%1$s', label)
                    self.assertEqual(expected[unit], actual, (tag, edge, unit))

    def test_plural_mutations_are_rejected(self):
        for tag, locale in self.locales.items():
            if not locale['plurals']:
                continue
            original = read_nodes(ROOT / locale['path'])
            for mutation in ('missing_form', 'duplicate_form', 'dropped_warning', 'unconditional', 'lost_count', 'nested_item'):
                nodes = copy.deepcopy(original)
                plural = nodes['plurals', 'ui_crop_preview_images']
                if mutation == 'missing_form': plural.remove(plural[0])
                elif mutation == 'duplicate_form': plural.append(copy.deepcopy(plural[0]))
                elif mutation == 'dropped_warning': plural[0].text = plural[0].text.split('. ')[0] + '.'
                elif mutation == 'nested_item': ET.SubElement(plural[0], 'b').text = 'unexpected text'
                elif mutation == 'unconditional': plural[0].text = plural[0].text.replace('voi siirtää', 'siirtää').replace('var pārvietot', 'pārvieto')
                else: plural[0].text = plural[0].text.replace('%3$d', '')
                with self.subTest(tag=tag, mutation=mutation), self.assertRaises(ValueError):
                    validate(nodes, locale)

    def test_side_template_requires_argument_separator_and_complete_unit(self):
        for tag, locale in self.locales.items():
            original = read_nodes(ROOT / locale['path'])
            for name in locale['strings']:
                for mutation in ('lost_argument', 'lost_separator', 'lost_unit'):
                    nodes = copy.deepcopy(original)
                    node = nodes['string', name]
                    if mutation == 'lost_argument': node.text = node.text.replace('%1$s', '')
                    elif mutation == 'lost_separator': node.text = node.text.replace(':', '')
                    else: node.text = node.text.rsplit(' ', 1)[0]
                    with self.subTest(tag=tag, name=name, mutation=mutation), self.assertRaises(ValueError):
                        validate(nodes, locale)

if __name__ == '__main__':
    unittest.main()
