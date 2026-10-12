"""M02-only contracts. Source/resource success is not Android or language acceptance."""
from commons_metadata_m04_scope import before_m04_catalogue
from commons_metadata_m04_composition_scope import before_m04_composed_production

import hashlib
import json
import pathlib
import unittest
from unittest.mock import patch

import translation_catalogues as catalogues
from hungarian_attribution_c05_scope import before_c05
from commons_metadata_m02_scope import fixture, before_m02_catalogue, before_m02_producer
from commons_metadata_m03_scope import before_m03_catalogue
from commons_metadata_composition_scope import without_m03_production
from test_translations import SCOPED_TAGS

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KEY = 'commons_metadata_http_error'

class CommonsMetadataM02Contracts(unittest.TestCase):
    def test_only_one_message_added_to_default_and_exact_59_catalogues(self):
        data = fixture()
        self.assertEqual(KEY, data['key'])
        self.assertEqual({'default'} | SCOPED_TAGS, {e['tag'] for e in data['entries']})
        self.assertEqual(60, len(data['entries']))
        for row in data['entries']:
            text = (ROOT / row['path']).read_text()
            text = (before_m04_catalogue(row['path'], text) if row['path'].endswith('/strings.xml')
                    else before_m04_composed_production(row['path'], text))
            text = (before_m03_catalogue(row['path'], text) if row['path'].endswith('/strings.xml')
                    else without_m03_production(row['path'], text))
            # C05's exact 17 replacements are independent of this one addition.
            historical = before_c05(row['path'], before_m02_catalogue(row['path'], text))
            self.assertEqual(row['before_sha256'], hashlib.sha256(historical.encode()).hexdigest())
            actual = catalogues.read_strings(ROOT / row['path'])[KEY]
            self.assertEqual({'%1$s': 1}, catalogues.placeholders(actual))
            self.assertIn('Commons', actual); self.assertIn('HTTP %1$s', actual)
            self.assertEqual([], catalogues.android_string_errors(actual))
            self.assertEqual([], catalogues.format_string_errors(actual))
            if row['tag'] != 'default' and not row['tag'].startswith('en-'):
                self.assertNotEqual(data['default'], actual)

    def test_all_140_tags_have_individual_dispositions_without_filling_81_fallbacks(self):
        data = json.loads((ROOT / 'verification/commons-metadata-m02-2026-10-11/all-language-dispositions.json').read_text())
        rows = data['dispositions']
        self.assertEqual(140, len(rows)); self.assertEqual(set(catalogues.offered_tags()), {r['tag'] for r in rows})
        self.assertEqual(59, sum(r['value'] is not None for r in rows))
        paths = catalogues.catalogue_paths()
        for row in rows:
            self.assertEqual('not-established', row['linguistic_acceptance'])
            if row['tag'] not in SCOPED_TAGS:
                self.assertEqual('missing-key-default-English-fallback-open', row['disposition'])
                self.assertNotIn(KEY, catalogues.read_strings(paths[row['tag']]))
            else:
                self.assertEqual(row['value'], catalogues.read_strings(paths[row['tag']])[KEY])

    def test_exact_two_file_production_delta_preserves_all_other_reasons_and_behavior(self):
        raw = (ROOT / 'tools/fixtures/commons_metadata_m02_production_scope.json').read_bytes()
        self.assertEqual(PRODUCTION_PIN, hashlib.sha256(raw).hexdigest())
        entries = json.loads(raw)['entries']
        self.assertEqual(2, len(entries))
        for row in entries:
            text = (ROOT / row['path']).read_text()
            text = (before_m04_catalogue(row['path'], text) if row['path'].endswith('/strings.xml')
                    else before_m04_composed_production(row['path'], text))
            text = (before_m03_catalogue(row['path'], text) if row['path'].endswith('/strings.xml')
                    else without_m03_production(row['path'], text))
            self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
            for edit in reversed(row['edits']):
                self.assertEqual(1, text.count(edit['after']))
                text = text.replace(edit['after'], edit['before'], 1)
            self.assertEqual(row['before_sha256'], hashlib.sha256(text.encode()).hexdigest())
        producer = (JAVA / 'CommonsAttribution.kt').read_text()
        self.assertIn('if (status != 200) throw HttpException(status)', producer)
        self.assertIn('class HttpException(val status: Int): IOException()', producer)
        self.assertNotIn('Commons metadata: HTTP $status', producer)
        self.assertIn('.appendQueryParameter("iiextmetadatalanguage", "en")', producer)
        self.assertIn('connection.instanceFollowRedirects = false', producer)
        gallery = (JAVA / 'MediaGalleryActivity.kt').read_text()
        self.assertEqual(2, gallery.count('commonsMetadataReason(error)'))
        self.assertIn('if(error is CommonsAttribution.HttpException) ui(R.string.commons_metadata_http_error,error.status.toString())', gallery)
        self.assertIn('else error.message', gallery)
        self.assertEqual(2, gallery.count('runOnUiThread {if(!isFinishing && !isDestroyed) {\n                    val reason='))

    def test_rejects_missing_duplicated_changed_and_unrelated_catalogue_edits(self):
        for row in fixture()['entries']:
            text = (ROOT / row['path']).read_text()
            text = (before_m04_catalogue(row['path'], text) if row['path'].endswith('/strings.xml')
                    else before_m04_composed_production(row['path'], text))
            text = (before_m03_catalogue(row['path'], text) if row['path'].endswith('/strings.xml')
                    else without_m03_production(row['path'], text))
            for bad in ('', row['line']*2, row['line'].replace('HTTP ', 'HTTPX ')):
                with self.subTest(tag=row['tag'], mutation=bad):
                    with self.assertRaises(AssertionError):
                        before_m02_catalogue(row['path'], text.replace(row['line'], bad, 1))
            changed = text.replace('</resources>', '    <string name="unrelated">oops</string>\n</resources>')
            self.assertNotEqual(row['before_sha256'], hashlib.sha256(before_m02_catalogue(row['path'], changed).encode()).hexdigest())

    def test_fixture_and_producer_controls_reject_broader_or_untyped_changes(self):
        raw = (ROOT / 'tools/fixtures/commons_metadata_http_scope.json').read_bytes()
        with patch.object(pathlib.Path, 'read_bytes', return_value=raw+b' '):
            with self.assertRaises(AssertionError): fixture()
        path = 'Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt'
        source = (ROOT/path).read_bytes()
        for old, new in [(b'throw HttpException(status)', b'throw IOException(status.toString())'),
                         (b'class HttpException(val status: Int): IOException()', b'class HttpException(val status: Int): Exception()')]:
            with self.assertRaises(AssertionError): before_m02_producer(path, source.replace(old,new))

    def test_android_contracts_cover_both_routes_and_exact_resources(self):
        tests = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
        flow = (tests/'CommonsMetadataHttpFlowTest.kt').read_text()
        for token in ['IllustrationPage.USE_SCHEME', 'GalleryPage.CREDIT_SCHEME', 'shouldOverrideUrlLoading',
                      'everyNon200StatusHasOnlyTypedAsciiData', 'bothActionsLocalizeTypedMetadataFailure',
                      'untypedHttpLookingAndPercentNewline', 'duplicateAndDestroyedActivities',
                      'representativeM02StatusRetainsFullAccessibleTextAtDoubleScale',
                      'assertFalse(requests.last().read)', 'assertEquals(before,files(activity))']:
            self.assertIn(token, flow)
        self.assertIn('@Config(qualifiers="w320dp-h640dp-port-xhdpi",fontScale=2f)', flow)
        self.assertNotIn('xhdpi-fontScale', flow)
        resolved = (tests/'CommonsMetadataHttpTranslationTest.kt').read_text()
        self.assertIn('@Config(sdk=[30,35])', resolved)
        self.assertIn('AppLanguage.select(context,tag)', resolved)
        self.assertIn('"ko-Kore-KR-anpaint"', resolved)
        self.assertIn('assertEquals(81,fallbacks)', resolved)
        for row in fixture()['entries'][1:]:
            value = catalogues.read_strings(ROOT/row['path'])[KEY]
            expected = json.dumps(row['tag'])+' to '+json.dumps(value,ensure_ascii=False).replace('$','\\$')
            self.assertIn(expected, resolved)

PRODUCTION_PIN = '2b740b35f1607602ba9520dda8e42a899a67880e06d85c0732fb862e7af2ec6c'
if __name__ == '__main__': unittest.main()
