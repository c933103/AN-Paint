#!/usr/bin/env python3
"""AGPL-3.0-or-later. Generate synthetic TIFF fixtures without the app codec.

Pillow/libtiff supplies LZW, PackBits, CCITT and JPEG interoperability fixtures.
A small, independent TIFF serializer supplies deterministic metadata/storage
variants that Pillow cannot write. Host Pillow reads every supported fixture as
an independent structural check. No downloaded photographs or profiles are used.
"""
import base64
import ctypes as C
import ctypes.util
import io
import json
import struct
import tempfile
import zlib
from pathlib import Path

from PIL import Image, features, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1] / 'Paintroid/src/androidTest/assets/tiff-fixtures'
ROOT.mkdir(parents=True, exist_ok=True)
MANIFEST = {'generator': {'pillow': pillow_version, 'libtiff': features.version('libtiff'),
                          'lcms': features.version('littlecms2')}, 'fixtures': {}}


def pattern(width=19, height=13):
    return [[(17*x + 3*y) % 256, (5*x + 29*y) % 256,
             (11*x + 7*y) % 256, 255] for y in range(height) for x in range(width)]


def write(name, data, size=None, pixels=None, tolerance=0, description=''):
    (ROOT / (name + '.tif.b64')).write_text(base64.b64encode(data).decode() + '\n')
    item = {'description': description}
    if size:
        item.update(width=size[0], height=size[1], tolerance=tolerance, rgba=pixels)
    MANIFEST['fixtures'][name] = item


