"""Structural controls for the new characterization fixture; not Android execution."""
from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "Paintroid/src/test/java/org/catrobat/paintroid/local/VerticalNoticeResizeCharacterizationTest.kt"
ORACLE = ROOT / "Paintroid/src/test/resources/vertical-notice-resize/expected-resources.json"
TAGS = {"mn-Mong", "mnc-Mong", "lzh-Hant", "en-XV", "qaa-Zsye-XV"}
KEYS = {"ui_cursor_pan_move32", "ui_cursor_tap_hint37", "ui_saved"}
METHODS = {
    "compiledAppResourcesKeepFiveVerticalProfilesOnSystemToasts",
    "unchangedHorizontalDirectHelperKeepsNodeTextAndDeadlineAcrossRepeatedGeometryChanges",
    "accessibilityObserverSeesControlsAndSeparatesInitialContentFromGeometryEvents",
    "currentRendererNominalFitIsNotAnInkContainmentOracle",
}


def contracts(source):
    """Fail closed on lost observer/pixel controls, independently of Python -O."""
    required = {
        "API30/35": "@Config(sdk=[30,35]",
        "native renderer": "@GraphicsMode(GraphicsMode.Mode.NATIVE)",
        "compiled wrapping": "super.attachBaseContext(AppLanguage.wrap(base))",
        "source locale": 'assertEquals(tag,a.resources.configuration.locales[0].toLanguageTag())',
        "oracle packaging": 'getResourceAsStream("/vertical-notice-resize/expected-resources.json")',
        "caller newline": 'getString(R.string.ui_cursor_pan_move32)+"\\n"+a.getString(R.string.ui_cursor_tap_hint37)',
        "real validator": "ExportNames.valid(joinedEmoji,ImageFormat.PNG)",
        "route remains toast": 'assertNull("Vertical profile must not take the direct-helper diagnostic route",notice(a))',
        "same node": "assertSame(n,notice(a));assertSame(body,label(a))",
        "before original expiry": "advanceTo(shownAt+7999);assertSame(n,notice(a))",
        "after original expiry": "advanceTo(shownAt+8001);assertNull(notice(a))",
        "no replay": "assertEquals(0,ShadowToast.shownToastCount())",
        "observer source": "Shadow.extract<ShadowAccessibilityRecord>(event).sourceRoot",
        "observer forwards": "return super.onRequestSendAccessibilityEvent(host,child,event)",
        "explicit positive": 'assertTrue("Observer must see an announcement from the actual node"',
        "mutation positive": 'assertTrue("A working observer must see a genuine TextView content mutation"',
        "event source identity": "it.source===body",
        "clear reference guard": 'assertTrue("Reference guard must not itself crop any ink: "+id,',
        "positive reference ink": 'assertTrue("Reference must have painted positive-control ink: "+id,total>0)',
        "actual parent": "n.draw(Canvas(actualBitmap))",
        "independent exact pixels": 'assertArrayEquals("Actual parent pixels must equal independently clipped full reference: "+id,expected,actual)',
        "exact ink loss": 'assertEquals("Parent must lose precisely the escaped reference ink: "+id,total-clipped,visible)',
        "real clipping counterexample": 'pixels.getInt("clipped_ink_pixels")>0',
        "ordinary controls": 'assertEquals("Fitting ordinary/joined-word controls must remain contained",0,pixels.getInt("clipped_ink_pixels"))',
        "incomplete output label": '.put("schema",1).put("completed",completed)',
    }
    return [label for label, snippet in required.items() if snippet not in source]


