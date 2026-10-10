"""Execute injected gallery controls against a minimal publisher DOM, using Node."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'


def script(name, replacements, declaration=None):
    source = (SOURCE / name).read_text()
    if declaration is not None:
        source = source.split(declaration, 1)[1]
    source = source.split('"""', 2)[1]
    for before, after in replacements.items():
        source = source.replace(before, after)
    return source


class GalleryTypographyTests(unittest.TestCase):
    def test_only_app_actions_are_marked_and_repeated_adaptation_keeps_publisher_content(self):
        common = {
            '${ArtworkMetadata.script}': "function artworkCredit(){return '';}",
            '${JSONObject.quote(useLabel)}': json.dumps('𡨸 Use'),
            '${JSONObject.quote(copyLabel)}': json.dumps('ᠮᠠᠨᠵᡠ Copy'),
            '${IllustrationPage.USE_SCHEME}': 'anpaint-gallery-use',
            '${USE_SCHEME}': 'anpaint-gallery-use',
            '$USE_SCHEME': 'anpaint-gallery-use',
            '${GalleryPage.CREDIT_SCHEME}': 'anpaint-gallery-credit',
            '$CREDIT_SCHEME': 'anpaint-gallery-credit',
            "${'$'}": '$',
            '${"$"}': '$',
        }
        scripts = {
            'CATROBAT': script('GalleryPage.kt', common),
            'IRASUTOYA': script('IllustrationPage.kt', common | {'${JSONObject.quote(provider.name)}': '"IRASUTOYA"'}),
            'OPENCLIPART': script('IllustrationPage.kt', common | {'${JSONObject.quote(provider.name)}': '"OPENCLIPART"'}),
            'COMMONS': script('IllustrationPage.kt', common, 'private fun commonsScript'),
        }
        runner = r'''
const assert=require('assert');const vm=require('vm');
const scripts=JSON.parse(process.argv[1]);
for(const [provider,script] of Object.entries(scripts)) {
  class Element {
    constructor(){this.attributes={};this.style={};this.children=[];this.textContent='Publisher artwork';this.className='publisher-button';}
    setAttribute(key,value){this.attributes[key]=value;if(key==='href')this.href=value;}
    getAttribute(key){return this.attributes[key]===undefined?null:this.attributes[key];}
    hasAttribute(key){return key in this.attributes;}
    appendChild(child){this.children.push(child);child.parentElement=this;}
    insertAdjacentElement(_,child){this.nextElementSibling=child;this.parentElement.appendChild(child);}
    querySelector(query){if(query==='img')return {alt:'Original title'};return this.children.find(x=>x.hasAttribute('data-anpaint-credit'))||null;}
  }
  const parent=new Element(),anchor=new Element(),title=new Element(),prose=new Element();parent.appendChild(anchor);
  const paths={CATROBAT:['https://catrobat.org/art.png','/figures-download/'],IRASUTOYA:['https://blogger.googleusercontent.com/art.png','/2026/01/art.html'],OPENCLIPART:['https://openclipart.org/image/2000px/123','/detail/123/art'],COMMONS:['https://upload.wikimedia.org/wikipedia/commons/1/12/Map.svg','/wiki/File:Map.svg']};
  anchor.href=paths[provider][0];const originalTitle=title.textContent,originalProse=prose.textContent;
  const originalAnchorText=anchor.textContent,originalAnchorHref=anchor.href;
  const document={body:{},title:'Original map - Wikimedia Commons',querySelectorAll:()=>[anchor],querySelector:q=>q.startsWith('.fullMedia ')?anchor:title,getElementById:id=>id==='anpaint-commons-actions'?(parent.children.find(x=>x.id===id)||null):title,createElement:()=>new Element()};
  const window={};const sandbox={document,window,URL,encodeURIComponent,location:{href:'https://publisher.example'+paths[provider][1],pathname:paths[provider][1]},MutationObserver:class {constructor(callback){this.callback=callback;}observe(){}disconnect(){}}};
  vm.runInNewContext(script,sandbox);
  let controls=provider==='CATROBAT'?[anchor,parent.children[1]]:anchor.nextElementSibling.children;
  assert.equal(controls.length,2);
  for(const item of controls)assert.equal(item.getAttribute('data-anpaint-action'),'true');
  const count=parent.children.length;
  for(const item of controls)delete item.attributes['data-anpaint-action'];
  (window.anPaintGalleryObserver||window.anPaintIllustrationObserver||window.anPaintCommonsObserver).callback();
  assert.equal(parent.children.length,count,'No duplicate buttons on page mutation');
  for(const item of controls)assert.equal(item.getAttribute('data-anpaint-action'),'true','Reused actions retain typography');
  assert.equal(title.textContent,originalTitle);assert.equal(prose.textContent,originalProse);
  assert.deepEqual(parent.style,{});assert.equal(parent.getAttribute('data-anpaint-action'),null);
  if(provider==='COMMONS') {
    assert.equal(anchor.textContent,originalAnchorText);assert.equal(anchor.href,originalAnchorHref);
    assert.equal(anchor.getAttribute('data-anpaint-action'),null);assert.deepEqual(anchor.style,{});
  }
}
'''
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node is required to execute gallery DOM checks')
        subprocess.run([node, '-e', runner, json.dumps(scripts)], check=True, capture_output=True, text=True)

    def test_font_style_is_idempotent_and_scoped_to_marked_controls(self):
        source = script('GalleryTypography.kt', {'${JSONObject.quote(css(context,locale))}': json.dumps('[data-anpaint-action]{font-family:ANPaintAction;}')})
        runner = r'''
const assert=require('assert');const vm=require('vm');let styles=[];
const document={head:{appendChild:s=>styles.push(s)},getElementById:id=>styles.find(s=>s.id===id),createElement:()=>({})};
const script=process.argv[1];const sandbox={document};vm.runInNewContext(script,sandbox);vm.runInNewContext(script,sandbox);
assert.equal(styles.length,1);assert.equal(styles[0].id,'anpaint-action-typography');
assert.equal(styles[0].textContent,'[data-anpaint-action]{font-family:ANPaintAction;}');
'''
        subprocess.run([shutil.which('node'), '-e', runner, source], check=True, capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()
