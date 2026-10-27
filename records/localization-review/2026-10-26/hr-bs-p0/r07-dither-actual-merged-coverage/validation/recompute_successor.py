"""Recompute actual c404 successor source coverage; runtime acceptance is separate."""
import argparse, hashlib, json
from pathlib import Path
import xml.etree.ElementTree as E
import xml.dom.minidom as D

MERGE='c404e7ea31ef0a22c3645d8c73e50b55d7ff959c'
TREE='1151529f41c0b0214f0a37b52cabc33d595a3e10'
BASE='c63cd44815ef84f498d1e2fbe46c354416b81cdc'
HEAD='362432da26525229a06c05dea0be1db59a358e59'
def require(ok,msg):
    if not ok: raise ValueError(msg)
def read(p): return json.loads(p.read_text())
def git(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def catalogue(raw):
    require(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(),'XML entity boundary')
    root=E.fromstring(raw); require(root.tag=='resources','resource root')
    containers=set(); leaves={}; nodes={}
    for n in root:
        ident=n.tag+'/'+n.attrib['name']; require(ident not in nodes,'duplicate resource');nodes[ident]=n
        if n.get('translatable')=='false':continue
        containers.add(ident)
        if n.tag=='string':leaves[ident]=''.join(n.itertext())
        else:
            for i,item in enumerate(n):
                key=ident+'['+(item.attrib['quantity'] if n.tag=='plurals' else str(i))+']'
                require(key not in leaves,'duplicate leaf');leaves[key]=''.join(item.itertext())
    return containers,leaves,nodes
def dom(raw):
    root=D.parseString(raw).documentElement;containers=set();leaves={}
    def text(n):return ''.join(c.data if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE) else text(c) if c.nodeType==c.ELEMENT_NODE else '' for c in n.childNodes)
    for n in root.childNodes:
        if n.nodeType!=n.ELEMENT_NODE or n.getAttribute('translatable')=='false':continue
        ident=n.tagName+'/'+n.getAttribute('name');require(ident not in containers,'DOM duplicate');containers.add(ident)
        if n.tagName=='string':leaves[ident]=text(n)
        else:
            for i,item in enumerate(c for c in n.childNodes if c.nodeType==c.ELEMENT_NODE):leaves[ident+'['+(item.getAttribute('quantity') if n.tagName=='plurals' else str(i))+']']=text(item)
    return containers,leaves
