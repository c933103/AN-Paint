"""Retained structural picker exceptions and orthography identities, not approved prose."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'Paintroid/src/main/res'
KEY = 'language20_translation_note'
TITLE_KEY = 'language20_app_language'

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

    def assertCode(self, source, fragment):
        self.assertTrue(code_locations(source, fragment), fragment)

    def classic_source(self, name):
        return (ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic' / name).read_text()

    def picker(self):
        return kotlin_block(self.classic_source('AppLanguage.kt'),
                            'fun showPicker(activity: Activity, changed: () -> Unit): AlertDialog {')

    def test_picker_notice_retains_typography_and_vertical_transformation(self):
        # Variety/orthography identity, not a frozen notice paragraph.
        for tag, identity in (('nan-Hant-TW', '臺灣台語'), ('nan-Latn-TW', 'Pe̍h-ōe-jī'), ('wuu-Hans', '上海闲话')):
            self.assertIn(identity, local_strings(tag)[KEY])
        note = kotlin_block(self.picker(), 'val note = TextView(activity).apply {')
        self.assertCode(note, 'LocaleTypography.typeface(activity)?.let { typeface = it }'
                        'VerticalUi.caption(this, 128)')
        self.assertCode(note, 'text = ui(R.string.language20_translation_note)')
        self.assertLess(code_locations(note, 'text = ui(R.string.language20_translation_note)')[0],
                        code_locations(note, 'VerticalUi.caption(')[0])

    def test_vertical_notice_caption_keeps_text_and_horizontal_bypass(self):
        caption = kotlin_block(self.classic_source('VerticalUi.kt'),
                               'fun caption(view: TextView, heightDp: Int = 144,'
                               'direction: TextDirection = VerticalText.uiDirection(view.context)) {')
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
        self.assertCode(first_layout, 'if (VerticalText.uiDirection(context) == TextDirection.VERTICAL_RL)'
                        'scrollTo((getChildAt(0).width - width + paddingLeft + paddingRight)'
                        '.coerceAtLeast(0), 0)')

if __name__ == '__main__':
    unittest.main()
