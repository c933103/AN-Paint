#!/usr/bin/env python3
"""Independent structural/source validation; never a linguistic acceptance test."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from xml.dom import minidom

def check(ok,message):
    if not ok: raise ValueError(message)
def digest(b): return hashlib.sha256(b).hexdigest()
def readj(p):
    def pairs(items):
        d={}
        for k,v in items:
            check(k not in d,'duplicate JSON key: '+k);d[k]=v
        return d
    return json.loads(p.read_bytes(),object_pairs_hook=pairs)
def xml(p):
    doc=minidom.parseString(p.read_bytes());d={}
    for node in doc.documentElement.childNodes:
        if node.nodeType!=node.ELEMENT_NODE:continue
        key=node.tagName+'/'+node.getAttribute('name');check(key not in d,'duplicate XML identity: '+key)
        value=''.join(x.data for x in node.childNodes if x.nodeType in [x.TEXT_NODE,x.CDATA_SECTION_NODE])
        d[key]={'value':value,'attrs':{node.attributes.item(i).name:node.attributes.item(i).value for i in range(node.attributes.length)}}
    return d

def main():
    a=argparse.ArgumentParser();a.add_argument('--source-root',type=Path,required=True);a.add_argument('--packet',type=Path,default=Path('.'));args=a.parse_args();root=args.source_root;packet=args.packet
    prov=readj(packet/'source-provenance.json');scope=readj(packet/'scope-and-holds.json');inventory=readj(packet/'source-production-inventory.json')
    check(prov['source_commit']==scope['source_commit']==inventory['source_commit']=='857a20103285a77846e340b326667c15a402ff9e','source pin')
    bindings={}
    for row in prov['source_bindings']+inventory['files']:
        if row['path'] in bindings:check(bindings[row['path']]==row,'inconsistent binding')
        bindings[row['path']]=row
    for p,b in bindings.items():
        data=(root/p).read_bytes();g=subprocess.run(['git','hash-object','--stdin'],input=data,stdout=subprocess.PIPE,check=True).stdout.decode().strip()
        check((len(data),digest(data),g)==(b['bytes'],b['sha256'],b['git_blob_sha1']),'source byte mismatch: '+p)
    base=xml(root/'Paintroid/src/main/res/values/strings.xml');nn=xml(root/'Paintroid/src/main/res/values-b+nn/strings.xml')
    check(len(base)==720 and sum(v['attrs'].get('translatable')!='false' for v in base.values())==717 and len(nn)==118,'source denominator drift')
    tier=readj(root/'translations/string-importance.json');p0=next(x['keys'] for x in tier['tiers'] if x['id']=='P0');check(len(p0)==len(set(p0))==92,'P0 keys')
    missing=set(p0)-set(nn);check(len(missing)==77,'missing set')
    scoped={r['identity']:r for r in scope['entries']};check(len(scoped)==len(scope['entries'])==77 and set(scoped)==missing,'scope exactness')
    allc={};group_hashes={};window_count=0;paths=set();production={b['path']:(root/b['path']).read_text().splitlines() for b in inventory['files']};check(len(production)==322,'production inventory')
    ph=re.compile(r'%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[a-zA-Z%]')
    for file in sorted(packet.glob('group-*.json')):
        group_hashes[file.name]=digest(file.read_bytes());group=readj(file)
        check(group['source_commit']==prov['source_commit'] and len(group['candidates'])==group['candidate_count'],'group binding/count')
        check(len(group['unchanged_nynorsk_terminology'])==118,'neighbor count')
        for neighbor in group['unchanged_nynorsk_terminology']:
            v=nn['string/'+neighbor['key']];check(v['value']==neighbor['nynorsk_xml_text'] and v['attrs']==neighbor['attributes'],'neighbor mismatch')
        for c in group['candidates']:
            key=c['identity'];check(key not in allc and key in missing,'overlap/nonmissing candidate');allc[key]=c
            check(c['source']==base[key]['value'] and c['attributes']==base[key]['attrs'],'source pair mismatch')
            check(isinstance(c['candidate'],str) and c['candidate'].strip() and not c['candidate'].startswith('@'),'empty/alias candidate')
            check(c['source_value_sha256_utf8']==digest(c['source'].encode()) and c['candidate_value_sha256_utf8']==digest(c['candidate'].encode()),'value hash')
            check(ph.findall(c['source'])==ph.findall(c['candidate'])==c['placeholder_tokens'],'placeholder contract')
            check(c['candidate_status']=='author proposal, independent review pending','acceptance inflation')
            name=key.split('/')[1];refs=[]
            for p,lines in production.items():
                if not p.endswith(('.kt','.java')):continue
                refs += [p+':'+str(i+1) for i,l in enumerate(lines) if re.search(r'\bR\.string\.'+re.escape(name)+r'\b',l)]
            check(sorted(refs)==sorted(c['direct_production_consumer_ids']) and len(refs)==c['direct_consumer_count'],'consumer extraction')
            check(len(c['consumer_contexts'])==len(refs),'context count')
            for w in c['consumer_contexts']:
                lines=production[w['path']];check(w['key']==key and w['id'] in refs,'consumer key')
                check(w['text']=='\n'.join(lines[w['start_line']-1:w['end_line']]),'context byte lines')
                check(w['url']==f"https://github.com/c933103/AN-Paint/blob/{prov['source_commit']}/{w['path']}#L{w['start_line']}-L{w['end_line']}",'context link')
                window_count+=1;paths.add(w['path'])
    check(len(allc)==72 and window_count==120 and len(paths)==21,'proposal/consumer totals')
    held=set(scoped)-set(allc);check(held=={'string/'+k for k in ['formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png']},'held identities')
    for key,r in scoped.items():
        check(r['source']==base[key]['value'] and r['attributes']==base[key]['attrs'] and r['current_nynorsk_value'] is None and not r['absence_is_defect'],'scope source semantics')
        if key in held:
            check(r['candidate'] is None and r['status']=='held-no-current-consumer-evidenced','held status')
            name=key.split('/')[1]
            for p,lines in production.items():
                pattern=(r'@string/'+re.escape(name)+r'\b') if p.endswith('.xml') else (r'\b'+re.escape(name)+r'\b')
                check(not any(re.search(pattern,line) for line in lines),'held reference now found')
    forbidden=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]+',r'-----BEGIN .*PRIVATE KEY-----',r'https?://[^\s]+[?&](?:token|sig|access_token)=']
    for file in packet.iterdir():
        if not file.is_file():continue
        text=file.read_bytes().decode('utf-8')
        if file.name!='verify_candidates.py':
            for prefix in ['/'+'tmp'+'/','/'+'workspace'+'/','/'+'home'+'/']:
                check(prefix not in text,'execution-local path leaked: '+file.name)
        for pattern in forbidden:
            if file.name!='verify_candidates.py':check(re.search(pattern,text) is None,'potential secret/private URL: '+file.name)
    manifest=packet/'manifest.json'
    if manifest.exists():
        m=readj(manifest);listed={f['path'] for f in m['files']};check(listed=={p.name for p in packet.iterdir() if p.is_file() and p.name!='manifest.json'},'manifest coverage')
        for f in m['files']:
            b=(packet/f['path']).read_bytes();check(len(b)==f['bytes'] and digest(b)==f['sha256'],'manifest bytes')
    print(json.dumps({'status':'passed structural/source validation; no linguistic verdict','source_commit':prov['source_commit'],'bound_files_checked':len(bindings),'production_files_scanned':len(production),'missing_P0':77,'author_proposals':72,'held':5,'consumer_windows':window_count,'consumer_files':len(paths),'untouched_values':len(nn),'group_sha256':group_hashes},indent=2))
if __name__=='__main__':main()
