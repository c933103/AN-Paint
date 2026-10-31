"""Current resource semantics; historical approval snapshots are not active text freezes."""
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues


from current_localization_contracts import current_display
from test_danish_norwegian_p0_wording import full_format_tokens


class CatalanRomanianImportWordingTests(unittest.TestCase):

    def test_current_product_and_numeric_literals_preserve_consumer_limits(self):
        for tag in ('ca', 'ro'):
            for key, literals in {'formats22_animation_message': ['AN Paint'],
                                  'formats22_animation_unknown': ['AN Paint'],
                                  'formats22_animation_poster': ['PNG'],
                                  'formats22_pdf_raster_hint': ['PDF', '144', 'dpi'],
                                  'save20_gif_description': ['GIF', '256'],
                                  'save20_unsupported_image_colour': ['AN Paint', 'sRGB', 'PNG']}.items():
                for literal in literals:self.assertIn(literal, current_display(tag, key))

if __name__ == '__main__':
    unittest.main()
