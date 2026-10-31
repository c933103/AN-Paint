"""Exact later acceptance, preserving the original held evidence unchanged."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as E
import legacy_discard_disposition as d
import translation_catalogues as c
from current_localization_contracts import fixture, residual_rows
from priority_cohort_checks import require_resource_shape


class LegacyDiscardDispositionTest(unittest.TestCase):
    def setUp(self):
        self.root = E.parse(c.catalogue_paths()['ps']).getroot()
        self.node = self.root.find("./string[@name='ui_discard']")
        self.previous = d.PREVIOUS

    def test_exact_predecessor_source_target_and_unchanged_acceptance(self):
        d.require_successor('ps', d.KEY, self.node, self.previous)
        eu = E.parse(c.catalogue_paths()['eu-ES']).getroot().find("./string[@name='ui_discard']")
        require_resource_shape(eu, 'string', d.UNCHANGED)
        for tag in ('ps', 'eu-ES'):
            self.assertNotIn((tag,d.KEY), residual_rows()) # Frozen PR247 packet is unchanged.
        for value in ('Discard', self.node.text, eu.text):
            self.assertFalse(c.placeholders(value))
            self.assertEqual([], c.android_string_errors(value))
            self.assertEqual([], c.format_string_errors(value, True))
        self.assertEqual('"'+self.node.text+'"', self.root.find("./string[@name='ui_discard_changes23']").text)

    def test_rejects_wrong_identity_predecessor_and_attributes(self):
        for tag,key in (('eu-ES',d.KEY),('ps','ui_discard_changes23'),('en',d.KEY)):
            with self.assertRaises(ValueError):d.require_successor(tag,key,self.node,self.previous)
        for previous in (None, {}, {'value':'forged','attributes':{'name':d.KEY}},
                         {'value':'رد کړئ','attributes':{'name':d.KEY,'formatted':'false'}}):
            with self.assertRaises(ValueError):d.require_successor('ps',d.KEY,self.node,previous)

    def test_rejects_all_target_shape_corruption(self):
        for mode in ('missing','type','text','placeholder','attribute','child','tail','old'):
            node = deepcopy(self.node)
            if mode=='missing':node=None
            elif mode=='type':node.tag='plurals'
            elif mode=='text':node.text+=' forged'
            elif mode=='placeholder':node.text+='%1$s'
            elif mode=='attribute':node.set('formatted','false')
            elif mode=='child':E.SubElement(node,'b')
            elif mode=='tail':node.tail='forged'
            else:node.text=self.previous['value']
            with self.subTest(mode=mode),self.assertRaises(ValueError):
                d.require_successor('ps',d.KEY,node,self.previous)

    def test_rejects_source_corruption_missing_duplicate_and_attributes(self):
        original=E.parse(d.ROOT/'Paintroid/src/main/res/values/strings.xml')
        for mode in ('missing','duplicate','type','text','placeholder','attributes','child'):
            tree=deepcopy(original);root=tree.getroot();node=root.find("./string[@name='ui_discard']")
            if mode=='missing':root.remove(node)
            elif mode=='duplicate':root.append(deepcopy(node))
            elif mode=='type':node.tag='plurals'
            elif mode=='text':node.text='Abandon'
            elif mode=='placeholder':node.text+='%1$s'
            elif mode=='attributes':node.set('formatted','false')
            else:E.SubElement(node,'b')
            with patch.object(d.E,'parse',return_value=tree):
                with self.subTest(mode=mode),self.assertRaises(ValueError):
                    d.require_successor('ps',d.KEY,self.node,self.previous)


if __name__=='__main__':unittest.main()
