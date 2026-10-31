"""737 additions, two replacements, and exact rejection of unaccepted expansion."""
from copy import deepcopy
from collections import Counter
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
import translation_catalogues as c
from current_localization_contracts import fixture, require_residual_or_previous
from remaining_accepted_wording import rows, TAGS, COUNTS, EXISTING, require_historical_catalogue
from priority_cohort_checks import require_resource_shape


class RemainingAcceptedWordingTests(unittest.TestCase):
    def test_exact_packet_accounting_source_and_serialization(self):
        accepted=rows()
        self.assertEqual(739,len(accepted))
        self.assertEqual(737,sum(r['previous_target'] is None for r in accepted.values()))
        english=ET.parse(c.RES/'values/strings.xml').getroot()
        roots={tag:ET.parse(c.catalogue_paths()[tag]).getroot() for tag in TAGS}
        for (tag,key),row in accepted.items():
            with self.subTest(tag=tag,key=key):
                require_resource_shape(english.find(f"./string[@name='{key}']"),'string',{'value':row['source'],'attributes':row['attributes']})
                require_residual_or_previous(roots[tag],tag,key,row['previous_target'])
                self.assertEqual(c.placeholders(row['source']),c.placeholders(row['target']))
                self.assertEqual([],c.android_string_errors(row['target']))
                self.assertEqual([],c.format_string_errors(row['target'],row['attributes'].get('formatted')!='false'))
        for tag in ('ang','non'):require_historical_catalogue(tag,roots[tag])
        for tag in TAGS:self.assertEqual([],c.validate_catalogue(tag))

    def test_every_value_rejects_shape_text_and_predecessor_mutations(self):
        for (tag,key),row in rows().items():
            def check(root,previous=row['previous_target']):
                require_residual_or_previous(root,tag,key,previous)
                require_resource_shape(root.find(f"./string[@name='{key}']"),'string',{'value':row['target'],'attributes':row['attributes']})
            original=ET.Element('resources');ET.SubElement(original,'string',row['attributes']).text=row['target']
            check(original)
            for mode in ('absent','duplicate','type','text','attribute','child','tail','predecessor'):
                root=deepcopy(original);node=root[0]
                if mode=='absent':root.remove(node)
                elif mode=='duplicate':root.append(deepcopy(node))
                elif mode=='type':node.tag='plurals'
                elif mode=='text':node.text+=' forged'
                elif mode=='attribute':node.set('translatable','false')
                elif mode=='child':ET.SubElement(node,'b')
                elif mode=='tail':node.tail='forged'
                else:node.text=row['previous_target'] or 'unreviewed'
                with self.subTest(tag=tag,key=key,mode=mode),self.assertRaises(ValueError):check(root)
            with self.assertRaises(ValueError):check(original,'forged predecessor')

    def test_holds_unchanged_undo_and_historical_fixture_predecessors(self):
        accepted=rows()
        for tag,key in [('br','ui_fit_image'),('sv','ui_main23'),('non','ui_autosave_is_paused_to_protect_that_draft_use')]:
            self.assertNotIn((tag,key),accepted)
        self.assertEqual('"Skeudenn o kenglotañ gant ar prenestr"',c.read_strings(c.catalogue_paths()['br'])['ui_fit_image'])
        self.assertEqual('Huvud',c.read_strings(c.catalogue_paths()['sv'])['ui_main23'])
        self.assertEqual('"ၶိုၼ်ၶိုၼ်း"',c.read_strings(c.catalogue_paths()['shn'])['ui_undo'])
        br=fixture('breton_asturian_occitan_priority_wording.json')['locales']['br']['accepted']
        self.assertEqual(br['ui_drawing_canvas_pinch_and_move_two_fingers_to'],accepted[('br','ui_drawing_canvas_pinch_and_move_two_fingers_to')]['previous_target'])
        batch=fixture('reviewed_priority_batches.json')['locales']['shn']
        self.assertEqual(batch['existing_unreviewed']['ui_brush']['value'],accepted[('shn','ui_brush')]['previous_target'])
        for tag in ('ang','non'):
            root=ET.parse(c.catalogue_paths()[tag]).getroot()
            ET.SubElement(root,'string',{'name':'unreviewed'}).text='not accepted'
            with self.assertRaises(ValueError):require_historical_catalogue(tag,root)


if __name__=='__main__':unittest.main()
