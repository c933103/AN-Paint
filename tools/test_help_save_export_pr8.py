"""Bounded save/export and conditional-movement wording regressions.

Compare complete reviewed paragraphs, including their subjects and negative
clauses, rather than accepting keywords found elsewhere in a long help entry.
The three main-help changes concern the retained, currently dormant resource;
assembly help is active. These are wording/structure and source-route checks,
not runtime, fluency, whole-catalogue or Mongolian parent-gate acceptance.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import current_localization_contracts as contracts
import translation_catalogues as catalogues
from test_assembly_help_pr8 import code_locations

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
MANUAL = 'ui_the_arrow_on_the_left_directly_below_the'
ASSEMBLY = 'ui_add_up_to_20_images_with_android_s'
SAVE_ROLES = (
    'context', 'save_as', 'save', 'export_subject', 'join', 'share_subject',
    'copy', 'preserve_destination', 'preserve_saved', 'share_after', 'star',
    'source_protection',
)
CAPTIONS = {
    'save_as': 'save20_title', 'save': 'ui_save',
    'export_subject': 'ui_export_as23', 'share_subject': 'ui_save_and_share',
    'share_after': 'ui_save_and_share',
}
DIRECTORIES = ('values-b+bo', 'values-b+dz', 'values-b+mn+Mong')


def read_xml(directory):
    return (RES / directory / 'strings.xml').read_text(encoding='utf-8')


def one_resource(xml, key):
    nodes = ET.fromstring(xml).findall(f"./string[@name='{key}']")
    if len(nodes) != 1:
        raise ValueError(f'{key}: expected exactly one resource, found {len(nodes)}')
    return nodes[0]


def joined_parts(contract):
    return ''.join(part['text'] for part in contract['parts'])


def require_help_paragraph(xml, key, index, contract):
    """Keep exact Unicode/Android escapes; no normalization or keyword fallback."""
    node = one_resource(xml, key)
    attributes = {'name': key}
    if key == MANUAL:
        attributes['formatted'] = 'false'
    if node.attrib != attributes or len(node) != 0:
        raise ValueError(f'{key}: unexpected attributes or child markup')
    value = node.text or ''
    paragraphs = value.split(r'\n\n')
    if len(paragraphs) != contract['paragraph_count']:
        raise ValueError(f'{key}: paragraph count differs')
    if paragraphs[index] != joined_parts(contract):
        raise ValueError(f'{key}: complete paragraph wording differs')
    errors = (catalogues.android_string_errors(value) +
              catalogues.format_string_errors(value, formatted=key != MANUAL))
    if errors or '\n' in value or '\r' in value or '\ufffd' in value:
        raise ValueError(f'{key}: invalid Android text/escape structure: {errors}')
    return value


def xml_with_value(key, value):
    """Build mutation inputs as XML, retaining the full surrounding help entry."""
    root = ET.Element('resources')
    node = ET.SubElement(root, 'string', name=key)
    if key == MANUAL:
        node.set('formatted', 'false')
    node.text = value
    return ET.tostring(root, encoding='unicode')


class HelpSaveExportPr8Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = contracts.fixture('help_save_export_pr8.json')
        cls.xmls = {directory: read_xml(directory) for directory in DIRECTORIES}

    def test_fixture_is_bounded_and_has_each_independent_semantic_part(self):
        self.assertEqual(1, self.fixture['schema_version'])
        self.assertEqual(set(DIRECTORIES), set(self.fixture['save']))
        for directory, contract in self.fixture['save'].items():
            with self.subTest(directory=directory):
                self.assertEqual(SAVE_ROLES, tuple(p['role'] for p in contract['parts']))
                self.assertTrue(all(p['text'] for p in contract['parts']))
        assembly = self.fixture['assembly']
        self.assertEqual('values-b+mn+Mong', assembly['directory'])
        self.assertEqual(('context', 'may_move', 'overlap_rejection'),
                         tuple(p['role'] for p in assembly['parts']))

    def test_complete_source_save_paragraph_retains_the_reviewed_meaning(self):
        source = one_resource(read_xml('values'), MANUAL).text
        self.assertEqual(self.fixture['english_save_paragraph'], source.split(r'\n\n')[3])

    def test_complete_local_save_paragraphs_include_both_routes_and_guarantees(self):
        for directory, contract in self.fixture['save'].items():
            with self.subTest(directory=directory):
                require_help_paragraph(self.xmls[directory], MANUAL, 3, contract)

    def test_all_four_menu_captions_match_their_correct_scoped_sentences(self):
        for directory, contract in self.fixture['save'].items():
            parts = {p['role']: p['text'] for p in contract['parts']}
            for role, key in CAPTIONS.items():
                with self.subTest(directory=directory, role=role):
                    label = one_resource(self.xmls[directory], key).text.rstrip('….།༎')
                    self.assertIn('«' + label + '»', parts[role])

    def test_complete_mongolian_placement_paragraph_keeps_movement_conditional(self):
        contract = self.fixture['assembly']
        require_help_paragraph(self.xmls[contract['directory']], ASSEMBLY, 2, contract)

    def test_full_entry_structure_and_placeholders_match_the_source(self):
        for directory in DIRECTORIES:
            keys = (MANUAL, ASSEMBLY) if directory == 'values-b+mn+Mong' else (MANUAL,)
            for key in keys:
                with self.subTest(directory=directory, key=key):
                    local = one_resource(self.xmls[directory], key).text
                    source = one_resource(read_xml('values'), key).text
                    self.assertEqual(catalogues.placeholders(source), catalogues.placeholders(local))
                    contract = (self.fixture['save'][directory] if key == MANUAL
                                else self.fixture['assembly'])
                    self.assertEqual(2 * (contract['paragraph_count'] - 1), local.count(r'\n'))
                    require_help_paragraph(self.xmls[directory], key, 3 if key == MANUAL else 2, contract)

    def test_each_save_clause_omission_fails_even_with_other_help_text_intact(self):
        # Independently remove both compound subjects, each negative guarantee,
        # each save route, copy action, sharing order and drawing-based star.
        # No localized-language classifier is implied by these fixed regressions.
        for directory, contract in self.fixture['save'].items():
            value = one_resource(self.xmls[directory], MANUAL).text
            parts = value.split(r'\n\n')
            parts[3] = joined_parts(contract)
            valid = r'\n\n'.join(parts)
            require_help_paragraph(xml_with_value(MANUAL, valid), MANUAL, 3, contract)
            for piece in contract['parts']:
                with self.subTest(directory=directory, omitted=piece['role']):
                    changed = [p for p in contract['parts'] if p['role'] != piece['role']]
                    mutated = list(parts)
                    mutated[3] = ''.join(p['text'] for p in changed)
                    with self.assertRaisesRegex(ValueError, 'complete paragraph wording differs'):
                        require_help_paragraph(xml_with_value(MANUAL, r'\n\n'.join(mutated)),
                                               MANUAL, 3, contract)

    def test_guarantees_moved_outside_the_copy_paragraph_do_not_satisfy_it(self):
        for directory, contract in self.fixture['save'].items():
            parts = one_resource(self.xmls[directory], MANUAL).text.split(r'\n\n')
            parts[3] = joined_parts(contract)
            for role in ('preserve_destination', 'preserve_saved'):
                with self.subTest(directory=directory, displaced=role):
                    piece = next(p['text'] for p in contract['parts'] if p['role'] == role)
                    mutated = list(parts)
                    mutated[3] = mutated[3].replace(piece, '', 1)
                    mutated[0] += ' ' + piece
                    with self.assertRaisesRegex(ValueError, 'complete paragraph wording differs'):
                        require_help_paragraph(xml_with_value(MANUAL, r'\n\n'.join(mutated)),
                                               MANUAL, 3, contract)

    def test_assembly_omission_and_unconditional_movement_mutations_fail(self):
        contract = self.fixture['assembly']
        parts = one_resource(self.xmls[contract['directory']], ASSEMBLY).text.split(r'\n\n')
        parts[2] = joined_parts(contract)
        sentence = next(p['text'] for p in contract['parts'] if p['role'] == 'may_move')
        for name, replacement in (('omitted', ''), ('unconditional', contract['unconditional_movement'])):
            with self.subTest(mutation=name):
                mutated = list(parts)
                mutated[2] = mutated[2].replace(sentence, replacement, 1)
                with self.assertRaisesRegex(ValueError, 'complete paragraph wording differs'):
                    require_help_paragraph(xml_with_value(ASSEMBLY, r'\n\n'.join(mutated)),
                                           ASSEMBLY, 2, contract)

    def test_duplicate_missing_and_bad_attribute_resources_fail(self):
        contract = self.fixture['save']['values-b+bo']
        value = one_resource(self.xmls['values-b+bo'], MANUAL).text
        paragraphs = value.split(r'\n\n')
        paragraphs[3] = joined_parts(contract)
        root = ET.fromstring(xml_with_value(MANUAL, r'\n\n'.join(paragraphs)))
        valid = ET.tostring(root, encoding='unicode')
        require_help_paragraph(valid, MANUAL, 3, contract)
        for name in ('missing', 'duplicate', 'attribute', 'child'):
            with self.subTest(mutation=name):
                mutated = ET.fromstring(valid)
                if name == 'missing':
                    mutated.remove(mutated[0])
                elif name == 'duplicate':
                    mutated.append(ET.fromstring(ET.tostring(mutated[0], encoding='unicode')))
                elif name == 'attribute':
                    mutated[0].set('formatted', 'true')
                else:
                    ET.SubElement(mutated[0], 'b').text = 'unexpected markup'
                with self.assertRaises(ValueError):
                    require_help_paragraph(ET.tostring(mutated, encoding='unicode'), MANUAL, 3, contract)

    def test_active_main_help_and_assembly_keep_their_distinct_resource_routes(self):
        classic = (CLASSIC / 'ClassicPaintActivity.kt').read_text(encoding='utf-8')
        assembly = (CLASSIC / 'AssemblyActivity.kt').read_text(encoding='utf-8')
        self.assertTrue(code_locations(classic, 'private fun showHelp() = message(ui(R.string.ui_help23))'))
        self.assertTrue(code_locations(assembly, 'private fun showHelp() = message(ui(R.string.' + ASSEMBLY + '))'))
        # Prevent attributing this retained-resource correction to displayed main Help.
        for path in CLASSIC.glob('*.kt'):
            self.assertFalse(code_locations(path.read_text(encoding='utf-8'), 'R.string.' + MANUAL), path.name)


if __name__ == '__main__':
    unittest.main()
