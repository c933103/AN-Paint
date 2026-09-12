"""Generate AN Paint's synthetic JPEG XL colour fixtures; AGPL-3.0-or-later.

Requires the libjxl and Little CMS shared libraries (Debian libjxl0.7/liblcms2-2
were used for the checked-in fixtures). No image or profile is downloaded.
The JPEG XL bitstream remains independently decodable by the pinned Android
libjxl 0.12.0. ICC data is generated from the stated D65/P3/gamma2.2 parameters.
Output is base64 so Git/API publication preserves the exact binary content.
"""
import base64
import ctypes as C
import ctypes.util
import math
from pathlib import Path

U32=C.c_uint32
class Preview(C.Structure):
    _fields_=[('xsize',U32),('ysize',U32)]
class Animation(C.Structure):
    _fields_=[('tps_numerator',U32),('tps_denominator',U32),('num_loops',U32),('have_timecodes',C.c_int)]
class Basic(C.Structure):
    _fields_=[('have_container',C.c_int),('xsize',U32),('ysize',U32),
              ('bits_per_sample',U32),('exponent_bits_per_sample',U32),
              ('intensity_target',C.c_float),('min_nits',C.c_float),
              ('relative_to_max_display',C.c_int),('linear_below',C.c_float),
              ('uses_original_profile',C.c_int),('have_preview',C.c_int),('have_animation',C.c_int),
              ('orientation',C.c_int),('num_color_channels',U32),('num_extra_channels',U32),
              ('alpha_bits',U32),('alpha_exponent_bits',U32),('alpha_premultiplied',C.c_int),
              ('preview',Preview),('animation',Animation),('intrinsic_xsize',U32),('intrinsic_ysize',U32),
              ('padding',C.c_uint8*100)]
class Colour(C.Structure):
    _fields_=[('color_space',C.c_int),('white_point',C.c_int),('white_point_xy',C.c_double*2),
              ('primaries',C.c_int),('primaries_red_xy',C.c_double*2),
              ('primaries_green_xy',C.c_double*2),('primaries_blue_xy',C.c_double*2),
              ('transfer_function',C.c_int),('gamma',C.c_double),('rendering_intent',C.c_int)]
class PixelFormat(C.Structure):
    _fields_=[('num_channels',U32),('data_type',C.c_int),('endianness',C.c_int),('align',C.c_size_t)]
class xyY(C.Structure):
    _fields_=[('x',C.c_double),('y',C.c_double),('Y',C.c_double)]
class Primaries(C.Structure):
    _fields_=[('red',xyY),('green',xyY),('blue',xyY)]

def bind(lib,name,result,*arguments):
    f=getattr(lib,name);f.restype=result;f.argtypes=arguments;return f

jxl=C.CDLL(ctypes.util.find_library('jxl'))
create=bind(jxl,'JxlEncoderCreate',C.c_void_p,C.c_void_p)
destroy=bind(jxl,'JxlEncoderDestroy',None,C.c_void_p)
init=bind(jxl,'JxlEncoderInitBasicInfo',None,C.POINTER(Basic))
set_info=bind(jxl,'JxlEncoderSetBasicInfo',C.c_int,C.c_void_p,C.POINTER(Basic))
srgb=bind(jxl,'JxlColorEncodingSetToSRGB',None,C.POINTER(Colour),C.c_int)
set_colour=bind(jxl,'JxlEncoderSetColorEncoding',C.c_int,C.c_void_p,C.POINTER(Colour))
set_icc=bind(jxl,'JxlEncoderSetICCProfile',C.c_int,C.c_void_p,C.c_void_p,C.c_size_t)
settings=bind(jxl,'JxlEncoderFrameSettingsCreate',C.c_void_p,C.c_void_p,C.c_void_p)
lossless=bind(jxl,'JxlEncoderSetFrameLossless',C.c_int,C.c_void_p,C.c_int)
distance=bind(jxl,'JxlEncoderSetFrameDistance',C.c_int,C.c_void_p,C.c_float)
add=bind(jxl,'JxlEncoderAddImageFrame',C.c_int,C.c_void_p,C.POINTER(PixelFormat),C.c_void_p,C.c_size_t)
close=bind(jxl,'JxlEncoderCloseInput',None,C.c_void_p)
process=bind(jxl,'JxlEncoderProcessOutput',C.c_int,C.c_void_p,C.POINTER(C.POINTER(C.c_uint8)),C.POINTER(C.c_size_t))

