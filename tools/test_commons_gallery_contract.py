"""AN Paint (2026), AGPL-3.0-or-later. Execute the Commons adapter with a tiny DOM fixture.

This checks URL/action contracts and idempotent mutation, not Android WebView rendering.
Native browser and attribution regressions live in CommonsCreditDeviceTest.
"""
from pathlib import Path
import json
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommonsGalleryContractTest(unittest.TestCase):
    def test_original_links_index_pages_labels_and_idempotency(self):
        node = shutil.which('node')
        if node is None:
            self.skipTest('Node unavailable; native WebView tests are still required')
        text = (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationPage.kt').read_text()
        script = text.split('private fun commonsScript', 1)[1].split('"""', 2)[1]
        substitutions = {
            '${JSONObject.quote(useLabel)}': json.dumps('Use image'),
            '${JSONObject.quote(copyLabel)}': json.dumps('Copy credit'),
            '${USE_SCHEME}': 'anpaint-gallery-use',
            '${GalleryPage.CREDIT_SCHEME}': 'anpaint-gallery-credit',
            '${"$"}': '$',
        }
        for key, value in substitutions.items():
            script = script.replace(key, value)
        self.assertNotIn('${', script)
        harness = r'''
const vm = require('node:vm'); const assert = require('node:assert/strict');
const script = SCRIPT;
let checks = 0;
function fixture(page, source, expected) {
  let mutations = 0, row;
  class Element {
    constructor() { this.children=[]; this.style={}; this.attributes={}; this._text=''; }
    set textContent(v) { this._text=v;mutations++; } get textContent() { return this._text; }
    setAttribute(k,v) { this.attributes[k]=v;mutations++; }
    getAttribute(k) { return this.attributes[k] ?? null; }
    appendChild(el) { this.children.push(el);mutations++; }
  }
  const original = {href:source,insertAdjacentElement:(_,r)=>{row=r;mutations++;}};
  const document = {title:'File:Test map - Wikimedia Commons',body:{},
    querySelector:()=>original,getElementById:()=>row,createElement:()=>new Element()};
  const context = vm.createContext({URL,document,location:{href:page},window:{},
    MutationObserver:class {observe() {} disconnect() {}}});
  vm.runInContext(script,context,{timeout:1000});
  assert.equal(!!row,expected); checks++;
  if(!expected) return;
  assert.equal(row.children.length,2); checks++;
  const use=new URL(row.children[0].getAttribute('href'));
  const credit=new URL(row.children[1].getAttribute('href'));
  assert.equal(use.protocol,'anpaint-gallery-use:'); assert.equal(credit.protocol,'anpaint-gallery-credit:');checks+=2;
  for(const action of [use,credit]) {
    assert.equal(action.searchParams.get('source'),source);
    assert.equal(action.searchParams.get('page'),page);checks+=2;
  }
  assert.equal(row.children[1].textContent,'Copy credit');checks++;
  const before=mutations; vm.runInContext(script,context,{timeout:1000});
  assert.equal(mutations,before,'Repeated adaptation must not trigger another mutation'); checks++;
}
const host='https://upload.wikimedia.org/wikipedia/commons/';
fixture('https://commons.wikimedia.org/wiki/File:Test.svg',host+'a/ab/Test.svg',true);
fixture('https://commons.wikimedia.org/w/index.php?title=File%3ATest.png',host+'a/ab/Test.png',true);
fixture('https://commons.wikimedia.org/wiki/File%3ATest.svg',host+'a/ab/Test.svg',true);
fixture('https://commons.wikimedia.org/wiki/Category:Blank_maps',host+'a/ab/Test.svg',false);
fixture('https://commons.wikimedia.org/wiki/File:Test.svg',host+'thumb/a/ab/Test.svg/800px-Test.svg.png',false);
fixture('https://commons.wikimedia.org/wiki/File:Test.svg',host+'archive/a/ab/Test.svg',false);
fixture('https://commons.wikimedia.org/wiki/File:Test.svg','https://upload.wikimedia.org.evil.example/wikipedia/commons/a/ab/Test.svg',false);
fixture('https://commons.wikimedia.org/wiki/File:Test.svg','https://user@upload.wikimedia.org/wikipedia/commons/a/ab/Test.svg',false);
console.log(checks+' Commons URL/action/mutation assertions passed');
'''.replace('SCRIPT', json.dumps(script))
        run = subprocess.run([node, '-e', harness], capture_output=True, text=True, timeout=15)
        self.assertEqual(0, run.returncode, run.stderr)
        self.assertIn('35 Commons URL/action/mutation assertions passed', run.stdout)


if __name__ == '__main__':
    unittest.main()
