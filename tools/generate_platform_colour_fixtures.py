#!/usr/bin/env python3
"""AGPL-3.0-or-later. Synthetic test fixtures; no third-party photographs.
Uses host LittleCMS to generate a P3/gamma-2.2 profile and independent expected
sRGB pixels. Pillow writes independently encoded JPEG and WebP containers.
"""
import base64, ctypes as C, ctypes.util, io, json, struct, zlib
from pathlib import Path
from PIL import Image, ImageCms
ROOT=Path(__file__).resolve().parents[1]/'Paintroid/src/androidTest/assets/colour-fixtures'
ROOT.mkdir(parents=True,exist_ok=True)
lib=C.CDLL(ctypes.util.find_library('lcms2'))
class xyY(C.Structure): _fields_=[('x',C.c_double),('y',C.c_double),('Y',C.c_double)]
class Triple(C.Structure): _fields_=[('Red',xyY),('Green',xyY),('Blue',xyY)]
lib.cmsBuildGamma.argtypes=[C.c_void_p,C.c_double];lib.cmsBuildGamma.restype=C.c_void_p
lib.cmsCreateRGBProfile.argtypes=[C.POINTER(xyY),C.POINTER(Triple),C.POINTER(C.c_void_p)];lib.cmsCreateRGBProfile.restype=C.c_void_p
lib.cmsSaveProfileToMem.argtypes=[C.c_void_p,C.c_void_p,C.POINTER(C.c_uint32)];lib.cmsSaveProfileToMem.restype=C.c_int
lib.cmsCloseProfile.argtypes=[C.c_void_p];lib.cmsFreeToneCurve.argtypes=[C.c_void_p]
curve=lib.cmsBuildGamma(None,2.2);curves=(C.c_void_p*3)(curve,curve,curve)
profile=lib.cmsCreateRGBProfile(C.byref(xyY(.3127,.3290,1)),C.byref(Triple(xyY(.68,.32,1),xyY(.265,.69,1),xyY(.15,.06,1))),curves)
n=C.c_uint32();assert lib.cmsSaveProfileToMem(profile,None,C.byref(n));b=C.create_string_buffer(n.value);assert lib.cmsSaveProfileToMem(profile,b,C.byref(n));icc=b.raw[:n.value]
# Make the creation timestamp deterministic for committed fixtures.
icc=icc[:24]+struct.pack('>6H',2026,9,12,0,0,0)+icc[36:]
lib.cmsCloseProfile(profile);lib.cmsFreeToneCurve(curve)
src=ImageCms.ImageCmsProfile(io.BytesIO(icc));dst=ImageCms.createProfile('sRGB')
def chunk(t,data): return struct.pack('>I',len(data))+t+data+struct.pack('>I',zlib.crc32(t+data)&0xffffffff)
def png16(pixels,metadata):
    width=len(pixels)*8;height=8
    row=b'\0'+b''.join(struct.pack('>4H',*p)*8 for p in pixels)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,16,6,0,0,0))+b''.join(chunk(t,d) for t,d in metadata)+chunk(b'IDAT',zlib.compress(row*height))+chunk(b'IEND',b'')
def save(name,value): (ROOT/(name+'.b64')).write_text(base64.b64encode(value).decode()+'\n')
patches=[(32768,16384,49151,65535),(16384,32768,24576,32768),(5000,50000,30000,0),(40000,25000,15000,65535)]
save('platform-p3-alpha16.png',png16(patches,[(b'iCCP',b'AN Paint P3 test\0\0'+zlib.compress(icc))]))
image=Image.new('RGB',(32,8));palette=[tuple(round(c*255/65535) for c in p[:3]) for p in patches]
for y in range(8):
    for x in range(32): image.putpixel((x,y),palette[x//8])
expected=ImageCms.profileToProfile(image,src,dst,outputMode='RGB',renderingIntent=1)
(ROOT/'platform-expected.json').write_text(json.dumps({'p3_source':palette,'p3_srgb':[expected.getpixel((x*8+4,4)) for x in range(4)]},indent=2)+'\n')
for ext,kwargs in [('jpg',{'quality':100,'subsampling':0}),('webp',{'lossless':True})]:
    out=io.BytesIO();image.save(out,format='JPEG' if ext=='jpg' else 'WEBP',icc_profile=icc,**kwargs);save('platform-p3.'+ext,out.getvalue())
linear=[(x,x,x,65535) for x in (0,10000,32768,65535)]
save('platform-linear16.png',png16(linear,[(b'cICP',bytes([1,8,0,1]))]))
save('platform-gamma-linear16.png',png16(linear,[(b'gAMA',struct.pack('>I',100000))]))
save('platform-gamma-chroma16.png',png16(patches,[(b'gAMA',struct.pack('>I',45455)),(b'cHRM',struct.pack('>8I',31270,32900,68000,32000,26500,69000,15000,6000))]))
def pq(nits):
    m1=2610/16384;m2=2523/32;c1=3424/4096;c2=2413/128;c3=2392/128
    y=(nits/10000)**m1;return ((c1+c2*y)/(1+c3*y))**m2
hdr=[tuple([round(pq(n)*65535)]*3+[65535]) for n in [10,100,400,1000]]
save('platform-pq16.png',png16(hdr,[(b'cICP',bytes([9,16,0,1]))]))
# The same tagged HDR PNG also carries a conflicting P3 ICC: cICP must win.
save('platform-pq-priority16.png',png16(hdr,[(b'iCCP',b'conflicting P3\0\0'+zlib.compress(icc)),(b'cICP',bytes([9,16,0,1]))]))
print('Wrote platform colour fixtures',ROOT)