def p3_gamma22_icc():
    lcms=C.CDLL(ctypes.util.find_library('lcms2'))
    gamma=bind(lcms,'cmsBuildGamma',C.c_void_p,C.c_void_p,C.c_double)
    new_profile=bind(lcms,'cmsCreateRGBProfile',C.c_void_p,C.POINTER(xyY),C.POINTER(Primaries),C.POINTER(C.c_void_p))
    save=bind(lcms,'cmsSaveProfileToMem',C.c_int,C.c_void_p,C.c_void_p,C.POINTER(U32))
    free=bind(lcms,'cmsFreeToneCurve',None,C.c_void_p)
    close_profile=bind(lcms,'cmsCloseProfile',None,C.c_void_p)
    curve=gamma(None,2.2)
    profile=new_profile(C.byref(xyY(.3127,.3290,1)),C.byref(Primaries(xyY(.68,.32,1),xyY(.265,.690,1),xyY(.150,.060,1))), (C.c_void_p*3)(curve,curve,curve))
    size=U32();assert save(profile,None,C.byref(size))
    data=(C.c_uint8*size.value)();assert save(profile,data,C.byref(size))
    close_profile(profile);free(curve)
    result=bytearray(data)
    # Deterministic profile timestamp; the profile ID was not calculated.
    result[24:36]=bytes.fromhex('07d000010001000000000000')
    return bytes(result)

def encode(name,values,bits=16,transfer=13,primaries=1,peak=255,icc=None,xyb=False):
    enc=create(None)
    try:
        info=Basic();init(C.byref(info));info.xsize=len(values);info.ysize=1
        info.bits_per_sample=bits;info.num_color_channels=3;info.uses_original_profile=0 if xyb else 1
        info.intensity_target=peak
        channels=len(values[0])
        if channels==4:info.alpha_bits=bits;info.num_extra_channels=1
        assert set_info(enc,C.byref(info))==0
        colour=Colour();srgb(C.byref(colour),0);colour.primaries=primaries;colour.transfer_function=transfer
        if icc is not None:
            icc_buffer=C.create_string_buffer(icc);assert set_icc(enc,icc_buffer,len(icc))==0
        else:assert set_colour(enc,C.byref(colour))==0
        frame=settings(enc,None);assert lossless(frame,0 if xyb else 1)==0
        if xyb:assert distance(frame,.01)==0
        # UINT16 is normalized to 0..65535; bits_per_sample independently sets
        # the actual 10-bit/16-bit codestream precision (not an 8-bit bitmap).
        samples=[round(max(0,min(1,c))*65535) for pixel in values for c in pixel]
        pixels=(C.c_uint16*len(samples))(*samples)
        fmt=PixelFormat(channels,3,0,0)
        assert add(frame,C.byref(fmt),pixels,C.sizeof(pixels))==0
        close(enc);result=bytearray()
        while True:
            buf=(C.c_uint8*65536)();next_out=C.cast(buf,C.POINTER(C.c_uint8));available=C.c_size_t(len(buf))
            status=process(enc,C.byref(next_out),C.byref(available));result.extend(bytes(buf[:len(buf)-available.value]))
            if status==0:break
            assert status==2,status
        dest=Path(__file__).resolve().parents[1]/'Paintroid/src/androidTest/assets/colour-fixtures'
        dest.mkdir(parents=True,exist_ok=True)
        (dest/(name+'.jxl.b64')).write_text(base64.b64encode(result).decode()+'\n')
        print(name,len(result),'bytes;',bits,'bits;',len(values),'pixels')
    finally:destroy(enc)

def pq(nits):
    m1=2610/16384;m2=2523/32;c1=3424/4096;c2=2413/128;c3=2392/128
    value=(nits/10000)**m1
    return ((c1+c2*value)/(1+c3*value))**m2

if __name__=='__main__':
    encode('linear16',[(v,v,v) for v in (0,.003,.018,.18,.5,1)],transfer=8)
    encode('linear16-hdr',[(v/1000,)*3 for v in (0,1,10,50,100,203,400,1000)],transfer=8,peak=1000)
    profile=p3_gamma22_icc()
    encode('p3-icc16',[(.8,.4,.2),(.2,.6,.4),(.3,.4,.7)],icc=profile)
    encode('p3-icc-alpha16',[(.8,.4,.2,a) for a in (0,.25,.5,1)],icc=profile)
    encode('pq10',[(pq(v),)*3 for v in (0,1,10,50,100,203,400,1000)],bits=10,transfer=16,primaries=9,peak=1000)
    encode('pq10-xyb',[(pq(v),)*3 for v in (0,1,10,50,100,203,400,1000)],bits=10,transfer=16,primaries=9,peak=1000,xyb=True)
    encode('pq10-alpha',[(pq(100),pq(100),pq(100),a) for a in (0,.25,.5,1)],bits=10,transfer=16,primaries=9,peak=1000)
    encode('pq10-chunks',[(pq((0,1,10,50,100,203,400,1000)[i%8]),)*3 for i in range(1031)],bits=10,transfer=16,primaries=9,peak=1000)
    encode('hlg10',[(v,v,v) for v in (0,.25,.5,.75,1)],bits=10,transfer=18,primaries=9,peak=1000)
