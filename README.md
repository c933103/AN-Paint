# PR123: preserve the complete eight-paragraph Japanese Help contract

## Confirmed hosted failure

[Run 39061702697](https://github.com/c933103/AN-Paint/actions/runs/39061702697), [JVM job 117480831327](https://github.com/c933103/AN-Paint/actions/runs/39061702697/job/117480831327), ran 1,105 JVM tests with exactly one failure. The downloaded regression artifact's SHA-256 matches GitHub's digest (`66753ee55ec3877f1e6fa1faf7bf123a0a2817ce8f24be43826415ff46005b61`). All 115 raw JUnit XML files are preserved in this packet, together with the complete raw job log and artifact metadata.

The exact JUnit message is `java.lang.AssertionError: expected:<7> but was:<8>` at `JapaneseActiveGuidanceTest.kt:96`, in `actualAssemblyHelpPreservesAllParagraphsAndQualifiesOnlyOptionalDataAndMovement`. The run tested merge commit `b5fe048c5b3c7ffa291b388e9ea6962dd389d206`; its complete source tree is identical to PR123 head `f1aae6ebd453bac18ddabf7c63e629b4291e4d59` (tree `b53357410180f08c6e5dd472b4be4c235c57a3c6`).

The existing test still required seven paragraphs. The reviewed correction intentionally added a separate Exact position paragraph, so the actual Help correctly has eight. The new `AssemblyActivityTest.japaneseHelpModesReachActualHelpAndCurrentPositionLabel` passed in this same hosted run; all 21 AssemblyActivityTest cases passed. A suppressed queued-looper diagnostic appears beneath the failing JUnit assertion, but it does not change the explicit 7-versus-8 mismatch. No speculative lifecycle/scheduling change is included.

## Bounded correction

Only `Paintroid/src/test/java/org/catrobat/paintroid/local/JapaneseActiveGuidanceTest.kt` changes relative to the prior PR head:

- Require exactly eight paragraphs.
- Also compare the shown message with the complete reviewed `assembly-help-japanese/expected.json` fixture, strengthening the older resource-to-message comparison.
- Preserve the existing resource equality plus all four positive/negative checks for optional provider metadata and conditional movement, verbatim.

No assertion is deleted or relaxed, and no production code/resource/fixture changes. All other 1,195 files and executable modes are unchanged. The branch retains its independent develop base `5dba779c904a25bde2ec6d6f8f48eb3cad901a1e`, merged PR121, and the original Japanese correction. No PR122 files, methods or dependencies are introduced. P3 and held PR56 remain unchanged.

[Original full-value review and old/new Japanese text](https://github.com/c933103/AN-Paint/blob/71e3280bc2482708bd6ee523eda22be9d3d16d75/README.md) remain intact. This repair does not broaden the linguistic, layout or device acceptance claims.

Repair commit: [08768f2d9e46e0d2ab873fdd1fefb192db2a456c](https://github.com/c933103/AN-Paint/commit/08768f2d9e46e0d2ab873fdd1fefb192db2a456c). All 1,196 remote source file contents/modes were verified before the non-force, expected-head branch update.

## Current verification

- PASS: 67 focused assembly-Help host tests normally and 67 optimized.
- PASS: catalogue structural validation; aapt2 compilation/linking and supplementary Kotlin/API35 compilation, including the repaired JapaneseActiveGuidanceTest and the existing new Japanese consumer.
- PASS: one-file scope/content/mode and whitespace checks; all five original semantic/resource assertions preserved verbatim.
- PASS: 903 complete host tests normally (223.116 s) and 903 optimized (220.124 s), on this repaired source. All four retained text expectations also pass an explicit host evaluation against the complete current resource value; that check is not Android execution.
- BLOCKED locally: the Gradle 8.13 download still reports `Network is unreachable`. This repaired JVM method has compiled but has not executed locally. A fresh hosted exact-head run is required; the original failing run is not relabelled as passing.

## Exact repair diff

```diff
diff --git a/Paintroid/src/test/java/org/catrobat/paintroid/local/JapaneseActiveGuidanceTest.kt b/Paintroid/src/test/java/org/catrobat/paintroid/local/JapaneseActiveGuidanceTest.kt
--- a/Paintroid/src/test/java/org/catrobat/paintroid/local/JapaneseActiveGuidanceTest.kt
+++ b/Paintroid/src/test/java/org/catrobat/paintroid/local/JapaneseActiveGuidanceTest.kt
@@ -93,7 +93,11 @@
         val dialog = ShadowAlertDialog.getLatestAlertDialog() as AlertDialog
         val shown = dialog.findViewById<TextView>(android.R.id.message).text.toString()
         assertEquals(ui(R.string.ui_add_up_to_20_images_with_android_s), shown)
-        assertEquals(7, shown.split("\n\n").size)
+        val expected = org.json.JSONObject(javaClass.getResourceAsStream("/assembly-help-japanese/expected.json")!!
+            .bufferedReader(Charsets.UTF_8).use { it.readText() }).getString("help")
+        assertEquals(expected, shown)
+        // Exact position is a separate paragraph; retain the complete Help contract.
+        assertEquals(8, shown.split("\n\n").size)
         assertTrue(shown.contains("下部のトレイには、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法が表示されます。提供元からファイル更新日時を取得できる場合は、その日時も表示されます。"))
         assertTrue(shown.contains("親画像をトリミングすると、そこに接続した画像も移動する場合があります。"))
         assertFalse(shown.contains("下部のトレイには、提供元から取得できる場合、"))
```
