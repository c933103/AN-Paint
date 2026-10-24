# Amharic size, radius and selection-control lexical drafts

Research date: 2026-10-24. Seven original short-label drafts only. No app-source changes, builds, CI, Work tasks, remote publication or independent acceptance occurred. These files are review evidence, not a locale patch.

## Proposed values

- ui_size_px: **መጠን (px)**
- ui_radius_px: **ራዲየስ (px)**
- ui_spray_radius_px: **የመርጫ ራዲየስ (px)**, **TERMINOLOGY HOLD**
- ui_strength: **ጥንካሬ (%)**, retain formatted="false"
- ui_tolerance: **ገደብ**, no percent suffix
- ui_original_size34: **ዋናው መጠን**, retain formatted="false"
- ui_lock_proportions: **ተመጣጣኝነት መጠበቂያ**

Every value remains an unaccepted original draft. High lexical confidence is not native acceptance, product-language acceptance, render/fit acceptance, accessibility acceptance or proof of source/consumer correctness.

## Evidence and transformation discipline

`exact-records.json` contains complete exact PO records with msgctxt, source references, local line spans and fuzzy flags, plus paired English/Amharic Android XML records with exact resource IDs. All selected positive PO records are nonfuzzy. Empty and English-retained counterexamples are retained explicitly rather than promoted as translations.

`sources.json` identifies full retained source files at immutable source commits and recomputed SHA-256 hashes. Full LibreOffice PO and AOSP XML snapshots are copied alongside this report. They are reused verified pinned bytes, not claimed to have been fetched again during this subtask. Headers and source attribution remain intact. `SHA256SUMS` covers the evidence files and drafts, excluding itself.

`draft-candidates.json` records exact proposed strings, rationale, confidence, alternatives, source record IDs and required review flags. `search-limits.json` records bounded negative searches. Search-engine results from secondary dictionaries and unrelated sources were not promoted as evidence.

The **Spray radius** candidate is deliberately held. Radius has an exact primary Amharic record in the rounded-corner setting, but the proposed spray component does not have an eligible primary attestation in this corpus. The compound is an original linguistic hypothesis and must not be accepted automatically.

**Strength** uses AOSP's exact Intensity → ጥንካሬ short label and supporting strength phrases. This is a cross-context adaptation, not evidence that Android already translates watercolor Strength (%). The product source independently confirms the numeric value controls alpha; the candidate does not silently rewrite Strength into Opacity.

**Lock proportions** shortens same-function LibreOffice prose. It is not an exact short-label match. The other source's Keep ratio → መጠን መጠበቂያ wording risks suggesting fixed dimensions, and empty current UI Keep ratio records are not usable translations. The proposed noun phrase captures maintaining proportionality; native grammar, checkbox-state interpretation and layout still need checking.

For **Original size**, only the foreign desktop accelerator underscore is removed from an exact source UI translation. A separately attested help-heading variant is recorded as an alternative. No claim of restoring position, rotation or arbitrary edits is intended.

## Product semantic constraints

Read ../consumer-context.json and its pinned consumer links for the full source binding. Size is shared stroke width or separate Pencil size; it does not necessarily change all tools' mark dimensions. Radius is rounded-corner radius, not diameter. Spray radius is the random disk radius in image pixels; spray points themselves remain 1px. Strength is watercolor alpha strength in 1..100 with literal (%). Tolerance is an absolute Euclidean ARGB distance threshold in 0..100 for connected fill, **not a percentage**. Original size restores retained source-image dimensions while preserving center and rotation. Lock proportions maintains the current gesture-start ratio, not necessarily the original ratio after earlier distortion.

No denied action, pending external action or uncertain write outcome occurred. No source-language defect is alleged by this lexical artifact. Any later genuine source correction must be handled English-first and trigger review of all affected locales.
