#!/usr/bin/env python3
"""Independent Pillow/NumPy cross-check of the two decoded installed records.
Requires separately validated raw protocol, exact APK/test-source/run binding,
and the reviewed strict transport decoder. Does not establish those by itself.
"""
import argparse,base64,hashlib,io,json,pathlib
import numpy as np
from PIL import Image,__version__ as PIL_VERSION
from audit_natural_ink import metrics,COUNT_FIELDS
from audit_natural_artifacts import messages,TREE,HEAD,MERGE,RUN

def require(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def audit(repo,records):
    expected=messages(repo);rows=[]
    for route in ('copy','insert'):
        metadata=records/(route+'.json');d=json.loads(metadata.read_bytes())
        require(d['source_tests_sha256']=='f8f8de6d967000411de5dc6a3e8a8309b6fd61f2eba9e4393556e3ad35fafe3e','installed source digest mismatch')
        for key in ('message','accessibility_text','complete_layout_text'):
            require(d[key]==expected[('ar',route)],'incomplete/exact-source Arabic '+key)
        require(d['locale']=='ar' and d['api']==35 and d['target_sdk']==35 and d['font_scale']==2,'installed profile mismatch')
        for key in ('alpha_cutoff','color_tolerance','position_tolerance_px'):require(type(d[key]) is int and d[key]==0,'tolerance changed')
        require(d['view_use_bounds_for_width'] is True and d['layout_use_bounds_for_width'] is True and d['shift_drawing_offset_for_start_overhang'] is False,'width/draw mode mismatch')
        images={};pins={}
        for kind in ('actual','reference'):
            path=records/(route+'-'+kind+'.png');raw=path.read_bytes();entry=d[kind+'_png']
            require(base64.b64decode(entry['base64'],validate=True)==raw,'extracted image differs from full transport')
            require(sha(raw)==entry['sha256'] and len(raw)==entry['bytes'],'image digest/length differs')
            with Image.open(io.BytesIO(raw)) as im:
                im.load();require(im.format=='PNG' and im.mode=='RGBA','unsupported PNG representation')
                require(im.size==(entry['width'],entry['height']),'dimensions differ')
                images[kind]=np.array(im)
            pins[kind]={'sha256':sha(raw),'dimensions':[entry['width'],entry['height']]}
        found=metrics(images['actual'],images['reference'],d)
        require(found['ink_pixels']>0,'empty reference')
        for key in COUNT_FIELDS:
            require(type(d[key]) is int and d[key]==found[key],'independent full-raster metric differs '+key)
            if key not in ('ink_pixels','ink_left','ink_right_exclusive'):require(found[key]==0,'installed ink failure '+key)
        rows.append({'route':route,'json_sha256':sha(metadata.read_bytes()),'png':pins,'independent_metrics':found,'content_width':d['content_width'],'measured_inset':d['measured_leading_inset_px'],'default_textview_use_bounds_for_width':d['default_textview_use_bounds_for_width'],'root_dimensions':[d['root_width'],d['root_height']],'density':d['density'],'fingerprint':d['fingerprint']})
    return {'status':'PASS','tree':TREE,'head':HEAD,'merge':MERGE,'run_id':RUN,'pillow_version':PIL_VERSION,'routes':rows,'limits':'Pixel and exact-source string consistency of native software-raster records only. Requires separate strict transport/raw protocol/exact installed source/run/APK bindings, complete 104 identity matrix, actual visual inspection and compiled resource comparison. No hardware screenshot or real network-failure-route claim.'}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('repo','records','output'):p.add_argument('--'+key,type=pathlib.Path,required=True)
    a=p.parse_args();r=audit(a.repo,a.records);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
