"""Bounded Portugal Portuguese/Spain Spanish contracts, not full-language certification."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

import translation_catalogues as catalogues
from current_localization_contracts import fixture, require_string

FIXTURE='portuguese_spanish_priority_wording.json'
EXPECTED={
    'pt-PT': {'save20_destination_error','ui_d_d_px_d_pixels_2f_mp',
              'ui_d_d_pixels_2f_mp_exceeds_the_current','ui_trim_in_pixels','ui_trim_in_percent',
              'ui_draw_again','ui_solid_fill','ui_cut','ui_canvas_size','ui_canvas_size_30460e'},
    'es-ES': {'save20_destination_error','ui_export_explanation23',
              'ui_higher_quality_usually_makes_a_larger_file_lossless','ui_percent',
              'ui_the_image_was_saved_but_android_could_not','ui_d_d_px_d_pixels_2f_mp',
              'ui_d_d_pixels_2f_mp_exceeds_the_current','ui_trim_in_pixels','ui_trim_in_percent','ui_draw_again'},
}
CLASSIC=catalogues.ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic'


def checked(data):
    if set(data['locales']) != set(EXPECTED):
        raise ValueError('Unexpected locale scope')
    for tag, keys in EXPECTED.items():
        rows=data['locales'][tag]['values']
        if set(rows) != keys: raise ValueError('Unexpected exact edit scope')
        for key,row in rows.items():
            if not all(isinstance(row.get(k),str) and row[k] for k in ('source','target','display','previous_target')):
                raise ValueError('Incomplete full-value binding')
            if row['target']==row['previous_target']: raise ValueError('Successor must change exact value')
            if row['attributes'] != row['previous_attributes'] or row['attributes'].get('name') != key:
                raise ValueError('Attributes or typed identity changed')
    return data['locales']


def constraints(value,attributes):
    return {'attributes':attributes,'formatted':attributes.get('formatted')!='false',
            'placeholders':catalogues.placeholders(value),'escaped_newline_count':value.count(r'\n')}


class PortugueseSpanishPriorityWordingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=fixture(FIXTURE);cls.locales=checked(cls.data)
        cls.xml={tag:catalogues.catalogue_paths()[tag].read_text() for tag in EXPECTED}
        cls.english=(catalogues.RES/'values/strings.xml').read_text()

    def test_full_values_bind_english_current_attributes_unicode_and_typed_arguments(self):
        for tag,data in self.locales.items():
            for key,row in data['values'].items():
                with self.subTest(tag=tag,key=key):
                    require_string(self.xml[tag],key,row['target'],constraints(row['target'],row['attributes']))
                    self.assertEqual(row['source'],ET.fromstring(self.english).find(f"./string[@name='{key}']").text)
                    self.assertEqual(catalogues.placeholders(row['source']),catalogues.placeholders(row['target']))
                    self.assertEqual([],catalogues.android_string_errors(row['target']))
                    self.assertEqual([],catalogues.format_string_errors(row['target'],row['attributes'].get('formatted')!='false'))

    def test_missing_duplicate_truncated_old_wrong_attribute_and_argument_mutations_fail(self):
        for tag,data in self.locales.items():
            for key,row in data['values'].items():
                for mutation in ('missing','duplicate','truncate','old','attribute','argument','markup'):
                    root=ET.fromstring(self.xml[tag]);node=root.find(f"./string[@name='{key}']")
                    if mutation=='missing':root.remove(node)
                    elif mutation=='duplicate':root.append(deepcopy(node))
                    elif mutation=='truncate':node.text=node.text[:-1]
                    elif mutation=='old':node.text=row['previous_target']
                    elif mutation=='attribute':node.set('formatted','false' if node.get('formatted')!='false' else 'true')
                    elif mutation=='argument':node.text+=' %9$d'
                    else:ET.SubElement(node,'b').text,node.text=node.text,None
                    with self.subTest(tag=tag,key=key,mutation=mutation),self.assertRaises(ValueError):
                        require_string(ET.tostring(root,encoding='unicode'),key,row['target'],constraints(row['target'],row['attributes']))

    def test_exact_fixture_scope_and_predecessor_require_full_values(self):
        for mutation in ('locale','extra-key','wrong-locale','key','empty','unchanged','attributes'):
            data=deepcopy(self.data)
            if mutation=='locale':del data['locales']['pt-PT']
            elif mutation=='extra-key':data['locales']['es-ES']['values']['unreviewed_extra']=deepcopy(data['locales']['es-ES']['values']['save20_destination_error'])
            elif mutation=='wrong-locale':data['locales']['es-419']=data['locales'].pop('es-ES')
            else:
                rows=data['locales']['es-ES']['values'];key='save20_destination_error';row=rows[key]
                if mutation=='key':del rows[key]
                elif mutation=='empty':row['source']=''
                elif mutation=='unchanged':row['target']=row['previous_target']
                else:row['attributes']['formatted']='false'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):checked(data)

    def test_catalogues_and_all_priority_identities_remain_present(self):
        manifest=json.loads((catalogues.ROOT/'translations/string-importance.json').read_text())
        priorities={key for tier in manifest['tiers'] if tier['id'] in ('P0','P1') for key in tier['keys']}
        self.assertEqual(341,len(priorities))
        for tag,xml in self.xml.items():
            self.assertEqual([],catalogues.validate_catalogue(tag,require_complete=True))
            typed=[node.tag+'/'+node.get('name') for node in ET.fromstring(xml)]
            self.assertEqual(len(typed),len(set(typed)))
            self.assertTrue(priorities <= set(typed))

    def test_count_label_handles_one_without_plural_agreement_and_keeps_actual_consumer(self):
        expected={'pt-PT':'%1$d × %2$d px · Contagem de píxeis: %3$,d (%4$.2f MP)',
                  'es-ES':'%1$d × %2$d px · Número de píxeles: %3$,d (%4$.2f MP)'}
        for tag,value in expected.items():self.assertEqual(value,self.locales[tag]['values']['ui_d_d_px_d_pixels_2f_mp']['target'])
        source=(CLASSIC/'ImageImport.kt').read_text()
        self.assertIn('val pixels: Long get() = width.toLong() * height',source)
        self.assertIn('ui(R.string.ui_d_d_px_d_pixels_2f_mp, width, height, pixels, pixels / 1_000_000.0)',source)
        self.assertIn('result.text = target?.describe()', (CLASSIC/'DimensionControls.kt').read_text())

    def test_destination_error_keeps_atomic_replacement_consumers(self):
        for filename in ('BitmapFileCodec.kt','DibCodec.kt','IcoCodec.kt','TextImageCodec.kt'):
            source=(CLASSIC/filename).read_text()
            with self.subTest(consumer=filename):
                self.assertRegex(source,r'if \(!temporary.renameTo\((?:file|destination)\)\) throw IOException\(ui\(R.string.save20_destination_error\)\)')
                self.assertRegex(source,r'finally\s*\{[^}]*temporary\.delete\(\)')

    def test_export_and_sharing_keep_state_distinctions_and_real_dialog_consumers(self):
        source=(CLASSIC/'SaveOptionsDialog.kt').read_text()
        self.assertIn('export->R.string.ui_export_explanation23',source)
        self.assertIn('else -> R.string.ui_higher_quality_usually_makes_a_larger_file_lossless',source)
        activity=(CLASSIC/'ClassicPaintActivity.kt').read_text()
        self.assertIn('if(!exporting) {filename=name;savedTarget=SavedTarget(uri,name,options);document.markSaved();scheduleAutosave()}',activity)
        self.assertIn('if(sharing) shareSavedImage(file,options.format)',activity)
        self.assertIn('message(ui(R.string.ui_the_image_was_saved_but_android_could_not, error.message))',activity)
        self.assertIn('ui(R.string.ui_percent)',(CLASSIC/'DimensionControls.kt').read_text())

    def test_crop_templates_and_canvas_commands_keep_atomic_labels_and_consumers(self):
        spanish=self.locales['es-ES']['values']
        self.assertEqual('%1$s: recorte en píxeles',spanish['ui_trim_in_pixels']['target'])
        self.assertEqual('%1$s: recorte en porcentaje',spanish['ui_trim_in_percent']['target'])
        self.assertEqual('Volver a dibujar',spanish['ui_draw_again']['target'])
        rows=self.locales['pt-PT']['values']
        self.assertEqual('%1$s: recorte em píxeis',rows['ui_trim_in_pixels']['target'])
        self.assertEqual('%1$s: recorte em percentagem',rows['ui_trim_in_percent']['target'])
        self.assertEqual('Tamanho da tela…',rows['ui_canvas_size']['target'])
        self.assertEqual('Tamanho da tela',rows['ui_canvas_size_30460e']['target'])
        source=(CLASSIC/'ImageCropDialog.kt').read_text()
        self.assertIn('ui(if(percent) R.string.ui_trim_in_percent else R.string.ui_trim_in_pixels,ui(edges.getValue(key)))',source)
        self.assertIn('contentDescription = ui(R.string.ui_trim_in_pixels, name)',source)
        activity=(CLASSIC/'ClassicPaintActivity.kt').read_text()
        self.assertIn('button(ui(R.string.ui_draw_again), "navigate_draw") { chooseTool(drawingTool) }',activity)
        self.assertIn('listOf(ui(R.string.ui_outline), ui(R.string.ui_solid_fill), ui(R.string.ui_fill_line))',activity)
        self.assertIn('command(ui(R.string.ui_canvas_size),R.drawable.classic_canvas_size) {dimensionsDialog(false,false)}',activity)
        self.assertIn('else ui(R.string.ui_canvas_size_30460e)',activity)

    def test_zero_budget_warning_uses_singular_image_subject_and_retains_every_safeguard(self):
        spanish=self.locales['es-ES']['values']['ui_d_d_pixels_2f_mp_exceeds_the_current']
        self.assertEqual(spanish['previous_target'].replace('píxeles','px'),spanish['target'])
        self.assertTrue(spanish['target'].startswith('Una imagen de %1$d × %2$d px (%3$.2f MP) supera '))
        value=self.locales['pt-PT']['values']['ui_d_d_pixels_2f_mp_exceeds_the_current']['target']
        self.assertTrue(value.startswith('Uma imagem de %1$d × %2$d px (%3$.2f MP) excede '))
        for clause in ('reserva espaço para transformações e seleções','A memória disponível determina este limite.',
                       'antes de alocar o bitmap demasiado grande.','Não foi aplicado qualquer redimensionamento automático.'):
            self.assertIn(clause,value)
        source=(CLASSIC/'ImageMemoryPolicy.kt').read_text()
        self.assertIn('(workingBytes - residentBytes).coerceAtLeast(0) / 12',source)
        self.assertIn('if (pixels > permitted) throw ImageSizeException(ui(R.string.ui_d_d_pixels_2f_mp_exceeds_the_current,',source)


if __name__=='__main__':unittest.main()
