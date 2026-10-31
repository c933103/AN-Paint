"""Read-only canonical-source presence audit; no linguistic inference."""
import csv,hashlib,io,json
from pathlib import Path
import translation_catalogues as c

out=Path(__file__).resolve().parent
source,plurals,keys,plural_keys=c.default_resources()
paths=c.catalogue_paths();tags=c.offered_tags()
assert len(tags)==len(set(tags))==171
errors=c.validate_all()
assert not errors,errors
rows=[]
for tag in tags:
    path=paths[tag];strings=c.read_strings(path);quantities=c.read_plurals(path)
    present_strings=len(keys & set(strings));present_plurals=len(plural_keys & set(quantities))
    missing_strings=len(keys-set(strings));missing_plurals=len(plural_keys-set(quantities))
    missing=missing_strings+missing_plurals
    rows.append(dict(tag=tag,catalogue=str(path.relative_to(c.ROOT)),catalogue_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),present_strings=present_strings,present_plural_resources=present_plurals,missing_strings=missing_strings,missing_plural_resources=missing_plurals,total_present=present_strings+present_plurals,total_missing=missing,presence_status='complete' if not missing else 'empty' if missing==len(keys)+len(plural_keys) else 'partial'))
summary=dict(actual_develop_commit='a087bf6e609c86ac60110c0b782c62dc6c72a8d3',verified_tree='71c2c50b624a0f730aa28c00eca99c9768cb2227',offered_options=len(tags),translatable_strings=len(keys),translatable_plural_resources=len(plural_keys),resource_identities_per_option=len(keys)+len(plural_keys),presence_complete=sum(r['presence_status']=='complete' for r in rows),partial=sum(r['presence_status']=='partial' for r in rows),empty=sum(r['presence_status']=='empty' for r in rows),missing_locale_resource_identities=sum(r['total_missing'] for r in rows),present_locale_resource_identities=sum(r['total_present'] for r in rows),empty_tags=[r['tag'] for r in rows if r['presence_status']=='empty'],unoffered_catalogue_tags=sorted(set(paths)-set(tags)),structural_validation_errors=errors,semantics='Own exact canonical Android catalogue presence only. Each plural resource counts once, not once per quantity. Missing identities use Android fallback; no fluency, review, native-human, layout or completeness certification follows from presence. English copies, aliases, notation and metadata count as present, not necessarily translated.')
assert summary['present_locale_resource_identities']+summary['missing_locale_resource_identities']==171*717
(out/'actual-main-171-option-presence.json').write_text(json.dumps(dict(summary=summary,options=rows),ensure_ascii=False,indent=2)+'\n')
fields=['tag','present_strings','present_plural_resources','missing_strings','missing_plural_resources','total_present','total_missing','presence_status','catalogue','catalogue_sha256']
with (out/'actual-main-171-option-presence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print(json.dumps(summary,indent=2))
