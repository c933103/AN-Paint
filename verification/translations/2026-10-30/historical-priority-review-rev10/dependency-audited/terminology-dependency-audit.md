# Terminology-dependency audit — frozen author revision10

**Unadopted experimental review.** This supersedes the preceding consolidated ledger's recommendation statuses, not its exact wording or author provenance. It is an AI research-assisted linguistic recommendation, not native-human certification or permission to integrate an entire screen.

## Result

| Locale | ACCEPT | CORRECT | HOLD | Total |
|---|---:|---:|---:|---:|
| ang | 219 | 0 | 122 | 341 |
| non | 230 | 0 | 111 | 341 |
| Total | 449 | 0 | 233 | 682 |

Four former ACCEPTs receive a shared-term HOLD. All 229 previous HOLDs remain held. Fifteen reasons are narrowed so that a held special construction does not accidentally invalidate accepted ordinary terminology. No target wording changed. Zero CORRECT does not certify held values.

**Exact usable subset:** `independently-usable-accepted-values.tsv` contains all 449 remaining ACCEPT locale/key pairs and their exact source/target, confidence, coinage disclosure, reason and dependency notes. They remain independently usable *as experimental recommendations within the declared conventions*. `prior-accept-value-gates.tsv` accounts for all 453 previous ACCEPTs, including the four exceptions. This is a row-level recommendation, not an assertion that surrounding held strings or interpolated values are accepted.

## Four dependency exceptions

| Locale | Key | Exact current target | Current recommendation |
|---|---|---|---|
| ang | ui_autosave_metadata_is_missing | Sidegewritu þære sylfhealdunge wana sind. | HOLD M |
| ang | ui_invalid_autosave_metadata | Unrihte sidegewritu þære sylfhealdunge. | HOLD M |
| non | ui_autosave_metadata_is_missing | Viðbótarrit sjálfvarðveizlu vantar. | HOLD M |
| non | ui_invalid_autosave_metadata | Ógild viðbótarrit sjálfvarðveizlu. | HOLD M |

They share the generic metadata convention with these already-held colour values:

| Locale | Key | Exact current target |
|---|---|---|
| ang | colour_invalid_metadata | Seo anlicnes hæfþ unriht hiwsidegewritu oþþe swilc þe þis weorctol ne onfo. |
| ang | colour_truncated_metadata | Þæt anlicnesgewrit endaþ innan his hiwsidegewrita. |
| non | colour_invalid_metadata | Myndin hefir ógild viðbótarrit um liti eða slík er verkfærit tekr eigi við. |
| non | colour_truncated_metadata | Myndritit endar innan viðbótarrita sinna um liti. |

### What the metadata hold actually means

This is a **semantic-convention uncertainty**, not a demonstrated morphology error. The four short autosave values correctly distinguish missing from invalid; their number/agreement was not the issue. Nor is the issue that no medieval software text contains these terms.

The proposed literal senses are accompanying/additional records or writings. Without the stated glossary they could be read as ordinary supplementary text, rather than the structured descriptors associated with encoded image or autosave data. Colour metadata can be embedded inside a file; “accompanying” must not inadvertently require a separate sidecar or extra document. **The current glossary does not explicitly assert that mistaken restriction**, so this is a possible reading requiring a consistent terminology decision, not proof that the targets mistranslate metadata. The author's conventions already define the intended technical sense as “metadata (accompanying descriptive records).” That definition is relevant positive evidence and must not be ignored.

The earlier review accepted that extension in the autosave batch but left the same convention unresolved in the colour batch. It cannot coherently count as settled in one place and a blanket unresolved base-term objection in the other without an explicit context distinction. The present conservative gate retains the unresolved judgment consistently, as requested. It is **not** an assertion that the proposed coinages are unusable or that modern concepts need impossible historical attestations.

**Minimal resolution:** independently decide that the disclosed record terms adequately name metadata across both autosave records and embedded colour descriptors, without implying arbitrary added prose or necessarily separate files. If that glossary-level judgment is accepted, these four short values need no identified grammatical repair. The colour values still need their separately recorded full-clause checks (including ANG `onfo` construction and the truncation phrase). A new medieval software citation is neither needed nor a sensible requirement.

## Shared terms that do not create new ACCEPT gates

The distinction is between the *same unresolved sense/construction* and a base word used in a different, adequately explicit context. Explicit modern coinage alone is not an adverse finding.

