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
import re
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


def kotlin_tokens(source):
    """Small source-contract lexer, not a Kotlin parser or runtime proof.

    Keep literals atomic and ignore comments/formatting so dead comments, quoted
    code and braces inside strings cannot satisfy or truncate a scoped guard.
    """
    if isinstance(source, tuple):
        return source
    pattern = r'"""[\s\S]*?"""|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|[A-Za-z_]\w*|\d+|[^\s]'
    return tuple(t for t in re.findall(pattern, source)
                 if not t.startswith(("//", "/*")))


def code_locations(source, fragment):
    source, fragment = kotlin_tokens(source), kotlin_tokens(fragment)
    return [i for i in range(len(source) - len(fragment) + 1)
            if source[i:i + len(fragment)] == fragment]


def kotlin_block(source, opening):
    source, opening = kotlin_tokens(source), kotlin_tokens(opening)
    matches = code_locations(source, opening)
    if len(matches) != 1 or opening.count("{") - opening.count("}") != 1:
        raise AssertionError("Expected one scoped Kotlin block: " + " ".join(opening))
    start, depth = matches[0] + len(opening), 1
    for end in range(start, len(source)):
        depth += (source[end] == "{") - (source[end] == "}")
        if depth == 0:
            return source[start:end]
    raise AssertionError("Unclosed Kotlin block")


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

    def assertCode(self, source, fragment):
        self.assertTrue(code_locations(source, fragment), fragment)

    def classic_source(self, name):
        return (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic' / name).read_text()

    def picker(self):
        return kotlin_block(self.classic_source('AppLanguage.kt'),
                            'fun showPicker(activity: Activity, changed: () -> Unit): AlertDialog {')

    def test_picker_still_uses_the_notice_as_its_custom_title(self):
        picker = self.picker()
        note = kotlin_block(picker, 'val note = TextView(activity).apply {')
        self.assertCode(note, 'text = ui(R.string.language20_translation_note)')
        # The same notice replaces the ordinary title on both paths. PR12 adds
        # horizontal scrolling for vertical columns, without replacing the text.
        self.assertEqual(1, len(code_locations(picker, '.setCustomTitle(')))
        self.assertCode(picker, 'return AlertDialog.Builder(activity)'
                        '.setTitle(ui(R.string.language20_app_language))'
                        '.setCustomTitle(if (VerticalText.uiVertical())'
                        'ColumnScrollView(activity).apply { addView(note) } else note)')

    def test_picker_notice_retains_typography_and_vertical_transformation(self):
        note = kotlin_block(self.picker(), 'val note = TextView(activity).apply {')
        self.assertCode(note, 'LocaleTypography.typeface(activity)?.let { typeface = it }'
                        'VerticalUi.caption(this, 128)')
        self.assertCode(note, 'text = ui(R.string.language20_translation_note)')
        self.assertLess(code_locations(note, 'text = ui(R.string.language20_translation_note)')[0],
                        code_locations(note, 'VerticalUi.caption(')[0])

    def test_vertical_notice_caption_keeps_text_and_horizontal_bypass(self):
        caption = kotlin_block(self.classic_source('VerticalUi.kt'),
                               'fun caption(view: TextView, heightDp: Int = 144,'
                               'direction: TextDirection = VerticalText.uiDirection()) {')
        self.assertCode(caption, 'if (direction == TextDirection.HORIZONTAL || view is EditText'
                        '|| view is FlowButton || view is FlowTextView) return')
        self.assertCode(caption, 'VerticalText.uiTypeface(view.context)?.let { view.typeface = it }')
        update = kotlin_block(caption, 'fun update() {')
        self.assertCode(update, 'val value = view.text.toString()')
        self.assertCode(update, 'view.text = SpannableString(value).apply { if (isNotEmpty())'
                        'setSpan(Caption(value, dp(view, heightDp).toFloat(), direction),'
                        '0, length, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE) }')
        self.assertCode(caption, 'override fun afterTextChanged(s: Editable?) = update()')
        self.assertCode(caption, '}); update()')

    def test_vertical_notice_wrapper_scrolls_from_the_first_reading_column(self):
        columns = kotlin_block(self.classic_source('RibbonWidgets.kt'),
                               'internal class ColumnScrollView(context: Context):'
                               'android.widget.HorizontalScrollView(context) {')
        self.assertCode(columns, 'private var positioned = false')
        layout = kotlin_block(columns, 'override fun onLayout(changed: Boolean, left: Int,'
                              'top: Int, right: Int, bottom: Int) {')
        self.assertCode(layout, 'super.onLayout(changed, left, top, right, bottom)')
        first_layout = kotlin_block(layout, 'if (!positioned && childCount > 0 && width > 0) {')
        self.assertCode(first_layout, 'positioned = true')
        self.assertCode(first_layout, 'if (VerticalText.uiDirection() == TextDirection.VERTICAL_RL)'
                        'scrollTo((getChildAt(0).width - width + paddingLeft + paddingRight)'
                        '.coerceAtLeast(0), 0)')


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
