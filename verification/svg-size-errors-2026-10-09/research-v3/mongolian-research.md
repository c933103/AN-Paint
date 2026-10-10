# Traditional Mongolian SVG-size messages: bounded v3 review

## Result

A complete **review-only** `mn-Mong` pair is now supported well enough to submit for independent composition review. `proposed-pair.json` is the authoritative candidate in this folder. No native acceptance or production readiness is claimed.

The earlier v2 pass's null pair is preserved. The change in assessment comes from examining the full 688-entry exact-locale catalogue, especially its long help, source conditions, normalization, animation substitution and save/error clauses, plus newly obtained primary evidence for **based on** and completed negation. It does not come from treating an old catalogue as automatically correct or requiring an existing corpus to contain these exact UI sentences.

## Candidate text

### No usable original declaration / no canvas-derived substitute

SVG ᠨᠢ ᠠᠰᠢᠭᠯᠠᠵᠤ ᠪᠣᠯᠬᠤ ᠠᠩᠬᠠᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠵᠢᠭᠠᠭ᠎ᠠ ᠦᠭᠡᠢ᠃ ᠲᠡᠭᠦᠨ ᠦ ᠣᠷᠣᠨ ᠳᠤ ᠵᠢᠷᠤᠭ ᠤᠨ ᠲᠠᠯᠪᠠᠢ ᠶᠢᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠳᠦ ᠦᠨᠳᠦᠰᠦᠯᠡᠭᠰᠡᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠠᠰᠢᠭᠯᠠᠭᠰᠠᠨ ᠦᠭᠡᠢ᠃

Backtranslation: The SVG has not specified an original size that can be used. In its place, a size based on the drawing canvas's size was not used.

### Original size above Android bitmap dimensions / no completed resize

SVG ᠵᠢᠷᠤᠭ ᠤᠨ ᠠᠩᠬᠠᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ Android ᠤᠨ bitmap ᠵᠢᠷᠤᠭ ᠤᠨ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠶᠢᠨ ᠬᠢᠵᠠᠭᠠᠷ ᠠᠴᠠ ᠬᠡᠲᠦᠷᠡᠪᠡ᠃ ᠬᠡᠮᠵᠢᠶ᠎ᠡ ᠶᠢ ᠥᠭᠡᠷᠡᠴᠢᠯᠡᠭᠰᠡᠨ ᠦᠭᠡᠢ᠃

Backtranslation: The original size of the SVG image exceeded the size limit of Android bitmap images. The size was not changed.

## Evidence by semantic clause

### 1. SVG specifies no usable original size

