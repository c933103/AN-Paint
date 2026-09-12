#!/usr/bin/env python3
"""Rebuild tiny original AVIF colour/alpha fixtures using FFmpeg/libaom.

The RGB code values are synthetic, losslessly encoded at 10 bits. The container
NCLX is authoritative (AV1 identity-matrix streams use the AV1 RGB defaults).
An ICC variant replaces that colr property and relocates iloc extents; its ICC is
our generated Display-P3/gamma2.2 profile, not third-party test artwork.
"""
from pathlib import Path
import base64
import math
import struct
import subprocess
import tempfile
from generate_jxl_colour_fixtures import p3_gamma22_icc

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Paintroid/src/androidTest/assets/colour-fixtures'

def boxes(data, start=0, end=None):
    end = len(data) if end is None else end
    while start < end:
        size, kind = struct.unpack_from('>I4s', data, start)
        assert size >= 8 and start + size <= end
        yield start, size, kind
        start += size

def with_icc(data, icc):
    def rebuild(data, start=0, end=None):
        result = bytearray()
        for pos, size, kind in boxes(data, start, end):
            payload = data[pos+8:pos+size]
            if kind == b'colr': payload = b'prof' + icc
            elif kind in (b'meta', b'iprp', b'ipco'):
                skip = 4 if kind == b'meta' else 0
                payload = payload[:skip] + rebuild(payload, skip)
            result += struct.pack('>I4s', len(payload)+8, kind) + payload
        return result
    output = rebuild(data)
    delta = len(output) - len(data)
    # FFmpeg emits version-0 iloc with absolute 32-bit offsets, no base offset.
    pos = output.index(b'iloc')+4
    assert output[pos:pos+6] == b'\0\0\0\0\x44\0'
    count = struct.unpack_from('>H',output,pos+6)[0]
    pos += 8
    for _ in range(count):
        pos += 4
        extents = struct.unpack_from('>H',output,pos)[0];pos += 2
        for _ in range(extents):
            old = struct.unpack_from('>I',output,pos)[0]
            struct.pack_into('>I',output,pos,old+delta)
            pos += 8
    return bytes(output)

def main():
    DEST.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp)
        def encode(name, patches, primaries, transfer, alpha=False, icc=False, bitstream_only=False):
            samples = []
            for c in (1,2,0): # GBR planar
                for y in range(32):
                    for x in range(64): samples.append(round(patches[x//8][c]*1023))
            if bitstream_only:
                samples = [round(patches[x//8][0]*1023) for y in range(32) for x in range(64)] + [512]*(64*32*2)
            raw = folder/'rgb.raw'; raw.write_bytes(struct.pack('<'+'H'*len(samples),*samples))
            args = ['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','yuv444p10le' if bitstream_only else 'gbrp10le','-video_size','64x32','-i',str(raw)]
            if alpha:
                raw_alpha=folder/'alpha.raw';raw_alpha.write_bytes(bytes([round((x//8)/7*255) for y in range(32) for x in range(64)]))
                args += ['-f','rawvideo','-pixel_format','gray','-video_size','64x32','-i',str(raw_alpha),'-map','0:v','-map','1:v']
            target=folder/'out.avif'
            args += ['-frames:v','1','-c:v','libaom-av1','-crf','0','-cpu-used','8','-color_primaries',primaries,'-color_trc',transfer,'-colorspace','bt2020nc' if bitstream_only else 'rgb','-color_range','pc']
            if bitstream_only: args += ['-pix_fmt','yuv444p10le']
            args += [str(target)]
            subprocess.run(args,check=True)
            data=target.read_bytes()
            if icc:data=with_icc(data,p3_gamma22_icc())
            if bitstream_only:
                # Keep all offsets/property indexes unchanged. The AV1 VUI now
                # supplies BT.2020/PQ; no colr property can mask its metadata.
                assert data.count(b'colrnclx') == 1
                data=data.replace(b'colrnclx',b'freenclx')
            (DEST/(name+'.avif.b64')).write_text(base64.b64encode(data).decode()+'\n')
        encode('heif-linear10',[(v,v,v) for v in (0,.05,.18,.25,.5,.75,.9,1)],'bt709','linear')
        def pq(nits):
            q=(nits/10000)**(2610/16384)
            return ((3424/4096+2413/128*q)/(1+2392/128*q))**(2523/32)
        encode('heif-pq10',[(pq(v),)*3 for v in (0,10,100,203,400,1000,4000,10000)],'bt2020','smpte2084')
        encode('heif-pq10-bitstream',[(pq(v),)*3 for v in (0,10,100,203,400,1000,4000,10000)],'bt2020','smpte2084',bitstream_only=True)
        encode('heif-hlg10',[(v,v,v) for v in (0,.1,.25,.5,.65,.75,.9,1)],'bt2020','arib-std-b67')
        encode('heif-p3-icc-alpha10',[(.5,.25,.75)]*8,'bt709','iec61966-2-1',alpha=True,icc=True)
        encode('heif-p3-icc10',[(.5,.25,.75)]*8,'bt709','iec61966-2-1',icc=True)
        hlg_patches=[(.77,.3,.45),(.4,.75,.4),(.3,.4,.75),(.7,.5,.3),(.5,.7,.3),(.3,.5,.7),(.5,.5,.5),(1,1,1)]
        encode('heif-p3-hlg10',hlg_patches,'smpte432','arib-std-b67')
        # Equivalent scene colours expressed in sRGB primaries. These reference
        # samples are generated from the standard P3-to-sRGB matrix, independently
        # of skcms/the decoder. Equality after HLG rendering checks that the OOTF
        # uses actual luminance, not hard-coded weights for a different primary set.
        matrix=((1.224940176,-.224940176,0),(-.042056955,1.042056955,0),(-.019637555,-.078636046,1.098273601))
        def inverse_hlg(v):return v*v/3 if v<=.5 else (math.exp((v-.55991073)/.17883277)+.28466892)/12
        def forward_hlg(v):return math.sqrt(3*v) if v<=1/12 else .17883277*math.log(12*v-.28466892)+.55991073
        converted=[]
        for pixel in hlg_patches:
            scene=[inverse_hlg(v) for v in pixel]
            target=[sum(row[c]*scene[c] for c in range(3)) for row in matrix]
            assert all(-.00001<=v<=1.00001 for v in target)
            converted.append(tuple(forward_hlg(max(0,min(1,v))) for v in target))
        encode('heif-srgb-hlg-equivalent10',converted,'bt709','arib-std-b67')
        encode('heif-p3-nclx10',[(.5,.25,.75)]*8,'smpte432','iec61966-2-1')

if __name__ == '__main__':main()
