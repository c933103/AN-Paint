#!/usr/bin/env python3
"""Fail-closed decoder for the installed API35 Arabic M04 native raster evidence.

This verifies full PNGs and recomputes the producer's exact alpha/ARGB oracle.
It is NOT an independent proof that an arbitrary PNG depicts the claimed text:
complete Layout/text coverage and permitted drawing features are established by
reviewed, source-bound producer assertions. APK/build/run provenance remains the
caller's responsibility. A successful, matching runner summary and the same raw
protocol are required for acceptance; extra result keys cannot pass a test.

Only Python's standard library is needed. PNG support is deliberately limited to
noninterlaced 8-bit RGBA (the producer's transparent ARGB_8888 software rasters),
with all five PNG row filters. Unsupported formats fail rather than convert,
rescale, crop, mask, threshold, or apply colour-management transformations.
"""
from __future__ import annotations

import argparse
import base64
import binascii
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys
import zlib

from run_android_instrumentation import parse_protocol, declared_tests, source_tests_sha256
from app_instrumentation_matrix import app_partition

DEFAULT_SOURCE_TESTS = Path(__file__).resolve().parents[1] / 'app/src/androidTest'

MAX_RECORD_BYTES = 128 * 1024
MAX_BUNDLE_BYTES = 512 * 1024
MAX_PNG_BYTES = 96 * 1024
MAX_RAW_BYTES = 32 * 1024 * 1024
MAX_SUMMARY_BYTES = 4 * 1024 * 1024
MAX_DIMENSION = 16384
MAX_PIXELS = 16_000_000
KEY_PREFIX = 'anpaint_m04_glyph_bounds_'
ROUTES = ('copy', 'insert')
PRODUCER_TEST = ('paint.anpaint.android.GalleryViewportDeviceTest',
                 'realBrowserKeepsItsViewportAtLargeTextAcrossGalleryRotation')
REFERENCE_SOURCE = 'Complete native Layout with API35 actual-glyph bounds; never an actual-view crop'
EVIDENCE_KIND = 'Installed API35 native software raster of injected actual status text; not network-route or hardware screenshot proof'
# Schema 1 is the exact current Arabic M04 route/profile, not a generic image API.
_REASON = 'فشل الاستعلام عن بيانات Commons الوصفية'
MESSAGES = {'copy': 'تعذر نسخ اعتماد الصورة: ' + _REASON,
            'insert': 'تعذر تحميل صورة المعرض: ' + _REASON}
COUNTS = ('ink_pixels', 'ink_left', 'ink_right_exclusive', 'allocation_edge_pixels',
          'horizontal_overflow_pixels', 'outside_view_pixels',
          'missing_expected_ink_pixels', 'different_argb_pixels')
FAILURE_COUNTS = COUNTS[3:]
FIELDS = frozenset(('reference_source', 'reference_box', 'glyph_bounds', 'origin_x', 'origin_y',
    'content_width', 'view_use_bounds_for_width', 'layout_use_bounds_for_width',
    'shift_drawing_offset_for_start_overhang', 'measured_leading_inset_px',
    *COUNTS, 'alpha_cutoff', 'position_tolerance_px', 'color_tolerance', 'schema', 'route',
    'locale', 'evidence_kind', 'source_tests_sha256', 'font_scale', 'api', 'target_sdk',
    'fingerprint', 'density', 'density_dpi', 'root_width', 'root_height', 'orientation',
    'default_textview_use_bounds_for_width', 'message', 'accessibility_text',
    'complete_layout_text', 'actual_png', 'reference_png'))
PNG_FIELDS = frozenset(('width', 'height', 'bytes', 'sha256', 'base64'))
DIGEST = re.compile(r'[0-9a-f]{64}')
INTEGER = r'-?(?:0|[1-9][0-9]*)'
RECT = re.compile(r'\[(' + INTEGER + r'),(' + INTEGER + r')\]\[(' + INTEGER + r'),(' + INTEGER + r')\]')
FLOAT = r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?'
RECTF = re.compile(r'RectF\((' + FLOAT + r'), (' + FLOAT + r'), (' + FLOAT + r'), (' + FLOAT + r')\)')
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


