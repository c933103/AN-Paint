from pathlib import Path
import json,hashlib,sys
out=Path('/workspace/shared/anpaint-m04-language-review-recovered-20261012')
values={
 'ain-Latn':'Tatum (noka oruspe) anak Commons a=konu eaykap.',
 'ain-Kana':'タトゥㇺ (ノカ オルㇱペ) アナㇰ Commons アコヌ エアイカㇷ゚.',
 'mnc-Mong':'Commons\u180eᡩᡝ ᠨᡳᡵᡠᡤᠠᠨ\u180eᡳ ᠮᡝᠵᡳᡤᡝ\u180eᠪᡝ ᡶᠣᠨᠵᡳᠮᡝ ᠮᡠᡨᡝᡥᡝᡴᡡ.',
 'bo':'Commons ལ་པར་གྱི་གནས་ཚུལ་དྲིས་པ་ལམ་ལྷོངས་མ་བྱུང་།',
 'mn-Mong':'Commons\u202fᠠᠴᠠ ᠵᠢᠷᠤᠭ\u202fᠤᠨ ᠮᠡᠳᠡᠭᠡᠯᠡᠯ\u202fᠢ ᠯᠠᠪᠯᠠᠬᠤ ᠬᠦᠰᠡᠯᠲᠡ ᠪᠦᠲᠦᠭᠰᠡᠨ ᠦᠭᠡᠢ᠃',
 'ryu':'Commonsんかい メタデータ たぬむしぬ ないはんちゃん。'
}
prior_value_hashes={
 'ain-Latn':'b088640dae7db686a0d5e454b8205c33452c22f74d3daaa22a97528b2d0ec165',
 'ain-Kana':'f64845a6f519af8c97ee165133f453920d620f90bba85367febf8c52fff199dc',
 'mnc-Mong':'9eedf78d87751652989ab2813be3479f3f4a7834b9d8a6756103f15f29b405df',
 'bo':'220e34954556f32203a5e684b86ebf8e8ca172be4797e0d16d817c4dbf8b14fe',
 'mn-Mong':'74d3789b03da22830d80c88645c12fe781403639b8c32dd2077e551628785012',
 'ryu':'a50fabc7da1d421af788c4fc679d1524977d58b342af06fd42eaa13fa1b87ace'
}
hashes={k:hashlib.sha256(v.encode()).hexdigest() for k,v in values.items()}
assert hashes==prior_value_hashes
raw=lambda obj:json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
(out/'six-final-values.json').write_text(raw(values))
for n,tags in [('accepted-ainu-manchu-followup-values.json',['ain-Latn','ain-Kana','mnc-Mong']),('accepted-other-languages-followup-values.json',['bo','mn-Mong']),('accepted-ryu-followup-value.json',['ryu'])]:
 (out/n).write_text(raw({t:values[t] for t in tags}))
manifest={'recovery_date':'2026-10-12','method':'Exact value strings and prior hashes from surviving review tool output; no new linguistic research.','known_final_v4_sha256':'00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d','six_values':{k:{'prior_sha256_utf8':prior_value_hashes[k],'recovered_sha256_utf8':hashes[k],'exact_value_bytes_verified':True} for k in values},'small_value_files_status':'Reconstructed with the original recorded Python JSON serializer and insertion order; values are hash-verified, but no prior complete-file hash was recorded for these three small files.','final_v4_status':'Waiting for parent’s frozen 53-value base.'}
if len(sys.argv)>1:
 base=Path(sys.argv[1]);b=json.loads(base.read_text());assert len(b)==53, len(b)
 assert not(set(b)&set(values));merged={**b,**values};v4raw=raw(merged);h=hashlib.sha256(v4raw.encode()).hexdigest()
 manifest.update({'base_file':str(base),'base_file_sha256_now':hashlib.sha256(base.read_bytes()).hexdigest(),'reconstructed_v4_sha256':h,'known_v4_hash_match':h==manifest['known_final_v4_sha256']})
 if h==manifest['known_final_v4_sha256']:
  (out/'accepted-and-proposed-values-v4.json').write_text(v4raw);manifest['final_v4_status']='Exact complete-file byte recovery verified against previously recorded SHA256.'
 else:
  (out/'accepted-and-proposed-values-v4-UNVERIFIED-RECONSTRUCTION.json').write_text(v4raw);manifest['final_v4_status']='Values reconstructed, but complete-file bytes do not match prior hash; do not call this exact recovery.'
(out/'RECOVERY-MANIFEST.json').write_text(raw(manifest))
print(json.dumps(manifest,ensure_ascii=False,indent=2))
