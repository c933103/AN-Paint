"""Current Help provider wording and menu contracts; no historical XML snapshots."""
from pathlib import Path
import re
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import current_display
ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KEY='ui_help23'

class HelpCommonsProviderTest(unittest.TestCase):


    def test_help_uses_live_provider_caption_without_requiring_approval_scope(self):
        paths = {'default': catalogues.RES/'values/strings.xml', **catalogues.catalogue_paths()}
        for tag, path in paths.items():
            strings = catalogues.read_strings(path)
            if KEY in strings and 'commons_blank_maps' in strings:
                with self.subTest(tag=tag):
                    self.assertEqual(1, strings[KEY].count(strings['commons_blank_maps']))
                    self.assertFalse(catalogues.placeholders(strings[KEY]))

    def test_locale_specific_provider_caption_punctuation(self):
        for tag, start, end in [('et', '„', '“'), ('fi', '”', '” -valinnan'),
                                 ('vi-Hani', '吧 「', '」'), ('ja', '［', '］があります。')]:
            caption = current_display(tag, 'commons_blank_maps')
            text = current_display(tag, KEY)
            self.assertIn(start + caption + end, text)
        self.assertNotIn(current_display('ja','commons_blank_maps') + '］ があります', current_display('ja', KEY))

    def test_nom_blank_map_label_help_and_encode_reason_agree(self):
        strings = catalogues.read_strings(catalogues.catalogue_paths()['vi-Hani'])
        caption = strings['commons_blank_maps']
        self.assertEqual('Wikimedia Commons · 版圖 𥧪…', caption)
        self.assertEqual(1, strings[KEY].count('「' + caption + '」'))
        self.assertIn('版圖 𥧪', strings['commons_svg_png_encode_failed'])


    def test_default_lists_actual_device_and_four_provider_choices(self):
        strings = catalogues.read_strings(catalogues.RES / 'values/strings.xml')
        self.assertIn('Draw > Insert > Other images contains device files, Catrobat, '
                      'Irasutoya, Openclipart and “Wikimedia Commons · Blank maps…”.', strings[KEY])
        provider = (JAVA / 'IllustrationSource.kt').read_text()
        entries = re.findall(r'^    ([A-Z]+)\("https://', provider, re.M)
        self.assertEqual(['CATROBAT', 'IRASUTOYA', 'OPENCLIPART', 'COMMONS'], entries)
        self.assertIn('COMMONS->ui(R.string.commons_blank_maps)', provider)
        editor = (JAVA / 'ClassicPaintActivity.kt').read_text()
        self.assertIn('val sources=listOf(ui(R.string.ui_from_device34))+IllustrationSource.values().map {it.label}', editor)
        self.assertIn('private fun showHelp() = message(ui(R.string.ui_help23))', editor)
        self.assertIn('ui(R.string.ui_how_to_use) to {showHelp()}', editor)
