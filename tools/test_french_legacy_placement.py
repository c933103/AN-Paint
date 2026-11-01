"""French right/below placement versus aligned edges; no dormant prose mirror."""
import unittest
from current_localization_contracts import current_display

class FrenchLegacyPlacementTest(unittest.TestCase):
    def test_legacy_manual_and_active_drag_hint_agree_on_both_edges(self):
        for key in ('ui_the_arrow_on_the_left_directly_below_the', 'ui_drop_at_a_highlighted_edge_right_top_aligned'):
            value = current_display('fr', key)
            self.assertIn('à droite avec les bords supérieurs alignés', value)
            self.assertIn('en dessous avec les bords gauches alignés', value)

if __name__ == '__main__': unittest.main()