`ui_gallery_artwork_catrobat_and_its_credited_creators_cc` already has a source subject followed by “other terms” and `ᠵᠢᠭᠠᠭ᠎ᠠ ᠦᠭᠡᠢ ᠪᠣᠯ`, meaning unless the source specifies separate terms. The proposal removes the conditional and supplies the new object. This is an ordinary indicating/specifying predicate, not a new technical word for XML declaration. The [Academy dictionary's ЗААХ entry](https://mongoltoli.mn/search.php?opt=1&ug_id=44533&word=%D0%97%D0%90%D0%90%D0%A5) supports the indicate/make-known semantic family; the exact traditional inflected form comes from the catalogue, not from transliterating the Cyrillic headword.

`ui_no_readable_image_data` supplies the pre-nominal “read + converb + can” construction. `colour_unsupported_icc_model` supplies exact `ᠠᠰᠢᠭᠯᠠᠵᠤ` (using). Combining it with `ᠪᠣᠯᠬᠤ` gives “that can be used.” `ui_original_size34` supplies the exact original-size phrase, while `ui_help23` explicitly links it to restoring source dimensions.

The negative therefore permits an SVG to contain an invalid/unusable dimension declaration. It denies a **usable original** declaration; it does not say the SVG has no declarations at all.

### 2. No canvas-based size used in its place

`ui_canvas_size_30460e` supplies the full canvas-size noun phrase and its genitives. The normalization help was inspected, including its “calculate relative to” construction. That wording is not forced into this sentence, because doing so could imply a specific proportional calculation absent from the source.

The [Academy dictionary's ҮНДЭСЛЭХ entry](https://mongoltoli.mn/dictionary/detail/100527) directly supplies traditional `ᠦᠨᠳᠦᠰᠦᠯᠡᠬᠦ` and the figurative base-on sense. Independently, an [Inner Mongolia University-hosted 2019 journal abstract](https://nom.imu.edu.cn/zh-hans/cmpn/paper/21930/) contains the dative basis + `ᠦᠨᠳᠦᠰᠦᠯᠡᠭᠰᠡᠨ` relative construction. Its [Mongolian Studies 2026/1 catalogue](https://nom.imu.edu.cn/zh-hans/cmpn/issue/1599/) also has the exact front-vowel pattern `ᠰᠡᠳᠬᠢᠯᠭᠡ ᠳᠦ ᠦᠨᠳᠦᠰᠦᠯᠡᠭᠰᠡᠨ`. The latter matches the proposed feminine dative after “size.” Both university sources were retrieved as indexed text; direct-page access failed. They are not represented as inspected article bodies.

`formats22_animation_poster` supplies genitive + “in place of,” and the long assembly help supplies the same construction with a separately written dative suffix. `ui_help23` supplies the demonstrative genitive `ᠲᠡᠭᠦᠨ ᠦ`. Its antecedent here is original size.

`formats22_pdf_invalid` already supplies exact perfective `ᠠᠰᠢᠭᠯᠠᠭᠰᠠᠨ`. `colour_converter_unavailable` supplies completed-action negation in “the image was not imported.” The picker error also supplies a bare indefinite object under this negative. These make the new “a canvas-based size was not used” construction defensible without assuming that a substitute size really existed.

### 3. Original SVG size above Android bitmap dimensions

`ui_the_assembly_exceeds_android_s_coordinate_range` supplies Android's genitive and a dimension-domain limit statement. `ui_the_normalized_image_dimensions_are_outside_android_s` confirms that the image-size noun denotes dimensions. The size-limit genitive and ablative “exceeded the limit” are established in `save20_bmp_size_limit` and `save20_encoding_budget`.

Only their grammar is reused. The proposal does **not** carry over the BMP file format, byte-size limit, or memory-budget referent. The actual [Kotlin source](https://github.com/c933103/AN-Paint/blob/5bf82b67199aaecbd341a8b150a887f8d60b5567/Paintroid/src/main/java/org/catrobat/paintroid/classic/SvgOriginalSize.kt) checks each ceiled dimension against `Int.MAX_VALUE`, after testing finite positive values. The proposal's “image size limit” preserves that dimensional ceiling without adding a numeric bound.

The Latin technical label **bitmap** already occurs in `ui_d_d_pixels_2f_mp_exceeds_the_current`. It is retained transparently, not presented as an independently standardized Mongolian term or as a proper name. Adding the native word for image lets the genitive attach to `ᠵᠢᠷᠤᠭ`, avoiding an invented suffix spelling for the foreign token. The reader-facing suitability of this retained loan label remains an explicit review point.

### 4. No resizing of any kind was applied

The [Academy dictionary's ӨӨРЧЛӨХ entry](https://www.mongoltoli.mn/dictionary/detail/72615), inspected in v2, supplies general change/alter and the traditional base. Several catalogue clauses, including `commons_check_file_licence`, supply exact perfective `ᠥᠭᠡᠷᠡᠴᠢᠯᠡᠭᠰᠡᠨ`. The long assembly help supplies size as the accusative object of this change verb. Combining that object/verb with the independently evidenced completed negative gives “the size was not changed.”

This removes the inherited automatic-only modifier and does not replace resizing with shrinking alone. It also avoids a generic future negative that might read as “will not change.”

[Hsiao's 2007 study, official open-access PDF](https://www.ling.sinica.edu.tw/item/en?act=journal&article_id=232&code=download), gives verbal-noun + negative predicate in Table 2 (p.500) and a written perfective-negative repair example (20, p.510), contrasted with a nonpast construction. Its primary data include the Inner Mongolia University modern corpus as well as historical texts. This supports the construction; it is not native review of this proposed wording. The official file was downloaded successfully despite the web renderer's inability to display its octet-stream MIME type.

## Script, case and scope controls

- No Cyrillic text was converted into the proposal. Native bases and inflected forms come from the exact traditional-script catalogue or directly printed traditional-script sources.
- `jirug-un`, `talbai-yin`, `hemjiy-e-yin` and `Android-un` are directly instantiated in source clauses. `tegün-ü` supplies the demonstrative genitive.
- `oron-du` is the in-place-of postpositional construction; `hemjiy-e-dü` is a front-vowel dative basis argument; `qijaγar-ača` is the ablative threshold after exceed.
- The perfectives `ashigla-γsan` and `ögerečile-gsen` are already spelled out in this locale. Attaching `ügei` is supported by both catalogue negative-event clauses and primary grammatical research.
- The source catalogue's ordinary suffix spacing and U+180E Mongolian vowel separator in “size” are retained. No mechanical script conversion or new shaping controls were introduced.
- The only Latin letter tokens are `SVG`, `Android`, and the expressly documented inherited technical label `bitmap`.
- Source-image dimensions, canvas-derived replacement, Android bitmap ceiling and completed no-change scope remain distinct.

## Limits and review questions

There is no remaining uncovered **semantic clause** at the composition-evidence level. That is narrower than saying the pair is accepted or natively idiomatic. Independent review should examine:

1. Whether the source-condition `jigaγ-a ügei` predicate reads naturally for a file's absent usable size declaration.
2. Whether “in its place” has a sufficiently clear original-size antecedent, and whether the long canvas-basis relative is comfortable UI prose.
3. Whether this locale should keep the existing Latin technical label `bitmap`, or prefer a separately established term in a later terminology review.
4. The final completed-action negative's naturalness in an Android error dialog.

The suggested cross-locale ICO key was checked. Here it says the icon dimensions disagree with the directory/reference entry. It does not supply “size written in the file,” so that evidence was not falsely attributed to Mongolian.

## Files and preservation

- `proposed-pair.json`: stable complete review-only pair, source URLs and backtranslations.
- `catalogue-evidence.json`: 23 exact checked excerpts with canonical keys and explanations.
- `full-aligned-catalogue.json`: all 688 exact-locale resource entries aligned to English for this pass; not an acceptance audit of the existing catalogue.
- `sources-attempted.json`: 24 relevant source/retrieval records with failures and limits.
- `validation.json`: source-message match, script/token checks and unchanged input hashes.
- `hsiao-2007.pdf` / `.txt`: locally retrieved research reference, not a claim that redistribution rights were reviewed.

No resources, original `proposals.json`, v2 snapshots, or frozen publication checkout were edited. No Manchu research was repeated. This bounded wording pass is complete.
