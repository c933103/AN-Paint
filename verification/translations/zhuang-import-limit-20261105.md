# Zhuang import file-size notice, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `22e064b9ab9e0f926e81ceb3a2ef14f3d968b442`, tree `fcecb36f255e7adcc34a2e972647db17783b4a17`; no previous operation was pending. This fills missing P1 `formats22_import_limit`, whose source says the file exceeds the 512 MiB import limit and asks the user to choose a smaller file. All 259 preceding typed resources remain unchanged; the total is 260. Only canonical XML and this report change.

Independent linguistic and actual-consumer review accepted a short operational paraphrase: this file is larger than 512 MiB, AN Paint cannot open it, and the user should choose a smaller file. The inability-to-open clause was added during review so the restriction is explicit without coining an import-specific technical term. It does not change the threshold into a RAM estimate, a pixel count or an inclusive rejection at exactly 512 MiB. The numeral and unit are preserved exactly.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports the component senses for file/document, large, small, choose and open, with comparison use of `gvaq`. Existing canonical resources use the same file and inability-to-open vocabulary; this establishes consistency, not independent linguistic proof. [Guangxi Minzu Bao, 17 January 2024](https://www.guangximinzubao.cn/szbzw/html/2024-01/17/content_49045.htm), second translation, attests `iq di` in a request to make a staff smaller. It supports the comparative construction, not file-size terminology.

Review confidence is high on numeric/consumer fidelity and **moderate on natural Zhuang wording**. The complete sentence is a composed software translation, not an independently attested interface phrase. The dictionary is OCR; no native-user or complete-language acceptance is claimed. Canonical XML owns the full current wording.

## Actual consumer

`ImportFiles.copy` in `ImportSelection.kt` is the sole direct consumer. It reads a provider stream into a staged file using a 64 KiB buffer, sums actual bytes in a `Long`, and throws the complete selected notice before writing the current chunk if the sum is **greater than** `512L * 1024 * 1024` (536,870,912 bytes). Equality is allowed by this guard. The restriction happens before format inspection and is distinct from decoder memory budgets and the separate PDF-file validation message.

Both editor `ClassicPaintActivity.readImage` and `AssemblyActivity` use this copy path. The editor includes the exception message in its opening-failure notice and deletes the partial temporary file. Assembly records the exception message with the source item, deletes the failed staged file and proceeds through its batch. No copying, cleanup, exception routing or import behavior changes.

## Executed checks

- All 171 offered-option catalogue checks and the importance manifest passed. Existing-node identity, source attributes, source numerals, literal tokens and escaping were checked.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.676 seconds**.
- Host Java parsed English and integrated Zhuang XML: **two cases passed**, preserving the single exact `512 MiB` token and the complete no-argument string. This is host XML/Java verification, not Android resource execution.
- Temporary token-aware source checks passed for the byte constant, strict-greater-than comparison, accumulated-byte check before writing, both real callers, error propagation and partial-file cleanup. These inspect the actual code; they do not execute a large-stream import.
- Base snapshot verification matched Git blob identity and executable mode for **1,278 materialized files**, retaining **269** unmaterialized non-tree entries. Publication checks the complete resulting path/mode/type/blob overlay, fresh expected-parent non-force lease and exact remote bytes.

`ImportSelectionFlowTest.base64AnimationGetsTheSameWarningAndCancelLeavesTheProviderOriginalIntact` was inspected, not run. It exercises a normal staged copy and cancellation, not the oversized threshold. No permanent per-edit wording mirror or duplicate test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **139/249**, P2 **52/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,352**, P2 **30,077**, P3 **7,481**; 46 options have complete resource presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android compilation, Robolectric, large-stream boundary execution, on-device error/cleanup flows, TalkBack and layout were not run. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
