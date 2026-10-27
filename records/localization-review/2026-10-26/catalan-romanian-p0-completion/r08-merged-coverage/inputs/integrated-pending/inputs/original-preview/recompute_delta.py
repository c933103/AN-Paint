"""Pinned PR178 preview only; no integration, CI, native or release claim."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, 'duplicate JSON key: ' + key)
        value[key] = item
    return value


def read(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(data, kind='blob'):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def emit(folder, name, data):
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def file_binding(path, public_name):
    raw = path.read_bytes()
    return {'path': public_name, 'bytes': len(raw), 'sha256': sha(raw), 'git_blob_sha1': git(raw)}


def parse(raw):
    require(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(), 'XML entity boundary')
    root = ET.fromstring(raw)
    require(root.tag == 'resources', 'invalid resource root')
    containers, leaves, nodes, names = {}, {}, {}, set()
    for node in root:
        require(node.tag in ('string', 'plurals', 'string-array'), 'unexpected catalogue resource type')
        name = node.get('name')
        require(bool(name) and name not in names, 'missing or duplicate resource name')
        names.add(name)
        identity = node.tag + '/' + name
        nodes[identity] = node
        if node.get('translatable') == 'false':
            continue
        if node.tag == 'string':
            value = ''.join(node.itertext())
            require(bool(value), 'empty string resource: ' + identity)
            containers[identity] = value
            leaves[identity] = value
        else:
            values = {}
            for index, item in enumerate(node):
                require(item.tag == 'item', 'invalid resource child')
                quantity = item.get('quantity') if node.tag == 'plurals' else str(index)
                require(quantity is not None and quantity not in values, 'missing or duplicate resource item')
                if node.tag == 'plurals':
                    require(quantity in {'zero', 'one', 'two', 'few', 'many', 'other'}, 'unknown plural quantity')
                value = ''.join(item.itertext())
                require(bool(value), 'empty resource item')
                values[quantity] = value
                leaves[identity + '[' + quantity + ']'] = value
            require(bool(values), 'empty resource container')
            containers[identity] = values
    return containers, leaves, nodes


def fingerprint(node):
    return node.tag, sorted(node.attrib.items()), node.text, tuple(fingerprint(c) for c in node)


def tokens(text):
    require('%' not in FORMAT_TOKEN.sub('', text), 'invalid/unescaped format token')
    return collections.Counter(FORMAT_TOKEN.findall(text))


def verify_tree(tree, expected_tree):
    require(tree.get('truncated') is False and tree['sha'] == expected_tree, 'wrong/truncated head tree')
    entries = tree['tree']
    bypath = {e['path']: e for e in entries}
    require(len(bypath) == len(entries), 'duplicate tree path')
    children = collections.defaultdict(list)
    for e in entries:
        path = Path(e['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe tree path')
        require(e['type'] in ('blob', 'tree'), 'unsupported tree entry')
        require(e['mode'] in ('100644', '100755', '120000', '040000'), 'unexpected tree mode')
        require(bool(re.fullmatch('[0-9a-f]{40}', e['sha'])), 'malformed tree SHA')
        children[path.parent.as_posix() if path.parent.as_posix() != '.' else ''].append(e)
    for parent, contents in children.items():
        raw = b''
        for e in sorted(contents, key=lambda x: (Path(x['path']).name + ('/' if x['type'] == 'tree' else '')).encode()):
            mode = e['mode'].lstrip('0')
            raw += mode.encode() + b' ' + Path(e['path']).name.encode() + b'\0' + bytes.fromhex(e['sha'])
        expected = expected_tree if not parent else bypath[parent]['sha']
        require(git(raw, 'tree') == expected, 'recursive Git tree hash mismatch: ' + parent)
    return {k: e for k, e in bypath.items() if e['type'] == 'blob'}


BASE_COMMIT='ce796879f4568a27b9d905a8e8db639dd0a93a30'
BASE_TREE='f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c'
SOURCE_COMMIT='93f27ed172cc730c80ed7a2ffbcacc1b0c04383f'
SOURCE_TREE='571ec84860cb837ae8376f72d0becfb8fd2b7b6d'
STATUS='PR178 source preview; not integrated or current production; no current PR/postmerge CI outcome inferred'
BASE_MANIFEST='e9c43186b3ccf028c6c2038d73f4fa1aa3912d42645b75ae053196a991641ce8'
APPROVED='1bf0f80cc79a82e52b8fd40d8ec8d9fd045a64162d9ec98e16a8ba31c5fe8cbb'
PRIOR_SAVE='601e8699a3fd26c3011a7519743c88fefdc561ce29219ee9e2aa3a3f6addc3cc'
SCOPE='8dd3dd99b633bbec8254639797ddc81000ce4d8bfa9c037503663123587399d5'
CANONICAL='Paintroid/src/main/res/values/strings.xml'
TAGS='Paintroid/src/main/res/values/app_language_tags.xml'
IMPORTANCE='translations/string-importance.json'
LOCALES={t:f'Paintroid/src/main/res/values-{t}/strings.xml' for t in ('ca','ro')}
HOLDS={'string/'+k for k in ('formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png')}
FORMAT_TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')

def safe(root,name):
    p=Path(name);require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe input path')
    out=root/p;require(out.resolve().is_relative_to(root.resolve()),'escaped input path');return out

def load_inputs(folder):
    manifest=read(folder/'baseline/manifest.json');require(sha((folder/'baseline/manifest.json').read_bytes())==BASE_MANIFEST,'baseline manifest identity')
    files=manifest['files'];require(len(files)==len({x['path'] for x in files})==46,'baseline manifest grain')
    require({p.relative_to(folder/'baseline').as_posix() for p in (folder/'baseline').rglob('*') if p.is_file()}=={x['path'] for x in files}|{'manifest.json'},'complete baseline package membership')
    for x in files:
        raw=safe(folder/'baseline',x['path']).read_bytes();require(len(raw)==x['bytes'] and sha(raw)==x['sha256'] and git(raw)==x['git_blob_sha1'],'baseline payload integrity')
    require(manifest['source_commit']==BASE_COMMIT and manifest['source_tree']==BASE_TREE,'baseline source identity')
    terminal=read(folder/'baseline/terminal-status-supplement.json');require(terminal['source_commit']==BASE_COMMIT and terminal['source_tree']==BASE_TREE and terminal['run']['id']==40327501312 and terminal['run']['head_sha']==BASE_COMMIT and terminal['run']['status']=='completed' and terminal['run']['conclusion']=='success','baseline terminal evidence')
    require(sha((folder/'approved-manifest.json').read_bytes())==APPROVED,'approved-manifest identity')
    require(sha((folder/'prior-save-scope-ledger.json').read_bytes())==PRIOR_SAVE,'prior save ledger identity')
    require(sha((folder/'packet/scope-and-source-context.json').read_bytes())==SCOPE,'selected scope identity')
    identity=read(folder/'source-head.json');require(identity=={'head':SOURCE_COMMIT,'tree':SOURCE_TREE,'base':BASE_COMMIT,'pr':178},'preview identity not integration')
    approved=read(folder/'approved-manifest.json');require(approved['source_commit']==BASE_COMMIT and approved['source_tree']==BASE_TREE and approved['final_values']==110,'review origin and count')
    receipts={};manifests={}
    for tag in LOCALES:
        f=folder/'review'/tag/(tag+'-review-manifest.json');require(sha(f.read_bytes())==approved['review_manifests'][tag],'review manifest identity');manifests[tag]=read(f)
    for e in approved['values']:
        path=e['receipt'];require(path.startswith(e['locale']+'/'),'receipt locale path')
        raw=safe(folder/'review',path).read_bytes();require(sha(raw)==e['receipt_sha256'],'exact independent receipt identity');receipts[path]=json.loads(raw,object_pairs_hook=unique)
    require(len(receipts)==6,'six independent receipts')
    return {'manifest':manifest,'terminal':terminal,'rows':read(folder/'baseline/structural-per-locale.json'),'baseline_delta':read(folder/'baseline/integrated-pending/coverage-delta.json'),'baseline_bindings':read(folder/'baseline/integrated-pending/source-bindings.json'),'prior_import':read(folder/'baseline/integrated-pending/review-scope-reconciliation.json'),'prior_save':read(folder/'prior-save-scope-ledger.json'),'scope':read(folder/'packet/scope-and-source-context.json'),'approved':approved,'receipts':receipts,'review_manifests':manifests,'identity':identity,'head_tree':read(folder/'head-tree.json'),'base_tree':read(folder/'base-source-tree.json')}

def source_snapshot(root,oldroot,m):
    blobs=verify_tree(m['head_tree'],SOURCE_TREE);oldblobs=verify_tree(m['base_tree'],BASE_TREE)
    require(len(blobs)==1379 and len(oldblobs)==1376,'full source blob counts')
    # Check every current raw file, not just assumed changed catalogues.
    raw={}
    for p,e in blobs.items():
        b=safe(root,p).read_bytes();require(git(b)==e['sha'] and len(b)==e['size'],'current raw Git source '+p);raw[p]=b
    selected={p for p in blobs if re.fullmatch(r'Paintroid/src/main/res/values[^/]*/strings\.xml',p)}
    actual={p.relative_to(root).as_posix() for p in (root/'Paintroid/src/main/res').glob('values*/strings.xml')}
    require(len(selected)==174 and selected==actual,'catalogue inventory')
    prior={x['path']:x for x in m['baseline_bindings']['files']};require(len(prior)==176 and set(prior)==selected|{TAGS,IMPORTANCE},'coverage input inventory')
    bindings=[];old={}
    for p in sorted(prior):
        b=safe(oldroot,p).read_bytes();require(git(b)==prior[p]['source_blob']==oldblobs[p]['sha'] and sha(b)==prior[p]['sha256'],'baseline raw source identity');old[p]=b
        bindings.append({'path':p,'baseline_blob':oldblobs[p]['sha'],'source_blob':blobs[p]['sha'],'sha256':sha(raw[p]),'bytes':len(raw[p]),'unchanged':oldblobs[p]['sha']==blobs[p]['sha']})
    changed={x['path'] for x in bindings if not x['unchanged']};require(changed==set(LOCALES.values()),'only two changed coverage inputs')
    full_delta=[{'path':p,'before':oldblobs.get(p,{}).get('sha'),'after':blobs.get(p,{}).get('sha'),'status':'added' if p not in oldblobs else 'removed' if p not in blobs else 'changed'} for p in sorted(oldblobs.keys()|blobs.keys()) if oldblobs.get(p,{}).get('sha')!=blobs.get(p,{}).get('sha')]
    require(len(full_delta)==12 and sum(x['status']=='added' for x in full_delta)==3 and all(not x['path'].startswith('Paintroid/src/main/') or x['path'] in LOCALES.values() for x in full_delta),'complete source delta boundary')
    return {'raw':raw,'old':old,'blobs':blobs,'bindings':bindings,'full_delta':full_delta}

def compute(m,s):
    before=m['rows'];require(len(before)==len({r['tag'] for r in before})==171,'baseline option grain')
    scope=m['scope'];selected={e['identity'] for e in scope['entries']};require(len(scope['entries'])==len(selected)==55 and len(selected&HOLDS)==0,'selected missing-only identity grain')
    base,leaves,_=parse(s['raw'][CANONICAL]);require(len(base)==717 and len(leaves)==718,'canonical denominator')
    tagroot=ET.fromstring(s['raw'][TAGS]);arrays=tagroot.findall('string-array');require(len(arrays)==1 and all(x.tag=='item' and x.text for x in arrays[0]),'picker schema');tags=[x.text for x in arrays[0]]
    require(len(tags)==len(set(tags))==171 and tags==[r['tag'] for r in before],'171 picker inventory/order')
    tierlist=json.loads(s['raw'][IMPORTANCE],object_pairs_hook=unique)['tiers'];tiers={t['id']:set(t['keys']) for t in tierlist}
    require(len(tierlist)==len(tiers)==4 and {t:len(v) for t,v in tiers.items()}=={'P0':92,'P1':249,'P2':305,'P3':71},'priority denominators')
    require(all(len(x['keys'])==len(set(x['keys'])) for x in tierlist) and sum(map(len,tiers.values()))==len(set.union(*tiers.values()))==717 and set.union(*tiers.values())==set(base),'tier disjoint partition')
    rows=[];locale_nodes={};old_nodes={}
    for oldrow in before:
        p=oldrow['path'];containers,ll,nodes=parse(s['raw'][p]);r={k:oldrow[k] for k in ('order','tag','path')};r['blob']=s['blobs'][p]['sha']
        for tier,keys in {**tiers,'all':set(base)}.items():r[tier+'_present']=len(keys&containers.keys());r[tier+'_missing']=len(keys-containers.keys())
        overlap=leaves.keys()&ll.keys();r.update(leaves_present=len(overlap),leaves_missing=len(leaves.keys()-ll.keys()),leaves_english_identical=sum(ll[k]==leaves[k] for k in overlap),leaves_source_different=sum(ll[k]!=leaves[k] for k in overlap))
        if r['tag'] not in LOCALES:require(r==oldrow,'unchanged other-option row')
        else:
            tag=r['tag'];_,_,prior=parse(s['old'][p]);require(len(prior)==150 and len(nodes)==205,'150 inherited /205 current catalogue')
            require(set(nodes)-set(prior)==selected and all(fingerprint(nodes[k])==fingerprint(v) and ''.join(nodes[k].itertext())==''.join(v.itertext()) for k,v in prior.items()),'exact additions and all inherited values')
            require(tiers['P0']-nodes.keys()==HOLDS and r['P1_present']==94 and r['P1_missing']==155,'five held P0 and unchanged P1');locale_nodes[tag]=nodes;old_nodes[tag]=prior
        rows.append(r)
    metrics=[k for k in rows[0] if k not in ('order','tag','path','blob')];before_totals={k:sum(r[k] for r in before) for k in metrics};require(before_totals==m['baseline_delta']['presence_totals'],'baseline row/summary totals')
    totals={k:sum(r[k] for r in rows) for k in metrics};delta={k:totals[k]-before_totals[k] for k in metrics}
    require({k:v for k,v in delta.items() if v}=={'P0_present':110,'P0_missing':-110,'all_present':110,'all_missing':-110,'leaves_present':110,'leaves_missing':-110,'leaves_source_different':110},'exact structural delta')
    prior_pairs={};prior_sources=[]
    for name,ledger,count in [('prior_save',m['prior_save'],20),('prior_import',m['prior_import'],26)]:
        require(len(ledger['new_review_scopes'])==count,'prior scope inventory')
        for v in ledger['new_review_scopes']:
            pair=(v['locale'],v['identity']);require(pair not in prior_pairs,'prior duplicate pair');prior_pairs[pair]=v
            node=locale_nodes[pair[0]][pair[1]];require(base[pair[1]]==v['source'] and node.text==v['xml_text'] and node.attrib==v['attributes'] and sha(node.text.encode())==v['xml_text_sha256'],'prior reviewed full pair still current')
        prior_sources.append({'ledger':name,'scope_count':count,'unchanged_and_current':True})
    require(collections.Counter(t for t,k in prior_pairs)=={'ca':23,'ro':23},'prior 23 per locale distinct')
    approved=m['approved'];require(len(approved['values'])==110 and set(approved['preserved_holds'])=={x.split('/')[1] for x in HOLDS},'approved count/holds')
    verdicts={};docs={}
    for path,doc in m['receipts'].items():
        require(doc['source_commit']==BASE_COMMIT and doc['source_tree']==BASE_TREE and doc['locale'] in LOCALES and doc['group'] in (2,3,4),'receipt origin')
        values=doc['entries' if doc['locale']=='ca' else 'verdicts'];require(len(values)=={2:28,3:16,4:11}[doc['group']],'receipt group count')
        for v in values:
            pair=(doc['locale'],v['identity']);require(pair not in verdicts,'duplicate receipt pair');verdicts[pair]=v;docs[pair]=path
    scopes=[];seen=set();decisions=collections.Counter();local={t:collections.Counter() for t in LOCALES}
    for entry in approved['values']:
        pair=(entry['locale'],entry['identity']);require(pair not in seen and pair not in prior_pairs and pair in verdicts,'disjoint new review join');seen.add(pair);tag,key=pair
        require(key in selected and key not in old_nodes[tag] and key in tiers['P0'],'new missing-only P0')
        v=verdicts[pair];require(v['priority']=='P0' and entry['verdict']==v['verdict'] and v['verdict'] in ('accept','revise'),'accepted complete-value decision')
        fields=('source','source_value_sha256_utf8','attributes','final_display_text','final_value_sha256_utf8','final_xml_text','final_xml_text_sha256_utf8')
        require(all(entry[f]==v[f] for f in fields) and entry['receipt']==docs[pair],'exact final independent verdict join')
        require(base[key]==entry['source'] and sha(entry['source'].encode())==entry['source_value_sha256_utf8'],'review current English hash')
        node=locale_nodes[tag][key];require(node.text==entry['final_xml_text'] and node.attrib==entry['attributes'] and not list(node),'review current target XML pair')
        require(sha(node.text.encode())==entry['final_xml_text_sha256_utf8'] and sha(entry['final_display_text'].encode())==entry['final_value_sha256_utf8'] and node.text=='"'+entry['final_display_text']+'"','review XML/display identities')
        require(tokens(entry['source'])==tokens(entry['final_display_text']),'review full format inventory')
        require((v['candidate_display_text']==v['final_display_text'])==(v['verdict']=='accept'),'revision decision consistency')
        scopes.append(dict(entry,source_and_current_target_hash_matched=True,baseline_target_absent=True,scope='bounded AI whole-value linguistic/source-static; all original qualifications retained',original_full_value_verdict=v,receipt_level_qualifications={k:m['receipts'][docs[pair]][k] for k in ('limitations','global_qualifications','cross_group_dependencies','static_composition_examples') if k in m['receipts'][docs[pair]]}))
        decisions[v['verdict']]+=1;local[tag][v['verdict']]+=1
    require(len(seen)==len(verdicts)==110 and seen=={(t,k) for t in LOCALES for k in selected} and decisions=={'accept':107,'revise':3} and dict(local)=={'ca':{'accept':53,'revise':2},'ro':{'accept':54,'revise':1}},'review complete 110 pair partition')
    missing={t:{'all_missing_P0':sorted(tiers['P0']-locale_nodes[t].keys()),'explicit_no_current_consumer_holds':sorted(HOLDS),'other_missing_P0':[],'missing_count':5,'explicit_hold_count':5,'outside_hold_count':0,'absence_implies_defect':False} for t in LOCALES}
    common={'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,'production_baseline_commit':BASE_COMMIT,'production_baseline_tree':BASE_TREE,'current_production_replaced':False}
    result=dict(common,options=171,canonical_containers=717,canonical_leaves=718,tiers={k:len(v) for k,v in tiers.items()},presence_totals=totals,presence_delta=delta,locales_before={t:next(r for r in before if r['tag']==t) for t in LOCALES},locales_after={t:next(r for r in rows if r['tag']==t) for t in LOCALES},unchanged_options=169,full_presence_options=sum(r['all_missing']==0 for r in rows),zero_presence_options=sum(r['all_present']==0 for r in rows),remaining_missing_P0_classification=missing,new_reviewed_pairs=110,prior_reviewed_pairs_per_locale_separate=23,new_Valencian_direct_acceptance=0,global_accepted_count=None,global_linguistic_categories_recomputed=False,absence_implies_defect=False,English_identical_implies_defect=False,counting_policy=m['baseline_delta']['counting_policy'],holds_preserved=list(m['baseline_delta']['holds_preserved']),workflow_results={'PR':178,'PR_CI':'not asserted by this coverage preparation','merge':'not asserted; pinned PR preview only','actual_postmerge_CI':'not applicable to unmerged preview'},historical_runtime_resolution_qualification=m['terminal']['actual_postmerge_runtime_resolution_verification'],historical_runtime_evidence_is_not_current_head_runtime_proof=True)
    result['holds_preserved'][0]='five explicit no-current-consumer P0 holds per ca/ro; no other missing P0 at this PR head'
    reconciliation=dict(common,new_disjoint_bounded_AI_whole_value_scopes=110,new_scope_verdict_counts=dict(decisions),per_locale_verdict_counts={k:dict(v) for k,v in local.items()},prior_catalogue_values_preserved={'ca':150,'ro':150},prior_23_reviewed_per_locale_preserved_separately=prior_sources,prior_categories=m['prior_import']['prior_categories'],global_accepted_count=None,global_count_not_recomputed_reason='Missing-only source delta. Prior classified/historical/qualified/clause-only/author-only/unmatched/synthetic scopes are carried by exact immutable baseline ledgers and unchanged original source values, not recounted, revoked, upgraded or guessed.',new_review_scopes=scopes,remaining_missing_P0_classification=missing,native_or_whole_language_certifications=0,new_Valencian_direct_acceptance=0)
    profile=dict(common,row_grain='one direct target catalogue per offered picker option',option_rows=171,unique_option_tags=171,catalogue_files=174,coverage_source_inputs=176,unchanged_coverage_source_inputs=174,changed_coverage_source_inputs=2,full_tracked_source_blobs_verified=1379,full_source_changed_or_added_paths=12,canonical_containers=717,canonical_leaves=718,tiers_partition_exact=True,new_pairs=110,unique_new_identities=55,per_locale_new=55,prior_current_review_pairs_rechecked=46,duplicate_rows_or_review_pairs=0,missing_independent_review_pairs=0,unmatched_new_reviews=0,actual_new_formatted_false_locale_values=sum(e['attributes'].get('formatted')=='false' for e in approved['values']),english_identical_total=totals['leaves_english_identical'],english_identical_delta=delta['leaves_english_identical'],inherited_runtime_fallback_not_counted_as_direct_presence=True)
    return {'structural-per-locale.json':rows,'coverage-delta.json':result,'review-scope-reconciliation.json':reconciliation,'data-quality-profile.json':profile,'source-bindings.json':dict(common,files=s['bindings'],unchanged_source_files=174,changed_source_files=2),'full-source-delta.json':dict(common,baseline_blob_count=1376,current_blob_count=1379,files=s['full_delta'])}

def run(a):
    m=load_inputs(a.inputs);s=source_snapshot(a.source_root,a.baseline_source_root,m);outputs=compute(m,s);a.out.mkdir(parents=True,exist_ok=True)
    for name,d in outputs.items():emit(a.out,name,d)
    with (a.out/'structural-per-locale.csv').open('w',newline='',encoding='utf-8') as stream:
        rows=outputs['structural-per-locale.json'];w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    bindings=[file_binding(p,p.relative_to(a.inputs).as_posix()) for p in sorted(a.inputs.rglob('*')) if p.is_file()]
    emit(a.out,'input-bindings.json',{'source_commit':SOURCE_COMMIT,'source_tree':SOURCE_TREE,'source_status':STATUS,'files':bindings,'all_paths_are_public_roles_not_execution_locations':True})
    print(json.dumps({'totals':outputs['coverage-delta.json']['presence_totals'],'delta':outputs['coverage-delta.json']['presence_delta'],'new_scopes':110,'source_status':STATUS},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('inputs','source-root','baseline-source-root','out'):p.add_argument('--'+name,type=Path,required=True)
    run(p.parse_args())
