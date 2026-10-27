"""Exact bounded successors and real caller contracts; not full-language certification."""
from copy import deepcopy
import json
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues
from current_localization_contracts import fixture, require_string

FIXTURE = 'italian_greek_turkish_priority_wording.json'
EXPECTED = {
    'it': {'string/'+k for k in ('ui_all','ui_none','ui_canvas_size_30460e','ui_draw_again','ui_solid_fill','ui_trim_in_pixels','ui_trim_in_percent')},
    'el': {'string/'+k for k in ('save20_destination_error','save20_gif_description','save20_dither','ui_d_d_pixels_2f_mp_exceeds_the_current','ui_all','ui_none','ui_draw_again','ui_trim_in_pixels','ui_trim_in_percent')} | {'plurals/ui_crop_preview_images'},
    'tr': {'string/'+k for k in ('save20_destination_error','ui_draw_again','ui_solid_fill')} | {'plurals/ui_crop_preview_images'},
}
CLASSIC = catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'


def checked(data):
    if data.get('schema_version') != 1 or set(data['locales']) != set(EXPECTED):
        raise ValueError('Unexpected locale scope')
    for tag, keys in EXPECTED.items():
        rows=data['locales'][tag]['values']
        if set(rows) != keys: raise ValueError('Unexpected exact typed scope')
        for identity,row in rows.items():
            kind,key=identity.split('/')
            for field in ('source','target','display','previous_target'):
                value=row.get(field)
                if kind=='string':
                    if not isinstance(value,str) or not value: raise ValueError('Incomplete full string')
                elif not isinstance(value,dict) or set(value)!={'one','other'} or not all(isinstance(v,str) and v for v in value.values()):
                    raise ValueError('Incomplete full plural')
            if row['target']==row['previous_target']: raise ValueError('Successor must change exact value')
            if row['attributes']!=row['previous_attributes'] or row['attributes']!={'name':key}:
                raise ValueError('Attribute binding changed')
    return data['locales']


def require_entry(xml,identity,row,field='target'):
    kind,key=identity.split('/'); expected=row[field]
    if kind=='string':
        return require_string(xml,key,expected,{'attributes':row['attributes'],'formatted':True,
            'placeholders':catalogues.placeholders(row['source']),'escaped_newline_count':expected.count(r'\n')})
    nodes=ET.fromstring(xml).findall(f"./plurals[@name='{key}']")
    if len(nodes)!=1:raise ValueError('Missing or duplicate full plural')
    node=nodes[0]
    if node.attrib!=row['attributes'] or len(node)!=len(expected):raise ValueError('Plural shape differs')
    quantities=[child.get('quantity') for child in node]
    if len(set(quantities))!=len(quantities) or set(quantities)!=set(expected):raise ValueError('Plural quantities differ')
    for child in node:
        quantity=child.get('quantity');value=child.text or ''
        if child.tag!='item' or child.attrib!={'quantity':quantity} or len(child) or value!=expected[quantity]:
            raise ValueError('Complete plural child differs')
        if catalogues.placeholders(value)!=catalogues.placeholders(row['source'][quantity]) or value.count(r'\n')!=1:
            raise ValueError('Plural arguments/newline differ')
        if catalogues.android_string_errors(value) or catalogues.format_string_errors(value,True):raise ValueError('Plural format invalid')
    return expected


class ItalianGreekTurkishPriorityWordingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=fixture(FIXTURE);cls.locales=checked(cls.data)
        cls.xml={tag:catalogues.catalogue_paths()[tag].read_text() for tag in EXPECTED}
        cls.english=(catalogues.RES/'values/strings.xml').read_text()

    def test_complete_typed_values_bind_current_english_attributes_and_arguments(self):
        for tag,locale in self.locales.items():
            for identity,row in locale['values'].items():
                with self.subTest(tag=tag,identity=identity):
                    require_entry(self.xml[tag],identity,row)
                    require_entry(self.english,identity,row,'source')

    def test_each_scalar_and_every_plural_child_rejects_old_truncated_arguments_and_markup(self):
        for tag,locale in self.locales.items():
            for identity,row in locale['values'].items():
                kind,key=identity.split('/')
                for quantity in (list(row['target']) if kind=='plurals' else [None]):
                    for mutation in ('old','truncate','argument','markup','attribute'):
                        root=ET.fromstring(self.xml[tag]);node=root.find(f"./{kind}[@name='{key}']")
                        child=node if quantity is None else node.find(f"./item[@quantity='{quantity}']")
                        if mutation=='old':child.text=row['previous_target'] if quantity is None else row['previous_target'][quantity]
                        elif mutation=='truncate':child.text=child.text[:-1]
                        elif mutation=='argument':child.text+=' %9$d'
                        elif mutation=='attribute':child.set('formatted','false')
                        else:ET.SubElement(child,'b').text,child.text=child.text,None
                        with self.subTest(tag=tag,identity=identity,quantity=quantity,mutation=mutation),self.assertRaises(ValueError):
                            require_entry(ET.tostring(root,encoding='unicode'),identity,row)

    def test_missing_duplicate_wrong_type_and_plural_quantity_mutations_fail(self):
        for tag,locale in self.locales.items():
            for identity,row in locale['values'].items():
                kind,key=identity.split('/')
                mutations=['missing','duplicate','wrong-type']+(['missing-child','duplicate-child','wrong-quantity','extra-child','parent-attribute'] if kind=='plurals' else [])
                for mutation in mutations:
                    root=ET.fromstring(self.xml[tag]);node=root.find(f"./{kind}[@name='{key}']")
                    if mutation=='missing':root.remove(node)
                    elif mutation=='duplicate':root.append(deepcopy(node))
                    elif mutation=='wrong-type':node.tag='plurals' if kind=='string' else 'string'
                    elif mutation=='missing-child':node.remove(node[0])
                    elif mutation=='duplicate-child':node[1].set('quantity',node[0].get('quantity'))
                    elif mutation=='wrong-quantity':node[0].set('quantity','few')
                    elif mutation=='parent-attribute':node.set('formatted','false')
                    else:ET.SubElement(node,'item',quantity='few').text=node[0].text
                    with self.subTest(tag=tag,identity=identity,mutation=mutation),self.assertRaises(ValueError):
                        require_entry(ET.tostring(root,encoding='unicode'),identity,row)

    def test_fixture_requires_exact_locales_keys_complete_predecessors_and_plural_maps(self):
        for mutation in ('locale','wrong-locale','missing','extra','empty','unchanged','attributes','plural-child'):
            data=deepcopy(self.data);values=data['locales']['el']['values'];row=values['string/save20_destination_error']
            if mutation=='locale':del data['locales']['it']
            elif mutation=='wrong-locale':data['locales']['el-CY']=data['locales'].pop('el')
            elif mutation=='missing':values.pop('string/save20_destination_error')
            elif mutation=='extra':values['string/unreviewed_extra']=deepcopy(row)
            elif mutation=='empty':row['source']=''
            elif mutation=='unchanged':row['target']=row['previous_target']
            elif mutation=='attributes':row['attributes']['formatted']='false'
            else:values['plurals/ui_crop_preview_images']['target'].pop('other')
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):checked(data)

    def test_all_catalogues_and_341_priority_identities_remain_structurally_present(self):
        manifest=json.loads((catalogues.ROOT/'translations/string-importance.json').read_text())
        priorities={key for tier in manifest['tiers'] if tier['id'] in ('P0','P1') for key in tier['keys']}
        self.assertEqual(341,len(priorities))
        for tag,xml in self.xml.items():
            self.assertEqual([],catalogues.validate_catalogue(tag,require_complete=True))
            typed=[node.tag+'/'+node.get('name') for node in ET.fromstring(xml)]
            self.assertEqual(len(typed),len(set(typed)));self.assertTrue(priorities<=set(typed))

    def test_destination_names_atomic_replacement_not_destination_selection(self):
        for name in ('BitmapFileCodec.kt','DibCodec.kt','IcoCodec.kt','TextImageCodec.kt'):
            source=(CLASSIC/name).read_text()
            self.assertRegex(source,r'if \(!temporary.renameTo\((?:file|destination)\)\) throw IOException\(ui\(R.string.save20_destination_error\)\)')
            self.assertRegex(source,r'finally\s*\{[^}]*temporary\.delete\(\)')

    def test_greek_zero_budget_warning_retains_every_later_clause(self):
        row=self.locales['el']['values']['string/ui_d_d_pixels_2f_mp_exceeds_the_current']
        old='%1$d × %2$d pixel (%3$.2f MP) υπερβαίνουν'
        new='Μια εικόνα %1$d × %2$d px (%3$.2f MP) υπερβαίνει'
        self.assertEqual(1,row['previous_target'].count(old))
        self.assertEqual(row['previous_target'].replace(old,new),row['target'])
        source=(CLASSIC/'ImageMemoryPolicy.kt').read_text()
        self.assertIn('(workingBytes - residentBytes).coerceAtLeast(0) / 12',source)
        self.assertIn('if (pixels > permitted) throw ImageSizeException(ui(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,',source)

    def test_joint_gif_description_checkbox_and_encoder_keep_same_dither_operation(self):
        rows=self.locales['el']['values']
        self.assertEqual('Πρόσμειξη χρωμάτων',rows['string/save20_dither']['target'])
        row=rows['string/save20_gif_description']
        self.assertEqual(row['previous_target'].replace('Η διασπορά','Η πρόσμειξη'),row['target'])
        source=(CLASSIC/'SaveOptionsDialog.kt').read_text()
        for exact in ('text=ui(R.string.save20_dither)','isChecked=initial.dither','ImageFormat.GIF -> R.string.save20_gif_description','ExportOptions(format,quality,format.supportsLossless && lossless,ditherBox.isChecked'):
            self.assertIn(exact,source)
        codec=(CLASSIC/'BitmapFileCodec.kt').read_text()
        self.assertIn('LegacyImageEncoder.gif(image.width, image.height, rows, output, budget, dither)',codec)
        self.assertIn('BitmapFileCodec.encode(image,file,options.format==ImageFormat.GIF,options.dither,budget)',(CLASSIC/'ImageExporter.kt').read_text())

    def test_crop_selection_labels_plural_children_and_navigation_have_real_consumers(self):
        crop=(CLASSIC/'ImageCropDialog.kt').read_text()
        for exact in ('listOf(ui(R.string.ui_all) to true,ui(R.string.ui_none) to false)',
            'uiQuantity(activity.resources,R.plurals.ui_crop_preview_images,count,crop.width(),crop.height(),count)',
            'ui(if(percent) R.string.ui_trim_in_percent else R.string.ui_trim_in_pixels,ui(edges.getValue(key)))'):
            self.assertIn(exact,crop)
        for tag,phrase in [('el','μπορεί να μετακινήσει'),('tr','yerini değiştirebilir')]:
            row=self.locales[tag]['values']['plurals/ui_crop_preview_images']
            for value in row['target'].values():self.assertIn(phrase,value)
        activity=(CLASSIC/'ClassicPaintActivity.kt').read_text()
        self.assertIn('button(ui(R.string.ui_draw_again), "navigate_draw") { chooseTool(drawingTool) }',activity)
        self.assertIn('listOf(ui(R.string.ui_outline), ui(R.string.ui_solid_fill), ui(R.string.ui_fill_line))',activity)
        self.assertIn('else ui(R.string.ui_canvas_size_30460e)',activity)


if __name__=='__main__':unittest.main()
