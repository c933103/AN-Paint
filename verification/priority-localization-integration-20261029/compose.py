from pathlib import Path
import subprocess,json,difflib,re
R=Path('/tmp/combined-localization-20261029/repo')
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
def show(ref,p):return git('show',ref+':'+p).decode()
BASE='origin/develop'; refs=['source/pr215','source/pr218','source/pr217','source/pr220']
changes={}
for ref in refs:
    mergebase=git('merge-base',BASE,ref).decode().strip()
    for p in git('diff','--name-only',mergebase,ref).decode().splitlines():changes.setdefault(p,[]).append(ref)
shared=[p for p,rs in changes.items() if len({git('rev-parse',r+':'+p) for r in rs})>1]
print('shared',shared)
Path('/tmp/combined-localization-20261029/changed-sources.json').write_text(json.dumps(changes,indent=2))
subprocess.run(['git','-C',str(R),'merge','--abort'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
subprocess.run(['git','-C',str(R),'reset','--hard',BASE],check=True)
for p,rs in changes.items():
    if p in shared:continue
    subprocess.run(['git','-C',str(R),'checkout',rs[0],'--',p],check=True)
# Merge ImportSelection: source215 has DA/NO, source217 adds NN in disjoint region.
p='Paintroid/src/test/java/org/catrobat/paintroid/local/ImportSelectionTitleTest.kt'
subprocess.run(['git','-C',str(R),'checkout','source/pr215','--',p],check=True)
patch=git('diff','0070c5816ad31911d227fab50ea193e2a39b13ab','source/pr217','--',p)
subprocess.run(['git','-C',str(R),'apply','-'],input=patch,check=True)
# The remaining shared tests start with HI/GU + Thai and retain each other cohort's exact inserted blocks.
for p in shared:
    if p.endswith('ImportSelectionTitleTest.kt'):continue
    s=show('source/pr218',p)
    base=show('0070c5816ad31911d227fab50ea193e2a39b13ab',p)
    if p.endswith('TaggedColourImportTest.kt'):continue
    if p.endswith('test_memory_warning_source_review.py') or p.endswith('test_memory_warning_successors.py'):
        s=s.replace('import EXACT_SCRIPT_ADDITIONS','import NORDIC_ADDITIONS, NN_BE_SQ_ADDITIONS, HR_BS_MK_ADDITIONS, EXACT_SCRIPT_ADDITIONS')
        s=s.replace(' | HI_GU_ADDITIONS',' | NORDIC_ADDITIONS | NN_BE_SQ_ADDITIONS | HR_BS_MK_ADDITIONS | HI_GU_ADDITIONS')
    else:
        # Exact insertions from the three independent sources, anchored to unchanged base neighbors.
        for ref in ['source/pr215','source/pr217','source/pr220']:
            b=base.splitlines(True); t=show(ref,p).splitlines(True)
            for tag,i,j,x,y in reversed(difflib.SequenceMatcher(None,b,t,autojunk=False).get_opcodes()):
                if tag!='insert':continue
                payload=''.join(t[x:y]);anchor=''.join(b[i:i+2])
                if payload in s:continue
                if i==0:s=payload+s
                else:
                    for length in range(2,80):
                        anchor=''.join(b[i:i+length])
                        if s.count(anchor)==1:break
                    assert s.count(anchor)==1,(p,ref,'anchor',anchor)
                    s=s.replace(anchor,payload+anchor)
        if p.endswith('test_current_localization_contracts.py'):
            # Distinguish full SVG cohorts from only newly direct colour members.
            s=s.replace(' | HI_GU_TAGS',' | NORDIC_TAGS | NN_BE_SQ_TAGS | HI_GU_TAGS')
            s=s.replace('set(HI_GU_TAGS)','NORDIC_COLOUR_TAGS | NN_BE_SQ_COLOUR_TAGS | {\'mk\'} | set(HI_GU_TAGS)')
            s=s.replace('or catalogue in HI_GU_TAGS','or catalogue in NORDIC_COLOUR_TAGS or catalogue in NN_BE_SQ_COLOUR_TAGS or catalogue == \'mk\' or catalogue in HI_GU_TAGS')
            s=s.replace('FAMILY_EXTRA_TAGS[FAMILIES[2]] |= set(GA_GD_CY_TAGS)','FAMILY_EXTRA_TAGS[FAMILIES[2]] |= set(GA_GD_CY_TAGS) | set(hr_bs_mk.TAGS)')
            s=s.replace("TAGGED_COLOUR_EXTRA_TAGS = {'am'","TAGGED_COLOUR_EXTRA_TAGS = {'mk', 'am'")
            s=s.replace("extra_tags = {'am'","extra_tags = set(hr_bs_mk.TAGS) | {'am'")
            s=s.replace("self.assertEqual({'am', 'sv'","self.assertEqual(set(hr_bs_mk.TAGS) | {'am', 'sv'")
    (R/p).write_text(s)
# Tagged test: every historical checkpoint survives, followed by every exact finite addition.
p='Paintroid/src/test/java/org/catrobat/paintroid/local/TaggedColourImportTest.kt';s=show('source/pr218',p)
blocks=[]
for ref,start in [('source/pr215','        val nordic='),('source/pr217','        val recovered='),('source/pr220','        val macedonian=')]:
    t=show(ref,p);a=t.index(start);b=t.index('        assertTrue(expected.has("bg"))',a)
    block=t[a:b];block=re.sub(r'        assertEquals\(\d+,expected.length\(\)\)\n','',block)
    blocks.append(block)
anchor='        // Finite recovered HI/GU additions after all existing checkpoints.'
s=s.replace(anchor,''.join(blocks)+anchor)
s=s.replace('        assertEquals(143, expected.length())\n','')
s=s.replace('        assertEquals(144, expected.length())\n','''        // The five candidates add this disjoint union, not five standalone totals.
        val combinedAddedTags = setOf("is", "hi", "gu", "be", "sq", "th", "mk")
        assertEquals(7, combinedAddedTags.size)
        assertTrue(combinedAddedTags.all { expected.has(it) })
        assertEquals(141 + combinedAddedTags.size, expected.length())
        val expectedFallbacks = 171 - expected.length()
        assertEquals(23, expectedFallbacks)
''')
s=s.replace('        assertEquals(27, fallbacks) // 171 offered - 144 direct, including Thai replacement; no inherited catalogue.','        assertEquals(expectedFallbacks, fallbacks) // 171 offered - 148 direct; no inherited catalogue.')
(R/p).write_text(s)
print('composed',len(changes),'files')
