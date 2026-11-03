"""One-time integration audit; evidence only, not an application test oracle."""
import collections
import hashlib
import json
import pathlib
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

BASE = pathlib.Path('/workspace/scratch/bbca2890f602')
W = BASE / 'priority-twentieth-20261102'
OUT = BASE / 'priority147-evidence'
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(W / 'tools'))
from current_localization_contracts import decode_display, require_string_root
from translation_catalogues import placeholders

def git(*args):
    return subprocess.check_output(['git', '-C', str(W), *args], text=True).strip()

def read_checked(path, expected):
    b = pathlib.Path(path).read_bytes()
    assert hashlib.sha256(b).hexdigest() == expected, path
    return json.loads(b)

old_rows = read_checked('/tmp/priority112-manifest.json', 'eda6307269f03876e4527cd686dfc86c8bd856dcd88c132d97a380ae16deecb8')
frozen = read_checked(BASE/'priority112-frozen-input.json', 'cd34764f3bd3d11591bea604092d6532c6f7a3b9da6c425159990aab680b3caa')
new_input = read_checked(BASE/'cohort-b-research-20261102-late/public-accepted-save-recovery35.json', '28e9778979e8fda0d69d7147434b854e40b3c401a26c6d30012b056d1bbd488b')
review = read_checked(BASE/'cohort-b-research-20261102-late/public-review-save-recovery35.json', 'dfbca1796f404095b20d09b068a82de514d1d448bf5a26ced33e530da9be1ef7')
gaps = read_checked('/tmp/current-priority-gaps-82e4ad5.json', 'e5fc68ff54567080b95c5dfb60d8ddde6dabeaa576784b80e4f72a9c42697c2e')
assert git('rev-parse', 'HEAD^{tree}') == 'aff7631225f56f3c8036d62b6f80851f2e3b4129'
assert git('write-tree') == 'b680233f1a85163d27f69b2d2baa2c81dabdb179'
assert not git('diff', '--name-only'), 'Unstaged changes before integration'
assert git('hash-object', 'translations/string-importance.json') == 'e76a3a440a8b169d31f5ab5d163a2695b0db93b1'
importance = json.loads((W/'translations/string-importance.json').read_text())
tiers = {key.split('/',1)[1]: tier['id'] for tier in importance['tiers'] for key in tier['keys']}
english = {x.get('name'): x for x in ET.parse(W/'Paintroid/src/main/res/values/strings.xml').getroot()}
prior_input = {(r['locale'],r['key']): r for r in frozen}
rows = []
for r0 in old_rows:
    r = dict(r0)
    r['tier'] = prior_input[r['locale'],r['key']]['tier']
    r['origin'] = 'recovered112/' + pathlib.Path(r['origin']).name
    r['coverage_kind'] = prior_input[r['locale'],r['key']].get('coverage_kind', 'linguistic')
    rows.append(r)
for r in new_input['entries']:
    raw = r['value']
    display = r.get('display', decode_display(raw))
    # Source packet values are canonical Android source, not automatic morphology.
    row = dict(locale=r['locale'], key=r['key'], raw=raw, display=display,
               attributes=r['attributes'], tier=r['tier'],
               origin='public-accepted-save-recovery35.json', coverage_kind='source/compositional linguistic',
               path=f"Paintroid/src/main/res/values-b+{r['locale']}/strings.xml")
    rows.append(row)
