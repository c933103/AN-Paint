"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


from current_localization_contracts import require_string
MEMORY = "ui_d_d_pixels_2f_mp_exceeds_the_current"
RESIZE = "ui_the_full_image_and_working_buffers_exceed_the"
COUNT = "ui_d_d_px_d_pixels_2f_mp"
NOTE = "language20_translation_note"

class DutchEditorWordingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = catalogues.catalogue_paths()['nl']
        cls.xml = {'nl': path.read_text()}
        cls.strings = {'nl': catalogues.read_strings(path)}

    def test_all_memory_warning_clauses_are_kept_and_allocation_names_memory(self):
        value = self.strings['nl'][MEMORY]
        clauses = (
            '%1$d × %2$d pixels (%3$.2f MP) overschrijdt de huidige veilige bewerkingslimiet van %4$.2f MP.',
            'AN Paint houdt de volledige afbeelding in het geheugen en reserveert ruimte voor transformaties en selecties.',
            'Het beschikbare geheugen bepaalt deze limiet.',
            'De bewerking is gestopt voordat er geheugen voor de te grote bitmap werd toegewezen.',
            'Er is niet automatisch verkleind.',
        )
        clauses=(clauses[0].replace('pixels','px',1),)+clauses[1:]
        self.assertEqual(' '.join(clauses),value)
        for clause in clauses:
            root = ET.fromstring(self.xml['nl'])
            root.find(f"./string[@name='{MEMORY}']").text = value.replace(clause, '')
            with self.subTest(omitted=clause), self.assertRaises(ValueError):
                require_string(ET.tostring(root, encoding='unicode'), MEMORY, value,
                               {'attributes': {'name': MEMORY}})

    def test_resize_reason_keeps_both_causes_copy_target_and_unchanged_original(self):
        value = self.strings['nl'][RESIZE]
        self.assertEqual(
            'De volledige afbeelding en werkbuffers overschrijden de huidige veilige geheugenlimiet, '
            'of Android kon er geen geheugen voor toewijzen. '
            'Wijzig het formaat van een kopie om deze te bewerken. '
            'Uw oorspronkelijke bestand blijft ongewijzigd.', value)

    def test_language_note_explains_maintenance_and_english_fallback_without_claiming_completeness(self):
        value = self.strings['nl'][NOTE]
        self.assertEqual(
            'App-taal\\n\\nVertalingen worden onderhouden in de taalbestanden van AN Paint. '
            'Nieuwe of onvertaalde tekst verschijnt in het Engels.', value)
        self.assertEqual(2, value.count('\\n'))
        self.assertNotIn('alle vertaalbare interfacetekst', value)

    def test_encoder_reports_unfinished_operation(self):
        self.assertEqual('De encoder heeft de bewerking niet voltooid.',
                         self.strings['nl']['ui_the_encoder_did_not_finish'])

    def test_ellipse_is_a_drawing_tool_and_is_distinct_from_selection(self):
        strings = self.strings['nl']
        self.assertEqual('Ellips', strings['ui_ellipse'])
        self.assertEqual(('Rechthoekige selectie', 'Vrije selectie'),
                         (strings['ui_rectangle_select'], strings['ui_free_form_select']))
        classic = catalogues.ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        document = (classic / 'PaintDocument.kt').read_text()
        categories = (classic / 'ToolCategoryButton.kt').read_text()
        self.assertRegex(document, r'ELLIPSE\(R\.string\.ui_ellipse\s*,')
        insert = re.search(r'INSERT\(R\.string\.ui_category_insert,listOf\((.*?)\)\)', categories, re.S)
        self.assertIsNotNone(insert)
        self.assertIn('PaintTool.ELLIPSE', insert.group(1))
        self.assertNotIn('PaintTool.SELECT', insert.group(1))

    def test_count_label_is_number_neutral_and_unit_labels_compose_in_lowercase(self):
        strings = self.strings['nl']
        self.assertEqual('%1$d × %2$d px · Aantal pixels: %3$,d (%4$.2f MP)', strings[COUNT])
        self.assertEqual('pixels', strings['ui_pixels_6ec9c2'])
        # Host-side text composition, not Android/TalkBack execution.
        for key, expected in (('ui_width_in', 'Breedte in pixels'),
                              ('ui_height_in', 'Hoogte in pixels')):
            self.assertEqual(expected, strings[key].replace('%1$s', strings['ui_pixels_6ec9c2']))

    def test_existing_save_choices_colour_abbreviations_and_prior_memory_text_are_preserved(self):
        strings = self.strings['nl']
        self.assertEqual(('Opslaan', 'Wijzigingen verwerpen', 'Doorgaan met bewerken'),
                         tuple(strings[k] for k in ('ui_save_a5d0d9', 'ui_discard_changes23', 'ui_keep_editing23')))
        self.assertEqual(('VG', 'AG'), (strings['ui_fg'], strings['ui_bg']))
        self.assertEqual(
            'De schattingen omvatten het huidige canvas en klembord, decodering met subsampling en bewerkingsbuffers. '
            'Het werkelijke geheugengebruik varieert. Een kleinere kopie verliest detail. '
            'Het oorspronkelijke bestand blijft ongewijzigd.', strings['ui_sampled_resize_memory_explanation'])

    def test_colour_swap_names_both_actual_colour_roles(self):
        value = self.strings['nl']['ui_swap_foreground_background']
        self.assertIn('Voorgrond', value)
        self.assertIn('achtergrondkleur', value)

if __name__ == '__main__':
    unittest.main()
