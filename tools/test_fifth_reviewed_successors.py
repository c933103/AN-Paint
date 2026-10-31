"""Exact 90 missing and 15 existing forward decisions, not whole-language acceptance."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from current_localization_contracts import residual_rows, fixture, require_residual_or_previous
from priority_cohort_checks import require_resource_shape

TAGS = ('ary', 'tok', 'sm', 'nds', 'eu-ES', 'ca-ES-valencia', 'ps', 'sd', 'ug')
MISSING_COUNTS = dict(zip(TAGS, (11, 11, 11, 11, 7, 8, 9, 11, 11)))
EXISTING = {
    ('nds', 'ui_save_a5d0d9'),
    ('nds', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'),
    ('ps', 'ui_drawing_canvas_pinch_and_move_two_fingers_to'),
} | {('tok', key) for key in (
    'formats22_ascii_description', 'ui_a_separate_recovery_copy_has_been_kept_use',
    'ui_autosave_is_paused_to_protect_that_draft_use', 'ui_share_explanation34',
    'ui_colour_palette_tap_for_foreground_hold_for_background',
    'ui_crop_preview_drag_an_edge_or_corner_drag',
    'ui_not_enough_memory_to_finish_opening_this_image',
    'ui_not_enough_memory_to_inspect_this_image', 'ui_tap_to_type_a_number',
    'ui_tool_categories', 'save20_destination_error', 'commons_svg_original_size_unavailable')}


class FifthReviewedSuccessors(unittest.TestCase):
    def test_exact_scope_and_held_discard_boundaries(self):
        rows = {identity: row for identity, row in residual_rows().items() if identity[0] in TAGS}
        self.assertEqual(105, len(rows))
        self.assertEqual(EXISTING, {i for i, r in rows.items() if r['previous_target'] is not None})
        self.assertEqual(MISSING_COUNTS, {tag: sum(i[0] == tag and r['previous_target'] is None
                                                for i, r in rows.items()) for tag in TAGS})
        self.assertIn('https://github.com/c933103/AN-Paint/pull/56#issuecomment-6532854518',
                      fixture('reviewed_residuals_20261030.json')['reviews'])
        for tag in ('eu-ES', 'ps'):
            self.assertNotIn((tag, 'ui_discard'), rows)
        self.assertEqual({'name': 'ui_share_explanation34', 'formatted': 'false'},
                         rows[('tok', 'ui_share_explanation34')]['attributes'])

    def test_every_decision_rejects_shape_text_and_predecessor_regressions(self):
        for (tag, key), row in residual_rows().items():
            if tag not in TAGS:
                continue
            original = ET.parse(catalogues.catalogue_paths()[tag]).getroot()
            def check(root, predecessor=row['previous_target']):
                require_residual_or_previous(root, tag, key, predecessor)
                nodes = root.findall(f"./*[@name='{key}']")
                if len(nodes) != 1:
                    raise ValueError('Exact successor identity differs')
                require_resource_shape(nodes[0], 'string', {'value': row['target'], 'attributes': row['attributes']})
            check(original)
            for mutation in ('missing', 'duplicate', 'type', 'text', 'attribute', 'child', 'tail', 'predecessor'):
                root = deepcopy(original); node = root.find(f"./string[@name='{key}']")
                if mutation == 'missing': root.remove(node)
                elif mutation == 'duplicate': root.append(deepcopy(node))
                elif mutation == 'type': node.tag = 'plurals'
                elif mutation == 'text': node.text += ' forged'
                elif mutation == 'attribute': node.set('translatable', 'false')
                elif mutation == 'child': ET.SubElement(node, 'b')
                elif mutation == 'tail': node.tail = 'forged'
                else: node.text = row['previous_target'] or 'unreviewed fallback'
                with self.subTest(tag=tag, key=key, mutation=mutation), self.assertRaises(ValueError):
                    check(root)
            with self.subTest(tag=tag, key=key, mutation='wrong predecessor'), self.assertRaises(ValueError):
                check(original, 'forged predecessor')



if __name__ == '__main__':
    unittest.main()