assert len(rows) == 147 and len({(r['locale'],r['key']) for r in rows}) == 147
assert collections.Counter(r['tier'] for r in rows) == {'P0':63,'P1':84}
updated = {}
for r in rows:
    key = r['key']; path = r['path']; base = ET.fromstring(git('show', 'HEAD:'+path))
    assert tiers[key] == r['tier'] and r['tier'] in ('P0','P1'), (r['locale'],key)
    assert 'string/'+key in gaps[r['locale']][r['tier']]['missing_keys'], (r['locale'],key,'not originally missing')
    assert base.find(f"string[@name='{key}']") is None, (r['locale'],key,'already in base')
    assert r['attributes'] == english[key].attrib, (r['locale'],key,'attrs differ')
    assert placeholders(r['raw']) == placeholders(''.join(english[key].itertext())), (r['locale'],key,'slots differ')
    assert decode_display(r['raw']) == r['display'], (r['locale'],key,'display differs')
    text = updated.get(path, (W/path).read_text())
    root = ET.fromstring(text)
    if r['origin'] == 'public-accepted-save-recovery35.json':
        assert root.find(f"string[@name='{key}']") is None, (r['locale'],key,'already in recovered112')
        line = '    <string '+' '.join(k+'='+quoteattr(v) for k,v in r['attributes'].items())+'>'+escape(r['raw'])+'</string>\n'
        assert text.count('</resources>') == 1
        text = text.replace('</resources>', line+'</resources>')
        root = ET.fromstring(text)
        updated[path] = text
    require_string_root(root,key,r['raw'],{'attributes':r['attributes']})

# Preserve all prior bytes line-for-line and every pre-existing XML element/attribute.
for path in sorted({r['path'] for r in rows}):
    original = git('show','HEAD:'+path)+'\n'
    current = updated.get(path,(W/path).read_text())
    o = ET.fromstring(original); c = ET.fromstring(current)
    assert all(line in current.splitlines() for line in original.splitlines()), path
    for n in o:
        matches=[x for x in c if x.tag==n.tag and x.get('name')==n.get('name')]
        assert len(matches)==1,(path,n.get('name'))
        n.tail=None; matches[0].tail=None
        assert ET.tostring(n)==ET.tostring(matches[0]),(path,n.get('name'))
for path,text in updated.items():
    (W/path).write_text(text)
subprocess.run(['git','-C',str(W),'add','--',*sorted(updated)],check=True)
tree=git('write-tree')
base_leaves={line.split('\t')[1]:line.split('\t')[0].split() for line in git('ls-tree','-r','HEAD').splitlines()}
head_leaves={line.split('\t')[1]:line.split('\t')[0].split() for line in git('ls-tree','-r',tree).splitlines()}
assert set(base_leaves)==set(head_leaves)
changed={p for p in base_leaves if base_leaves[p]!=head_leaves[p]}
assert changed=={r['path'] for r in rows}
assert all(base_leaves[p][:2]==head_leaves[p][:2] for p in base_leaves)
counts=git('diff','--cached','--numstat').splitlines()
assert sum(int(x.split('\t')[0]) for x in counts)==147
assert sum(int(x.split('\t')[1]) for x in counts)==0
for name,value in [('manifest.json',rows),('recovered112-frozen-input.json',frozen),('adopted35-candidate.json',new_input),('adopted35-review.json',review)]:
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
receipt=dict(scope='Frozen coherent next PR: recovered112 + root-adopted35; later wording excluded',
             actual_parent='79bfae14b8138d2464756cfb13f508635ed25765',
             synthetic_local_base=git('rev-parse','HEAD'),base_tree=git('rev-parse','HEAD^{tree}'),tree=tree,
             original_importance_blob='e76a3a440a8b169d31f5ab5d163a2695b0db93b1',
             original_missing_inventory_sha256='e5fc68ff54567080b95c5dfb60d8ddde6dabeaa576784b80e4f72a9c42697c2e',
             counts=dict(collections.Counter(r['tier'] for r in rows)),
             locales=dict(collections.Counter(r['locale'] for r in rows)),
             coverage_kinds=dict(collections.Counter(r['coverage_kind'] for r in rows)),
             leaves=len(head_leaves),changed_paths=sorted(changed),additions=147,deletions=0,
             checks=['147 unique original-missing P0/P1 identities','all absent in exact actual-parent tree',
                     'source attributes and typed placeholders match current English',
                     'all selected raw Android strings and decoded displays match reviewed manifests',
                     'all prior XML entries/attributes and original lines preserved',
                     'every untouched blob and all file modes preserved'],
             not_claimed=['native fluency','layout fit','Android compilation before hosted artifact inspection'],
             historical_outcomes='Prior 108-row local pass does not qualify this147 candidate; recovered112 retained without preparation-script replay.')
(OUT/'integration-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
(OUT/'source.diff').write_text(git('diff','--cached')+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
