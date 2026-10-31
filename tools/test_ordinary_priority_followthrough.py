"""Current count composition and conditional crop semantics, not approval history."""
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
from current_localization_contracts import decode_display


class OrdinaryPriorityFollowthroughTest(unittest.TestCase):
    def test_finite_display_counts_and_conditional_crop_semantics(self):
        paths = catalogues.catalogue_paths()
        es = decode_display(catalogues.read_strings(paths['es-419'])['ui_d_d_px_d_pixels_2f_mp'])
        self.assertIn('Número de píxeles: %3$,d', es)
        for tag, label in [('es-419', 'Número de páginas: %3$d.'), ('eo', 'Nombro de paĝoj: %3$d.'), ('ar', 'عدد الصفحات: %3$d.'), ('pt-BR', 'Número de páginas: %3$d.')]:
            self.assertIn(label, decode_display(catalogues.read_strings(paths[tag])['formats22_page_description']))
        for tag, conditional, old in [('es-419', 'puede mover las imágenes unidas a ellas.', 'reposiciona sus uniones'), ('pt-BR', 'pode mover as imagens conectadas a elas.', 'também reposiciona')]:
            items = ET.parse(paths[tag]).findall("./plurals[@name='ui_crop_preview_images']/item")
            self.assertEqual({'one', 'other'}, {n.get('quantity') for n in items})
            for item in items:
                value = decode_display(item.text)
                self.assertIn(conditional, value)
                self.assertNotIn(old, value)


if __name__ == '__main__':
    unittest.main()
