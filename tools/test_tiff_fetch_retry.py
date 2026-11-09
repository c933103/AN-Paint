"""Offline contracts for bounded source-download retries."""
import hashlib
import io
from pathlib import Path
import tempfile
import tarfile
import json
import contextlib
import ssl
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

    def test_jpeg_gateway_switches_to_official_asset_bytes(self):
        error = self.error(504)
        log = io.StringIO()
        with patch.object(fetch.urllib.request, 'urlopen',
                          side_effect=[error, io.BytesIO(b'archive')]) as opened, \
                patch.object(fetch.time, 'sleep') as sleep, contextlib.redirect_stdout(log):
            self.assertEqual(fetch.download_source(fetch.JPEG_RELEASE_URL), b'archive')
        self.assertEqual(opened.call_args_list[0].args, (fetch.JPEG_RELEASE_URL,))
        request = opened.call_args_list[1].args[0]
        self.assertEqual(request.full_url, fetch.JPEG_ASSET_URL)
        self.assertEqual(request.get_header('Accept'), 'application/octet-stream')
        self.assertEqual(opened.call_args_list[1].kwargs, {'timeout': 120})
        self.assertTrue(error.closed)
        sleep.assert_called_once_with(2)
        self.assertIn(fetch.JPEG_ASSET_URL, log.getvalue())

    def test_jpeg_primary_success_does_not_contact_fallback(self):
        with patch.object(fetch.urllib.request, 'urlopen',
                          return_value=io.BytesIO(b'archive')) as opened:
            self.assertEqual(fetch.download_source(fetch.JPEG_RELEASE_URL), b'archive')
        opened.assert_called_once_with(fetch.JPEG_RELEASE_URL, timeout=120)

    def test_jpeg_transient_exhaustion_has_three_total_requests(self):
        with patch.object(fetch.urllib.request, 'urlopen',
                          side_effect=[self.error(504) for _ in range(3)]) as opened, \
                patch.object(fetch.time, 'sleep') as sleep:
            with self.assertRaises(urllib.error.HTTPError):
                fetch.download_source(fetch.JPEG_RELEASE_URL)
        self.assertEqual(opened.call_count, 3)
        self.assertEqual([c.args[0].full_url for c in opened.call_args_list[1:]],
                         [fetch.JPEG_ASSET_URL, fetch.JPEG_ASSET_URL])
        self.assertEqual([c.args for c in sleep.call_args_list], [(2,), (4,)])

    def test_permanent_fallback_failure_is_not_retried(self):
        with patch.object(fetch.urllib.request, 'urlopen',
                          side_effect=[self.error(504), self.error(404)]) as opened, \
                patch.object(fetch.time, 'sleep') as sleep:
            with self.assertRaises(urllib.error.HTTPError):
                fetch.download_source(fetch.JPEG_RELEASE_URL)
        self.assertEqual(opened.call_count, 2)
        sleep.assert_called_once_with(2)

    def test_socket_timeout_falls_back_but_certificate_error_fails_closed(self):
        for error in (TimeoutError('timed out'), urllib.error.URLError(TimeoutError())):
            with self.subTest(error=error), patch.object(fetch.urllib.request, 'urlopen',
                    side_effect=[error, io.BytesIO(b'ok')]) as opened, \
                    patch.object(fetch.time, 'sleep'):
                self.assertEqual(fetch.download_source(fetch.JPEG_RELEASE_URL), b'ok')
                self.assertEqual(opened.call_count, 2)
        with patch.object(fetch.urllib.request, 'urlopen', side_effect=
                urllib.error.URLError(ssl.SSLCertVerificationError('untrusted'))) as opened:
            with self.assertRaises(urllib.error.URLError):
                fetch.download_source(fetch.JPEG_RELEASE_URL)
        self.assertEqual(opened.call_count, 1)

    def test_fallback_hash_failure_retains_existing_tree_without_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            (dest / 'codec').mkdir()
            (dest / 'codec/old').write_text('retained')
            with patch.object(fetch, 'DEST', dest), \
                    patch.object(fetch, 'SOURCES', [('codec', '1', fetch.JPEG_RELEASE_URL,
                        hashlib.sha256(b'expected').hexdigest())]), \
                    patch.object(fetch.urllib.request, 'urlopen',
                        side_effect=[self.error(504), io.BytesIO(b'wrong')]) as opened, \
                    patch.object(fetch.time, 'sleep'), patch.object(fetch.tarfile, 'open') as extract:
                with self.assertRaisesRegex(RuntimeError, 'hash mismatch'):
                    fetch.fetch_sources()
            self.assertEqual(opened.call_count, 2)
            extract.assert_not_called()
            self.assertEqual((dest / 'codec/old').read_text(), 'retained')
            self.assertFalse((dest / 'sources.json').exists())

    def test_verified_fallback_installs_staged_tree_and_records_configured_routes(self):
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode='w:gz') as archive:
            member = tarfile.TarInfo('codec-1/LICENSE')
            member.size = 7
            archive.addfile(member, io.BytesIO(b'licence'))
        raw = data.getvalue()
        digest = hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as directory, patch.object(fetch, 'DEST', Path(directory)), \
                patch.object(fetch, 'SOURCES', [('codec', '1', fetch.JPEG_RELEASE_URL, digest)]), \
                patch.object(fetch.urllib.request, 'urlopen',
                    side_effect=[self.error(504), io.BytesIO(raw)]) as opened, \
                patch.object(fetch.time, 'sleep'):
            fetch.fetch_sources()
            dest = Path(directory)
            self.assertEqual((dest / 'codec/LICENSE').read_text(), 'licence')
            self.assertEqual((dest / 'codec/.anpaint-revision').read_text(),
                             f'codec-1 sha256:{digest}\n')
            record = json.loads((dest / 'sources.json').read_text())[0]
            self.assertEqual(record['url'], fetch.JPEG_RELEASE_URL)
            self.assertEqual(record['download_urls'], [fetch.JPEG_RELEASE_URL, fetch.JPEG_ASSET_URL])
            self.assertEqual(record['sha256'], digest)
            fetch.fetch_sources()  # Matching verified cache does not redownload.
            self.assertEqual(opened.call_count, 2)
            self.assertEqual(sorted(p.name for p in dest.iterdir()), ['codec', 'sources.json'])

    def test_read_timeout_closes_response_before_fallback(self):
        class SlowResponse(io.BytesIO):
            def read(self):
                raise TimeoutError('read timed out')
        first = SlowResponse()
        with patch.object(fetch.urllib.request, 'urlopen',
                side_effect=[first, io.BytesIO(b'ok')]) as opened, \
                patch.object(fetch.time, 'sleep'):
            self.assertEqual(fetch.download_source(fetch.JPEG_RELEASE_URL), b'ok')
        self.assertTrue(first.closed)
        self.assertEqual(opened.call_count, 2)

    def test_verified_but_invalid_archive_retains_existing_tree_and_cleans_stage(self):
        raw = b'not a tar archive'
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            (dest / 'codec').mkdir()
            (dest / 'codec/old').write_text('retained')
            with patch.object(fetch, 'DEST', dest), \
                    patch.object(fetch, 'SOURCES', [('codec', '1', fetch.JPEG_RELEASE_URL,
                                                   hashlib.sha256(raw).hexdigest())]), \
                    patch.object(fetch.urllib.request, 'urlopen',
                                 return_value=io.BytesIO(raw)) as opened:
                with self.assertRaises(tarfile.ReadError):
                    fetch.fetch_sources()
            self.assertEqual(opened.call_count, 1)
            self.assertEqual((dest / 'codec/old').read_text(), 'retained')
            self.assertEqual([p.name for p in dest.iterdir()], ['codec'])


if __name__ == '__main__':
    unittest.main()
