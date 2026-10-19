# Independent challenge of five Afrikaans corrections

Review date: 2026-10-19. Input: `corrections.json`, bound to source commit `798e6159939fa06beb27755700a1320a5970cb7b`.

An independent model-based reviewer compared the English, before/after Afrikaans and supplied consumer excerpts for all five proposals. Result: **5 reviewed, 5 acceptable, 0 required revisions, 0 blocking findings, 2 optional style alternatives**. No files were edited by that reviewer. This is not native-speaker sign-off, runtime execution or rendered-layout evidence. The independent challenge covers the five corrections, not all 341 priority strings.

## 1. Incomplete encoding

`ui_the_encoder_did_not_finish`: “Die enkodeerder het nie die enkodering voltooi nie.”

Accepted. Correct `het … voltooi` and `nie … nie` construction. Adding the encoding object is faithful in all three callers, `TextImageCodec.kt:33`, `IcoCodec.kt:97` and `ImageExporter.kt:25`, which throw after bitmap compression returns false. It neither claims a cause nor suggests success. Repeating the `enkodeer` stem is slightly heavy, but “Die enkodering is nie voltooi nie” is only an optional shorter alternative that changes the English subject. Keep the proposed wording.

Terminology corroboration: [official DBE Afrikaans assessment material using “enkodeerder”](https://www.education.gov.za/LinkClick.aspx?fileticket=YKn7YKXOGK4%3D&forcedownload=true&mid=10127&portalid=0&tabid=2922).

## 2. Saved-image sharing options

`ui_the_image_was_saved_but_android_could_not`: “Die beeld is gestoor, maar Android kon nie die deelopsies oopmaak nie: %1$s”.

Accepted. `Kon nie … oopmaak nie` is grammatical; `deelopsies` supplies an intelligible noun instead of awkward bare `deel`. `ClassicPaintActivity.kt:1380` follows `startActivity(Intent.createChooser(...))`, so opening sharing options describes the specific UI failure. Preserve the successful-save clause and `%1$s` detail. Do not simplify to “kon nie die beeld deel nie”, which would blur failure to open the chooser with failure to deliver an image.

Sources: [Google Afrikaans support using “deelopsies”](https://support.google.com/youtube/answer/171780?hl=af), [VivA explanation of Afrikaans negation](https://dev2.viva-afrikaans.org/lees-luister/blog/item/592-nee-mamma-nee-ontkenning-in-afrikaans-i). This is not a claim that the first `nie` must always precede its object; “kon die deelopsies nie oopmaak nie” could also work here.

## 3. Lossless explanation

`ui_higher_quality_usually_makes_a_larger_file_lossless`: “Hoër kwaliteit lewer gewoonlik ’n groter lêer. Kompressie sonder verlies behou elke kleurwaarde.”

Accepted. All meaning is retained, the remaining English term is translated, and every colour value remains explicit rather than only perceived quality. `SaveOptionsDialog.kt:103` uses this explanation near the lossless checkbox; `kompressie` clarifies the elliptical English subject. “Verlieslose kompressie behou elke kleurwaarde” is a more compact technical alternative, not a required correction. Existing `kwaliteit` also agrees with `save20_lossy_quality_description`.

Terminology corroboration: [official DBE material using “verlieslose kompressie”](https://www.education.gov.za/LinkClick.aspx?fileticket=4t6jTP-Xy70%3D&mid=7348&portalid=0&tabid=1856).

## 4. Language-picker explanation

`language20_translation_note`: “App-taal\n\nVertalings word in AN Paint se taalhulpbronne onderhou. Nuwe of onvertaalde teks verskyn in Engels.”

Accepted. Restores all three source components and removes the unsupported all-text completeness guarantee. The passive construction, `AN Paint se` possessive and new/untranslated distinction are sound. `App-taal` matches adjacent existing language labels. `Taalhulpbronne` accurately names resource content here. Both escaped newlines match the source.

Source-location clarification by the implementation author: `AppLanguage.kt:149` uses this view as the dialog custom title **above** the choices, rather than below them. The reviewer's initial location description was imprecise; this does not change the accepted text. The new test checks the full custom-title text and Cancel in the actual picker.

## 5. Pixel count

`ui_d_d_px_d_pixels_2f_mp`: “%1$d × %2$d px · Aantal piksels: %3$,d (%4$.2f MP)”.

Accepted. `Aantal piksels` is idiomatic and explicitly identifies the total count. `ImageImport.kt:15` supplies width, height, width×height as a `Long`, and count/1,000,000 as MP. All four positional placeholders, grouping/precision flags, units and separators are preserved. The prior wording was intelligible; the correction restores explicit-label parity without changing numeric meaning.

Additional boundary rationale by the implementation author: `ImageDimensions(1, 1)` is supported, and the old fixed suffix would produce `1 piksels`; the count-neutral label avoids that singular/plural mismatch. The authored live-consumer test includes one pixel, two pixels and a grouped large count. This additional boundary analysis is separate from the independent reviewer's five-value acceptance.

## Conclusion

The independent reviewer reported high confidence in the five values' meaning, grammar and supplied UI context. Encoder repetition and long-form lossless terminology remain optional style choices. Neither the review nor the cited terminology evidence certifies the entire language, installed UI, accessibility, all current consumers or unreviewed P2/P3 content.
