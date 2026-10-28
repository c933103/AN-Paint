"""One finite device-language addition; historical routing fixture is immutable."""
import copy,json,unittest
from unittest.mock import patch
import basque_frisian_uzbek_priority_expectations as h

class UzbekScriptPrioritySuccessor(unittest.TestCase):
    def old(self):
        return {'requested_tag':'uz-Latn','resource_tag':'uz-Latn','expected':{'ui_save':'Saqlash','ui_menu_file':'Fayl','language20_device_default':'Use device language'}}
    def test_exact_addition_keeps_historical_input_and_every_other_row(self):
        path=h.ROOT/'Paintroid/src/test/resources/exact-script-resources/expected.json'
        rows=json.loads(path.read_text());before=copy.deepcopy(rows)
        targets=[r for r in rows if r['requested_tag']=='uz-Latn'];self.assertEqual(1,len(targets));self.assertEqual(self.old(),targets[0])
        current=[h.reviewed_uzbek_script_row(r) if r['requested_tag']=='uz-Latn' else r for r in rows]
        self.assertEqual(before,rows);self.assertEqual(28,len(current))
        self.assertEqual(1,sum(a!=b for a,b in zip(rows,current)))
        out=next(r for r in current if r['requested_tag']=='uz-Latn')
        self.assertEqual('Qurilma tilidan foydalanish',out['expected']['language20_device_default'])
        self.assertEqual('Saqlash',out['expected']['ui_save']);self.assertEqual('Fayl',out['expected']['ui_menu_file'])
    def test_changed_predecessor_and_review_fixture_are_rejected(self):
        old=self.old();bad=[]
        for key in old:
            r=copy.deepcopy(old);del r[key];bad.append(r)
        for key in ('requested_tag','resource_tag'):
            r=copy.deepcopy(old);r[key]='uz';bad.append(r)
        r=copy.deepcopy(old);r['extra']=True;bad.append(r)
        for key in old['expected']:
            r=copy.deepcopy(old);del r['expected'][key];bad.append(r)
            r=copy.deepcopy(old);r['expected'][key]='forged';bad.append(r)
        r=copy.deepcopy(old);r['expected']['extra']=True;bad.append(r)
        r=copy.deepcopy(old);r['expected']['language20_device_default']='Qurilma tilidan foydalanish';bad.append(r)
        self.assertEqual(14,len(bad))
        for r in bad:
            with self.subTest(row=r),self.assertRaises(ValueError):h.reviewed_uzbek_script_row(r)
        fixture=h.bound_fixture('uz-Latn')
        for field in ('type','source','previous_target','reviewed_value','reviewed_attributes','display'):
            f=copy.deepcopy(fixture);f['values']['language20_device_default'].pop(field)
            with self.subTest(field=field),self.assertRaises(ValueError):h.reviewed_uzbek_script_row(old,f)
        f=copy.deepcopy(fixture);f['values']['language20_device_default']['reviewed_value']='"forged"';f['values']['language20_device_default']['display']='forged'
        with self.assertRaises(ValueError):h.reviewed_uzbek_script_row(old,f)
    def test_changed_live_english_is_rejected(self):
        parse=h.E.parse
        for kind in ('text','attributes','children','tail','missing'):
            def altered(path,*a,**kw):
                tree=parse(path,*a,**kw);root=tree.getroot();node=root.find("./string[@name='language20_device_default']")
                if kind=='text':node.text='forged'
                elif kind=='attributes':node.set('formatted','false')
                elif kind=='children':h.E.SubElement(node,'b').text='forged'
                elif kind=='tail':node.tail='forged'
                else:root.remove(node)
                return tree
            with self.subTest(kind=kind),patch.object(h.E,'parse',side_effect=altered),self.assertRaises(ValueError):h.reviewed_uzbek_script_row(self.old())

if __name__=='__main__':unittest.main()
