"""Complete newly reviewed manual values and the precise historical-hold successor."""
from copy import deepcopy
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as E
import swedish_legacy_manual as m
import translation_catalogues as c
from current_localization_contracts import fixture


class SwedishLegacyManualTests(unittest.TestCase):
    def setUp(self):
        self.data = m.decision()
        self.roots = {tag: E.parse(m.ROOT/'Paintroid/src/main/res'/folder/'strings.xml').getroot()
                      for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}

    def previous(self, tag):
        return {'value': self.data['previous_source'], 'attributes': m.ATTRIBUTES} if tag == 'default' else None

    def node(self, tag):
        return self.roots[tag].find(f"./string[@name='{m.KEY}']")

    def test_complete_values_and_explicit_historical_hold_disposition(self):
        for tag in self.roots:
            nodes = self.roots[tag].findall(f"./*[@name='{m.KEY}']")
            self.assertEqual(1, len(nodes))
            m.require_successor(tag, m.KEY, nodes[0], self.previous(tag))
            value = nodes[0].text
            self.assertEqual(10, len(value.split(r'\n\n')))
            self.assertEqual(18, value.count(r'\n'))
            self.assertEqual({}, c.placeholders(value))
            self.assertEqual([], c.android_string_errors(value))
            self.assertEqual([], c.format_string_errors(value, False))
        historical = fixture('swedish_extended_wording.json')
        self.assertIn(m.KEY, historical['held_missing'])
        self.assertEqual(['ui_main23'], historical['present_held'])
        self.assertEqual('Huvud', self.roots['sv'].find("./string[@name='ui_main23']").text)
        self.assertIsNone(self.data['previous_swedish'])

    def test_exact_identity_predecessor_required(self):
        for tag,key,old in [('en-US',m.KEY,None), ('sv','ui_help23',None),
                            ('sv',m.KEY,{'value':'forged','attributes':m.ATTRIBUTES}),
                            ('default',m.KEY,None), ('default',m.KEY,{'value':self.data['source'],'attributes':m.ATTRIBUTES})]:
            with self.subTest(tag=tag,key=key), self.assertRaises(ValueError):
                m.require_successor(tag,key,self.node('sv'),old)

    def test_target_corruption_missing_markup_attributes_tail_and_old_wording_rejected(self):
        for tag in self.roots:
            for mode in ('missing','type','text','placeholder','attributes','child','tail','old'):
                node=deepcopy(self.node(tag))
                if mode=='missing': node=None
                elif mode=='type': node.tag='plurals'
                elif mode=='text': node.text=node.text[:-1]
                elif mode=='placeholder': node.text+='%1$s'
                elif mode=='attributes': node.set('formatted','true')
                elif mode=='child': E.SubElement(node,'b')
                elif mode=='tail': node.tail='unexpected'
                else: node.text=self.data['previous_source']
                with self.subTest(tag=tag,mode=mode), self.assertRaises(ValueError):
                    m.require_successor(tag,m.KEY,node,self.previous(tag))

    def test_source_mutations_cannot_bind_swedish_to_wrong_or_duplicate_source(self):
        for mode in ('missing','duplicate','type','text','attributes','child','tail'):
            root=deepcopy(self.roots['default']);node=root.find(f"./string[@name='{m.KEY}']")
            if mode=='missing': root.remove(node)
            elif mode=='duplicate': root.append(deepcopy(node))
            elif mode=='type': node.tag='plurals'
            elif mode=='text': node.text=self.data['previous_source']
            elif mode=='attributes': node.set('formatted','true')
            elif mode=='child': E.SubElement(node,'b')
            else: node.tail='unexpected'
            with patch.object(m.E,'parse',return_value=E.ElementTree(root)):
                with self.subTest(mode=mode), self.assertRaises(ValueError):
                    m.require_successor('sv',m.KEY,self.node('sv'),None)

    def test_live_labels_and_behavioral_distinctions_are_not_stale(self):
        expected = {
            'default': {1:['Color tab','foreground or background','existing canvas','white backing'],
                        2:['Draw again','floating selection'],4:['options panel','Edit > Selection','quick actions'],
                        6:['Drawing category','View > Magnifier lets you enable'],
                        7:['Wikimedia Commons'],8:['Exact position','permits overlaps','may move to fill the gap']},
            'sv': {1:['Fliken Färg','förgrunds- eller bakgrundsdel','befintliga ritytan','vit bakgrund'],
                   2:['Fortsätt rita','flytande markering'],4:['alternativpanelen','Redigera > Markering','snabbåtgärder'],
                   6:['kategorin Ritverktyg','Visa > Förstoringsglas kan du aktivera'],
                   7:['Wikimedia Commons'],8:['Exakt position','tillåter överlappning','kan flyttas för att fylla luckan']}}
        for tag, checks in expected.items():
            paragraphs=self.node(tag).text.split(r'\n\n')
            for index, parts in checks.items():
                for part in parts:
                    with self.subTest(tag=tag,paragraph=index+1,part=part): self.assertIn(part,paragraphs[index])
            self.assertNotIn('one undoable selection edit',paragraphs[4])
            self.assertNotIn('fixed at the lower left',paragraphs[1])
        self.assertIn('fäller ihop eller fäller ut panelen.',self.node('sv').text)

    def test_fixture_scope_is_finite(self):
        for field,value in [('key','ui_help23'),('schema_version',True),('previous_swedish','forged'),
                            ('attributes',{'name':m.KEY}),('source',self.data['previous_source'])]:
            data=deepcopy(self.data);data[field]=value
            with patch.object(m,'fixture',return_value=data), self.subTest(field=field), self.assertRaises(ValueError):
                m.decision()


if __name__=='__main__': unittest.main()
