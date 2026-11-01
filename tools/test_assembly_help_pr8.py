"""PR #8's two assembly-help regressions in canonical Android XML.

These are source-contract and known-wording guards, not a fluency or rendering
classifier. Native linguistic and Traditional Mongolian layout acceptance stay
separate. No translations JSON is an input to this test.
"""
from functools import lru_cache
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "Paintroid/src/main/res"
CLASSIC = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic"
KEY = "ui_add_up_to_20_images_with_android_s"

@lru_cache(maxsize=None)
def strings(directory):
    return {e.get("name"): "".join(e.itertext()) for e in
            ET.parse(RES / directory / "strings.xml").getroot()
            if e.tag == "string"}

def paragraph(directory, index):
    return re.split(r"\\n\\n|\n\s*\n", strings(directory)[KEY])[index]

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

class AssemblyHelpPr8Tests(unittest.TestCase):
    def assertCode(self, source, fragment):
        self.assertTrue(code_locations(source, fragment), fragment)

    def dialog_wrapper(self):
        return kotlin_block((CLASSIC / "VerticalUi.kt").read_text(),
                            "internal class EditorDialogBuilder(context: Context): AlertDialog.Builder(context) {")

    def test_assembly_help_display_route_uses_the_script_aware_dialog(self):
        # PR8 used a raw platform builder. PR12 intentionally routes through its
        # wrapper, retaining native horizontal dialogs and a vertical shell.
        activity = (CLASSIC / "AssemblyActivity.kt").read_text()
        interface = kotlin_block(activity, "private fun buildInterface() {")
        self.assertCode(interface, 'button(ui(R.string.ui_how_to_use), "assembly_help") { showHelp() }')
        self.assertCode(activity, "private fun showHelp() = message(ui(R.string." + KEY + "))")
        message = kotlin_block(activity, "private fun message(value: String) {")
        self.assertCode(message, "lastError = value")
        self.assertCode(message, 'if (!isDestroyed && !isFinishing) EditorDialogBuilder(this)'
                        '.setTitle("AN Paint").setMessage(value)'
                        '.setPositiveButton(ui(R.string.ui_ok), null).show()')
        self.assertIn('<item name="android:fontFamily">sans</item>', (RES / "values/classic.xml").read_text())

    def test_help_wrapper_retains_native_title_and_message_delegation(self):
        wrapper = self.dialog_wrapper()
        title = kotlin_block(wrapper, "override fun setTitle(title: CharSequence?): AlertDialog.Builder {")
        self.assertCode(title, "heading = title; return super.setTitle(title)")
        message = kotlin_block(wrapper, "override fun setMessage(message: CharSequence?): AlertDialog.Builder {")
        self.assertCode(message, "prose = message; return super.setMessage(message)")
        # The activity's positive action uses the inherited platform setter and
        # show(), which calls create(); a new override needs its own review.
        for method in ("setPositiveButton", "show"):
            self.assertFalse(code_locations(wrapper, "override fun " + method))

    def test_help_wrapper_mounts_only_vertical_and_installs_typography_on_both_paths(self):
        create = kotlin_block(self.dialog_wrapper(), "override fun create(): AlertDialog {")
        self.assertCode(create, "val dialog = super.create()")
        self.assertCode(create, "dialog.window!!.decorView.addOnAttachStateChangeListener(object: View.OnAttachStateChangeListener {")
        attached = kotlin_block(create, "override fun onViewAttachedToWindow(view: View) {")
        self.assertCode(attached, "view.removeOnAttachStateChangeListener(this)")
        post = kotlin_block(attached, "view.post {")
        shown = kotlin_block(post, "if (dialog.isShowing) {")
        self.assertCode(shown, "if (VerticalText.uiVertical(context)) mount(dialog) LocaleTypography.install(dialog.window!!.decorView)")
        self.assertCode(create, "return dialog")

    def test_vertical_help_preserves_body_and_original_positive_action(self):
        mount = kotlin_block(self.dialog_wrapper(), "private fun mount(dialog: AlertDialog) {")
        add = kotlin_block(mount, "fun add(view: View) {")
        self.assertCode(add, "columns.addView(VerticalUi.detach(view),")
        for role in ("heading", "prose"):
            content = kotlin_block(mount, role + "?.let {")
            self.assertCode(content, "add(FlowTextView(context).apply { text = it;")
        self.assertCode(mount, "shell.addView(ColumnScrollView(context).apply {")
        columns = kotlin_block(mount, "ColumnScrollView(context).apply {")
        self.assertCode(columns, "addView(columns)")
        actions = kotlin_block(mount, ".forEach { which ->")
        self.assertCode(mount, "AlertDialog.BUTTON_POSITIVE).forEach { which ->")
        self.assertCode(actions, "dialog.getButton(which)?.takeIf { it.visibility == View.VISIBLE }?.let { button ->")
        button = kotlin_block(actions, "?.let { button ->")
        self.assertCode(button, "VerticalUi.detach(button); VerticalUi.caption(button, 96)")
        self.assertCode(button, "actions.addView(button,")
        self.assertFalse(code_locations(button, "setOnClickListener"))
        self.assertCode(mount, "shell.addView(HorizontalScrollView(context).apply { isFillViewport = true; addView(actions) }")
        self.assertCode(mount, "dialog.setContentView(LimitedScrollView(context,")
        self.assertCode(mount, ".apply { addView(shell) })")

    def test_help_role_selection_keeps_mongolian_vertical_and_default_horizontal(self):
        vertical = (CLASSIC / "VerticalText.kt").read_text()
        direction = kotlin_block(vertical, "fun uiDirection(locale: Locale = Locale.getDefault()): TextDirection = when {")
        self.assertCode(direction, 'locale.script == "Mong" -> TextDirection.VERTICAL_LR')
        self.assertCode(direction, 'locale.language == "lzh" -> TextDirection.VERTICAL_RL')
        self.assertCode(direction, "else -> TextDirection.HORIZONTAL")
        self.assertCode(vertical, "fun uiVertical() = uiDirection() != TextDirection.HORIZONTAL")

    def test_dz_warning_names_the_smallest_output(self):
        # Reuse an already present local term. This guards literal wording,
        # not native fluency or an independent execution of the memory policy.
        prefix = "གྲུབ་འབྲས་ཆུང་ཤོས་ཡང་"
        warning = strings("values-b+dz")["ui_no_resize_fits_decoder_memory"]
        self.assertTrue(warning.startswith("གྲུབ་འབྲས་ཀྱི་ཚད་ཆུང་ཤོས་ཨིན་རུང་"))
        self.assertIn(prefix, strings("values-b+dz")[KEY])
        self.assertNotIn("གྲུབ་འབྲས་ཆུང་ཀུ་རང་ཨིན་རུང་", strings("values-b+dz")[KEY])

    def test_tibetan_crop_caption_keeps_correct_instrumental_particle(self):
        values = strings('values-b+bo')
        # Standalone control ends in shad; embedded noun before a particle does not.
        caption = '«' + values['ui_crop_image'].rstrip('།') + '»'
        self.assertIn(caption + ' ཀྱིས', values[KEY])
        self.assertNotIn(caption + ' ཡིས', values[KEY])

