#!/usr/bin/env python3
"""Conservative selection screen. Reports counts/locations only; never emits values or value hashes."""
import argparse, json, pathlib, re
FIELD=re.compile(rb'(?i)\b(set-cookie|cookie|authorization|proxy-authorization|x-api-key|access_token|refresh_token|client_secret|password)\s*[:=]\s*(.*)')
TOKEN=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)')
def screen(root, files):
    rows=[]
    for p in files:
        suspicious=[];masked=[]
        for i,line in enumerate(p.read_bytes().splitlines(),1):
            m=FIELD.search(line)
            if m:
                value=m[2].strip().strip(b'\"\x27')
                if m[1].lower() in (b'authorization',b'proxy-authorization') and re.fullmatch(rb'(?i)(?:basic|bearer)\s+\*{3}',value):masked.append(i)
                else:suspicious.append(i)
            if TOKEN.search(line):suspicious.append(i)
        if suspicious or masked:rows.append({'path':p.relative_to(root).as_posix(),'suspected_value_lines':sorted(set(suspicious)),'provider_masked_authorization_lines':masked})
    return {'files_screened':len(files),'suspected_value_count':sum(len(r['suspected_value_lines']) for r in rows),'masked_authorization_count':sum(len(r['provider_masked_authorization_lines']) for r in rows),'locations_only':rows}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ci-root',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args()
    raw=[a.ci_root/'build-job.log',*(a.ci_root/'exact-script-generation').iterdir()]
    raw=[p for p in raw if p.is_file()]
    selected=[p for p in sorted(a.packet.rglob('*')) if p.is_file() and p.name not in ('evidence-screen-result.json','DELIVERY-FILES.json')]
    result={'status':'PASS','raw_build_and_probe_inputs':screen(a.ci_root,raw),'selected_packet':screen(a.packet,selected),'raw_log_content_in_packet':False,'suspected_values_or_value_hashes_in_report':False,'limits':['Pattern-based conservative selection check; not a universal secret detector.','Selected build evidence contains expected markers rather than arbitrary surrounding log lines.','No raw prior API30 packet, raw logcat, APK, source ZIP or full source inventory is copied.']}
    if result['raw_build_and_probe_inputs']['suspected_value_count'] or result['selected_packet']['suspected_value_count']:result['status']='HOLD'
    (a.packet/'evidence-screen-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status']+': screened raw build/probe inputs and selected compact packet; no raw values or value hashes reported.')
    if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
