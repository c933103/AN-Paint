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
        self.assertEqual('Αποθήκευση των αλλαγών;', strings[QUESTION])
        self.assertEqual('Η τρέχουσα εικόνα έχει μη αποθηκευμένες αλλαγές.', strings['ui_your_current_image_has_unsaved_changes'])
        self.assertEqual('@string/ui_save', strings['ui_save_a5d0d9'])
        self.assertEqual('Αποθήκευση', strings['ui_save'])
        self.assertEqual('Απόρριψη αλλαγών', strings['ui_discard_changes23'])
        self.assertEqual('Συνέχεια επεξεργασίας', strings['ui_keep_editing23'])
        self.assertRegex(self.activity, r'fun confirmReplacement\(action: \(\) -> Unit\)')
        self.assertIn('.setTitle(ui(R.string.' + QUESTION + ')).setMessage(ui(R.string.ui_your_current_image_has_unsaved_changes))', self.activity)

    def test_recovery_instruction_names_current_file_open_command(self):
        strings = self.strings['el']
        command = strings['ui_load_image'].rstrip('…')
        self.assertEqual('Άνοιγμα εικόνας', command)
        self.assertEqual('Αρχείο', strings['ui_menu_file'])
        self.assertEqual('Το αντίγραφο ανάκτησης εξήχθη. Εξαγάγετε το canvas.png από το ZIP και ανοίξτε το με '
                         + strings['ui_menu_file'] + ' > ' + command
                         + '. Το ZIP περιέχει επίσης τις ρυθμίσεις του προχείρου και τυχόν αιωρούμενη επιλογή.', strings[RECOVERY])
        self.assertRegex(self.activity, r'"File"->\(listOf[\s\S]*?ui\(R\.string\.ui_load_image\) to \{confirmReplacement \{launchOpen\(false\)\}\}')
        self.assertIn('message(ui(R.string.' + RECOVERY + '))', self.activity)

    def test_language_note_keeps_new_and_untranslated_fallback_without_temporary_promise(self):
        self.assertEqual(r'Γλώσσα εφαρμογής\n\nΟι μεταφράσεις διατηρούνται στους γλωσσικούς πόρους του AN Paint. '
                         'Το νέο ή αμετάφραστο κείμενο εμφανίζεται στα αγγλικά.', self.strings['el'][NOTE])
        self.assertEqual(2, self.strings['el'][NOTE].count('\\n'))
        self.assertNotIn('προσωρινά', self.strings['el'][NOTE])
        picker = (CLASSIC / 'AppLanguage.kt').read_text(encoding='utf-8')
        self.assertIn('text = ui(R.string.' + NOTE + ')', picker)

    def test_shape_style_retains_distinct_outline_solid_and_outline_plus_fill_options(self):
        strings = self.strings['el']
        self.assertEqual(('Περίγραμμα', 'Συμπαγές γέμισμα', 'Γέμισμα + γραμμή'),
                         tuple(strings[key] for key in ('ui_outline', FILL, 'ui_fill_line')))
        self.assertIn('addChoice(listOf(ui(R.string.ui_outline), ui(R.string.' + FILL + '), ui(R.string.ui_fill_line)), document.shapeStyle)', self.activity)

if __name__ == '__main__':
    unittest.main()
