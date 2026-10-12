"""Adversarial host transport/raster checks; synthetic pixels are NOT device evidence."""
import base64
import contextlib
import copy
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib

import installed_glyph_ink_evidence as ink
from run_android_instrumentation import parse_protocol

SOURCE = ink.source_tests_sha256(ink.DEFAULT_SOURCE_TESTS)
EXPECTED = ink.source_expected_inventory(SOURCE)


def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)


def png(width, height, rgba, filters=(0,)):
    rows = bytearray()
    for y in range(height):
        mode = filters[y % len(filters)]
        rows.append(mode)
        for x in range(width * 4):
            pos = y * width * 4 + x
            a = rgba[pos - 4] if x >= 4 else 0
            b = rgba[pos - width * 4] if y else 0
            c = rgba[pos - width * 4 - 4] if y and x >= 4 else 0
            if mode == 0:
                prediction = 0
            elif mode == 1:
                prediction = a
            elif mode == 2:
                prediction = b
            elif mode == 3:
                prediction = (a + b) // 2
            elif mode == 4:
                p = a + b - c
                distances = (abs(p - a), abs(p - b), abs(p - c))
                prediction = (a, b, c)[distances.index(min(distances))]
            else:
                prediction = 0
            rows.append((rgba[pos] - prediction) & 255)
    return (ink.PNG_SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
            + chunk(b'sBIT', b'\x08\x08\x08\x08') + chunk(b'IDAT', zlib.compress(bytes(rows))) + chunk(b'IEND', b''))


def metadata(raw):
    width, height = struct.unpack_from('>II', raw, 16)
    return {'width': width, 'height': height, 'bytes': len(raw), 'sha256': ink.sha256(raw),
            'base64': base64.b64encode(raw).decode('ascii')}


def fixture(route='copy', inset=0):
    width, height = 8, 5
    box = (-2 - inset, -2, 8 + inset, 5)
    rw, rh = box[2] - box[0], box[3] - box[1]
    reference, actual = bytearray(rw * rh * 4), bytearray(width * height * 4)
    # The first edge glyph uses alpha=1 to catch any illicit opacity threshold.
    pixels = [(0, 1, (12, 34, 56, 1)), (2, 1, (78, 90, 123, 128)), (5, 1, (200, 201, 202, 255))]
    for x, y, color in pixels:
        r = ((y - box[1]) * rw + x - box[0]) * 4
        a = ((y + 1) * width + x + 1) * 4
        reference[r:r + 4] = actual[a:a + 4] = bytes(color)
    record = {'reference_source': ink.REFERENCE_SOURCE,
        'reference_box': f'[{box[0]},{box[1]}][{box[2]},{box[3]}]',
        'glyph_bounds': 'RectF(0.0, 0.0, 6.0, 3.0)', 'origin_x': 1, 'origin_y': 1,
        'content_width': 6, 'view_use_bounds_for_width': True, 'layout_use_bounds_for_width': True,
        'shift_drawing_offset_for_start_overhang': False, 'measured_leading_inset_px': inset,
        'ink_pixels': 3, 'ink_left': 0, 'ink_right_exclusive': 6, 'allocation_edge_pixels': 0,
        'horizontal_overflow_pixels': 0, 'outside_view_pixels': 0,
        'missing_expected_ink_pixels': 0, 'different_argb_pixels': 0,
        'alpha_cutoff': 0, 'position_tolerance_px': 0, 'color_tolerance': 0,
        'schema': 1, 'route': route, 'locale': 'ar', 'evidence_kind': ink.EVIDENCE_KIND,
        'source_tests_sha256': SOURCE, 'font_scale': 2, 'api': 35, 'target_sdk': 35,
        'fingerprint': 'synthetic/unit-test/api35', 'density': 2.0, 'density_dpi': 320,
        'root_width': 12, 'root_height': 6, 'orientation': 2,
        'default_textview_use_bounds_for_width': False, 'message': ink.MESSAGES[route],
        'accessibility_text': ink.MESSAGES[route], 'complete_layout_text': ink.MESSAGES[route],
        'actual_png': metadata(png(width, height, actual)),
        'reference_png': metadata(png(rw, rh, reference))}
    return record


