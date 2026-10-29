"""Bounded Indonesian conditional warning: full finite values and corruption controls."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import json,re,tempfile,unittest,xml.etree.ElementTree as ET
from unittest.mock import patch
import indonesian_crop_expectations as oracle
import translation_catalogues as catalogues

class IndonesianCropFollowthroughTest(unittest.TestCase):
    def setUp(self):
        self.data=oracle.reviewed_fixture()
        self.source=catalogues.RES/'values/strings.xml'
        self.paths={t:catalogues.catalogue_paths()[t] for t in self.data['locales']}
    def test_exact_single_other_container_and_retained_context(self):
        self.assertEqual({'id'},set(self.data['locales']))
        self.assertIn('id',catalogues.offered_tags())
        self.assertEqual('values-in',self.paths['id'].parent.name)
        rows=self.data['locales']['id']
        self.assertEqual({'plurals/ui_crop_preview_images','string/ui_choose_at_least_one_image'},set(rows))
        changed=[r for r in rows.values() if r['changed']]
        self.assertEqual(1,len(changed));r=changed[0]
        self.assertEqual({'other'},set(r['display']))
        self.assertEqual(r['previous']['attributes'],r['target']['attributes'])
        self.assertEqual(r['previous']['value'][0]['attributes'],r['target']['value'][0]['attributes'])
        self.assertEqual({'quantity':'other'},r['target']['value'][0]['attributes'])
        old=r['previous']['value'][0]['value'];new=r['target']['value'][0]['value']
        self.assertEqual(old.split('Pemangkasan')[0],new.split('Pemangkasan')[0])
        self.assertEqual(Counter(re.findall(r'%\d+\$[sdf]',old)),Counter(re.findall(r'%\d+\$[sdf]',new)))
        self.assertIn('dapat menggeser gambar yang tersambung dengannya.',new)
        self.assertTrue(oracle.validate_resources(self.data,self.source,self.paths))
    def test_fixture_is_detached_and_all_metadata_and_previous_changes_fail(self):
        original=oracle.reviewed_fixture()
        for tag,rows in original['locales'].items():
            for key in rows:
                for field in ['source','previous','target','display','changed','scope']:
                    data=deepcopy(original);data['locales'][tag][key][field]='forged'
                    with self.subTest(tag=tag,key=key,field=field),self.assertRaises(ValueError):oracle.row(data,tag,key)
                data=deepcopy(original);del data['locales'][tag][key]['previous']
                with self.assertRaises(ValueError):oracle.require_reviewed_fixture(data)
        self.assertEqual(original,oracle.reviewed_fixture())
    def test_each_coordinated_target_display_resource_mutation_fails(self):
        for tag,rows in self.data['locales'].items():
            for key,r in rows.items():
                if not r['changed']:continue
                data=deepcopy(self.data);forged=data['locales'][tag][key];forged['target']['value']='forged';forged['display']='forged'
                with tempfile.TemporaryDirectory()as d:
                    target=Path(d)/'strings.xml';root=ET.parse(self.paths[tag]).getroot();kind,name=key.split('/');node=root.find(f"./{kind}[@name='{name}']");node.text='forged'
                    for child in list(node):node.remove(child)
                    ET.ElementTree(root).write(target,encoding='unicode')
                    with self.assertRaises(ValueError):oracle.validate_resources(data,self.source,{**self.paths,tag:target})
    def test_missing_duplicate_attributes_markup_plural_swap_and_truncation_fail(self):
        for tag,rows in self.data['locales'].items():
            for key,r in rows.items():
                if not r['changed']:continue
                for mode in ['missing','duplicate','attributes','markup','truncate','plural-quantity','plural-extra-item']:
                    kind,name=key.split('/')
                    if mode.startswith('plural')and kind!='plurals':continue
                    with tempfile.TemporaryDirectory()as d:
                        target=Path(d)/'strings.xml';root=ET.parse(self.paths[tag]).getroot();node=root.find(f"./{kind}[@name='{name}']")
                        if mode=='missing':root.remove(node)
                        elif mode=='duplicate':root.append(deepcopy(node))
                        elif mode=='attributes':node.set('formatted','false')
                        elif mode=='markup':ET.SubElement(node,'b').text='forged'
                        elif mode=='truncate':
                            n=node if kind=='string'else node[0];n.text=n.text[:-3]
                        elif mode=='plural-quantity':node[0].set('quantity','zero')
                        else:node.append(deepcopy(node[0]))
                        ET.ElementTree(root).write(target,encoding='unicode')
                        with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):oracle.validate_resources(self.data,self.source,{**self.paths,tag:target})
    def test_root_tail_nested_plural_and_wrong_type_duplicates_fail(self):
        cases=[('id','string/ui_choose_at_least_one_image',m)for m in ['resource-tail','root-text','root-tag','root-attribute','wrong-type-duplicate']]
        cases += [('id','plurals/ui_crop_preview_images',m)for m in ['nested-plural','plural-tail','plural-text','plural-item-type','wrong-type-duplicate']]
        for tag,key,mode in cases:
            with tempfile.TemporaryDirectory()as d:
                p=Path(d)/'strings.xml';root=ET.parse(self.paths[tag]).getroot();kind,name=key.split('/');node=root.find(f"./{kind}[@name='{name}']")
                if mode=='resource-tail':node.tail='FORGED EXTRA TEXT'
                elif mode=='root-text':root.text='FORGED EXTRA TEXT'
                elif mode=='root-tag':root.tag='forged'
                elif mode=='root-attribute':root.set('forged','true')
                elif mode=='wrong-type-duplicate':
                    other=deepcopy(node);other.tag='plurals'if kind=='string'else'string';root.append(other)
                elif mode=='nested-plural':ET.SubElement(node[0],'b').text='FORGED EXTRA TEXT'
                elif mode=='plural-tail':node[0].tail='FORGED EXTRA TEXT'
                elif mode=='plural-text':node.text='FORGED EXTRA TEXT'
                else:node[0].tag='string'
                ET.ElementTree(root).write(p,encoding='unicode')
                with self.subTest(tag=tag,mode=mode),self.assertRaises(ValueError):oracle.validate_resources(self.data,self.source,{**self.paths,tag:p})
    def test_unrelated_valid_resource_types_remain_outside_finite_scope(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/'strings.xml';root=ET.parse(self.paths['id']).getroot()
            ET.SubElement(root,'color',{'name':'unrelated'}).text='#ffffff'
            ET.SubElement(root,'string',{'name':'unrelated'}).text='Independent unrelated value'
            ET.ElementTree(root).write(p,encoding='unicode')
            self.assertTrue(oracle.validate_resources(self.data,self.source,{**self.paths,'id':p}))
    def test_raw_fixture_hash_and_boolean_number_type_changes_fail(self):
        data=deepcopy(self.data);data['schema']=True
        with self.assertRaises(ValueError):oracle.require_reviewed_fixture(data)
        data=deepcopy(self.data);data['locales']['id']['string/ui_choose_at_least_one_image']['changed']=1
        with self.assertRaises(ValueError):oracle.require_reviewed_fixture(data)
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/'fixture.json';p.write_bytes(oracle.FIXTURE.read_bytes()+b' ')
            oracle._baseline.cache_clear()
            try:
                with patch.object(oracle,'FIXTURE',p),self.assertRaises(ValueError):oracle.reviewed_fixture()
            finally:oracle._baseline.cache_clear()
    def test_source_binding_and_top_level_metadata_cannot_change(self):
        for field in ['schema','scope','review_packet_sha256','independent_receipt_sha256']:
            data=deepcopy(self.data);data[field]='forged'
            with self.assertRaises(ValueError):oracle.require_reviewed_fixture(data)
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/'source.xml';root=ET.parse(self.source).getroot()
            root.find("./plurals[@name='ui_crop_preview_images']")[0].text='forged'
            ET.ElementTree(root).write(p,encoding='unicode')
            with self.assertRaises(ValueError):oracle.validate_resources(self.data,p,self.paths)
if __name__=='__main__':unittest.main()