class EvidenceError(ValueError):
    """Malformed, unsupported, inconsistent or non-passing evidence."""


def require(condition: bool, message: str) -> None:
    # Do not use Python assert: python -O must retain every acceptance check.
    if not condition:
        raise EvidenceError(message)


def integer(value, name: str, minimum: int, maximum: int) -> int:
    require(type(value) is int and minimum <= value <= maximum, f'{name}: invalid integer')
    return value


def number(value, name: str, minimum: float, maximum: float) -> float:
    require(type(value) in (int, float) and minimum <= value <= maximum
            and math.isfinite(value), f'{name}: invalid finite number')
    return value


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON field: {key}')
        result[key] = value
    return result


def _invalid_constant(value):
    raise EvidenceError(f'non-finite JSON constant: {value}')


def _bounded_json_int(value):
    require(len(value) <= 21, 'JSON integer exceeds bounded evidence schema')
    return int(value)


def strict_json(raw: bytes | str) -> dict:
    try:
        text = raw.decode('utf-8', errors='strict') if isinstance(raw, bytes) else raw
        # Reject unpaired escaped Unicode surrogates too, not only invalid UTF-8.
        result = json.loads(text, object_pairs_hook=_unique_object, parse_constant=_invalid_constant,
                            parse_int=_bounded_json_int)
        stack = [(result, 0)]
        while stack:
            value, depth = stack.pop()
            require(depth <= 16, 'JSON nesting limit exceeded')
            if type(value) is dict:
                stack.extend((child, depth + 1) for child in value.values())
            elif type(value) is list:
                stack.extend((child, depth + 1) for child in value)
        json.dumps(result, ensure_ascii=False, allow_nan=False).encode('utf-8', errors='strict')
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise EvidenceError(f'invalid JSON/UTF-8: {exc}') from exc
    require(type(result) is dict, 'JSON record must be an object')
    return result


def bounded_read(path: Path, maximum: int) -> bytes:
    with path.open('rb') as handle:
        raw = handle.read(maximum + 1)
    require(len(raw) <= maximum, f'{path.name}: size limit exceeded')
    return raw


