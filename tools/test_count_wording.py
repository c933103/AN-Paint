"""Reviewed count-invariant labels; actual chooser/assembly tests live with Android tests."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / 'Paintroid/src/main/res'
ENGLISH = {
    'ui_d_d_px_d_pixels_2f_mp': '%1$d × %2$d px · Pixel count: %3$,d (%4$.2f MP)',
    'formats22_page_description': r'%1$s · %2$s\nNumber of pages: %3$d. Choose one page to edit as an image.',
    'ui_you_can_add_more_images_select_fewer_files': 'Number of images you can still add: %1$s. Select fewer files.',
    'ui_rendering_images': 'Images processed: %1$s / %2$s…',
}
FRENCH = {
    'ui_d_d_px_d_pixels_2f_mp': '%1$d × %2$d px · Nombre de pixels : %3$,d (%4$.2f MP)',
    'formats22_page_description': r'%1$s · %2$s\nNombre de pages : %3$d. Choisissez une page à modifier comme image.',
    'ui_an_paint_image_assembly_20_images_placed': r'AN Paint · Assemblage d’images\nImages : %1$s/20 · Images placées : %2$s',
    'ui_you_can_add_more_images_select_fewer_files': 'Nombre d’images pouvant encore être ajoutées : %1$s. Sélectionnez moins de fichiers.',
    'ui_rendering_images': 'Images traitées : %1$s / %2$s…',
}


def strings(folder):
    return {item.get('name'): item.text for item in ET.parse(RES / folder / 'strings.xml').getroot()}


class CountWordingTest(unittest.TestCase):
    def test_english_overrides_do_not_restore_the_singular_defect(self):
        folders = ['values', 'values-b+en+001', 'values-b+en+XV', 'values-b+qaa+Zsye+XV']
        folders += [f'values-en-r{region}' for region in ['AU', 'CA', 'GB', 'IN', 'SG', 'US']]
        for folder in folders:
            for key, expected in ENGLISH.items():
                with self.subTest(folder=folder, key=key):
                    prefixes = {'ui_you_can_add_more_images_select_fewer_files': '📁 ', 'ui_d_d_px_d_pixels_2f_mp': '🧪 '}
                    prefix = prefixes.get(key, '🖼️ ') if folder == 'values-b+qaa+Zsye+XV' else ''
                    self.assertEqual(prefix + expected, strings(folder)[key])

    def test_french_complete_reviewed_values_and_argument_types(self):
        actual = strings('values-fr')
        for key, expected in FRENCH.items():
            with self.subTest(key=key):
                self.assertEqual(expected, actual[key])
                self.assertEqual(re.findall(r'%\d+\$[,.\d]*[sdf]', strings('values')[key]),
                                 re.findall(r'%\d+\$[,.\d]*[sdf]', actual[key]))

    def test_japanese_page_count_keeps_its_valid_invariant_wording(self):
        self.assertEqual(r'%1$s · %2$s\n全%3$dページ。画像として編集するページを1つ選んでください。',
                         strings('values-ja')['formats22_page_description'])


if __name__ == '__main__':
    unittest.main()
