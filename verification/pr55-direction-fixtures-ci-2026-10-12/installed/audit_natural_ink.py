#!/usr/bin/env python3
"""Whole-reference installed raster metrics with zero pixel tolerance."""
import re,hashlib
import numpy as np
COUNT_FIELDS=('ink_pixels','ink_left','ink_right_exclusive','allocation_edge_pixels','horizontal_overflow_pixels','outside_view_pixels','missing_expected_ink_pixels','different_argb_pixels')
def require(v,msg):
    if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def reference_box(s):
    m=re.fullmatch(r'\[(-?\d+),(-?\d+)\]\[(-?\d+),(-?\d+)\]',s)
    require(m is not None,'invalid reference rectangle');return tuple(map(int,m.groups()))
def metrics(actual,reference,data):
    l,t,r,b=reference_box(data['reference_box']);h,w=reference.shape[:2];ah,aw=actual.shape[:2]
    require((r-l,b-t)==(w,h),'reference rectangle/dimensions mismatch')
    for name in ('origin_x','origin_y','content_width'):
        require(type(data[name]) is int,'invalid integer '+name)
    ox,oy,cw=data['origin_x'],data['origin_y'],data['content_width']
    require(w>0 and h>0 and w*h<=16_000_000 and ah*aw<=16_000_000 and cw>0,'invalid/big allocation')
    mask=reference[:,:,3]>0;ys,xs=np.nonzero(mask);require(len(xs)>0,'empty reference')
    lx=xs+l;ly=ys+t;vx=lx+ox;vy=ly+oy;inside=(vx>=0)&(vx<aw)&(vy>=0)&(vy<ah)
    missing=int(np.count_nonzero(~inside))
    missing+=int(np.count_nonzero(actual[vy[inside],vx[inside],3]==0))
    expected=np.zeros_like(actual)
    ax0=max(0,ox+l);ay0=max(0,oy+t);ax1=min(aw,ox+r);ay1=min(ah,oy+b)
    if ax1>ax0 and ay1>ay0:
        expected[ay0:ay1,ax0:ax1]=reference[ay0-oy-t:ay1-oy-t,ax0-ox-l:ax1-ox-l]
    return {'ink_pixels':len(xs),'ink_left':int(lx.min()),'ink_right_exclusive':int(lx.max())+1,
      'allocation_edge_pixels':int(np.count_nonzero((xs==0)|(ys==0)|(xs==w-1)|(ys==h-1))),
      'horizontal_overflow_pixels':int(np.count_nonzero((lx<0)|(lx>=cw))),
      'outside_view_pixels':int(np.count_nonzero(~inside)),
      'missing_expected_ink_pixels':missing,'different_argb_pixels':int(np.count_nonzero(np.any(actual!=expected,axis=2)))}
