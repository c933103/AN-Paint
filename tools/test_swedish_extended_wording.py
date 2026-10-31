"""Current locale semantics; historical approval snapshots live in immutable source history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues

MANUAL_KEY = 'ui_the_arrow_on_the_left_directly_below_the'

class SwedishExtendedWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text()
                   for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.manual_roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-sv/strings.xml')

    def test_crop_singular_plural_keep_full_conditional_movement_warning(self):
        entry = {tag: {n.get('quantity'): n.text for n in ET.fromstring(self.xml[tag]).findall("./plurals[@name='ui_crop_preview_images']/item")} for tag in ('default', 'sv')}
        for tag in ('default', 'sv'):
            nodes = ET.fromstring(self.xml[tag]).findall("./plurals[@name='ui_crop_preview_images']")
            self.assertEqual(1, len(nodes))
            items = nodes[0].findall('item')
            self.assertEqual(['one', 'other'], [n.get('quantity') for n in items])
            for node in items:
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(node.text))
        for value in entry['sv'].values():
            self.assertIn('kan bilder som är fästa vid dem flyttas.', value)
            self.assertEqual(1, value.count('\\n'))
        self.assertIn('%3$d bild.', entry['sv']['one'])
        self.assertIn('%3$d bilder.', entry['sv']['other'])

    def test_active_help_navigation_matches_actual_controls(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        help_text = s['ui_help23']
        for key in ('ui_menu_view', 'ui_navigate', 'ui_draw26', 'ui_drawing23', 'ui_category_selection',
                    'ui_category_insert', 'ui_swap23', 'ui_reset_bw23', 'ui_use_colour', 'ui_add_colour26',
                    'ui_advanced', 'ui_pixel_grid33', 'ui_cursor_drawing32', 'ui_about_credits23', 'commons_blank_maps'):
            self.assertIn(s[key], help_text, key)
        navigation = f"{s['ui_menu_file']} → {s['ui_about_credits23']} → {s['ui_image_credits']}"
        for key in ('gallery_description', 'ui_irasutoya_help34', 'ui_openclipart_help34'):
            self.assertIn(navigation, s[key])
            self.assertIn(s['gallery_use_image'], s[key])
        self.assertIn(s['gallery_copy_credit'], s['gallery_description'])
        self.assertEqual('@string/ui_cursor_help31', s['ui_cursor_help29'])

    def test_behavioural_distinctions_are_not_flattened(self):
        s = self.strings
        self.assertEqual('Färghjul', s['ui_wheel'])
        self.assertEqual('Överkant', s['ui_top'])
        self.assertEqual('Rund', s['ui_round'])
        self.assertIn('Jämna ut frihandsdrag', s['ui_smooth_freehand_strokes'])
        self.assertIn('Överlappning är tillåten här.', s['ui_assembly_position_help'])
        self.assertIn('Övriga bilder behåller sina nuvarande positioner.', s['ui_assembly_position_help'])
        self.assertIn('Bilder som importerats senare ritas ovanpå.', s['ui_assembly_position_help'])
        self.assertIn('Beskärningar och storlekar förblir oförändrade.', s['ui_assembly_position_help'])
        self.assertIn('Bilden importerades inte.', s['gallery_image_component_unavailable'])
        self.assertIn('kan minska filstorleken utan att ändra bildpunkterna', s['formats22_tiff_description'])
        self.assertIn('antiAlias=false; strokeDashArray=none; background=#FFFFFF.', s['commons_import_svg_changes'])
        self.assertIn('background=#FFFFFF', s['commons_import_raster_changes'])

    def test_assembly_help_preserves_separate_modes_and_actual_control_labels(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        value = s['ui_add_up_to_20_images_with_android_s']
        paragraphs = value.split(r'\n\n')
        self.assertEqual(8, len(paragraphs))
        self.assertIn('Vid fästning börjar den första bilden i origo och överlappningar avvisas.', paragraphs[2])
        self.assertIn('räknat från noll', paragraphs[3])
        self.assertIn('Övriga bilder behåller sina positioner och överlappningar är tillåtna.', paragraphs[3])
        self.assertIn('kan flyttas för att fylla luckan', paragraphs[5])
        for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                    'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest',
                    'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                    'ui_save_png', 'ui_edit_in_paint', 'ui_menu_file', 'ui_about_credits23'):
            self.assertIn(s[key], value, key)

    def test_curve_hint_describes_early_completion_not_an_attachment(self):
        hint = self.strings['ui_drag_a_line_then_drag_twice_to_set']
        self.assertIn(self.strings['ui_finish_curve'], hint)
        self.assertIn('slutföra kurvan innan båda böjarna har ställts in.', hint)
        self.assertNotIn('fästa', hint)

    def _manual_node(self, tag):
        return self.manual_roots[tag].find(f"./string[@name='{MANUAL_KEY}']")

    def test_live_labels_and_behavioral_distinctions_are_not_stale(self):
        expected = {
            'default': {1:['Color tab','foreground or background','existing canvas','white backing'],
                        2:['Draw again','floating selection'],4:['options panel','Edit > Selection','quick actions'],
                        6:['Drawing category','View > Magnifier lets you enable'],
                        7:['Wikimedia Commons'],8:['Exact position','permits overlaps','may move to fill the gap']},
            'sv': {1:['Fliken Färg','förgrunds- eller bakgrundsdel','befintliga ritytan','vit bakgrund'],
                   2:['Fortsätt rita','flytande markering'],4:['alternativpanelen','Redigera > Markering','snabbåtgärder'],
                   6:['kategorin Ritverktyg','Visa > Förstoringsglas kan du aktivera'],
                   7:['Wikimedia Commons'],8:['Exakt position','tillåter överlappning','kan flyttas för att fylla luckan']}}
        for tag, checks in expected.items():
            paragraphs=self._manual_node(tag).text.split(r'\n\n')
            for index, parts in checks.items():
                for part in parts:
                    with self.subTest(tag=tag,paragraph=index+1,part=part): self.assertIn(part,paragraphs[index])
            self.assertNotIn('one undoable selection edit',paragraphs[4])
            self.assertNotIn('fixed at the lower left',paragraphs[1])
        self.assertIn('fäller ihop eller fäller ut panelen.',self._manual_node('sv').text)

if __name__ == '__main__':
    unittest.main()
