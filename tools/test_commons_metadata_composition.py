"""Direct union and negative contracts for accepted M02 + merged M03."""
import hashlib
import itertools
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import commons_metadata_m02_scope as m02
import commons_metadata_m03_scope as m03
import hungarian_attribution_c05_scope as c05
from commons_metadata_composition_scope import (COMBINED_HELPER, HTTP_HELPER,
    LIMIT_BRANCH, without_m02_production, without_m03_production)
from localized_dialog_develop_scope import before_develop_successor, scope
from app_instrumentation_matrix import DIALOG, app_partition
from run_android_instrumentation import declared_tests

ROOT = Path(__file__).resolve().parents[1]
JAVA = 'Paintroid/src/main/java/org/catrobat/paintroid/classic/'


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


class CommonsMetadataCompositionContracts(unittest.TestCase):
    def test_all_six_resource_reversal_orders_restore_all_original_endpoints(self):
        reversals = (m02.before_m02_catalogue, m03.before_m03_catalogue, c05.before_c05)
        for row in m02.fixture()['entries']:
            path = row['path']; text = (ROOT / path).read_text()
            self.assertEqual(1, text.count('name="commons_metadata_http_error"'))
            self.assertEqual(1, text.count('name="commons_metadata_response_too_large"'))
            for order in itertools.permutations(reversals):
                restored = text
                for reverse in order:
                    restored = reverse(path, restored)
                self.assertEqual(row['before_sha256'], digest(restored), path)

    def test_both_exact_standalone_producers_are_recoverable_with_unchanged_original_pins(self):
        m02_rows = json.loads((ROOT/'tools/fixtures/commons_metadata_m02_production_scope.json').read_text())['entries']
        m03_rows = m03.production_fixture()['entries']
        for old02, old03 in zip(m02_rows, m03_rows):
            path = old02['path']; self.assertEqual(path, old03['path'])
            text = (ROOT/path).read_text()
            standalone02 = without_m03_production(path, text)
            standalone03 = without_m02_production(path, text)
            self.assertEqual(old02['after_sha256'], digest(standalone02))
            self.assertEqual(old03['after_sha256'], digest(standalone03))
            restored02 = standalone02
            for edit in reversed(old02['edits']):
                self.assertEqual(1, restored02.count(edit['after']))
                restored02 = restored02.replace(edit['after'], edit['before'], 1)
            restored03 = m03.before_m03_production(path, standalone03)
            self.assertEqual(restored02, restored03)
            self.assertEqual(old02['before_sha256'], digest(restored02))
            self.assertEqual(old03['before_sha256'], digest(restored03))

    def test_one_discriminator_preserves_both_typed_routes_and_the_verbatim_default(self):
        text = (ROOT/JAVA/'MediaGalleryActivity.kt').read_text()
        self.assertEqual(1, text.count(COMBINED_HELPER))
        self.assertEqual(1, text.count('private fun commonsMetadataReason('))
        self.assertEqual(2, text.count('commonsMetadataReason(error)'))
        self.assertEqual(2, text.count('runOnUiThread {if(!isFinishing && !isDestroyed) {\n                    val reason='))
        self.assertEqual(1, COMBINED_HELPER.count('else error.message'))
        self.assertNotIn('error.message==', text)
        self.assertNotIn('error.message ==', text)
        producer = (ROOT/JAVA/'CommonsAttribution.kt').read_text()
        self.assertIn('if (status != 200) throw HttpException(status)', producer)
        self.assertIn('if (bytes.size().toLong() + count > MAX_RESPONSE) throw ResponseLimitException()', producer)
        self.assertIn('.appendQueryParameter("iiextmetadatalanguage", "en")', producer)

    def test_projections_reject_missing_duplicate_or_changed_discriminator_and_unrelated_edits(self):
        path = JAVA+'MediaGalleryActivity.kt'; original = (ROOT/path).read_text()
        for project in (without_m02_production, without_m03_production):
            for change in ('', COMBINED_HELPER*2, HTTP_HELPER,
                           COMBINED_HELPER.replace('else error.message', 'else null'),
                           COMBINED_HELPER.replace('error.status.toString()', '"503"')):
                with self.subTest(project=project, change=change), self.assertRaises(AssertionError):
                    project(path, original.replace(COMBINED_HELPER, change, 1))
            self.assertNotEqual(digest(project(path, original)), digest(project(path, original+'\n// unrelated\n')))

    def test_historical_overlap_receipts_reject_any_unapproved_content_or_fixture_change(self):
        for row in scope()['historical_overlaps']:
            path=row['path']; original=(ROOT/path).read_bytes()
            self.assertEqual(row['pr52_sha256'], hashlib.sha256(before_develop_successor(path, original)).hexdigest())
            with self.assertRaises(AssertionError): before_develop_successor(path, original+b'\n')
        raw=(ROOT/'tools/fixtures/localized_dialog_develop_successor_scope.json').read_bytes()
        with patch.object(Path, 'read_bytes', return_value=raw+b' '):
            with self.assertRaises(AssertionError): scope()

    def test_legacy_omission_cannot_silently_drop_a_new_sdk_eligible_dialog_method(self):
        for sdk in (21,24,30):
            expected=declared_tests(ROOT/'app/src/androidTest', sdk_level=sdk)
            with self.assertRaises(ValueError): app_partition(expected|{(DIALOG,'unexpectedEligibleCase')},sdk)
