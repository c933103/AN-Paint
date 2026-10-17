# Turkish P0 + P1 source-bound linguistic review

Source-bound review of the current Turkish priority catalogue, with a separately reviewed nine-value correction candidate. The baseline ledger and candidate acceptance are deliberately separate. This evidence is retained outside the application tree.

## Exact scope

- Repository: c933103/AN-Paint
- Source: e414a4df64a56c2d8a2f374741b1f1b58fceea9b (merged develop, not unmerged PR114)
- Source tree: 74972d7a7e6fb94015d2b7dcb51a2b64796f6bed
- Turkish canonical XML blob: ae8e88fff322b7238ceacab0487653792ea0e736
- English canonical XML blob: 50fe59f226e55fa13d1164d5bf1808038ab3d936
- Priority manifest blob: e76a3a440a8b169d31f5ab5d163a2695b0db93b1
- Exactly 341 P0/P1 resource identities: P0 92 + P1 249. All are present in Turkish.
- The full current catalogue contains 717 identities; the other 376 are outside this batch.
- One separately requested P3 Navigate companion is reviewed independently and is not included in 341.

PR56 was read at cc1d2718b88b9f08e25b3013ccdbc10770e7f332. Its receipt ledger blob 004a38a070bc4ea215a82fdd41028aac5e341f3b contains one overlapping exact Turkish priority receipt, sampled-resize memory. That existing receipt is retained, not newly earned. Three other known prior bounded reviews cover the colour-profile error and two SVG-size errors. The fresh packet does not mint aggregate tracker credit, restore withdrawn PR7 conclusions, or replace those historical receipts.

No recent complete Turkish priority packet was found in the checked tracker, Turkish PR/branch search or existing review packets. Previously reviewed PL/CS/IT/NL/FR/DE/ES/RU/PT-PT batches were not repeated.

## Baseline review result

- 302 entries accepted in their current source-consumer context
- 27 entries accepted for catalogue meaning only, with no direct current production reference found
- Eight priority entries have open correction proposals
- Four entries remain open for terminology or missing composition context

Every entry has complete English and Turkish values, an individual linguistic judgment, confidence, pair hashes, consumer snippets and source hashes where available, plus explicit runtime/layout limits. This is an AI-assisted source/target linguistic review, not a structural-check surrogate or native-speaker certification.

The eight priority corrections were independently reviewed as complete source/target pairs and accepted for the candidate. The original baseline ledger retains its proposal states; candidate-adoption-review.json records the later decision separately. No new aggregate tracker credit is claimed.

Eight priority corrections:
1. Preserve all retained pixels positioned at the top-left origin, rather than only pixels already at the top left.
2. Make recovery instructions name the actual “Görüntü aç” File command.
3. Restore English fallback for new or untranslated text without a temporary/new-text-only promise.
4. Correct the canvas accessibility gesture directions and distinguish two-finger panning.
5. Replace the malformed/imprecise selection-outline term with “seçim konturu”.
6. Explicitly name memory allocation in the resize failure alternative.
7. Explicitly describe exchanging foreground/background colours in the live swap action.
8. Make the same exchange meaning explicit in the legacy foreground/background swap key; no live-consumer or layout acceptance is claimed.

The separately reviewed P3 Navigate hint also reverses pinch-to-zoom-in. It now explicitly describes spreading to zoom in, closing to zoom out, and dragging to pan. Its P3 classification is unchanged.

Remaining holds: visible FG/BG abbreviations, the legacy Main label without an established noun/context, and the third inserted component of the unused palette description. They are not counted accepted. No replacement is invented for these holds.

## Candidate and evidence

