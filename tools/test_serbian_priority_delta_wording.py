"""Exact accepted delta and mutation tests; retained context is not linguistic acceptance."""
from collections import Counter
from copy import deepcopy
import json,re,unittest,xml.etree.ElementTree as ET
from unittest.mock import patch
from current_localization_contracts import fixture,require_string, require_string_root
import serbian_priority_delta_expectations as current
import translation_catalogues as cat
TOKEN=re.compile(r'%(?:(?:\d+)\$)?[-#+ 0,(<]*(?:\d+)?(?:\.\d+)?(?:[tT][A-Za-z]|[bBhHsScCdoxXeEfgGaA%n])')
HOLDS={'formats22_derived_exported','ui_save_as','ui_save_as_jpeg','ui_save_as_jpeg_xl','ui_save_as_png','ui_foreground_background_colour_palette','ui_pinch_and_pan_mode'}
class SerbianPriorityDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=current.cohort()
        cls.xml={t:(cat.RES/('values' if t=='default' else 'values-b+'+t.replace('-','+'))/'strings.xml').read_text() for t in ['default','sr-Cyrl','sr-Latn']}
        cls.roots={t:ET.fromstring(v) for t,v in cls.xml.items()}
    def test_scope_separates_changed_values_context_holds_and_pending_retained_rows(self):
        tiers=json.loads((cat.DATA/'string-importance.json').read_text())['tiers']
        keys={k.split('/',1)[1] for tier in tiers if tier['id'] in ('P0','P1') for k in tier['keys']}
        self.assertEqual(341,len(keys));self.assertEqual(current.TAGS,set(self.data));self.assertTrue(current.TAGS<=set(cat.offered_tags()))
        for tag,d in self.data.items():
            self.assertEqual(keys,set(d['priority_status']));self.assertEqual(HOLDS,set(d['held_absent']));self.assertEqual(['ui_discard'],d['held_existing'])
            self.assertEqual(144 if tag=='sr-Cyrl' else 146,len(d['values']));self.assertEqual(4,len(d['dependencies']))
            self.assertEqual(118 if tag=='sr-Cyrl' else 117,Counter(d['priority_status'].values())['retain_pending_prior_binding'])
            self.assertEqual(75 if tag=='sr-Cyrl' else 74,sum(s.startswith('prior_exact_P0_carry') for s in d['priority_status'].values()))
            for key in HOLDS:self.assertIsNone(self.roots[tag].find(f"./string[@name='{key}']"))
            for row in d['context'].values():self.assertFalse(row['changed']);self.assertNotEqual('accepted_delta',row['review_status'])
    def test_complete_targets_and_source_attributes_slots_newlines(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                with self.subTest(tag=tag,key=key):
                    s=self.roots['default'].find(f"./string[@name='{key}']")
                    self.assertEqual((s.text,s.attrib),(row['source'],row['attributes']))
                    require_string_root(self.roots[tag],key,row['target'],{'attributes':row['attributes'],'child_elements':0})
                    self.assertEqual(Counter(TOKEN.findall(row['source'])),Counter(TOKEN.findall(row['target'])))
                    for newline in ('\n','\\n'):self.assertEqual(row['source'].count(newline),row['target'].count(newline))
                    self.assertTrue(row['changed']);self.assertNotEqual(row['previous'],row['target'])
    def test_missing_duplicate_truncated_markup_attributes_type_and_slot_corruption_fail(self):
        for tag,d in self.data.items():
            for key,row in d['values'].items():
                for mode in ['missing','duplicate','truncated','markup','attribute','type','argument']:
                    root=ET.Element('resources');n=ET.SubElement(root,'string',row['attributes']);n.text=row['target']
                    if mode=='missing':root.remove(n)
                    elif mode=='duplicate':root.append(deepcopy(n))
                    elif mode=='truncated':n.text=n.text[:-2]
                    elif mode=='markup':ET.SubElement(n,'b').text,n.text=n.text,None
                    elif mode=='attribute':n.set('translatable','false')
                    elif mode=='type':n.tag='plurals'
                    else:n.text+=' %9$s'
                    with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):require_string(ET.tostring(root,encoding='unicode'),key,row['target'],{'attributes':row['attributes'],'child_elements':0})
    def test_finite_forward_binding_rejects_forged_previous_source_and_attributes(self):
        for tag,d in self.data.items():
            for key,r in d['values'].items():
                self.assertEqual(r['target'],current.current_value(tag,key,r['previous'],r['attributes'],r['source']))
                for old,attrs,source in [('forged',r['attributes'],r['source']),(r['previous'],{'name':key,'formatted':'forged'},r['source']),(r['previous'],r['attributes'],r['source']+' forged')]:
                    with self.subTest(tag=tag,key=key),self.assertRaises(ValueError):current.current_value(tag,key,old,attrs,source)
            self.assertIsNone(current.current_value('unbound','ui_no_resize_fits_decoder_memory',None,{},''))
    def test_independently_revised_svg_and_demonstrated_action_defects(self):
        exact={'sr-Cyrl':{'ui_crop_image':'Исеци слику','ui_rectangle_select':'Правоугаони избор','ui_keep_editing23':'Настави уређивање','commons_svg_original_size_too_large':'Изворне димензије SVG-а премашују ограничења система Android за димензије битмапе. Величина није промењена.'},'sr-Latn':{'ui_crop_image':'Iseci sliku','ui_rectangle_select':'Pravougaoni izbor','ui_keep_editing23':'Nastavi uređivanje'}}
        for tag,rows in exact.items():
            for key,text in rows.items():self.assertEqual(text,current.row(tag,key)['display'])
    def test_paste_hint_and_dirty_confirmation_keep_distinct_actual_labels(self):
        for tag in current.TAGS:
            v=lambda k:current.row(tag,k)['display']
            for key in ['ui_draw26','ui_category_insert','ui_other_images34']:self.assertIn(v(key),v('ui_paste_hint34'))
            self.assertEqual(3,len({v('ui_save'),v('ui_discard_changes23'),v('ui_keep_editing23')}))
    def test_dependencies_are_exact_absent_to_target_additions(self):
        for tag,d in self.data.items():
            self.assertEqual({'ui_width_in','ui_trim_in_pixels','ui_trim_in_percent','formats22_at_least_frames'},set(d['dependencies']))
            for key in d['dependencies']:
                r=d['values'][key];self.assertIsNone(r['previous']);self.assertEqual(r['target'],current.addition(tag,key,r['source'],None))
                with self.assertRaises(ValueError):current.addition(tag,key,r['source'],'forged')
    def test_retained_top_P2_context_is_complete_exact_and_not_an_accepted_change(self):
        for tag,label in [('sr-Cyrl','Горе'),('sr-Latn','Gore')]:
            key='ui_top';row=current.row(tag,key)
            self.assertEqual({'source':'Top','attributes':{'name':key},'previous':'"'+label+'"','target':'"'+label+'"','display':label,'changed':False,'review_status':'retained_P2_consumer_context'},row)
            self.assertNotIn(key,self.data[tag]['values']);self.assertNotIn(key,self.data[tag]['priority_status'])
            self.assertEqual(('Top',{'name':key}),(self.roots['default'].find(f"./string[@name='{key}']").text,self.roots['default'].find(f"./string[@name='{key}']").attrib))
            require_string_root(self.roots[tag],key,row['target'],{'attributes':row['attributes'],'child_elements':0})
            for field in ('source','previous','target','display','review_status'):
                bad=current.reviewed_fixture();bad['locales'][tag]['context'][key][field]='forged'
                with self.subTest(tag=tag,field=field),self.assertRaises(ValueError):current.require_reviewed_fixture(bad)
            bad=current.reviewed_fixture();del bad['locales'][tag]['context'][key]['previous']
            with self.assertRaises(ValueError):current.require_reviewed_fixture(bad)
            for mode in ('missing','duplicate','text','attributes'):
                root=ET.fromstring(self.xml[tag]);node=root.find(f"./string[@name='{key}']")
                if mode=='missing':root.remove(node)
                elif mode=='duplicate':root.append(deepcopy(node))
                elif mode=='text':node.text='forged'
                else:node.set('formatted','false')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):require_string(ET.tostring(root,encoding='unicode'),key,row['target'],{'attributes':row['attributes'],'child_elements':0})
    def test_coordinated_target_display_and_xml_cannot_replace_any_accepted_row(self):
        for tag,locale in self.data.items():
            for key,row in locale['values'].items():
                bad=current.reviewed_fixture();changed=bad['locales'][tag]['values'][key]
                changed['target']+=' forged';changed['display']+=' forged'
                root=ET.fromstring(self.xml[tag]);root.find(f"./string[@name='{key}']").text=changed['target']
                # The altered resource matches the altered fixture, so its own full-text
                # comparison passes. The separately bound finite fixture must reject it.
                require_string(ET.tostring(root,encoding='unicode'),key,changed['target'],{'attributes':changed['attributes'],'child_elements':0})
                with self.subTest(tag=tag,key=key),patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):
                    current.current_value(tag,key,row['previous'],row['attributes'],row['source'])
    def test_bound_fixture_rejects_metadata_previous_attributes_and_context_mutations(self):
        for tag in current.TAGS:
            for mutation in ('previous','missing-previous','attributes','source','review-status','held','scope','context','display-only'):
                bad=current.reviewed_fixture();loc=bad['locales'][tag];row=loc['values']['ui_choose_location']
                if mutation=='previous':row['previous']='forged'
                elif mutation=='missing-previous':del row['previous']
                elif mutation=='attributes':row['attributes']['name']='wrong'
                elif mutation=='source':row['source']='forged'
                elif mutation=='review-status':row['review_status']='retained'
                elif mutation=='held':loc['held_absent'].remove('ui_save_as_png')
                elif mutation=='scope':bad['scope']='full language certified'
                elif mutation=='context':loc['context']['ui_save']['display']='forged'
                else:row['display']='forged'
                with self.subTest(tag=tag,mutation=mutation),self.assertRaises(ValueError):current.require_reviewed_fixture(bad)
                with patch.object(current,'fixture',return_value=bad),self.assertRaises(ValueError):current.addition(tag,'ui_choose_location','Choose location…',None)
        raw=(cat.ROOT/'tools/fixtures/current_localization'/current.FIXTURE).read_bytes().decode('utf-8')
        self.assertEqual(current.reviewed_fixture(),current.validated_fixture_text(raw))
        for corrupted in (raw+' ',raw.replace('accepted_delta','forged',1)):
            with self.assertRaises(ValueError):current.validated_fixture_text(corrupted)
        first=current.cohort();first['sr-Cyrl']['values']['ui_keep_editing23']['target']='forged'
        self.assertNotEqual(first,current.cohort())
        reviewed=current.reviewed_fixture();reviewed['scope']='forged'
        self.assertNotEqual(reviewed,current.reviewed_fixture())
if __name__=='__main__':unittest.main()
