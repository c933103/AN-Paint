# Four-script P2 status/control translation batch

Source commit: `984ae0731e566dda68d25d79feb29eaca153bc19`. Base: `51ca0b7abf9b6ba824411ebea98b74d39672859d`. Source tree: `287767b1e2d5566947d31cb3a3734054ca4835fb`.

Adds 30 previously missing active P2 values: Serbian Cyrillic 9, Hebrew 8, Armenian 7 and Nepali 6. Only four canonical XML files change; all 1,672 previous complete nodes and attributes are preserved. No application code, tests, workflow, priority inventory or permanent wording oracle changes.

Independent complete-value model review retained 28 of the self-reviewed values and revised two unsupported-image-URL messages. The Serbian wording explicitly identifies the redirected request; the Hebrew wording explicitly makes the URL unsupported. The archive includes original candidates, the separate self-review, final independent decisions, all 30 accepted full messages and real consumer context. The four undrafted Armenian/Nepali redirect clauses and all older holds remain unchanged.

## Verification

- 46 affected existing host checks passed on the final independent-review source. Command: `python -m unittest test_translations.TranslationCatalogueTests test_translations.AndroidResourceValidationTests test_string_importance.StringImportanceTests -v`, in `tools/`. Python 3.12.14.
- Four actual-JDK exact-output cases passed for Serbian/Armenian lossless labels. OpenJDK 21.0.13; `java FormattingCheck.java format-cases.tsv 4`. Both format values are byte-identical after independent review, so results are carried without redundant execution. Cases cover a real compound format name and an argument containing percent/format-like text.
- Fresh reconciliation found all 17 other open PR heads unchanged. Twelve Git-hash-verified immutable historical blobs establish zero candidate-key overlap in 32 target catalogue/head pairs at the eight held PR heads. The archive contains their immutable identities and results, not redundant whole catalogues.
- All 378 locally materialized tracked source files matched the base before edits. All 1,283 final remote source leaves were checked for exact path, mode, type and blob identity before publication. Source commit, expected parent and non-force new branch were verified.

Exact-head Codex and required CI are pending. No merge, final-develop qualification or release is claimed. Before this batch, merged P2 direct presence is 22,602 / 46,683; the proposed total is 22,632. Presence is not linguistic acceptance.

Independent AI/source review is not native-human certification or exhaustive installed layout, glyph, speech or device acceptance. Hebrew mixed RTL/LTR display has not been visually checked. Android vendor application labels may vary. No external primary terminology source was consulted.

## Evidence

`preparation.zip`: 27,979 bytes; SHA-256 `19ed81144d8f16a6f5e3a05e2392a944073c0dfd38f8f827fb1eea8e5a1a8c1b`. Fifteen members including the manifest. Each of the fourteen content members has a verified size and SHA-256. Historical evidence stays off the application branch; Git source/diffs remain authoritative for the four XML changes.
