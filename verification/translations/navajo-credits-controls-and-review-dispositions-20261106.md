# Navajo credits, controls and existing-review dispositions

6 November 2026. Integration base: `91da5ae148de29472aa915a6492252d8d2324a49`. This change adds **22 independently reviewed Navajo priorities: 3 P0 and 19 P1**, repairs one previously held Swedish caption, and resolves one Breton historical applicability hold without changing its wording. It does not fill missing P2/P3, re-review accepted unchanged catalogues, or qualify a release.

## Measured result

- All 171 offered options: **85,394 present source-matching typed identities**. **34 priority gaps remain, all Navajo: 17 P0 + 17 P1**. 170 options have complete direct P0/P1 presence; presence is not linguistic certification.
- Navajo now has **313 entries: 77/94 P0, 232/249 P1 and four earlier accepted P2**. All **291** preceding values and attributes remain exact, with no repeat language-review credit.
- Swedish changes only `ui_main23`; all other **718 resource nodes** and their attributes remain exact. Breton XML is unchanged.
- The source catalogue, priority manifest, production consumers, scope restrictions and other languages remain unchanged. The 59-scoped/112-outside-scope distinctions and orthography exclusions remain in force.

## New complete meanings reviewed

### Credit retention: three P0

`gallery_credit_could_not_save`, `gallery_credit_too_large`, `legacy_credits_unreadable`.

The credit category is described functionally as information about the image maker and rules. This identifies the attribution record, not just an author's name or arbitrary image metadata. The three complete warnings preserve, respectively:

1. Save-or-restore failure, retention of previously saved information, and retry.
2. The conditional **would** make the serialized drawing too large to restore, plus retention of **both** previous drawing and previous credits. A review correction repeats the previous qualifier for both objects, rather than leaving its scope dependent on adjacency.
3. **Some** stored information could not be read, while the corresponding stored copies still exist. This does not promise successful decoding or reconstruction.

