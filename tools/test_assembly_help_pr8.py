"""PR #8's two assembly-help regressions in canonical Android XML.

These are source-contract and known-wording guards, not a fluency or rendering
classifier. Native linguistic and Traditional Mongolian layout acceptance stay
separate. No translations JSON is an input to this test.
"""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "Paintroid/src/main/res"
CLASSIC = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic"
KEY = "ui_add_up_to_20_images_with_android_s"
CONTRACTS = {
    "values-b+bo": {
        "tag": "bo",
        "paragraph_count": 8,
        "output_index": 6,
        "post_crop": "གཅོད་པ་དང་",
        "post_adjustment": "གིས་ཚད་བསྒྱུར་རྗེས་ཀྱི་པར་རིས་ཀྱི་ཆེ་ཆུང",
        "stale_tray": "གཅོད་ཁུལ་གྱི་ཆེ་ཆུང",
        "offer": "འདྲ་བཤུས་ཆུང་བ་འདེམས་རྒྱུ་ཡོད་ན་དེ་འདེམས།",
        "floor": "གྲུབ་འབྲས་ཧ་ཅང་ཆུང་བ་ཞིག་ལ་དགོས་པའི་ནང་གསོག་ཀྱང་ཚད་དེ་ལས་བརྒལ་ན། ཉེར་སྤྱོད་ཀྱིས་ཆེ་ཆུང་འདེམས་ཆས་ཀྱི་ཚབ་ཏུ་ནང་གསོག་གི་ཉེན་བརྡ་སྟོན།",
        "stale_output": "གྲུབ་འབྲས་དྲན་ཤེས་ཚད་ལས་བརྒལ་ན་འདྲ་བཤུས་ཆུང་བ་འདེམས།",
    },
    "values-b+dz": {
        "tag": "dz",
        "paragraph_count": 8,
        "output_index": 6,
        "post_crop": "བཏོག་ནི་དང་",
        "post_adjustment": "གིས་ཚད་བསྒྱུར་བའི་ཤུལ་གྱི་གཟུགས་བརྙན་གྱི་ཚད",
        "stale_tray": "བཏོག་ཚད",
        "offer": "འདྲ་བཤུས་ཆུང་ཀུ་སེལ་འཐུ་འབད་ནིའི་གདམ་ཁ་བྱིན་པ་ཅིན་སེལ་འཐུ་འབད།",
        "floor": "གྲུབ་འབྲས་ཆུང་ཤོས་ཡང་དྲན་ཚད་ལས་བརྒལ་བ་ཅིན་ གློག་རིམ་གྱིས་ཚད་སེལ་ཆས་ཀྱི་ཚབ་ལུ་དྲན་ཚད་ཀྱི་ཉེན་བརྡ་སྟོནམ་ཨིན།",
        "stale_output": "གྲུབ་འབྲས་དྲན་ཚད་ལས་བརྒལ་བ་ཅིན་འདྲ་བཤུས་ཆུང་ཀུ་སེལ་འཐུ་འབད།",
    },
    "values-b+mn+Cyrl+MN": {
        "tag": "mn-Cyrl-MN",
        "post_crop": "тайралт болон",
        "post_adjustment": "тохируулгын дараах зургийн хэмжээ",
        "stale_tray": "тайралтын хэмжээ",
        "offer": "жижиг гаралтын хуулбар сонгох боломжийг санал болгосон үед сонгоно.",
        "floor": "Маш жижиг гаралт ч хязгаараас давбал апп хэмжээ сонгогчийн оронд санах ойн анхааруулга харуулна.",
        "stale_output": "Гаралт санах ойн хязгаараас давбал жижиг хуулбар сонгоно.",
    },
    "values-b+mn+Mong": {
        "tag": "mn-Mong",
        "post_crop": "ᠣᠭᠲᠣᠯᠣᠯᠲᠠ ᠪᠠ",
        "post_adjustment": "ᠲᠣᠬᠢᠷᠠᠭᠤᠯᠭ᠎ᠠ ᠶᠢᠨ ᠳᠠᠷᠠᠭᠠᠬᠢ ᠵᠢᠷᠤᠭ ᠤᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ",
        "stale_tray": "ᠣᠭᠲᠣᠯᠬᠤ ᠬᠡᠮᠵᠢᠶ᠎ᠡ",
        "offer": "ᠰᠣᠩᠭᠣᠬᠤ ᠪᠣᠯᠣᠮᠵᠢ ᠣᠯᠭᠣᠭᠰᠠᠨ ᠦᠶ᠎ᠡ ᠳᠦ ᠰᠣᠩᠭᠣᠨ᠎ᠠ᠃",
        "floor": "ᠮᠠᠰᠢ ᠪᠠᠭ᠎ᠠ ᠭᠠᠷᠭᠠᠯᠲᠠ ᠴᠤ ᠬᠢᠵᠠᠭᠠᠷ ᠠᠴᠠ ᠬᠡᠲᠦᠷᠡᠪᠡᠯ᠂ ᠠᠫᠫ ᠨᠢ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠰᠣᠩᠭᠣᠭᠤᠷ ᠤᠨ ᠣᠷᠣᠨ ᠳᠤ ᠰᠠᠨᠠᠬᠤ ᠣᠢ ᠶᠢᠨ ᠠᠩᠬᠠᠷᠤᠭᠤᠯᠭ᠎ᠠ ᠬᠠᠷᠠᠭᠤᠯᠤᠨ᠎ᠠ᠃",
        "stale_output": "ᠭᠠᠷᠭᠠᠯᠲᠠ ᠰᠠᠨᠠᠬᠤ ᠣᠢ ᠶᠢᠨ ᠬᠢᠵᠠᠭᠠᠷ ᠠᠴᠠ ᠬᠡᠲᠦᠷᠡᠪᠡᠯ ᠪᠠᠭ᠎ᠠ ᠭᠠᠷᠭᠠᠯᠲᠠ ᠶᠢᠨ ᠬᠠᠭᠤᠯᠪᠤᠷᠢ ᠰᠣᠩᠭᠣᠨ᠎ᠠ᠃",
    },
}


