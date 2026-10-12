#!/usr/bin/env python3
"""Fresh migration diagnostic/readability audit. Prior exact-zero artifacts remain frozen."""
import json,re,hashlib,pathlib,math
import numpy as np
from PIL import Image
TAGS=('en-GB','ain-Kana','ain-Latn','bo','ryu','fr','ar','ja','vi-Hani')
CONTROL_TAGS=('en-GB','ain-Kana','bo','ar','ja','vi-Hani')
MUTATIONS=('left-overflow','right-overflow','wholly-left-of-view','wholly-right-of-view','clip-first-spatial-ink','clip-last-spatial-ink')
REF_SOURCE='Complete native Layout with API35 actual-glyph bounds; never an actual-view crop'
EVIDENCE='Robolectric NATIVE unmasked exact-raster diagnostic; consult hard JUnit checks and explicit review disposition'
COUNT_FIELDS=('ink_pixels','ink_left','ink_right_exclusive','allocation_edge_pixels','horizontal_overflow_pixels','outside_view_pixels','missing_expected_ink_pixels','different_argb_pixels')
def require(v,msg):
    if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read_json(p):
    def reject(x):raise ValueError('Nonfinite JSON '+x)
    return json.loads(p.read_bytes(),parse_constant=reject)
def read_rgba(p):
    with Image.open(p) as im:
        im.load();require(im.format=='PNG','not PNG');return np.array(im.convert('RGBA'))
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
    from scipy.ndimage import label
    labels,ncomponents=label(mask,structure=np.ones((3,3),dtype=bool))
    surviving=np.zeros(mask.shape,dtype=bool)
    surviving[ys[inside],xs[inside]]=actual[vy[inside],vx[inside],3]>0
    survivors=set(np.unique(labels[surviving]).tolist())-{0}
    missing_opaque=int(np.count_nonzero((reference[:,:,3]==255)&~surviving))
    return {'ink_components':int(ncomponents),'missing_complete_components':int(ncomponents)-len(survivors),'missing_opaque_reference_pixels':missing_opaque,'ink_pixels':len(xs),'ink_left':int(lx.min()),'ink_right_exclusive':int(lx.max())+1,
      'allocation_edge_pixels':int(np.count_nonzero((xs==0)|(ys==0)|(xs==w-1)|(ys==h-1))),
      'horizontal_overflow_pixels':int(np.count_nonzero((lx<0)|(lx>=cw))),
      'outside_view_pixels':int(np.count_nonzero(~inside)),
      'missing_expected_ink_pixels':missing,'different_argb_pixels':int(np.count_nonzero(np.any(actual!=expected,axis=2)))}
def check_frame(directory,stem):
    meta=directory/(stem+'.json');actualpath=directory/(stem+'-actual-textview.png');referencepath=directory/(stem+'-complete-layout.png')
    data=read_json(meta);a=read_rgba(actualpath);r=read_rgba(referencepath)
    require(data['reference_source']==REF_SOURCE and data['evidence_kind']==EVIDENCE,'frame source/evidence classification')
    for name in ('alpha_cutoff','position_tolerance_px','color_tolerance'):require(type(data[name]) is int and data[name]==0,'relaxed '+name)
    mode=not stem.endswith('-original-plain-before')
    for name in ('view_use_bounds_for_width','layout_use_bounds_for_width'):
        require(type(data[name]) is bool and data[name] is mode,'wrong bounds-width mode '+name)
    require(data['shift_drawing_offset_for_start_overhang'] is False,'shifted draw origin')
    inset=data['measured_leading_inset_px'];require(type(inset) is int and 0<=inset<100000,'invalid measured inset')
    if not mode:require(inset==0,'original plain control has a margin')
    m=re.fullmatch(r'RectF\(([-+0-9.eE]+), ([-+0-9.eE]+), ([-+0-9.eE]+), ([-+0-9.eE]+)\)',data['glyph_bounds'])
    require(m is not None,'invalid glyph bounds');g=tuple(map(float,m.groups()))
    require(all(math.isfinite(v) and abs(v)<100000 for v in g) and g[0]<=g[2] and g[1]<=g[3],'nonfinite/inverted glyph bounds')
    l,t,rr,b=reference_box(data['reference_box'])
    require(l<=math.floor(min(0,g[0]-inset))-2 and t<=math.floor(min(0,g[1]))-2 and rr>=math.ceil(max(data['content_width'],g[2]+inset))+2 and b>=math.ceil(max(0,g[3]))+2,'insufficient full glyph/margin allocation')
    measured=metrics(a,r,data)
    for k,v in measured.items():require(type(data[k]) is int and data[k]==v,'recomputed '+k+' differs')
    require(measured['allocation_edge_pixels']==0,'reference touches finite allocation edge')
    exact=all(measured[k]==0 for k in ('allocation_edge_pixels','horizontal_overflow_pixels','outside_view_pixels','missing_expected_ink_pixels','different_argb_pixels')) and measured['ink_pixels']>0
    require(data['exact_pixel_comparison_passed'] is exact and data['review_required'] is (not exact),'exact/review booleans disagree with unmasked pixels')
    require(data['component_scope']=='Eight-connected alpha>0 ink, not glyph segmentation; unexplained partial loss requires review','component scope differs')
    return data,a,r,{'stem':stem,'independent_metrics':measured,'files':[{'name':p.name,'sha256':sha(p.read_bytes())} for p in (meta,actualpath,referencepath)]}
