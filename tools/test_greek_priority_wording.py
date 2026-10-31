"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

RECOVERY = 'ui_recovery_copy_exported_extract_canvas_png_from_the'

QUESTION = 'ui_save_your_changes'

NOTE = 'language20_translation_note'

FILL = 'ui_solid_fill'

CLASSIC = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'

class GreekPriorityWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text(encoding='utf-8')
                   for tag, folder in [('default', 'values'), ('el', 'values-el')]}
        cls.strings = {tag: {n.get('name'): ''.join(n.itertext()) for n in ET.fromstring(xml) if n.tag == 'string'}
                       for tag, xml in cls.xml.items()}
        cls.activity = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')

    def test_save_question_and_actions_are_consistent_in_replacement_dialog(self):
        strings = self.strings['el']
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual(3, len({strings[key] for key in ('ui_save', 'ui_discard_changes23', 'ui_keep_editing23')}))

    def test_recovery_instruction_names_current_file_open_command(self):
        strings = self.strings['el']
        command = strings['ui_load_image'].rstrip('…')
        self.assertIn(strings['ui_menu_file'] + ' > ' + command, strings[RECOVERY])
        self.assertIn('canvas.png', strings[RECOVERY])
        self.assertIn('ZIP', strings[RECOVERY])
        self.assertIn('ρυθμίσεις', strings[RECOVERY])
        self.assertIn('τυχόν αιωρούμενη επιλογή', strings[RECOVERY])
        # Recovery-export notification has no independently mapped runtime binding yet.
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_keeps_new_and_untranslated_fallback_without_temporary_promise(self):
        value = self.strings['el'][NOTE]
        self.assertIn('νέο ή αμετάφραστο', value)
        self.assertNotIn('προσωρινά', value)

    def test_shape_style_retains_distinct_outline_solid_and_outline_plus_fill_options(self):
        strings = self.strings['el']
        self.assertEqual(3, len({strings[key] for key in ('ui_outline', FILL, 'ui_fill_line')}))

if __name__ == '__main__':
    unittest.main()
