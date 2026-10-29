"""Shared exact-successor guard tests, not fresh linguistic or runtime approval."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from current_localization_contracts import require_string
from memory_warning_source_review import SERBIAN_DELTA_ADDITIONS, NORDIC_ADDITIONS, NN_BE_SQ_ADDITIONS, HR_BS_MK_ADDITIONS, EXACT_SCRIPT_ADDITIONS, EU_FY_UZ_ADDITIONS, GA_GD_CY_ADDITIONS, YO_ZU_XH_ADDITIONS, HA_IG_LN_ADDITIONS, JV_SU_KY_ADDITIONS, AS_KM_LO_ADDITIONS, NE_PA_ADDITIONS, KN_ML_ADDITIONS, HI_GU_ADDITIONS, THAI_ADDITIONS, MR_TA_TE_ADDITIONS, PRIORITY_TAGS, PRIORITY_ADDITIONS, SK_SL_CA_ADDITIONS, SINGLE_KEY_EXPECTATIONS, current_source_expectation, review_record, KA_HY_AZ_ADDITIONS, GL_ADDITIONS, SO_WO_HT_ADDITIONS, KK_TG_PS_ADDITIONS, BR_AST_OC_ADDITIONS, CEB_NDS_CSB_ADDITIONS, IA_LA_KU_ADDITIONS, MI_SM_RW_ADDITIONS, WA_SE_SA_ADDITIONS, KAB_MWW_MAI_ADDITIONS, SD_PCM_TPI_ADDITIONS, CKB_UG_TT_ADDITIONS, ARY_MN_TOK_ADDITIONS, BO_DZ_VAL_ADDITIONS, HNE_YI_HK_ADDITIONS
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
        self.assertEqual(120, len(self.index))
        self.assertEqual(60, len({tag for tag, key in self.index}))
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
            for wrong in ((old or '') + ' changed', expected, source, ''):
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

    def test_expected_constant_and_source_corruption_is_rejected(self):
        for key in KEYS:
            data = deepcopy(self.data); data['sources'][key] += ' changed'
            with self.subTest(key=key), self.assertRaises(ValueError): validated_successors(data)
        for tag, terms in self.data['values'].items():
            for key in terms:
                data = deepcopy(self.data); data['values'][tag][key] += ' forged'
                with self.subTest(tag=tag, key=key), self.assertRaises(ValueError): validated_successors(data)

    def test_missing_extra_held_and_unknown_candidates_are_rejected(self):
        for mutation in ('missing', 'extra', 'held', 'unknown', 'missing-key', 'extra-key'):
            data = deepcopy(self.data); tag = next(iter(data['values']))
            if mutation == 'missing': data['values'].pop(tag)
            elif mutation in ('extra', 'held', 'unknown'):
                name = {'extra': 'en-001', 'held': 'jje', 'unknown': 'unknown'}[mutation]
                data['values'][name] = deepcopy(data['values'][tag])
            elif mutation == 'missing-key': data['values'][tag].pop(next(iter(KEYS)))
            else: data['values'][tag]['other_key'] = 'arbitrary'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): validated_successors(data)

    def test_held_missing_and_canonical_values_are_preserved_not_accepted(self):
        counts = {'held': 0, 'missing': 0, 'canonical': 0, 'qualified-priority': 0, 'qualified-single-key': 0, 'qualified-new-priority': 0}
        for option in review_record()['options']:
            tag = option['tag']; actual = catalogues.read_strings(ROOT / option['catalogue'])
            for key, term in option['terms'].items():
                if (tag, key) in self.index: continue
                if (tag, key) in SINGLE_KEY_EXPECTATIONS:
                    with self.subTest(tag=tag, key=key):
                        self.assertIsNone(term['value'])
                        expected = current_source_expectation(key, tag, None)
                        self.assertEqual(expected, actual.get(key))
                        with self.assertRaises(ValueError): accepted_warning(key, tag)
                        with self.assertRaises(ValueError): current_source_expectation(key, tag, expected)
                    counts['qualified-single-key'] += 1
                    continue
                if (tag, key) in PRIORITY_ADDITIONS | SK_SL_CA_ADDITIONS | MR_TA_TE_ADDITIONS | KN_ML_ADDITIONS | NORDIC_ADDITIONS | NN_BE_SQ_ADDITIONS | HR_BS_MK_ADDITIONS | SERBIAN_DELTA_ADDITIONS | HI_GU_ADDITIONS | THAI_ADDITIONS | NE_PA_ADDITIONS | YO_ZU_XH_ADDITIONS | HA_IG_LN_ADDITIONS | JV_SU_KY_ADDITIONS | AS_KM_LO_ADDITIONS | GA_GD_CY_ADDITIONS | EU_FY_UZ_ADDITIONS | KA_HY_AZ_ADDITIONS | GL_ADDITIONS | SO_WO_HT_ADDITIONS | KK_TG_PS_ADDITIONS | BR_AST_OC_ADDITIONS | CEB_NDS_CSB_ADDITIONS | IA_LA_KU_ADDITIONS | MI_SM_RW_ADDITIONS | WA_SE_SA_ADDITIONS | KAB_MWW_MAI_ADDITIONS | SD_PCM_TPI_ADDITIONS | CKB_UG_TT_ADDITIONS | ARY_MN_TOK_ADDITIONS | BO_DZ_VAL_ADDITIONS | HNE_YI_HK_ADDITIONS | EXACT_SCRIPT_ADDITIONS:
                    with self.subTest(tag=tag,key=key):
                        self.assertIsNone(term['value'])
                        expected=current_source_expectation(key,tag,None)
                        self.assertEqual(expected,actual.get(key))
                        with self.assertRaises(ValueError):accepted_warning(key,tag)
                        with self.assertRaises(ValueError):current_source_expectation(key,tag,expected)
                    counts['qualified-new-priority'] += 1
                    continue
                if tag in PRIORITY_TAGS:
                    with self.subTest(tag=tag, key=key):
                        self.assertIsNone(term['value'])
                        expected = current_source_expectation(key, tag, None)
                        self.assertEqual(expected, actual.get(key))
                        with self.assertRaises(ValueError): accepted_warning(key, tag)
                        with self.assertRaises(ValueError): current_source_expectation(key, tag, expected)
                    counts['qualified-priority'] += 1
                    continue
                with self.subTest(tag=tag, key=key):
                    self.assertEqual(term['value'], actual.get(key))
                    with self.assertRaises(ValueError): accepted_warning(key, tag)
                if tag == 'en-001': counts['canonical'] += 1
                elif term['value'] is None: counts['missing'] += 1
                else: counts['held'] += 1
        self.assertEqual({'held': 4, 'missing': 195-len(GA_GD_CY_ADDITIONS | MR_TA_TE_ADDITIONS | KN_ML_ADDITIONS | NORDIC_ADDITIONS | NN_BE_SQ_ADDITIONS | HR_BS_MK_ADDITIONS | SERBIAN_DELTA_ADDITIONS | HI_GU_ADDITIONS | THAI_ADDITIONS | NE_PA_ADDITIONS | YO_ZU_XH_ADDITIONS | HA_IG_LN_ADDITIONS | JV_SU_KY_ADDITIONS | AS_KM_LO_ADDITIONS | EU_FY_UZ_ADDITIONS | KA_HY_AZ_ADDITIONS | GL_ADDITIONS | SO_WO_HT_ADDITIONS | KK_TG_PS_ADDITIONS | BR_AST_OC_ADDITIONS | CEB_NDS_CSB_ADDITIONS | IA_LA_KU_ADDITIONS | MI_SM_RW_ADDITIONS | WA_SE_SA_ADDITIONS | KAB_MWW_MAI_ADDITIONS | SD_PCM_TPI_ADDITIONS | CKB_UG_TT_ADDITIONS | ARY_MN_TOK_ADDITIONS | BO_DZ_VAL_ADDITIONS | HNE_YI_HK_ADDITIONS | EXACT_SCRIPT_ADDITIONS), 'canonical': 2, 'qualified-priority': 4, 'qualified-single-key': 11, 'qualified-new-priority': 6+len(GA_GD_CY_ADDITIONS | MR_TA_TE_ADDITIONS | KN_ML_ADDITIONS | NORDIC_ADDITIONS | NN_BE_SQ_ADDITIONS | HR_BS_MK_ADDITIONS | SERBIAN_DELTA_ADDITIONS | HI_GU_ADDITIONS | THAI_ADDITIONS | NE_PA_ADDITIONS | YO_ZU_XH_ADDITIONS | HA_IG_LN_ADDITIONS | JV_SU_KY_ADDITIONS | AS_KM_LO_ADDITIONS | EU_FY_UZ_ADDITIONS | KA_HY_AZ_ADDITIONS | GL_ADDITIONS | SO_WO_HT_ADDITIONS | KK_TG_PS_ADDITIONS | BR_AST_OC_ADDITIONS | CEB_NDS_CSB_ADDITIONS | IA_LA_KU_ADDITIONS | MI_SM_RW_ADDITIONS | WA_SE_SA_ADDITIONS | KAB_MWW_MAI_ADDITIONS | SD_PCM_TPI_ADDITIONS | CKB_UG_TT_ADDITIONS | ARY_MN_TOK_ADDITIONS | BO_DZ_VAL_ADDITIONS | HNE_YI_HK_ADDITIONS | EXACT_SCRIPT_ADDITIONS)}, counts)

    def test_compact_behavior_oracle_corruption_is_rejected(self):
        original_read = Path.read_bytes
        def corrupt(path):
            raw = original_read(path)
            return raw + b' changed' if path == RECORD else raw
        with patch.object(Path, 'read_bytes', corrupt), self.assertRaises(ValueError):
            validated_successors(self.data)

    def test_historical_source_drift_is_rejected(self):
        original_read = Path.read_text
        for key in KEYS:
            def corrupt(path, *args, **kwargs):
                raw = original_read(path, *args, **kwargs)
                if path == binding_module.QUEUE:
                    data = json.loads(raw); data['keys'][key]['corrected_english'] += ' changed'
                    return json.dumps(data)
                return raw
            with self.subTest(key=key), patch.object(Path, 'read_text', corrupt), self.assertRaises(ValueError):
                validated_successors(self.data)

    def test_amharic_missing_history_cannot_be_rewritten(self):
        original_read = Path.read_text
        for key in KEYS:
            def corrupt(path, *args, **kwargs):
                raw = original_read(path, *args, **kwargs)
                if path == binding_module.QUEUE:
                    data = json.loads(raw)
                    option = next(o for o in data['options'] if o['tag'] == 'am')
                    option['terms'][key]['value'] = 'invented old target'
                    return json.dumps(data)
                return raw
            with self.subTest(key=key), patch.object(Path, 'read_text', corrupt), self.assertRaises(ValueError):
                validated_successors(self.data)

    def test_held_historical_target_drift_is_rejected_without_acceptance(self):
        for option in review_record()['options']:
            if option['tag'] not in ('jje', 'vi-Hani'): continue
            for key, term in option['terms'].items():
                self.assertEqual(term['value'], current_source_expectation(key, option['tag'], term['value']))
                with self.assertRaises(ValueError):
                    current_source_expectation(key, option['tag'], term['value'] + ' changed')

    def test_unmapped_keys_cannot_obtain_acceptance(self):
        for tag, key in [('unknown', next(iter(KEYS))), ('af', 'unrelated'), ('jje', next(iter(KEYS)))]:
            with self.subTest(tag=tag, key=key), self.assertRaises(ValueError): accepted_warning(key, tag)
        self.assertEqual('unrelated', current_source_expectation('other_key', 'af', 'unrelated'))
        with self.assertRaises(ValueError): current_source_expectation(next(iter(KEYS)), 'unknown', 'arbitrary actual')

    def test_canonical_old_source_drift_rejected(self):
        for key in KEYS:
            with self.assertRaises(ValueError): current_source_expectation(key, 'default', 'unknown source')


if __name__ == '__main__':
    unittest.main()
