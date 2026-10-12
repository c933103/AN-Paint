"""M04 query-failure contracts; host/source checks do not certify language or Android UI."""
import hashlib
import json
import pathlib
import unittest
from unittest.mock import patch

import translation_catalogues as catalogues
from test_translations import SCOPED_TAGS
from commons_metadata_m04_scope import (catalogue_fixture, production_fixture, test_fixture,
    before_m04_catalogue, before_m04_production, before_m04_test)
from commons_metadata_m03_scope import (catalogue_fixture as m03_catalogue_fixture,
    production_fixture as m03_production_fixture, before_m03_catalogue, before_m03_production)

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'verification/commons-metadata-m04-2026-10-12'
KEY = 'commons_metadata_query_failed'
DEFAULT = 'Commons metadata query failed'


class CommonsMetadataM04Contracts(unittest.TestCase):
    def test_exact_default_plus_59_message_additions_preserve_all_previous_catalogue_bytes(self):
        data = catalogue_fixture()
        self.assertEqual(KEY, data['key']); self.assertEqual(DEFAULT, data['default'])
        self.assertEqual({'default'} | SCOPED_TAGS, {row['tag'] for row in data['entries']})
        self.assertEqual(60, len(data['entries']))
        for row in data['entries']:
            text = (ROOT / row['path']).read_text()
            with self.subTest(tag=row['tag']):
                self.assertEqual(row['before_sha256'], hashlib.sha256(before_m04_catalogue(row['path'], text).encode()).hexdigest())
                self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
                value = catalogues.read_strings(ROOT / row['path'])[KEY]
                self.assertEqual({}, catalogues.placeholders(value)); self.assertIn('Commons', value)
                self.assertEqual([], catalogues.android_string_errors(value))
                self.assertEqual([], catalogues.format_string_errors(value))
                if row['tag'] == 'default' or row['tag'].startswith('en-'):
                    self.assertEqual(DEFAULT, value)
                else:
                    self.assertNotEqual(DEFAULT, value)

    def test_every_present_value_and_unresolved_tag_matches_independent_review(self):
        data = json.loads((EVIDENCE / 'all-language-dispositions.json').read_text())
        decisions = json.loads((EVIDENCE / 'linguistic-review/successor-recovered/decisions-v4.json').read_text())
        paths = catalogues.catalogue_paths(); rows = data['dispositions']
        self.assertEqual(SCOPED_TAGS,set(decisions))
        self.assertEqual(140,len(rows)); self.assertEqual(set(catalogues.offered_tags()),{row['tag'] for row in rows})
        implemented = {tag for tag, decision in decisions.items() if decision['value'] is not None}
        unresolved = SCOPED_TAGS - implemented
        self.assertEqual(unresolved,set(data['unresolved_scoped_tags']))
        self.assertEqual(set(catalogues.offered_tags())-SCOPED_TAGS,set(data['fallback_tags']))
        self.assertEqual(81,len(data['fallback_tags']))
        self.assertEqual({'default'}|implemented,{row['tag'] for row in catalogue_fixture()['entries']})
        for row in catalogue_fixture()['entries']:
            text=(ROOT/row['path']).read_text()
            self.assertEqual(row['before_sha256'],hashlib.sha256(before_m04_catalogue(row['path'],text).encode()).hexdigest())
            self.assertEqual(row['after_sha256'],hashlib.sha256(text.encode()).hexdigest())
            value=catalogues.read_strings(ROOT/row['path'])[KEY]
            self.assertEqual(DEFAULT if row['tag']=='default' else decisions[row['tag']]['value'],value)
            self.assertIn('Commons',value);self.assertEqual({},catalogues.placeholders(value))
            self.assertEqual([],catalogues.android_string_errors(value));self.assertEqual([],catalogues.format_string_errors(value))
        for row in rows:
            self.assertEqual('not-established',row['linguistic_acceptance'])
            self.assertTrue(row['review_limit']);self.assertTrue(row['rationale']);self.assertTrue(row['confidence'])
            if row['tag'] in implemented:
                self.assertEqual(decisions[row['tag']]['value'],row['value'])
                self.assertEqual(row['value'],catalogues.read_strings(paths[row['tag']])[KEY])
            else:
                self.assertIsNone(row['value']);self.assertNotIn(KEY,catalogues.read_strings(paths[row['tag']]))
                expected='unresolved-scoped-proposal-default-English-fallback-open' if row['tag'] in unresolved else 'missing-key-default-English-fallback-open'
                self.assertEqual(expected,row['disposition'])

    def test_all_140_individual_dispositions_retain_81_open_fallbacks(self):
        data = json.loads((EVIDENCE / 'all-language-dispositions.json').read_text())
        rows = data['dispositions']; paths = catalogues.catalogue_paths()
        self.assertEqual(140, len(rows)); self.assertEqual(set(catalogues.offered_tags()), {row['tag'] for row in rows})
        self.assertEqual(set(catalogues.offered_tags()) - SCOPED_TAGS, set(data['fallback_tags']))
        self.assertEqual(81, len(data['fallback_tags']))
        self.assertEqual(59, sum(row['value'] is not None for row in rows))
        for row in rows:
            with self.subTest(tag=row['tag']):
                self.assertEqual('not-established', row['linguistic_acceptance'])
                self.assertTrue(row['review_limit']); self.assertTrue(row['rationale']); self.assertTrue(row['confidence'])
                if row['tag'] in SCOPED_TAGS:
                    self.assertEqual(row['value'], catalogues.read_strings(paths[row['tag']])[KEY])
                    self.assertTrue(row['backtranslation'])
                else:
                    self.assertEqual('missing-key-default-English-fallback-open', row['disposition'])
                    self.assertIsNone(row['value']); self.assertNotIn(KEY, catalogues.read_strings(paths[row['tag']]))

    def test_exact_two_file_production_change_keeps_the_query_trigger_and_untyped_details(self):
        data = production_fixture()
        self.assertEqual(2, len(data['entries']))
        for row in data['entries']:
            text = (ROOT / row['path']).read_text()
            self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
            self.assertEqual(row['before_sha256'], hashlib.sha256(before_m04_production(row['path'], text).encode()).hexdigest())
        java = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
        producer = (java / 'CommonsAttribution.kt').read_text()
        self.assertIn('class QueryFailureException: IOException()', producer)
        self.assertIn('if (root.has("error")) throw QueryFailureException()', producer)
        self.assertNotIn(DEFAULT, producer)
        for token in ['private const val MAX_RESPONSE = 2 * 1024 * 1024', 'private const val MAX_FIELD = 64 * 1024',
                      'require(json.length <= MAX_RESPONSE)', 'appendQueryParameter("iiextmetadatalanguage", "en")',
                      'if (status != 200) throw IOException("Commons metadata: HTTP $status")',
                      'if (bytes.size().toLong() + count > MAX_RESPONSE) throw ResponseLimitException()',
                      'finally { connection.disconnect(); active(null) }']:
            self.assertIn(token, producer)
        gallery = (java / 'MediaGalleryActivity.kt').read_text()
        self.assertIn('else if(error is CommonsAttribution.QueryFailureException) ui(R.string.' + KEY + ')', gallery)
        self.assertEqual(2, gallery.count('commonsMetadataReason(error)'))
        self.assertEqual(2, gallery.count('runOnUiThread {if(!isFinishing && !isDestroyed) {\n                    val reason='))
        self.assertIn('else error.message', gallery)
        self.assertNotIn('error.message ==', gallery); self.assertNotIn('error.message==', gallery)

    def test_existing_query_expectation_is_the_only_prior_kotlin_test_change(self):
        rows = test_fixture()['entries']
        self.assertEqual(1, len(rows))
        for row in rows:
            text = (ROOT / row['path']).read_text()
            self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
            self.assertEqual(row['before_sha256'], hashlib.sha256(before_m04_test(row['path'], text).encode()).hexdigest())
        preserved = json.loads((EVIDENCE / 'preserved-baseline.json').read_text())
        for path, digest in preserved['untouched_paths'].items():
            self.assertEqual(digest, hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), path)

    def test_original_m03_pins_and_endpoints_still_hold_after_only_the_m04_reversal(self):
        for fixture, reversal, old_reversal in [(m03_catalogue_fixture, before_m04_catalogue, before_m03_catalogue),
                                               (m03_production_fixture, before_m04_production, before_m03_production)]:
            for row in fixture()['entries']:
                text = reversal(row['path'], (ROOT / row['path']).read_text())
                self.assertEqual(row['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
                self.assertEqual(row['before_sha256'], hashlib.sha256(old_reversal(row['path'], text).encode()).hexdigest())

    def test_all_catalogues_reject_removed_duplicated_corrupted_and_unrelated_changes(self):
        for row in catalogue_fixture()['entries']:
            text = (ROOT / row['path']).read_text()
            for replacement in ['', row['line'] * 2, row['line'].replace('Commons', 'CommonX')]:
                with self.subTest(tag=row['tag'], mutation=replacement), self.assertRaises(AssertionError):
                    before_m04_catalogue(row['path'], text.replace(row['line'], replacement, 1))
            changed = text.replace('</resources>', '    <string name="unrelated">oops</string>\n</resources>')
            self.assertNotEqual(row['before_sha256'], hashlib.sha256(before_m04_catalogue(row['path'], changed).encode()).hexdigest())

    def test_production_and_test_reversals_reject_wider_changes_and_missing_substitutions(self):
        for fixture, reverse in [(production_fixture, before_m04_production), (test_fixture, before_m04_test)]:
            for row in fixture()['entries']:
                text = (ROOT / row['path']).read_text()
                for edit in row['edits']:
                    for replacement in ['', edit['after'] * 2, edit['before']]:
                        with self.subTest(path=row['path'], replacement=replacement), self.assertRaises(AssertionError):
                            reverse(row['path'], text.replace(edit['after'], replacement, 1))
                self.assertNotEqual(row['before_sha256'], hashlib.sha256(reverse(row['path'], text+'\n// unrelated\n').encode()).hexdigest())

    def test_all_three_scope_pins_reject_fixture_corruption(self):
        for filename, load in [('commons_metadata_query_failure_scope.json', catalogue_fixture),
                               ('commons_metadata_m04_production_scope.json', production_fixture),
                               ('commons_metadata_m04_test_scope.json', test_fixture)]:
            raw = (ROOT / 'tools/fixtures' / filename).read_bytes()
            with patch.object(pathlib.Path, 'read_bytes', return_value=raw + b' '), self.assertRaises(AssertionError):
                load()

    def test_android_tests_cover_real_condition_both_routes_locale_resolution_and_lifecycle(self):
        tests = ROOT / 'Paintroid/src/test/java/org/catrobat/paintroid/local'
        flow = (tests / 'CommonsMetadataQueryFailureFlowTest.kt').read_text()
        for token in ['GalleryPage.CREDIT_SCHEME', 'IllustrationPage.USE_SCHEME', 'shouldOverrideUrlLoading',
                      'everyTopLevelErrorValueIsTypedButNestedErrorAndValidMetadataAreNot',
                      'queryErrorFetchClosesInputDisconnectsAndClearsActiveWithoutProviderLeakage',
                      'httpResponseLimitFieldAndValidationReasonsRemainSeparate',
                      'bothActionsLocalizeTypedMetadataFailureKeepStateAndRetryWithValidMetadata',
                      'typedFailurePreservesAnUnacceptedCreditDraftForBothActions',
                      'queuedTypedFailureResolvesResourcesOnlyWhenTheAliveUiCallbackRuns',
                      'untypedQueryLookingAndPercentNewlineDetailsStayVerbatimOnBothActions',
                      'absentAndBlankUntypedReasonsRetainEachActionsExistingWrapper',
                      'destructionDropsQueuedTypedQueryFailures',
                      'duplicateAndDestroyedInFlightQueryRequestsRemainCancelled',
                      'destroyedActivityDropsAlreadyQueuedSuccessAndRemovesReturnedFile',
                      'representativeM04StatusRetainsFullAccessibleTextAtDoubleScale',
                      'shortLandscapeM04RetainsFullAccessibleTextAtDoubleScale',
                      'repeatedVerticalQueryFailureResetsScrolledStatusToReadingStart',
                      'assertEquals(View.ACCESSIBILITY_LIVE_REGION_POLITE,status(activity).accessibilityLiveRegion)',
                      'rail.resetToReadingStart()', 'assertEquals(before,files(activity))']:
            self.assertIn(token, flow)
        self.assertNotIn('callInstanceMethod', flow)
        translation = (tests / 'CommonsMetadataQueryFailureTranslationTest.kt').read_text()
        for token in ['@Config(sdk=[30,35])', 'AppLanguage.select(context,tag)', '"ko-Kore-KR-anpaint"', 'assertEquals(81,fallbacks)']:
            self.assertIn(token, translation)
        for row in catalogue_fixture()['entries']:
            if row['tag'] == 'default': continue
            value = catalogues.read_strings(ROOT / row['path'])[KEY]
            expected = json.dumps(row['tag']) + ' to ' + json.dumps(value, ensure_ascii=False).replace('$', '\\$')
            self.assertIn(expected, translation)


if __name__ == '__main__': unittest.main()
