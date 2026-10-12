#!/usr/bin/env python3
"""Build an explicit sanitized derivative from a frozen held selection. Local only.
Never print/store cookie values or value hashes. Original input bytes are read-only.
"""
import argparse,gzip,hashlib,io,json,pathlib,re,shutil,tarfile
EXPECTED_SELECTION='7f5e33a1e9015527a1f7bc877ecdeafd191701013ec44aaaea0ed84800d7a389'
EXPECTED_ARCHIVE='786b527dc893aa76f253b504734e30e8b73b26cd4f674d88057966ddbbf8e54d'
EXPECTED_LOG='d7d2e746e2a55afac2914a82ba30aabdf56d6cb3d0f410d01bb1da2f59077587'
TARGET='current-inputs/api30/logcat.txt';LINE=20476
p=argparse.ArgumentParser();p.add_argument('--held-selection',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();src=a.held_selection;dst=a.output
if dst.exists() or dst.resolve().is_relative_to(src.resolve()):raise ValueError('output must be fresh and separate')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
mraw=(src/'DELIVERY-FILES.json').read_bytes();m=json.loads(mraw)
if sha(mraw)!=EXPECTED_SELECTION:raise ValueError('held selection changed')
for f in m['files']:
 b=(src/f['path']).read_bytes()
 if len(b)!=f['bytes'] or sha(b)!=f['sha256']:raise ValueError('held selected bytes changed')
dst.mkdir(parents=True)
for f in m['files']:
 if f['path'] in ('supporting-evidence.tar.gz','SUPPORTING-INPUTS.json','README.md'):continue
 target=dst/f['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((src/f['path']).read_bytes())
sm=json.loads((src/'SUPPORTING-INPUTS.json').read_bytes());arc=(src/'supporting-evidence.tar.gz').read_bytes()
if sha(arc)!=EXPECTED_ARCHIVE:raise ValueError('held archive changed')
rows=[];changed=[];headers=[];unchanged=0
with tarfile.open(fileobj=io.BytesIO(arc)) as old, (dst/'supporting-evidence.tar.gz').open('wb') as output:
 with gzip.GzipFile(fileobj=output,filename='',mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as new:
  for info in old.getmembers():
   if not info.isfile():raise ValueError('nonregular member')
   b=old.extractfile(info).read();orig=b
   if info.name==TARGET:
    if sha(b)!=EXPECTED_LOG:raise ValueError('target log differs')
    lines=b.splitlines(keepends=True);line=lines[LINE-1]
    if b'NetworkMonitor/101: PROBE_FALLBACK http://www.google.com/gen_204 ' not in line:raise ValueError('context mismatch')
    start=line.index(b'headers={');end=line.rindex(b'}')+1
    headers=re.findall(rb'(?:\{|,\s+)([A-Za-z][A-Za-z0-9-]*)=\[',line[start:end])
    # Suppress all response-header values on the one independently classified line.
    replacement=b'headers={[REDACTED: third-party response headers]}'
    lines[LINE-1]=line[:start]+replacement+line[end:];b=b''.join(lines)
    if len(b.splitlines())!=len(orig.splitlines()):raise ValueError('line count changed')
    changed.append({'path':info.name,'line':LINE,'original_whole_file_sha256':sha(orig),'sanitized_whole_file_sha256':sha(b),'original_bytes':len(orig),'sanitized_bytes':len(b),'line_count':len(lines),'line_count_preserved':True,'response_field':'headers','response_header_names':[x.decode() for x in headers],'cookie_field_names':['__Secure-STRP','SEARCH_SAMESITE'],'replacement':'headers={[REDACTED: third-party response headers]}','all_bytes_outside_this_response_field_unchanged':True})
   else:unchanged+=1
   n=tarfile.TarInfo(info.name);n.size=len(b);n.mode=info.mode;n.uid=n.gid=n.mtime=0;n.uname=n.gname='';new.addfile(n,io.BytesIO(b));rows.append({'path':info.name,'bytes':len(b),'sha256':sha(b)})
if len(changed)!=1:raise ValueError('target count differs')
newarc=(dst/'supporting-evidence.tar.gz').read_bytes();sm['archive']={'path':'supporting-evidence.tar.gz','bytes':len(newarc),'sha256':sha(newarc)};sm['files']=rows;sm['expanded_bytes']=sum(x['bytes'] for x in rows);sm['scope']='SANITIZED DERIVATIVE. One API30 logcat response-headers field is redacted; the other 89 archive members are unchanged original evidence. Never describe the redacted log or this TAR as byte-identical raw CI replay.';sm['limits']='Original CI/outer-ZIP/source hashes identify historical held inputs, not the sanitized log. See REDACTION-MANIFEST.json and SANITIZED-PROVENANCE.json. No new Android execution; no publication authorization.';sm['derivative_kind']='SANITIZED_NOT_RAW';sm['original_archive_sha256']=EXPECTED_ARCHIVE;sm['redaction_manifest']='REDACTION-MANIFEST.json';dump(dst/'SUPPORTING-INPUTS.json',sm)
red={'schema':1,'status':'LOCAL_SANITIZED_DERIVATIVE_PENDING_INDEPENDENT_REVIEW','original_selection_sha256':EXPECTED_SELECTION,'original_archive_sha256':EXPECTED_ARCHIVE,'sanitized_archive_sha256':sha(newarc),'original_archive_bytes':len(arc),'sanitized_archive_bytes':len(newarc),'changed_members':changed,'unchanged_archive_members':unchanged,'reason':'Unmasked third-party response-cookie values and associated response-header material in the Android connectivity probe; not a claim of authenticated user-account access.','provider_host':'www.google.com','request_path':'/gen_204','cookie_values_or_cookie_value_hashes_included':False,'original_input_bytes_preserved':True,'requires':'Independent content scan and source/test-protocol verification before any publication recommendation.'};dump(dst/'REDACTION-MANIFEST.json',red)
changed_paths=['README.md','SUPPORTING-INPUTS.json','supporting-evidence.tar.gz'];retained=[x for x in m['files'] if x['path'] not in changed_paths]
prov={'schema':1,'derivative_kind':'SANITIZED_NOT_RAW','source_head':m['head'],'source_tree':m['tree'],'run_id':m['run_id'],'original_selection_sha256':EXPECTED_SELECTION,'original_acceptance_sha256':sha((src/'ACCEPTANCE.json').read_bytes()),'acceptance_bytes_unchanged':(src/'ACCEPTANCE.json').read_bytes()==(dst/'ACCEPTANCE.json').read_bytes(),'retained_original_receipt_scope':'All unchanged reports, ACCEPTANCE.json, PORTABLE-VERIFICATION.json and original artifact/outer/archive checks describe the ORIGINAL held raw inputs. They are historical functional evidence, not fresh sanitized replay receipts.','original_receipts_retained_unchanged':retained,'modified_original_selected_paths':changed_paths,'support_member_change_count':1,'unchanged_support_members':unchanged,'sanitized_reverification':'Independent fresh results must be labeled sanitized-log verification; raw matrices/source/pixels should retain meanings, while whole-log hash-bearing results will differ.','outside_scope':'No mutation of held inputs, application code or tests; no GitHub writes; no permission/publication decision.'};dump(dst/'SANITIZED-PROVENANCE.json',prov)
readme='''# PR55 installed evidence: SANITIZED DERIVATIVE

This separate packet contains the original bounded functional acceptance and a deliberately sanitized supporting archive. It is **not byte-identical raw CI replay**. Original held evidence has not been changed.

## Source and functional boundary

The source is head `4a35933ff6b6d0013dac8743cc5eeac1c1033e05`, tree `b6bf7626c1d7c4aef669394970046ffc89a5c877`, run `38303992927`. `ACCEPTANCE.json` is retained byte-for-byte as the historical original-input functional result (SHA-256 `e5684bf7b81df201bc02477403e2aae24c3eb0f070da6a6c5d2adb1ce3be8280`). It records API30 95/95 from actual attempt 2 and API35 104/104 from actual attempt 1. API30 attempt 1 remains setup-failed before instrumentation, with all 95 tests unrun.

All unchanged audit reports and `PORTABLE-VERIFICATION.json` describe the original held inputs. Their original raw log, CI ZIP and payload hashes are provenance of those original inputs, not hashes of the sanitized log. `SANITIZED-PROVENANCE.json` lists exact unchanged files and their scope. Do not treat historical raw-archive checks as newly reproduced by this packet.

## Deliberate redaction

`REDACTION-MANIFEST.json` identifies one changed member, `current-inputs/api30/logcat.txt`, and its original/sanitized whole-file hashes. At original line 20476, the entire third-party connectivity-probe response-headers field was replaced with an explicit marker. This removes the response cookie values and associated response-header material while preserving line count and every byte outside that field. It does not remove any instrumentation line or assert that these cookies authenticated a user account.

The other 89 support members, including all phase protocols, XML, native-export ZIPs, and original failed-attempt job log, are unchanged. All 192 current native images remain their original bytes, as are their original reviewed visual results. Four Arabic PNGs had exact-e19 visual reuse in the historical result. No image pixels were edited.

`SUPPORTING-INPUTS.json` binds the sanitized TAR and current member hashes. `DELIVERY-FILES.json` binds this derivative selection. Only this derivative TAR belongs to this selection; no held original log/TAR or APK/source/outer-CI ZIP is included. The original freezing script is retained as historical audit methodology; it is not a command for creating this derivative.

## Verify and replay the sanitized selection

Run `python3 verify_selection.py`, then `python3 verify_support.py --output /fresh/output`. The extraction verifies the sanitized hashes. With the exact source tree, Python 3, Pillow and NumPy, the unchanged matrix, receipt-only prebuilt, platform and native checkers can inspect `/fresh/output/current-inputs`. Their results must be labeled sanitized-log verification. Hash-bearing whole-log results will differ from historical original-input reports, while source, test identities, test outcomes, PNGs and parsed instrumentation evidence should retain their meanings.

`run_audit.py` and outer-archive/payload checks still require the original held ZIP/APK/source downloads and are not reproducible from this sanitized compact packet alone. No new Android or application-test execution occurred. Independent derivative verification and disclosure review are required before publication recommendation; this local artifact does not authorize publication.

## Limits

This remains bounded installed regression and API35 framework LocaleConfig discovery. It does not establish language fluency, Settings-screen visibility, physical-device acceptance, an API33 installed constructor run, private signing, live Commons-provider acceptance, or full translation coverage. Existing short-landscape and pre-click/post-mount limitations remain in the unchanged acceptance. Redaction must not be used to claim universal secret absence or exact raw replay.
'''
(dst/'README.md').write_text(readme)
(dst/'build_sanitized_derivative.py').write_bytes(pathlib.Path(__file__).read_bytes())
rows=[]
for f in sorted(dst.rglob('*')):
 if f.is_file():b=f.read_bytes();rows.append({'path':f.relative_to(dst).as_posix(),'bytes':len(b),'sha256':sha(b)})
manifest={'schema':1,'head':m['head'],'tree':m['tree'],'merge':m['merge'],'run_id':m['run_id'],'kind':'SANITIZED_DERIVATIVE','file_count':len(rows),'total_bytes':sum(x['bytes'] for x in rows),'files':rows,'scope':'Self-contained sanitized derivative of the original 74-file installed selection, with redaction/provenance/recipe additions. Unchanged acceptance/reports are historical original-input evidence.'};dump(dst/'DELIVERY-FILES.json',manifest)
# Recheck every original selected byte after building; the source manifest stays unchanged.
if (src/'DELIVERY-FILES.json').read_bytes()!=mraw:raise ValueError('original selection manifest changed')
for f in m['files']:
 b=(src/f['path']).read_bytes()
 if len(b)!=f['bytes'] or sha(b)!=f['sha256']:raise ValueError('held selection changed during construction')
print(json.dumps({'output':str(dst),'manifest_sha256':sha((dst/'DELIVERY-FILES.json').read_bytes()),'file_count':len(rows),'bytes':manifest['total_bytes'],'redaction':changed,'original_selection_unchanged':True},indent=2))
