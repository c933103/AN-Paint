# P07-008: Brazilian Portuguese clipboard terminology recheck

Date: 10 October 2026. Scope: **P07-008 only**, with separate dispositions for directly associated UI, help and error occurrences. This does not accept P07-007/P07-009, the full pt-BR catalogue, PR7, or any withdrawn completion claim. The reset registers are unchanged.

## Result

The current clipboard noun **área de transferência** and commands **Recortar / Copiar / Colar** accurately describe the implemented operations. No new pt-BR clipboard glossary rewrite is justified. The historical **área de download** error is independently established from source, its correction is traced, and the corrected wording remains in current develop.

The [per-occurrence record](occurrences.tsv) contains **41 cases across 29 resources**: action labels and accessibility/tooltip surfaces, both internal-image and Android-text clipboard paths, all app-owned copy buttons, four injected gallery providers, direct error branches, memory help, and retained duplicate/legacy strings. Each row includes exact English and pt-BR text, immutable resource links, operation-source links and a semantic judgment. Repeated controls are separate cases even when they share one resource.

Two operational qualifications prevent an unbounded clean-bill-of-health statement:

1. The unused legacy manual still describes obsolete clipboard-control placement in both English and pt-BR (C26). Current clipboard icons are in the header; Select all is in Edit. The clipboard words themselves are correct. This is a shared manual-maintenance issue, not evidence that pt-BR needs a wholesale rewrite.
2. Commons metadata-only Copy credit failures currently use image-load/inspection/converter wording (E12–E14). The Portuguese accurately follows the English but is wrong for that handler. [PR34](https://github.com/c933103/AN-Paint/pull/34), separately owned and still pending, supplies operation-specific errors. Its changes were not copied into this patch.

## Exact source identity

- Initial source: develop `eab28203893ffba45f14a7f96df6d19cf4d19d3b`, tree `537185be479023d1567ab583d808ffaa7a4d3db8`.
- Develop advanced during review. Final inspected base: **`80c14372b0504bc44f9f2809ad477247fdc8100b`**, tree **`d9858229f98068bef9c6194c90d77610c5ecceec`**.
- GitHub's [exact comparison](https://github.com/c933103/AN-Paint/compare/eab28203893ffba45f14a7f96df6d19cf4d19d3b...80c14372b0504bc44f9f2809ad477247fdc8100b) changes seven SDK-harness/documentation files. Neither resource catalogue nor any reviewed clipboard consumer changed. The seven new files were read from GitHub; the complete temporary source tree was reconstructed and its Git tree matched the final base exactly before adding this evidence/guard.
- [English catalogue](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/res/values/strings.xml): blob `576616126cd8b12f5ddfcb4f97e61341b337413c`.
- [pt-BR catalogue](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/res/values-pt-rBR/strings.xml): blob `1d60f1400d503409c28134ed4460febdcf102008`.
- Both catalogues have 691 translatable strings and one plural. Those counts establish inventory, not correctness.
- [remote-receipt.json](remote-receipt.json) records independently read remote identities, base advancement and historical blobs. [source-results.json](source-results.json) records SHA-256 and Git-blob hashes for every resource/consumer input.

## Original requirement and recovered correction history

The original user request for a separate PR covering English variants, pt-PT, pt-BR, Italian, Greek and Turkish was recovered as a complete message dated 22 September 2026, 07:08 UTC. The final visible original-thread reply dated 23 September 2026, 05:24 UTC claimed catalogue completion; that remains a withdrawn historical claim, not evidence of accuracy.

The clipboard-specific integration chat excerpt describes a mistaken “download area” rendering. Exact retrieval of that message returned unavailable, so it cannot establish the complete original wording, subsequent corrections or all latest discussion. No private conversation text or links are published here. The public P07-008 register explicitly requires clipboard terminology rechecking. Current PR7 description/comments and its sole review/inline comment were read; no retrieved public clipboard-specific instruction supersedes that requirement. This is a bounded retrieval statement, not proof that no other relevant conversation exists.

Source independently establishes the relevant correction:

- [7288fe1d26ae7af7f696c74ecb1cb37d3c477216](https://github.com/c933103/AN-Paint/blob/7288fe1d26ae7af7f696c74ecb1cb37d3c477216/Paintroid/src/main/res/values-pt-rBR/strings.xml#L318) has **área de download** in `ui_estimates_include_the_current_canvas_and_clipboard_sampled`. Its blob is `94c1dffa85824d71f8535b8991e5801869e80ec5`.
- [595bedb6050064a5c37704eac16b3f6f46042c86](https://github.com/c933103/AN-Paint/commit/595bedb6050064a5c37704eac16b3f6f46042c86), dated 23 September 2026, 23:07:48 UTC, changes it to **área de transferência**, also repairing the immediately surrounding Portuguese grammar. The parent still has the erroneous term. Corrected blob: `58f1ddf52d69fede9380c3d1d7990c16a68a9186`.
- Original PR7's current head [730319aea40eb205d18c894c496e500d6f660ac6](https://github.com/c933103/AN-Paint/blob/730319aea40eb205d18c894c496e500d6f660ac6/Paintroid/src/main/res/values-pt-rBR/strings.xml#L318) and current develop preserve the corrected complete memory sentence byte-for-byte.

Thus the specific historical correction has fresh source-lineage evidence, while the complete original clipboard discussion remains incompletely recovered.

## Terminology and operation review

The conclusions here are contextual language judgments, corroborated by primary Brazilian-Portuguese terminology sources, not inferred from Latin script or matching key counts:

- [Microsoft's pt-BR clipboard support](https://support.microsoft.com/pt-br/office/troubleshoot-copy-and-paste-errors-in-office-for-the-web) uses **área de transferência** and **Recortar, Copiar e Colar**. This supports AN Paint's noun and action labels; it does not establish AN Paint's behavior.
- [LibreOffice's pt-BR standard-toolbar help](https://help.libreoffice.org/latest/pt-BR/text/shared/main0201.html) distinguishes removing/copying a selection and inserting clipboard content. It uses **Cortar** for cut, showing that a different legitimate product glossary does not make AN Paint's Microsoft-conventional **Recortar** erroneous. Its **Copiar**, **Colar** and **área de transferência** agree with the chosen terminology.

AN Paint has two distinct implementations:

- `PaintDocument.clipboard` stores a bitmap plus credit provenance inside the app. Copy renders the transformed selection; Cut invokes Copy then Delete; Paste duplicates the stored bitmap into a floating selection. The memory estimate counts that resident bitmap. Calling it área de transferência is accurate without promising system-clipboard interoperability.
- `LegalInfo` and `GalleryCredits` publish plain text through Android `ClipboardManager`. **Copiar tudo**, **Copiar crédito**, **Texto completo copiado** and **Crédito copiado** describe their actual payloads. Singular crédito can denote the attribution text collectively, including multiple lines/sources; automatic pluralization is not necessary.

The empty-paste hint uses a natural imperative, **Copie uma área**, and the actual **Desenhar → Inserir → Outras imagens** route. The retained duplicate has the same displayed meaning despite an obsolete File-related identifier. The error **Selecione primeiro uma área** states the precondition for Cut/Copy. No glossary patch is made just to replace one natural Brazilian synonym with another.

The long Catrobat caption was examined for its copy-credit clause and destination, not accepted wholesale as a legal explanation or full prose review. The legacy manual was examined for its three clipboard clauses only. Other non-clipboard content in those resources remains outside this conclusion.

## Boundaries and exclusions

- [source-results.json](source-results.json) inventories every English lexical candidate containing copy/copies/copied/cut/paste/clipboard. Excluded candidates concern file/recovery copies, resized output, exported/shared files, or stored records. “Copy: dimensions” in the resize dialog means a resized duplicate, not a clipboard action. The active `ui_help23` uses copy in the file-export sense and has no clipboard instruction.
- Crop/trim actions share the Portuguese verb recortar but operate on image geometry and use qualified labels such as **Recortar para a seleção**. Those separate commands were checked for disambiguation; this is not a review of every crop translation.
- No current production consumer was found for the legacy manual or duplicate paste-hint resource in Kotlin/Java, non-values XML, HTML or JavaScript under `Paintroid/src/main`. Absence is recorded as a source scan, not a device observation.
- Text selection in legal text and exported-credit TextViews, editable fields such as the credit editor, and WebView/Android system context menus can expose OS-owned copy/cut/paste commands. Those labels come from Android/WebView, not AN Paint's pt-BR catalogue. Device-specific labels and rendering were not inspected. Legacy archived-credit text explicitly disables selection.
- Drag-and-drop and import/share intent `ClipData` instances are not clipboard commands. Raw artwork titles, credit bodies, bundled legal texts and external website prose are not to be rewritten as app clipboard vocabulary.
- The directly reachable app-localized wrappers and precondition/error resources are listed separately (E01–E14). Arbitrary operating-system/dependency exception strings, low-level I/O diagnostics and all conceivable shared save/history failures are not certified as localized. A glossary review is not an exhaustive fault-injection test.
- No new Android build, resource compilation, lint, instrumentation or device-language switch was run for this evidence-only/application-source-unchanged pass.

## Separate pending Commons fix

At [PR34 head 209098ae341d28a6ca3279c5c1ed53476d84ee99](https://github.com/c933103/AN-Paint/blob/209098ae341d28a6ca3279c5c1ed53476d84ee99/Paintroid/src/main/res/values-pt-rBR/strings.xml#L700), independently read proposed pt-BR text is:

- `commons_credit_copy_failed`: **Não foi possível copiar o crédito da imagem.**
- `commons_credit_copy_failed_reason`: **Não foi possível copiar o crédito da imagem: %1$s**
- `commons_credit_copy_out_of_memory`: **Não há memória suficiente para copiar o crédito da imagem.**

These are natural pt-BR and name the actual copy-credit operation. The generic and reason-specific messages retain the distinction between no supplied reason and a `%1$s` reason; the OOM variant identifies insufficient memory. This is a bounded wording assessment of those three proposed strings. It does not imply PR34 is merged, its complete locale set is accepted, or its CI is fully passing.

## Proposed guard and verification

No production source/resource file is changed. The proposed `tools/test_ptbr_clipboard_terms.py` protects seven individually reviewed command/success labels plus the repaired memory noun. It rejects the recovered download-area regression, unreviewed replacement of every guarded label, and individual omission of each guarded resource. These are regression checks, not a general semantic classifier.

Fresh checks:

- `python3 tools/translation_catalogues.py`: pass, structural catalogue validation.
- `python3 -m unittest discover -s tools -p 'test_ptbr_clipboard_terms.py' -v`: 4 tests pass; includes 16 individual negative-control subcases (7 replacements, 1 historical mistranslation, 8 omissions).
- `python3 -m unittest discover -s tools -p 'test_localized_help.py' -v`: 8 pass, including both paste-hint route assertions. These tests do not validate every legacy placement statement.
- `python3 -m unittest discover -s tools -p 'test_translations.py' -v`: 32 pass, structural/provenance checks.
- Complete host discovery: **370 tests pass** in 51.665 seconds; see `host-tests.log`. Diagnostic failure messages later in that log are intentional negative-fixture output, not failed test outcomes.
- `python3 verification/ptbr-clipboard-recheck-2026-10-10/verify_scope.py`: reproduces the source extraction, per-occurrence TSV, resource/consumer hashes and retained-resource scan. Semantic judgments are explicit reviewed inputs in `review-data.json`, not outputs of the scanner.

Publication has not been performed. This bounded result is ready for review; the register remains pending full recheck. Before any broader closure, reconcile the unrecovered original clipboard discussion, handle the retained manual placement in its shared-help scope, and verify the separate Commons correction after integration. Do not convert this result into complete Brazilian-Portuguese acceptance.
