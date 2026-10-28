"""Negative probes for all fifteen finite memory/SVG/tagged family additions."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import somali_wolof_haitian_creole_priority_expectations as additions
import memory_warning_source_review as memory
import test_current_localization_contracts as families

class SomaliWolofHaitianCreoleFamilyAdditions(unittest.TestCase):
    def test_all_fifteen_exact_rows_reject_every_bound_field_mutation(self):
        pairs=additions.MEMORY_ADDITIONS|additions.SVG_ADDITIONS|{(t,'save20_unsupported_image_colour')for t in additions.TAGS}
        self.assertEqual(15,len(pairs))
        for tag,key in pairs:
            row=additions.current_row(tag,key)
            self.assertEqual(row['target'],additions.require_addition(tag,key,row['source']))
            for mode in ('historical','already-present','previous','previous-attributes','missing-previous','source','source-attributes','target-attributes','type','changed','empty','alias','different-target'):
                bad=deepcopy(row);args={}
                if mode=='historical':args['historical_value']='forged'
                elif mode=='already-present':args['already_present']=True
                elif mode=='previous':bad['previous_target']='forged'
                elif mode=='previous-attributes':bad['previous_attributes']={'name':key}
                elif mode=='missing-previous':bad.pop('previous_target')
                elif mode=='source':bad['source']='forged'
                elif mode=='source-attributes':bad['source_attributes']['formatted']='false'
                elif mode=='target-attributes':bad['attributes']['translatable']='false'
                elif mode=='type':bad['type']='plurals'
                elif mode=='changed':bad['changed']=False
                elif mode=='empty':bad['target']=''
                elif mode=='alias':bad['target']='@string/ui_save'
                else:bad['target']+='forged'
                with self.subTest(tag=tag,key=key,mode=mode),patch.object(additions,'current_row',return_value=bad),self.assertRaises(ValueError):
                    additions.require_addition(tag,key,row['source'],**args)
        for tag,key in [('unknown','ui_assembly_source_memory_floor'),('so','ui_save')]:
            with self.assertRaises(ValueError):additions.require_addition(tag,key,'forged')

    def test_central_fixture_binding_rejects_changed_maps_and_missing_null_history(self):
        original=additions.fixture(additions.NAME)
        for tag in additions.TAGS:
            for mode in ('target','source','missing-null','non-null','prior-attrs'):
                data=deepcopy(original);key='save20_unsupported_image_colour';locale=data['locales'][tag]
                if mode=='target':locale['accepted'][key]+='forged'
                elif mode=='source':data['sources'][key]['source']='forged'
                elif mode=='missing-null':locale['previous_targets'].pop(key)
                elif mode=='non-null':locale['previous_targets'][key]='forged'
                else:locale['predecessors'][key]={'attributes':{'name':key}}
                with self.subTest(tag=tag,mode=mode),patch.object(additions,'fixture',return_value=data),self.assertRaises(ValueError):additions.current_row(tag,key)

    def test_memory_adapters_reject_old_queue_source_and_current_row_mutations(self):
        for tag,key in additions.MEMORY_ADDITIONS:
            row=additions.current_row(tag,key)
            self.assertEqual(row['target'],memory.current_source_expectation(key,tag,None))
            for mode in ('old','source'):
                data=memory.review_record()
                if mode=='old':next(o for o in data['options']if o['tag']==tag)['terms'][key]['value']='forged'
                else:data['keys'][key]['corrected_english']='forged'
                with self.subTest(tag=tag,key=key,mode=mode),patch.object(memory,'review_record',return_value=data),self.assertRaises(ValueError):memory.current_source_expectation(key,tag,None)
            bad=deepcopy(row);bad['type']='plurals'
            with patch.object(memory,'so_wo_ht_row',return_value=bad),self.assertRaises(ValueError):memory.current_source_expectation(key,tag,None)

    def test_svg_adapter_rejects_old_presence_source_and_current_target_drift(self):
        original=families.fixture
        for tag,key in additions.SVG_ADDITIONS:
            for mode in ('present','source'):
                def changed(name):
                    data=original(name)
                    if name==families.FAMILIES[2]:
                        if mode=='present':data['values'][key][tag]='forged'
                        else:data['values'][key]['default']='forged'
                    return data
                with self.subTest(tag=tag,key=key,mode=mode),patch.object(families,'fixture',side_effect=changed),self.assertRaises(ValueError):families.wording_fixture(families.FAMILIES[2])
            def badrow(actual_tag,actual_key):
                row=additions.current_row(actual_tag,actual_key)
                if (actual_tag,actual_key)==(tag,key):row['target']+='forged'
                return row
            with patch.object(families,'so_wo_ht_row',side_effect=badrow),self.assertRaises(ValueError):families.wording_fixture(families.FAMILIES[2])

    def test_tagged_adapter_rejects_type_previous_attributes_and_same_row_target_drift(self):
        for tag in additions.TAGS:
            for mode in ('type','previous-attributes','target'):
                def badrow(actual_tag,key):
                    row=additions.current_row(actual_tag,key)
                    if actual_tag==tag:
                        if mode=='type':row['type']='plurals'
                        elif mode=='previous-attributes':row['previous_attributes']={'name':key}
                        else:row['target']+='forged'
                    return row
                with self.subTest(tag=tag,mode=mode),patch.object(families,'so_wo_ht_row',side_effect=badrow),self.assertRaises(ValueError):families.current_tagged_colour_data()

    def test_tagged_projection_rejects_forged_display_and_uses_the_bound_row(self):
        for tag in additions.TAGS:
            row=additions.current_row(tag,'save20_unsupported_image_colour')
            self.assertEqual(additions.display_row(row),families.current_tagged_colour_data()[tag])
            data=families.current_tagged_colour_data();data[tag]+='forged'
            with self.subTest(tag=tag),self.assertRaises(ValueError):families.tagged_colour_expectations(data)

if __name__=='__main__':unittest.main()
