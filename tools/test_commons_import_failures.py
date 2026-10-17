"""Current Commons application-failure contracts; not Android execution or linguistic acceptance.

Production behavior is exercised by CommonsImportFailureFlowTest. This inexpensive host
check binds its typed producers, UI resource dispatch and complete-value fixture, while
leaving the existing catalogue-completeness gates fully enforced.
"""
from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET
import translation_catalogues as catalogues
import current_localization_contracts as current

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
LOCAL = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
CONTRACT = {
    'NotFilePage': ('commons_metadata_not_file_page', 'Not a Commons file page', 'IllegalArgumentException'),
    'AmbiguousFile': ('commons_metadata_ambiguous_file', 'Commons metadata returned an ambiguous file', 'IOException'),
    'MetadataUnavailable': ('commons_metadata_unavailable', 'Commons file metadata is unavailable', 'IOException'),
    'MetadataOriginalMismatch': ('commons_metadata_original_mismatch', 'Commons attribution does not match the selected original file', 'IOException'),
    'InvalidAttributionPage': ('commons_metadata_invalid_page', 'Invalid Commons attribution page', 'IOException'),
    'FieldTooLarge': ('commons_metadata_field_too_large', 'Commons attribution field exceeds the text limit', 'IOException'),
    'CacheFailed': ('commons_metadata_cache_failed', 'Could not retain Commons attribution', 'IOException'),
    'DownloadOriginalMismatch': ('commons_download_original_mismatch', 'The Commons download redirected to a different original file.', 'IllegalArgumentException'),
    'PngEncodeFailed': ('commons_svg_png_encode_failed', 'Could not encode blank map as PNG', 'IOException'),
}


