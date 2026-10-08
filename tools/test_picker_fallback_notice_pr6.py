"""Guard the three PR #6 picker notices against losing source obligations.

Finding: https://github.com/c933103/AN-Paint/pull/6#discussion_r4215259754
Inspected source: d959a0b9a580fe71ce7c9ce99454335f86f5a4d5.
AppLanguage.showPicker uses this resource as its custom title, replacing the
ordinary title. Keep the local heading, resource-maintenance explanation,
new/untranslated-text English fallback, and existing locale convention.

These bounded literal guards detect the reported omissions. They do not prove
native-language fluency, arbitrary semantic equivalence, Android resolution,
font rendering, or dialog layout. A reviewed paraphrase should update the
relevant clause expectation, not remove its obligation.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
KEY = 'language20_translation_note'
TITLE_KEY = 'language20_app_language'
CASES = {
    'nan-Hant-TW': {
        'maintenance': '翻譯佇 AN Paint 的語言資源內底維護。',
        'fallback': '新的抑是猶未翻譯的文字會用英文顯示。',
        'convention': '這份翻譯用臺灣台語。技術名詞用通行的寫法。',
    },
    'nan-Latn-TW': {
        'maintenance': 'Hoan-e̍k tī AN Paint ê gí-giân chu-goân lāi-té ûi-hō͘.',
        'fallback': 'Sin ê ia̍h-sī iáu-bōe hoan-e̍k ê bûn-jī ē ēng Eng-bûn hián-sī.',
        'convention': 'Chit hūn hoan-e̍k ēng Tâi-oân Tâi-gí, siá Pe̍h-ōe-jī. '
                      'Ki-su̍t bêng-sû ēng thong-hêng ê siá-hoat.',
    },
    'wuu-Hans': {
        'maintenance': '翻译辣 AN Paint 个语言资源里向维护。',
        'fallback': '新个或者还呒没翻译个文字会用英文显示。',
        'convention': '搿份翻译用上海闲话。技术名词照通行个写法。',
    },
}


def strings(folder):
    nodes = ET.parse(RES / folder / 'strings.xml').getroot()
    for key in (KEY, TITLE_KEY):
        if sum(node.tag == 'string' and node.get('name') == key for node in nodes) != 1:
            raise AssertionError(f'{folder}: expected one canonical {key}')
    return {node.get('name'): ''.join(node.itertext()) for node in nodes}


def local_strings(tag):
    return strings('values-b+' + tag.replace('-', '+'))


class PickerFallbackNoticePr6Tests(unittest.TestCase):
    def test_scope_is_the_three_reported_active_catalogues(self):
        self.assertEqual({'nan-Hant-TW', 'nan-Latn-TW', 'wuu-Hans'}, set(CASES))
        tags = {node.text for node in ET.parse(RES / 'values/app_language_tags.xml').findall('.//item')}
        self.assertLessEqual(set(CASES), tags)

    def test_default_message_still_has_the_reviewed_obligations(self):
        values = strings('values')
        self.assertEqual(
            values[TITLE_KEY] + r'\n\n'
            + 'Translations are maintained in AN Paint’s language resources. '
            + 'New or untranslated text appears in English.',
            values[KEY],
            'Reassess the local notices if the source obligations change.',
        )

    def test_picker_still_uses_the_notice_as_its_custom_title(self):
        source = (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt').read_text()
        picker = source.split('fun showPicker(', 1)[1]
        self.assertIn('text = ui(R.string.language20_translation_note)', picker)
        self.assertIn('.setCustomTitle(note)', picker)


def heading_test(tag):
    def test(self):
        values = local_strings(tag)
        self.assertTrue(values[KEY].startswith(values[TITLE_KEY] + r'\n\n'),
                        tag + ': custom title must start with the actual localized heading')
    return test


def clause_test(tag, field):
    def test(self):
        text = local_strings(tag)[KEY]
        self.assertIn(CASES[tag][field], text, tag + ': missing ' + field + ' obligation')
    return test


def convention_test(tag):
    def test(self):
        text = local_strings(tag)[KEY]
        self.assertTrue(text.endswith(CASES[tag]['convention']),
                        tag + ': retain the existing variety/orthography note at the end')
    return test


def order_test(tag):
    def test(self):
        text = local_strings(tag)[KEY]
        case = CASES[tag]
        positions = [text.find(case[field]) for field in ('maintenance', 'fallback', 'convention')]
        self.assertTrue(all(position >= 0 for position in positions), tag + ': missing clause')
        self.assertLess(positions[0], positions[1])
        self.assertLess(positions[1], positions[2])
    return test


for tag in CASES:
    suffix = tag.replace('-', '_')
    setattr(PickerFallbackNoticePr6Tests, 'test_heading_' + suffix, heading_test(tag))
    setattr(PickerFallbackNoticePr6Tests, 'test_maintenance_' + suffix, clause_test(tag, 'maintenance'))
    setattr(PickerFallbackNoticePr6Tests, 'test_fallback_' + suffix, clause_test(tag, 'fallback'))
    setattr(PickerFallbackNoticePr6Tests, 'test_convention_' + suffix, convention_test(tag))
    setattr(PickerFallbackNoticePr6Tests, 'test_clause_order_' + suffix, order_test(tag))


if __name__ == '__main__':
    unittest.main()