def intact(data):
    require(data['ink_pixels']>0,'positive reference empty')
    for key in ('allocation_edge_pixels','missing_complete_components','missing_opaque_reference_pixels'):
        require(data[key]==0,'positive hard readability check fails '+key)
def tight_reference(r):
    y,x=np.nonzero(r[:,:,3]);return r[y.min():y.max()+1,x.min():x.max()+1]
def audit(directory,expected_messages):
    directory=pathlib.Path(directory);wanted={f'api35-{tag}-640x320-font{scale}-{action}':'live' for tag in TAGS for scale in (1.0,2.0) for action in ('copy','insert')}
    for tag in CONTROL_TAGS:
        for scale in (1.0,2.0):
            base=f'api35-{tag}-640x320-font{scale}-negative-controls'
            wanted[base+'-intact']='intact'
            wanted.update({base+'-'+name:name for name in MUTATIONS})
            wanted.update({base+'-reset-'+name:'reset' for name in ('width','font','mixed-paragraphs','short-message','restored')})
    wanted['api35-ar-640x320-font2.0-negative-controls-original-plain-before']='original-before'
    for scale in (1.0,2.0):
        base=f'api35-en-GB-640x320-font{scale}-negative-controls'
        wanted[base+'-complete-loss-intact']='complete-loss-intact'
        wanted.update({base+'-remove-'+name:'loss-'+name for name in ('whole-glyph','detached-mark','opaque-stroke')})
    summaries={f'{prefix}-font{scale}.json' for scale in (1.0,2.0) for prefix in ('native-negative-controls','native-inset-resets')}
    expected={stem+s for stem in wanted for s in ('.json','-actual-textview.png','-complete-layout.png')}|summaries
    present={p.name for p in directory.iterdir() if p.is_file()} if directory.exists() else set()
    missing=sorted(expected-present);extra=sorted(present-expected);errors=[];frames=[];computed=[];loaded={};receipts=[]
    for stem,kind in sorted(wanted.items()):
        if not {stem+s for s in ('.json','-actual-textview.png','-complete-layout.png')}<=present:continue
        try:
            data,a,r,record=check_frame(directory,stem)
            record['kind']=kind;computed.append(record)
            if kind in ('live','intact','reset','complete-loss-intact'):intact(data)
            elif kind=='original-before':require(data['horizontal_overflow_pixels']>0 and data['missing_expected_ink_pixels']>0,'original Arabic control did not reproduce real clipping')
            elif kind.startswith('loss-'):
                require(data['missing_expected_ink_pixels']>0,'content-loss control removed no ink')
                if kind=='loss-opaque-stroke':require(data['missing_complete_components']==0 and data['missing_opaque_reference_pixels']==1,'opaque guard not independent')
                else:require(data['missing_complete_components']>0,'complete-loss guard not reached')
            elif kind.startswith('clip-'):
                require(data['horizontal_overflow_pixels']==data['outside_view_pixels']==0,'clip failed unrelated containment')
                require(data['missing_expected_ink_pixels']>0 and data['different_argb_pixels']>0,'clip removed no expected ink')
            else:require(data['horizontal_overflow_pixels']>0,'translation did not overflow')
            record['kind']=kind;frames.append(record);loaded[stem]=(data,a,r)
        except Exception as ex:errors.append({'frame':stem,'error':str(ex)})
    for scale in (1.0,2.0):
        name=f'native-negative-controls-font{scale}.json'
        if name not in present:continue
        try:
            receipt=read_json(directory/name);require(isinstance(receipt,list) and len(receipt)==6,'control locale count')
            require({row['locale'] for row in receipt}==set(CONTROL_TAGS),'control locale inventory')
            for row in receipt:
                tag=row['locale'];require(row['font_scale']==scale and row['intact_structural_passed'] is True,'control identity/intact')
                require(type(row['logical_first_character_is_rtl']) is bool,'logical direction flag')
                base=f'api35-{tag}-640x320-font{scale}-negative-controls';idata,ia,ir=loaded[base+'-intact']
                require(row['intact_exact_pixel_comparison_passed'] is idata['exact_pixel_comparison_passed'] and row['review_required'] is idata['review_required'],'intact summary booleans')
                cases=row['cases'];require(len(cases)==6 and {c['mutation'] for c in cases}==set(MUTATIONS),'mutant inventory')
                for c in cases:
                    mutation=c['mutation'];md,ma,mr=loaded[base+'-'+mutation]
                    expectedcase={k:v for k,v in md.items() if k!='evidence_kind'}|{'mutation':mutation,'rejected':True,'reason':'clipped expected ink' if mutation.startswith('clip-') else 'horizontal painted-ink overflow'}
                    expectedcase|={'actual_draw_changed':True,'newly_missing_expected_ink_pixels':md['missing_expected_ink_pixels']-idata['missing_expected_ink_pixels'] if mutation.startswith('clip-') else None}
                    require(c==expectedcase,'summary differs from actual frame or intended rejection')
                    require(not np.array_equal(ma,ia),'mutant did not change actual draw')
                    require(md['ink_pixels']==idata['ink_pixels'],'reference glyph ink lost')
                    require((md['origin_x'],md['origin_y'],md['content_width'])==(idata['origin_x'],idata['origin_y'],idata['content_width']),'mutant changed content geometry')
                    if mutation.startswith('clip-'):
                        require(md['reference_box']==idata['reference_box'] and md['glyph_bounds']==idata['glyph_bounds'] and np.array_equal(mr,ir),'clip changed full reference')
                        require(md['missing_expected_ink_pixels']>idata['missing_expected_ink_pixels'],'clip did not add missing ink')
                        expected_actual=ia.copy()
                        if mutation=='clip-first-spatial-ink':expected_actual[:,:idata['origin_x']+idata['ink_left']+1]=0
                        else:expected_actual[:,idata['origin_x']+idata['ink_right_exclusive']-1:]=0
                        require(np.array_equal(ma,expected_actual),'actual clip differs from independent native clip expectation')
                    else:
                        delta={'left-overflow':-idata['ink_left']-1,'right-overflow':idata['content_width']-idata['ink_right_exclusive']+1,'wholly-left-of-view':-4*idata['content_width'],'wholly-right-of-view':4*idata['content_width']}[mutation]
                        require(md['ink_left']==idata['ink_left']+delta and md['ink_right_exclusive']==idata['ink_right_exclusive']+delta,'wrong spatial translation')
                        require(np.array_equal(tight_reference(mr),tight_reference(ir)),'translated reference changed glyph pixels')
                        shifted=np.zeros_like(ia);width=ia.shape[1]
                        if -width<delta<width:
                            if delta>=0:shifted[:,delta:]=ia[:,:width-delta]
                            else:shifted[:,:width+delta]=ia[:,-delta:]
                        require(np.array_equal(ma,shifted),'actual native translation differs from intact draw shifted and clipped')
                if tag=='en-GB':
                    controls=row['complete_loss_controls'];require(len(controls)==3,'complete loss control inventory')
                    fd,fa,fr=loaded[base+'-complete-loss-intact']
                    intact(fd);require(fd['exact_pixel_comparison_passed'] is True,'focused intact not exact')
                    for c in controls:
                        mutation=c['mutation'];require(mutation in ('remove-whole-glyph','remove-detached-mark','remove-opaque-stroke'),'unexpected complete-loss mutation')
                        md,ma,mr=loaded[base+'-'+mutation]
                        require(np.array_equal(fr,mr) and fd['reference_box']==md['reference_box'] and fd['glyph_bounds']==md['glyph_bounds'],'loss control changed independent reference')
                        changed=np.any(fa!=ma,axis=2);removed=(fa[:,:,3]>0)&(ma[:,:,3]==0)
                        require(np.array_equal(changed,removed) and np.count_nonzero(removed)==c['removed_native_ink_pixels'],'native loss modified something other than erased ink')
                        require(md['missing_expected_ink_pixels']==c['removed_native_ink_pixels'] and c['rejected'] is True,'loss rejection/count')
                        reason='opaque reference ink completely missing' if mutation=='remove-opaque-stroke' else 'complete reference ink component missing'
                        expectedcase={k:v for k,v in md.items() if k!='evidence_kind'}|{'mutation':mutation,'rejected':True,'reason':reason,'removed_native_ink_pixels':int(np.count_nonzero(removed))}
                        require(c==expectedcase,'focused control receipt differs')
                        if mutation=='remove-opaque-stroke':require(md['missing_complete_components']==0 and md['missing_opaque_reference_pixels']==1,'opaque loss control not independent')
                        else:require(md['missing_complete_components']==1,'whole glyph/mark did not remove exactly one native component')
                else:require('complete_loss_controls' not in row,'unexpected focused controls')
            receipts.append({'name':name,'sha256':sha((directory/name).read_bytes()),'intact_profiles':6,'rejected_native_mutants':39})
        except Exception as ex:errors.append({'summary':name,'error':str(ex)})
    for scale in (1.0,2.0):
        name=f'native-inset-resets-font{scale}.json'
        if name not in present:continue
        try:
            receipt=read_json(directory/name);require(isinstance(receipt,list) and len(receipt)==6,'reset locale count')
            wanted_profiles={f'api35-{tag}-640x320-font{scale}-negative-controls' for tag in CONTROL_TAGS}
            require({x['profile'] for x in receipt}==wanted_profiles,'reset profiles differ')
            for row in receipt:
                base=row['profile'];tag=next(t for t in CONTROL_TAGS if base==f'api35-{t}-640x320-font{scale}-negative-controls')
                require(row['repeat_count']==3 and row['all_structural_checks_passed'] is True,'reset/no-growth result differs')
                idata,ia,ir=loaded[base+'-intact'];require(row['initial_inset']==idata['measured_leading_inset_px'],'initial inset differs')
                cases=row['cases'];require(len(cases)==5 and {x['case'] for x in cases}=={'width','font','mixed-paragraphs','short-message','restored'},'reset case inventory')
                require(row['review_required'] is any(c['review_required'] for c in cases),'reset review-required aggregation')
                originals=[x['text_size_px'] for x in cases if x['case']!='font']
                require(len(set(originals))==1 and type(originals[0]) in (float,int) and originals[0]>0,'reset original paint sizes disagree')
                original_size=originals[0]
                for c in cases:
                    kind=c['case'];md,ma,mr=loaded[base+'-reset-'+kind]
                    msg=expected_messages[(tag,'copy')]
                    if kind=='mixed-paragraphs':msg+='\nABC\nالعربية'
                    if kind=='short-message':msg='OK'
                    size=original_size*.75 if kind=='font' else original_size
                    wanted_case={k:v for k,v in md.items() if k!='evidence_kind'}|{'case':kind,'message':msg,'text_size_px':size,'view_width':ma.shape[1]}
                    require(c==wanted_case,'reset receipt/paint/text/frame mismatch '+kind)
                    require(ma.shape[1]==ia.shape[1]-(48 if kind=='width' else 0),'reset width mismatch '+kind)
                    if kind=='short-message':require(md['measured_leading_inset_px']==0,'short message retained margin')
                    if kind=='restored':
                        require(md['measured_leading_inset_px']==row['initial_inset'],'restored inset differs')
                        require(md==idata and np.array_equal(ma,ia) and np.array_equal(mr,ir),'restored complete native state/pixels differ')
            receipts.append({'name':name,'sha256':sha((directory/name).read_bytes()),'profiles':6,'positive_reset_cases':30})
        except Exception as ex:errors.append({'summary':name,'error':str(ex)})
    return {'status':'PASS' if not (missing or extra or errors) else 'FAIL','expected_frames':len(wanted),'checked_frames':len(computed),'valid_frames':len(frames),'expected_positive_frames':110,'expected_original_clipping_counterfactuals':1,'expected_mutants':78,'missing':missing,'unexpected':extra,'errors':errors,'frames':computed,'control_receipts':receipts,'positive_review_required':[s for s,(d,_,_) in loaded.items() if wanted[s] in ('live','intact','reset','complete-loss-intact') and d['review_required']],'limits':'Diagnostic consistency and hard readability checks only; review-required positive differences still need explicit visual disposition. Requires current-source JVM identity reconciliation and external source/run/archive binding. No installed-device claim.'}
if __name__=='__main__':
    import argparse,sys
    p=argparse.ArgumentParser();p.add_argument('directory',type=pathlib.Path);p.add_argument('--messages',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args();messages={(r['locale'],r['action']):r['message'] for r in json.loads(args.messages.read_bytes())};result=audit(args.directory,messages);args.output.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['checked_frames'],'frames',len(result['errors']),'errors');sys.exit(0 if result['status']=='PASS' else 1)
