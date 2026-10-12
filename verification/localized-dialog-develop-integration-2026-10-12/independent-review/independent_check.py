import base64, hashlib, itertools, json, pathlib, subprocess, sys, xml.etree.ElementTree as ET
ROOT=pathlib.Path('/workspace/shared/anpaint-pr52-current-develop-20261012')
OUT=pathlib.Path(__file__).parent

def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args])
def content(ref,path): return git('show',f'{ref}:{path}')
def sha(v): return hashlib.sha256(v).hexdigest()
def paths(ref,prefix=''): return git('ls-tree','-r','--name-only',ref,'--',prefix or '.').decode().splitlines()
def data(name): return json.loads((ROOT/'tools/fixtures'/name).read_bytes())
def demand(ok,message):
    if not ok: raise AssertionError(message)
def replace(b,old,new):
    old=old.encode() if isinstance(old,str) else old;new=new.encode() if isinstance(new,str) else new
    demand(b.count(old)==1,'Exact substitution absent or duplicated')
    return b.replace(old,new,1)

result={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'notes':['Local refs are independently supplied snapshots, not remote commit identities.','Checks below are source/host checks, not runtime or linguistic acceptance.']}
m02=data('commons_metadata_http_scope.json');m03=data('commons_metadata_response_limit_scope.json');c05=data('hungarian_attribution_c05_scope.json')
rows02={r['path']:r for r in m02['entries']};rows03={r['path']:r for r in m03['entries']}
demand(rows02.keys()==rows03.keys(),'M02/M03 scopes differ')
oldfixture=['commons_metadata_http_scope.json','commons_metadata_m02_production_scope.json','hungarian_attribution_c05_scope.json','localized_dialog_composition_scope.json']
newfixture=['commons_metadata_response_limit_scope.json','commons_metadata_m03_production_scope.json','commons_metadata_m03_font_scope.json']
for ref,names in [('accepted-pr52',oldfixture),('current-develop',newfixture)]:
    for n in names:demand(content(ref,'tools/fixtures/'+n)==(ROOT/'tools/fixtures'/n).read_bytes(),'Historical fixture changed: '+n)
result['immutable_fixture_count']=len(oldfixture)+len(newfixture)

def strip(which,path,b):
    if which in ('m02','m03'):
        return replace(b,({'m02':rows02,'m03':rows03}[which])[path]['line'],b'')
    if path.endswith('/values-hu/strings.xml'):
        for r in c05['entries']:b=replace(b,r['after'],r['before'])
    return b
resource_receipts=[];negative_count=0
for p,r in rows02.items():
    b=(ROOT/p).read_bytes()
    demand(strip('m03',p,b)==content('accepted-pr52',p),'M03-only removal does not restore PR52: '+p)
    demand(strip('c05',p,strip('m02',p,b))==content('current-develop',p),'M02/C05 removal does not restore develop: '+p)
    for order in itertools.permutations(('m02','m03','c05')):
        v=b
        for which in order:v=strip(which,p,v)
        demand(sha(v)==r['before_sha256']==rows03[p]['before_sha256'],'Shared historical endpoint not restored: '+p)
    for which,rr in [('m02',r),('m03',rows03[p])]:
        line=rr['line'].encode()
        for mutation in (b'',line*2,line.replace(b'Commons',b'AlteredProvider',1)):
            try:strip(which,p,replace(b,line,mutation))
            except AssertionError:negative_count+=1
            else:raise AssertionError('Undetected resource mutation')
    # XML delta does not silently change any other entry, attributes, plural/array or root.
    before=ET.fromstring(content('current-develop',p));after=ET.fromstring(b)
    def xml_index(root):return {(e.tag,e.attrib.get('name')):ET.tostring(e) for e in root}
    a=xml_index(before);z=xml_index(after)
    demand(z.keys()-a.keys()=={('string','commons_metadata_http_error')},'Unexpected new resource key')
    demand(not a.keys()-z.keys(),'Deleted resource key')
    actual={k[1] for k in a.keys()&z.keys() if a[k]!=z[k]}
    expected={x['key'] for x in c05['entries']} if p.endswith('/values-hu/strings.xml') else set()
    demand(actual==expected,'Unexpected resource replacement: '+p)
    resource_receipts.append({'path':p,'six_orders':True,'pr52_endpoint':True,'develop_endpoint':True})
all_resources=[p for p in paths('HEAD','Paintroid/src/main/res') if p.endswith('/strings.xml')]
for p in all_resources:
    if p not in rows02:demand((ROOT/p).read_bytes()==content('current-develop',p)==content('accepted-pr52',p),'Unscoped resource change: '+p)
