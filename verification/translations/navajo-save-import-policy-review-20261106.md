# Navajo save, import, memory and policy review

6 November 2026. Base `37ea666d3b81aa95f51c4611bb80e943b8c98d5a`.

## Result and scope

Adds **12 missing priorities: 4 P0 + 8 P1**. All **279 existing values/attributes** are unchanged, with zero repeated linguistic-review credit. No missing P2/P3, production code, default English, fonts or other locale wording changes.

Final Navajo: **291 entries**, including 74/94 P0, 213/249 P1 and four earlier accepted P2 entries. **56 priority gaps remain: 20 P0 +36 P1.** Fresh all-171 inventory: **85,372 present typed identities**, those same 56 priority gaps entirely Navajo, 170 options with complete direct P0/P1 presence, 65 with all source identities. P2/P3 gaps remain30,043/7,478. Presence is not whole-project linguistic acceptance and does not override the 59-scoped/112-outside-scope fallback restrictions.

The separate [review-receipt reconciliation checkpoint](review-receipt-lineage-checkpoint-20261106.md) preserves already accepted evidence rather than restarting language reviews. Its24,194-row bounded subtotal overlaps other inventories and is not an additive all-project reviewed total. Full union reconciliation continues.

## Twelve changed-only decisions

- **Eyedropper:** explicit from-image relation makes the image the source of the colour choice. The consumer samples the touched in-bounds bitmap pixel into foreground, rather than selecting a preset palette or describing a medicinal dropper.
- **Solid fill:** interior/all/painting describes the shape-style foreground fill, distinct from outline and background-fill-plus-outline. This is not the flood-fill tool, a technical noun claim or an assertion that all alpha is opaque.
- **Decoder/editing memory:** approximate required memory and allowed work-memory cap remain distinct. A narrow correction names the operation's RAM cap, not total installed/free device RAM. A smaller copy is suggested without promising every decoder floor can fit.
- **Minimum-size failure:** the explicit 1×1 output floor matches the actual import-plan test. It does not claim the original source has one pixel or that a ratio-locked control necessarily offers a 1×1 target. Cancel then choose a smaller source remains the next action.
- **Full-image/work-memory failure:** both image and auxiliary work RAM are named, with the alternative Android failure. It asks to reduce and edit a copy; original-file nonchange is scoped to this staged import/resize, not later Save or all editor state.
- **Two ratio checkboxes:** directly sourced width/height proportionality names the constraint, not a physical lock, equal dimensions or frozen size. Dimension entry follows the original image ratio; floating-selection resizing preserves its current ratio. Integer rounding and independent rotation/movement remain existing behavior.
- **PNG poster warning (P0):** identifies the separately contained motionless image inside PNG, not the first animation frame. Only that image will open; animated content is excluded; Save still produces only a still image. A narrow correction makes the motion predicate an explicit topic rather than silently treating a finite verb as a noun. It does not claim import has already succeeded or the source lacks animation.
- **Export explanation (P0):** names ICO, Base64 text and ASCII output. The image-preservation clause is scoped directly to creating that derived artifact; current ordinary Save destination, including an unset destination, is not reassigned. This is not an all-future-state guarantee.
- **Share explanation (P0):** first choose a location and save a copy, then select an Android tool for the quoted Send action. The ordinary Save destination remains distinct from the newly selected copy destination. App selection is not proof of delivery; launch can fail after saving.
- **Save-reuse explanation (P0):** format and byte-compacting settings are distinct from image dimensions. The ordinary Save policy explicitly reuses filename, destination, format and settings after a successful normal save establishes its target. It does not apply this policy to Export/Share, cancellation or failed saves, or guarantee every encoded file gets smaller.
- **Device language policy:** the new according-to relation makes Android's language the governing source rather than a fixed language-category choice. Empty selected-tag policy re-resolves system/device locale and clears app overrides; this is not reset-all-settings or merely the app's current language.

The eight import/memory/ratio/poster entries were independently accepted with two narrow corrections. The three Save/export/share entries were independently accepted with two further corrections. The device-follow composition was independently accepted using an already inspected primary relation. All corrections were acknowledged by the author; no prior accepted wording was reopened.

