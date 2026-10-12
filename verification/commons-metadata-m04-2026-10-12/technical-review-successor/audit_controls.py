#!/usr/bin/env python3
"""Source-only exact Unicode/Kotlin map and retained readability-oracle audit."""
import argparse,hashlib,json,pathlib,re
p=argparse.ArgumentParser(description=__doc__)
for arg in ('repo','frozen','accepted','output'):p.add_argument('--'+arg,type=pathlib.Path,required=True)
a=p.parse_args();root=a.repo.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
raw=a.accepted.read_bytes();assert hashlib.sha256(raw).hexdigest()=='00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d';accepted=json.loads(raw)
path='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureTranslationTest.kt';kt=(root/path).read_text()
block=kt.split('private val expectedMessages=mapOf(',1)[1].split('\n    )',1)[0]
rows=re.findall(r'^        ("[^"]+") to (".*")(?:,)?$',block,re.M)
values={json.loads(k):json.loads(v.replace('\\$','$')) for k,v in rows}
assert len(rows)==59 and len(values)==59 and values==accepted
path='Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt'
flow=(root/path).read_text();old=(a.frozen/path).read_text()
assert flow.replace('"ain-Latn","bo","ryu","fr"','"ain-Latn","fr"')==old
render=flow.split('private fun readable(',1)[1];line=next(x for x in render.splitlines() if 'for(tag in listOf(' in x);tags=re.findall(r'"([^"]+)"',line)
assert len(tags)==14 and {'ain-Kana','ain-Latn','bo','mn-Mong','mnc-Mong','ryu'}<=set(tags)
assert values['mnc-Mong'].count('\u180e')==3 and values['mn-Mong'].count('\u202f')==3
result=dict(status='PASS',exact_kotlin_messages=len(values),manchu_mvs_positions=[i for i,c in enumerate(values['mnc-Mong']) if c=='\u180e'],mongolian_nnbsp_positions=[i for i,c in enumerate(values['mn-Mong']) if c=='\u202f'],render_profiles=tags,render_configurations=4,actions_per_profile=2,planned_capture_count=112,existing_flow_assertions_preserved=True,runtime_status='UNRUN; source assertions only')
(out/'unicode-and-render-source-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