def event(code, name=ink.PRODUCER_TEST, count=len(EXPECTED)):
    return (f'INSTRUMENTATION_STATUS: class={name[0]}\n'
            f'INSTRUMENTATION_STATUS: test={name[1]}\n'
            f'INSTRUMENTATION_STATUS: numtests={count}\n'
            + ('INSTRUMENTATION_STATUS: stack=java.lang.AssertionError: actual ink failure\n' if code == -2 else '')
            + f'INSTRUMENTATION_STATUS_CODE: {code}\n')


def results(records=None):
    records = records if records is not None else {route: fixture(route) for route in ink.ROUTES}
    return ''.join(f'INSTRUMENTATION_RESULT: {ink.KEY_PREFIX}{route}='
                   + json.dumps(record, ensure_ascii=False, separators=(',', ':')) + '\n'
                   for route, record in records.items())


def capture(records=None, status=0):
    tests = ''.join(event(1, identity) + event(status if identity == ink.PRODUCER_TEST else 0, identity)
                    for identity in sorted(EXPECTED))
    raw = (tests + results(records) + 'INSTRUMENTATION_CODE: -1\n').encode()
    summary = parse_protocol(raw.decode(), EXPECTED)
    summary.update(source_tests_sha256=SOURCE, device_sdk=35)
    return raw, summary


def replace_pixels(record, name, mutate):
    original = ink.decode_png(base64.b64decode(record[name]['base64']))
    pixels = bytearray(original.rgba)
    mutate(pixels, original.width, original.height)
    record[name] = metadata(png(original.width, original.height, pixels))


def refresh_counts(record):
    actual = ink.decode_png(base64.b64decode(record['actual_png']['base64']))
    reference = ink.decode_png(base64.b64decode(record['reference_png']['base64']))
    box = tuple(map(int, ink.RECT.fullmatch(record['reference_box']).groups()))
    record.update(ink.recompute(actual, reference, box, record['origin_x'], record['origin_y'], record['content_width']))


