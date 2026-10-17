# Greek P0 + P1 linguistic review, 17 October 2026

## Result and exact scope

Read all **341 complete English/Greek pairs** in Greek (`el`): **92 P0 + 249 P1**, with current production references and surrounding source where present. Source: [`e414a4df64a56c2d8a2f374741b1f1b58fceea9b`](https://github.com/c933103/AN-Paint/commit/e414a4df64a56c2d8a2f374741b1f1b58fceea9b), tree `74972d7a7e6fb94015d2b7dcb51a2b64796f6bed`. Greek catalogue baseline blob `d3bf88390e9b2858d59b81b7c415b352f9ac8106`. The canonical translatable catalogue has 717 entries; 376 outside this batch were not linguistically reviewed.

Baseline judgments: **304 accepted with static current consumer context, 28 accepted for catalogue semantics only, 4 correction proposals, 5 open holds**. Thirty entries have no direct current production reference; two of those remain held. The individually authored judgments, confidence, full values, typed keys, SHA-256 value hashes and current consumer snapshots are in `greek-p0-p1-341-review.json` inside the packet. `compact-ledger.json` preserves all 341 full pairs and judgments in a smaller standalone file. Structural validation supports this actual pair-by-pair reading; it is not substituted for it.

## Four accepted bounded corrections

The application candidate changes only four Greek values, one compact full-value fixture and one focused regression test. No Kotlin/runtime source changes.

- Save-changes question: untranslated `Save changes?` → `Αποθήκευση των αλλαγών;`. Greek semicolon marks the question. Shown above the translated unsaved-change message with Save/Discard/Keep editing.
- Recovery instructions: replace `Αρχείο > Φόρτωση εικόνας` with `Αρχείο > Άνοιγμα εικόνας`, matching the actual File menu entry while preserving `canvas.png`, ZIP, draft settings and floating selection.
- Language explanation: preserve both source cases, new or untranslated text, and remove the unsupported temporary/post-update-only fallback implication. Complete proposed text is in the correction record.
- Shape style: untranslated `Fill` → `Συμπαγές γέμισμα`, distinct from outline and fill-plus-line.

`greek-corrections-and-holds.json` contains every complete English/current/proposed pair, hash and relevant consumer context. Independent parent review accepted these four pairs; an additional independent application/test review found no blocking changes. See `acceptance-and-limits.json`. The original baseline ledger remains unchanged; its proposal-pending labels describe the baseline review stage, while this acceptance record records the later bounded candidate decision. No tracker credit was silently advanced.

## Five holds stay explicit

1. `save20_gif_description`: Greek dithering terminology needs joint review with the outside-batch P2 `save20_dither` control. GIMP distinguishes dithering (Πρόσμειξη) from the spread filter (Διασπορά); this corroborates concern, not automatic authority to replace AN Paint terminology. Both strings are unchanged.
2. `ui_bg`: English BG abbreviation, despite full Greek accessibility description; localized compact fit/comprehension unresolved.
3. `ui_fg`: same FG abbreviation issue.
4. `ui_foreground_background_colour_palette`: third placeholder's actual composition has no current consumer; grammar remains unresolved.
5. `ui_main23`: the adjective Κύρια depends on an absent consumer/noun context.

PR56 is untouched. Existing Hakka and ms/id/ja/zh-HK processing-label holds remain untouched. Unmerged PR114 runtime and PR113 source are excluded.

## Prior credit preserved

Prior tracker receipts are retained byte-for-byte (Git blob `004a38a070bc4ea215a82fdd41028aac5e341f3b`). The exact overlapping Greek P0/P1 receipt for `ui_sampled_resize_memory_explanation` is preserved without new credit. Prior bounded colour-import diagnostic work (PR86) and two SVG-size messages (PR29) are recorded as prior work. Withdrawn historical PR7 claims remain withdrawn. No whole-language or tracker acceptance count is claimed.

## Evidence and reproduction

The packet includes complete ledgers, per-entry authored decisions, full source/target pairs, exact source and candidate file manifests, current consumer text, original English/Greek resources, candidate three files, compact fixtures, verification scripts, logs and compiled Greek resource output. The text-source subset is explicitly listed by the packet manifest; it is not a full checkout. For full-tree integrity reproduction, restore all baseline files from commit `e414a4df` into `source/`, copy that tree to `candidate/`, apply `greek-application.patch` there, then run `python validate_packet.py` and `python -O validate_packet.py`. These checks require the full checkout; `source-manifest.json` binds every one of its 1,178 leaves. Python bytecode caches are excluded from publishable file manifests.

Full-value fixture contracts exercise all four complete bilingual values, attributes, placeholders and newline structure, with missing/duplicate/truncated/wrong-type/markup/format/escape negative cases. Every former Greek value is rejected by the new full-value contract. Forward and reverse patch application preserves exact bytes. Candidate tree: `1e889212ae7ab9b58ada819dfd0981405b2b526f`, **1,180 leaves, no removals**.

See `test-summary.json` for terminal results and exact commands. Bulk evidence is isolated from the application branch. No native-speaker certification, whole-language acceptance, Android runtime/layout/device/APK/JVM/lint acceptance, or execution of the source-described consumers is claimed. Hosted exact-head review and required CI remain the merge gate.

Primary terminology references: [Microsoft Greek solid fill](https://support.microsoft.com/el-gr/office/graphics-visuals/create-a-venn-diagram), [Microsoft save-changes prompt](https://support.microsoft.com/el-GR/Excel/how-to-suppress-save-changes-prompt-when-you-close-a-workbook-in-excel), [GIMP Greek dithering](https://docs.gimp.org/3.0/el/gimp-filter-dither.html), [GIMP Greek spread](https://testing.docs.gimp.org/3.2/el/gimp-filter-noise-spread.html), [GIMP foreground/background swap](https://docs.gimp.org/3.0/el/gimp-tools.html).
