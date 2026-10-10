# Second-pass SVG translation review index

This pass adds five complete review-only candidate pairs (both Hakka scripts, Tibetan, Dzongkha, Nôm) and a Jeju size-limit-only candidate. No new pair is accepted. Six locale tags still lack a complete review candidate.

The original 48-pair proposal snapshot is unchanged. Published incomplete draft: [PR #29](https://github.com/c933103/AN-Paint/pull/29), head `80f0448f878165213eaa7e9bd5ad286be00e4ce8`.

| Locale | Current bounded outcome | Deliverable |
|---|---|---|
| hak-Hant-TW | complete_review_candidate | [hakka-nom-paraphrase-candidates.json](hakka-nom-paraphrase-candidates.json) |
| hak-Latn-TW | complete_review_candidate | [hakka-nom-paraphrase-candidates.json](hakka-nom-paraphrase-candidates.json) |
| bo | complete_review_candidate | [v2-bo-dz-jje/candidates-and-evidence.json](v2-bo-dz-jje/candidates-and-evidence.json) |
| dz | complete_review_candidate | [v2-bo-dz-jje/candidates-and-evidence.json](v2-bo-dz-jje/candidates-and-evidence.json) |
| mn-Mong | withheld_complete_messages | [v2-mongolian-manchu/language-evidence.json](v2-mongolian-manchu/language-evidence.json) |
| jje | one_review_candidate_too_large_only | [v2-bo-dz-jje/candidates-and-evidence.json](v2-bo-dz-jje/candidates-and-evidence.json) |
| mnc-Mong | withheld_complete_messages | [v2-mongolian-manchu/language-evidence.json](v2-mongolian-manchu/language-evidence.json) |
| ain-Kana | withheld_complete_messages | [v2-ainu-okinawan/review.json](v2-ainu-okinawan/review.json) |
| ain-Latn | withheld_complete_messages | [v2-ainu-okinawan/review.json](v2-ainu-okinawan/review.json) |
| ryu | withheld_complete_messages | [v2-ainu-okinawan/review.json](v2-ainu-okinawan/review.json) |
| vi-Hani | complete_review_candidate | [hakka-nom-paraphrase-candidates.json](hakka-nom-paraphrase-candidates.json) |

## Important new evidence and cautions

- Jeju: a primary negation study distinguishes native 아녀다 from Korean 않다; copying the existing narrowing/shrinking-only sentence and changing suffixes is not enough. This is a bounded constructional review risk, not a full-catalogue defect finding.
- Ainu: pororu is an independently documented coinage in a named lexicon, not a word newly coined in this pass. Its community acceptance and technical dimension sense remain unverified. Fourth-person a= is not a universal passive marker.
- Manchu: daci is described as an adverb in the inspected grammar. The original-size noun phrase needs contextual review; the evidence does not prove it wrong.
- Traditional Mongolian: deleting the automatic modifier from a nominal no-change clause does not independently establish completed-operation semantics.

## Limits

- Exact source URLs, retrieval outcomes and per-clause support are stored in the linked reports.
- Some official PDFs were only available through indexed excerpts; failed direct fetches and unverified page images are explicitly recorded.
- Complete candidates combine supported vocabulary and constructions; none is a quoted pre-existing SVG UI sentence or independently certified natural translation.
- No production resources, tests or first-pass snapshot were edited by this work.

The index hashes describe the reviewed files at assembly time. Independent review may revise its own candidate files afterward; do not assume a stale index hash is evidence against an intentional later revision.

## Exact six remaining tags and gaps

### mn-Mong

- Complete usable-original-dimension declaration in traditional written Mongolian.
- Natural canvas-derived substitution clause with verified suffix/case forms.
- Android bitmap dimensional-bound expression.
- Completed negative size-change predicate: a nominal “no change” clause, even without automatic, does not itself establish that the operation performed no resizing.

### jje

- Complete declaration/recording predicate and usable-original-size relative clause.
- Natural canvas-derived substitute wording.
- The too_large-only candidate still needs orthographic/register and noun-chain review; its new short negative avoids copying Korean contracted 않다.

### mnc-Mong

- Declaration predicate suitable for an SVG document.
- Usable-original-dimension syntax, including contextual review of adverbial daci in the existing original-size phrase.
- Drawing-area-derived replacement argument structure.
- Android bitmap dimensional-bound expression. The completed negative halahakū construction itself now has independent grammatical support.

### ain-Kana

- Validated canvas/dimension terminology and original/intrinsic-size sense of the full noun phrase.
- SVG declaration and usability argument structure.
- Canvas-derived replacement argument structure; fourth-person a= cannot simply be assumed to be a general passive.
- Android bitmap dimensional ceiling and a complete unqualified no-resize clause. Must remain paired with ain-Latn.

### ain-Latn

- Validated canvas/dimension terminology and original/intrinsic-size sense of the full noun phrase.
- SVG declaration and usability argument structure.
- Canvas-derived replacement argument structure; fourth-person a= cannot simply be assumed to be a general passive.
- Android bitmap dimensional ceiling and a complete unqualified no-resize clause. Must remain paired with ain-Kana.

### ryu

- Complete SVG declaration and usable-original-size construction.
- Canvas-derived substitution syntax and argument roles.
- Natural Android bitmap dimensional ceiling comparison.
- Completed polite negative resize clause; dictionary confirmation of change/negative past does not alone validate the full polite nominalized sentence.

## Composition-review update

Hakka Han/PFS/Nôm clause meanings were reported coherent. Before inclusion, the PFS candidate requires `sông → song` (上) and `tiau → thiàu` (調, adjust). Existing full Nôm assembly help independently contains `朱 別`; it is not a freshly guessed compound. Tibetan/Dzongkha composition review is still pending at this index finalization. These review results do not imply native acceptance or accepted coverage.

## Later composition-review disposition

The [independent final review](independent-composition-review.json) subsequently found all five complete pairs coherent for source-assisted draft inclusion. It also requires `tiam → tiám` for 點, in addition to the two PFS corrections above. The [exact added values](added-proposed-values.json) incorporate all three. Six scoped tags remain withheld; linguistic acceptance remains open.
