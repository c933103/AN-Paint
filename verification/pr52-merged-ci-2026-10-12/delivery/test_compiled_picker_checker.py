"""Portable parser controls; synthetic data does not count as APK acceptance."""
import json, struct, unittest
from audit_compiled_picker import array_block,binary_application_attributes

def sample_array(values=('a','b'),declared=2,config='',suffix=''):
    return '    resource 0x7f020002 array/test\n      ('+config+') (array) size='+str(declared)+'\n        '+json.dumps(values)+'\n'+suffix

def sample_xml(utf8=False,app='application',two_apps=False):
    values=[app,'localeConfig','http://schemas.android.com/apk/res/android']
    offsets=[];data=b''
    for value in values:
        offsets.append(len(data))
        if utf8:
            encoded=value.encode('utf-8');data+=bytes([len(value),len(encoded)])+encoded+b'\0'
        else:
            encoded=value.encode('utf-16-le');data+=struct.pack('<H',len(value))+encoded+b'\0\0'
    data+=b'\0'*((-len(data))%4)
    start=28+4*len(values)
    pool=struct.pack('<HHIIIIII',1,28,start+len(data),len(values),0,0x100 if utf8 else 0,start,0)+struct.pack('<III',*offsets)+data
    resource_map=struct.pack('<HHIII',0x180,8,16,0,0x010100ff)
    element=struct.pack('<HHIII',0x102,16,56,1,0xffffffff)+struct.pack('<IIHHHHHH',0xffffffff,0,20,20,1,0,0,0)+struct.pack('<IIIHBBI',2,1,0xffffffff,8,0,1,0x7f100000)
    content=pool+resource_map+element+(element if two_apps else b'')
    return struct.pack('<HHI',3,8,8+len(content))+content

class ArrayParserTest(unittest.TestCase):
    def test_exact_values(self):self.assertEqual(array_block(sample_array(),'test')[2],['a','b'])
    def test_next_type_boundary(self):self.assertEqual(array_block(sample_array(suffix='  type attr id=03 entryCount=1\n    resource 0x7f030000 attr/test\n'),'test')[2],['a','b'])
    def test_declared_count_rejected(self):
        with self.assertRaisesRegex(ValueError,'count/type'):array_block(sample_array(declared=3),'test')
    def test_nonstring_rejected(self):
        with self.assertRaisesRegex(ValueError,'count/type'):array_block(sample_array(values=['a',1]),'test')
    def test_duplicate_resource_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing/duplicate'):array_block(sample_array()*2,'test')
    def test_missing_resource_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing/duplicate'):array_block(sample_array(),'absent')
    def test_extra_config_rejected(self):
        with self.assertRaisesRegex(ValueError,'configuration or syntax'):array_block(sample_array(suffix='      (ar) (array) size=1\n        ["a"]\n'),'test')
    def test_nondefault_config_rejected(self):
        with self.assertRaisesRegex(ValueError,'configuration or syntax'):array_block(sample_array(config='ar'),'test')

class BinaryManifestParserTest(unittest.TestCase):
    def test_utf16_reference_and_numeric_id(self):
        row=binary_application_attributes(sample_xml())[0]
        self.assertEqual(row,{'namespace':'http://schemas.android.com/apk/res/android','name':'localeConfig','name_resource_id':'0x010100ff','raw_value':None,'value_type':'0x01','data':'0x7f100000','string_value':None})
    def test_utf8_pool(self):self.assertEqual(binary_application_attributes(sample_xml(True)),binary_application_attributes(sample_xml()))
    def test_missing_application(self):
        with self.assertRaisesRegex(ValueError,'missing/duplicate application'):binary_application_attributes(sample_xml(app='activity'))
    def test_duplicate_application(self):
        with self.assertRaisesRegex(ValueError,'missing/duplicate application'):binary_application_attributes(sample_xml(two_apps=True))
    def test_incorrect_envelope(self):
        data=sample_xml()
        with self.assertRaisesRegex(ValueError,'envelope'):binary_application_attributes(data+b'\0')
    def test_incorrect_value_type_header(self):
        data=bytearray(sample_xml());struct.pack_into('<H',data,len(data)-8,7)
        with self.assertRaisesRegex(ValueError,'typed XML value'):binary_application_attributes(data)
    def test_incorrect_attribute_size(self):
        data=bytearray(sample_xml());struct.pack_into('<H',data,len(data)-56+26,19)
        with self.assertRaisesRegex(ValueError,'attribute size'):binary_application_attributes(data)

if __name__=='__main__':unittest.main()
