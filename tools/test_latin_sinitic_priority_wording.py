"""Exact own-script reviewed-value and held/outside boundary regressions."""
import copy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as E
import latin_sinitic_priority_expectations as g
ROOT=Path(__file__).resolve().parents[1]
SOURCE_ROOT=ROOT
class LatinSiniticPriorityTests(unittest.TestCase):
    def root(self,tag):return E.parse(ROOT/g.bound_fixture(tag)['catalogue_path']).getroot()
    def test_exact_three_catalogues_and_full_source(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);self.assertEqual(341,len(d['priority_identities']));self.assertEqual(361,len(d['rows'])+len(d['held']));g.require_catalogue(tag,self.root(tag));g.require_source(tag,E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot())
    def test_exact_counts_and_holds(self):
        for tag,edits,holds in [('yue-Latn',14,11),('hak-Latn-TW',9,19),('nan-Latn-TW',15,11)]:
            d=g.bound_fixture(tag);self.assertEqual(edits,sum(r['decision']=='edited' for r in d['rows'].values()));self.assertEqual(holds,len(d['held']));self.assertEqual(717,len(d['original_catalogue']))
    def test_every_standalone_reviewed_row_and_coordinate_mutant(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag)
            for key,row in d['rows'].items():
                with self.subTest(tag=tag,key=key):
                    n=root.find("./*[@name='"+key+"']");g.require_reviewed_resource(tag,key,n,row)
                    bad=copy.deepcopy(row);bad['reviewed_value']='forged';bad['reviewed_display']='forged';n=copy.deepcopy(n);n.clear();n.tag='string';n.set('name',key);n.text='forged'
                    with self.assertRaises(ValueError):g.require_reviewed_resource(tag,key,n,bad)
    def test_supplied_fixture_cannot_coordinate_target_and_root(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag);key=next(iter(d['rows']));d['rows'][key]['reviewed_value']='forged';root.find("./*[@name='"+key+"']").text='forged'
            with self.assertRaises(ValueError):g.require_catalogue(tag,root,d)
    def test_mutating_returned_fixture_cannot_change_fresh_binding(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key=next(iter(d['rows']));d['rows'][key]['reviewed_value']='forged';self.assertNotEqual('forged',g.bound_fixture(tag)['rows'][key]['reviewed_value'])
    def test_every_held_and_outside_value_remains_exact(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);root=self.root(tag)
            for key in set(d['original_catalogue'])-set(d['rows']):
                with self.subTest(tag=tag,key=key):
                    n=root.find("./*[@name='"+key+"']");old=n.text;n.text='forged'
                    with self.assertRaises(ValueError):g.require_catalogue(tag,root)
                    n.text=old
    def test_wrong_parent_text_attributes_tail_and_identity_rejected(self):
        for tag in g.TAGS:
            root=self.root(tag)
            for mutation in [lambda r:setattr(r,'text','bad'),lambda r:setattr(r,'tail','bad'),lambda r:r.set('extra','bad'),lambda r:setattr(r,'tag','wrong'),lambda r:r.remove(r[0]),lambda r:r.append(copy.deepcopy(r[0]))]:
                r=copy.deepcopy(root);mutation(r)
                with self.assertRaises(ValueError):g.require_catalogue(tag,r)
    def test_cross_type_same_name_duplicate_rejected(self):
        for tag in g.TAGS:
            r=self.root(tag);n=E.Element('plurals',{'name':r[0].get('name')});r.append(n)
            with self.assertRaises(ValueError):g.require_catalogue(tag,r)
    def test_scalar_children_attributes_and_tail_rejected(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key=next(k for k,r in d['rows'].items() if r['type']=='string');n=self.root(tag).find("./string[@name='"+key+"']")
            for mutation in [lambda x:x.append(E.Element('b')),lambda x:x.set('formatted','false'),lambda x:setattr(x,'tail','bad'),lambda x:setattr(x,'text','')]:
                bad=copy.deepcopy(n);mutation(bad)
                with self.assertRaises(ValueError):g.require_reviewed_resource(tag,key,bad,d['rows'][key])
    def test_plural_shape_rejects_parent_item_tail_and_extra_forms(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key='ui_crop_preview_images';n=self.root(tag).find("./plurals[@name='"+key+"']")
            for mutation in [lambda x:setattr(x,'text','bad'),lambda x:setattr(x[0],'tail','bad'),lambda x:x[0].append(E.Element('b')),lambda x:x.append(copy.deepcopy(x[0])),lambda x:x[0].set('quantity','one'),lambda x:x[0].set('extra','bad')]:
                bad=copy.deepcopy(n);mutation(bad)
                with self.assertRaises(ValueError):g.require_reviewed_resource(tag,key,bad,d['rows'][key])
    def test_source_change_and_same_name_wrong_type_rejected(self):
        for tag in g.TAGS:
            d=g.bound_fixture(tag);key=next(iter(d['rows']));r=E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot();r.find("./*[@name='"+key+"']").text='changed'
            with self.assertRaises(ValueError):g.require_source(tag,r)
            r=E.parse(SOURCE_ROOT/'Paintroid/src/main/res/values/strings.xml').getroot();r.append(E.Element('plurals',{'name':key}))
            with self.assertRaises(ValueError):g.require_source(tag,r)
    def test_fixture_omitted_added_and_foreign_locale_rejected(self):
        for tag in g.TAGS:
            for mutation in [lambda d:d.pop('held'),lambda d:d.update(extra=True),lambda d:d['rows'].pop(next(iter(d['rows']))),lambda d:d.update(locale='wrong')]:
                d=g.bound_fixture(tag);mutation(d)
                with self.assertRaises(ValueError):g.require_fixture(tag,d)
        with self.assertRaises(ValueError):g.bound_fixture('yue-Hant')
    def test_prior_counterparts_do_not_lift_hakka_holds(self):
        d=g.bound_fixture('hak-Latn-TW')
        for key in ['ui_keeps_pixels_at_the_top_left_smaller_canvas','ui_drawing_canvas_pinch_and_move_two_fingers_to','formats22_pdf_raster_hint','ui_colour_palette_tap_for_foreground_hold_for_background','ui_tool_categories','ui_codec_resize_memory_floor','ui_sampled_resize_memory_explanation','save20_unsupported_image_colour']:
            self.assertIn(key,d['held']);self.assertNotIn(key,d['rows'])
    def test_save_aliases_are_exact_independent_complete_labels(self):
        for tag,expected in [('yue-Latn','Cyu5 cyun4…'),('hak-Latn-TW','Pó-sùn…'),('nan-Latn-TW','Pó-chûn…')]:
            d=g.bound_fixture(tag);self.assertEqual(expected,d['rows']['ui_save_a5d0d9']['reviewed_display']);self.assertNotEqual(d['rows']['ui_save']['reviewed_display'],expected)
    def test_compiled_projection_preserves_raw_wording_and_exact_three_differences(self):
        differences=[]
        for tag in g.TAGS:
            d=g.bound_fixture(tag)
            for key,row in d['rows'].items():
                if row['reviewed_display']!=row['compiled_display']:differences.append((tag,key))
        self.assertEqual([('nan-Latn-TW','ui_autosave_failed_use_save'),('nan-Latn-TW','ui_autosave_paused_use_save'),('nan-Latn-TW','ui_paste_hint34')],differences)
        for tag,key in differences:
            r=g.bound_fixture(tag)['rows'][key];self.assertEqual('retained',r['decision']);self.assertEqual(r['reviewed_display'].replace('"',''),r['compiled_display'])
            bad=copy.deepcopy(r);bad['compiled_display']='forged'
            with self.assertRaises(ValueError):g.require_row(tag,key,bad)
    def test_complete_jvm_consumer_source_and_mutations(self):
        text=(ROOT/g.JVM_PATH).read_text();g.require_jvm_source(text)
        self.assertEqual(16,text.count('@Test fun '))
        for before,after in [('requireRow(tag,key,supplied)','supplied'),('latinSiniticSameJson(latinSiniticBoundFixture(tag),supplied)','Unit'),('val quantity=if(values.has(selected)) selected else "other"','val quantity="other"'),('assertEquals(expected(tag,"ui_fg"),ui(R.string.ui_fg))','assertTrue(true)'),('"compiled_display"','"reviewed_display"')]:
            self.assertIn(before,text)
            with self.assertRaises(ValueError):g.require_jvm_source(text.replace(before,after,1))
    def test_main_successor_exact_three_complete_branches_and_negatives(self):
        text=(ROOT/g.MAIN_PATH).read_text();g.require_main_successor(text)
        for bad in [text.replace(g.SAVE_BRANCHES,''),text.replace(g.SAVE_BRANCHES,g.SAVE_BRANCHES*2),text.replace('Cyu5 cyun4…','forged')]:
            with self.assertRaises(ValueError):g.require_main_successor(bad)
if __name__=='__main__':unittest.main()