class InstalledGlyphTransportTests(unittest.TestCase):
    def test_two_routes_full_pngs_source_and_successful_protocol_are_required(self):
        raw, summary = capture()
        receipt, records = ink.verify_capture(raw, SOURCE, summary)
        self.assertTrue(receipt['success'])
        self.assertEqual(ink.sha256(raw), receipt['raw_output_sha256'])
        self.assertEqual(set(ink.ROUTES), set(records))
        for record in records.values():
            self.assertEqual(3, record.recomputed['ink_pixels'])
            self.assertEqual({0}, {record.recomputed[k] for k in ink.FAILURE_COUNTS})
            self.assertEqual(base64.b64decode(record.record['actual_png']['base64']), record.actual_png)
        self.assertIn('caller must separately establish APK/build/run provenance', receipt['scope'])

    def test_measured_leading_margin_conservative_expansion_is_accepted(self):
        verified = ink.verify_record(fixture(inset=2), 'copy', SOURCE)
        self.assertEqual(3, verified.recomputed['ink_pixels'])
        record = fixture(inset=2)
        record['reference_box'] = '[-2,-2][8,5]'
        with self.assertRaisesRegex(ink.EvidenceError, 'geometry/allocation guards'):
            ink.verify_record(record, 'copy', SOURCE)

    def test_missing_duplicate_unknown_and_swapped_routes_fail(self):
        raw, _ = capture()
        invalid = [results({'copy': fixture()}).encode(), raw + results({'copy': fixture()}).encode(),
                   raw + b'INSTRUMENTATION_RESULT: anpaint_m04_glyph_bounds_other={}\n',
                   raw.replace(b'"route":"copy"', b'"route":"insert"')]
        for bad in invalid:
            with self.subTest(bad=bad[-80:]), self.assertRaises(ink.EvidenceError):
                records = ink.extract_records(bad)
                for route, record in records.items():
                    ink.verify_record(record, route, SOURCE)

    def test_duplicate_json_fields_even_nested_are_rejected(self):
        raw, _ = capture()
        for before, after in [(b'"schema":1', b'"schema":1,"schema":1'),
                              (b'"width":8', b'"width":8,"width":8')]:
            with self.subTest(before=before), self.assertRaisesRegex(ink.EvidenceError, 'duplicate JSON'):
                ink.extract_records(raw.replace(before, after, 1))

    def test_malformed_truncated_multiline_nonobject_and_nonfinite_json_fail(self):
        prefix = b'INSTRUMENTATION_RESULT: anpaint_m04_glyph_bounds_copy='
        for value in (b'{', b'{} trailing', b'[]', b'null', b'{"x":NaN}', b'{"x":Infinity}',
                      b'{"x":\n1}', b'{"x":"\\ud800"}', b'{"x":"\xff"}'):
            with self.subTest(value=value), self.assertRaises(ink.EvidenceError):
                ink.extract_records(prefix + value + b'\n' + results({'insert': fixture('insert')}).encode())

    def test_payload_unicode_line_separators_cannot_smuggle_protocol_records(self):
        for separator in ('\x85', '\u2028', '\u2029'):
            records = {route: fixture(route) for route in ink.ROUTES}
            records['copy']['fingerprint'] = 'device' + separator + 'INSTRUMENTATION_CODE: -1'
            raw, summary = capture(records)
            with self.subTest(separator=repr(separator)), self.assertRaisesRegex(ink.EvidenceError, 'protocol line separator'):
                ink.verify_capture(raw, SOURCE, summary)

    def test_extreme_numbers_and_deep_json_fail_as_evidence_errors(self):
        for raw in ('{\"x\":' + '1'*5000 + '}', '{\"x\":' + '['*2000 + '0' + ']'*2000 + '}'):
            with self.assertRaises(ink.EvidenceError):
                ink.strict_json(raw)
        record = fixture(); record['density'] = 10**1000
        with self.assertRaises(ink.EvidenceError):
            ink.verify_record(record, 'copy', SOURCE)

    def test_record_raw_and_bundle_size_limits_fail_closed(self):
        raw, _ = capture()
        with patch.object(ink, 'MAX_RECORD_BYTES', 10), self.assertRaisesRegex(ink.EvidenceError, 'record size'):
            ink.extract_records(raw)
        with patch.object(ink, 'MAX_RAW_BYTES', 10), self.assertRaisesRegex(ink.EvidenceError, 'raw protocol size'):
            ink.extract_records(raw)
        with patch.object(ink, 'MAX_BUNDLE_BYTES', 10), self.assertRaisesRegex(ink.EvidenceError, 'Parcel Bundle'):
            ink.extract_records(raw)

    def test_wrong_source_profile_text_and_permissive_flags_fail(self):
        changes = {'source_tests_sha256': 'b' * 64, 'schema': 2, 'locale': 'en', 'api': 34,
                   'target_sdk': 34, 'font_scale': 1, 'orientation': 1, 'root_width': 6,
                   'view_use_bounds_for_width': False, 'layout_use_bounds_for_width': False,
                   'shift_drawing_offset_for_start_overhang': True, 'alpha_cutoff': 1,
                   'position_tolerance_px': 1, 'color_tolerance': 1, 'density': 3,
                   'reference_source': 'crop of actual view', 'evidence_kind': 'hardware screenshot',
                   'message': ink.MESSAGES['insert'], 'accessibility_text': 'truncated',
                   'complete_layout_text': 'truncated', 'fingerprint': '',
                   'default_textview_use_bounds_for_width': 0}
        for name, value in changes.items():
            record = fixture()
            record[name] = value
            with self.subTest(name=name), self.assertRaises(ink.EvidenceError):
                ink.verify_record(record, 'copy', SOURCE)

    def test_invalid_schema_types_missing_unknown_fields_and_geometry_fail(self):
        invalid = []
        for name, value in [('schema', True), ('font_scale', 2.0), ('origin_x', True),
                            ('origin_y', -1), ('content_width', 0), ('ink_pixels', 3.0),
                            ('measured_leading_inset_px', -1), ('reference_box', 'Rect(-2,-2,8,5)'),
                            ('reference_box', '[-2,-2][9,5]'), ('glyph_bounds', 'RectF(NaN, 0.0, 6.0, 3.0)'),
                            ('glyph_bounds', 'RectF(0.0, 0.0, 100000.0, 3.0)'),
                            ('glyph_bounds', 'RectF(6.0, 0.0, 0.0, 3.0)'), ('density', float('inf'))]:
            record = fixture()
            record[name] = value
            invalid.append((name, record))
        record = fixture(); del record['reference_source']; invalid.append(('missing', record))
        record = fixture(); record['success'] = True; invalid.append(('unknown', record))
        for name, record in invalid:
            with self.subTest(name=name), self.assertRaises(ink.EvidenceError):
                ink.verify_record(record, 'copy', SOURCE)

    def test_altered_frame_metrics_cannot_replace_actual_pixel_evidence(self):
        for name, value in [('origin_x', 0), ('origin_y', 0), ('content_width', 5),
                            ('ink_pixels', 2), ('ink_left', 1), ('ink_right_exclusive', 5)]:
            record = fixture()
            record[name] = value
            with self.subTest(name=name), self.assertRaises(ink.EvidenceError):
                ink.verify_record(record, 'copy', SOURCE)

    def test_first_and_last_glyph_corruption_with_updated_png_hash_still_fail(self):
        for local_x in (0, 5):
            record = fixture()
            def erase(pixels, width, height):
                offset = (2 * width + 1 + local_x) * 4
                pixels[offset:offset + 4] = b'\0' * 4
            replace_pixels(record, 'actual_png', erase)
            unchanged_reference = copy.deepcopy(record['reference_png'])
            with self.subTest(local_x=local_x), self.assertRaisesRegex(ink.EvidenceError, 'recomputation'):
                ink.verify_record(record, 'copy', SOURCE)
            refresh_counts(record)
            self.assertEqual(1, record['missing_expected_ink_pixels'])
            self.assertEqual(1, record['different_argb_pixels'])
            self.assertEqual(unchanged_reference, record['reference_png'])
            with self.assertRaisesRegex(ink.EvidenceError, 'nonzero missing_expected_ink_pixels'):
                ink.verify_record(record, 'copy', SOURCE)

    def test_color_and_alpha_changes_are_exact_even_without_missing_ink(self):
        for component in range(4):
            record = fixture()
            def change(pixels, width, height):
                pixels[(2 * width + 3) * 4 + component] ^= 1
            replace_pixels(record, 'actual_png', change)
            refresh_counts(record)
            self.assertEqual(0, record['missing_expected_ink_pixels'])
            self.assertEqual(1, record['different_argb_pixels'])
            with self.subTest(component=component), self.assertRaisesRegex(ink.EvidenceError, 'different_argb_pixels'):
                ink.verify_record(record, 'copy', SOURCE)

    def test_whole_actual_view_detects_extra_ink_and_invisible_rgb(self):
        for pixel in (b'\xff\x00\x00\x01', b'\x00\x01\x00\x00'):
            record = fixture()
            replace_pixels(record, 'actual_png', lambda data, w, h: data.__setitem__(slice(0, 4), pixel))
            refresh_counts(record)
            self.assertEqual(1, record['different_argb_pixels'])
            with self.subTest(pixel=pixel), self.assertRaisesRegex(ink.EvidenceError, 'different_argb_pixels'):
                ink.verify_record(record, 'copy', SOURCE)

    def test_genuine_overflow_is_rejected_even_when_the_actual_view_contains_it(self):
        record = fixture()
        # local x=-1 lies within the full actual view's left padding at view x=0.
        replace_pixels(record, 'reference_png', lambda data, w, h:
                       data.__setitem__(slice((3*w+1)*4, (3*w+1)*4+4), b'\x01\x02\x03\xff'))
        replace_pixels(record, 'actual_png', lambda data, w, h:
                       data.__setitem__(slice(2*w*4, 2*w*4+4), b'\x01\x02\x03\xff'))
        refresh_counts(record)
        self.assertEqual(1, record['horizontal_overflow_pixels'])
        self.assertEqual(0, record['different_argb_pixels'])
        with self.assertRaisesRegex(ink.EvidenceError, 'horizontal_overflow_pixels'):
            ink.verify_record(record, 'copy', SOURCE)

    def test_reference_ink_outside_actual_view_fails(self):
        record = fixture()
        # local y=-2 maps above actual y=0 and touches the full allocation edge.
        replace_pixels(record, 'reference_png', lambda data, w, h:
                       data.__setitem__(slice(3*4, 3*4+4), b'\x01\x02\x03\xff'))
        refresh_counts(record)
        self.assertEqual(1, record['outside_view_pixels'])
        self.assertEqual(1, record['missing_expected_ink_pixels'])
        with self.assertRaises(ink.EvidenceError):
            ink.verify_record(record, 'copy', SOURCE)

    def test_allocation_edge_ink_fails_even_with_honestly_reported_counts(self):
        record = fixture()
        replace_pixels(record, 'reference_png', lambda data, w, h:
                       data.__setitem__(slice((3*w)*4, (3*w)*4+4), b'\x01\x02\x03\xff'))
        refresh_counts(record)
        self.assertEqual(1, record['allocation_edge_pixels'])
        with self.assertRaisesRegex(ink.EvidenceError, 'allocation_edge_pixels'):
            ink.verify_record(record, 'copy', SOURCE)

    def test_empty_reference_and_cropped_actual_as_reference_fail(self):
        record = fixture()
        replace_pixels(record, 'reference_png', lambda data, w, h: data.__setitem__(slice(None), b'\0'*len(data)))
        refresh_counts(record)
        with self.assertRaisesRegex(ink.EvidenceError, 'no ink'):
            ink.verify_record(record, 'copy', SOURCE)
        record = fixture()
        record['reference_png'] = copy.deepcopy(record['actual_png'])
        with self.assertRaisesRegex(ink.EvidenceError, 'dimensions disagree'):
            ink.verify_record(record, 'copy', SOURCE)
        record['reference_box'] = '[0,0][8,5]'
        with self.assertRaisesRegex(ink.EvidenceError, 'geometry/allocation guards'):
            ink.verify_record(record, 'copy', SOURCE)

    def test_bad_base64_hash_size_dimensions_and_extra_metadata_fail(self):
        changes = [('base64', '!!!!'), ('base64', fixture()['actual_png']['base64'] + '\n'),
                   ('sha256', '0'*64), ('sha256', 'A'*64), ('bytes', 1), ('width', 7),
                   ('height', True), ('height', ink.MAX_DIMENSION+1), ('base64', ''), ('extra', 1)]
        for name, value in changes:
            record = fixture()
            record['actual_png'][name] = value
            with self.subTest(name=name), self.assertRaises(ink.EvidenceError):
                ink.verify_record(record, 'copy', SOURCE)

    def test_cross_route_device_metrics_must_agree(self):
        records = {route: fixture(route) for route in ink.ROUTES}
        for name, value in [('fingerprint', 'other/device'), ('root_width', 13),
                            ('default_textview_use_bounds_for_width', True)]:
            changed = copy.deepcopy(records)
            changed['insert'][name] = value
            raw, summary = capture(changed)
            with self.subTest(name=name), self.assertRaisesRegex(ink.EvidenceError, 'route device/profile mismatch'):
                ink.verify_capture(raw, SOURCE, summary)

    def test_final_evidence_keys_do_not_manufacture_success_or_hide_real_failure(self):
        raw, failed = capture(status=-2)
        self.assertFalse(failed['success'])
        case = next(c for c in failed['cases'] if (c['classname'], c['name']) == ink.PRODUCER_TEST)
        self.assertEqual('failure', case['status'])
        self.assertIn('actual ink failure', case['message'])
        with self.assertRaisesRegex(ink.EvidenceError, 'successful runner summary'):
            ink.verify_capture(raw, SOURCE, failed)
        _, forged = capture()
        with self.assertRaisesRegex(ink.EvidenceError, 'raw instrumentation did not pass'):
            ink.verify_capture(raw, SOURCE, forged)
        empty = (results() + 'INSTRUMENTATION_CODE: -1\n').encode()
        self.assertFalse(parse_protocol(empty.decode(), {ink.PRODUCER_TEST})['success'])
        with self.assertRaisesRegex(ink.EvidenceError, 'raw instrumentation did not pass'):
            ink.verify_capture(empty, SOURCE, forged)

    def test_nonpassing_truncated_or_wrong_source_summary_is_rejected(self):
        raw, summary = capture()
        changes = [('success', False), ('source_tests_sha256', 'b'*64), ('device_sdk', 30),
                   ('returncode', 1), ('returncode', False), ('timed_out', True), ('errors', ['oops']),
                   ('missing', ['test']), ('unexpected', ['test']), ('expected_tests', 2),
                   ('completed_tests', True), ('cases', [])]
        for field, value in changes:
            altered = copy.deepcopy(summary)
            altered[field] = value
            with self.subTest(field=field), self.assertRaises(ink.EvidenceError):
                ink.verify_capture(raw, SOURCE, altered)
        with self.assertRaises(ink.EvidenceError):
            ink.verify_capture(raw.replace(b'INSTRUMENTATION_CODE: -1\n', b''), SOURCE, summary)
        altered = copy.deepcopy(summary); altered['cases'][0]['message'] = 'not from this raw output'
        with self.assertRaisesRegex(ink.EvidenceError, 'summary/raw protocol disagree'):
            ink.verify_capture(raw, SOURCE, altered)
        altered = copy.deepcopy(summary); altered['cases'] *= 2
        with self.assertRaisesRegex(ink.EvidenceError, 'duplicate runner case'):
            ink.verify_capture(raw, SOURCE, altered)

    def test_self_consistent_producer_only_subset_fails_exact_source_inventory(self):
        raw = (event(1, count=1) + event(0, count=1) + results() + 'INSTRUMENTATION_CODE: -1\n').encode()
        summary = parse_protocol(raw.decode(), {ink.PRODUCER_TEST})
        self.assertTrue(summary['success'])
        summary.update(source_tests_sha256=SOURCE, device_sdk=35)
        with self.assertRaisesRegex(ink.EvidenceError, 'source-derived ordinary-app partition'):
            ink.verify_capture(raw, SOURCE, summary)

    def test_changed_local_source_digest_rejects_otherwise_consistent_capture(self):
        raw, summary = capture()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path/'Other.kt').write_text('package example\nclass Other { @Test fun x() {} }')
            with self.assertRaisesRegex(ink.EvidenceError, 'source does not match'):
                ink.verify_capture(raw, SOURCE, summary, path)

    def test_wrong_producer_identity_fails(self):
        other = ('paint.anpaint.android.OtherTest', 'passes')
        raw = (event(1, other, 1) + event(0, other, 1) + results() + 'INSTRUMENTATION_CODE: -1\n').encode()
        summary = parse_protocol(raw.decode(), {other})
        summary.update(source_tests_sha256=SOURCE, device_sdk=35)
        with self.assertRaisesRegex(ink.EvidenceError, 'producer test is absent'):
            ink.verify_capture(raw, SOURCE, summary)

    def test_cli_extracts_verified_bytes_receipt_and_never_overwrites(self):
        raw, summary = capture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'raw.log').write_bytes(raw)
            (root/'summary.json').write_text(json.dumps(summary))
            args = ['--raw-output', str(root/'raw.log'), '--expected-source-sha256', SOURCE,
                    '--runner-summary', str(root/'summary.json'), '--output-dir', str(root/'out')]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, ink.main(args))
            receipt = json.loads((root/'out/receipt.json').read_text())
            self.assertEqual(ink.sha256((root/'summary.json').read_bytes()), receipt['runner_summary_sha256'])
            self.assertEqual(7, len(list((root/'out').iterdir())))
            self.assertEqual(base64.b64decode(fixture()['actual_png']['base64']), (root/'out/copy-actual.png').read_bytes())
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(1, ink.main(args))
            failed, _ = capture(status=-2)
            (root/'raw.log').write_bytes(failed)
            args[-1] = str(root/'failed')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(1, ink.main(args))
            self.assertFalse((root/'failed').exists())


