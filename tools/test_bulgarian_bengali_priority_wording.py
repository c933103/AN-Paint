"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

TAGS = {'bg', 'bn'}

class BulgarianBengaliPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('bg', 'values-bg'), ('bn', 'values-bn')]}
        cls.roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}

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
