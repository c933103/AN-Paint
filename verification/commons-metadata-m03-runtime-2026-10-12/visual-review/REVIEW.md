# M03 rendered-status review, 12 October 2026

No actionable rendered-status defect was identified in the 16 inspected screenshots. This is a bounded rendering result, not a merge/readiness or linguistic-certification decision.

## Exact evidence

- Source head: `d4ee9762580bbaf983fc58edb84755840c31626c`.
- Tested merge commit: `d43c6b33fdb79b93d1be137d8f332f9be579ca91`.
- Shared source/tested tree: `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`.
- [GitHub run 38191148104](https://github.com/c933103/AN-Paint/actions/runs/38191148104), artifact `11720749614`.
- Archive SHA-256: `63bdbe65c224fe0f8dad1416b6d5ce7d4c2c623cdf94a2c73daf17d432367a1f`.

The archive digest, all 48 extracted PNG/JSON pairs against archive bytes, all 16 selected messages against source resources, and the staged Git tree ID were independently recomputed. The GitHub head/merge/tree association comes from the parent's verified run metadata; PNG sidecars do not embed commit IDs. The local checkpoint commit ID differs, but its staged tree matches the tested tree exactly.

All images are **Robolectric NATIVE host rendering**, API 35, 320 × 640 dp at xhdpi (640 × 1280 pixels). They are not installed-device screenshots. Visually inspected: Ainu Kana, Ainu Latin, Manchu and Vietnamese Hán/Nôm, each for copy and insertion at font scales 1 and 2. The other 32 M03 captures received integrity/metadata checks only. [review.json](review.json) contains exact per-image and sidecar hashes and individual observations.

## Visual findings

- **Ainu Kana and Latin:** full M03 status is visible through its final punctuation at both scales, without apparent tofu, overlapping status lines or clipped status ink. At 2×, the Kana screen has scrolled the controls to reveal the status; lower controls continue beyond the initial viewport.
- **Vietnamese Hán/Nôm:** full M03 status is visible at both scales, including U+8FD4 (返), without apparent tofu or status clipping. All four PNG hashes also match the initial-head captures, but this conclusion uses the independently verified copies in the successor archive.
- **Manchu:** normal-scale status is wholly visible in vertical columns without apparent tofu or vertical ink clipping. At 2×, the status rail shows its trailing columns and a partially visible left-edge column. This is horizontal scroll-window clipping at the recorded terminal position; it does not establish an application defect or unreachable text. The offscreen 2× columns were not visually certified.

Archived JUnit XML independently totals **820 tests across 87 suites, with zero failures, errors or skips**. The M03 flow suite has 12 passing tests and translation suite has 4. These are inspected hosted results, not a local rerun. All 16 selected JSON messages exactly match the corresponding resource wrapper and M03 reason.

## Scroll and capture interpretation

The M03 flow checks assert complete source/accessibility text, no ellipsizing, complete measured layout and visibility. Horizontal statuses additionally have their full visible bounds checked. For vertical statuses, the test programmatically scrolls to both rail ends and checks full-height visibility and the corresponding content edges.

The vertical test then calls `resetToReadingStart()` immediately before drawing. That method requests layout; no additional explicit layout occurs before the PNG. The Manchu 2× stills therefore show the terminal tested position rather than a fresh reading-start view. This limits the stills, while both-end reachability assertions passed. It does not establish a first-reading-position application defect. This review also does not claim M03 touch-gesture or physical-device verification.

## Disclosed limits

No competent-language, native-speaker or script-specific shaping certification is claimed. Source equality, intact layout and visible glyphs are narrower evidence.

The previously disclosed Pillow/FreeType U+8FD4 source/subset difference at 24 px remains a raster-equivalence limit. The 48/96 px match and preserved outlines/metrics do not prove all-size pixel identity; no cause is inferred here. The difference is not itself an application bug, and no actionable defect is apparent in these actual app-status renders.

Installed API 35 font loading/hash checks are separate evidence and do not directly exercise M03 status text. This report makes no claim about their outcome. No unrelated blocker or mandatory human/native approval gate is introduced.

No source edits, heavy tests, remote writes, or merge/readiness decisions were performed in this review.
