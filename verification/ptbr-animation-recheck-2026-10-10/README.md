# P07-007: bounded Brazilian Portuguese animation-warning review

Date: 10 October 2026. Inspected application source: `80c14372b0504bc44f9f2809ad477247fdc8100b`, tree `d9858229f98068bef9c6194c90d77610c5ecceec`.

## Result and limits

Seven resources have separate contextual dispositions in [dispositions.json](dispositions.json), with complete English/Portuguese text, immutable source links, historical values, placeholder checks and per-resource qualifications. This is a **model linguistic and direct-source review**, corroborated by primary terminology references. It is not native-speaker attestation, Android execution, catalogue acceptance or completion of P07-007. No native-speaker certification requirement is inferred.

The six body/count/action resources preserve the reviewed operation distinctions; no translation defect was identified in this bounded review. The title is a faithful translation but has an **open shared contextual caveat, A01**: “Animated image” / “Imagem animada” also heads the uncertain-detection dialog. The body explains uncertainty, but the title is more definite than the scanner's established result.

No translations, application source or tests are changed. Original scope/review/reset requirements are now partially recovered as recorded below; term-specific history, complete original-thread reconciliation and runtime validation remain pending. P07-007, P07-008, P07-009, CAT-040 and PR7 remain open. The authoritative [register](https://github.com/c933103/AN-Paint/blob/54557562afea97541e6a67d5a2dce93e2508e48c/verification/localization-recheck-register.md#L240-L242) is the source of the parent obligations. The existing [P07-008 clipboard evidence](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6093327556) remains separate.

## Seven individual dispositions

1. **P07-007-ANIM-01 — formats22_animation_title:** “Imagem animada” is the correct translation for confirmed animation. Keep A01 open for the uncertain branch.
2. **P07-007-ANIM-02 — formats22_animation_message:** “quadros” names animation frames; the sentence preserves the format/count placeholders and the warning that animation is not retained. Its plural is used only after at least two frames are established.
3. **P07-007-ANIM-03 — formats22_animation_unknown:** “confirmar se” preserves uncertainty and “não preservará nenhuma animação” preserves the limitation. “Complexo demais” refers to exceeding bounded inspection capability. The sentence describes the selected import mode if import succeeds, rather than guaranteeing that a malformed input decodes.
4. **P07-007-ANIM-04 — formats22_at_least_frames:** “pelo menos %1$d” remains a lower bound, composed into the outer string's %2$s argument. The zero/one-frame uncertainty body does not display this count.
5. **P07-007-ANIM-05 — formats22_animation_still:** “Apenas o primeiro quadro” correctly describes the selected first-frame branch. The saving sentence preserves the warning that the source animation is lost.
6. **P07-007-ANIM-06 — formats22_animation_poster:** “imagem padrão separada” and “no lugar dos quadros da animação” preserve APNG's separate static/default-image distinction. Calling it PNG is consistent with APNG being a PNG stream. This wording assessment is not an official Portuguese translation of the PNG specification.
7. **P07-007-ANIM-07 — formats22_open_still:** “Abrir imagem estática” is an appropriate action infinitive for proceeding with the single-image import. It does not promise animation playback. The related Cancel control remains “Cancelar”; that contextual control is checked without expanding the seven-resource acceptance scope.

Each JSON disposition gives its full reasoning. Equal source text and matching placeholders are inventory evidence, not the basis for linguistic acceptance.

## Source lineage and original discussion

[Correction 595bedb](https://github.com/c933103/AN-Paint/commit/595bedb6050064a5c37704eac16b3f6f46042c86) changes four of these resources from its parent `614f54a5dccfe806f5d8f9fc50d9f722da2f8d93`: message, unknown, still and poster. It replaces “fotogramas” with “quadros,” updates the uncertainty prose and changes the separate-image explanation to the current wording. This establishes the edit history; it does not prove every former synonym was incorrect.

All seven current pt-BR text values match that correction, original PR7 head `730319aea40eb205d18c894c496e500d6f660ac6`, and integration head `54557562afea97541e6a67d5a2dce93e2508e48c`. The complete catalogue blobs differ because other entries changed. [source-evidence.json](source-evidence.json) records every read source's exact Git blob, ref and URL.

The PR7 description, public discussion and review finding were inspected for the initial evidence pass. The public inline review concerns duplicate pt-PT configurations; its resolution history cannot accept these Portuguese meanings. The latest inspected comment before the initial evidence publication was [6093327556](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6093327556).

### Partial original-scope recovery, 10 October 2026

A later read-only recovery verified original owner-authored scope, review and reset requirements. The following bounded project-scope summary replaces any interpretation that the original requirements are wholly unrecovered:

- The original PR7 language scope is English variants, European Portuguese, Brazilian Portuguese, Italian, Greek and Turkish.
- Inherited Paintroid or other-app translations can contain known errors. They must not be treated as invariably correct or automatically preferred over independent review.
- Incomplete original language-thread work must be finished, and applicable shared application corrections must be propagated beyond only the originally selected language branches.
- The reset includes findings and updates outside PR reviews. Completing the other 81 locales is outside this reset scope.
- The rejected entire delivery requires individual full rechecks; prior progress and completion claims do not carry acceptance forward.

This establishes why the inherited Portuguese text needs an independent contextual review and why shared application findings cannot be confined to one language branch. It does not establish approval of any chosen Portuguese word or acceptance of the seven reviewed resources.

**Still missing:** no owner-specific clipboard or animation word-choice instruction has yet been recovered. Some assistant search hits lack readable exact-message anchors; complete latest-thread and alternate-branch reconciliation remain incomplete. An assistant search excerpt is not owner terminology evidence. No inference that additional instructions do not exist is made.

Only the project-scope paraphrase is published here. Private conversation transcripts, message identifiers and conversation links are excluded. This recovery changes no semantic disposition, runtime result, native-speaker claim, parent-row status or completion count.

## Primary linguistic and software references

- [GIMP's Brazilian-Portuguese GIF export documentation](https://docs.gimp.org/3.0/pt_BR/file-gif-export.html) uses “quadro” in animation-frame instructions. This partly untranslated page is used only for that Portuguese term.
- [Adobe's Brazilian-Portuguese application documentation](https://helpx.adobe.com/br/after-effects/desktop/work-with-other-applications/work-with-other-adobe-applications/effects-applications.html), section “Trocar imagens estáticas,” uses “imagens estáticas” and “quadros individuais.” These attest the terminology distinction, not the correctness of every AN Paint sentence.
- The [W3C PNG specification, sections 4.1 and 4.9.1](https://www.w3.org/TR/png-3/#apng-frame-based-animation), defines the static/default image and explains that it may be part of the animation or separate. That supports the APNG meaning reviewed here. Portuguese wording remains an explicitly identified model judgment.

All three were read on 10 October 2026. No external source certifies AN Paint's runtime behavior.

## Handler and decoder tracing

[ImportSelection.start](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L49-L66) inspects animation only after excluding PDF/TIFF page selection. A non-null animation result opens the warning; a null result proceeds with ordinary selection. Null can mean an unsupported, single-frame or malformed container, so it must not be reported as proof that all input is static.

[showAnimation](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L89-L96) selects:
- frameCount below two: the uncertainty body only;
- at least two frames: the known-animation message, exact or lower-bound count, followed by either the first-frame or separate-default-image paragraph.

[AnimationMetadata](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/AnimationMetadata.java) is a bounded metadata scanner. The work cap is 100,000 block operations, independent of file size. Valid prefixes at the cap can return incomplete counts; malformed probes normally return null. APNG records whether IDAT data preceded the first frame control. It does not decode pixels.

The positive button invokes [finishSelection(0)](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L69-L96), then constructs ImportedImage and hands it to the caller. The index alone does not select an APNG poster. [ImportedImage.decode](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageImport.kt) uses the static bitmap decode path for these formats. Existing decoder-test assertions separately distinguish expected first-frame pixels and APNG poster pixels. [ImageExporter](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageExporter.kt#L9-L27) accepts one Bitmap, consistent with the loss-of-animation warning; every codec's implementation has not been exhaustively audited here.

Cancel calls dispose and the cancellation callback; on-cancel uses the same path. [UiText.ui](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/UiText.kt#L13-L27) retrieves selected-app-language resources and delegates formatting to Android Resources. These are source-derived behavior statements, not observations from clicking a device.

## Composed-dialog examples

[composed-dialogs.json](composed-dialogs.json) contains complete English and pt-BR title, body and action texts for seven cases:

- D01: exact three-frame GIF
- D02: GIF with at least two proven frames
- D03: PNG with zero frames established before the work cap
- D04: GIF with one frame established before the work cap
- D05: three-frame APNG whose default image is its first animation frame
- D06: three-frame APNG with a separate default poster
- D07: exact three-frame WebP

Examples are mechanically composed from the actual resource text and handler branches. They are not screenshots, Android formatting tests or app execution. Their small substitution routine only covers the %s/%d arguments in these specific examples; it does not validate Android's general resource-formatting implementation.

## A01: shared title/body consistency remains open

An ordinary PNG with sufficiently many metadata chunks can yield `PNG|0|false|false`, as reflected in the production scanner and [existing fixture assertion](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/tools/test_animation_metadata.py#L174-L186). The same handler uses “Animated image” / “Imagem animada” even though the body says animation could not be confirmed. This source-established mismatch in definiteness is shared with English.

The body mitigates the ambiguity. No broken import, user harm, installed rendering failure or Portuguese-only mistranslation is established. A later authorized follow-through should decide whether the uncertain branch needs a conditional title and verify the complete displayed interaction. This evidence pass makes no source change and does not close A01.

## Verification actually performed

- Read complete named English/pt-BR source files, history snapshots, handler/scanner/import/export wrappers and test files through GitHub.
- Checked presence and exact ordered placeholder tokens for all seven resources.
- Checked all seven pt-BR values across correction, original PR7, integration and develop snapshots; four changed at the historical correction.
- Generated and inspected seven full dialog examples.
- Inspected assertions in all eleven host metadata test methods and four Android decoder tests.

**No host tests, Android build, resource compilation, lint, instrumentation or installed-device checks were executed for this pass.** No historical passing result is promoted to a fresh pass.

The host test source covers exact/lower-bound/unknown metadata outcomes but not localized UI. The four Android tests assert exactly three frames and one decoded pixel for GIF, WebP and both APNG outcomes; they do not select pt-BR or assert dialog wording. Their existence is not execution evidence.

## Remaining requirements and next validation

The recovered scope/review/reset requirements narrow the history gap. Term-specific instruction recovery, complete latest-thread/alternate-branch reconciliation, A01 disposition and fresh runtime evidence remain open. Future validation should exercise pt-BR exact/lower-bound/unknown dialogs, both APNG paths, Open/Cancel, accessibility and rendering, then run the applicable metadata/decoder tests on an exact source identity. Any approved title change must be propagated and rechecked in the affected shared/translated scope.

Other substantive pt-BR entries and full rewrite preservation require their own individual results. This seven-resource record does not change parent acceptance statuses or the reset register's completion count.