def compute(root,previous):
    src=root/'source';tree=read(root/'source-head-tree.json');base=read(root/'actual-base-tree.json');merge=read(root/'postmerge-ci/merge.json')
    require(merge['sha']==MERGE and merge['tree']['sha']==TREE and [p['sha'] for p in merge['parents']]==[BASE,HEAD],'actual merge/tree/parents')
    require(tree['sha']==TREE and not tree['truncated'] and base['sha']=='08550405b070ef263d1511226f8295519ea2ab65','pinned source trees')
    entries={e['path']:e for e in tree['tree'] if e['type']=='blob'};old={e['path']:e for e in base['tree'] if e['type']=='blob'}
    require(len(entries)==len(old)==1388 and entries.keys()==old.keys(),'full source inventory')
    for path,e in entries.items():
        p=src/path;require(git(p.read_bytes())==e['sha'],'source blob '+path);require(('100755' if p.stat().st_mode & 0o111 else '100644')==e['mode'],'source mode '+path)
    changes={p for p,e in entries.items() if (e['sha'],e['mode'])!=(old[p]['sha'],old[p]['mode'])}
    require(changes=={e['path'] for e in read(root/'checks/source-tree-plan.json')['changed']} and len(changes)==4,'four-file delta')
    hr='Paintroid/src/main/res/values-hr/strings.xml';oldhr=(previous/'source'/hr).read_bytes();require(git(oldhr)==old[hr]['sha'],'immediate baseline HR bytes')
    before=catalogue(oldhr)[2];after=catalogue((src/hr).read_bytes())[2]
    require(before.keys()==after.keys(),'no resource additions/removals')
    changed={k for k in before if E.tostring(before[k])!=E.tostring(after[k])};require(changed=={'string/save20_dither','string/save20_gif_description'},'exact atomic two-value correction')
    fpath=src/'tools/fixtures/current_localization/croatian_bosnian_p0_wording.json';require(hashlib.sha256(fpath.read_bytes()).hexdigest()=='c50f4d203e8d2e870d250daa771506c9105fca660e69cac1a84bae3564c53240','accepted current fixture pin');fixture=read(fpath)
    for tag in ['hr','bs']:
        nodes=catalogue((src/f'Paintroid/src/main/res/values-{tag}/strings.xml').read_bytes())[2]
        for key,value in fixture['values'].items():require(nodes['string/'+key].text==value[tag] and nodes['string/'+key].attrib==fixture['constraints'][key][tag]['attributes'],'reviewed whole value/attributes')
        for key,value in fixture['preserved_values'][tag].items():require(nodes['string/'+key].text==value['value'] and nodes['string/'+key].attrib==value['attributes'],'preserved whole value/attributes')
    require(after['string/save20_dither'].text==fixture['dither_label_successor']['value'] and after['string/save20_dither'].attrib==fixture['dither_label_successor']['constraints']['attributes'],'reviewed label/attributes')
    require(sum(len(x) for x in fixture['preserved_values'].values())==214 and len(fixture['values'])*2+1==157,'current 157/214 scope')
    mapping=read(previous/'coverage-terminal/inputs/baseline/structural-per-locale.json')
    tags=[n.text for n in E.parse(src/'Paintroid/src/main/res/values/app_language_tags.xml').findall('./string-array/item')]
    require(tags==[r['tag'] for r in mapping] and len(set(tags))==171,'actual picker grain')
    canonical,english,_=catalogue((src/'Paintroid/src/main/res/values/strings.xml').read_bytes());require(len(canonical)==717 and len(english)==718,'denominators')
    tiers={t['id']:set(t['keys']) for t in read(src/'translations/string-importance.json')['tiers']};rows=[];prior=[]
    def row(item,raw):
        co,le,_=catalogue(raw);dc,dl=dom(raw);require(co==dc and le==dl,'independent DOM exact')
        r={k:item[k] for k in ['order','tag','path']};r['blob']=git(raw)
        for tier,keys in {**tiers,'all':canonical}.items():r[tier+'_present']=len(keys&co);r[tier+'_missing']=len(keys-co)
        overlap=english.keys()&le.keys();r.update(leaves_present=len(overlap),leaves_missing=len(english.keys()-le.keys()),leaves_english_identical=sum(le[k]==english[k] for k in overlap),leaves_source_different=sum(le[k]!=english[k] for k in overlap));return r
    for item in mapping:
        path=item['path'];raw=(src/path).read_bytes();r=row(item,raw);rows.append(r)
        previous_raw=oldhr if path==hr else raw;require(git(previous_raw)==old[path]['sha'],'baseline locale bytes');prior.append(row(item,previous_raw))
    metrics=[k for k in rows[0] if k not in ('order','tag','path','blob')]
    require(all({k:a[k] for k in metrics}=={k:b[k] for k in metrics} for a,b in zip(rows,prior)),'all171 structural counts unchanged')
    totals={k:sum(r[k] for r in rows) for k in metrics};require((totals['P0_present'],totals['P0_missing'])==(7298,8434),'recomputed P0 totals')
    return {'structural-per-locale.json':rows,'coverage-delta.json':{'source_commit':MERGE,'source_tree':TREE,'immediate_baseline_commit':BASE,'options':171,'presence_totals':totals,'presence_delta':{k:0 for k in metrics},'all_171_presence_rows_unchanged':True,'current_HR_BS_reviewed':157,'current_HR_BS_preserved':214,'original_PR183_reviewed':156,'original_PR183_preserved':215,'unchanged_prior_reviewed':155,'new_atomic_reviewed_pair':2,'terminology_qualification':'Moderate-confidence technical clarity for Dithering boja; not preferred native terminology certification.','independent_DOM_exact':True,'new_native_human_or_global_linguistic_acceptance':0,'actual_postmerge_status':'pending separate actual run and artifact verification','no_release':True}}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();outputs=compute(a.root,a.previous);a.out.mkdir(parents=True,exist_ok=True)
    for name,value in outputs.items():(a.out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(outputs['coverage-delta.json'],indent=2))
