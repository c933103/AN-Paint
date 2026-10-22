"""Complete bounded Korean wording contracts, with corruption sensitivity.

The fixture contains the full independently reviewed values, not a generator.
These source checks do not certify native fluency, rendered layout, or any
withdrawn catalogue review. Model behavior stays covered by AssemblyModelTest.
"""
from collections import Counter
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import current_localization_contracts as contracts
import translation_catalogues as catalogues
from test_assembly_help_pr8 import code_locations, kotlin_block

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
CLASSIC = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic'
KP = 'values-b+ko+KP'
DIRECTORIES = (KP, 'values-b+ko+KR', 'values-b+ko+Kore+KR')
MANUAL = 'ui_the_arrow_on_the_left_directly_below_the'
ASSEMBLY = 'ui_add_up_to_20_images_with_android_s'
CROP = 'ui_crop_preview_images'
PARTICLE = 'ui_d_d_pixels_2f_mp_exceeds_the_current'
KP_KEYS = {
    PARTICLE, 'gallery_copy_credit', 'ui_image_credits',
    'ui_no_gallery_images_have_been_inserted', 'gallery_description',
    'gallery_edit_credits', 'gallery_credit_copied', 'gallery_credit_saved',
    'legacy_credits_title', 'legacy_credits_hint', 'legacy_credits_add',
    'legacy_credits_save_text', 'legacy_credits_existing', 'legacy_credits_added',
    'legacy_credits_unreadable', 'gallery_credit_too_large',
    'gallery_credit_could_not_save', 'commons_credit_copy_failed',
    'commons_credit_copy_failed_reason', 'commons_credit_copy_out_of_memory',
    'ui_catrobat_s_own_artwork_uses_cc_by_sa', MANUAL,
    'ui_irasutoya_help34', 'ui_openclipart_help34', ASSEMBLY, CROP,
}
ACKNOWLEDGEMENTS = {
    'ui_about_credits23', 'ui_credits_terms', 'ui_icons_fonts_artwork_credits',
    'ui_open_source_credits_and_notices', 'ui_gimp_translations31', 'ui_help23',
}


def resource(xml, entry):
    tag = 'plurals' if entry['quantity'] else 'string'
    nodes = ET.fromstring(xml).findall(f"./{tag}[@name='{entry['key']}']")
    if len(nodes) != 1:
        raise ValueError('Expected one resource: ' + entry['key'])
    parent = nodes[0]
    if parent.attrib != entry['attributes']:
        raise ValueError('Resource attributes differ')
    if not entry['quantity']:
        node = parent
    else:
        if len(parent) != 1 or parent[0].tag != 'item':
            raise ValueError('Expected only the Korean other quantity')
        node = parent[0]
        if node.attrib != {'quantity': 'other'}:
            raise ValueError('Quantity attributes differ')
    if len(node):
        raise ValueError('Unexpected child markup')
    return node.text or ''


def require_value(xml, entry):
    value = resource(xml, entry)
    if value != entry['value']:
        raise ValueError('Complete accepted value differs')
    errors = (catalogues.android_string_errors(value) +
              catalogues.format_string_errors(value, entry['attributes'].get('formatted') != 'false'))
    if errors or any(c in value for c in ('\n', '\r', '\ufffd')):
        raise ValueError('Invalid Android text: ' + str(errors))
    return value


def require_assembly_paragraphs(english, value, directory):
    """Preserve separate locale review boundaries, including under python -O."""
    counts = {KP: 8, 'values-b+ko+KR': 7, 'values-b+ko+Kore+KR': 7}
    if directory not in counts:
        raise ValueError('Unexpected Korean assembly locale')
    for label, text, count in (('English', english, 8), (directory, value, counts[directory])):
        paragraphs = text.split(r'\n\n')
        if (len(paragraphs) != count or not all(paragraphs)
                or text.count(r'\n') != 2 * (count - 1)
                or '\n' in text or '\r' in text):
            raise ValueError('Assembly paragraph structure differs: ' + label)


def xml_with_value(entry, value):
    root = ET.Element('resources')
    node = ET.SubElement(root, 'plurals' if entry['quantity'] else 'string', entry['attributes'])
    if entry['quantity']:
        node = ET.SubElement(node, 'item', quantity=entry['quantity'])
    node.text = value
    return ET.tostring(root, encoding='unicode')


class KoreanImageAttributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = contracts.fixture('korean_image_attribution.json')
        cls.entries = cls.fixture['entries']
        cls.xml = {d: (RES / d / 'strings.xml').read_text(encoding='utf-8') for d in DIRECTORIES}
        cls.kp = {node.get('name'): node.text or '' for node in ET.fromstring(cls.xml[KP])
                  if node.tag == 'string'}

    def test_exact_scope_has_no_missing_duplicate_or_extra_entries(self):
        expected = {(KP, key, 'other' if key == CROP else None) for key in KP_KEYS}
        expected |= {(d, key, 'other' if key == CROP else None)
                     for d in DIRECTORIES[1:] for key in (ASSEMBLY, CROP)}
        self.assertEqual(1, self.fixture['schema_version'])
        self.assertEqual(Counter({identity: 1 for identity in expected}),
                         Counter((e['directory'], e['key'], e['quantity']) for e in self.entries))
        self.assertEqual(ACKNOWLEDGEMENTS, set(self.fixture['unchanged_acknowledgements']))

    def test_all_thirty_complete_recorded_values_and_attributes(self):
        for entry in self.entries:
            with self.subTest(directory=entry['directory'], key=entry['key']):
                require_value(self.xml[entry['directory']], entry)

    def test_source_format_arguments_keep_order_multiplicity_and_newlines(self):
        source = ET.parse(RES / 'values/strings.xml').getroot()
        for entry in self.entries:
            path = (f"./plurals[@name='{entry['key']}']/item[@quantity='other']"
                    if entry['quantity'] else f"./string[@name='{entry['key']}']")
            english = source.find(path).text
            value = require_value(self.xml[entry['directory']], entry)
            with self.subTest(directory=entry['directory'], key=entry['key']):
                self.assertEqual(catalogues.placeholders(english), catalogues.placeholders(value))
                if entry['key'] == ASSEMBLY:
                    # Only ko-KP Help is aligned in this isolated proposal.
                    # Ordinary ko-KR and mixed-script ko-Kore-KR retain this
                    # base's seven paragraphs; sibling branches stay separate.
                    require_assembly_paragraphs(english, value, entry['directory'])
                else:
                    self.assertEqual(english.count(r'\n'), value.count(r'\n'))

    def test_assembly_paragraph_contract_rejects_cross_locale_count_drift(self):
        english = ET.parse(RES / 'values/strings.xml').find(f"./string[@name='{ASSEMBLY}']").text
        for entry in self.entries:
            if entry['key'] != ASSEMBLY:
                continue
            value, directory = entry['value'], entry['directory']
            require_assembly_paragraphs(english, value, directory)
            paragraphs = value.split(r'\n\n')
            mutations = (
                r'\n\n'.join(paragraphs[:-1]),
                value + r'\n\n' + paragraphs[-1],
                value.replace(r'\n\n', r'\n', 1),
                value.replace(r'\n\n', r'\n\n\n', 1),
                value.replace(r'\n', '\n', 1),
                value + '\r',
                r'\n\n' + r'\n\n'.join(paragraphs[1:]),
            )
            for mutated in mutations:
                with self.subTest(directory=directory, mutation=mutated), self.assertRaises(ValueError):
                    require_assembly_paragraphs(english, mutated, directory)
            with self.subTest(directory=directory, mutation='stale-English'), self.assertRaises(ValueError):
                require_assembly_paragraphs(r'\n\n'.join(english.split(r'\n\n')[:-1]), value, directory)
        with self.assertRaises(ValueError):
            require_assembly_paragraphs(english, english, 'values-ko')

    def test_north_korean_complete_help_rejects_sentence_and_paragraph_loss(self):
        entry = next(e for e in self.entries if e['directory'] == KP
                     and e['key'] == ASSEMBLY)
        value = require_value(self.xml[entry['directory']], entry)
        paragraphs = value.split(r'\n\n')
        self.assertEqual(8, len(paragraphs))
        sentences = [s + '.' for p in paragraphs for s in p[:-1].split('. ')]
        self.assertEqual(34, len(sentences))
        for sentence in sentences:
            self.assertEqual(1, value.count(sentence))
            for replacement in ('', sentence + ' ' + sentence):
                with self.subTest(sentence=sentence, replacement=replacement), self.assertRaises(ValueError):
                    require_value(xml_with_value(entry, value.replace(sentence, replacement, 1)), entry)
        for index in range(8):
            for kind in ('omit', 'duplicate'):
                changed = list(paragraphs)
                if kind == 'omit': del changed[index]
                else: changed.insert(index, changed[index])
                with self.subTest(paragraph=index, mutation=kind), self.assertRaises(ValueError):
                    require_value(xml_with_value(entry, r'\n\n'.join(changed)), entry)
        for index in range(7):
            changed = list(paragraphs)
            changed[index], changed[index + 1] = changed[index + 1], changed[index]
            with self.subTest(paragraph=index, mutation='reorder'), self.assertRaises(ValueError):
                require_value(xml_with_value(entry, r'\n\n'.join(changed)), entry)

    def test_broad_acknowledgements_and_active_main_help_stay_unchanged(self):
        for key, expected in self.fixture['unchanged_acknowledgements'].items():
            with self.subTest(key=key):
                contracts.require_string(self.xml[KP], key, expected,
                                         {'attributes': {'name': key, **({'formatted': 'false'}
                                                                        if key == 'ui_about_credits23' else {})}})
        self.assertEqual('프로그람 정보, 리용허가 및 감사의 말', self.kp['ui_about_credits23'])
        final_paragraph = self.kp[ASSEMBLY].split(r'\n\n')[-1]
        self.assertIn(self.kp['ui_about_credits23'], final_paragraph)
        self.assertIn('자산 감사의 말', final_paragraph)

    def test_dependent_routes_and_copy_edit_captions_match_actual_labels(self):
        parts = [self.kp[k] for k in ('ui_menu_file', 'ui_about_credits23', 'ui_image_credits')]
        for key, separator in (
            ('gallery_description', ' → '),
            ('ui_catrobat_s_own_artwork_uses_cc_by_sa', ' > '),
            (MANUAL, ' > '), ('ui_irasutoya_help34', ' → '),
            ('ui_openclipart_help34', ' → '),
        ):
            with self.subTest(key=key):
                self.assertEqual(1, self.kp[key].count(separator.join(parts)))
        for key in ('gallery_copy_credit', 'gallery_edit_credits'):
            self.assertEqual(1, self.kp['gallery_description'].count(self.kp[key]))
        self.assertEqual('화상 저작자·출처 정보', self.kp['ui_image_credits'])
        self.assertEqual('저작자·출처 정보 복사', self.kp['gallery_copy_credit'])
        self.assertEqual('저작자·출처 정보 편집', self.kp['gallery_edit_credits'])

    def test_each_entry_rejects_stale_particle_attribution_or_unconditional_movement(self):
        for entry in self.entries:
            value, key = entry['value'], entry['key']
            if key == PARTICLE:
                stale = value.replace('MP)는', 'MP)은', 1)
            elif key == ASSEMBLY:
                if entry['directory'] == KP:
                    conditional = '기준이 되는 화상을 자르면 거기에 련결된 화상이 이동할수 있습니다.'
                    self.assertEqual(1, value.count(conditional))
                    stale = value.replace(conditional, conditional.replace('이동할수 있습니다.', '이동합니다.'), 1)
                else:
                    stale = value.replace('이동할 수 있습니다.', '이동합니다.', 1)
            elif key == CROP:
                stale = value.replace('조정될 수 있습니다.', '조정됩니다.', 1)
            else:
                stale = value.replace('저작자·출처 정보', '감사의 말', 1)
            with self.subTest(directory=entry['directory'], key=key):
                self.assertNotEqual(value, stale)
                with self.assertRaisesRegex(ValueError, 'Complete accepted value differs'):
                    require_value(xml_with_value(entry, stale), entry)

    def test_each_entry_rejects_truncation_and_unrelated_clause_corruption(self):
        for entry in self.entries:
            for value in (entry['value'][:-1], entry['value'] + ' 변경됨'):
                with self.subTest(directory=entry['directory'], key=entry['key'], value=value[-20:]):
                    with self.assertRaisesRegex(ValueError, 'Complete accepted value differs'):
                        require_value(xml_with_value(entry, value), entry)

    def test_conditional_crop_clause_cannot_move_to_an_unrelated_paragraph(self):
        for entry in self.entries:
            if entry['key'] != ASSEMBLY:
                continue
            paragraphs = entry['value'].split(r'\n\n')
            sentences = paragraphs[2].split('. ')
            if entry['directory'] == KP:
                conditional = '기준이 되는 화상을 자르면 거기에 련결된 화상이 이동할수 있습니다'
                self.assertEqual(1, sentences.count(conditional))
            else:
                conditional = next(s for s in sentences if '이동할 수 있습니다' in s)
            paragraphs[2] = paragraphs[2].replace(conditional + '. ', '', 1)
            paragraphs[0] += ' ' + conditional + '.'
            with self.subTest(directory=entry['directory']):
                with self.assertRaisesRegex(ValueError, 'Complete accepted value differs'):
                    require_value(xml_with_value(entry, r'\n\n'.join(paragraphs)), entry)

    def test_missing_duplicate_attributes_quantity_and_child_markup_fail(self):
        for entry in self.entries:
            valid = xml_with_value(entry, entry['value'])
            require_value(valid, entry)
            cases = ['missing', 'duplicate', 'attribute', 'child']
            if entry['quantity']:
                cases += ['quantity', 'duplicate_quantity']
            for case in cases:
                root = ET.fromstring(valid)
                node = root[0][0] if entry['quantity'] else root[0]
                if case == 'missing':
                    root.remove(root[0])
                elif case == 'duplicate':
                    root.append(ET.fromstring(ET.tostring(root[0])))
                elif case == 'attribute':
                    root[0].set('translatable', 'false')
                elif case == 'child':
                    ET.SubElement(node, 'b').text = 'markup'
                elif case == 'quantity':
                    node.set('quantity', 'one')
                else:
                    root[0].append(ET.fromstring(ET.tostring(node)))
                with self.subTest(directory=entry['directory'], key=entry['key'], mutation=case):
                    with self.assertRaises(ValueError):
                        require_value(ET.tostring(root, encoding='unicode'), entry)

    def test_placeholders_unicode_and_android_escape_mutations_fail(self):
        for entry in self.entries:
            value = entry['value']
            mutations = []
            if '%1$' in value:
                mutations.append(value.replace('%1$', '%2$', 1))
            if r'\n' in value:
                mutations.append(value.replace(r'\n', '\n', 1))
            if '·' in value:
                mutations.append(value.replace('·', '-', 1))
            if '連結' in value:
                mutations.append(value.replace('連結', '연결', 1))
            for mutated in mutations:
                with self.subTest(directory=entry['directory'], key=entry['key']):
                    with self.assertRaises(ValueError):
                        require_value(xml_with_value(entry, mutated), entry)

    def test_production_parent_submenu_and_caption_routes(self):
        classic = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
        about = kotlin_block(classic, 'private fun showAboutOptions() {')
        for source, fragment in (
            (classic, 'ui(R.string.ui_about_credits23) to {showAboutOptions()}'),
            (about, 'ui(R.string.ui_image_credits) to {showImageCredits()}'),
            (about, 'setScrollableTitle(ui(R.string.ui_about_credits23))'),
            ((CLASSIC / 'GalleryCredits.kt').read_text(),
             'EditorDialogBuilder(activity).setTitle(ui(R.string.ui_image_credits))'),
            ((CLASSIC / 'GalleryCredits.kt').read_text(),
             '.setNegativeButton(ui(R.string.gallery_copy_credit),null)'),
            ((CLASSIC / 'MediaGalleryActivity.kt').read_text(),
             'action(ui(R.string.gallery_edit_credits),"gallery_edit_credits") {showCreditEditor()}'),
            ((CLASSIC / 'MediaGalleryActivity.kt').read_text(),
             'IllustrationPage.script(provider,ui(R.string.gallery_use_image),ui(R.string.gallery_copy_credit))'),
        ):
            with self.subTest(fragment=fragment):
                self.assertTrue(code_locations(source, fragment))

    def test_crop_and_help_source_routes_keep_active_and_dormant_text_distinct(self):
        assembly = (CLASSIC / 'AssemblyActivity.kt').read_text()
        crop = (CLASSIC / 'ImageCropDialog.kt').read_text()
        self.assertTrue(code_locations(assembly, 'private fun showHelp() = message(ui(R.string.' + ASSEMBLY + '))'))
        guarded = ('status.text = uiQuantity(activity.resources,'
                   'R.plurals.ui_crop_preview_images,count,crop.width(),crop.height(),count)')
        def require_guarded(source): self.assertTrue(code_locations(source, guarded))
        require_guarded(crop)
        with self.assertRaises(AssertionError):
            require_guarded(crop.replace('uiQuantity(activity.resources,', 'activity.resources.getQuantityString('))
        classic = (CLASSIC / 'ClassicPaintActivity.kt').read_text()
        self.assertTrue(code_locations(classic, 'private fun showHelp() = message(ui(R.string.ui_help23))'))
        for path in CLASSIC.glob('*.kt'):
            self.assertFalse(code_locations(path.read_text(), 'R.string.' + MANUAL), path.name)


if __name__ == '__main__':
    unittest.main()
