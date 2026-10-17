# Indonesian P0/P1 complete-value review, 17 October 2026

## Scope and result

This fresh model-based review read all **341 complete English/Indonesian P0/P1 pairs** (92 P0, 249 P1), their source consumers and relevant action chains at develop `9bff0abd8f7bc04facbb556908b3a6f578c7346f`, tree `5f0fab23aadd6cc6ecec4233e2fc7a88f7784b24`.

- 303 unchanged values accepted within inspected static consumer context.
- 32 accepted for wording only: 29 have no direct consumer; three have references in dormant settings/menu fallback paths.
- Two complete-value corrections accepted by an independent model reviewer.
- Four explicit uncertainty holds remain unchanged.

No whole-language, native-speaker, installed-layout or TalkBack acceptance is implied. The other 376 canonical entries were not fully reviewed. PR56 remains read-only and its counters are unchanged. Its 609 Indonesian prior records are preserved in the packet; 306 overlap this selected batch and receive **no duplicate tracker credit**. The one prior processing-label hold remains open, outside this batch.

Dutch was not repeated: its full 341-entry batch already exists on `evidence/priority-review-it-nl-fr-20261017`, with seven corrections merged in PR110. The three current branch-list pages and recent/open PRs showed no existing Indonesian full priority batch.

## Two corrections

1. `ui_the_encoder_did_not_finish`: `Enkoder tidak selesai.` → `Enkoder tidak menyelesaikan pengodean.` The new full sentence identifies encoding as the unfinished operation. The original terse sentence leaves the unfinished object ambiguous; this is a clarity repair, not a claim that every reader necessarily misinterprets it. `ImageExporter`, `TextImageCodec` and `IcoCodec` emit it when bitmap compression returns false.
2. `ui_pixels_6ec9c2`: `Piksel` → `piksel`. The actual `DimensionControls` composition becomes `Lebar dalam piksel` and `Tinggi dalam piksel`. Standalone `Piksel` remains capitalized. The count label is unchanged because Indonesian `piksel` is number-neutral, including `1 piksel`.

Only the two value spans in the Indonesian catalogue change; all keys, attributes, format arguments, other locale files and application behavior remain unchanged. Three compact test/fixture files accompany the XML correction. Application head: `949e8ccb0d60ac2e46da1b30e33069ff56ec8506`; candidate tree: `f12e3f31420ab23c8edc67d72607150b796b1571`. All 1,200 remote leaves match the locally reviewed content/type/mode manifest.

## Explicit holds and preserved choices

- `ui_the_draft_is_saving_try_again_shortly`: faithful wording, but the generic-busy credit-attachment use remains under the existing [PR72 source-context investigation](https://github.com/c933103/AN-Paint/pull/72). No context acceptance or source change here.
- `ui_foreground_background_colour_palette`: the absent consumer leaves the third substitution's intended composition uncertain.
- `ui_fg` / `ui_bg`: compact `Depan` / `Latar` remain unchanged pending clarity/fit confirmation. Their existence is not asserted to be a defect.
- The `ui_save_a5d0d9` alias remains `@string/ui_save`. Its actual action can save directly to an existing destination, so no mandatory-dialog implication is introduced.
- All four held `ui_rendering_images` values (Indonesian, Malay, Japanese, Hong Kong Chinese) remain byte-identical. Their old findings and tracker status are preserved.
- The Japanese/English complete assembly Help work in PR123/122 is separate and not duplicated. No P2/P3 or processing-label change is included.

## Evidence and checks

Download the [full packet](indonesian-review-packet.zip), [test summary](test-summary.json) and [archive checksum](packet.sha256).

The packet includes every full source/old/candidate value, resource attributes, individual authored rationale, decision/confidence, static consumers, immutable source binding and scalar hashes. It also includes the exact two full correction pairs, independent review, source/candidate manifests, application patch, validation scripts, prior receipts, focused/full host logs and compile receipts.

Six focused host tests cover exact complete values, attributes/syntax, fail-closed inventories and mutations, actual static emitters, composed labels, preserved aliases/holds and complete catalogue structure. Two authored Robolectric methods exercise repeated actual pixel/percentage switching and all three real encoding entry paths with the existing bounded PNG-failure shadow, preserving source pixels and transactional derived-output destinations. They also include a successful real PNG control.

Full resource AAPT2 compilation, exact-script mirrors and resource linking passed. Supplementary Kotlin/API35 compilation of the new test passed with existing compiled dependencies and fresh resource symbols. This is **not** full Gradle compilation or execution. Local Gradle first failed at an unavailable default-cache lock path; a bounded retry using a private local cache then failed downloading Gradle 8.13 with `Network is unreachable`. Both attempts are preserved. Hosted exact-head runtime/lint/APK/device checks remain separate gates.

The initial evidence validator rejected an overly terse Paste rationale (its mechanical minimum-length rule); the rationale was expanded and normal/optimized validation now passes. Both reports are retained. Structural validation is not used as a substitute for linguistic judgment.

This evidence commit preserves the complete application tree and adds this evidence directory; it is not an evidence-only replacement of an application parent.
