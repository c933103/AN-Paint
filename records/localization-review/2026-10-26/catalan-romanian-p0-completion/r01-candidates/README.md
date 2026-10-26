# Catalan/Romanian P0 completion candidates — frozen author snapshot

Pinned source [`ce796879f4568a27b9d905a8e8db639dd0a93a30`](https://github.com/c933103/AN-Paint/commit/ce796879f4568a27b9d905a8e8db639dd0a93a30), tree `f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c`. These are author candidates and source/structural evidence, **not acceptance or application changes**. This preserves the pre-review candidate state; independent outcomes are recorded separately in r02-reviewed, never inferred from this snapshot.

## One coherent completion batch

Each catalogue currently has 150 values and P0 32/92. Its remaining 60 missing P0 values partition into **55 current-consumer values + five explicit no-current-consumer holds**. The selected scope is 110 locale-values across 55 identities:

| Review workflow | Each locale | Combined |
|---|---:|---:|
| Recovery, autosave and undo integrity | 28 | 56 |
| Assembly, memory, resize and destructive actions | 16 | 32 |
| Credit integrity, destinations and encoding failures | 11 | 22 |

The six canonical `packet/*-candidates.json` files carry exact complete English/target pairs, format-token inventories, XML attributes, complete consumer windows, qualifications and author uncertainties. Their two actual `formatted=false` values (one history-warning identity per locale) must not hide extra format tokens. The separate foundation records every one of the 150 inherited values and attributes per locale, plus actual neighboring action labels/fallbacks. Author confidence is not independent acceptance.

## Source-context preparation correction preserved

The initial reused workflow context had correct English strings, attributes and 98 exact consumer windows, but five semantic notes still named the previous Danish/Norwegian catalogue labels. Both locale authors identified this before review. `packet/source-context-correction.json` records those old notes and their exact current ca/ro replacements; `preparation-history/r01/` preserves the original scope/manifest/structural verification bytes, explicitly as history. Canonical context is now `packet/scope-and-source-context.json`, SHA-256 `8dd3dd99b633bbec8254639797ddc81000ce4d8bfa9c037503663123587399d5`.

Original complete author files remain in `packet/author-proposals/`. Canonical normalization changed common bindings and source-note carry only; target text, attrs, confidence and original author uncertainties were not silently changed. Old author context hashes can refer to the historical scope; canonical `shared_source_context` identifies the corrected current metadata. No Danish/Norwegian linguistic acceptance transfers to these candidates.

Actual labels remain intact: Catalan Fitxer / Desa / Anomena i desa… / Desfés / Ajusta la mida de la imatge…; Romanian Fișier / Salvează / Salvează ca… / Anulează / Scalează imaginea…. `Image format` and `Load image…` remain intentional English context. Review must preserve singular optional floating-selection semantics, ZIP/canvas.png literals, complete conditional memory warnings, failure-prefix punctuation and current Save/recovery behavior.

## Boundaries and continuation

Only final independently approved missing values may enter one combined source/test/CI batch. If all 55 per locale are approved, structural P0 would become 87/92 with the five held absences remaining; this is conditional, not current acceptance. Existing 300 values/attrs are not replacement targets. Shared source verification does not share linguistic verdicts.

No ca-ES-valencia resource or review acceptance is added: parent inheritance remains routing evidence. Paired warning/P1/frozen/global59/112 boundaries, NN/DA/NO holds, prior qualifications, PR56 never-merge, PR113/PR159, Help callback/archive identity, interrupted archive and release pauses stay unchanged. No native-human, physical-device, layout or whole-language certification; no release.

The completed PR177 report remains [immutable and verified](https://github.com/c933103/AN-Paint/tree/68509d1a7e2845e1f625cc333ff88a4cf3ba9cf3/records/localization-review/2026-10-26/catalan-romanian-p0-import/r08-merged-coverage); its monitor is closed. New full-value reviews will be recorded separately rather than rewriting this candidate snapshot.

## Reproducible integrity checks

`verification/` contains the exact scripts, ordinary/optimized receipts, independent Git/ElementTree crosscheck and preserved preparation findings. All 110 real candidates passed; 368 packet mutations rejected, including 26 tests on the two actual formatted=false values. The separate 13 synthetic format negatives and nine synthetic tree/source negatives are not production cases. Ordinary and optimized receipts are byte-identical. `source-tree.json` is the full pinned Git tree.