@lru_cache(maxsize=None)
def strings(directory):
    return {e.get("name"): "".join(e.itertext()) for e in
            ET.parse(RES / directory / "strings.xml").getroot()
            if e.tag == "string"}


def paragraph(directory, index):
    return re.split(r"\\n\\n|\n\s*\n", strings(directory)[KEY])[index]


def require_complete_bo_help(root):
    """Guard the exact independently accepted v2 XML value, not runtime fluency."""
    nodes = root.findall(f"./string[@name='{KEY}']")
    if len(nodes) != 1 or nodes[0].attrib != {"name": KEY} or len(nodes[0]):
        raise ValueError("Tibetan Help key, attributes or markup changed")
    expected = "1106922bbcd1dbf72639721a52f5d1e4f9427f3f8fc1e77282902d0538e8dabf"
    if sha256((nodes[0].text or "").encode("utf-8")).hexdigest() != expected:
        raise ValueError("Complete Tibetan Help differs from accepted v2")


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
        self.assertTrue(strings("values-b+dz")["ui_no_resize_fits_decoder_memory"].startswith(prefix))
        self.assertIn(prefix, paragraph("values-b+dz", CONTRACTS["values-b+dz"]["output_index"]))
        self.assertNotIn("གྲུབ་འབྲས་ཆུང་ཀུ་རང་ཨིན་རུང་", paragraph("values-b+dz", CONTRACTS["values-b+dz"]["output_index"]))

    def test_source_contract_still_matches_the_documented_behaviour(self):
        activity = (CLASSIC / "AssemblyActivity.kt").read_text()
        model = (CLASSIC / "ImageAssembly.kt").read_text()
        renderer = (CLASSIC / "AssemblyRenderer.kt").read_text()
        self.assertIn("private fun showHelp() = message(ui(R.string." + KEY + "))", activity)
        self.assertIn('${item.placedSize.width} × ${item.placedSize.height}', activity)
        placed = model.split("val placedSize:", 1)[1].split("data class SnapTarget", 1)[0]
        for phrase in ("normalization ?: return croppedSize", "NormalizeAxis.WIDTH", "crop.width()", "crop.height()"):
            self.assertIn(phrase, placed)
        self.assertIn("if (!fits(ImageDimensions(1,1))) return null", renderer)
        self.assertRegex(activity, r"if \(suggested == null\)\s*\{\s*message\(ui\(R.string.ui_assembly_source_memory_floor\)\)\s*return\s*\}")
        self.assertLess(activity.index("if (suggested == null)"), activity.index("val sizing = DimensionControls(this,renderer.original,suggested"))

    def test_bo_complete_help_is_bound_to_reviewed_source(self):
        # Accepted v2 against b12c1ce79e2683d5cc841f218c1d19d74e9fd699.
        # A source change needs re-review, not blind regeneration of this guard.
        self.assertEqual("6ae12f86846110a7573a5c608b8561b0c03b037454f1905d3b5bf8342fb26aac",
                         sha256(strings("values")[KEY].encode("utf-8")).hexdigest())
        require_complete_bo_help(ET.parse(RES / "values-b+bo/strings.xml").getroot())

    def test_bo_complete_oracle_rejects_mode_and_instrumental_regressions(self):
        root = ET.parse(RES / "values-b+bo/strings.xml").getroot()
        original = root.find(f"./string[@name='{KEY}']").text
        position = paragraph("values-b+bo", 3)
        mutations = (
            ("missing-position", position + r"\n\n", ""),
            ("unscoped-origin", "མཐའ་ལ་སྦྱར་བའི་ཐབས་ཀྱིས་གནས་འཇོག་བྱེད་སྐབས། པར་རིས་དང་པོ་", "པར་རིས་དང་པོ་"),
            ("unscoped-overlap", "མཐའ་ལ་སྦྱར་བའི་ཐབས་ཀྱིས་གནས་འཇོག་བྱེད་སྐབས། པར་རིས་ཕན་ཚུན་བརྩེགས་མི་ཆོག", "པར་རིས་ཕན་ཚུན་བརྩེགས་མི་ཆོག"),
            ("guaranteed-anchor-move", "གནས་ས་འགྱུར་སྲིད།", "གནས་ས་འགྱུར།"),
            ("wrong-position-label", "«གནས་ས་ཏག་ཏག»", "«Exact position»"),
            ("wrong-coordinate-origin", " 0 ནས་འགོ་འཛུགས།", " 1 ནས་འགོ་འཛུགས།"),
            ("missing-other-position-preservation", "པར་རིས་གཞན་རྣམས་རང་རང་གི་ད་ལྟའི་གནས་སུ་གནས།", ""),
            ("reject-exact-overlap", "འདིར་པར་རིས་ཕན་ཚུན་བརྩེགས་ཆོག", "འདིར་པར་རིས་ཕན་ཚུན་བརྩེགས་མི་ཆོག"),
            ("guaranteed-gap", "ཁ་སྐོང་བའི་ཆེད་དུ་སྤོ་སྲིད།", "ཁ་སྐོང་བའི་ཆེད་དུ་སྤོ།"),
            ("v1-crop-instrumental", "«པར་རིས་གཅོད» ཀྱིས", "«པར་རིས་གཅོད» ཡིས"),
        )
        for mutation, before, after in mutations:
            with self.subTest(mutation=mutation):
                self.assertEqual(1, original.count(before))
                broken = deepcopy(root)
                node = broken.find(f"./string[@name='{KEY}']")
                node.text = original.replace(before, after, 1)
                self.assertNotEqual(original, node.text)
                with self.assertRaises(ValueError):
                    require_complete_bo_help(broken)
        for mutation in ("truncated", "duplicate", "missing", "attribute", "markup"):
            broken = deepcopy(root)
            node = broken.find(f"./string[@name='{KEY}']")
            if mutation == "truncated": node.text = node.text[:-1]
            elif mutation == "duplicate": broken.append(deepcopy(node))
            elif mutation == "missing": broken.remove(node)
            elif mutation == "attribute": node.set("formatted", "false")
            elif mutation == "markup": ET.SubElement(node, "b")
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                require_complete_bo_help(broken)

    def test_english_contract_and_four_exact_active_catalogues(self):
        first, output = paragraph("values", 0), paragraph("values", 6)
        self.assertIn("image dimensions after cropping and any Same width or Same height adjustment", first)
        self.assertIn("choose a smaller output copy if offered", output)
        self.assertIn("If even a tiny output exceeds the budget, the app shows a memory warning instead of a size chooser.", output)
        offered = [node.text for node in ET.parse(RES / "values/app_language_tags.xml").findall(".//item")]
        for directory, clauses in CONTRACTS.items():
            with self.subTest(directory=directory):
                self.assertIn(clauses["tag"], offered)
                self.assertEqual(clauses.get("paragraph_count", 7), len(re.split(r"\\n\\n|\n\s*\n", strings(directory)[KEY])))


def make_tray_test(directory, clauses):
    def test(self):
        first = paragraph(directory, 0)
        local = strings(directory)
        self.assertNotIn(clauses["stale_tray"], first)
        self.assertIn(clauses["post_crop"], first)
        self.assertIn(clauses["post_adjustment"], first)
        # Paragraph 4 already names both controls, so whole-help matching would
        # falsely accept the original bug. Check paragraph 1 only.
        for key in ("ui_same_width", "ui_same_height"):
            self.assertIn("«" + local[key] + "»", first)
    return test


def make_output_test(directory, clauses, name):
    def test(self):
        output = paragraph(directory, clauses.get("output_index", 5))
        self.assertNotIn(clauses["stale_output"], output)
        self.assertIn(clauses[name], output)
    return test


for directory, clauses in CONTRACTS.items():
    suffix = clauses["tag"].replace("-", "_")
    setattr(AssemblyHelpPr8Tests, "test_" + suffix + "_tray_post_crop_and_normalization", make_tray_test(directory, clauses))
    for name in ("offer", "floor"):
        setattr(AssemblyHelpPr8Tests, "test_" + suffix + "_output_" + name, make_output_test(directory, clauses, name))


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