result['resources']={'catalogues':len(rows02),'all_reversal_orders':6*len(rows02),'negative_mutations_rejected':negative_count,'unscoped_catalogues_unchanged':len(all_resources)-len(rows02),'rows':resource_receipts}
# Independently recover each original full production endpoint, using literal exact replacements.
java='Paintroid/src/main/java/org/catrobat/paintroid/classic/'
http='    /** Do not classify provider/framework exceptions by their text or format their detail twice. */\n    private fun commonsMetadataReason(error: Exception): String? =\n        if(error is CommonsAttribution.HttpException) ui(R.string.commons_metadata_http_error,error.status.toString())\n        else error.message\n\n'
limitbranch='        else if(error is CommonsAttribution.ResponseLimitException) ui(R.string.commons_metadata_response_too_large)\n'
combined=http.replace('        else error.message\n',limitbranch+'        else error.message\n')
prod02=data('commons_metadata_m02_production_scope.json')['entries'];prod03=data('commons_metadata_m03_production_scope.json')['entries']
prods=[]
for a,z in zip(prod02,prod03):
    p=a['path'];demand(p==z['path'],'Producer path mismatch');b=(ROOT/p).read_bytes()
    if p.endswith('CommonsAttribution.kt'):
        just02=b
        for e in reversed(z['edits']):just02=replace(just02,e['after'],e['before'])
        just03=b
        for e in reversed(a['edits']):just03=replace(just03,e['after'],e['before'])
    else:
        just02=replace(b,combined,http)
        just03=replace(b,combined,'')
        just03=replace(just03,z['edits'][0]['before'],z['edits'][0]['after'])
    demand(just02==content('accepted-pr52',p),'PR52 producer not recovered')
    demand(just03==content('current-develop',p),'Develop producer not recovered')
    demand(sha(just02)==a['after_sha256'] and sha(just03)==z['after_sha256'],'Standalone pin mismatch')
    endpoint02=just02;endpoint03=just03
    for e in reversed(a['edits']):endpoint02=replace(endpoint02,e['after'],e['before'])
    for e in reversed(z['edits']):endpoint03=replace(endpoint03,e['after'],e['before'])
    demand(endpoint02==endpoint03,'Original endpoints differ')
    demand(sha(endpoint02)==a['before_sha256']==z['before_sha256'],'Original pin mismatch')
    prods.append({'path':p,'original_sha256':sha(endpoint02),'pr52_sha256':sha(just02),'develop_sha256':sha(just03)})
result['production_endpoints']=prods
# Production inheritance independently excludes all unrelated production deltas.
unchanged52=[];unchangeddevelop=[]
for p in paths('HEAD','Paintroid/src/main')+paths('HEAD','app/src/main'):
    b=(ROOT/p).read_bytes()
    if p.startswith('Paintroid/src/main/res/') and p.endswith('/strings.xml'):continue
    if p in {r['path'] for r in prod02}:continue
    if p.startswith('Paintroid/src/main/assets/fonts/'):
        demand(b==content('current-develop',p),'Merged font asset changed: '+p);unchangeddevelop.append(p)
    else:
        demand(b==content('accepted-pr52',p),'PR52 production source changed: '+p);unchanged52.append(p)
result['unchanged_production_paths']={'from_pr52':len(unchanged52),'font_paths_from_develop':len(unchangeddevelop)}
fontscope=data('commons_metadata_m03_font_scope.json');p='Paintroid/src/main/assets/fonts/anpaintnomui.ttf';b=(ROOT/p).read_bytes()
demand(sha(b)==fontscope['after_sha256'],'Font after hash');rev=b
for e in reversed(fontscope['edits']):
    at=e['after_offset'];a=base64.b64decode(e['after_base64'],validate=True);z=base64.b64decode(e['before_base64'],validate=True)
    demand(rev[at:at+len(a)]==a,'Font byte reversal mismatch');rev=rev[:at]+z+rev[at+len(a):]
demand(sha(rev)==fontscope['before_sha256'] and rev==content('accepted-pr52',p),'Font before hash')
result['font']={'merged_sha256':sha(b),'recovered_pr52_sha256':sha(rev),'exact_develop_bytes':True}
# Runtime tests stay exact except the single explicitly M03-superseded expectation.
accepted_kotlin=[p for p in paths('accepted-pr52') if p.endswith('.kt') and ('/src/test/' in p or '/src/androidTest/' in p)]
changed=[p for p in accepted_kotlin if (ROOT/p).read_bytes()!=content('accepted-pr52',p)]
demand(changed==['Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsCopyCreditErrorTest.kt'],'Unexpected changed accepted runtime tests')
result['runtime_test_preservation']={'accepted_source_files':len(accepted_kotlin),'exactly_preserved':len(accepted_kotlin)-len(changed),'changed':changed}
result['success']=True
(OUT/'independent-preservation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='resources'},indent=2));print('Resource catalogue checks:',len(rows02),'all reversal orders:',6*len(rows02),'negative controls:',negative_count)
