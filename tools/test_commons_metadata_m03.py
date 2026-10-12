"""M03-only contracts. Host/source success is not Android or language acceptance."""
import hashlib
import json
import pathlib
import unittest
import unicodedata
from unittest.mock import patch

import translation_catalogues as catalogues
from commons_metadata_m04_scope import before_m04_catalogue, before_m04_production
from commons_metadata_m03_scope import (catalogue_fixture, production_fixture,
    before_m03_catalogue, before_m03_production)
from test_translations import SCOPED_TAGS

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
EVIDENCE = ROOT / 'verification/commons-metadata-m03-2026-10-11'
KEY = 'commons_metadata_response_too_large'
DEFAULT = 'Commons metadata exceeds the response limit'


class CommonsMetadataM03Contracts(unittest.TestCase):
    def test_reviewed_three_language_successor_matches_decisions_and_limits(self):
        evidence = ROOT / 'verification/commons-metadata-m03-languages-2026-10-12'
        decisions = json.loads((evidence / 'decisions.json').read_text())
        self.assertEqual({'ain-Kana', 'ain-Latn', 'mnc-Mong'}, set(decisions))
        paths = catalogues.catalogue_paths()
        for tag, decision in decisions.items():
            self.assertEqual('accept_source_assisted_contextual_paraphrase', decision['decision'])
            self.assertEqual('moderate', decision['confidence'])
            self.assertFalse(decision['native_speaker_approval_claimed'])
            self.assertTrue(decision['backtranslation']); self.assertTrue(decision['residual_limit'])
            value = catalogues.read_strings(paths[tag])[KEY]
            self.assertEqual(decision['value'], value)
            self.assertEqual(unicodedata.normalize('NFC', value), value)
            self.assertFalse(any(unicodedata.category(ch).startswith('C') for ch in value))

    def test_reviewed_scripts_are_in_normal_and_double_scale_status_routes(self):
        flow = (ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataResponseLimitFlowTest.kt').read_text()
        readable = flow[flow.index('private fun readable('):]
        for tag in ('ain-Kana', 'ain-Latn', 'mnc-Mong'):
            self.assertIn('"'+tag+'"', readable)
        self.assertIn('representativeM03StatusRetainsFullAccessibleTextAtNormalScale() = readable(1f)', flow)
        self.assertIn('representativeM03StatusRetainsFullAccessibleTextAtDoubleScale() = readable(2f)', flow)

    def test_only_one_message_added_to_default_and_exact_59_catalogues(self):
        data = catalogue_fixture()
        self.assertEqual(KEY, data['key']); self.assertEqual(DEFAULT, data['default'])
        self.assertEqual({'default'} | SCOPED_TAGS, {e['tag'] for e in data['entries']})
        self.assertEqual(60, len(data['entries']))
        self.assertEqual(DEFAULT, catalogues.read_strings(catalogues.RES/'values/strings.xml')[KEY])
        for row in data['entries']:
            text = (ROOT / row['path']).read_text()
            text = before_m04_catalogue(row['path'], text) if '/res/' in row['path'] else before_m04_production(row['path'], text)
            self.assertEqual(row['before_sha256'], hashlib.sha256(before_m03_catalogue(row['path'], text).encode()).hexdigest())
            self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
            actual = catalogues.read_strings(ROOT / row['path'])[KEY]
            self.assertEqual({}, catalogues.placeholders(actual)); self.assertIn('Commons', actual)
            self.assertEqual([], catalogues.android_string_errors(actual))
            self.assertEqual([], catalogues.format_string_errors(actual))
            if row['tag'] != 'default' and not row['tag'].startswith('en-'):
                self.assertNotEqual(DEFAULT, actual)

    def test_all_140_tags_have_individual_dispositions_and_81_explicit_fallbacks(self):
        data = json.loads((EVIDENCE / 'all-language-dispositions.json').read_text())
        rows = data['dispositions']
        self.assertEqual(140, len(rows)); self.assertEqual(set(catalogues.offered_tags()), {r['tag'] for r in rows})
        self.assertEqual(59, sum(r['value'] is not None for r in rows))
        self.assertEqual(set(catalogues.offered_tags()) - SCOPED_TAGS, set(data['fallback_tags']))
        self.assertEqual(81, len(data['fallback_tags']))
        paths = catalogues.catalogue_paths()
        for row in rows:
            self.assertEqual('not-established', row['linguistic_acceptance'])
            self.assertTrue(row['review_limit'])
            if row['tag'] not in SCOPED_TAGS:
                self.assertEqual('missing-key-default-English-fallback-open', row['disposition'])
                self.assertNotIn(KEY, catalogues.read_strings(paths[row['tag']]))
            else:
                self.assertEqual(row['value'], catalogues.read_strings(paths[row['tag']])[KEY])
                self.assertTrue(row['rationale']); self.assertTrue(row['confidence'])

    def test_every_current_disposition_and_present_entry_is_checked_even_when_completeness_fails(self):
        data = json.loads((EVIDENCE / 'all-language-dispositions.json').read_text())
        rows = data['dispositions']; paths = catalogues.catalogue_paths()
        self.assertEqual(140, len(rows)); self.assertEqual(set(catalogues.offered_tags()), {r['tag'] for r in rows})
        unresolved = {r['tag'] for r in rows if r['tag'] in SCOPED_TAGS and r['value'] is None}
        self.assertEqual(unresolved, set(data['unresolved_scoped_tags']))
        self.assertEqual(set(catalogues.offered_tags()) - SCOPED_TAGS, set(data['fallback_tags']))
        self.assertEqual(81, len(data['fallback_tags']))
        for row in rows:
            self.assertEqual('not-established', row['linguistic_acceptance'])
            self.assertTrue(row['review_limit']); self.assertTrue(row['rationale']); self.assertTrue(row['confidence'])
            actual = catalogues.read_strings(paths[row['tag']])
            if row['value'] is None:
                self.assertNotIn(KEY, actual)
                self.assertEqual('unresolved-scoped-proposal-default-English-fallback-open' if row['tag'] in SCOPED_TAGS
                                 else 'missing-key-default-English-fallback-open', row['disposition'])
            else:
                self.assertIn(row['tag'], SCOPED_TAGS)
                self.assertEqual(row['value'], actual[KEY])
        entries = catalogue_fixture()['entries']
        self.assertEqual({'default'} | (SCOPED_TAGS - unresolved), {r['tag'] for r in entries})
        self.assertEqual(len(entries), len({r['tag'] for r in entries}))
        for row in entries:
            text = (ROOT / row['path']).read_text()
            text = before_m04_catalogue(row['path'], text) if '/res/' in row['path'] else before_m04_production(row['path'], text)
            self.assertEqual(row['before_sha256'], hashlib.sha256(before_m03_catalogue(row['path'], text).encode()).hexdigest())
            self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
            actual = catalogues.read_strings(ROOT / row['path'])[KEY]
            self.assertIn('Commons', actual); self.assertEqual({}, catalogues.placeholders(actual))
            self.assertEqual([], catalogues.android_string_errors(actual)); self.assertEqual([], catalogues.format_string_errors(actual))
            if row['tag'] != 'default' and not row['tag'].startswith('en-'):
                self.assertNotEqual(DEFAULT, actual)

    def test_exact_two_file_production_delta_preserves_all_other_reasons_and_behavior(self):
        entries = production_fixture()['entries']
        self.assertEqual(2, len(entries))
        for row in entries:
            text = (ROOT / row['path']).read_text()
            text = before_m04_catalogue(row['path'], text) if '/res/' in row['path'] else before_m04_production(row['path'], text)
            self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
            original = before_m03_production(row['path'], text)
            self.assertEqual(row['before_sha256'], hashlib.sha256(original.encode()).hexdigest())
        producer = before_m04_production((JAVA / 'CommonsAttribution.kt').relative_to(ROOT).as_posix(), (JAVA / 'CommonsAttribution.kt').read_text())
        self.assertIn('class ResponseLimitException: IOException()', producer)
        self.assertIn('if (bytes.size().toLong() + count > MAX_RESPONSE) throw ResponseLimitException()', producer)
        self.assertNotIn(DEFAULT, producer)
        for original in ['private const val MAX_RESPONSE = 2 * 1024 * 1024',
                         'require(json.length <= MAX_RESPONSE)',
                         'if (status != 200) throw IOException("Commons metadata: HTTP $status")',
                         'if (html.length > MAX_FIELD) throw IOException("Commons attribution field exceeds the text limit")',
                         'finally { connection.disconnect(); active(null) }']:
            self.assertIn(original, producer)
        gallery = before_m04_production((JAVA / 'MediaGalleryActivity.kt').relative_to(ROOT).as_posix(), (JAVA / 'MediaGalleryActivity.kt').read_text())
        self.assertEqual(2, gallery.count('commonsMetadataReason(error)'))
        self.assertIn('if(error is CommonsAttribution.ResponseLimitException) ui(R.string.'+KEY+')', gallery)
        self.assertIn('else error.message', gallery)
        self.assertEqual(2, gallery.count('runOnUiThread {if(!isFinishing && !isDestroyed) {\n                    val reason='))
        self.assertNotIn('error.message ==', gallery)
        self.assertNotIn('error.message==', gallery)

    def test_all_catalogues_reject_missing_duplicated_changed_and_unrelated_edits(self):
        for row in catalogue_fixture()['entries']:
            text = (ROOT / row['path']).read_text()
            text = before_m04_catalogue(row['path'], text) if '/res/' in row['path'] else before_m04_production(row['path'], text)
            for bad in ('', row['line']*2, row['line'].replace('Commons', 'CommonX')):
                with self.subTest(tag=row['tag'], mutation=bad):
                    with self.assertRaises(AssertionError):
                        before_m03_catalogue(row['path'], text.replace(row['line'], bad, 1))
            changed = text.replace('</resources>', '    <string name="unrelated">oops</string>\n</resources>')
            self.assertNotEqual(row['before_sha256'], hashlib.sha256(before_m03_catalogue(row['path'], changed).encode()).hexdigest())

    def test_production_reversal_rejects_broader_or_untyped_changes(self):
        for row in production_fixture()['entries']:
            text = (ROOT / row['path']).read_text()
            text = before_m04_catalogue(row['path'], text) if '/res/' in row['path'] else before_m04_production(row['path'], text)
            for edit in row['edits']:
                for replacement in ('', edit['after']*2, edit['before']):
                    with self.subTest(path=row['path'], replacement=replacement):
                        with self.assertRaises(AssertionError):
                            before_m03_production(row['path'], text.replace(edit['after'], replacement, 1))
            self.assertNotEqual(row['before_sha256'], hashlib.sha256(before_m03_production(row['path'], text+'\n// unrelated\n').encode()).hexdigest())

    def test_resource_and_production_pins_reject_fixture_corruption(self):
        for filename, load in [('commons_metadata_response_limit_scope.json', catalogue_fixture),
                               ('commons_metadata_m03_production_scope.json', production_fixture)]:
            raw = (ROOT / 'tools/fixtures' / filename).read_bytes()
            with patch.object(pathlib.Path, 'read_bytes', return_value=raw+b' '):
                with self.assertRaises(AssertionError): load()

    def test_android_contracts_cover_stream_boundaries_both_real_routes_and_late_results(self):
        tests = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
        flow = (tests/'CommonsMetadataResponseLimitFlowTest.kt').read_text()
        for token in ['IllustrationPage.USE_SCHEME', 'GalleryPage.CREDIT_SCHEME', 'shouldOverrideUrlLoading',
                      'exactTwoMiBParsesButOneExtraByteThrowsOnlyTypedIOExceptionAndClosesStream',
                      'parserPreconditionAndFieldLimitRemainSeparateUnchangedFailures',
                      'unrelatedStreamFailureAndCancellationStillCloseAndClearActiveConnection',
                      'bothActionsLocalizeTypedMetadataFailureKeepStateAndRetryAtExactBoundary',
                      'typedFailurePreservesAnUnacceptedCreditDraftForBothActions',
                      'queuedTypedFailureResolvesResourcesOnlyWhenTheAliveUiCallbackRuns',
                      'untypedLimitLookingAndPercentNewlineDetailsStayVerbatimOnBothActions',
                      'duplicateAndDestroyedActivitiesDoNotPublishLateTypedFailuresForEitherAction',
                      'destroyedActivityDropsAlreadyQueuedSuccessAndRemovesReturnedFile',
                      'representativeM03StatusRetainsFullAccessibleTextAtDoubleScale',
                      'val limit=2*1024*1024', 'listOf(limit,limit+1)', 'paddedMetadata(limit+1)',
                      'assertTrue(input.closed)', 'assertEquals(before,files(activity))']:
            self.assertIn(token, flow)
        self.assertNotIn('callInstanceMethod', flow)
        self.assertIn('@Config(qualifiers="w320dp-h640dp-port-xhdpi",fontScale=2f)', flow)
        self.assertNotIn('xhdpi-fontScale', flow)
        resolved = (tests/'CommonsMetadataResponseLimitTranslationTest.kt').read_text()
        self.assertIn('@Config(sdk=[30,35])', resolved)
        self.assertIn('AppLanguage.select(context,tag)', resolved)
        self.assertIn('"ko-Kore-KR-anpaint"', resolved)
        self.assertIn('assertEquals(81,fallbacks)', resolved)
        for row in catalogue_fixture()['entries'][1:]:
            value = catalogues.read_strings(ROOT/row['path'])[KEY]
            expected = json.dumps(row['tag'])+' to '+json.dumps(value,ensure_ascii=False).replace('$','\\$')
            self.assertIn(expected, resolved)


if __name__ == '__main__': unittest.main()
