"""Shared exact-successor guard tests, not fresh linguistic or runtime approval."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from current_localization_contracts import require_string
from memory_warning_source_review import current_source_expectation, review_record
from memory_warning_successors import (RECORD, ROOT, KEYS, accepted_warning,
                                      successors, validated_successors)
import translation_catalogues as catalogues
import memory_warning_successors as binding_module


class MemoryWarningSuccessors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RECORD.read_text())
        cls.index = successors()

    def test_exact_inventory_and_every_complete_current_value(self):
        self.assertEqual(114, len(self.index))
        self.assertEqual(57, len({tag for tag, key in self.index}))
        for (tag, key), (old, expected, source, path) in self.index.items():
            with self.subTest(tag=tag, key=key):
                self.assertNotEqual(old, expected)
                xml = (ROOT / path).read_text()
                constraints = {'attributes': {'name': key}, 'formatted': True,
                               'placeholders': {}, 'escaped_newline_count': 0}
                self.assertEqual(expected, current_source_expectation(key, tag, old))
                self.assertEqual(expected, accepted_warning(key, tag))
                require_string(xml, key, expected, constraints)
                self.assertEqual(source, catalogues.read_strings(catalogues.RES / 'values/strings.xml')[key])

    def test_every_successor_rejects_wrong_historical_target(self):
        for (tag, key), (old, expected, source, path) in self.index.items():
            for wrong in (old + ' changed', expected, source, ''):
                if wrong == old: continue
                with self.subTest(tag=tag, key=key, wrong=wrong), self.assertRaises(ValueError):
                    current_source_expectation(key, tag, wrong)

    def test_all_current_values_have_positive_and_corruption_controls(self):
        for (tag, key), (old, expected, source, path) in self.index.items():
            node = ET.fromstring((ROOT / path).read_text()).find(f"./string[@name='{key}']")
            constraints = {'attributes': {'name': key}, 'formatted': True,
                           'placeholders': {}, 'escaped_newline_count': 0}
            # Both the positive and every negative use the exact same independent oracle.
            require_string('<resources>' + ET.tostring(node, encoding='unicode') + '</resources>', key, expected, constraints)
            for mutation in ('old', 'missing', 'duplicate', 'truncate', 'changed', 'markup', 'placeholder', 'attribute'):
                root = ET.Element('resources'); changed = deepcopy(node)
                if mutation != 'missing': root.append(changed)
                if mutation == 'old': changed.text = old
                elif mutation == 'duplicate': root.append(deepcopy(changed))
                elif mutation == 'truncate': changed.text = expected[:-1]
                elif mutation == 'changed': changed.text = expected + ' changed'
                elif mutation == 'markup': ET.SubElement(changed, 'b').text, changed.text = expected, None
                elif mutation == 'placeholder': changed.text += ' %1$s'
                elif mutation == 'attribute': changed.set('translatable', 'false')
                with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, expected, constraints)

    def test_successor_metadata_corruption_is_rejected(self):
        # Self-consistent fake value/hash must still fail against independent receipt/index.
        for field in ('source', 'source_sha256', 'historical_value', 'historical_sha256',
                      'value', 'value_sha256', 'catalogue', 'tag', 'key'):
            data = deepcopy(self.data); data['rows'][0][field] += ' corrupted'
            with self.subTest(field=field), self.assertRaises(ValueError): validated_successors(data)
        data = deepcopy(self.data); row = data['rows'][0]; row['value'] += ' forged'
        row['value_sha256'] = sha256(row['value'].encode()).hexdigest()
        with self.assertRaises(ValueError): validated_successors(data)
        data = deepcopy(self.data); row = data['rows'][0]; row['source'] += ' forged'
        row['source_sha256'] = sha256(row['source'].encode()).hexdigest()
        with self.assertRaises(ValueError): validated_successors(data)

    def test_receipt_identity_and_selector_cannot_be_substituted(self):
        for field in ('path', 'sha256', 'selector'):
            data = deepcopy(self.data); data['rows'][0]['receipt'][field] += ' changed'
            with self.subTest(field=field), self.assertRaises(ValueError): validated_successors(data)

    def test_missing_duplicate_extra_and_held_candidates_are_rejected(self):
        for mutation in ('missing', 'duplicate', 'extra', 'held', 'unknown'):
            data = deepcopy(self.data)
            if mutation == 'missing': data['rows'].pop()
            elif mutation == 'duplicate': data['rows'][1] = deepcopy(data['rows'][0])
            elif mutation == 'extra': data['rows'].append(deepcopy(data['rows'][0]))
            elif mutation == 'held': data['rows'][0]['tag'] = 'ain-Kana'
            else: data['rows'][0]['tag'] = 'unknown'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): validated_successors(data)

    def test_held_missing_and_canonical_values_are_preserved_not_accepted(self):
        counts = {'held': 0, 'missing': 0, 'canonical': 0}
        for option in review_record()['options']:
            tag = option['tag']; actual = catalogues.read_strings(ROOT / option['catalogue'])
            for key, term in option['terms'].items():
                if (tag, key) in self.index: continue
                with self.subTest(tag=tag, key=key):
                    self.assertEqual(term['value'], actual.get(key))
                    with self.assertRaises(ValueError): accepted_warning(key, tag)
                if tag == 'en-001': counts['canonical'] += 1
                elif term['value'] is None: counts['missing'] += 1
                else: counts['held'] += 1
        self.assertEqual({'held': 8, 'missing': 218, 'canonical': 2}, counts)

    def test_checked_in_export_index_and_queue_corruption_is_rejected(self):
        original_read = Path.read_bytes
        for target in ('receipt-exports.json', 'accepted-value-receipts.tsv', 'memory-warnings-20261021.json'):
            def corrupt(path, target=target):
                raw = original_read(path)
                return raw + b' changed' if path.name == target else raw
            with self.subTest(target=target), patch.object(Path, 'read_bytes', corrupt):
                with self.assertRaises(ValueError): validated_successors(self.data)

    def test_export_decision_original_identity_and_index_remain_bound(self):
        path = binding_module.EVIDENCE / 'receipt-exports.json'
        original = json.loads(path.read_text())
        original_read = Path.read_bytes
        for mutation in ('decision', 'original-sha', 'index-sha', 'value', 'source', 'historical', 'duplicate', 'missing'):
            export = deepcopy(original); row = export['rows'][0]
            if mutation == 'decision': row['decision'] = 'revise'
            elif mutation == 'original-sha': row['original_receipt']['sha256'] = '0' * 64
            elif mutation == 'index-sha': export['original_index_sha256'] = '0' * 64
            elif mutation == 'value':
                row['value'] += ' arbitrary'; row['value_sha256'] = sha256(row['value'].encode()).hexdigest()
            elif mutation == 'source': row['source'] += ' changed'
            elif mutation == 'historical': row['historical_value'] += ' changed'
            elif mutation == 'duplicate': export['rows'][1] = deepcopy(row)
            else: export['rows'].pop()
            raw = json.dumps(export).encode()
            def changed_read(target):
                return raw if target == path else original_read(target)
            # Even a newly sealed export cannot waive the decision/original-index bindings.
            with self.subTest(mutation=mutation), patch.object(Path, 'read_bytes', changed_read), patch.object(binding_module, 'EXPORT_HASH', sha256(raw).hexdigest()):
                with self.assertRaises(ValueError): validated_successors(self.data)

    def test_held_historical_target_drift_is_rejected_without_acceptance(self):
        for option in review_record()['options']:
            if option['tag'] not in ('ain-Kana', 'ain-Latn', 'jje', 'vi-Hani'): continue
            for key, term in option['terms'].items():
                self.assertEqual(term['value'], current_source_expectation(key, option['tag'], term['value']))
                with self.assertRaises(ValueError):
                    current_source_expectation(key, option['tag'], term['value'] + ' changed')

    def test_unmapped_keys_cannot_obtain_acceptance(self):
        for tag, key in [('unknown', next(iter(KEYS))), ('af', 'unrelated'), ('ain-Kana', next(iter(KEYS)))]:
            with self.subTest(tag=tag, key=key), self.assertRaises(ValueError): accepted_warning(key, tag)
        self.assertEqual('unrelated', current_source_expectation('other_key', 'af', 'unrelated'))
        with self.assertRaises(ValueError): current_source_expectation(next(iter(KEYS)), 'unknown', 'arbitrary actual')

    def test_canonical_old_source_drift_rejected(self):
        for key in KEYS:
            with self.assertRaises(ValueError): current_source_expectation(key, 'default', 'unknown source')


if __name__ == '__main__':
    unittest.main()
