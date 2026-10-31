"""Two bounded warning corrections; full-message language acceptance remains open."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import require_string
import translation_catalogues as catalogues


KEY = 'ui_sampled_resize_memory_explanation'
TAGS = {'default', 'bo', 'jje'}
EXPECTED = catalogues.ROOT / 'Paintroid/src/test/resources/memory-modality/expected.json'


class SampledMemoryModalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(EXPECTED.read_text(encoding='utf-8'))
        cls.xml = {tag: (catalogues.RES / directory / 'strings.xml').read_text(encoding='utf-8')
                   for tag, directory in cls.fixture['catalogues'].items()}

    def test_exact_scope_and_complete_scalar_values_attributes_and_placeholders(self):
        data = self.fixture
        self.assertEqual(1, data['schema_version'])
        self.assertEqual(KEY, data['key'])
        for field in ('values', 'constraints', 'catalogues'):
            self.assertEqual(TAGS, set(data[field]))
        self.assertEqual({'bo': False, 'jje': False}, data['whole_value_accepted'])
        for tag in TAGS - {'bo'}:
            with self.subTest(tag=tag):
                self.assertEqual({'attributes': {'name': KEY}, 'formatted': True,
                                  'placeholders': {}}, data['constraints'][tag])
                require_string(self.xml[tag], KEY, data['values'][tag], data['constraints'][tag])
                self.assertEqual({}, catalogues.placeholders(data['values'][tag]))
                # No plural/array replacement or shadow definition may impersonate this scalar.
                matching = [node for node in ET.fromstring(self.xml[tag]) if node.get('name') == KEY]
                self.assertEqual(['string'], [node.tag for node in matching])

    def test_complete_value_rejects_resource_corruption(self):
        for tag in TAGS - {'bo'}:
            for mutation in ('truncate', 'missing', 'duplicate', 'markup', 'attribute',
                             'formatted', 'placeholder', 'plural', 'apostrophe'):
                root = ET.fromstring(self.xml[tag])
                node = root.find(f"string[@name='{KEY}']")
                if mutation == 'truncate': node.text = node.text[:-1]
                elif mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'markup':
                    ET.SubElement(node, 'b').text, node.text = node.text, None
                elif mutation == 'attribute': node.set('translatable', 'false')
                elif mutation == 'formatted': node.set('formatted', 'false')
                elif mutation == 'placeholder': node.text += ' %1$d'
                elif mutation == 'plural':
                    node.tag = 'plurals'
                    ET.SubElement(node, 'item', {'quantity': 'other'}).text, node.text = node.text, None
                else: node.text += " '"
                with self.subTest(tag=tag, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), KEY,
                                   self.fixture['values'][tag], self.fixture['constraints'][tag])

    def test_definite_detail_loss_preserves_variable_actual_usage_and_original(self):
        for tag, detail, variable, original, previous in (
            ('bo', 'འདྲ་བཤུས་ཆུང་བས་ཞིབ་ཆ་ཉམས།',
             'དངོས་སྤྱོད་དྲན་ཤེས་མི་འདྲ་བ་སྲིད།', 'མ་ཡིག་མི་བསྒྱུར།',
             'འདྲ་བཤུས་ཆུང་བས་ཞིབ་ཆ་ཉམས་སྲིད།'),
            ('jje', '작은 사본을 만들민 세밀헌 부분은 줄어들어 이수다.',
             '실제 쓰는 양은 다를 수 이수다.', '원본 파일은 그대로우다.',
             '작은 사본을 만들민 세밀헌 부분은 줄어들 수 이수다.'),
        ):
            value = ET.fromstring(self.xml[tag]).find("string[@name='"+KEY+"']").text
            if tag == 'bo':
                variable = 'དངོས་སུ་སྤྱོད་པའི་ནང་གསོག་གི་ཚད་མི་འདྲ་བ་ཡིན།'
            for clause in (detail, variable, original):
                self.assertEqual(1, value.count(clause), (tag, clause))
            self.assertNotIn(previous, value)
            if tag == 'bo':
                continue  # The semantic clauses above remain; full approved text is not mirrored.
            root = ET.fromstring(self.xml[tag])
            root.find(f"string[@name='{KEY}']").text = value.replace(detail, previous)
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), KEY, self.fixture['values'][tag],
                               self.fixture['constraints'][tag])

    def test_affected_catalogues_remain_well_formed(self):
        for tag in ('bo', 'jje'):
            with self.subTest(tag=tag):
                self.assertEqual([], catalogues.validate_catalogue(tag, require_complete=False))
                nodes = ET.fromstring(self.xml[tag])
                identities = [(node.tag, node.get('name')) for node in nodes]
                self.assertEqual(len(identities), len(set(identities)))


if __name__ == '__main__':
    unittest.main()
