"""Offline contracts for bounded source-download retries."""
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import fetch_tiff_sources as fetch


class SourceRetryTest(unittest.TestCase):
    def error(self, status):
        return urllib.error.HTTPError('https://example.invalid/source', status,
                                      'test response', {}, io.BytesIO(b'error'))

    def test_gateway_recovers_with_original_url_timeout_and_closes_errors(self):
        errors = [self.error(504), self.error(502)]
        with patch.object(fetch.urllib.request, 'urlopen',
                          side_effect=errors + [io.BytesIO(b'archive')]) as opened, \
                patch.object(fetch.time, 'sleep') as sleep:
            self.assertEqual(fetch.download_source('https://example.invalid/source'), b'archive')
        self.assertEqual(opened.call_count, 3)
        for call in opened.call_args_list:
            self.assertEqual(call.args, ('https://example.invalid/source',))
            self.assertEqual(call.kwargs, {'timeout': 120})
        self.assertEqual([c.args for c in sleep.call_args_list], [(2,), (4,)])
        self.assertTrue(all(error.closed for error in errors))

    def test_exhaustion_stops_after_three_attempts(self):
        for status in (502, 503, 504):
            with self.subTest(status=status):
                errors = [self.error(status) for _ in range(3)]
                with patch.object(fetch.urllib.request, 'urlopen', side_effect=errors) as opened, \
                        patch.object(fetch.time, 'sleep') as sleep:
                    with self.assertRaises(urllib.error.HTTPError) as result:
                        fetch.download_source('https://example.invalid/source')
                self.assertIs(result.exception, errors[-1])
                self.assertEqual(opened.call_count, 3)
                self.assertEqual(sleep.call_count, 2)

    def test_permanent_and_unapproved_http_errors_are_not_retried(self):
        for status in (400, 401, 403, 404, 429, 500):
            with self.subTest(status=status), \
                    patch.object(fetch.urllib.request, 'urlopen', side_effect=self.error(status)) as opened, \
                    patch.object(fetch.time, 'sleep') as sleep:
                with self.assertRaises(urllib.error.HTTPError):
                    fetch.download_source('https://example.invalid/source')
                self.assertEqual(opened.call_count, 1)
                sleep.assert_not_called()

    def test_transport_errors_not_broadly_swallowed(self):
        with patch.object(fetch.urllib.request, 'urlopen',
                          side_effect=urllib.error.URLError('certificate failure')) as opened, \
                patch.object(fetch.time, 'sleep') as sleep:
            with self.assertRaises(urllib.error.URLError):
                fetch.download_source('https://example.invalid/source')
            self.assertEqual(opened.call_count, 1)
            sleep.assert_not_called()

    def test_hash_failure_never_extracts_or_retries(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(fetch, 'DEST', Path(directory)), \
                patch.object(fetch, 'SOURCES', [('codec', '1', 'https://example.invalid/source',
                                               hashlib.sha256(b'expected').hexdigest())]), \
                patch.object(fetch.urllib.request, 'urlopen', return_value=io.BytesIO(b'wrong')) as opened, \
                patch.object(fetch.time, 'sleep') as sleep, \
                patch.object(fetch.tarfile, 'open') as extract:
            with self.assertRaisesRegex(RuntimeError, 'hash mismatch'):
                fetch.fetch_sources()
            self.assertEqual(opened.call_count, 1)
            sleep.assert_not_called()
            extract.assert_not_called()
            self.assertFalse((Path(directory) / 'codec').exists())
            self.assertFalse((Path(directory) / 'sources.json').exists())


if __name__ == '__main__':
    unittest.main()
