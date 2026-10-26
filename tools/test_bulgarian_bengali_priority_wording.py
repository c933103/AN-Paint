"""Bounded BG/BN priority contracts, not native-reader or Android UI certification."""
from copy import deepcopy
import json
import re
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import fixture, require_string
import translation_catalogues as catalogues

TAGS = {'bg', 'bn'}
FIXTURE = 'bulgarian_bengali_priority_wording.json'


class BulgarianBengaliPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = fixture(FIXTURE)
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('bg', 'values-bg'), ('bn', 'values-bn')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}
        cls.tiers = json.loads((catalogues.DATA / 'string-importance.json').read_text())['tiers']
        cls.keys = {identity.split('/', 1)[1] for tier in cls.tiers if tier['id'] in ('P0', 'P1')
                    for identity in tier['keys'] if identity.startswith('string/')}

    def test_all_current_priority_scalars_present_with_source_attributes_and_format(self):
        self.assertEqual({'P0': 92, 'P1': 249},
                         {t['id']: len(t['keys']) for t in self.tiers if t['id'] in ('P0', 'P1')})
        for tag in TAGS:
            for key in self.keys:
                with self.subTest(tag=tag, key=key):
                    nodes = self.roots[tag].findall(f"./string[@name='{key}']")
                    self.assertEqual(1, len(nodes))
                    node = nodes[0]
                    source = self.roots['default'].find(f"./string[@name='{key}']")
                    self.assertEqual(0, len(node))
                    self.assertEqual(source.attrib, node.attrib)
                    self.assertEqual(catalogues.placeholders(source.text), catalogues.placeholders(node.text))
                    self.assertEqual(re.findall(r'\\+n', source.text), re.findall(r'\\+n', node.text))
                    self.assertEqual(source.text.count('\n'), node.text.count('\n'))
                    self.assertEqual([], catalogues.android_string_errors(node.text))
                    self.assertEqual([], catalogues.format_string_errors(node.text, node.get('formatted') != 'false'))

    def test_complete_bounded_values_keep_exact_wording_and_attributes(self):
        self.assertEqual(1, self.data['schema_version'])
        self.assertEqual(set(self.data['values']), set(self.data['constraints']))
        self.assertEqual(44, len(self.data['values']))
        self.assertLessEqual(set(self.data['values']), self.keys)
        for key, values in self.data['values'].items():
            self.assertEqual(TAGS | {'default'}, set(values))
            self.assertEqual(set(values), set(self.data['constraints'][key]))
            for tag, expected in values.items():
                with self.subTest(tag=tag, key=key):
                    require_string(self.xml[tag], key, expected, self.data['constraints'][key][tag])

    def test_bounded_guards_reject_missing_duplicate_truncated_markup_and_attribute_changes(self):
        for tag in TAGS:
            for key, values in self.data['values'].items():
                for mutation in ('missing', 'duplicate', 'truncate', 'markup', 'attribute', 'wrong-type'):
                    root = deepcopy(self.roots[tag])
                    node = root.find(f"./string[@name='{key}']")
                    if mutation == 'missing': root.remove(node)
                    elif mutation == 'duplicate': root.append(deepcopy(node))
                    elif mutation == 'truncate': node.text = node.text[:-1]
                    elif mutation == 'markup': ET.SubElement(node, 'b').text, node.text = node.text, None
                    elif mutation == 'attribute': node.set('translatable', 'false')
                    else: node.tag = 'plurals'
                    with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                        require_string(ET.tostring(root, encoding='unicode'), key, values[tag],
                                       self.data['constraints'][key][tag])

    def test_actions_stay_distinct_at_the_real_replacement_and_viewport_consumers(self):
        for tag in TAGS:
            values = {n.get('name'): (n.text or '').strip('"') for n in self.roots[tag] if n.tag == 'string'}
            self.assertEqual(3, len({values[key] for key in ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')}))
            self.assertNotEqual(values['ui_keep_editing23'], values['ui_cancel'])
            self.assertNotEqual(values['ui_fit'], values['ui_resize_image'])
        activity = (catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        self.assertIn('.setNegativeButton(ui(R.string.ui_keep_editing23), null)', activity)
        self.assertIn('button(ui(R.string.ui_fit),"zoom_fit_view") {paintCanvas.fit()}', activity)
        self.assertIn('listOf(ui(R.string.ui_outline), ui(R.string.ui_solid_fill), ui(R.string.ui_fill_line))', activity)

    def test_affected_catalogues_are_structurally_valid_not_claimed_complete(self):
        for tag in TAGS:
            with self.subTest(tag=tag):
                self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=False))
                names = [(node.tag, node.get('name')) for node in self.roots[tag]]
                self.assertEqual(len(names), len(set(names)))


if __name__ == '__main__':
    unittest.main()
