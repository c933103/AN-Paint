"""Current Swedish catalogue coverage and complete critical-message regressions.

These tests are not a linguistic certificate. Unused ambiguous legacy keys and
source-correction dependencies stay explicit rather than being counted accepted.
"""
from copy import deepcopy
import unittest
import xml.etree.ElementTree as ET
import current_localization_contracts as contracts
import translation_catalogues as catalogues
from pathlib import Path
from unittest.mock import patch
from current_localization_contracts import fixture
from priority_cohort_checks import require_resource_shape


# One finite source-gate disposition, using the existing strict shared shape check.
ROOT = Path(__file__).resolve().parents[1]
MANUAL_KEY = 'ui_the_arrow_on_the_left_directly_below_the'
MANUAL_ATTRIBUTES = {'name': MANUAL_KEY, 'formatted': 'false'}


def manual_decision():
    data = fixture('swedish_legacy_manual_successor.json')
    if (set(data) != {'schema_version', 'key', 'attributes', 'review',
                     'previous_source', 'previous_swedish', 'source', 'swedish'}
            or type(data['schema_version']) is not int or data['schema_version'] != 1
            or data['key'] != MANUAL_KEY or data['attributes'] != MANUAL_ATTRIBUTES
            or data['previous_swedish'] is not None
            or not all(isinstance(data[k], str) and data[k] for k in
                       ('previous_source', 'source', 'swedish', 'review'))
            or data['source'] == data['previous_source']):
        raise ValueError('Outside exact Swedish legacy-manual decision')
    return data


def require_manual_successor(tag, key, element, previous):
    data = manual_decision()
    old = {'value': data['previous_source'], 'attributes': MANUAL_ATTRIBUTES} if tag == 'default' else None
    if tag not in ('default', 'sv') or key != MANUAL_KEY or previous != old:
        raise ValueError('Outside exact manual identity/predecessor')
    source = ET.parse(ROOT/'Paintroid/src/main/res/values/strings.xml').getroot()
    nodes = source.findall(f"./*[@name='{MANUAL_KEY}']")
    if len(nodes) != 1:
        raise ValueError('Manual source missing or duplicated')
    require_resource_shape(nodes[0], 'string', {'value': data['source'], 'attributes': MANUAL_ATTRIBUTES})
    require_resource_shape(element, 'string', {
        'value': data['source' if tag == 'default' else 'swedish'], 'attributes': MANUAL_ATTRIBUTES})


def identities(xml):
    return {(e.tag, e.get('name')) for e in ET.fromstring(xml)
            if e.get('translatable') != 'false'}


class SwedishExtendedWordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = contracts.fixture('swedish_extended_wording.json')
        cls.manual_data = manual_decision()
        cls.xml = {tag: (catalogues.RES / folder / 'strings.xml').read_text()
                   for tag, folder in [('default', 'values'), ('sv', 'values-sv')]}
        cls.manual_roots = {tag: ET.fromstring(xml) for tag, xml in cls.xml.items()}
        cls.strings = catalogues.read_strings(catalogues.RES / 'values-sv/strings.xml')

    def test_every_current_identity_exists_except_named_source_holds(self):
        source, target = (identities(self.xml[t]) for t in ('default', 'sv'))
        held = {('string', k) for k in self.data['held_missing']}
        # The old hold record is historical; validate current palette semantics directly.
        palette = 'ui_foreground_background_colour_palette'
        self.assertIn(('string', palette), held)
        palette_text = self.strings[palette]
        self.assertIn('Förgrundsfärg', palette_text)
        self.assertIn('bakgrundsfärg', palette_text)
        self.assertEqual({'%1$s': 1, '%2$s': 1, '%3$s': 1}, catalogues.placeholders(palette_text))
        # This complete, newly source-bound pair supersedes only the manual hold.
        # The original held fixture remains historical evidence, not rewritten acceptance.
        self.assertIn(('string', MANUAL_KEY), held)
        require_manual_successor('sv', MANUAL_KEY,
                                 ET.fromstring(self.xml['sv']).find(f"./string[@name='{MANUAL_KEY}']"), None)
        self.assertEqual(held - {('string', palette), ('string', MANUAL_KEY)}, source - target)
        self.assertFalse(target - source)
        self.assertEqual(['ui_main23'], self.data['present_held'])
        self.assertEqual('Huvud', self.strings['ui_main23'])
        self.assertEqual([], catalogues.validate_catalogue('sv'))

    def test_complete_critical_values_and_format_contracts(self):
        contracts.require_wording_shape(self.data, set(self.data['values']), {'default', 'sv'})
        for key, values in self.data['values'].items():
            for tag, expected in values.items():
                with self.subTest(key=key, tag=tag):
                    contracts.require_string(self.xml[tag], key, expected, self.data['constraints'][key])

    def test_missing_full_message_fragment_markup_and_format_mutations_fail(self):
        for key, values in self.data['values'].items():
            node = ET.fromstring(self.xml['sv']).find(f"./string[@name='{key}']")
            for mutation in ('missing', 'duplicate', 'fragment', 'markup', 'format'):
                root = ET.Element('resources'); changed = deepcopy(node)
                if mutation != 'missing': root.append(changed)
                if mutation == 'duplicate': root.append(deepcopy(changed))
                elif mutation == 'fragment': changed.text = changed.text[:-1]
                elif mutation == 'markup': ET.SubElement(changed, 'b').text, changed.text = changed.text, None
                elif mutation == 'format': changed.set('formatted', 'true' if changed.get('formatted') == 'false' else 'false')
                with self.subTest(key=key, mutation=mutation), self.assertRaises(ValueError):
                    contracts.require_string(ET.tostring(root, encoding='unicode'), key, values['sv'], self.data['constraints'][key])

    def test_crop_singular_plural_keep_full_conditional_movement_warning(self):
        entry = self.data['plural']
        for tag in ('default', 'sv'):
            nodes = ET.fromstring(self.xml[tag]).findall(f"./plurals[@name='{entry['key']}']")
            self.assertEqual(1, len(nodes))
            items = nodes[0].findall('item')
            self.assertEqual(['one', 'other'], [n.get('quantity') for n in items])
            self.assertEqual(entry[tag], {n.get('quantity'): n.text for n in items})
            for node in items:
                self.assertEqual({'%1$d': 1, '%2$d': 1, '%3$d': 1}, catalogues.placeholders(node.text))
        for value in entry['sv'].values():
            self.assertIn('kan bilder som är fästa vid dem flyttas.', value)
            self.assertEqual(1, value.count('\\n'))
        self.assertIn('%3$d bild.', entry['sv']['one'])
        self.assertIn('%3$d bilder.', entry['sv']['other'])

    def test_active_help_navigation_matches_actual_controls(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        help_text = s['ui_help23']
        for key in ('ui_menu_view', 'ui_navigate', 'ui_draw26', 'ui_drawing23', 'ui_category_selection',
                    'ui_category_insert', 'ui_swap23', 'ui_reset_bw23', 'ui_use_colour', 'ui_add_colour26',
                    'ui_advanced', 'ui_pixel_grid33', 'ui_cursor_drawing32', 'ui_about_credits23', 'commons_blank_maps'):
            self.assertIn(s[key], help_text, key)
        navigation = f"{s['ui_menu_file']} → {s['ui_about_credits23']} → {s['ui_image_credits']}"
        for key in ('gallery_description', 'ui_irasutoya_help34', 'ui_openclipart_help34'):
            self.assertIn(navigation, s[key])
            self.assertIn(s['gallery_use_image'], s[key])
        self.assertIn(s['gallery_copy_credit'], s['gallery_description'])
        self.assertEqual('@string/ui_cursor_help31', s['ui_cursor_help29'])

    def test_behavioural_distinctions_are_not_flattened(self):
        s = self.strings
        self.assertEqual('Färghjul', s['ui_wheel'])
        self.assertEqual('Överkant', s['ui_top'])
        self.assertEqual('Rund', s['ui_round'])
        self.assertIn('Jämna ut frihandsdrag', s['ui_smooth_freehand_strokes'])
        self.assertIn('Överlappning är tillåten här.', s['ui_assembly_position_help'])
        self.assertIn('Övriga bilder behåller sina nuvarande positioner.', s['ui_assembly_position_help'])
        self.assertIn('Bilder som importerats senare ritas ovanpå.', s['ui_assembly_position_help'])
        self.assertIn('Beskärningar och storlekar förblir oförändrade.', s['ui_assembly_position_help'])
        self.assertIn('Bilden importerades inte.', s['gallery_image_component_unavailable'])
        self.assertIn('kan minska filstorleken utan att ändra bildpunkterna', s['formats22_tiff_description'])
        self.assertIn('antiAlias=false; strokeDashArray=none; background=#FFFFFF.', s['commons_import_svg_changes'])
        self.assertIn('background=#FFFFFF', s['commons_import_raster_changes'])

    def test_assembly_help_preserves_separate_modes_and_actual_control_labels(self):
        s = {k: v.strip('"') for k, v in self.strings.items()}
        value = s['ui_add_up_to_20_images_with_android_s']
        paragraphs = value.split(r'\n\n')
        self.assertEqual(8, len(paragraphs))
        self.assertIn('Vid fästning börjar den första bilden i origo och överlappningar avvisas.', paragraphs[2])
        self.assertIn('räknat från noll', paragraphs[3])
        self.assertIn('Övriga bilder behåller sina positioner och överlappningar är tillåtna.', paragraphs[3])
        self.assertIn('kan flyttas för att fylla luckan', paragraphs[5])
        for key in ('ui_assembly_exact_position', 'ui_crop_image', 'ui_batch_crop', 'ui_reset_crop',
                    'ui_same_width', 'ui_same_height', 'ui_smallest', 'ui_largest',
                    'ui_restore_original_sizes', 'ui_unplace', 'ui_remove', 'ui_show_all',
                    'ui_save_png', 'ui_edit_in_paint', 'ui_menu_file', 'ui_about_credits23'):
            self.assertIn(s[key], value, key)

    def test_curve_hint_describes_early_completion_not_an_attachment(self):
        hint = self.strings['ui_drag_a_line_then_drag_twice_to_set']
        self.assertIn(self.strings['ui_finish_curve'], hint)
        self.assertIn('slutföra kurvan innan båda böjarna har ställts in.', hint)
        self.assertNotIn('fästa', hint)


    def _manual_previous(self, tag):
        return {'value': self.manual_data['previous_source'], 'attributes': MANUAL_ATTRIBUTES} if tag == 'default' else None

    def _manual_node(self, tag):
        return self.manual_roots[tag].find(f"./string[@name='{MANUAL_KEY}']")

    def test_complete_values_and_explicit_historical_hold_disposition(self):
        for tag in self.manual_roots:
            nodes = self.manual_roots[tag].findall(f"./*[@name='{MANUAL_KEY}']")
            self.assertEqual(1, len(nodes))
            require_manual_successor(tag, MANUAL_KEY, nodes[0], self._manual_previous(tag))
            value = nodes[0].text
            self.assertEqual(10, len(value.split(r'\n\n')))
            self.assertEqual(18, value.count(r'\n'))
            self.assertEqual({}, catalogues.placeholders(value))
            self.assertEqual([], catalogues.android_string_errors(value))
            self.assertEqual([], catalogues.format_string_errors(value, False))
        historical = fixture('swedish_extended_wording.json')
        self.assertIn(MANUAL_KEY, historical['held_missing'])
        self.assertEqual(['ui_main23'], historical['present_held'])
        self.assertEqual('Huvud', self.manual_roots['sv'].find("./string[@name='ui_main23']").text)
        self.assertIsNone(self.manual_data['previous_swedish'])

    def test_exact_identity_predecessor_required(self):
        for tag,key,old in [('en-US',MANUAL_KEY,None), ('sv','ui_help23',None),
                            ('sv',MANUAL_KEY,{'value':'forged','attributes':MANUAL_ATTRIBUTES}),
                            ('default',MANUAL_KEY,None), ('default',MANUAL_KEY,{'value':self.manual_data['source'],'attributes':MANUAL_ATTRIBUTES})]:
            with self.subTest(tag=tag,key=key), self.assertRaises(ValueError):
                require_manual_successor(tag,key,self._manual_node('sv'),old)

    def test_target_corruption_missing_markup_attributes_tail_and_old_wording_rejected(self):
        for tag in self.manual_roots:
            for mode in ('missing','type','text','placeholder','attributes','child','tail','old'):
                node=deepcopy(self._manual_node(tag))
                if mode=='missing': node=None
                elif mode=='type': node.tag='plurals'
                elif mode=='text': node.text=node.text[:-1]
                elif mode=='placeholder': node.text+='%1$s'
                elif mode=='attributes': node.set('formatted','true')
                elif mode=='child': ET.SubElement(node,'b')
                elif mode=='tail': node.tail='unexpected'
                else: node.text=self.manual_data['previous_source']
                with self.subTest(tag=tag,mode=mode), self.assertRaises(ValueError):
                    require_manual_successor(tag,MANUAL_KEY,node,self._manual_previous(tag))

    def test_source_mutations_cannot_bind_swedish_to_wrong_or_duplicate_source(self):
        for mode in ('missing','duplicate','type','text','attributes','child','tail'):
            root=deepcopy(self.manual_roots['default']);node=root.find(f"./string[@name='{MANUAL_KEY}']")
            if mode=='missing': root.remove(node)
            elif mode=='duplicate': root.append(deepcopy(node))
            elif mode=='type': node.tag='plurals'
            elif mode=='text': node.text=self.manual_data['previous_source']
            elif mode=='attributes': node.set('formatted','true')
            elif mode=='child': ET.SubElement(node,'b')
            else: node.tail='unexpected'
            with patch.object(ET,'parse',return_value=ET.ElementTree(root)):
                with self.subTest(mode=mode), self.assertRaises(ValueError):
                    require_manual_successor('sv',MANUAL_KEY,self._manual_node('sv'),None)

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
            paragraphs=self._manual_node(tag).text.split(r'\n\n')
            for index, parts in checks.items():
                for part in parts:
                    with self.subTest(tag=tag,paragraph=index+1,part=part): self.assertIn(part,paragraphs[index])
            self.assertNotIn('one undoable selection edit',paragraphs[4])
            self.assertNotIn('fixed at the lower left',paragraphs[1])
        self.assertIn('fäller ihop eller fäller ut panelen.',self._manual_node('sv').text)

    def test_fixture_scope_is_finite(self):
        for field,value in [('key','ui_help23'),('schema_version',True),('previous_swedish','forged'),
                            ('attributes',{'name':MANUAL_KEY}),('source',self.manual_data['previous_source'])]:
            data=deepcopy(self.manual_data);data[field]=value
            with patch(__name__+'.fixture',return_value=data), self.subTest(field=field), self.assertRaises(ValueError):
                manual_decision()


if __name__ == '__main__':
    unittest.main()