class StrictPngTests(unittest.TestCase):
    def test_all_five_filters_decode_exact_raw_rgba(self):
        pixels = bytes((i*73+19) % 256 for i in range(9*7*4))
        for modes in [(0,), (1,), (2,), (3,), (4,), (0, 1, 2, 3, 4)]:
            with self.subTest(modes=modes):
                decoded = ink.decode_png(png(9, 7, pixels, modes))
                self.assertEqual((9, 7), (decoded.width, decoded.height))
                self.assertEqual(pixels, decoded.rgba)

    def test_crc_truncation_trailing_bytes_duplicate_and_unsupported_chunks_fail(self):
        valid = png(2, 2, b'\x00'*16)
        header = valid[8:33]
        corrupt = bytearray(valid); corrupt[29] ^= 1
        invalid = [bytes(corrupt), valid[:-1], valid+b'\0', valid[:8]+header+valid[8:],
                   ink.PNG_SIGNATURE+chunk(b'IDAT', b'x')+valid[8:],
                   valid[:-12]+chunk(b'tEXt', b'extra')+valid[-12:],
                   valid[:-12]+chunk(b'acTL', b'\x00'*8)+valid[-12:], valid[:-12]]
        for raw in invalid:
            with self.subTest(size=len(raw)), self.assertRaises(ink.EvidenceError):
                ink.decode_png(raw)

    def test_dimensions_pixel_budget_color_depth_interlace_filter_fail_closed(self):
        for width, height, bits, color, interlace in [(0, 2, 8, 6, 0), (ink.MAX_DIMENSION+1, 1, 8, 6, 0),
               (4096, 4096, 8, 6, 0), (2, 2, 16, 6, 0), (2, 2, 8, 2, 0), (2, 2, 8, 6, 1)]:
            raw = (ink.PNG_SIGNATURE+chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, bits, color, 0, 0, interlace))
                   +chunk(b'IDAT', zlib.compress(b'\0'*18))+chunk(b'IEND', b''))
            with self.subTest(profile=(width, height, bits, color, interlace)), self.assertRaises(ink.EvidenceError):
                ink.decode_png(raw)
        with self.assertRaisesRegex(ink.EvidenceError, 'row filter'):
            ink.decode_png(png(2, 2, b'\0'*16, (5,)))

    def test_bounded_inflate_rejects_bomb_truncation_and_concatenated_streams(self):
        prefix = ink.PNG_SIGNATURE+chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0))
        compressed = [zlib.compress(b'\0'*1000000), zlib.compress(b'\0'*4),
                      zlib.compress(b'\0'*5)[:-1], zlib.compress(b'\0'*5)+zlib.compress(b'extra'),
                      zlib.compress(b'\0'*5)+b'junk', b'not-zlib']
        for data in compressed:
            with self.subTest(length=len(data)), self.assertRaises(ink.EvidenceError):
                ink.decode_png(prefix+chunk(b'IDAT', data)+chunk(b'IEND', b''))

    def test_consecutive_idat_chunks_and_standard_native_metadata_work(self):
        compressed = zlib.compress(b'\0\x10\x20\x30\xff')
        prefix = ink.PNG_SIGNATURE+chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0))
        raw = (prefix+chunk(b'sRGB', b'\0')+chunk(b'gAMA', struct.pack('>I', 45455))
               +chunk(b'IDAT', compressed[:3])+chunk(b'IDAT', compressed[3:])+chunk(b'IEND', b''))
        self.assertEqual(b'\x10\x20\x30\xff', ink.decode_png(raw).rgba)


if __name__ == '__main__':
    unittest.main()