| Family | Existing overlap and decision |
|---|---|
| Copy | All 44 occurrences of `efenwyrht` / `eptirrit` remain HOLD. No accepted row silently adopts that copy convention. `eptirrit` remains explicitly modern/reconstructed; that status alone is not a proved defect. |
| Draft | All 28 `weorcgewrit` / `vinnurit` occurrences remain HOLD for the particular recoverable-draft meaning and/or their full context. Autosave naming itself need not be held merely because it appears beside draft. |
| Undo | NON `Gera aptr ógert` is held in all six occurrences. ANG `Undon` remains ACCEPT; naming a specialized undo cache/history is a separate question. The ANG top-left warning stays HOLD for positional/full-clause wording, not because `Undon` itself is uncertified. NON accepted `Gera aptr` means Redo; adding `ógert` creates the unresolved undo construction. |
| Canvas | The 21 ACCEPT occurrences of `metingbord` / `myndborð` remain usable. Holds concern fit/result phrases, coordinates, recovery state/copy, source-size derivation or gesture syntax—not the disclosed drawing-board metaphor. |
| Pixels / bitmap | The 19 ACCEPT occurrences identified in the pixel/raster-picture family remain usable. Holds concern scalar pixel count versus resolution/dimensions, vector rendering, dimension conversion, upper-left/undo wording or a long allocation/reserve chain. A literal pixel-count label is not evidence that the same noun phrase correctly translates resolution. `-pricena` is a supported normalization; reduced `-prica` is not condemned by a fabricated universal rule. |
| Buffers | Both `save20_encoding_budget` values remain ACCEPT: temporary stores explicitly tied to encoding and a memory budget convey buffers. Other held sentences contain sampled-decoding/copy or more specialized working-store/allocation wording. Their broad “buffer/copy” reasons have been narrowed; they do not establish a blanket defect in `hwilendlic hord` or `geymsla um hríð`. |
| App/tool | The 11 ACCEPT occurrences remain usable in explicit language/application or tool contexts. Share explanations remain held for copy semantics; Enable remains held for a disabled-app state, not for the general tool-as-app extension. Toolbox and input-control compounds are separate terms. |
| Settings | Six ACCEPT occurrences remain usable. Colour profile is not automatically generic settings; draft/copy settings and NON `teikning` can create independent holds. |
| Apply versus ratio-lock | NON `Festa hlutfellingu breiddar ok hæðar` and `Festa hlutfellingar` remain ACCEPT for constraining proportions. This does not settle `Festa` as the general Apply/commit action. ANG ratio phrases have their own ratio-versus-absolute-measure ambiguity. |
| Tap/hold/scroll | Simple tap and an explicit “move so that you see more tools” instruction remain usable. Holding a finger must specifically convey sustained screen contact; ANG `Scrid to ma hiwum` also differs from the explicitly purposive accepted scrolling clause. No blanket objection to a movement verb is inferred. |
| Font/category/menu | The ordinary kind/category and options vocabulary can be used without accepting the font/typeface or standalone menu-list conventions. `Ceasung` as a menu is not the same semantic claim as explicit `ceasunga` options. |
| Colour, numbers, shape | ANG accepted singular `hiw` and explicit colour-value/format contexts do not settle the exact `Hiwu` plural or colour model/profile terms. Actual numeric colour values and pixel counts are not arbitrary encoded-image data. Held `anlicnesgetæl` / `myndtǫlur` data metaphors therefore do not block ordinary numbers. |
| Other fully held families | Font naming, frame compounds, NON `hreyfanlig`, NON `teikning`, credit records, NON `hætta við`, interface-control naming, toolbox compounds and airbrush compounds have no ACCEPT occurrence of the held term in the audited register. A related historical base word does not automatically establish every derivative. |

The family counts are overlapping lexical review aids, not disjoint totals. `family-membership.tsv` supplies exact members and statuses; it is not a claim that every accidental substring is a semantic dependency. The judgment considers the complete source/target context.

## Dynamic-template boundary

All four revision10 expand/collapse category templates remain ACCEPT with the fixed known-gender heading:

- ANG `%1$s. Gecoren tol: %2$s. Unfeald tol and ceasunga`
- ANG `%1$s. Gecoren tol: %2$s. Feald tol and ceasunga togædere`
- NON `%1$s. Valit verkfæri: %2$s. Breið út verkfæri ok valkosti`
- NON `%1$s. Valit verkfæri: %2$s. Fell saman verkfæri ok valkosti`

Read-only supplied call-site context established that `%2$s` receives the selected tool label. The heading avoids an adjective incorrectly agreeing with that arbitrary value. **Acceptance of this template does not accept a held tool label inserted into it.** The same general principle applies to arbitrary `%s` contents elsewhere. A complete rendered screen must still account for its separately held values.

## Artifacts and verification

- `current-value-recommendations.tsv` / `.md`: superseding 682-row ledger, with unchanged exact text and original pre-audit reasons/statuses retained in TSV columns.
- `dependency-hold-exceptions.tsv`: the four exact status changes.
- `reason-scope-corrections.tsv`: fifteen narrowed reasons, all still HOLD.
- `independently-usable-accepted-values.tsv`: exact 449-row subset.
- `prior-accept-value-gates.tsv`: complete 453-row accounting of the former ACCEPT subset.
- `family-membership.tsv`: exact term-family cross-reference.
- `manifest.json`: input identities, counts and hashes.

Verification checked unique 341 source keys per locale, 682 rows, exact equality of all English/target text to the frozen current ledger, unchanged author ledger/index hashes, retention of all 229 previous HOLDs, exactly four ACCEPT→HOLD changes, and no new CORRECT or invented grammatical allegations. The withdrawn OE weak-II `-aþ` objection remains withdrawn.

This historical review stage did not change application resources or run project tests. All recommendations at that stage remained pending final acceptance review, not rejected or adopted.
