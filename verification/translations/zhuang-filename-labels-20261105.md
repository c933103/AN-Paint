# Zhuang: default filename and filename sorting

Date: 2026-11-05 (UTC). Base: `562a1e2b3c5c162c4506455a386f5bf8ee147949`, tree `f8c8934505400d80942e1f2213bf7a92461d7d6d`.

## Change and independent review

Added P1 `ui_untitled` and P2 `ui_filename_a_z`, `ui_filename_z_a` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 210 previous typed resources are unchanged. Canonical XML owns the wording.

Independent review accepted all three with moderate linguistic confidence. “Has no name/unnamed” fits the actual filename-default consumers better than a literal topic/heading term and makes no unsaved-state assertion. The filename compound is a supported composition, consistent with the existing save-field label, not an independently attested standardized software phrase. A–Z/Z–A remain the source UI's sorting shorthand, not a claim of Zhuang-specific collation. Native-human approval is not a gate or a claimed certification.

Sources directly checked:
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `mingz`, name (M.htm 40/56); `vwnzgen`, document/file (V.htm 19/19); `daezmoeg`, topic/title (D.htm 10/110). The OCR warns of incomplete proofreading.
- [Guangxi Minzu Bao grammar discussion, 22 June 2016](https://www.guangximinzubao.cn/szbzw/html/2016-06/22/content_17989.htm), examples 45–48 and discussion: `mbouj miz` negates possession/existence. The proposed no-name phrase is compositional, not quoted from the article.
- [Zhuang Wiktionary PDF-file page](https://za.wiktionary.org/wiki/File%3AIntroduction_to_Wikipedia_and_its_principles.pdf): the file tab uses `Vwnzgen`, corroborating digital-file usage. This is community-interface evidence, not normative terminology; much of the surrounding interface falls back to Chinese.

## Actual consumer boundaries

`ClassicPaintActivity` uses the untitled label as its initial/new-document filename and as the blank proposed-name fallback for Android's destination picker. `SaveOptionsDialog` uses it when the initial filename is blank. Both save paths continue through `ExportNames.withExtension`. `EditorDraftRecovery` also starts with this filename default; recovered metadata has a distinct recovered-image fallback. This label is not a save-success, unsaved-state or recovery-loss message. Existing user-provided names are not renamed by this resource addition.

`AssemblySort` maps the two sorting resources to ascending/descending name enums. `AssemblyActivity` selects by enum position, not translated text, then renders the tray from `assembly.sorted(sort)`. The comparator uses `Locale.ROOT` lowercase names, then original names, then IDs; descending reverses that comparator. It returns a sorted list without modifying the model or rearranging placed images. This is neither locale-specific alphabetic collation nor natural numeric filename sorting.

## Verification

- Fresh remote head/tree reconciled with the preceding verified publication. All **1,254 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,523 base leaves.
- The original 210 resource nodes, attributes and prefix bytes are preserved; three missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literal tokens pass. New XML Git blob: `7da9ba7dd36385d432b1935d8fab52bc2632e512`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.388 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Six host Java literal-label cases passed**, covering all three keys in English and Zhuang.
- Targeted token-aware source checks passed for all bindings, blank-name fallback and extension-helper calls, the separate recovered-name fallback, enum-based sort selection and the complete comparator order. Input-contract checks confirm the new default has a nonblank trimmed stem without slashes, backslashes, ISO control characters or a misleading extension; both sorting direction markers remain exact and distinct. These checks do not execute Kotlin filename or sorting code.

Zhuang now has **213 typed resources**: P0 **69/94**, P1 **130/249**, P2 **14/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,361, P2 30,115, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed save-picker/recovery/sorting path, provider-specific filename acceptance, device layout, accessibility or font checks were run. Consumer findings are static source checks. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
