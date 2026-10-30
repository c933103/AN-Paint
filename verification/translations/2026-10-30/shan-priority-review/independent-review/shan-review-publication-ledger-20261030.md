# Shan priority localization — source-bound review ledger

## Scope and disposition

Baseline: develop **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**. This is an independent AI/model linguistic and semantic review, not native-human certification, completed integration, automated validation or installed-UI proof.

| Missing-resource disposition | P0 | P1 | Total |
|---|---:|---:|---:|
| Accepted lexical values | 26 | 114 | **140** |
| Accepted notation-only templates | 0 | 7 | **7** |
| Held values, excluded from additions | 27 | 9 | **36** |
| Entire missing-resource scope | **53** | **130** | **183** |

**147 missing values are accepted**, including seven nonlexical templates. Those seven are not seven newly authored lexical translations. The 36 holds remain English fallbacks; no whole-language-completion claim is made. The newly accepted palette parent is backed by a recovered historical contract; its absent embedded fragments and mixed-language fallback limits remain explicit.

Separately, two already-present P1 values were reviewed: **Undo accepted unchanged** and **Brush accepted as a replacement**. Neither is a missing-resource addition. Previously accepted PR #237 entries and the six earlier unchanged Shan decisions are preserved without duplicate credit.

## Complete review partitions

The exact per-value review tables provide the target text, backtranslation or meaning, reason, confidence and disposition for every lexical candidate and notation template. This ledger supplies final precedence over historical proposal decisions.

| Partition | Missing P0 | Missing P1 | Final accepted | Final held | Exact decision record |
|---|---:|---:|---:|---:|---|
| A lexical | 9 | 28 | 37 | 0 | `shan-review-batch-a-independent-20261030.tsv` plus resolution overrides |
| B lexical | 5 | 16 | 21 | 0 | `shan-review-batch-b-independent-20261030.tsv` plus resolution overrides |
| C lexical | 5 | 25 | 30 | 0 | `shan-review-batch-c-independent-20261030.tsv` plus resolution override |
| D lexical | 0 | 33 | 32 | 1 | `shan-review-batch-d-independent-20261030.tsv` |
| E lexical | 5 | 12 | 17 | 0 | `shan-review-batch-e-independent-20261030.tsv` plus palette resolution override |
| F lexical | 2 | 1 | 3 | 0 | `shan-review-batch-f-independent-20261030.tsv`; two exact successors |
| Notation/templates | 0 | 7 | 7 | 0 | `shan-review-format-invariants-independent-20261030.tsv` |
| Draft-dependent holds | 12 | 2 | 0 | 14 | `draft-term-holds.tsv`; unchanged exclusions below |
| Other semantic holds | 15 | 6 | 0 | 21 | `remaining-semantic-holds.tsv`; unchanged exclusions below |

A's separate existing-value rows are not included in its 37 missing-resource count. The original A/B/C proposal records contain historical holds/corrections that have been resolved only by the exact successors below.

## Authoritative precedence for final target values

1. For A/B/C entries whose original independent row is `accept`, use that exact value and the source attributes. Do not revive a historical held value.
2. For the following eight missing keys, the exact values in **`shan-review-resolutions-independent-20261030.tsv`** supersede the original A/B/C rows:
   - `ui_png_encoding_failed`
   - `ui_the_encoder_did_not_finish`
   - `ui_autosave_image_encoding_failed`
   - `ui_autosave_selection_encoding_failed`
   - `save20_encoding_budget`
   - `ui_rotate_90_clockwise`
   - `ui_enter_a_trim_amount_for_every_edge`
   - `ui_enter_all_four_trim_amounts`