Application commit: [5a43d2a6a90fc578319914537b7ea55e46c75070](https://github.com/c933103/AN-Paint/commit/5a43d2a6a90fc578319914537b7ea55e46c75070), directly based on the source revision above. Only the Turkish resource and two compact regression files differ from develop. All 1,178 baseline paths and executable modes were checked; no path was removed. The final remote candidate tree was compared with all 1,180 local candidate leaf entries.

- candidate-adoption-review.json: complete accepted candidate values, hashes, tiers, holds and acceptance limits
- final-test-summary.json: exact candidate host/focused results
- candidate-tree-check.json: application delta and source-preservation result
- independent-candidate-check.json: independent bounded patch/test check
- final-artifact-manifest.json: SHA-256 and Git blob hashes for each packet member
- turkish-review-final-packet.zip: reproducible complete packet, with source snapshot and bulky341-entry ledger

### Original per-entry evidence

- turkish-p0-p1-341-review.json: full source/target/context ledger
- compact-ledger.json: compact full-value and judgment ledger
- turkish-corrections-and-open-items.json: eight priority proposals, four holds, separate P3 record
- p3-navigate-companion-review.json: complete independently bounded P3 pair/context
- turkish-nine-combined-corrections.patch: all proposed source changes together
- turkish-six-corrections.patch: initial six priority proposals only
- turkish-two-swap-proposals.patch: separately assessed exchange terminology
- turkish-one-p3-companion.patch: P3 proposal only
- turkish-eight-priority-corrections.patch: all eight P0/P1 proposals, no P3
- combined-candidate/Paintroid/src/main/res/values-tr/strings.xml: full nine-change candidate

The combined patch changes exactly nine values in one existing Turkish catalogue. All 717 identities/attributes remain, and 708 other values are unchanged. English, importance tiers, other locales, processing-label holds and the Hakka/tracker tasks remain unchanged.

## Validation

Normal and optimized packet validation pass. Both verify 117 exact source files against the fetched current Git tree, all 341 pairs and typed placeholder contracts, all catalogue Android string syntax, source-consumer snippets, the nine-value-only delta and forward/reverse patch reproduction. Nine reverted-value controls reject the former values against the proposed complete-value expectations; these are mechanical checks, not independent linguistic review.

The initial normal/optimized attempt failed because the validator's splitlines() dropped a final empty snippet line. The fixed validator counts split("\n") instead. No source, review decision or candidate changed to obtain the pass. The failure remains recorded in initial-validation-failure.txt.

AAPT2 2.19-11948202 compiled the entire final nine-change Turkish catalogue successfully. Fourteen focused tests pass both normally and under optimized Python. The complete host-suite results and timings are recorded in final-test-summary.json. The initial focused-test failures reflected an incorrect assumption that the preserved Turkish swap attribute was formatted=true and an overly narrow multiline source regex; those test assumptions were corrected without changing the approved resource candidate. The failure logs remain in the packet.

No local Android SDK was detected. Android linking, app build, JVM behavior, lint and device execution therefore remain unrun locally and require exact-head hosted results. Neither source assertions nor compilation establish layout/width, gesture runtime, Undo behavior or native-language fluency. Code/security correctness is a separate review dimension.

To reproduce from this packet, with Python and git available:

    python build_packet.py
    python build_companions.py
    python validate_packet.py
    python -O validate_packet.py

prepare.py documents extraction and can reuse the supplied verified source snapshot. The packet contains only the three changed application files under application-candidate/, rather than another full application checkout. To run the regression suite, check out the application commit above and follow CI.md. The complete source tree and source-preservation manifests are evidence, not permanent whole-source hash gates in application tests.

PR56 and its receipt ledger were read-only. Existing Hakka and processing-label holds were not changed. This review neither borrows results from unmerged work nor claims whole-language acceptance.

## External terminology corroboration

- Official GNOME GIMP Turkish translation history attests “titreme” for dithering. That existing term was not treated as a defect merely because of its everyday sense: https://lists.gnome.org/archives/commits-list/2020-January/msg05380.html
- Google Turkish touch guidance confirms spreading fingers for zoom-in and closing them for zoom-out: https://support.google.com/pixelcamera/answer/14106982?hl=tr

The review's operative evidence is the pinned source and complete target values. External references corroborate the two narrow terminology/gesture questions; they do not certify the full catalogue.