## Important preservation boundary

`writeImage` calls `applyPending` before taking the encoding snapshot. This can commit selection/drawing geometry, affect history/selection and set dirty=true. Export/Share does not call `markSaved`, clear dirty or replace the ordinary saved target, but **dirty status and every editor state are not invariant**. The final warnings preserve only their actual scoped promise. The earlier overbroad evidence note was corrected without counting it as a new resource repair. Source/destination, preservation versus successful completion, and save-copy versus actual sending remain separate.

## Sources and review limits

New clauses reuse exact accepted image, Save, language, width/height, colour and action components from [post-reset receipts](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6682089017) and the preceding [operation review](navajo-operations-colour-transform-review-20261106.md). Reuse does not automatically accept new combinations; the whole new meanings and consumers were independently checked.

- [Wall/Morgan's primary dictionary](https://upload.wikimedia.org/wikipedia/commons/6/6c/Navajo-English_Dictionary.pdf) supports inside and other carried relations. [Wilson's primary dictionary](https://www.rexresearch1.com/NavajoLanguageLibrary/ConversationalNavajoDictionaryWilson.pdf), PDF 56/printed 99, directly supplies proportional-to; its work/purpose and original-state entries support the bounded memory/file constructions. Physical-to-digital extensions remain explicit.
- The [make paradigm](https://en.wiktionary.org/wiki/íílééh), revision 91652409, supplies the passive future used in new conditional/purpose/nonchange clauses, rather than invented tense. Existence/nonexistence labels distinguish an assigned from an absent ordinary Save target. The new from-image relation is supported by the cited derived-from postposition; full software sentences are authored, not dictionary quotations.
- [Young/Morgan's primary grammar](https://theswissbay.ch/pdf/Books/Linguistics/Mega%20linguistics%20pack/North%20American/Na-Dene/Navajo%3B%20The%20Navaho%20Language%20%28Young%20%26%20Morgan%29.pdf), PDF 34/printed 22, already independently inspected for the immediately preceding transform review, supports according-to. That component evidence is reused for the new governing-language composition without repeating the old review. Primary SHA-256: `2970097782bd17e39122f23aad38efac7955d3b95f35a11bb0336bf71f06061a`.

Confidence remains bounded contextual/source-compositional, not native-speaker certification or standardized software-vocabulary claims. Quoted action/property labels deliberately refer to existing UI names; long property chains and mathematical notation are not certified spoken-accessibility or installed-layout results. Technical identifiers such as bytes/PNG/Android are not counted as translated lexical vocabulary.

Exact accepted-map SHA-256 values:
- Eight-entry packet: `30b3ada32951cd5c89bed182e3b5583ed05d322cd679470a63a0bedff6c22453`.
- Three-P0 packet: `32b759aeff4d879b9516f7a723197eb8f25c340e20074785a8ebe0867b7a8da4`.
- Device policy: `152b605d7ef81257496dedda04f79c85c6d23d406bf11160b419beaaced36528`.

Canonical XML owns wording. No full-value approval mirrors or copied-source fixtures are introduced.

## Final checks and next gates

- All accepted values matched exact decisions; cited direct and supplementary production blobs match the base. Source values, required attributes, slots, Android escaping/format/literals, NFC and XML roundtrip pass. Exactly 12 absent keys added; all 279 previous values/attributes retained.
- **105 host tests passed** against final resources, and **570 actual JDK formatting cases passed** across 291 Navajo items. Fresh all-171 counts and `git diff --check` pass. This is structural/format verification, not renewed linguistic review of those 279 entries.
- No local Android SDK/Kotlin compiler: no AAPT/Gradle/Robolectric, installed glyph/layout, TalkBack, native comprehension or hosted exact-head CI/review pass is claimed. Long warnings and compound labels still need normal runtime checks. No develop merge, signing or release occurred.

Continue the remaining 56 priority meanings and the evidence union, retaining real holds and the [release gates](p0-p1-release-plan-20261106.md). Do not infer full completion from source-key presence, count unreviewed proposals, or reopen unchanged accepted catalogues.