3. Use D and E rows marked `accept` exactly. **Exclude** D's held `ui_airbrush`. E's historical `ui_foreground_background_colour_palette` hold is superseded only by **`shan-review-palette-resolution-independent-20261030.tsv`**: `သီတၢင်းၼႃႈ %1$s၊ သီပိုၼ်ႉလင် %2$s။ ပၢၼ်ႉသီ — %3$s။`. Use this new em-dash topic/instruction value, not the original unseparated E target. The separate P2 right-arrow row is ancillary linguistic evidence, not an authorized addition or P0/P1 credit.
4. F's exact final table takes precedence over original batch F. `ui_sampled_resize_memory_explanation` uses the **sampled-decode revision**, and `ui_export_explanation23` uses the **attested icon revision**. `ui_codec_resize_memory_floor` uses the unchanged accepted original. These are three keys, not five translation credits.
5. The seven templates in **`shan-review-format-invariants-independent-20261030.tsv`** retain separate notation-only classification and exact formatting attributes.
6. Existing `ui_undo` remains exactly serialized as **`"ၶိုၼ်ၶိုၼ်း"`**. Existing `ui_brush` takes **`ယူႈယွမ်ႉသီ`**, with the full independent resolution in the resolution TSV. This suitable replacement is not a proven-defect claim about the prior unreviewed Brush compound.
7. The 35 prior semantic/draft holds remain excluded. No prior unaccepted proposal gains acceptance by resemblance to a reviewed noun or by a source lookup alone.

### Resolution meanings

The five encoding successors explicitly describe converting image or selected content into file data. They do not imply entering program code, successful destination writing or loss of previous autosave data. PNG, incomplete encoder work, whole-image versus selected-content autosave and temporary conversion-buffer memory demand remain distinct.

The clockwise successor **ပၼ်ႇလိဝ်ၶႂႃ 90°** combines rotation and clockwise direction; it is not mirroring or moving right. The trim successors describe **amounts to remove**, preserving every-edge and all-four quantifiers. The sampled-decode successor says pixel-count reduction is **possible**, not guaranteed when the sampling factor is 1. The icon successor retains both unchanged current image and unchanged Save destination.

### Palette historical-contract resolution

