"""Current Help provider wording and menu contracts; no historical XML snapshots."""
from pathlib import Path
import re
import unittest
import translation_catalogues as catalogues
from current_localization_contracts import fixture, require_string, require_locale_scope
from test_translations import SCOPED_TAGS
ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KEY='ui_help23'

class HelpCommonsProviderTest(unittest.TestCase):
    def test_provider_captions_segments_and_boundaries_match_current_help(self):
        data=fixture('help_commons_provider_current_contract.json')
        _, fallback = require_locale_scope(fixture('locale_contract_scope.json'), SCOPED_TAGS, catalogues.offered_tags())
        paths={'default': catalogues.RES/'values/strings.xml', **catalogues.catalogue_paths()}
        self.assertEqual(['cs', 'sv'], data['additional_reviewed_tags'])
        self.assertEqual({'default'}|SCOPED_TAGS|{'cs', 'sv'},set(data['provider_segments']))
        for tag,segment in data['provider_segments'].items():
            with self.subTest(tag=tag):
                strings=catalogues.read_strings(paths[tag]);value=strings[KEY]
                caption=data['values']['commons_blank_maps'][tag]
                require_string(paths[tag].read_text(),'commons_blank_maps',caption)
                self.assertEqual(1,value.count(caption))
                self.assertEqual(1,value.count(segment))
                self.assertIn(data['caption_boundary_fragments'][tag],value)
                self.assertEqual({},catalogues.placeholders(value))
                self.assertEqual([],catalogues.android_string_errors(value))
                self.assertEqual([],catalogues.format_string_errors(value,False))
        for tag,path in paths.items():
            if tag in fallback - {'cs', 'sv'}:
                self.assertNotIn(KEY,catalogues.read_strings(path))

    def test_source_assisted_punctuation_corrections(self):
        rows=fixture('help_commons_provider_current_contract.json')['provider_segments']
        self.assertTrue(rows['et'].endswith('„Wikimedia Commons · Kontuurkaardid…“'))
        self.assertTrue(rows['fi'].endswith('”Wikimedia Commons · Ääriviivakartat…” -valinnan'))
        self.assertTrue(rows['vi-Hani'].endswith('吧 「Wikimedia Commons · 版圖 𥧪…」'))

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

    def test_complete_japanese_provider_sentence_joins_label_and_particle(self):
        help_text = catalogues.read_strings(catalogues.RES / 'values-ja/strings.xml')[KEY]
        expected = ('［描画］→［挿入］→［ほかの画像］には、端末内ファイル、Catrobat、'
                    'いらすとや、Openclipart、［Wikimedia Commons · 白地図…］があります。')
        self.assertIn(expected, help_text)
        self.assertNotIn('白地図…］ があります', help_text)

    def test_android_resource_test_uses_same_explicit_scope(self):
        source = (ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsHelpProviderTranslationTest.kt').read_text()
        tags = re.search(r'private val scopedTags=listOf\((.*?)\n    \)', source, re.S).group(1)
        self.assertEqual(set(SCOPED_TAGS) | {'cs', 'sv'}, set(re.findall(r'"([\w-]+)"', tags)))
        self.assertIn('EditorTestNavigation.command(activity,"File",7)', source)
        self.assertIn('ShadowAlertDialog.getLatestAlertDialog()', source)
