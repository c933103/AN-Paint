# Greek priority review and current-base integration

The **341-entry Greek P0+P1 linguistic review** (92 P0, 249 P1) is preserved without changing its original `e414a4df64a56c2d8a2f374741b1f1b58fceea9b` source binding. Read [the full baseline report](baseline/README.md), [all 341 complete pairs and decisions](baseline/compact-ledger.json), [four complete correction pairs and five holds](baseline/greek-corrections-and-holds.json), and the [full hash-bound packet](baseline/greek-review-packet.zip).

## Current integration

The same four accepted Greek corrections, test and fixture are composed onto develop **`75d56c8c9597f135799d2a3aac84c1e8aa3ee2a4`**, source tree `a1856f32503dce470d606ee65b88a5d1c92f0995`. Candidate tree **`58e82faaddfacc1b64d721ba3845aa28ae841580`** has 1,182 leaves: one changed Greek XML and two added regression files, with no removals, executable-mode drift or application-code edits. All 1,180 existing source leaves were verified against the live Git tree.

Since the linguistic baseline, only Turkish XML/fixture/test (PR115) and `test_ci_emulator.py` (PR116) changed. Every one of the 341 complete English/Greek baseline values, the priority manifest and all 37 directly referenced production consumer files remain byte-identical. The three Greek application blobs exactly match those independently reviewed and previously uploaded. [Current-base integration evidence](integration/verification-normal.json) records the reconciliation; it does not mislabel the historical review as newly performed or advance tracker credits.

[Current integration tests](integration/test-summary.json) and the [integration packet](integration/integration-evidence.zip) bind fresh normal/optimized aggregate runs and Greek resource compilation to that current source. The original baseline tests remain in `baseline/test-summary.json` and the historical packet.

## Limits and unchanged holds

Five Greek holds remain open and unchanged: dithering terminology/control pairing (`save20_gif_description`, with P2 `save20_dither` outside the batch), BG, FG, the colour-palette third-placeholder composition, and the absent noun context for `ui_main23`. Prior exact sampled-resize and other bounded diagnostic/SVG review credit stays preserved. PR56, Hakka, ms/id/ja/zh-HK processing-label holds, unmerged PR114 runtime and PR113 source remain untouched.

This is AI-assisted complete-pair linguistic review plus static consumer review and bounded tests. It is not whole-language acceptance, native-speaker certification, installed UI/layout/device validation or proof of executing the Kotlin consumers. Hosted exact-head review and required CI remain the merge gate. Bulk evidence is kept on this separate evidence ref, outside the application tree.

Historical packet SHA-256: `a0bbd54cd9ee2607e9ad2a3725bbeee8943d76d53d3d07a45ff89a2820304a7f` (2,800,152 bytes). Its original pending upload completed successfully once as Git blob `0c900ae3b95551588bdad27af70eb76a6415fb34`; the same blob is reused, not re-uploaded.