The [historical caller at f47d9ee9458f2f9207eae5e3514f211baecdfa51](https://github.com/c933103/AN-Paint/blob/f47d9ee9458f2f9207eae5e3514f211baecdfa51/Paintroid/src/main/java/org/catrobat/paintroid/classic/ColourStatusButton.kt#L37-L44) was independently fetched: the third argument is a complete left-arrow/collapse or right-arrow/expand instruction, not a state, name or count. The revised parent makes the palette an explicit topic before the intact instruction. Both full Shan compositions are accepted at moderate-high semantic and moderate idiomatic confidence. Foreground/background arguments already contain `#`; the target adds none.

Current Shan contains neither arrow fragment; the left P1 proposal is separately accepted but not implemented. The exact right fragment **ပိုၼ်ၸီႉၶႂႃ: ၶႂၢၵ်ႈ** is independently acceptable as ancillary P2 wording, with **zero priority credit and no source-integration authorization**. Both conditional English-fallback compositions are semantically compatible but remain mixed-language. Current code no longer calls this composite; no runtime or TalkBack proof is claimed. Exact full examples and limits are preserved in `shan-review-palette-compositions-independent-20261030.tsv` and the palette resolution report.

## All held values

Each exclusion below is specific. It is not evidence that Shan cannot express the concept, and it does not block unrelated accepted messages.

| Key | Tier | Exact unresolved point |
|---|---|---|
| `ui_airbrush` | P1 | Exact compound `ၶိူင်ႈၽူၼ်သီ` does not yet have a secured spray sense; `ၽူၼ်` is attested as rain. |
| `ui_draft_not_saved_yet` | P0 | Draft noun not established as persistent editable autosave state rather than example/model. |
| `ui_draft_saved` | P0 | Same draft-object gap; must not falsely report normal external Save completion. |
| `ui_draft_restored` | P0 | Same draft-object gap; restored saved state must not become a new drawing. |
| `ui_autosaving_draft` | P1 | Unfinished-artwork wording would misdescribe visually complete but autosaved work. |
| `ui_draft_pending` | P1 | Pending is a save-state label, not artwork incompleteness, saved success or failure. |
| `ui_the_draft_is_saving_try_again_shortly` | P0 | Draft noun and explicit short delay before retry both unresolved. |
| `ui_previous_draft_kept_for_recovery` | P0 | Must identify previous persisted draft and retention for recovery, not generic recoverability. |
| `ui_the_previous_draft_could_not_be_preserved_separately` | P0 | Previous draft object and separate-preservation failure; cannot imply deletion or read/export failure. |
| `ui_the_previous_draft_could_not_be_restored` | P0 | Previous draft object and restoration failure distinct from preservation failure. |
| `ui_the_previous_draft_could_not_be_moved_to` | P0 | Previous draft object and failed move-aside transaction, not successful copying/export. |
| `ui_the_previous_draft_needs_more_memory_to_reopen` | P0 | Prior draft identity plus working-memory need, not storage shortage or corruption. |
| `ui_history_unavailable34` | P0 | Canvas restored, history unreadable, original draft retained as recovery copy must remain three distinct propositions. |
| `ui_autosave_is_paused_to_protect_that_draft_use` | P0 | Protected older draft/export action must remain distinct from current work's PNG/JPEG Save action. |
| `ui_recovery_copy_exported_extract_canvas_png_from_the` | P0 | Exact ZIP extraction instruction plus draft settings and possible floating selection contents cannot imply ordinary project import. |
| `formats22_animation_poster` | P0 | Separate PNG default-image identity cannot become the first animated frame or generic base image. |
| `formats22_pdf_raster_hint` | P0 | Rendering text/vector objects into pixels at 144 dpi, not merely displaying them. |
| `save20_gif_description` | P0 | Dithering/gradient relation must not become blur, added actual colors or ordinary interpolation. |
| `save20_invalid_name` | P0 | Encoding control characters not secured; must not mean UI-control text. Slash evidence alone is insufficient. |
| `save20_unsupported_image_colour` | P0 | Color profile and color-managed editor, with required sRGB PNG conversion before import. |
| `colour_unsupported_icc_model` | P1 | ICC model versus profile and color-managed application; RGB copy/first action must remain exact. |
| `ui_an_assembly_source_image_is_missing` | P0 | Editable assembly object distinct from flattened composite; underlying source image is missing. |
| `ui_assembly_saved` | P0 | Persistent editable assembly saved, not simply images combined. |
| `ui_could_not_save_the_assembly` | P0 | Assembly-state save failure, distinct from composite export; `%1$s` belongs to this failure. |
| `ui_could_not_store_the_assembly` | P0 | Persistent arrangement store failure, not generic image saving. |
| `ui_the_saved_assembly_could_not_be_opened` | P0 | Saved editable assembly open failure, not ordinary image decoding; `%1$s` retained. |
| `ui_not_enough_memory_for_this_operation_the_assembly` | P0 | Underlying assembly source files retained, not merely flattened output. |
| `ui_assembly_source_memory_floor` | P0 | Editable assembly, minimum-output memory floor, inadequate dimension-only reduction, remedies and unchanged arrangement. |
| `gallery_credit_too_large` | P0 | Attribution records, hypothetical restore-size limit and retention of both previous drawing and credits. |
| `gallery_credit_could_not_save` | P0 | Attribution-record save/restore failure versus existing saved credits retained and retry. |
| `legacy_credits_unreadable` | P0 | Some attribution records unreadable while stored copies remain; not all lost or all restored. |
| `ui_drawing_canvas_pinch_and_move_two_fingers_to` | P1 | Precise pinch/spread two-finger zoom/pan gesture and one-finger Navigate exception. |
| `ui_pinch_and_pan_mode` | P1 | Pinch input must not disappear into a generic zoom/move label. |
| `ui_ellipse` | P1 | Exact ellipse geometry, not egg-shape, asymmetric oval or circle only. |
| `ui_enter_positive_canvas_dimensions_within_android_s_coordinate` | P1 | Strict-positive dimensions and coordinate-range limit, not memory/pixel-count limit. |
| `ui_invert_colours` | P1 | RGB channel complements with alpha retained, not conversion, slot swapping, mirroring or grayscale. |

## Preserved technical form

All reviewed values are bound to the exact English source and attributes. Indexed placeholder identities, types and precision, literal escaped newlines, units, numeric ranges, punctuation and `formatted="false"` attributes are part of the reviewed targets. In particular, the long budget warning retains `%1$d`, `%2$d`, `%3$.2f` and `%4$.2f`; no placeholders are substituted with example values. The notation-only templates preserve their exact supplied-argument contracts without claiming that embedded text is localized by these rows.

Manual comparison is not a parser test. No scripts, tests, source edits or publication were performed as part of this linguistic review.

## Primary terminology evidence and limits

- [MediaWiki Shan catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json) supplies real edit-reversion usage for Undo and image-context usage for pixel and metadata terms. Full app sentences and app history behavior were assessed separately; dictionary repetition alone did not establish Undo.
- [Unicode CLDR49 Shan summary](https://unicode.org/cldr/charts/49/summary/shn.html) distinguishes paintbrush from toothbrush, clockwise from anticlockwise, rectangle from square, and supplies pencil, palette and percentage terms. These are contextual lexical evidence, not blanket acceptance of compounds.
- [VisualEditor Shan catalogue](https://github.com/wikimedia/mediawiki-extensions-VisualEditor/blob/master/i18n/ve-mw/shn.json) and its [English counterpart](https://github.com/wikimedia/mediawiki-extensions-VisualEditor/blob/master/i18n/ve-mw/en.json) establish the digital-icon noun used in the final export sentence. A UI-control icon noun was independently judged suitable for exported icon imagery.
- The [rain dictionary entry](https://en.wiktionary.org/wiki/ၽူၼ်) supports the narrow Airbrush lexical uncertainty; absence of a retrieved spray gloss is not proof that no spray sense exists.

Long functional labels, typography, rendering, compact-control fit and TalkBack output remain unverified. Moderate confidence is intentionally retained where compositional technical paraphrases are semantically sound but native idiomatic preference has not been established.

## Frozen source and input fingerprints

SHA-256 fingerprints bind exact bytes, not successful integration or execution.

| Canonical resource | SHA-256 |
|---|---|
| `Paintroid/src/main/res/values/strings.xml` | `743bd9f04c391fb8e94dfb72f81fb24bbe2e3eb36f1584f35821687a1b96a261` |
| `Paintroid/src/main/res/values-b+shn/strings.xml` | `c2bbbea24cbebbe5ea641d5820f5d39e830c185ed665b080909674ae50078454` |
| `translations/string-importance.json` | `9b5bfb6d25f2ad034158816d943b94feed8296ad4117c2176f09a95dad506879` |
| `tools/fixtures/current_localization/reviewed_priority_batches.json` | `429c8a063938708597f234ef28ae213df45eac9bf56264abd3f458b20ba92a5c` |

| Exact independent decision record | SHA-256 |
|---|---|
| `shan-review-batch-a-independent-20261030.tsv` | `458620dac52b10c9fe09f6de787e3961a4251cca1a41070d83f45a6d92d67760` |
| `shan-review-batch-b-independent-20261030.tsv` | `913d69e07a970cf597dab1e6a43616c736fa2ecee9ccf5a3b7165f3bdfcd7fc5` |
| `shan-review-batch-c-independent-20261030.tsv` | `73d603be17ad4e4e6e82d2f9e2ed43b2259ca07d093873c37e34c7f2ef12bc6b` |
| `shan-review-batch-d-independent-20261030.tsv` | `6d2f98057010497c7889fb944d9724d73994243c5da266ade5f2eb55a847a5b1` |
| `shan-review-batch-e-independent-20261030.tsv` | `701e225c274793c810a6f0052753ede1e6d624ab7c353859e5ee03fb43c0a83e` |
| `shan-review-batch-f-independent-20261030.tsv` | `851ee358ab6c6d9ec24590a77b0dd9cf80546f1be600e2834d9f23f64ea7152b` |
| `shan-review-resolutions-independent-20261030.tsv` | `404f9717bd6a1f47d008098baa6f63651743f1e0cbd9bab65eb6e6379f9181bf` |
| `shan-review-format-invariants-independent-20261030.tsv` | `fbbe9274e9849b26e1c38f41d9dfaef95e0cdcec93a8887e2208635eb88a06a1` |
| `shan-review-palette-resolution-independent-20261030.tsv` | `baabc720b3fc64556383b8f7d081c64e59df82ed50bb44dbf61164247928e573` |
| `shan-review-palette-compositions-independent-20261030.tsv` | `20567d03d0ee77123b1671210e9e62dedaba6f30a96b77934e6d0a82bfe77e9b` |

| Candidate/revision record | SHA-256 |
|---|---|
| `batch-a.tsv` | `d30ba3b7332f135a39dd1e73c24f2f82fa6b589c1246fd890b07082fb16da2f7` |
| `batch-b.tsv` | `b032bf1d857fc977bc95edab01620756ca6868f76521b5d75c431b32835e22bb` |
| `batch-c.tsv` | `9d0bfa49e8a678cc99260cbf4208f701da10c957a5999809ceba233d873ec954` |
| `batch-d.tsv` | `22900957f5a94c1444ed7b84b8f23e2b1e8b65f2ff1e3ba812665ffe8a0d7d66` |
| `batch-e.tsv` | `f530fe83cc902a7a27ed836e7e5764d558346d7169fee0b64b8886e18b03d776` |
| `batch-f.tsv` | `182611c49de8b8544f253ab548eb690aabe3cf70a5525d8ddae20bcb8a5e89ce` |
| `encoding-revisions.tsv` | `b4258ecba9bfe76bb594c50997a670ccdcc300f6ed8a49ab3c2b7ab83e1a3595` |
| `rotation-revision.tsv` | `f2a3303fa197868e37ff79f629b387c0bf2660cd5b43fe6900161c0b76547b89` |
| `trim-secondcheck-receipt.tsv` | `06b33d3e631d856d3dae41470dac7919ee7ad7f12f3ae660d49859e5114db30e` |
| `brush-reassessment.tsv` | `ebfba1de293fcdb82aa9b9ec69c6d210fdd79282729b94db6d4c04decfe1236c` |
| `sampled-decode-revision.tsv` | `0c7b14ec809f796cdec991a1cc4317782938827125b255fdd95bc06fd306f44f` |
| `export-icon-revision.tsv` | `fb55574a5c3948ad25cc27731e89e1e7bd7f36daa7d7b6182f64969f38137952` |
| `format-invariant-review.tsv` | `d0c274d9e4b9ea0de8aa33c8b5756671f6c3c0a4e7dca14c49a6cbe9579679e4` |
| `draft-term-holds.tsv` | `e01cd6eedc3546dcd10a42be93ec9bfcc3054e1b41aefa2730effd96300c40cf` |
| `remaining-semantic-holds.tsv` | `dcaf8ebf21ad76b14324af6fe3bbd4544a45caed64f7026a53754afe6e2644c6` |
| `palette-historical-contract-revision.tsv` | `350b0b18557e5a2e9a753ca963a01fc0608ac500d9f193c475c6d4b75b402c7e` |
| `palette-historical-compositions.tsv` | `9758ac8455ca7c39c91040639a4839fdf3ba3907e6c29f79fed35e82c4e77ee1` |
| `palette-historical-contract-review.md` | `fe9ccb215d9522fbc68daac55ffa45f3b6f1437550e7c4e2497433f86d9f42ec` |

Batch C's Pencil rationale is the corrected version: crisp edges at any selected width, not a one-pixel-only tool. Its target text is unchanged. Historical input records are retained for traceability, but only final accepted rows and explicit successors above are eligible for integration.
