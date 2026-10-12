#!/usr/bin/env python3
"""Audit emitted native mutant pairs even when a later failed intact case prevents a summary."""
import argparse,json,pathlib,numpy as np
import audit_painted_ink as a

def main():
 p=argparse.ArgumentParser();p.add_argument('directory',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args();root=args.directory;checked=[];absent=[]
 for scale in (1.0,2.0):
  for tag in a.CONTROL_TAGS:
   base=f'api35-{tag}-640x320-font{scale}-negative-controls'
   available=[m for m in a.MUTATIONS if (root/(base+'-'+m+'.json')).exists()]
   if not available:
    absent.append({'locale':tag,'scale':scale,'mutants_emitted':0});continue
   idata,ia,ir,_=a.check_frame(root,base+'-intact');a.intact(idata)
   for mutation in available:
    md,ma,mr,_=a.check_frame(root,base+'-'+mutation)
    a.require(md['ink_pixels']==idata['ink_pixels'],'reference lost ink')
    a.require((md['origin_x'],md['origin_y'],md['content_width'])==(idata['origin_x'],idata['origin_y'],idata['content_width']),'geometry changed')
    if mutation.startswith('clip-'):
     a.require(md['reference_box']==idata['reference_box'] and md['glyph_bounds']==idata['glyph_bounds'] and np.array_equal(mr,ir),'clip reference changed')
     expected=ia.copy()
     if mutation=='clip-first-spatial-ink':expected[:,:idata['origin_x']+idata['ink_left']+1]=0
     else:expected[:,idata['origin_x']+idata['ink_right_exclusive']-1:]=0
     a.require(np.array_equal(ma,expected),'actual clipping differs');a.require(md['missing_expected_ink_pixels']>0 and md['horizontal_overflow_pixels']==0 and md['outside_view_pixels']==0,'wrong clipping effect')
    else:
     dx={'left-overflow':-idata['ink_left']-1,'right-overflow':idata['content_width']-idata['ink_right_exclusive']+1,'wholly-left-of-view':-4*idata['content_width'],'wholly-right-of-view':4*idata['content_width']}[mutation]
     a.require(md['ink_left']==idata['ink_left']+dx and md['ink_right_exclusive']==idata['ink_right_exclusive']+dx and md['horizontal_overflow_pixels']>0,'wrong overflow')
     a.require(np.array_equal(a.tight_reference(mr),a.tight_reference(ir)),'native glyph pixels changed')
     expected=np.zeros_like(ia);w=ia.shape[1]
     if -w<dx<w:
      if dx>=0:expected[:,dx:]=ia[:,:w-dx]
      else:expected[:,:w+dx]=ia[:,-dx:]
     a.require(np.array_equal(ma,expected),'actual translation differs')
    checked.append({'locale':tag,'scale':scale,'mutation':mutation,'overflow_pixels':md['horizontal_overflow_pixels'],'removed_expected_pixels':md['missing_expected_ink_pixels']})
 result={'status':'AVAILABLE_PAIRS_MATCH_EXACT_NATIVE_MUTATIONS','checked_mutants':len(checked),'planned_mutants':72,'checked':checked,'profiles_without_mutants':absent,'acceptance':'INCOMPLETE: partial emitted controls cannot replace the missing double-scale completion receipt or the failed intact baseline.'};args.output.write_text(json.dumps(result,indent=2)+'\n');print(len(checked),'of 72 planned mutants independently matched; still incomplete')
if __name__=='__main__':main()
