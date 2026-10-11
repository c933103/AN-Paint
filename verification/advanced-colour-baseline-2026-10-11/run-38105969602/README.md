# Baseline Advanced Colour diagnostic evidence

This is a diagnostic-only archive of [run 38105969602](https://github.com/c933103/AN-Paint/actions/runs/38105969602) for [PR #50](https://github.com/c933103/AN-Paint/pull/50). It preserves original selected artifact bytes. It does **not** certify dialog fit, installed 2x-text acceptance, a green workflow, or comprehensive baseline/candidate UI acceptance.

## Provenance and scope

- Diagnostic source: `1744530d3a61e4ba9e1652c898bfbec5886e3f84`; tree `4f901f44446da1dcf83768895c99c1877ec4a3d8`.
- Untouched production source: develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`.
- Synthetic PR merge commit recorded for the run: `9b19cf47db35c30d02a86a3e676a21d372d79927`.
- Baseline and candidate diagnostic test SHA-256: `5a29d04f6071968a47c6b16d47696ae0390ef910b7c26ec316cee50188b51549`.
- Original `regression.zip`: 35,505,888 bytes; SHA-256 `9269a5bd25b170e58c3bcaded9ea22c7ca69b8f55aca08d161a499e711e5231c`.
- Original `emulator.zip`: 93,113 bytes; SHA-256 `0457d621d8459107a17dc70f9b577ae4c19abbabe842ca57afa7475a9d354992`.

The small archive contains **70 members**: 68 copied byte-for-byte from the original two artifact ZIPs and two explicitly labelled supplements. The selected original members are:

- All 24 PNGs and 8 geometry JSONs under `regression/Paintroid/build/reports/advanced-colour-diagnostic/`.
- The exact `TEST-org.catrobat.paintroid.local.AdvancedColourLayoutDiagnosticTest.xml`.
- All seven installed phase summaries, instrumentation protocols, JUnit XMLs and install logs.
- Installed source-inventory coverage JSONs, accepted-credit process-boundary protocol and verify status, and the exact `vertical-locale-pull.log` collection failure.

The supplements are the supplied derived `diagnostic-summary.json` (whose referenced JSON hashes were checked) and selected GitHub run/job metadata in `workflow-status.json`. The manifest distinguishes original archive members from these supplements. Unrelated regression images, full emulator/logcat logs, APKs and signing material are outside this archive.

Every original member was compared against its source ZIP member before packing. ZIP construction is deterministic: sorted paths, DEFLATE level 9, fixed 1980-01-01 timestamps and Unix regular-file mode 0644. Repeated construction was byte-identical; concatenated parts, ZIP CRCs and all member hashes were verified.

## What the evidence establishes

The four Robolectric NATIVE diagnostic methods completed successfully while deliberately recording negative geometry as diagnostic data. The actual production dialog was exercised on API 30/35, English/Hungarian, 640x320 dp short landscape (1280x640 rendered pixels), at 1x and 2x text.

- At 2x, the inner colour scroller has zero height; tabs/Add-to-palette labels or controls are clipped and the hex field has no visible pointer target.
- At 1x, the inner scroller remains limited to 40 pixels in English and 53 pixels in Hungarian; the hex field's label is not completely visible.
- The native Cancel pointer path closes the dialog with one close callback and zero colour-commit callbacks.

The seven existing installed API 35 phases report 99/99 methods passed: native 74, ordinary app 16, gallery draft 3, vertical 2+2, and accepted-credit seed/verify 1+1. This is existing installed-suite coverage, not installed large-font dialog acceptance.

The overall workflow **failed**. Resource generation, regression/lint and APK/source build jobs succeeded, but the emulator job failed during adb evidence collection. The retained collection log says `adb: error: failed to get feature set: device offline`. Passing individual methods does not change that failed workflow conclusion.

A later [comparison receipt](baseline-candidate-comparison-38107965583.json) independently verifies that all 32 original diagnostic files (24 PNGs and 8 JSONs) are byte-identical between this baseline and candidate `386078641e8793058573f328ce6c2805216893b9` in [run 38107965583](https://github.com/c933103/AN-Paint/actions/runs/38107965583). Candidate JVM results are 832/832, with lint successful. Its workflow still failed: all three new installed fixtures stopped at exporter cache-path preflight before their UI actions. No installed 2x acceptance is established. The receipt supersedes only the pending-comparison status in the frozen baseline archive/manifest snapshot; all archive bytes and digests remain unchanged. This evidence branch does not edit production, advance the candidate PR branch, merge changes, close PR #50, or change repository visibility or permissions.

## Retrieve and verify

The ZIP is stored as **16 ordered binary parts**, each at most 50,000 bytes. The final part is 35,715 bytes; the reconstructed archive is **785,715 bytes**.

Archive SHA-256: `219eabb9d47514d2837cd89585b2a4f1d6643ba821b699c73df1783019019ca3`.

From this directory run `python3 verify_archive.py`. It verifies each part's size and SHA-256, reconstructs the ZIP, verifies its SHA-256 and all 70 uncompressed member hashes, and writes `baseline-colour-diagnostic-evidence.zip`. It does not extract files or run tests. Alternatively, concatenate the zero-padded parts in lexical order and use `ARCHIVE.sha256`; `PARTS.sha256` and `MEMBERS.sha256` retain the independent per-file digests.

`manifest.json` is the complete source/member/part ledger. The four successful capture methods are not four successful fit assertions; no all-locales or historical localization acceptance is claimed.
