"""Negative controls bound to compact evidence from the actual fresh APK.

These perturb decoded actual inputs; they are checker controls, not mutated APK
acceptance or installed Android execution. Binary XML byte-parser controls are
separate in test_compiled_picker_checker.py.
"""
import argparse, copy, json, pathlib, re, unittest
from audit_compiled_picker import check_manifest_binding, locale_resource, check_platform_tags, sha

EVIDENCE=None

class ActualBindingControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((EVIDENCE/'compiled-picker-result.json').read_bytes())
        if cls.result['status']!='PASS':raise ValueError('actual APK acceptance required before controls')
        for name,digest in cls.result['scoped_evidence_sha256'].items():
            if sha((EVIDENCE/name).read_bytes())!=digest:raise ValueError('actual scoped input differs: '+name)
        cls.manifest=(EVIDENCE/'compiled-platform-manifest.txt').read_text()
        cls.attrs=json.loads((EVIDENCE/'compiled-application-attributes.json').read_bytes())
        cls.resource=(EVIDENCE/'compiled-platform-resource.txt').read_text()
        cls.xml=(EVIDENCE/'compiled-platform-locales.txt').read_text()
        cls.tags=json.loads((EVIDENCE/'compiled-platform-tags.json').read_bytes())
        cls.rid=cls.result['locale_resource_id']
        if sha(cls.xml.encode())!=cls.result['platform_xml_dump_sha256']:raise ValueError('actual platform XML receipt differs')
        if locale_resource(cls.resource)[0]!=cls.rid:raise ValueError('actual resource ID differs')
        if check_manifest_binding(cls.manifest,cls.attrs,cls.rid)['binary']!=cls.result['manifest_locale_binding_binary']:raise ValueError('actual manifest receipt differs')
        check_platform_tags(cls.xml,cls.tags,cls.tags)

    def reject_binding(self,mutator,pattern):
        attrs=copy.deepcopy(self.attrs);manifest=self.manifest;rid=self.rid
        manifest,attrs,rid=mutator(manifest,attrs,rid)
        with self.assertRaisesRegex(ValueError,pattern):check_manifest_binding(manifest,attrs,rid)

    def attr_change(self,key,value):
        def change(m,a,r):
            next(x for x in a if x['name']=='localeConfig')[key]=value
            return m,a,r
        return change

    def test_actual_binding(self):self.assertEqual(check_manifest_binding(self.manifest,self.attrs,self.rid)['binary'],self.result['manifest_locale_binding_binary'])
    def test_missing_binary_attribute(self):self.reject_binding(lambda m,a,r:(m,[x for x in a if x['name']!='localeConfig'],r),'missing/duplicate')
    def test_missing_aapt_attribute(self):self.reject_binding(lambda m,a,r:(re.sub(r'^.*:localeConfig.*\n','',m,flags=re.M),a,r),'missing/duplicate')
    def test_wrong_binary_namespace(self):self.reject_binding(self.attr_change('namespace','urn:not-android'),'wrong namespace')
    def test_missing_binary_namespace(self):self.reject_binding(self.attr_change('namespace',None),'wrong namespace')
    def test_wrong_aapt_namespace(self):self.reject_binding(lambda m,a,r:(m.replace('http://schemas.android.com/apk/res/android:localeConfig','urn:not-android:localeConfig'),a,r),'missing/duplicate')
    def test_wrong_binary_type(self):self.reject_binding(self.attr_change('value_type','0x10'),'wrong type')
    def test_wrong_aapt_type(self):self.reject_binding(lambda m,a,r:(m.replace('=@'+r,'="'+r+'"'),a,r),'missing/duplicate')
    def test_wrong_binary_target(self):self.reject_binding(self.attr_change('data','0x7fff7777'),'wrong target')
    def test_wrong_aapt_target(self):self.reject_binding(lambda m,a,r:(m.replace('=@'+r,'=@0x7fff7777'),a,r),'wrong target')
    def test_consistent_wrong_target_both_parsers(self):
        def change(m,a,r):
            next(x for x in a if x['name']=='localeConfig')['data']='0x7fff7777'
            return m.replace('=@'+r,'=@0x7fff7777'),a,r
        self.reject_binding(change,'wrong target')
    def test_wrong_framework_name_id(self):self.reject_binding(self.attr_change('name_resource_id','0x010100ff'),'framework attribute ID')
    def test_consistent_wrong_framework_id_both_parsers(self):
        def change(m,a,r):
            row=next(x for x in a if x['name']=='localeConfig');old=row['name_resource_id'];row['name_resource_id']='0x010100ff'
            return m.replace(':localeConfig('+old+')',':localeConfig(0x010100ff)'),a,r
        self.reject_binding(change,'framework attribute ID')
    def test_duplicate_binary_attribute(self):self.reject_binding(lambda m,a,r:(m,a+[copy.deepcopy(next(x for x in a if x['name']=='localeConfig'))],r),'missing/duplicate')
    def test_duplicate_aapt_attribute(self):self.reject_binding(lambda m,a,r:(m+next(x for x in m.splitlines(True) if ':localeConfig' in x),a,r),'missing/duplicate')
    def test_child_attribute_does_not_bind_application(self):
        def change(m,a,r):
            line=next(x for x in m.splitlines(True) if ':localeConfig' in x)
            m=m.replace(line,'')+'        E: activity (line=99)\n  '+line
            return m,a,r
        self.reject_binding(change,'missing/duplicate')
    def test_changed_resource_id_is_derived(self):
        # A new valid resource table ID, matched by both independent views, passes.
        changed='0x7ffe1234';attrs=copy.deepcopy(self.attrs)
        next(x for x in attrs if x['name']=='localeConfig')['data']=changed
        rid=locale_resource(self.resource.replace(self.rid,changed))[0]
        self.assertEqual(rid,changed)
        self.assertEqual(check_manifest_binding(self.manifest.replace('=@'+self.rid,'=@'+changed),attrs,rid)['binary'][0]['data'],changed)
    def test_resource_missing(self):
        with self.assertRaisesRegex(ValueError,'missing/duplicate'):locale_resource(self.resource.replace('xml/app_locales','xml/not_app_locales'))
    def test_resource_duplicate(self):
        with self.assertRaisesRegex(ValueError,'missing/duplicate'):locale_resource(self.resource*2)
    def test_resource_wrong_type(self):
        with self.assertRaisesRegex(ValueError,'unexpected locale file'):locale_resource(self.resource.replace('type=XML','type=PNG'))
    def test_resource_wrong_packaged_path(self):
        with self.assertRaisesRegex(ValueError,'unexpected locale file'):locale_resource(self.resource.replace('res/xml/app_locales.xml','res/xml/other.xml'))
    def test_resource_extra_configuration(self):
        with self.assertRaisesRegex(ValueError,'unexpected locale file'):locale_resource(self.resource+'      (ar) (file) res/xml/app_locales.xml type=XML\n')
    def test_actual_tags(self):self.assertEqual(check_platform_tags(self.xml,self.tags,self.tags),self.tags)
    def test_wrong_platform_root(self):
        with self.assertRaisesRegex(ValueError,'root/element/nesting'):check_platform_tags(self.xml.replace('E: locale-config','E: resources'),self.tags,self.tags)
    def test_nested_platform_locale(self):
        with self.assertRaisesRegex(ValueError,'root/element/nesting'):check_platform_tags(self.xml.replace('      E: locale','        E: locale',1),self.tags,self.tags)
    def test_extra_platform_attribute(self):
        with self.assertRaisesRegex(ValueError,'attribute inventory'):check_platform_tags(self.xml+'        A: other=\"value\"\n',self.tags,self.tags)
    def test_platform_locale_removed(self):
        changed=re.sub(r'      E: locale \(line=\d+\)\n[^\n]*\n','',self.xml,count=1)
        with self.assertRaisesRegex(ValueError,'root/element/nesting'):check_platform_tags(changed,self.tags,self.tags)
    def test_platform_tag_changed(self):
        changed=self.xml.replace('="'+self.tags[0]+'"','="und"',1)
        with self.assertRaisesRegex(ValueError,'order/content'):check_platform_tags(changed,self.tags,self.tags)
    def test_platform_name_namespace_changed(self):
        changed=self.xml.replace('http://schemas.android.com/apk/res/android:name','urn:wrong:name',1)
        with self.assertRaisesRegex(ValueError,'inventory'):check_platform_tags(changed,self.tags,self.tags)
    def test_source_tag_removed(self):
        with self.assertRaisesRegex(ValueError,'root/element/nesting'):check_platform_tags(self.xml,self.tags[1:],self.tags)
    def test_picker_tag_duplicated(self):
        changed=self.tags.copy();changed[0]=changed[1]
        with self.assertRaisesRegex(ValueError,'order/content'):check_platform_tags(self.xml,self.tags,changed)
    def test_picker_order_changed(self):
        changed=self.tags.copy();changed[0],changed[1]=changed[1],changed[0]
        with self.assertRaisesRegex(ValueError,'order/content'):check_platform_tags(self.xml,self.tags,changed)
    def test_picker_tag_extra(self):
        with self.assertRaisesRegex(ValueError,'order/content'):check_platform_tags(self.xml,self.tags,self.tags+['und'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--evidence-directory',type=pathlib.Path,required=True)
    args,extra=parser.parse_known_args();EVIDENCE=args.evidence_directory
    unittest.main(argv=['test_platform_binding_checker.py',*extra])