def extract_records(raw: bytes) -> dict[str, dict]:
    require(type(raw) is bytes and len(raw) <= MAX_RAW_BYTES, 'raw protocol size limit exceeded')
    try:
        text = raw.decode('utf-8', errors='strict')
    except UnicodeError as exc:
        raise EvidenceError('raw protocol is not UTF-8') from exc
    records = {}
    parcel_values = []
    prefix = 'INSTRUMENTATION_RESULT: '
    for line in text.split('\n'):
        line = line.removesuffix('\r')
        if not line.startswith(prefix):
            continue
        key, sep, payload = line[len(prefix):].partition('=')
        if not key.startswith(KEY_PREFIX):
            continue
        require(bool(sep), 'missing result-key separator')
        route = key[len(KEY_PREFIX):]
        require(route in ROUTES, f'unknown evidence route: {route}')
        require(route not in records, f'duplicate evidence route: {route}')
        require(not any(c in payload for c in '\v\f\x1c\x1d\x1e\x85\u2028\u2029'),
                'evidence payload contains a protocol line separator')
        encoded = payload.encode('utf-8')
        require(0 < len(encoded) <= MAX_RECORD_BYTES, f'{route}: record size limit exceeded')
        # A JSON string may contain escaped newlines, but the record must occupy one line.
        records[route] = strict_json(encoded)
        parcel_values.append((key, payload))
    require(set(records) == set(ROUTES), 'exactly one copy and one insert result required')
    # Android Bundle/ArrayMap: length + magic + count; each key is String16,
    # each value has a 4-byte VAL_STRING tag plus String16. Native producer also
    # checks actual Parcel.dataSize(); this is its two-string Bundle counterpart.
    def string16_size(value):
        units = len(value.encode('utf-16-le')) // 2
        return 4 + ((2 * (units + 1) + 3) // 4) * 4
    parcel_bytes = 12 + sum(string16_size(key) + 4 + string16_size(value)
                            for key, value in parcel_values)
    require(parcel_bytes <= MAX_BUNDLE_BYTES, 'two-record Parcel Bundle size limit exceeded')
    return records


@dataclass(frozen=True)
class Raster:
    width: int
    height: int
    rgba: bytes


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def decode_png(raw: bytes) -> Raster:
    """Validate CRC/chunk order/zlib bounds, then losslessly undo RGBA row filters."""
    require(0 < len(raw) <= MAX_PNG_BYTES, 'PNG size limit exceeded')
    require(raw.startswith(PNG_SIGNATURE), 'invalid PNG signature')
    position, width, height = len(PNG_SIGNATURE), 0, 0
    seen = set()
    compressed = bytearray()
    data_started = data_ended = finished = False
    while position < len(raw):
        require(position + 12 <= len(raw), 'truncated PNG chunk header')
        length, = struct.unpack_from('>I', raw, position)
        kind = raw[position + 4:position + 8]
        end = position + 12 + length
        require(end <= len(raw), 'truncated PNG chunk')
        require(re.fullmatch(rb'[A-Za-z]{4}', kind) is not None and 65 <= kind[2] <= 90,
                'invalid PNG chunk type')
        payload = raw[position + 8:position + 8 + length]
        crc, = struct.unpack_from('>I', raw, position + 8 + length)
        require((zlib.crc32(kind + payload) & 0xffffffff) == crc, 'PNG chunk CRC mismatch')
        require(seen or kind == b'IHDR', 'PNG IHDR must be first')
        if kind == b'IHDR':
            require(kind not in seen and length == 13, 'invalid or duplicate PNG IHDR')
            width, height, bits, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', payload)
            integer(width, 'PNG width', 1, MAX_DIMENSION)
            integer(height, 'PNG height', 1, MAX_DIMENSION)
            require(width * height <= MAX_PIXELS, 'PNG pixel allocation limit exceeded')
            require((bits, color, compression, filtering, interlace) == (8, 6, 0, 0, 0),
                    'PNG must be noninterlaced 8-bit RGBA')
        elif kind == b'IDAT':
            require(not data_ended, 'PNG IDAT chunks must be consecutive')
            data_started = True
            compressed.extend(payload)
        elif kind == b'IEND':
            require(data_started and length == 0, 'invalid PNG IEND or missing IDAT')
            require(end == len(raw), 'trailing bytes after PNG IEND')
            finished = True
        else:
            # Android may emit sBIT and colour-space metadata. None changes the
            # stored samples used for the native exact ARGB comparison.
            require(kind in (b'sBIT', b'sRGB', b'gAMA', b'cHRM', b'iCCP', b'pHYs'),
                    f'unsupported PNG chunk: {kind!r}')
            require(kind not in seen and not data_started, 'invalid PNG ancillary chunk order/duplicate')
            if kind == b'sBIT':
                require(payload == b'\x08\x08\x08\x08', 'PNG significant bits must remain RGBA8')
            elif kind == b'sRGB':
                require(length == 1 and payload[0] <= 3 and b'iCCP' not in seen, 'invalid PNG sRGB')
            elif kind == b'gAMA':
                require(length == 4 and int.from_bytes(payload, 'big') > 0, 'invalid PNG gAMA')
            elif kind == b'cHRM':
                require(length == 32, 'invalid PNG cHRM')
            elif kind == b'pHYs':
                require(length == 9 and payload[8] in (0, 1), 'invalid PNG pHYs')
            elif kind == b'iCCP':
                name, separator, profile = payload.partition(b'\0')
                require(1 <= len(name) <= 79 and bool(separator) and len(profile) > 1
                        and profile[0] == 0 and b'sRGB' not in seen, 'invalid PNG iCCP')
                # ICC data is intentionally not decompressed/applied. It is not
                # a pixel source and cannot alter this raw-sample comparison.
        seen.add(kind)
        if data_started and kind != b'IDAT':
            data_ended = True
        position = end
    require(finished and compressed, 'incomplete PNG')
    row_bytes = width * 4
    expected = (row_bytes + 1) * height
    inflater = zlib.decompressobj()
    try:
        scanlines = inflater.decompress(bytes(compressed), expected + 1)
    except zlib.error as exc:
        raise EvidenceError('invalid PNG deflate stream') from exc
    require(len(scanlines) == expected and inflater.eof and not inflater.unconsumed_tail
            and not inflater.unused_data, 'truncated, excessive, or trailing PNG deflate data')
    rgba = bytearray(width * height * 4)
    for y in range(height):
        start = y * (row_bytes + 1)
        filter_type = scanlines[start]
        require(filter_type <= 4, 'invalid PNG row filter')
        row = y * row_bytes
        encoded = scanlines[start + 1:start + 1 + row_bytes]
        if filter_type == 0:
            rgba[row:row + row_bytes] = encoded
            continue
        for x, value in enumerate(encoded):
            a = rgba[row + x - 4] if x >= 4 else 0
            b = rgba[row + x - row_bytes] if y else 0
            c = rgba[row + x - row_bytes - 4] if y and x >= 4 else 0
            prediction = (a if filter_type == 1 else b if filter_type == 2
                          else (a + b) // 2 if filter_type == 3 else _paeth(a, b, c))
            rgba[row + x] = (value + prediction) & 255
    return Raster(width, height, bytes(rgba))


def decode_image(record: dict, name: str) -> tuple[bytes, Raster]:
    require(type(record) is dict and set(record) == PNG_FIELDS, f'{name}: exact PNG metadata required')
    width = integer(record['width'], name + '.width', 1, MAX_DIMENSION)
    height = integer(record['height'], name + '.height', 1, MAX_DIMENSION)
    require(width * height <= MAX_PIXELS, f'{name}: pixel allocation limit exceeded')
    size = integer(record['bytes'], name + '.bytes', 1, MAX_PNG_BYTES)
    require(type(record['sha256']) is str and DIGEST.fullmatch(record['sha256']), f'{name}: invalid SHA256')
    encoded = record['base64']
    require(type(encoded) is str and 0 < len(encoded) <= 4 * ((MAX_PNG_BYTES + 2) // 3),
            f'{name}: invalid/bounded base64 required')
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise EvidenceError(f'{name}: malformed base64') from exc
    require(base64.b64encode(raw).decode('ascii') == encoded, f'{name}: noncanonical base64')
    require(len(raw) == size and sha256(raw) == record['sha256'], f'{name}: PNG byte count/hash mismatch')
    raster = decode_png(raw)
    require((raster.width, raster.height) == (width, height), f'{name}: PNG dimensions mismatch')
    return raw, raster


def recompute(actual: Raster, reference: Raster, box: tuple[int, int, int, int],
              origin_x: int, origin_y: int, content_width: int) -> dict[str, int]:
    """Same coordinate contract as the native oracle, with no tolerant comparisons."""
    left, top, _, _ = box
    counts = dict.fromkeys(COUNTS, 0)
    ink_left, ink_right = None, None
    actual_words = memoryview(actual.rgba).cast('I')
    reference_words = memoryview(reference.rgba).cast('I')
    for p in range(reference.width * reference.height):
        if reference.rgba[p * 4 + 3] == 0:
            continue
        y, x = divmod(p, reference.width)
        local_x, local_y = left + x, top + y
        counts['ink_pixels'] += 1
        ink_left = local_x if ink_left is None else min(ink_left, local_x)
        ink_right = local_x + 1 if ink_right is None else max(ink_right, local_x + 1)
        if x in (0, reference.width - 1) or y in (0, reference.height - 1):
            counts['allocation_edge_pixels'] += 1
        if local_x < 0 or local_x >= content_width:
            counts['horizontal_overflow_pixels'] += 1
        vx, vy = origin_x + local_x, origin_y + local_y
        if not (0 <= vx < actual.width and 0 <= vy < actual.height):
            counts['outside_view_pixels'] += 1
            counts['missing_expected_ink_pixels'] += 1
        elif actual.rgba[(vy * actual.width + vx) * 4 + 3] == 0:
            counts['missing_expected_ink_pixels'] += 1
    counts['ink_left'] = ink_left if ink_left is not None else 2147483647
    counts['ink_right_exclusive'] = ink_right if ink_right is not None else -2147483648
    for y in range(actual.height):
        ry = y - origin_y - top
        for x in range(actual.width):
            rx = x - origin_x - left
            expected = (reference_words[ry * reference.width + rx]
                        if 0 <= rx < reference.width and 0 <= ry < reference.height else 0)
            if actual_words[y * actual.width + x] != expected:
                counts['different_argb_pixels'] += 1
    return counts


@dataclass(frozen=True)
class VerifiedRecord:
    record: dict
    actual_png: bytes
    reference_png: bytes
    recomputed: dict[str, int]


def verify_record(record: dict, route: str, expected_source_sha256: str) -> VerifiedRecord:
    require(route in ROUTES, 'unsupported route')
    require(type(expected_source_sha256) is str and DIGEST.fullmatch(expected_source_sha256),
            'expected source digest must be lowercase SHA256')
    require(type(record) is dict and set(record) == FIELDS, f'{route}: exact schema fields required')
    exact = {'schema': 1, 'route': route, 'locale': 'ar', 'evidence_kind': EVIDENCE_KIND,
             'reference_source': REFERENCE_SOURCE, 'source_tests_sha256': expected_source_sha256,
             'font_scale': 2, 'api': 35, 'target_sdk': 35, 'orientation': 2,
             'view_use_bounds_for_width': True, 'layout_use_bounds_for_width': True,
             'shift_drawing_offset_for_start_overhang': False,
             'alpha_cutoff': 0, 'position_tolerance_px': 0, 'color_tolerance': 0}
    for name, expected in exact.items():
        require(type(record[name]) is type(expected) and record[name] == expected,
                f'{route}: incorrect {name}')
    for name in ('message', 'accessibility_text', 'complete_layout_text'):
        require(record[name] == MESSAGES[route], f'{route}: incorrect/incomplete {name}')
    require(type(record['fingerprint']) is str and 0 < len(record['fingerprint']) <= 1024
            and all(32 <= ord(c) <= 126 for c in record['fingerprint']), f'{route}: invalid fingerprint')
    require(type(record['default_textview_use_bounds_for_width']) is bool,
            f'{route}: default width flag must be boolean')
    density = number(record['density'], 'density', 0.1, 16)
    dpi = integer(record['density_dpi'], 'density_dpi', 16, 2560)
    require(abs(density * 160 - dpi) <= 0.0002, 'density/density_dpi disagree')
    root_w = integer(record['root_width'], 'root_width', 1, MAX_DIMENSION)
    root_h = integer(record['root_height'], 'root_height', 1, MAX_DIMENSION)
    require(root_w > root_h, 'landscape root dimensions required')
    x = integer(record['origin_x'], 'origin_x', 0, MAX_DIMENSION)
    y = integer(record['origin_y'], 'origin_y', 0, MAX_DIMENSION)
    content_width = integer(record['content_width'], 'content_width', 1, MAX_DIMENSION)
    inset = integer(record['measured_leading_inset_px'], 'measured_leading_inset_px', 0, MAX_DIMENSION)
    require(type(record['reference_box']) is str and len(record['reference_box']) <= 128, 'invalid reference_box')
    match = RECT.fullmatch(record['reference_box'])
    require(match is not None, 'reference_box must be Android Rect.toShortString')
    box = tuple(map(int, match.groups()))
    require(all(-100002 <= v <= 100002 for v in box), 'reference_box coordinate limit exceeded')
    require(type(record['glyph_bounds']) is str and len(record['glyph_bounds']) <= 256, 'invalid glyph_bounds')
    match = RECTF.fullmatch(record['glyph_bounds'])
    require(match is not None, 'glyph_bounds must be Android RectF.toString')
    glyph = tuple(map(float, match.groups()))
    require(all(math.isfinite(v) and abs(v) < 100000 for v in glyph)
            and glyph[0] <= glyph[2] and glyph[1] <= glyph[3], 'invalid finite glyph bounds')
    require(box[0] <= math.floor(min(0, glyph[0] - inset)) - 2
            and box[1] <= math.floor(min(0, glyph[1])) - 2
            and box[2] >= math.ceil(max(content_width, glyph[2] + inset)) + 2
            and box[3] >= math.ceil(max(0, glyph[3])) + 2,
            'reference_box omits complete geometry/allocation guards')
    actual_raw, actual = decode_image(record['actual_png'], 'actual_png')
    reference_raw, reference = decode_image(record['reference_png'], 'reference_png')
    require((box[2] - box[0], box[3] - box[1]) == (reference.width, reference.height),
            'reference_box and full PNG dimensions disagree')
    require(actual.width <= root_w and actual.height <= root_h, 'actual view exceeds root dimensions')
    require(x + content_width <= actual.width and y < actual.height, 'invalid actual-view origin/content width')
    for name in COUNTS:
        integer(record[name], name, -2147483648 if name in ('ink_left', 'ink_right_exclusive') else 0,
                2147483647 if name in ('ink_left', 'ink_right_exclusive') else MAX_PIXELS)
    observed = recompute(actual, reference, box, x, y, content_width)
    for name, count in observed.items():
        require(record[name] == count, f'{route}: reported {name} differs from full-raster recomputation')
    require(observed['ink_pixels'] > 0, f'{route}: complete reference contains no ink')
    for name in FAILURE_COUNTS:
        require(observed[name] == 0, f'{route}: nonzero {name}: {observed[name]}')
    require(any(actual.rgba[i] == 0 for i in range(3, len(actual.rgba), 4)),
            f'{route}: actual PNG must retain transparent background')
    return VerifiedRecord(record, actual_raw, reference_raw, observed)


def source_expected_inventory(expected_source_sha256: str, source_tests: Path = DEFAULT_SOURCE_TESTS) -> set[tuple[str, str]]:
    """Derive the exact ordinary-app phase from the same SDK-aware source inventory."""
    try:
        require(source_tests_sha256(source_tests) == expected_source_sha256,
                'checked-out app test source does not match expected source digest')
        return app_partition(declared_tests(source_tests, sdk_level=35), 35)['ordinary']
    except ValueError as exc:
        raise EvidenceError(f'cannot establish exact ordinary-app source inventory: {exc}') from exc


def verify_runner(raw: bytes, summary: dict, expected_source_sha256: str,
                  source_tests: Path = DEFAULT_SOURCE_TESTS) -> dict:
    """Reconcile all protocol outcome fields; never take success from extra results."""
    require(type(summary) is dict and summary.get('success') is True, 'successful runner summary required')
    require(summary.get('source_tests_sha256') == expected_source_sha256, 'runner source digest mismatch')
    require(type(summary.get('device_sdk')) is int and summary['device_sdk'] == 35, 'runner must capture API35')
    require(type(summary.get('returncode')) is int and summary['returncode'] == 0
            and summary.get('timed_out') is False, 'runner exited unsuccessfully or timed out')
    for field in ('errors', 'missing', 'unexpected'):
        require(summary.get(field) == [], f'runner {field} must be empty')
    cases = summary.get('cases')
    require(type(cases) is list and 0 < len(cases) <= 10000, 'nonempty bounded runner cases required')
    reported = set()
    for case in cases:
        require(type(case) is dict and set(case) == {'classname', 'name', 'status', 'message'},
                'invalid runner case fields')
        require(all(type(case[k]) is str and case[k] for k in ('classname', 'name'))
                and case['status'] == 'passed' and type(case['message']) is str, 'all runner cases must pass')
        identity = (case['classname'], case['name'])
        require(identity not in reported, 'duplicate runner case')
        reported.add(identity)
    require(PRODUCER_TEST in reported, 'producer test is absent from successful runner cases')
    expected = source_expected_inventory(expected_source_sha256, source_tests)
    require(reported == expected, 'runner cases differ from exact source-derived ordinary-app partition')
    for field in ('expected_tests', 'completed_tests'):
        require(type(summary.get(field)) is int and summary[field] == len(expected), 'runner inventory count mismatch')
    try:
        text = raw.decode('utf-8', errors='strict')
    except UnicodeError as exc:
        raise EvidenceError('raw protocol is not UTF-8') from exc
    parsed = parse_protocol(text, expected, returncode=summary['returncode'], timed_out=summary['timed_out'])
    require(parsed['success'] is True, 'raw instrumentation did not pass')
    for field, value in parsed.items():
        require(summary.get(field) == value, f'runner summary/raw protocol disagree: {field}')
    return parsed


def verify_capture(raw: bytes, expected_source_sha256: str, runner_summary: dict,
                   source_tests: Path = DEFAULT_SOURCE_TESTS) -> tuple[dict, dict[str, VerifiedRecord]]:
    require(type(expected_source_sha256) is str and DIGEST.fullmatch(expected_source_sha256),
            'expected source digest must be lowercase SHA256')
    records = extract_records(raw)
    protocol = verify_runner(raw, runner_summary, expected_source_sha256, source_tests)
    verified = {route: verify_record(records[route], route, expected_source_sha256) for route in ROUTES}
    for name in ('fingerprint', 'api', 'target_sdk', 'font_scale', 'density', 'density_dpi',
                 'root_width', 'root_height', 'orientation', 'default_textview_use_bounds_for_width'):
        require(records['copy'][name] == records['insert'][name], f'route device/profile mismatch: {name}')
    receipt = {'schema': 1, 'success': True, 'raw_output_sha256': sha256(raw),
               'source_tests_sha256': expected_source_sha256, 'device_sdk': 35,
               'producer_test': list(PRODUCER_TEST), 'runner_completed_tests': protocol['completed_tests'],
               'runner_inventory_scope': 'Exact API35 source-derived ordinary-app partition only; combined matrix remains separate',
               'evidence_kind': EVIDENCE_KIND,
               'scope': 'Full native software rasters; exact alpha>0 containment and whole-view raw ARGB. '
                        'Complete Layout/text comes from reviewed source-bound producer assertions; '
                        'caller must separately establish APK/build/run provenance.',
               'routes': {route: {'recomputed': item.recomputed,
                                  'actual_png_sha256': sha256(item.actual_png),
                                  'reference_png_sha256': sha256(item.reference_png)}
                          for route, item in verified.items()}}
    return receipt, verified


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-output', type=Path, required=True)
    parser.add_argument('--expected-source-sha256', required=True)
    parser.add_argument('--runner-summary', type=Path, required=True)
    parser.add_argument('--source-tests', type=Path, default=DEFAULT_SOURCE_TESTS,
                        help='Exact checkout app/src/androidTest used to derive ordinary-app inventory')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, help='Default: OUTPUT_DIR/receipt.json')
    args = parser.parse_args(argv)
    try:
        raw = bounded_read(args.raw_output, MAX_RAW_BYTES)
        summary_raw = bounded_read(args.runner_summary, MAX_SUMMARY_BYTES)
        receipt, verified = verify_capture(raw, args.expected_source_sha256, strict_json(summary_raw), args.source_tests)
        receipt['runner_summary_sha256'] = sha256(summary_raw)
        # No extraction occurs until both routes, the source and the run pass.
        # Do not overwrite an older capture or leave it looking like this one.
        require(not args.output_dir.exists(), 'output directory already exists; use a fresh capture directory')
        receipt_path = args.receipt or args.output_dir / 'receipt.json'
        require(not receipt_path.exists(), 'receipt already exists; refusing to overwrite')
        require(receipt_path.name not in ('copy.json', 'insert.json', 'copy-actual.png',
            'copy-reference.png', 'insert-actual.png', 'insert-reference.png'), 'receipt conflicts with extracted artifact')
        args.output_dir.mkdir(parents=True)
        for route, item in verified.items():
            (args.output_dir / f'{route}-actual.png').write_bytes(item.actual_png)
            (args.output_dir / f'{route}-reference.png').write_bytes(item.reference_png)
            (args.output_dir / f'{route}.json').write_text(
                json.dumps(item.record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        with receipt_path.open('x', encoding='utf-8') as handle:
            handle.write(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'success': True, 'receipt': str(receipt_path), 'routes': list(ROUTES)}))
        return 0
    except (EvidenceError, OSError) as exc:
        print(f'Installed glyph ink evidence rejected: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