# Only eleven independently identified suffix gaps in the two new spans are
# covered. U+202F follows the legacy convention; actual font shaping is untested.
MONGOLIAN_SUFFIX_BOUNDARIES = (
    (0, "ᠥᠨᠳᠦᠷ»", "ᠦᠨ", 0),
    (0, "ᠲᠣᠬᠢᠷᠠᠭᠤᠯᠭ᠎ᠠ", "ᠶᠢᠨ", 0),
    (0, "ᠵᠢᠷᠤᠭ", "ᠤᠨ", 0),
    (5, "ᠣᠢ", "ᠶᠢᠨ", 0),
    (5, "ᠣᠢ", "ᠶᠢᠨ", 1),
    (5, "ᠬᠢᠵᠠᠭᠠᠷ", "ᠠᠴᠠ", 0),
    (5, "ᠬᠢᠵᠠᠭᠠᠷ", "ᠠᠴᠠ", 1),
    (5, "ᠭᠠᠷᠭᠠᠯᠲᠠ", "ᠶᠢᠨ", 0),
    (5, "ᠦᠶ᠎ᠡ", "ᠳᠦ", 0),
    (5, "ᠰᠣᠩᠭᠣᠭᠤᠷ", "ᠤᠨ", 0),
    (5, "ᠣᠷᠣᠨ", "ᠳᠤ", 0),
)

def make_suffix_separator_test(index, stem, suffix, occurrence):
    def test(self):
        value = paragraph("values-b+mn+Mong", index)
        matches = list(re.finditer(re.escape(stem) + r"([\u0020\u202f\u180e])" + re.escape(suffix), value))
        self.assertGreater(len(matches), occurrence, (stem, suffix, occurrence))
        self.assertEqual("\u202f", matches[occurrence][1])
    return test

for number, (index, stem, suffix, occurrence) in enumerate(MONGOLIAN_SUFFIX_BOUNDARIES, 1):
    setattr(AssemblyHelpPr8Tests, f"test_mn_Mong_suffix_separator_{number:02d}",
            make_suffix_separator_test(index, stem, suffix, occurrence))

if __name__ == "__main__":
    unittest.main()