The actual editor/preflight/atomic-write and archive-read paths were checked. A failed workflow is not claimed to prove that no raw file was ever written or cleaned up. Previously accepted credit information is distinct from rejected unsaved fields. Conditional order is directly supported by the [Navajo Language Academy/Swarthmore entry](https://talkingdictionary.swarthmore.edu/navajo_particle/?entry=2834) and primary Young/Morgan PDF268, printed123. The maker relation was directly read in a [published Navajo sentence](https://www.bible.com/bible/1098/PSA.121.NVJOB); no source sentence is reproduced. Direct entries support [rules](https://en.wiktionary.org/w/index.php?title=bee_haz%CA%BC%C3%A1anii&oldid=81786902) and [continued existence](https://en.wiktionary.org/w/index.php?title=h%C3%B3l%C7%AB%CC%81&oldid=89882968). New technical compositions retain moderate-low contextual confidence, not native or standardized-term certification.

### Colour controls: six P1

`ui_colour`, `ui_edit_colour26`, `ui_add_colour26`, `ui_invalid_colour`, `ui_new_colour`, `ui_selected_colour23`.

The existing Colors topic is separated from the individual value/action. A demonstrative is not falsely claimed to be inherently singular; live one-value consumers supply that referent. The Add correction explicitly names the existing Palette caption as the insertion container. The source-only New caption uses the sourced numeral one. The current-colour preview is neither selection history nor an already committed choice. Add may require replacing a full palette slot and does not guarantee a greater number of saved colours.

### Dimension and colour-information guidance: four P1

`ui_choose_a_smaller_output_copy_the_source_images`, `ui_scales_the_image_unlock_the_ratio_to_stretch`, `ui_polygon`, `colour_invalid_metadata`.

- The reduced **output** is distinct from original source images and retained pixel-coordinate crop settings.
- The exact proportional-dimensions checkbox is identified as off before changing width/height separately. This is image resampling, not crop/extend of canvas bounds, and does not invent a No button.
- The [direct polygonal predicate](https://en.wiktionary.org/w/index.php?title=b%C3%ADdazneesk%CA%BC%C4%85%CC%81&oldid=87335362) names the variable-vertex tool. The secondary entry's cited 1992 primary page was not inspected. Optional open-path mode does not change the tool-family label into a promise of closure or fill.
- Invalid **or** currently unsupported colour information remains disjunctive. The functional does-not-use description is scoped to this application's parser rejection, not a claim that all editors are incapable or that all unsupported data is corrupt.

### Gestures and navigation: eight P1

`ui_colour_palette_tap_for_foreground_hold_for_background`, `ui_colour_tap_foreground_hold_background`, `ui_crop_preview_drag_an_edge_or_corner_drag`, `ui_drawing_canvas_pinch_and_move_two_fingers_to`, `ui_pinch_and_pan_mode`, `ui_tool_categories`, `ui_trim_expand_canvas_by_touch`, `ui_left_arrow_collapse`.

Independent review read the complete primary held-press, drag, corner, finger/touch, toward-each-other/apart and more/kinds evidence, then checked the complete new instructions. The sustained-press form was corrected during authoring rather than copying an incomplete paradigm stem. Pinch is described through two fingers moving together/apart; pan concerns the view, not resampling. The trim/expand correction repeats the **bounds** object before make-smaller/larger. Four source-only entries retain future binding, speech and presentation limits. No author-approval gate or native-human review is claimed.

### Historical Fit alias: one P1

`ui_fit_image` reuses the exact already accepted `ui_fit` wording. Its first accepted lineage is the isolated `decbe43612737196c8776e78230c81476b30eab0` cohort, carried by the [188-entry receipt](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6682089017), not a newly repeated language review. The [old View action](https://github.com/c933103/AN-Paint/blob/f47d9ee9458f2f9207eae5e3514f211baecdfa51/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L611-L618) and the three current Fit controls invoke `paintCanvas.fit()`. This closes the missing historical action relationship; it does not mean scaling a selection into the canvas. The old key is source-only now.

## Existing held wording, narrowly resolved

- **Swedish `ui_main23`: `Huvud` → `Huvudpanel`.** The recovered [pre-rename Main tab/panel binding](https://github.com/c933103/AN-Paint/blob/5c4b1447024a422880bdcd297d10f24b6ce34953/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L626-L628) proves the drawing-tools panel referent. The compound supplies that omitted referent without substituting Home or the newer Draw command. [Official Swedish GUI terminology](https://docs.oracle.com/cd/E19683-01/816-3941/6ma6hcpjj/index.html) directly attests the compound. Independent acceptance applies only to this historically proved caption; no active consumer or future unrelated use is certified.
- **Breton `ui_fit_image`: existing acceptance made applicable, no XML change.** Its full target equals accepted `ui_fit`, with attributes equal except identity. The [immutable accepted packet](https://github.com/c933103/AN-Paint/blob/5367fe1e9703593bf464e1dd7f1aab2eab750868/tools/fixtures/current_localization/breton_asturian_occitan_priority_wording.json) and the same historical/current `paintCanvas.fit()` relation supply the previously missing applicability evidence. This is zero new linguistic-review credit, not approval by phrase similarity alone. Future unrelated consumers remain outside that scope.

## Verification

All accepted maps were hash-verified before integration. Exact default-source values, attributes, current consumer blobs, placeholder signatures, Android escapes, literal boundaries, NFC and XML roundtrips pass. **105 existing host tests pass**. **2,022 actual JDK formatting cases pass across 1,033 string/plural/array items in the two affected catalogues**; this item count is not the typed-identity count used for coverage. No permanent wording mirror or per-edit wording test was added.

The accompanying [second receipt-union checkpoint](review-receipt-union-checkpoint-2-20261106.md) links 56,104 existing identities at the **pre-change** baseline. It preserves different acceptance and classification scopes; it is not 56,104 fresh reviews or proof that the remaining receipt-enumeration queue lacks prior review. This integration contributes only its actual new/repaired scopes.

No Android SDK, AAPT/Gradle/Robolectric, installed layout/glyph/TalkBack, native-speaker, exact-head CI or release certification is claimed here. The 34 remaining priority gaps, review-evidence normalization, live lower-tier dependency questions, current-develop integration and exact-head review/CI gates remain open. Publish to the existing review branch with an expected-parent non-force lease, verify every retained path/content/mode and changed remote file, and report actual exact-head CI status separately.
