# Author secondcheck / superseding candidate ledger

This ledger supersedes only the specified candidate cells, not application resources. Earlier batches remain visible as version 1 drafts. No linguistic acceptance is implied.

## Revision 2 — 2026-10-30

### non `ui_keep_editing23`

- Exact English: **Keep editing**.
- Version 1: `Halda áfram at breyta` — **withdrawn candidate**.
- Version 2 candidate: **`Halda fram breytingu`**.
- Backtranslation: **Continue the editing/alteration**.
- Confidence: **L**, pending independent specialist review of the activity-noun choice and UI idiom.
- Author assessment: reviewer objection is supported. Cleasby–Vigfusson [p. 233](https://www.germanic-lexicon-project.org/html/oi_cleasbyvigfusson/b0233.html) explicitly distinguishes modern `halda áfram` from historically cited `halda fram` with a dative activity object. The word order chosen follows the printed historical pattern with `fram` before the dative. `breytingu` is dative singular of the proposed action noun; the editing sense is a modern extension, **not a historical software phrase**. This means continue the activity, not perform the previous action again (`ui_redo`). `Halda breytingu fram` is also a candidate ordering, but is not the selected version 2.
- ang is unchanged. No blanket change of feminine plural `-e` to `-a` is authorized or made in this secondcheck.

### non `ui_export_did_not_save23`

This later version 1 row independently inherited the same `halda áfram` problem. Replace its final clause only:

- Version 1 full candidate: `Hið útfœrða verk var gert. Nýt «Varðveita» eða «Varðveita sem» til at varðveita núverandi mynd áðr en þú heldr áfram.`
- Version 2 full candidate: **`Hið útfœrða verk var gert. Nýt «Varðveita» eða «Varðveita sem» til at varðveita núverandi mynd áðr en þú heldr fram verki þínu.`**
- Backtranslation: **The export output was created. Use Save or Save as to save the current image before you continue your work.**
- Confidence: **L**. Same dative activity construction; `verki þínu` makes continuing the work explicit. All source safety clauses remain.

### `eptirrit`: terminology status correction, not historical attestation

Reviewer objection is supported by Cleasby–Vigfusson [p. 131](https://www.germanic-lexicon-project.org/html/oi_cleasbyvigfusson/b0131.html): `eptir-rit` is marked modern. Therefore the version 1 glossary description “technical extension” was insufficient and must not be read as a medieval attestation claim.

**Version 2 proposed convention:** retain `eptirrit` only as an **explicitly modern/reconstructed compound**, formed from historical `eptir` + `rit`, with the new computational meaning “copy of an image/file/archive”. It is not a securely medieval whole-word base. The rationale is a short consistent copy term across image, ZIP and clipboard operations; merely saying “another image” would falsely exclude recovery archives. The choice is provisional and may be rejected by a historical-language reviewer. Its coincidence with later Icelandic copy vocabulary is disclosed, not used to claim medieval occurrence or to substitute modern Icelandic prose.

Affected recovery-control version 2 cells retain the same surface wording but have changed evidence status:

| Key | Exact English | non version 2 candidate | Backtranslation | Rationale / confidence |
|---|---|---|---|---|
| ui_export_recovery_copy | Export recovery copy… | Fœra út eptirrit til viðgerðar… | Export a copy for restoration… | `eptirrit` explicitly modern/reconstructed, NOT attested medieval whole word; N,S; L |
| ui_export_recovery_copy_144b8a | Export recovery copy | Fœra út eptirrit til viðgerðar | Export a copy for restoration | Same provisional convention; N,S; L |
| ui_could_not_export_the_recovery_copy | Could not export the recovery copy | Eigi mátti fœra út eptirritit til viðgerðar | Could not export the restoration copy | Same convention; failure not success; N,S; L |

This status applies to **every** inflected `eptirrit` occurrence in batches 1–6, not just these three rows. It is a proposed coinage convention requiring acceptance, not a waived linguistic gate.

### ang `efenwyrht`

Bosworth–Toller [wyrht](https://bosworthtoller.com/36971) identifies the historical base as feminine. The draft's proposed feminine gender is therefore grounded in that base. The compound `efenwyrht` and its computing-copy suitability remain **unverified modern coinage**, L confidence. No whole-compound attestation is claimed.

### Additional checks, not acceptance

- Bosworth–Toller [ge-mynd](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0419.html) permits neuter and feminine. This draft chooses feminine consistently, so batch 2 was internally corrected to `maran gemynde`; the alternative neuter lexeme itself is not an error.
- Bosworth–Toller [p. 7 via public-domain dictionary](https://keithbriggs.info/documents/Bosworth-Toller.pdf) supports `adilegian` as blot out/destroy. Its digital-clear application remains modern.
- Zoëga [hætta](https://norroen.info/dct/zoega/h.html) supports cease with dative or infinitive; it does not itself attest the draft's complete `hætta við` label. That exact idiom remains L and needs review, not a silently promoted M.
- Avoid the initially suggested `bráðabirgðageymsla` buffer compound in new rows. The drafted sentences instead use **`geymsla um hríð`** (“storage for a while”), still a modern technical phrase. This avoids an unexplained modern-Icelandic technical substitution.

## Revision 3 — source-supported case and temporary-pause corrections

### non `ui_share_explanation34`

- Exact English: `Save a copy to your chosen location, then choose an app to share it. Your current Save destination stays unchanged.`
- Version 1: `Varðveit eptirrit á vǫldum stað þínum; vel þá verkfæri til at deila því. Núverandi «Varðveita»-staðr þinn er óbreyttr.` — superseded.
- **Version 2 full candidate:** `Varðveit eptirrit á vǫldum stað þínum; vel þá verkfæri til at deila þat. Núverandi «Varðveita»-staðr þinn er óbreyttr.`
- Backtranslation: **Save a copy at your chosen place; then choose an application to share that copy. Your current Save location is unchanged.**
- Author assessment: C&V [DEILA p. 98](https://www.germanic-lexicon-project.org/html/oi_cleasbyvigfusson/b0098.html) explicitly prescribes accusative, not dative, for divide/deal. `þat` is neuter accusative referring to `eptirrit`, not the app. Digital sharing remains a new metaphor and the compound retains its disclosed modern/reconstructed status. **L**, not accepted.

### non `ui_share_saved_image` — same case error found in batch 4

- Exact English: `Share saved image`.
- Version 1 `Deila varðveittri mynd` is superseded.
- **Version 2 full candidate:** `Deila varðveitta mynd`.
- Backtranslation: **Share a saved image**.
- Accusative feminine noun phrase, same DEILA evidence. Digital-share sense is new. **L**, not accepted.

### ang `ui_autosave_paused_use_save`

- Exact English: `Autosave paused · use Save`.
- Version 1 `Sylfhealdung abiden · bruc «Healdan»` is withdrawn: `abiden` was not a reliable passive for paused.
- **Version 2 full candidate:** `Sylfhealdung is hwilendlice oþstilled · bruc «Healdan»`.
- Backtranslation: **Autosave is temporarily stopped · use Save**.
- Author assessment: [B–T oþ-stillan, p. 770](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0770.html) documents a stopping verb with passive `oþstilled`. [B–T hwílend-líc, p. 576](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0576.html) documents temporary/lasting only a time. `hwilendlice` here is a productively formed adverb from that base, **not claimed as an exact independently attested UI phrase**. Unlike `abiden`, this directly encodes stopping; it makes no promise of automatic restart or specific duration. **L** pending specialist idiom review.

### ang `ui_autosave_is_paused_to_protect_that_draft_use`

- Exact English: `%1$s Autosave is paused to protect that draft. Use “File → Export recovery copy…” to keep it, and “File → Save as…” (File format: PNG / JPEG) to save your current work.`
- **Version 2 full candidate:** `%1$s Sylfhealdung is hwilendlice oþstilled þæt þæt weorcgewrit gehealden beo. Bruc «Gewrit → Utberan efenwyrhte to eftstaþelunge…» þæt þu hit healde, and «Gewrit → Healdan swa…» (Gewrites hiw: PNG / JPEG) þæt þu þin andwearde weorc healde.`
- Backtranslation: **%1$s Autosave is temporarily stopped so that that draft is protected. Use File → Export recovery copy to keep it, and File → Save as (File format: PNG / JPEG) to save your current work.**
- Supersedes version 1's `is abiden` only; recovery/current-work distinction, literal formats and placeholder retained. Same primary lexical basis as preceding row; all compounds and complete syntax remain **L**, unaccepted.

## Revision 4 — one pixel paradigm and remaining concrete grammar findings

Primary checks: [C&V hlutr p. 273](https://www.germanic-lexicon-project.org/html/oi_cleasbyvigfusson/b0273.html) gives ordinary nominative plural `hlutir`, accusative plural `hluti`. The pixel coinage is consistently **strong masculine `myndhlutr`**, not the separate weak `hluti` used for selected portion. Nominative singular `myndhlutr`, accusative singular `myndhlut`, dative singular `myndhlut`, genitive singular `myndhlutar`; plural nominative `myndhlutir`, accusative `myndhluti`, dative `myndhlutum`, genitive `myndhluta`. The compound and its pixel sense remain new, L. No claim that `myndhlutr` is an attested historical word.

Exact non version 2 replacement cells:

| Key | Exact English | Full non v2 candidate | Backtranslation | Case / rationale |
|---|---|---|---|---|
| ui_autosave_pixels_are_missing | Autosave pixels are missing. | Myndhluti sjálfvarðveizlu vantar. | Autosave pixels are missing. | Accusative plural with impersonal vantar |
| ui_autosave_pixels_could_not_be_read | Autosave pixels could not be read. | Eigi mátti lesa myndhluti sjálfvarðveizlu. | Autosave pixels could not be read. | Accusative plural object of lesa |
| ui_d_d_pixels_2f_mp_exceeds_the_current | %1$d × %2$d pixels (%3$.2f MP) exceeds the current safe editing budget of %4$.2f MP. AN Paint keeps the complete image in memory and reserves space for transforms and selections. Available memory determines this budget. The operation was stopped before allocating the oversized bitmap. No automatic resizing was applied. | %1$d × %2$d myndhlutir (%3$.2f MP) fara yfir núverandi öruggt mark til breytinga, %4$.2f MP. AN Paint heldr allri myndinni í minni ok tekr rúm frá til ummyndana ok valinna hluta. Þat minni er laust er setr þetta mark. Verkit var stöðvat áðr en rúm var fengit hinni of stóru myndhlutamynd. Engin sjálfvirk stærðarbreyting var gerð. | %1$d × %2$d pixels (%3$.2f MP) exceed the current safe edit limit of %4$.2f MP. Full image and transform/selection space are retained in memory; available memory sets limit. Work stopped before oversized allocation. No automatic resize. | Nominative plural subject; all safety clauses and placeholders unchanged |
| formats22_pdf_raster_hint | PDF pages are rendered at 144 dpi. Text and vector objects become pixels. | PDF-blǫð eru mynduð við 144 dpi. Rit ok línugerðir hlutir verða myndhlutir. | PDF pages rendered at 144 dpi. Text and vector objects become pixels. | Nominative plural predicative after verða |
| ui_pixels | Pixels | Myndhlutir | Pixels | Nominative plural label |
| ui_pixels_6ec9c2 | pixels | myndhlutir | pixels | Lower-case nominative plural label |
| ui_size_pixels | Size (pixels) | Stærð (myndhlutir) | Size (pixels) | Parenthetic unit label nominative plural |

Every listed replacement is **L**. Genitive plural `myndhluta` in a phrase such as `tal myndhluta` is retained; no blind global replacement is valid.

### ang `ui_previous_draft_kept_for_recovery`

- Exact English: `Previous draft kept for recovery`.
- **Full v2:** `Ærre weorcgewrit gehealden to eftstaþelunge`.
- Backtranslation: **Previous working draft kept for restoration**.
- `Ærra` was masculine; declared neuter `weorcgewrit` requires `ærre` here. [B–T ǽr](https://bosworthtoller.com/731) explicitly lists feminine/neuter comparative `ǽre/ǽrre`. L because draft/recovery compounds remain provisional.

### ang `gallery_credit_too_large`

- Exact English: `These image credits would make the drawing too large to restore. Your previous drawing and credits have been kept.`
- **Full v2:** `Þas wyrhtgetalu þære anlicnesse woldon don þa metinge to micle to eftstaþelunge. Þin ærre meting and hire wyrhtgetalu sind gehealdene.`
- Backtranslation: **These image-credit records would make the drawing too large to restore. Your previous drawing and its credits have been kept.**
- `þa metinge` is accusative feminine; predicative `micle` is accusative feminine, replacing dative `micelre`. `to` here means too, not the preposition governing the adjective. Complete syntax and compounds remain L, unaccepted.

### non `ui_the_draft_is_saving_try_again_shortly`

- Exact English: `The draft is saving. Try again shortly.`
- **Full v2:** `AN Paint varðveitir nú vinnuritit. Reyn aptr innan skamms.`
- Backtranslation: **AN Paint is saving the draft now. Try again shortly.**
- Explicit known application subject and ordinary present + `nú` avoid the unverified impersonal `Nú er verit at ...` construction. This is **not** a blanket claim that historical `vera at` + infinitive is invalid. L: activity-in-progress reading and draft term need review, but no false completion is asserted.

### non proportion terminology — author preventive correction

The same C&V p. 273 explicitly marks `hlutfall` in the proportion sense modern, but separately records `hlutfelling` as proportion. Prefer the historically grounded noun with a new UI sense:

- `ui_lock_aspect_ratio`, exact English `Lock aspect ratio`: **`Festa hlutfellingu breiddar ok hæðar`**; backtranslation **Lock the proportion of width and height**; v2, L.
- `ui_lock_proportions`, exact English `Lock proportions`: **`Festa hlutfellingar`**; backtranslation **Lock the proportions**; v2, L.

This is a proposed terminology improvement, not accepted wording. The data-resizing constraint remains a modern application of the historical noun.

## Revision 5 — passive completion and historical “only”

### ang `ui_higher_quality_usually_makes_a_larger_file_lossless`

- Exact English: `Higher quality usually makes a larger file. Lossless keeps every colour value.`
- **Full v2 candidate:** `Betere godnes wyrcþ gewunelice mare gewrit. Butan lyre gehealden biþ ælc hiwgetæl.`
- Backtranslation: **Higher quality usually makes a larger file. Without loss every colour value is preserved.**
- Author assessment: `geheald` in v1 was not the intended passive participle; `gehealden` is the required form for the proposed healdan convention. Retains every value, not merely more detail. L: quality/value compounds and clause idiom still unaccepted.

### non `formats22_animation_unknown`

- Exact English: `This %1$s is too complex to confirm whether it contains multiple frames. AN Paint will open only a still image and will not preserve any animation.`
- **Full v2 candidate:** `Þetta %1$s er of flókit til at staðfesta hvárt þat hefir fleiri myndskeið. AN Paint mun opna at eins kyrra mynd ok eigi varðveita neina hreyfingu.`
- Backtranslation: **This %1$s is too complex to confirm whether it has multiple frames. AN Paint will open only a still image and preserve no animation.**
- C&V [EINN, VI.1, transcription](https://norroen.info/dct/cleasby/e.html) cites historical `at eins` for only; modern normalized `aðeins` in v1 is superseded. Placeholder, unresolved frame count, still-only opening and loss of animation retained. L: frame/animation terminology and sentence remain unaccepted.

## Revision 6 — painting morphology, zoom false friend, complexity and “alone” scope

### ang `formats22_pdf_raster_hint`

- Exact English: `PDF pages are rendered at 144 dpi. Text and vector objects become pixels.`
- **Full v2 candidate:** `PDF-leaf beoþ gemet æt 144 dpi. Gewrit and striclæce þing weorþaþ anlicnesprican.`
- Backtranslation: **PDF pages are rendered at 144 dpi. Text and vector objects become pixels.**
- Author assessment: [B–T ge-metan](https://bosworthtoller.com/15222) explicitly gives painting preterite `-mette`, participle `-mett/-met`. V1 `gemetod` is withdrawn. V2 selects attested bare verbal participle `gemet` with the passive, not an invented `gemeted`. Whether a specialist prefers an inflected predicative participle in this sentence remains a review question. Digital rendering and vector terminology are modern senses; **L**. No “verified published UI phrase” claim.

### ang zoom/view-scale family

V1 `mærsian/gemærsode` was a false-friend choice: celebration/extolling does not establish optical enlargement. It is withdrawn everywhere it occurred (two rows). V2 uses the explicit **viewing-scale** coinage `gesihþmicelnes` and physical size/increase vocabulary rather than praise. [B–T micel-ness p. 683](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0683.html) documents physical size; [B–T écan in Dictionary E](https://lrc.la.utexas.edu/books/asd/dict-E) documents transitive increase/add. The UI compound is still newly proposed.

| Key | Exact English | Full ang v2 candidate | Backtranslation | Confidence |
|---|---|---|---|---|
| ui_zoom_in | Zoom in | Ecan gesihþmicelnesse | Increase the viewing scale | L |
| ui_zoom_out | Zoom out | Læssian gesihþmicelnesse | Decrease the viewing scale | L |
| ui_show_magnified_drawing_preview | Show magnified drawing preview | Ætywan metinge foresceawunge on maran gesihþmicelnesse | Show drawing preview at a greater viewing scale | L |

`ui_zoom_out` is harmonized to the same scale object; the old cell was not a praise false friend. These candidates must not be used as synonyms for resampling image pixels. No data dimensions change is asserted.

### ang additive labels — related transitivity check

The same primary lookup distinguishes intransitive strong `eácan` from transitive weak `écan`. With length marks omitted by policy, select **Ecan**, not v1 Eacan:

| Key | Exact English | Full ang v2 candidate | Backtranslation | Confidence |
|---|---|---|---|---|
| ui_add_text | Add text | Ecan gewrit | Add text | L |
| ui_add_colour26 | Add colour | Ecan hiw | Add colour | L |

These are author-identified consistency repairs, not an expansion of scope.

### ang `formats22_animation_unknown`

- Exact English: `This %1$s is too complex to confirm whether it contains multiple frames. AN Paint will open only a still image and will not preserve any animation.`
- **Full v2 candidate:** `Þis %1$s is swa earfoðe to oncnawenne þæt man ne mæg gewissian hwæþer hit hæfþ ma anlicnessticca. AN Paint openaþ ane stille anlicnesse and ne hylt nane styrunge.`
- Backtranslation: **This %1$s is so difficult to interpret that it cannot be confirmed whether it contains multiple frames. AN Paint opens only a still image and preserves no animation.**
- [B–T ge-þwǽrian](https://bosworthtoller.com/16533) means make accordant/mild, not complex: v1 `geþwæred` is withdrawn. [B–T earfoþe supplement p. 171](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/d0171.html) documents difficult and constructions for difficulty of knowing/understanding. V2 paraphrases complexity as **difficulty of interpreting the file**, not uncertainty about the number itself alone. Placeholder, unknown multi-frame status, still-only opening and animation loss preserved. **L**, pending exact sentence review.

### non `ui_assembly_source_memory_floor`

- Exact English: `This assembly is estimated to exceed the current working-memory budget, even at the smallest output size. Reducing the assembly dimensions alone is not enough under the current limits. Close other documents or prepare a smaller source image before trying again. Your assembly is unchanged.`
- **Full v2 candidate:** `Ætlat er at þessi samsetning fari yfir núverandi mark vinnuminnis, jafnvel við minnstu stærð útkomu. Eigi nægir undir núverandi mǫrkum at minnka at eins stærðir samsetningarinnar. Lúk ǫðrum ritum eða bú til minni frummynd áðr en þú reynir aptr. Samsetning þín er óbreytt.`
- Backtranslation: **This assembly is estimated to exceed the current working-memory limit even at minimum output size. Under current limits it is not enough to reduce only the assembly dimensions. Close other documents or prepare a smaller source image before retrying. Your assembly is unchanged.**
- V1 genitive `samsetningar einnar` incorrectly attached “alone” to assembly. V2 puts historical `at eins` immediately with the dimension-reduction object, not the assembly's identity. No source-file remedy or original-retention promise is omitted; no assertion that output-only reduction succeeds. **L**, exact scope still requires independent second review.

## Revision 7 — explicit dithering subject, lost detail, free-form case and pixel genitives

These are **exact candidate overrides, all L and unaccepted**. Limited repairs do not certify the remaining clauses. No Norse `tvá fingr` correction is proposed: that historical form is not an error merely because it differs from modern normalization.

### ang `save20_gif_description`

- Exact English: `Still image, up to 256 colours. Dithering smooths colour gradients. Animated GIFs open as their first frame.`
- **Full v2 candidate:** `Stille anlicnes, oþ 256 hiwa. Gemengung hiwpricena gesmeþaþ hiwa stæpmæle awendinga. Styriende GIF-gewritu openiaþ swa heora forme anlicnessticce.`
- Backtranslation: **Still image, up to 256 colours. Mixing colour dots smooths gradual colour changes. Animated GIF files open as their first frame.**
- Replaces the opaque infinitival subject with explicit singular feminine `Gemengung`; [B–T Dictionary G, ge-mengung](https://lrc.la.utexas.edu/books/asd/dict-G) records the mixing noun. `hiwpricena` is genitive plural of the proposed colour-dot compound. The new technical sense describes dithering, not palette blending as an independently accepted algorithm name.
- **Agreement qualification:** the finding must not be recorded as “-aþ is necessarily plural.” Weak-II singular `sméðaþ` is attested with singular `þæt neb` in [B–T Dictionary S, sméðian](https://lrc.la.utexas.edu/books/asd/dict-S). [B–T ge-sméþian transcription](https://oldenglishdictionary.net/home/word/ge-sm%C3%A9%C3%BEian) gives the prefixed smoothing verb with past `-ode`. The v2 keeps `gesmeþaþ` as a weak-II third-person singular form; its subject is now unambiguous. Modern image-gradient meaning remains a proposal. **L**; 256 colours and first-frame-only behavior are retained, not an animation preservation promise.

### ang `ui_sampled_resize_memory_explanation`

- Exact English: `Estimates include the current canvas and clipboard, sampled decoding and editing buffers. Actual memory use varies. A smaller copy loses detail. The original file stays unchanged.`
- **Full v2 candidate:** `Þa ætlanunga habbaþ mid þæt andwearde metingbord and þæt efenwyrhta hord, dælmæle tacnonrædinge and hwilendlice hord to awendinge. Soþ gemyndbrucung wrixlaþ. Læsse efenwyrht forlyst smæle dælas. Þæt frumgewrit wunigeþ unawend.`
- Backtranslation: **The estimates include the current canvas and clipboard, sampled decoding and temporary editing stores. Actual memory use varies. A smaller copy loses fine details. The original file remains unchanged.**
- The lost details are now accusative plural `smæle dælas`, replacing unsupported genitive `smælra dæla`. [B–T for-leósan, p. 314](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0314.html) documents accusative objects and singular `forlýst`. This does not claim accusative is the only government ever attested. The mathematical memory estimates, variation, detail loss and unchanged original remain distinct. **L**; decoder/buffer compounds and wider sentence idiom are still held for review.

### ang `ui_free_form_select`

- Exact English: `Free-form select`
- **Full v2 candidate:** `Ceosan dæl mid freoum hiwe`
- Backtranslation: **Select a portion with free shape.**
- `mid` + chosen neuter `hiw` has dative `hiwe`; use compatible adjective `freoum`, not v1 `frige`. [B–T freó](https://bosworthtoller.com/46387) documents singular dative/instrumental-compatible forms such as `frióum anwalde` and `fríum cyre`. The shape-not-constrained-to-a-rectangle UI sense is new. **L**.

### ang `ui_codec_resize_memory_floor`

- Exact English: `This format must decode its source image or source tiles before resizing. A smaller output may still exceed available memory.`
- **Full v2 candidate:** `Þis hiw sceal onrædan his frumanlicnesse oþþe hire frumdælas ær micelnesse awendinge. Læsse utweorc mæg þeah oferstigan þa gemynd þe to brucenne is.`
- Backtranslation: **This format must decode its source image or its source tiles before resizing. A smaller output may nevertheless exceed the available memory.**
- Replaces `frumdæla` with accusative plural `frumdælas`, coordinated with the decoded image as direct object. `hire` continues to refer to the feminine source image. This is a case repair under the proposed transitive decoding sense, **not** independent historical attestation of `onrædan` as decode. That technical verb/compound family remains explicitly unverified and requires terminology review. **L**; pre-resize decoding floor and possibility of memory failure despite smaller output are retained.

### ang weak-pixel genitive plural — three complete overrides

[B–T Dictionary P, prica](https://lrc.la.utexas.edu/books/asd/dict-P) explicitly gives masculine `prica, an` and documents genitive plural `pricena`. For the already-declared weak-masculine compound `anlicnesprica`, keep nominative/accusative plural `anlicnesprican` and genitive plural **`anlicnespricena`**. Do not substitute a strong declension or change every occurrence of the compound stem. `bruc` is being used with the genitive in these proposed instructions.

| Key | Exact English | Full ang v2 candidate | Backtranslation | Confidence |
|---|---|---|---|---|
| ui_d_d_px_d_pixels_2f_mp | %1$d × %2$d px · Pixel count: %3$,d (%4$.2f MP) | %1$d × %2$d px · Anlicnespricena getæl: %3$,d (%4$.2f MP) | Dimensions in px; count of pixels: %3$,d (%4$.2f MP) | L |
| ui_use_1_1024_pixels | Use 1–1024 pixels. | Bruc 1–1024 anlicnespricena. | Use 1–1024 pixels. | L |
| ui_trim_amounts_must_fit_inside_each_image_use | Trim amounts must fit inside each image; use whole pixels or percentages. | Snidinggemetu sceolon gefegan innan ælcre anlicnesse; bruc halra anlicnespricena oþþe hunddæla. | Trim amounts must fit inside each image; use whole pixels or percentages. | L |

Numbered placeholders, grouping comma, range, `px` and `MP` are unchanged. The pixel compound and decimal-percent convention remain modern proposals, not historically established units.

## Revision 8 — explicit decoding terminology proposal after the lexical hold

Author follow-up, not independent acceptance: withdraw the **unverified `onrædan/tacnonræd-` formation** rather than imply that its base is historically established. A failed lookup is not proof that no such form could occur, but there is no reason to rely on it here. Prefer attested [B–T á-rǽdan](https://bosworthtoller.com/38876), reading/interpreting what is written, here explicitly assigned a new image-data decoding sense; [B–T Dictionary R](https://lrc.la.utexas.edu/books/asd/dict-R) records `ræding` f. reading and `rædere` m. reader. These support new **`tacnræding`** f. encoded-sign reading/decoding and **`tacnrædere`** m. encoded-sign reader/decoder, not historically attested computing senses. The digital-data interpretation is a defined proposed convention. All five rows remain **L**; in particular, specialists must judge whether the technical distinctions are intelligible.

These exact v3/v2 candidates supersede the ANG cells below, including the freshly repaired v2 sampled-resize and codec-floor cells in revision 7. Their existing accusative case corrections are retained. No NON cell is altered.

| Key | Exact English | Full ang candidate | Backtranslation | Version / confidence |
|---|---|---|---|---|
| ui_android_could_not_decode_this_image | Android could not decode this image. | Android ne mihte þisse anlicnesse tacngewrit arædan. | Android could not interpret/decode this image's encoded data. | v2 / L |
| ui_the_decoder_and_editing_buffers_need_about_the | The decoder and editing buffers need about %1$s; the current safe editing budget is %2$s. Choose a smaller copy. | Se tacnrædere and þa hwilendlican hord to awendinge þurfon be %1$s; þæt andwearde orsorge awendinggemet is %2$s. Ceos læssan efenwyrhte. | The decoder and temporary editing stores need about %1$s; the current safe editing limit is %2$s. Choose a smaller copy. | v2 / L |
| colour_unsupported_icc_model | This image uses an ICC colour model that the image decoder cannot convert. Export an RGB copy in a colour-managed application first. | Þeos anlicnes bricþ ICC-hiwgebisnes þe se anlicnesse tacnrædere ne mæg awendan. Utber ærest RGB-efenwyrhte on weorctole þe hiwum stiereþ. | This image uses an ICC colour model the image decoder cannot convert. First export an RGB copy in an application that manages colours. | v2 / L |
| ui_codec_resize_memory_floor | This format must decode its source image or source tiles before resizing. A smaller output may still exceed available memory. | Þis hiw sceal arædan his frumanlicnesse oþþe hire frumdælas ær micelnesse awendinge. Læsse utweorc mæg þeah oferstigan þa gemynd þe to brucenne is. | This format must decode its source image or its source tiles before resizing. A smaller output may nevertheless exceed available memory. | v3 / L |
| ui_sampled_resize_memory_explanation | Estimates include the current canvas and clipboard, sampled decoding and editing buffers. Actual memory use varies. A smaller copy loses detail. The original file stays unchanged. | Þa ætlanunga habbaþ mid þæt andwearde metingbord and þæt efenwyrhta hord, dælmæle tacnrædinge and hwilendlice hord to awendinge. Soþ gemyndbrucung wrixlaþ. Læsse efenwyrht forlyst smæle dælas. Þæt frumgewrit wunigeþ unawend. | Estimates include the current canvas and clipboard, sampled decoding and temporary editing stores. Actual memory use varies. A smaller copy loses fine details. The original file remains unchanged. | v3 / L |

**Codec-floor case distinction:** v3 retains the coordinated direct objects `his frumanlicnesse` and `hire frumdælas` from the corrected v2; both depend on transitive `arædan` in its newly proposed decoding sense. No genitive direct object is reintroduced. The necessity before resizing, tentative memory exceedance, and all literals/placeholders remain unchanged in intended meaning. The dictionary establishes the interpreting verb, not the digital-image object construction.

## Revision 9 — category plural, enabled-app state and colour-model lemma

### ang `ui_tool_categories`

- Exact English: `Tool categories. Scroll to see more tools`
- **Full v2 candidate:** `Tolcynn. Scrid þæt þu ma tola geseo`
- Backtranslation: **Tool categories. Scroll to see more tools.**
- [B–T Dictionary C, CYN/CYNN](https://lrc.la.utexas.edu/books/asd/dict-C) gives neuter `cynn` and explicit plural `twá cynn`. Select new compound `tolcynn`, neuter, nominative/accusative plural `tolcynn`, not unsubstantiated v1 `tolcynnu`. The compound is a proposed category term, not a cited historical software word. **L**.

### ang `ui_android_could_not_find_a_file_picker_enable`

- Exact English: `Android could not find a file picker. Enable the Files or Documents app in Android settings, then try again.`
- **Full v2 candidate:** `Android ne mihte gewritceosere findan. On Android-gesetnessum do þæt weorctol «Files» oþþe «Documents» gearu to brucenne, þæt hit weorcan mæge; costna þonne eft.`
- Backtranslation: **Android could not find a file chooser. In Android settings make the Files or Documents app ready/available for use so that it can operate; then try again.**
- V1 `Ongin` (“begin/start”) is withdrawn: launching the app is not the required action. The v2 specifies a Settings change to its usable/operable state, not opening it, starting a process, granting access to a particular file, or installing a different picker. [B–T gearo/gearu](https://bosworthtoller.com/13504) supports prepared/ready state; its **enabled/usable application-state sense is newly proposed**, not historical software terminology. Neuter `weorctol` takes predicative `gearu`; the purpose clause expresses ability, not a claim that the app is already running. **L**, particularly the risk that “ready for use” remains less explicit to readers than a separately standardized Enable label. Independent reviewer must assess that source-specific state meaning; the backtranslation alone is not proof.

### ang `colour_unsupported_icc_model` — replace undocumented model lemma

- Exact English: `This image uses an ICC colour model that the image decoder cannot convert. Export an RGB copy in a colour-managed application first.`
- **Full v3 candidate:** `Þeos anlicnes bricþ ICC-hiwbisene þe se anlicnesse tacnrædere ne mæg awendan. Utber ærest RGB-efenwyrhte on weorctole þe hiwum stiereþ.`
- Backtranslation: **This image uses an ICC colour model that the image decoder cannot convert. First export an RGB copy in a colour-managed application.**
- V1/v2 did not adequately establish the lemma/gender behind `hiwgebisnes`. It is **withdrawn**, not retroactively certified as a neuter noun just to justify `-es`.
- New explicit convention: **`hiwbisen` f.**, a new colour-model compound built from historical **`bisen` f. (genitive `bisene`)**, documented as an exemplar/model/pattern in [B–T bisen](https://bosworthtoller.com/40422). Select the uncontracted feminine pattern for this compound: singular nominative `hiwbisen`, accusative/genitive/dative `hiwbisene`; plural nominative/accusative/genitive `hiwbisena`, dative `hiwbisenum`. This is a proposed editorial paradigm; the dictionary also records other variants, not a reason to mix paradigms in one glossary.
- The row's `ICC-hiwbisene` is **genitive singular governed by `bricþ`** under the chosen use-verb convention. `tacnrædere` carries revision 8's new decoder sense. ICC model, inability to convert, RGB export remedy, colour-managed application and first-step ordering are retained. **L**, including whether “model/pattern” is intelligible for a mathematical colour representation.