def tiff(width, height, samples, bits=8, photo=2, channels=3, *, endian='<',
         big=False, tile=False, planar=False, orientation=1, compression=1,
         alpha=None, palette=None, icc=None, sample_format=1, invalid_offset=False,
         additional_tags=None):
    """samples are stored pixel tuples; pack TIFF rows independently of libtiff."""
    def row(values):
        if bits == 8:
            return bytes(values)
        if bits == 16:
            return struct.pack(endian + 'H'*len(values), *values)
        packed = bytearray((len(values)*bits+7)//8)
        for index, value in enumerate(values):
            packed[index*bits//8] |= value << (8-bits-(index*bits % 8))
        return bytes(packed)

    blocks = []
    block_w, block_h = (16, 16) if tile else (width, 5)
    for plane in range(channels if planar else 1):
        for top in range(0, height, block_h):
            for left in range(0, width, block_w):
                block = bytearray()
                for y in range(top, top+block_h if tile else min(top+block_h, height)):
                    values = []
                    for x in range(left, left+block_w):
                        value = samples[y*width+x] if x < width and y < height else [0]*channels
                        values.extend([value[plane]] if planar else value)
                    block += row(values)
                blocks.append(zlib.compress(block) if compression == 8 else bytes(block))

    # Values are type/count/bytes. Offset arrays are replaced once metadata size is known.
    tags = {}
    def tag(number, kind, values):
        if isinstance(values, bytes):
            count, data = len(values), values
        else:
            count = len(values)
            data = struct.pack(endian + {3:'H', 4:'I', 16:'Q'}[kind]*count, *values)
        tags[number] = (kind, count, data)
    tag(256, 4, [width]); tag(257, 4, [height]); tag(258, 3, [bits]*channels)
    tag(259, 3, [compression]); tag(262, 3, [photo]); tag(274, 3, [orientation])
    tag(277, 3, [channels]); tag(284, 3, [2 if planar else 1])
    tag(339, 3, [sample_format]*channels)
    offset_tag, count_tag = (324, 325) if tile else (273, 279)
    if tile:
        tag(322, 4, [block_w]); tag(323, 4, [block_h])
    else:
        tag(278, 4, [block_h])
    offset_kind = 16 if big else 4
    tag(offset_tag, offset_kind, [0]*len(blocks)); tag(count_tag, offset_kind, [len(b) for b in blocks])
    if alpha is not None:
        tag(338, 3, [alpha])
    if palette is not None:
        tag(320, 3, [c for channel in range(3) for p in palette for c in [p[channel]*257]])
    if icc:
        tag(34675, 7, icc)
    for number, kind, values in additional_tags or []:
        tag(number, kind, values)

    header_size, entry_size, inline = (16, 20, 8) if big else (8, 12, 4)
    data_start = header_size + (8 if big else 2) + len(tags)*entry_size + (8 if big else 4)
    for _, _, data in tags.values():
        if len(data) > inline:
            data_start += (len(data)+1)//2*2
    offsets = []
    position = data_start
    for block in blocks:
        offsets.append(0xfffffffffffffff0 if big and invalid_offset else
                       0xfffffff0 if invalid_offset else position)
        position += len(block)
    tag(offset_tag, offset_kind, offsets)

    out = bytearray((b'II' if endian == '<' else b'MM') +
                    (struct.pack(endian+'HHHQ', 43, 8, 0, 16) if big else
                     struct.pack(endian+'HI', 42, 8)))
    out += struct.pack(endian+('Q' if big else 'H'), len(tags))
    extra = bytearray()
    extra_start = header_size + (8 if big else 2) + len(tags)*entry_size + (8 if big else 4)
    for number, (kind, count, data) in sorted(tags.items()):
        out += struct.pack(endian+('HHQ' if big else 'HHI'), number, kind, count)
        if len(data) <= inline:
            out += data.ljust(inline, b'\0')
        else:
            out += struct.pack(endian+('Q' if big else 'I'), extra_start+len(extra))
            extra += data
            if len(extra) % 2:
                extra += b'\0'
    out += bytes(8 if big else 4) + extra + b''.join(blocks)
    return bytes(out)


def combine_pages(pages):
    """Relocate independently serialized one-page TIFFs into a main-IFD chain."""
    endian = '<' if pages[0][:2] == b'II' else '>'
    big = struct.unpack_from(endian+'H', pages[0], 2)[0] == 43
    ptr_format, inline, count_bytes, entry_bytes = ('Q', 8, 8, 20) if big else ('I', 4, 2, 12)
    pointer_at = 8 if big else 4
    bases, position = [], 0
    for page in pages:
        bases.append(position)
        position += (len(page)+1)//2*2
    output = bytearray()
    for index, original in enumerate(pages):
        assert original[:4] == pages[0][:4]
        page = bytearray(original)
        base = bases[index]
        directory = struct.unpack_from(endian+ptr_format, page, pointer_at)[0]
        count = struct.unpack_from(endian+('Q' if big else 'H'), page, directory)[0]
        for entry_index in range(count):
            at = directory + count_bytes + entry_index*entry_bytes
            tag, kind = struct.unpack_from(endian+'HH', original, at)
            elements = struct.unpack_from(endian+('Q' if big else 'I'), original, at+4)[0]
            data_at = at + (12 if big else 8)
            size = {3:2, 4:4, 7:1, 16:8}[kind] * elements
            if size > inline:
                data_at = struct.unpack_from(endian+ptr_format, original, data_at)[0]
                struct.pack_into(endian+ptr_format, page, at+(12 if big else 8), data_at+base)
            if tag in (273, 324):
                number_format = {3:'H', 4:'I', 16:'Q'}[kind]
                unit = struct.calcsize(number_format)
                for n in range(elements):
                    old = struct.unpack_from(endian+number_format, original, data_at+n*unit)[0]
                    struct.pack_into(endian+number_format, page, data_at+n*unit, old+base)
        next_pointer = directory + count_bytes + count*entry_bytes
        next_offset = 0 if index+1 == len(pages) else bases[index+1] + struct.unpack_from(endian+ptr_format,pages[index+1],pointer_at)[0]
        struct.pack_into(endian+ptr_format,page,next_pointer,next_offset)
        output += page
        if len(output) % 2:
            output += b'\0'
    return bytes(output)


def image_bytes(image, **options):
    output = io.BytesIO()
    image.save(output, format='TIFF', **options)
    return output.getvalue()


def linear_icc(gray=False):
    lib = C.CDLL(ctypes.util.find_library('lcms2'))
    class xyY(C.Structure):
        _fields_ = [('x', C.c_double), ('y', C.c_double), ('Y', C.c_double)]
    class Triple(C.Structure):
        _fields_ = [('Red', xyY), ('Green', xyY), ('Blue', xyY)]
    lib.cmsBuildGamma.argtypes = [C.c_void_p, C.c_double]
    lib.cmsBuildGamma.restype = C.c_void_p
    lib.cmsCreateRGBProfile.argtypes = [C.POINTER(xyY), C.POINTER(Triple), C.POINTER(C.c_void_p)]
    lib.cmsCreateRGBProfile.restype = C.c_void_p
    lib.cmsCreateGrayProfile.argtypes = [C.POINTER(xyY), C.c_void_p]
    lib.cmsCreateGrayProfile.restype = C.c_void_p
    lib.cmsSaveProfileToMem.argtypes = [C.c_void_p, C.c_void_p, C.POINTER(C.c_uint32)]
    lib.cmsSaveProfileToMem.restype = C.c_int
    lib.cmsCloseProfile.argtypes = [C.c_void_p]
    lib.cmsFreeToneCurve.argtypes = [C.c_void_p]
    curve = lib.cmsBuildGamma(None, 1.0)
    white = xyY(.3127, .3290, 1)
    curves = (C.c_void_p*3)(curve, curve, curve)
    primaries = Triple(xyY(.64, .33, 1), xyY(.30, .60, 1), xyY(.15, .06, 1))
    profile = lib.cmsCreateGrayProfile(C.byref(white), curve) if gray else \
        lib.cmsCreateRGBProfile(C.byref(white), C.byref(primaries), curves)
    count = C.c_uint32()
    assert lib.cmsSaveProfileToMem(profile, None, C.byref(count))
    data = C.create_string_buffer(count.value)
    assert lib.cmsSaveProfileToMem(profile, data, C.byref(count))
    icc = data.raw[:count.value]
    icc = icc[:24] + struct.pack('>6H', 2026, 9, 13, 0, 0, 0) + icc[36:]
    lib.cmsCloseProfile(profile); lib.cmsFreeToneCurve(curve)
    return icc


def normalized(value):
    return (value*255+32767)//65535


def linear_srgb(value):
    x = value/65535
    return round(255*(12.92*x if x <= .0031308 else 1.055*x**(1/2.4)-.055))


pixels = pattern()
rgb = [p[:3] for p in pixels]
for name, args in [('strips-le', {}), ('strips-be', {'endian':'>'}),
                   ('bigtiff-le', {'big':True}), ('bigtiff-be', {'big':True, 'endian':'>'}),
                   ('planar-separate', {'planar':True}), ('deflate-strips', {'compression':8})]:
    write(name, tiff(19, 13, rgb, **args), (19, 13), pixels)

tile_pixels = pattern(35, 19)
for name, args in [('tiles-deflate', {}), ('tiles-planar-deflate', {'planar':True})]:
    write(name, tiff(35, 19, [p[:3] for p in tile_pixels], tile=True, compression=8, **args),
          (35, 19), tile_pixels, description='16x16 tiles with partial right and bottom edges')

image = Image.new('RGB', (19, 13))
image.putdata([tuple(p[:3]) for p in pixels])
for name, compression in [('lzw', 'tiff_lzw'), ('packbits', 'packbits')]:
    write(name, image_bytes(image, compression=compression), (19, 13), pixels)
write('lzw-predictor', image_bytes(image, compression='tiff_lzw', tiffinfo={317:2}),
      (19, 13), pixels, description='LZW plus horizontal differencing predictor')

bilevel = Image.new('1', (19, 13))
bilevel.putdata([255 if (x//3+y//2) % 2 else 0 for y in range(13) for x in range(19)])
mono_pixels = [[v, v, v, 255] for v in bilevel.convert('L').get_flattened_data()]
for name, compression in [('ccitt-group3', 'group3'), ('ccitt-group4', 'group4')]:
    write(name, image_bytes(bilevel, compression=compression), (19, 13), mono_pixels)

jpeg = Image.new('RGB', (32, 16))
jpeg.putdata([(40+x*5, 50+y*8, 80+x+y) for y in range(16) for x in range(32)])
jpeg_data = image_bytes(jpeg, compression='jpeg', quality=95)
jpeg_reference = Image.open(io.BytesIO(jpeg_data)).convert('RGBA')
write('jpeg', jpeg_data, jpeg.size, [list(p) for p in jpeg_reference.get_flattened_data()], 3,
      'Reference decoded by independent host Pillow/libtiff; tolerance covers JPEG library rounding')

for orientation in range(1, 9):
    w, h = ((13, 19) if orientation >= 5 else (19, 13))
    transformed = []
    for y in range(h):
        for x in range(w):
            sx, sy = {1:(x,y), 2:(18-x,y), 3:(18-x,12-y), 4:(x,12-y),
                      5:(y,x), 6:(y,12-x), 7:(18-y,12-x), 8:(18-y,x)}[orientation]
            transformed.append(pixels[sy*19+sx])
    write(f'orientation-{orientation}', tiff(19, 13, rgb, orientation=orientation),
          (w, h), transformed, description='Expected coordinates from TIFF Orientation specification')

for bits in (1, 2, 4, 8):
    values = [(x+3*y) % (1 << bits) for y in range(13) for x in range(19)]
    for photo, name in [(1, 'black'), (0, 'white')]:
        expected = [round(v*255/((1 << bits)-1)) for v in values]
        if photo == 0:
            expected = [255-v for v in expected]
        write(f'gray{bits}-{name}', tiff(19, 13, [[v] for v in values], bits=bits, photo=photo, channels=1),
              (19, 13), [[v,v,v,255] for v in expected])

for bits in (4, 8):
    palette = [[(i*37) % 256, (i*71) % 256, (i*113) % 256] for i in range(1 << bits)]
    indices = [(x+3*y) % len(palette) for y in range(13) for x in range(19)]
    write(f'palette{bits}', tiff(19, 13, [[i] for i in indices], bits=bits, photo=3, channels=1, palette=palette),
          (19, 13), [palette[i]+[255] for i in indices])

values = [0, 1, 128, 256, 257, 1000, 10000, 32768, 60000, 65535]
write('gray16', tiff(10, 1, [[v] for v in values], bits=16, photo=1, channels=1),
      (10, 1), [[normalized(v)]*3+[255] for v in values], 1)
samples16 = [[v, values[(i+3) % 10], values[(i+6) % 10]] for i, v in enumerate(values)]
for name, args in [('rgb16-be', {'endian':'>'}), ('rgb16-planar', {'planar':True})]:
    write(name, tiff(10, 1, samples16, bits=16, **args), (10, 1),
          [[normalized(v) for v in p]+[255] for p in samples16], 1)

linear_values = [0, 1, 2, 16, 64, 128, 196, 1000, 1179, 11800, 32768, 65535]
for gray, name in [(False, 'linear-rgb16-icc'), (True, 'linear-gray16-icc')]:
    channels = 1 if gray else 3
    write(name, tiff(12, 1, [[v]*channels for v in linear_values], bits=16,
                    channels=channels, photo=1 if gray else 2, icc=linear_icc(gray)),
          (12, 1), [[linear_srgb(v)]*3+[255] for v in linear_values], 1,
          'Expected IEC 61966-2-1 transfer applied to original 16-bit linear samples before 8-bit rounding')

alphas = [0, 64, 128, 255]
unassociated = [[200,100,50,a] for a in alphas]
associated = [[round(c*a/255) for c in [200,100,50]]+[a] for a in alphas]
expected_alpha = [[200,100,50,a] if a else [0,0,0,0] for a in alphas]
write('alpha-unassociated', tiff(4, 1, unassociated, channels=4, alpha=2), (4, 1), expected_alpha, 2)
write('alpha-associated', tiff(4, 1, associated, channels=4, alpha=1), (4, 1), expected_alpha, 2)
write('alpha16-unassociated', tiff(4, 1, [[51400,25700,12850,a*257] for a in alphas],
                                 bits=16, channels=4, alpha=2), (4, 1), expected_alpha, 2)

second = Image.new('RGB', (7, 3), (255, 0, 0))
write('multipage', image_bytes(image, save_all=True, append_images=[second]), (19, 13), pixels,
      description='First page 19x13 pattern, second page 7x3 red; selectable pages')
for name, args in [('multipage-classic-be', {'endian':'>'}),
                   ('multipage-bigtiff-le', {'big':True}),
                   ('multipage-bigtiff-be', {'big':True,'endian':'>'})]:
    pages = [tiff(19,13,rgb,**args),
             tiff(7,3,[p[:3] for p in pattern(7,3)],orientation=6,**args),
             tiff(2,2,[[0,255,0]]*4,**args)]
    write(name,combine_pages(pages),(19,13),pixels,
          description='Three selectable pages:19x13 pattern;7x3 pattern with orientation6(display3x7);2x2 green')
chain = bytearray(tiff(19,13,rgb))
first = struct.unpack_from('<I',chain,4)[0]
next_pointer = first+2+struct.unpack_from('<H',chain,first)[0]*12
struct.pack_into('<I',chain,next_pointer,first)
write('invalid-page-cycle',bytes(chain),description='Main-IFD next pointer cycles to itself')
struct.pack_into('<I',chain,next_pointer,len(chain)+100)
write('invalid-page-chain',bytes(chain),description='Next main-IFD lies outside the file')
tiny_page = tiff(1,1,[[255,0,0]])
write('too-many-pages',combine_pages([tiny_page]*4097),description='4097 valid mainIFDs exceed the explicit4096-page limit')
write('invalid-offset', tiff(19, 13, rgb, invalid_offset=True), description='Strip addresses outside the file')
write('truncated', tiff(19, 13, rgb)[:-50], description='Last strip lacks 50 declared sample bytes')
write('invalid-magic', b'not a TIFF file\0\1\2', description='No TIFF signature')
for name, mode in [('unsupported-cmyk','CMYK'), ('unsupported-lab','LAB'), ('unsupported-float','F')]:
    write(name, image_bytes(Image.new(mode, (4, 3))), description=f'Unsupported {mode} photometric/sample format')
transfer_curve = [round((value/255)**2.2*65535) for value in range(256)]
write('unsupported-transfer-function',
      tiff(19, 13, rgb, additional_tags=[(301, 3, transfer_curve*3)]),
      description='RGB samples with TIFF TransferFunction calibration and no ICC; reject unsupported colour interpretation')
write('invalid-icc', tiff(19, 13, rgb, icc=b'not a valid ICC profile'),
      description='Embedded ICC bytes do not form a usable profile; never silently assume sRGB')
write('mismatched-gray-icc', tiff(19, 13, rgb, icc=linear_icc(gray=True)),
      description='Valid grayscale ICC attached to three-channel RGB samples; reject mismatched profile colour space')

# Check byte-level interoperability without using the Android implementation.
checked = 0
for name, item in MANIFEST['fixtures'].items():
    if 'rgba' not in item:
        continue
    data = base64.b64decode((ROOT / (name+'.tif.b64')).read_text())
    if name == 'bigtiff-be' or name == 'multipage-bigtiff-be':
        # Pillow 12.3's EXIF parser rejects big-endian BigTIFF. Validate using
        # stock host libtiff directly, including every decoded RGB scanline.
        lib = C.CDLL(ctypes.util.find_library('tiff'))
        lib.TIFFOpen.argtypes = [C.c_char_p, C.c_char_p]; lib.TIFFOpen.restype = C.c_void_p
        lib.TIFFReadScanline.argtypes = [C.c_void_p, C.c_void_p, C.c_uint32, C.c_uint16]
        lib.TIFFClose.argtypes = [C.c_void_p]
        with tempfile.NamedTemporaryFile(suffix='.tif') as temporary:
            temporary.write(data); temporary.flush()
            handle = lib.TIFFOpen(temporary.name.encode(), b'r')
            assert handle
            try:
                row = C.create_string_buffer(item['width']*3)
                for y in range(item['height']):
                    assert lib.TIFFReadScanline(handle, row, y, 0) == 1
                    expected = bytes(c for p in item['rgba'][y*item['width']:(y+1)*item['width']] for c in p[:3])
                    assert row.raw == expected
            finally:
                lib.TIFFClose(handle)
        checked += 1
        continue
    with Image.open(io.BytesIO(data)) as decoded:
        decoded.load()
        assert decoded.size == (item['width'], item['height']), (name, decoded.size)
        # Pillow intentionally truncates 16-bit RGB to 8 bits and does not apply
        # ICC here; only use it as a format/parser oracle for those fixtures.
        if '16' not in name and not name.startswith('alpha'):
            actual = list(decoded.convert('RGBA').get_flattened_data())
            assert len(actual) == len(item['rgba'])
            error = max(abs(a-b) for p,q in zip(actual, item['rgba']) for a,b in zip(p,q))
            assert error <= item['tolerance'], (name, error)
    checked += 1
MANIFEST['generator']['independently_readable_fixtures'] = checked
(ROOT / 'expected.json').write_text(json.dumps(MANIFEST, separators=(',', ':'))+'\n')
print(f'Wrote {len(MANIFEST["fixtures"])} fixtures; host Pillow/libtiff validated {checked}: {ROOT}')