class CommonsImportFailureContractTest(unittest.TestCase):
    def test_each_reason_has_its_original_exception_category_without_worker_prose(self):
        source = (MAIN / 'CommonsImportFailure.kt').read_text()
        self.assertIn('sealed interface CommonsImportFailure', source)
        self.assertEqual(set(CONTRACT), set(re.findall(r'class (\w+):', source)))
        for kind, (_, english, category) in CONTRACT.items():
            self.assertIn(f'class {kind}: {category}(), CommonsImportFailure', source)
            self.assertNotIn(english, source)

    def test_all_nine_old_literals_have_typed_producers(self):
        metadata = (MAIN / 'CommonsAttribution.kt').read_text()
        gallery = (MAIN / 'MediaGalleryActivity.kt').read_text()
        svg = (MAIN / 'BlankMapSvg.kt').read_text()
        for kind, (_, english, _) in CONTRACT.items():
            source = svg if kind == 'PngEncodeFailed' else gallery if kind == 'DownloadOriginalMismatch' else metadata
            self.assertEqual(1, source.count(f'throw CommonsImportFailure.{kind}()'), kind)
            self.assertNotIn(f'"{english}"', source, kind)
        self.assertIn('if (pages.length() != 1) throw CommonsImportFailure.AmbiguousFile()', metadata)
        self.assertIn('page.optBoolean("missing") || page.optInt("ns", -1) != 6', metadata)
        self.assertIn('if (html.length > MAX_FIELD) throw CommonsImportFailure.FieldTooLarge()', metadata)
        self.assertIn('.commit()) throw CommonsImportFailure.CacheFailed()', metadata)
        self.assertIn('if(!bitmap.compress(Bitmap.CompressFormat.PNG,100,out)) throw CommonsImportFailure.PngEncodeFailed()', svg)
        self.assertIn('finally {bitmap.recycle()}', svg)

    def test_dispatch_is_typed_and_both_calls_stay_inside_alive_ui_guards(self):
        source = (MAIN / 'MediaGalleryActivity.kt').read_text()
        dispatch = source.split('private fun commonsMetadataReason', 1)[1].split('private fun showStatus', 1)[0]
        for kind, (key, _, _) in CONTRACT.items():
            self.assertIn(f'is CommonsImportFailure.{kind} -> R.string.{key}', dispatch)
        self.assertIn('else error.message', dispatch)
        self.assertNotIn('error.message ==', dispatch)
        for marker in ('private fun copyCommonsCredit', 'private fun download'):
            body = source.split(marker, 1)[1].split('catch(error: Exception)', 1)[1]
            callback = body.split('runOnUiThread {if(!isFinishing && !isDestroyed) {', 1)[1].split('}}', 1)[0]
            self.assertIn('commonsMetadataReason(error)', callback)
        self.assertEqual(2, source.count('commonsMetadataReason(error)'))

    def test_provider_source_limits_and_file_cleanup_contracts_remain(self):
        metadata = (MAIN / 'CommonsAttribution.kt').read_text()
        gallery = (MAIN / 'MediaGalleryActivity.kt').read_text()
        for token in ('MAX_RESPONSE = 2 * 1024 * 1024', 'MAX_FIELD = 64 * 1024',
                      '.appendQueryParameter("iiextmetadatalanguage", "en")',
                      'connection.instanceFollowRedirects = false',
                      'finally { connection.disconnect(); active(null) }',
                      'a.path == b.path', 'commons-attribution-v1'):
            self.assertIn(token, metadata)
        self.assertIn('download(uri,page.take(4096),title.take(512)', gallery)
        identity = gallery.index('throw CommonsImportFailure.DownloadOriginalMismatch()')
        self.assertLess(identity, gallery.index('source.inputStream.use'))
        self.assertIn('temporary?.delete();rendered?.delete();downloading=false', gallery)

    def test_default_resource_meanings_are_complete_and_translatable(self):
        nodes = {node.get('name'): node for node in ET.parse(catalogues.RES / 'values/strings.xml').getroot()}
        for key, english, _ in CONTRACT.values():
            self.assertEqual(english, ''.join(nodes[key].itertext()))
            self.assertNotEqual('false', nodes[key].get('translatable'))
            self.assertEqual({}, dict(catalogues.placeholders(english)))

    def test_fixture_binds_every_implemented_catalogue_and_leaves_missing_entries_visible(self):
        fixture = current.fixture('commons_import_failures_current_wording.json')
        expected = fixture['values']
        self.assertEqual({row[0] for row in CONTRACT.values()}, set(expected))
        self.assertEqual(set(expected), set(fixture['constraints']))
        scope = json.loads((ROOT / 'tools/fixtures/current_localization/locale_contract_scope.json').read_text())
        offered = set(catalogues.offered_tags())
        self.assertEqual(offered, set(scope['scoped_tags']) | set(scope['fallback_tags']))
        self.assertEqual(59, len(scope['scoped_tags']))
        self.assertEqual(112, len(scope['fallback_tags']))
        paths = catalogues.catalogue_paths()
        for key, values in expected.items():
            self.assertLessEqual(set(values), offered | {'default'})
            self.assertEqual(catalogues.read_strings(catalogues.RES / 'values/strings.xml')[key], values['default'])
            for tag in offered:
                actual = catalogues.read_strings(paths[tag])
                if tag in values:
                    self.assertEqual(values[tag], actual[key], f'{tag}/{key}')
                    current.require_string(paths[tag].read_text(), key, values[tag], fixture['constraints'][key])
                    self.assertEqual([], catalogues.android_string_errors(values[tag]))
                    self.assertEqual({}, dict(catalogues.placeholders(values[tag])))
                    if not tag.startswith('en-') and tag != 'qaa-Zsye-XV':
                        self.assertNotEqual(values['default'], values[tag], f'{tag}: copied English is not translation')
                else:
                    self.assertNotIn(key, actual, f'{tag}: an implemented value needs a reviewed fixture entry')
                    if tag in scope['scoped_tags']:
                        self.assertTrue(any(key in error for error in catalogues.validate_catalogue(tag, require_complete=True)),
                                        f'{tag}: pending translation must still fail the existing completeness gate')

    def test_real_failure_test_covers_original_conditions_and_test_only_failure_injection(self):
        flow = (LOCAL / 'CommonsImportFailureFlowTest.kt').read_text()
        fixtures = (LOCAL / 'CommonsImportFailureFixtures.kt').read_text()
        for name in ('directMetadataFailuresRetainIOExceptionTypesAndNoWorkerProse',
                     'everyMetadataValidationConditionUsesBothLiveActionsAndRecovers',
                     'cacheCommitFailureIsTypedAndBothActionsKeepEditsThenRecover',
                     'invalidPageIsTypedBeforeConnectingAndBothEntryGuardsMakeZeroRequests',
                     'insertionPageTruncationTriggersTypedPreconditionWithoutMetadataRequestAndRetryWorks',
                     'copyCreditDoesNotTruncateTheValidIndexPage',
                     'redirectedOriginalMismatchFailsBeforeReadingBodyOrMetadataAndRetryWorks',
                     'pngEncodingFalseIsTypedRecyclesBitmapClosesOutputAndInsertionCleansBothFiles',
                     'allTypedReasonsResolveOnlyWhenTheAliveUiCallbackRuns',
                     'destructionDropsEveryQueuedTypedFailure',
                     'duplicateAndDestroyedInFlightMetadataRequestsStayCancelled',
                     'rotationKeepsThePendingMetadataOperationAndItsTypedResult'):
            self.assertIn(f'fun {name}(', flow)
        self.assertIn('override fun commit(): Boolean', fixtures)
        self.assertIn('@Implements(Bitmap::class,callNativeMethodsByDefault=true)', fixtures)
        self.assertIn('Shadow.directlyOn', fixtures)
        self.assertIn('rejectedBitmap!!.isRecycled', flow)
        self.assertIn('rejectedStream!!.write(1)', flow)
        for name in ('CommonsAttribution.kt', 'BlankMapSvg.kt', 'MediaGalleryActivity.kt'):
            self.assertNotIn('CommonsCacheFailureContext', (MAIN / name).read_text())
            self.assertNotIn('CommonsPngFailureShadow', (MAIN / name).read_text())


if __name__ == '__main__':
    unittest.main()
