"""Shared checks for the sixteen complete Assembly Help locale contracts.

Locale modules pass current paths and validators at each call; accepted text and
language-specific corruption scenarios remain in their existing modules.
"""
from copy import deepcopy
import json
import xml.etree.ElementTree as ET


def set_up_class(cls, fixture_path, resource_path, require_fixture):
    cls.fixture = json.loads(fixture_path.read_text(encoding='utf-8'))
    cls.expected = require_fixture(cls.fixture)
    cls.root = ET.parse(resource_path).getroot()
    cls.paragraphs = cls.expected.split('\\n\\n')


def reject_value(self, value, key, require_complete):
    self.assertNotEqual(self.expected, value, 'Corruption must not be a no-op')
    broken = deepcopy(self.root)
    broken.find(f"./string[@name='{key}']").text = value
    with self.assertRaises(ValueError):
        require_complete(broken, self.expected)


def check_complete_eight_paragraph_value(self, root_dir, key, require_complete):
    require_complete(self.root, self.expected)
    self.assertEqual(8, len(self.paragraphs))
    self.assertEqual(14, self.expected.count('\\n'))
    self.assertNotRegex(self.expected, '%\\d+\\$')
    english = ET.parse(root_dir / 'Paintroid/src/main/res/values/strings.xml').find(f"./string[@name='{key}']").text
    self.assertEqual(8, len(english.split('\\n\\n')))
    self.assertEqual(14, english.count('\\n'))


def check_paragraph_corruptions(self):
    for index in range(8):
        for kind in ('omit', 'duplicate'):
            changed = list(self.paragraphs)
            if kind == 'omit':
                del changed[index]
            else:
                changed.insert(index, changed[index])
            with self.subTest(paragraph=index, mutation=kind):
                self.reject_value('\\n\\n'.join(changed))
    for index in range(7):
        changed = list(self.paragraphs)
        changed[index], changed[index + 1] = (changed[index + 1], changed[index])
        with self.subTest(paragraph=index, mutation='adjacent-swap'):
            self.reject_value('\\n\\n'.join(changed))


def check_resource_structure(self, key, require_complete):
    for mutation in ('missing', 'duplicate', 'wrong-key', 'attribute', 'markup', 'empty', 'truncated'):
        broken = deepcopy(self.root)
        node = broken.find(f"./string[@name='{key}']")
        if mutation == 'missing':
            broken.remove(node)
        elif mutation == 'duplicate':
            broken.append(deepcopy(node))
        elif mutation == 'wrong-key':
            node.set('name', key + '_wrong')
        elif mutation == 'attribute':
            node.set('formatted', 'false')
        elif mutation == 'markup':
            ET.SubElement(node, 'b').text = 'Unexpected'
        elif mutation == 'empty':
            node.text = None
        elif mutation == 'truncated':
            node.text = node.text[:-1]
        with self.subTest(mutation=mutation), self.assertRaises(ValueError):
            require_complete(broken, self.expected)