class VerticalNoticeCharacterizationContractTest(unittest.TestCase):
    def test_four_tests_keep_real_resource_pixel_and_observer_controls(self):
        source = TEST.read_text()
        self.assertEqual([], contracts(source))
        self.assertEqual(METHODS, set(re.findall(r"@Test fun (\w+)", source)))
        self.assertNotIn("manifest=Config.NONE", source)
        self.assertNotIn("addAssetPath", source)
        self.assertNotIn("@Ignore", source)
        self.assertNotIn("assumeTrue(", source)

    def test_resource_oracle_matches_five_current_exact_catalogues(self):
        oracle = json.loads(ORACLE.read_text())
        self.assertEqual(TAGS, set(oracle["locales"]))
        for tag, values in oracle["locales"].items():
            with self.subTest(tag=tag):
                path = ROOT / "Paintroid/src/main/res" / ("values-b+" + tag.replace("-", "+")) / "strings.xml"
                entries = {e.get("name"): "".join(e.itertext()).replace("\\n", "\n")
                           .replace("\\'", "'").replace('\\"', '"')
                           for e in ET.parse(path).getroot().findall("string")}
                self.assertEqual(KEYS, set(values))
                self.assertEqual(values, {key: entries[key] for key in KEYS})
                self.assertEqual(1, (values["ui_cursor_pan_move32"] + "\n"
                                     + values["ui_cursor_tap_hint37"]).count("\n"))
                self.assertEqual(1, values["ui_saved"].count("%1$s"))

    def test_corpus_and_direction_do_not_depend_on_configured_face(self):
        source = TEST.read_text()
        match = re.search(r"private val tags=listOf\((.*?)\)", source).group(1)
        self.assertEqual(TAGS, set(re.findall('"([^"]+)"', match)))
        self.assertIn('private val nullFaces=setOf("lzh-Hant","en-XV","qaa-Zsye-XV")', source)
        name = re.search(r'private val joinedEmoji="([^"]+)"', source).group(1)
        self.assertEqual(6, name.count("\U0001f600"))
        self.assertEqual(5, name.count("\u200d"))
        self.assertTrue(name.endswith(".png"))
        self.assertIn('assertEquals(5,clippedCounterexamples)', source)
        self.assertIn('assertEquals(10,ordinaryControls)', source)

    def test_geometry_scope_retains_both_window_modes_and_repeated_transitions(self):
        source = TEST.read_text()
        self.assertIn("for(edgeToEdge in listOf(false,true))", source)
        self.assertIn('"initial","ime","restored","shrink180","shrink124","expand","same-layout"', source)
        self.assertIn("a.window.setDecorFitsSystemWindows(!edgeToEdge)", source)
        self.assertIn("host(a).rootWindowInsets.getInsets(WindowInsets.Type.ime()).bottom", source)
        self.assertIn("if(old!=null) Reflection.setStaticField(type,\"sNewInsetsMode\",old)", source)
        self.assertIn("assertInsets(a,n)", source)

    def test_control_removal_mutations_are_rejected(self):
        source = TEST.read_text()
        mutations = [
            'assertTrue("Observer must see an announcement from the actual node"',
            'assertTrue("A working observer must see a genuine TextView content mutation"',
            'assertTrue("Reference guard must not itself crop any ink: "+id,',
            'assertArrayEquals("Actual parent pixels must equal independently clipped full reference: "+id,expected,actual)',
            'assertEquals("Parent must lose precisely the escaped reference ink: "+id,total-clipped,visible)',
            'advanceTo(shownAt+7999);assertSame(n,notice(a))',
            'advanceTo(shownAt+8001);assertNull(notice(a))',
            'return super.onRequestSendAccessibilityEvent(host,child,event)',
        ]
        for snippet in mutations:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, source)
                self.assertTrue(contracts(source.replace(snippet, "REMOVED_CONTROL", 1)))

    def test_characterization_does_not_enable_route_or_implement_policy(self):
        route = (ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleTypography.kt").read_text()
        self.assertIn("if(Build.VERSION.SDK_INT>=30 && !VerticalText.uiVertical())", route)
        source = TEST.read_text()
        self.assertIn('importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_NO', source)
        self.assertEqual(1, source.count("announceForAccessibility("))
        self.assertNotIn(".sendAccessibilityEvent(", source)
        # Only the marked test positive control deliberately calls an announcement API.
        self.assertEqual(1, source.count("body.announceForAccessibility(marker)"))
        self.assertIn('recorder.phase="explicit-positive-control"', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
