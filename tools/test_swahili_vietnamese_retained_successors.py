"""Four source-bound successors, not fresh whole-language or installed-UI certification."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

from test_danish_norwegian_p0_wording import FULL_FORMAT_TOKEN
import translation_catalogues as catalogues

FIXTURE=Path(__file__).parent/'fixtures/current_localization/swahili_vietnamese_retained_successors.json'
KEYS={'sw':{'string/ui_draw_again','plurals/ui_crop_preview_images'},
      'vi':{'string/ui_show_magnified_drawing_preview','plurals/ui_crop_preview_images'}}
QUANTITIES={'sw':{'one','other'},'vi':{'other'}}
PREVIOUS={
 'sw':{'string/ui_draw_again':'Chora tena',
       'plurals/ui_crop_preview_images':{
          'one':r'Onyesho: %1$d × %2$d px\nTumia kwa picha %3$d. Kukata picha iliyowekwa husogeza viambatisho vyake.',
          'other':r'Onyesho: %1$d × %2$d px\nTumia kwa picha %3$d. Kukata picha zilizowekwa husogeza viambatisho vyake.'}},
 'vi':{'string/ui_show_magnified_drawing_preview':'Hiện xem trước vẽ phóng đại',
       'plurals/ui_crop_preview_images':{
          'other':r'Xem trước: %1$d × %2$d px\nÁp dụng cho %3$d ảnh. Cắt ảnh đã đặt cũng điều chỉnh vị trí các ảnh gắn kèm.'}}
}


def require_shape(data):
    if data.get('schema_version')!=1 or set(data.get('locales',{}))!=set(KEYS):
        raise ValueError('Exact successor locale/schema set differs')
    for tag,locale in data['locales'].items():
        if set(locale.get('rows',{}))!=KEYS[tag]:raise ValueError('Exact typed successor scope differs')
        for identity,row in locale['rows'].items():
            typ,key=identity.split('/')
            if row.get('previous_target')!=PREVIOUS[tag][identity] or row.get('previous_attributes')!={'name':key}:
                raise ValueError('Exact historical predecessor differs')
            if row.get('attributes')!={'name':key} or row.get('source_attributes')!={'name':key}:
                raise ValueError('Exact resource attributes differ')
            if typ=='plurals':
                if set(row.get('target',{}))!=QUANTITIES[tag] or set(row.get('source',{}))!={'one','other'}:
                    raise ValueError('Complete plural quantity contract differs')
            elif not isinstance(row.get('target'),str) or not row['target']:
                raise ValueError('Complete string required')
    if data['locales']['vi']['rows']['string/ui_show_magnified_drawing_preview'].get('fresh_candidate') is not False:
        raise ValueError('Previously accepted Vietnamese magnifier is not new candidate credit')
    return data


def require_complete(root,identity,row):
    typ,key=identity.split('/');nodes=root.findall(f"./{typ}[@name='{key}']")
    if len(nodes)!=1 or nodes[0].attrib!=row['attributes']:raise ValueError('Typed resource/attribute mismatch')
    node=nodes[0]
    if typ=='string':
        if list(node) or node.text!=row['target']:raise ValueError('Complete successor differs')
        pairs=[(node.text,row['source'])]
    else:
        if any(n.tag!='item' or set(n.attrib)!={'quantity'} or list(n) for n in node):raise ValueError('Plural child shape differs')
        target={n.get('quantity'):n.text for n in node}
        if len(target)!=len(node) or target!=row['target']:raise ValueError('Complete plural successor differs')
        pairs=[(text,row['source'][quantity]) for quantity,text in target.items()]
    for target,source in pairs:
        if Counter(FULL_FORMAT_TOKEN.findall(target))!=Counter(FULL_FORMAT_TOKEN.findall(source)) or target.count(r'\n')!=source.count(r'\n'):
            raise ValueError('Complete token/newline contract differs')


class SwahiliVietnameseRetainedSuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=require_shape(json.loads(FIXTURE.read_text()))
        cls.roots={tag:ET.parse(catalogues.catalogue_paths()[tag]).getroot() for tag in KEYS}
        cls.english=ET.parse(catalogues.RES/'values/strings.xml').getroot()

    def test_all_four_typed_values_are_exact_and_source_bound(self):
        for tag,locale in self.data['locales'].items():
            for identity,row in locale['rows'].items():
                with self.subTest(tag=tag,identity=identity):
                    require_complete(self.roots[tag],identity,row)
                    typ,key=identity.split('/');e=self.english.find(f"./{typ}[@name='{key}']")
                    self.assertEqual(row['source_attributes'],e.attrib)
                    self.assertEqual(row['source'],e.text if typ=='string' else {n.get('quantity'):n.text for n in e})

    def test_predecessor_and_scope_laundering_are_rejected(self):
        mutations=[]
        for tag in KEYS:
            for identity in KEYS[tag]:
                bad=deepcopy(self.data);bad['locales'][tag]['rows'].pop(identity);mutations.append(bad)
                bad=deepcopy(self.data);bad['locales'][tag]['rows'][identity]['previous_target']='forged';mutations.append(bad)
        bad=deepcopy(self.data);bad['locales']['en']=bad['locales'].pop('sw');mutations.append(bad)
        bad=deepcopy(self.data);bad['locales']['vi']['rows']['string/ui_show_magnified_drawing_preview']['fresh_candidate']=True;mutations.append(bad)
        for bad in mutations:
            with self.assertRaises(ValueError):require_shape(bad)

    def test_every_full_value_rejects_wrong_locale_and_truncated_text(self):
        for tag,locale in self.data['locales'].items():
            for identity,row in locale['rows'].items():
                typ,key=identity.split('/')
                for replacement in ('wrong language',''):
                    root=deepcopy(self.roots[tag]);n=root.find(f"./{typ}[@name='{key}']")
                    if typ=='string':n.text=replacement
                    else:
                        for child in n:child.text=replacement
                    with self.assertRaises(ValueError):require_complete(root,identity,row)
                root=deepcopy(self.roots[tag]);root.find(f"./{typ}[@name='{key}']").set('formatted','false')
                with self.assertRaises(ValueError):require_complete(root,identity,row)

    def test_plural_quantity_removal_addition_duplicate_and_each_child_corruption_reject(self):
        identity='plurals/ui_crop_preview_images'
        for tag in KEYS:
            row=self.data['locales'][tag]['rows'][identity]
            for quantity in QUANTITIES[tag]:
                for mutation in ('remove','add','duplicate','wrong-token','truncate','newline','attribute','markup'):
                    root=deepcopy(self.roots[tag]);n=root.find("./plurals[@name='ui_crop_preview_images']");child=n.find(f"./item[@quantity='{quantity}']")
                    if mutation=='remove':n.remove(child)
                    elif mutation=='add':ET.SubElement(n,'item',{'quantity':'many'}).text=child.text
                    elif mutation=='duplicate':n.append(deepcopy(child))
                    elif mutation=='wrong-token':child.text=child.text.replace('%3$d','%3$s')
                    elif mutation=='truncate':child.text=child.text[:-1]
                    elif mutation=='newline':child.text=child.text.replace(r'\n',' ')
                    elif mutation=='attribute':child.set('formatted','false')
                    else:ET.SubElement(child,'b').text='markup'
                    with self.subTest(tag=tag,quantity=quantity,mutation=mutation),self.assertRaises(ValueError):require_complete(root,identity,row)
            other='vi' if tag=='sw' else 'sw'
            root=deepcopy(self.roots[tag]);n=root.find("./plurals[@name='ui_crop_preview_images']")
            for child in n:child.text=self.data['locales'][other]['rows'][identity]['target']['other']
            with self.assertRaises(ValueError):require_complete(root,identity,row)

    def test_return_to_drawing_consumer_does_not_recreate_content(self):
        source=(catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        self.assertIn('button(ui(R.string.ui_draw_again), "navigate_draw") { chooseTool(drawingTool) }',source)
        self.assertEqual('Rudi kuchora',self.data['locales']['sw']['rows']['string/ui_draw_again']['target'])

    def test_magnifier_label_remains_shared_between_cursor_and_active_preview(self):
        source=(catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt').read_text()
        self.assertIn('tag="cursor_magnifier_enabled";text=ui(R.string.ui_show_magnified_drawing_preview)',source)
        self.assertIn('toggle(ui(R.string.ui_show_magnified_drawing_preview),paintCanvas.activeMagnifier,"magnifier_enabled")',source)
        self.assertEqual('Hiện bản xem trước phóng đại của bản vẽ',self.data['locales']['vi']['rows']['string/ui_show_magnified_drawing_preview']['target'])


if __name__=='__main__':unittest.main()
