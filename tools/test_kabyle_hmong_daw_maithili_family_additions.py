"""Finite family successor guards; frozen old fixtures remain unchanged."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import kabyle_hmong_daw_maithili_priority_expectations as additions
import memory_warning_source_review as memory
import test_current_localization_contracts as families

class KabyleHmongDawMaithiliFamilyAdditions(unittest.TestCase):
    def test_fifteen_exact_additions_reject_each_bound_field_mutation(self):
        pairs=additions.MEMORY_ADDITIONS|additions.SVG_ADDITIONS|{(t,'save20_unsupported_image_colour')for t in additions.TAGS}
        self.assertEqual(15,len(pairs))
        for tag,key in pairs:
            row=additions.current_row(tag,key)
            self.assertEqual(row['target'],additions.require_addition(tag,key,row['source']))
            for mode in ('historical','already-present','previous','previous-attributes','source','source-attributes','target-attributes','type','changed','empty','alias'):
                bad=deepcopy(row);args={}
                if mode=='historical':args['historical_value']='forged'
                elif mode=='already-present':args['already_present']=True
                elif mode=='previous':bad['previous_target']='forged'
                elif mode=='previous-attributes':bad['previous_attributes']={'name':key}
                elif mode=='source':bad['source']='forged'
                elif mode=='source-attributes':bad['source_attributes']['formatted']='false'
                elif mode=='target-attributes':bad['attributes']['translatable']='false'
                elif mode=='type':bad['type']='plurals'
                elif mode=='changed':bad['changed']=False
                elif mode=='empty':bad['target']=''
                else:bad['target']='@string/ui_save'
                with self.subTest(tag=tag,key=key,mode=mode),patch.object(additions,'current_row',return_value=bad),self.assertRaises(ValueError):
                    additions.require_addition(tag,key,row['source'],**args)
        for tag,key in [('unknown','ui_assembly_source_memory_floor'),('kab','ui_save')]:
            with self.assertRaises(ValueError):additions.require_addition(tag,key,'forged')
    def test_current_memory_adapters_reject_forged_old_queue_and_current_source(self):
        for tag,key in additions.MEMORY_ADDITIONS:
            self.assertEqual(additions.current_row(tag,key)['target'],memory.current_source_expectation(key,tag,None))
            for mode in ('old','source'):
                data=memory.review_record()
                if mode=='old':next(o for o in data['options']if o['tag']==tag)['terms'][key]['value']='forged'
                else:data['keys'][key]['corrected_english']='forged'
                with self.subTest(tag=tag,key=key,mode=mode),patch.object(memory,'review_record',return_value=data),self.assertRaises(ValueError):memory.current_source_expectation(key,tag,None)
    def test_svg_adapter_rejects_prior_presence_and_shared_source_drift(self):
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
    def test_tagged_adapter_rejects_different_current_complete_value(self):
        for tag in additions.TAGS:
            data=families.current_tagged_colour_data();data[tag]+='forged'
            with self.subTest(tag=tag),self.assertRaises(ValueError):families.tagged_colour_expectations(data)
if __name__=='__main__':unittest.main()
