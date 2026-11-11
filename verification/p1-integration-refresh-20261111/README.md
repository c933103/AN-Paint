# P1 integration refresh, 11 November 2026

## Current state

Existing PR #395 was refreshed to `59a6a4a43396c1db402e705cbc3a16b39f564cae`, with ordered parents `53589f6a3f7c235dccde06c723fcae0684b1432f` and actual develop `c3f58c6cbebbc3bc385b79143352ad87e4233d67`. Its verified tree is `5b770dca9d41f84dd73a69d017cb3609809892a6`.

Only the original three-file source fix differs from develop. The downloader and retry test retain their exact original reviewed blobs. CI.md combines the independent current cache paragraph and original source-transport section. No substantive three-way conflict was found. All 1,283 remote leaves and modes were checked; all resources and other develop work are preserved. The existing branch was updated with a non-force expected-head lease, not replaced.

Fresh local source-fix validation passed 22 affected downloader/native-cache/Gradle-cache tests, Python compilation and diff whitespace checks. One preliminary invocation lacked the not-yet-materialized workflow input; the full invocation passed after fetching and checking its immutable blob. Android SDK/device tests were not run locally.

[Normal exact-head CI run 43014684262](https://github.com/c933103/AN-Paint/actions/runs/43014684262), attempt 1, remains pending at preparation publication. Current-head code review completed clean. Security review was requested once because its summary still referred to the old head. The old qualifications do not transfer automatically, and this preparation is not merge or release acceptance.

## Preserved translation preparation

The separate local dry run reconciles the original resource-only additions from #396, #397 and #398 against the refreshed current source:

- #396: 423 entries in 22 files.
- #397: 405 entries in 17 files.
- #398: 554 entries in 26 files.
- Total: 1,382 distinct additions in 62 canonical catalogues. Every original reviewed XML node value and attribute is retained exactly.
- All 23,225 existing complete nodes in those 62 current develop files are preserved. No key collision, prior-value revision, deletion, or held-key import occurred.

The preparation passed 46 affected current translation/resource/priority tests. An initial broad module invocation passed these 46 and errored on six unrelated unchanged provenance tests because their source JSON/notice inputs were not materialized. The affected classes were subsequently run explicitly and passed; this is not a claim that the entire host suite passed.

The actual Java 21 source launcher executed 543 exact-output formatting cases across 181 templates: boundary integer/hex values and format-looking literal string arguments. The standalone javac command was absent; the installed Java compiler module executed the source successfully. All 1,382 additions passed XML uniqueness, source-attribute/placeholder, Android escaping, NFC, exact newline sequence and P1 membership checks.

Prospective direct resource presence across all 171 options: P0 16,074/16,074; P1 47,683/48,393, with the same 710 separate held-key gaps; P2 22,828/46,683; P3 4,777/11,799. These are prospective source-presence counts only. The translation PR heads remain unchanged and unmerged at this checkpoint.

## Packet and reproduction

`preparation.zip` SHA-256: `dcd78e925cefea9883cd8f91a33c480609aa404e8f2f4cef8d3ab68ff2ce6383`.

The ZIP contains the exact original PR patch records, current develop tree metadata, merge-preparation script, original-additions-only patch, per-stage report, raw local test outcomes, Java test source/input/results and a SHA-256 member manifest. Source files remain available at the immutable commits rather than being duplicated in the packet.

To reproduce the translation dry run, materialize tracked source from the refreshed #395 head into a sibling `stack-dryrun` directory, place the packet files next to it, and execute `prepare_stack.py` once. It validates baseline resource Git identities before appending exact original nodes. Its named test modules use the same source tree. Run `java StackFormattingCheck.java stack-format-cases.tsv` for the formatting cases. The script is a one-time evidence helper, not a new application or CI contract.

## Boundaries

No fresh linguistic acceptance, native-speaker certification, installed layout/glyph/speech acceptance, Android build, physical-device claim or release is made by the preparation. Previous source-grounded review and its limitations remain in the original PRs. No duplicate translation work or merged-count credit is claimed. New heads must complete their own exact-head review and required CI, and actual merge trees must be verified. Separate held work remains untouched.
