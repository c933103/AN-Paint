# Independent exact review — revision10 dynamic tool labels

Fixed ledger: `90-author-secondcheck.rev10-snapshot.md`, SHA-256 `533e16a1aea28666f53b0c66f0ba5aad34f7d569bd451c017c4ae789363a5901`. Only the four new revision10 values below are added to the prior independent review through revision9. Later mutable edits are not included.

**All four: ACCEPT M as experimental candidates.** No native-human certification, automatic source integration, runtime check or release credit.

| Locale / key | Exact English | Exact reviewed v2 target | Independent reason |
|---|---|---|---|
| ang / ui_expand_tool_category | %1$s: %2$s selected. Expand tools and options | %1$s. Gecoren tol: %2$s. Unfeald tol and ceasunga | Gecoren modifies fixed neuter tol; inserted tool name is after colon, not its agreement controller. Unfold metaphor expresses expansion, and tools/options remain distinct. |
| ang / ui_collapse_tool_category | %1$s: %2$s selected. Collapse tools and options | %1$s. Gecoren tol: %2$s. Feald tol and ceasunga togædere | Same stable heading; folding together reverses expansion, not selection or deletion. Both original placeholder roles retained. |
| non / ui_expand_tool_category | %1$s: %2$s selected. Expand tools and options | %1$s. Valit verkfæri: %2$s. Breið út verkfæri ok valkosti | Valit now agrees with fixed neuter verkfæri, so masculine Bursti or an infinitival tool label causes no predicate-agreement failure. Expand-tools-and-options action retained. |
| non / ui_collapse_tool_category | %1$s: %2$s selected. Collapse tools and options | %1$s. Valit verkfæri: %2$s. Fell saman verkfæri ok valkosti | Same correct fixed neuter heading; imperative fold-together preserves collapse polarity. Inflected option object valkosti is coherent under declared new UI sense. |

The new periods/colon segment category, selected-tool heading/value, and action. They do not swap or duplicate the two placeholders. Each template remains intelligible whether the chosen label names a masculine/feminine/neuter tool or an infinitival action; it no longer requires gender/number from the arbitrary inserted phrase.

Primary grounds include [B–T ge-coren](https://bosworthtoller.com/13939), [B–T tól](https://lrc.la.utexas.edu/books/asd/dict-T), and [C–V færi with verk-færi](https://www.germanic-lexicon-project.org/html/oi_cleasbyvigfusson/b0185.html). The physical-tool and choose/fold/spread bases support productive interface extensions, not attested medieval UI quotations. A failed direct fetch of C–V p697 was an ordinary lookup error; an accessible dictionary cross-entry corroborated the tool noun instead. No refusal or user denial inferred.

Read-only caller evidence remains `ToolCategoryButton.kt:27` and `PaintDocument.kt` in the supplied local baseline: `%1$s` is category, `%2$s` is selectedTool.label. This is not a build or runtime result. No implementation or project test result is asserted.

## Updated override-review tally

Through revision10: **47 reviewed latest proposals**, consisting of **44 text overrides + 3 evidence-only restatements**. **27 ACCEPT recommendations / 20 HOLD / 0 new CORRECT** among those overrides. This is not47 additional source keys and not accepted localization coverage. The682-value v1 register remains historical; these four decisions supersede its two ang HOLDs and two non CORRECTs for the exact v2 targets only.
