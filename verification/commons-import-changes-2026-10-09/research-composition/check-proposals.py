#!/usr/bin/env python3
"""Frozen-review structural checks only; not a fluency or rendering test."""
from pathlib import Path
import hashlib, json, re, xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
p=HERE.parent/'research-specialist/proposals.json'
raw=p.read_bytes(); j=json.loads(raw); tr=j['translations']
assert set(tr)=={'ain-Kana','ain-Latn','bo','dz','hak-Hant-TW','hak-Latn-TW','jje','mn-Mong','mnc-Mong','ryu','vi-Hani'}
svg='commons_import_svg_changes'; raster='commons_import_raster_changes'
results={}
for lang,pair in tr.items():
 assert set(pair)=={svg,raster}
 a,b=pair[svg],pair[raster]
 assert a.startswith('AN Paint: SVG → PNG; ')
 assert a.endswith('; antiAlias=false; strokeDashArray=none; background=#FFFFFF.')
 assert a.count('AN Paint')==1 and a.count('SVG → PNG')==1
 assert b.startswith('AN Paint: background=#FFFFFF (') and b.endswith(').')
 assert b.count('alpha')==1 and b.count('background=#FFFFFF')==1
 assert not any(x in a+b for x in ['%s','%1$','{alpha}','alpha compositing','imported=true'])
 for key,val in pair.items():
  e=ET.Element('string',{'name':key});e.text=val
  assert ET.fromstring(ET.tostring(e,encoding='unicode')).text==val
 results[lang]={'whole_resource_shape':True,'literals_preserved':True,'xml_round_trip':True,'messages':{k:hashlib.sha256(v.encode()).hexdigest() for k,v in pair.items()}}
# Frozen lexeme alignment checks use reviewer-specified equivalences, not a claim
# of independently validated transliteration or PFS tone rules.
ain={'hoski pororu':'ホㇱキ ポロル','alpha ani noka kor iro newa oka iro a=ukopoye':'alpha アニ ノカ コㇿ イロ ネワ オカ イロ アウコポイェ'}
for lat,kana in ain.items():
 key=svg if lat=='hoski pororu' else raster
 assert lat in tr['ain-Latn'][key] and kana in tr['ain-Kana'][key]
hak={'原本大細':'ngièn-pún thai-se','照 alpha 混合圖像个色水摎背景色':'cheu alpha fun-ha̍p thù-siong ke set-súi lâu poi-kín set'}
for han,lat in hak.items():
 key=svg if han=='原本大細' else raster
 assert han in tr['hak-Hant-TW'][key] and lat in tr['hak-Latn-TW'][key]
out={'schema_version':1,'input':'../research-specialist/proposals.json','input_sha256':hashlib.sha256(raw).hexdigest(),'locale_count':len(tr),'message_count':sum(map(len,tr.values())),'structural_pass':True,'paired_script_lexeme_alignment':{'ain-Kana/ain-Latn':True,'hak-Hant-TW/hak-Latn-TW':True},'limits':['Not a native-speaker acceptance','Not a PFS pronunciation or tone validator','Not an Android rendering/shaping test','Not a font coverage test','No assertion about the underlying raster implementation'],'locales':results}
(HERE/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['input_sha256','locale_count','message_count','structural_pass','paired_script_lexeme_alignment']},ensure_ascii=False))
