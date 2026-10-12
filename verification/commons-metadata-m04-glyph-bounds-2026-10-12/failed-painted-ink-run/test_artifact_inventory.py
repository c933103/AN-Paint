"""Synthetic checker controls, not native JVM evidence."""
import unittest,tempfile,pathlib,json,xml.etree.ElementTree as ET
from unittest.mock import patch
import audit_ink_artifacts as a
SOURCE=pathlib.Path(__file__).with_name('expected-jvm-identities.json')
class InventoryCheckTest(unittest.TestCase):
    def xml(self,p,identities,skip=False):
        suite=ET.Element('testsuite',tests=str(len(identities)),failures='0',errors='0',skipped='1' if skip else '0')
        for i,(c,n) in enumerate(identities):
            case=ET.SubElement(suite,'testcase',classname=c,name=n)
            if i==0 and skip:ET.SubElement(case,'skipped')
        (p/'TEST-synthetic.xml').write_bytes(ET.tostring(suite))
    def test_exact_892_multiset_not_just_count(self):
        inventory=json.loads(SOURCE.read_bytes())['expected'];self.assertEqual(892,len(inventory))
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);self.xml(p,inventory);self.assertEqual('PASS',a.junit_audit(p,inventory)['status'])
            self.xml(p,inventory[:-1]);self.assertEqual('FAIL',a.junit_audit(p,inventory)['status'])
            self.xml(p,inventory[:-1]+[inventory[0]]);result=a.junit_audit(p,inventory);self.assertEqual('FAIL',result['status']);self.assertTrue(result['duplicates']);self.assertTrue(result['missing'])
            self.xml(p,inventory,True);self.assertEqual('FAIL',a.junit_audit(p,inventory)['status'])
    def test_cannot_claim_acceptance_before_publication_binding(self):
        with patch.object(a,'TREE','PENDING'),self.assertRaisesRegex(ValueError,'actual publication binding is pending'):
            a.bind_archive(pathlib.Path('/does-not-exist'),pathlib.Path('/does-not-exist'),{})
if __name__=='__main__':unittest.main()
