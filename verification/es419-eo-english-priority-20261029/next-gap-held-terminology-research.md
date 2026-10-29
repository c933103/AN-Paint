# Read-only FI/ET/LV held-row follow-through — 2026-10-29

Source tree45bb547cdc60fb6658c69a6c02e797f4b78a13d5; PR225 remains frozen. This is not another full review, acceptance promotion, or source patch. All FI9/ET7/LV5 holds remain.

All21 held complete pairs and their earlier per-row reasons were read. No concrete new production correction has yet been established. The five FI/ET busy/edge cases already have separately documented source/P2 successors; these must not be counted as new repairs. Compact BG/FG, absent palette-state/Main consumers and sampled-decoding technical idiom remain unresolved.

## Dithering terminology: primary-source investigation

- Finnish GIMP official manual, https://docs.gimp.org/2.10/fi/gimp-image-convert-indexed.html, lines22,30–33 and46–55: uses **sekoitus** for dithering and explains palette colour approximation and Floyd–Steinberg examples. This attests an alternative; it does **not** prove existing Rasterointi wrong or certify all clauses. The linked Finnish glossary is largely English and supplies no additional Finnish lexical acceptance.
- Andrus Rinde, Tallinn University informatics teaching material, https://www.cs.tlu.ee/~rinde/mm_materjal/pdf/mm_graafika.pdf, page3/lines74–87: **Virvtoonimine (dithering)**, with colour approximation, smooth gradients and 8-bit/256-colour context. This is strong contextual terminology support, but not independent acceptance of a replacement full app message. Current Estonian description uses Rasterdamine; actual GIF checkbox uses Rasterda värvid. Any eventual material wording proposal must consider both full values and this actual control, not silently change only one label.
- Actual SaveOptionsDialog.kt creates export_dither checkbox at64, shows it only forGIF at90, and passes isChecked into ExportOptions at196. This is the relevant control/description family, not generic raster-image conversion.
- Estonian EKI direct dictionary URL failed in the web tool; no contents read, no denial inferred. Latvian terminology portal exact query likewise inaccessible; a Tēzaurs direct entry cache miss supplies no lexical evidence. Search-only Glosbe/mirrors not used for acceptance.

No glossary-based cosmetic replacement is authorized/applied. No native-human, runtime or layout certification. Source-backed full-pair independent review would still be required for any candidate correction; original uncertainty receipts stay immutable.

## Current source follow-through

Read current ClassicPaintActivity.editAction and attachLegacyImageCredit: draft-saving notice is selected only when autosaving; generic busy attachment uses ui_please_wait_for_the_current_operation. This confirms the already-recorded source successor rather than a new fix. FI current trim templates are exactly the accepted colon compositions, so the historical Vasen/Oikea/Alhaalla compound complaint does not justify changing standalone priority labels. No direct main-source references to ui_main23 or ui_foreground_background_colour_palette were found in the current classic Kotlin scan; no new referent invented.

The Estonian EUCIP educational colour-model page https://eopearhiiv.edu.ee/e-kursused/eucip/arendus/4211_vrvimudelid.html uses kuueteistkümnend compounds alongside #RRGGBB examples (lines64–71). This confirms the number-system terminology but does not settle idiomatic standalone caption truncation. Keep its hold; no cosmetic caption change proposed. FESPA glossary direct page failed cache retrieval; its search excerpt is not treated as full evidence.
