"""Exercise existing gallery label sinks with arbitrary display text, not HTML."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'


class GalleryTranslationDataTest(unittest.TestCase):
    def test_quotes_controls_unicode_and_repeated_adaptation_keep_action_identity(self):
        node=shutil.which('node')
        if node is None: self.skipTest('Node unavailable; Android quoting test still applies')
        source=(JAVA/'GalleryPage.kt').read_text()
        self.assertIn('${JSONObject.quote(useLabel)}',source)
        self.assertIn('${JSONObject.quote(copyLabel)}',source)
        script=source.split('"""',2)[1]
        # Metadata extraction is independently tested. No metadata inputs are
        # involved in this label-only DOM test.
        use='\"\\\n\u2028\u2029\u202eᠮᠣᠩᠭᠣᠯ\u202c <img src=x onerror=boom()> %1$999999s'
        copy="';globalThis.boom(); // 𡨸 👩🏽‍🎨"
        for old,new in {'${JSONObject.quote(useLabel)}':json.dumps(use),
                        '${JSONObject.quote(copyLabel)}':json.dumps(copy),
                        '${ArtworkMetadata.script}':"function artworkCredit() {return '';}",
                        '${IllustrationPage.USE_SCHEME}':'anpaint-gallery-use',
                        '$CREDIT_SCHEME':'anpaint-gallery-credit'}.items(): script=script.replace(old,new)
        self.assertNotIn('${',script)
        harness=r'''
const vm=require('node:vm'), assert=require('node:assert/strict');
const script=SCRIPT, expectedUse=USE, expectedCopy=COPY;
let copy=null, mutations=0, disconnected=0;
const parent={querySelector:()=>copy};
const link={parentElement:parent,className:'download',href:'https://catrobat.org/picture.png',textContent:'old',
 attrs:{},getAttribute(k){return this.attrs[k]??null;},setAttribute(k,v){this.attrs[k]=v;mutations++;},
 insertAdjacentElement(where,value){copy=value;copy.parentElement=parent;mutations++;}};
const document={body:{},getElementById:()=>null,querySelectorAll:()=>[link],createElement:()=>({style:{},attrs:{},
 getAttribute(k){return this.attrs[k]??null;},setAttribute(k,v){this.attrs[k]=v;mutations++;}})};
const context=vm.createContext({URL,document,location:{href:'https://catrobat.org/artwork/'},window:{},
 MutationObserver:class {observe(){} disconnect(){disconnected++;}},boom(){throw Error('Label executed');}});
vm.runInContext(script,context,{timeout:1000});
assert.equal(link.textContent,expectedUse);assert.equal(link.attrs['aria-label'],expectedUse);
assert.equal(copy.textContent,expectedCopy);
assert.equal(new URL(link.attrs.href).protocol,'anpaint-gallery-use:');
assert.equal(new URL(copy.attrs.href).protocol,'anpaint-gallery-credit:');
assert.equal(new URL(link.attrs.href).searchParams.get('source'),'https://catrobat.org/picture.png');
const before=copy;
for(let i=0;i<5;i++) vm.runInContext(script,context,{timeout:1000});
assert.equal(copy,before);assert.equal(disconnected,5);assert.equal(copy.textContent,expectedCopy);
'''
        harness=harness.replace('SCRIPT',json.dumps(script)).replace('USE',json.dumps(use)).replace('COPY',json.dumps(copy))
        result=subprocess.run([node,'-e',harness],text=True,capture_output=True,timeout=10)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
