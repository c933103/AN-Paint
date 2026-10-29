from nynorsk_belarusian_albanian_priority_expectations import MEMORY_ADDITIONS as NN_BE_SQ_ADDITIONS
"""Source wording and review-queue structure, not linguistic or runtime approval."""
from collections import Counter
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET

from current_localization_contracts import require_string
from memory_warning_source_review import EXACT_SCRIPT_ADDITIONS, EU_FY_UZ_ADDITIONS, GA_GD_CY_ADDITIONS, YO_ZU_XH_ADDITIONS, HA_IG_LN_ADDITIONS, JV_SU_KY_ADDITIONS, AS_KM_LO_ADDITIONS, NE_PA_ADDITIONS, KN_ML_ADDITIONS, MR_TA_TE_ADDITIONS, KEYS, current_source_expectation, review_record, KA_HY_AZ_ADDITIONS, GL_ADDITIONS, SO_WO_HT_ADDITIONS, KK_TG_PS_ADDITIONS, BR_AST_OC_ADDITIONS, CEB_NDS_CSB_ADDITIONS, IA_LA_KU_ADDITIONS, MI_SM_RW_ADDITIONS, WA_SE_SA_ADDITIONS, KAB_MWW_MAI_ADDITIONS, SD_PCM_TPI_ADDITIONS, CKB_UG_TT_ADDITIONS, ARY_MN_TOK_ADDITIONS, BO_DZ_VAL_ADDITIONS, HNE_YI_HK_ADDITIONS
import translation_catalogues as catalogues


EXPECTED = {
    'ui_no_resize_fits_decoder_memory':
        'Even at the smallest output size, this image cannot be loaded for editing within the current memory limits. '
        'Cancel and use a smaller source image.',
    'ui_assembly_source_memory_floor':
        'This assembly is estimated to exceed the current working-memory budget, even at the smallest output size. '
        'Reducing the assembly dimensions alone is not enough under the current limits. '
        'Close other documents or prepare a smaller source image before trying again. Your assembly is unchanged.',
}
CONSTRAINTS = {'formatted': True, 'placeholders': {}, 'escaped_newline_count': 0}


class MemoryWarningSourceReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = review_record()
        cls.xml = (catalogues.RES / 'values/strings.xml').read_text(encoding='utf-8')

    def test_complete_english_source_and_scalar_contract(self):
        self.assertEqual(KEYS, set(self.data['keys']))
        for key, expected in EXPECTED.items():
            with self.subTest(key=key):
                self.assertEqual(expected, self.data['keys'][key]['corrected_english'])
                require_string(self.xml, key, expected, {**CONSTRAINTS, 'attributes': {'name': key}})
                nodes = [n for n in ET.fromstring(self.xml) if n.get('name') == key]
                self.assertEqual(['string'], [n.tag for n in nodes])

    def test_source_rejects_old_diagnosis_and_corruptions(self):
        for key, expected in EXPECTED.items():
            node = ET.fromstring(self.xml).find(f"./string[@name='{key}']")
            for mutation in ('old-diagnosis', 'missing', 'duplicate', 'truncate', 'markup', 'placeholder', 'attribute'):
                root = ET.Element('resources')
                changed = deepcopy(node)
                if mutation != 'missing': root.append(changed)
                if mutation == 'old-diagnosis': changed.text = self.data['keys'][key]['old_english']
                elif mutation == 'duplicate': root.append(deepcopy(changed))
                elif mutation == 'truncate': changed.text = expected[:-1]
                elif mutation == 'markup':
                    ET.SubElement(changed, 'b').text, changed.text = expected, None
                elif mutation == 'placeholder': changed.text += ' %1$s'
                elif mutation == 'attribute': changed.set('translatable', 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    require_string(ET.tostring(root, encoding='unicode'), key, expected,
                                   {**CONSTRAINTS, 'attributes': {'name': key}})

    def test_queue_covers_every_offered_option_in_sequential_order(self):
        rows = self.data['options']
        tags = catalogues.offered_tags()
        self.assertEqual(tags, [r['tag'] for r in rows])
        self.assertEqual(list(range(1, len(tags) + 1)), [r['order'] for r in rows])
        self.assertEqual(171, len(set(tags)))
        self.assertEqual(342, sum(len(r['terms']) for r in rows))
        self.assertEqual(171, self.data['scope']['offered_options'])
        self.assertEqual(342, self.data['scope']['review_items'])
        for row in rows:
            self.assertEqual(KEYS, set(row['terms']), row['tag'])

    def test_values_absences_fallbacks_and_english_variants_are_explicit(self):
        paths = catalogues.catalogue_paths()
        counts = Counter()
        current_counts = Counter()
        for row in self.data['options']:
            tag = row['tag']
            path = catalogues.RES / 'values/strings.xml' if tag == 'en-001' else paths[tag]
            self.assertEqual(path.relative_to(catalogues.ROOT).as_posix(), row['catalogue'])
            strings = catalogues.read_strings(path)
            kind = ('canonical-english' if tag == 'en-001' else 'private-use-english' if tag == 'en-XV'
                    else 'english-variant' if tag.startswith('en-') else 'non-english')
            self.assertEqual(kind, row['kind'])
            for key, term in row['terms'].items():
                with self.subTest(tag=tag, key=key):
                    self.assertEqual(strings.get(key), current_source_expectation(key, tag, term['value']) if tag != 'en-001' else term['value'])
                    # The initial queue remains historical, including absences.
                    present = term['value'] is not None
                    self.assertEqual('present' if present else 'missing', term['value_status'])
                    self.assertEqual(None if present else 'canonical-english', term['fallback'])
                    counts[(key, term['value_status'])] += 1
                    current_counts[(key, 'present' if key in strings else 'missing')] += 1
        for key in KEYS:
            self.assertEqual(62, counts[(key, 'present')])
            self.assertEqual(109, counts[(key, 'missing')])
            # Explicit separate priority additions; the frozen queue still retains every historical absence.
            added = (12 if key == 'ui_assembly_source_memory_floor' else 5) + sum(k==key for _,k in MR_TA_TE_ADDITIONS | KN_ML_ADDITIONS | NN_BE_SQ_ADDITIONS | NE_PA_ADDITIONS | YO_ZU_XH_ADDITIONS | HA_IG_LN_ADDITIONS | JV_SU_KY_ADDITIONS | AS_KM_LO_ADDITIONS | GA_GD_CY_ADDITIONS | EU_FY_UZ_ADDITIONS | KA_HY_AZ_ADDITIONS | GL_ADDITIONS | SO_WO_HT_ADDITIONS | KK_TG_PS_ADDITIONS | BR_AST_OC_ADDITIONS | CEB_NDS_CSB_ADDITIONS | IA_LA_KU_ADDITIONS | MI_SM_RW_ADDITIONS | WA_SE_SA_ADDITIONS | KAB_MWW_MAI_ADDITIONS | SD_PCM_TPI_ADDITIONS | CKB_UG_TT_ADDITIONS | ARY_MN_TOK_ADDITIONS | BO_DZ_VAL_ADDITIONS | HNE_YI_HK_ADDITIONS | EXACT_SCRIPT_ADDITIONS)
            self.assertEqual(65 + added, current_counts[(key, 'present')])
            self.assertEqual(106 - added, current_counts[(key, 'missing')])

    def test_initial_queue_grants_no_renewed_acceptance_or_language_credit(self):
        self.assertEqual(0, self.data['scope']['reviewed_against_corrected_source'])
        self.assertEqual(0, self.data['scope']['new_language_completion_credit'])
        dispositions = {'source-corrected-review-pending', 'needs-edit-after-review',
                        'needs-translation-or-fallback-decision', 'needs-review-edit-if-required'}
        for row in self.data['options']:
            for key, term in row['terms'].items():
                with self.subTest(tag=row['tag'], key=key):
                    self.assertEqual('needs-review', term['review_status'])
                    self.assertIsNone(term['review_receipt'])
                    self.assertIn(term['edit_disposition'], dispositions)

    def test_default_source_binding_preserves_unknown_and_unrelated_pairs(self):
        for key in KEYS:
            old = self.data['keys'][key]['old_english']
            self.assertEqual(EXPECTED[key], current_source_expectation(key, 'default', old))
            for tag in ('unknown-tag', 'ain-Kana', 'ain-Latn', 'jje', 'vi-Hani'):
                with self.assertRaises(ValueError):
                    current_source_expectation(key, tag, old)
            with self.assertRaises(ValueError):
                current_source_expectation(key, 'default', old + ' corrupted')
        self.assertEqual('unrelated', current_source_expectation('another_key', 'default', 'unrelated'))


if __name__ == '__main__':
    unittest.main()
