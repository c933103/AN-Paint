# Retained failed visual evidence and focused capture repair

## Exact historical attempt

These are the original 32 PNGs from [PR18 run 38019403273, attempt 2](https://github.com/c933103/AN-Paint/actions/runs/38019403273/attempts/2), not screenshots produced by this repair.

- Head: `dc47456df0eea18f106d6e0af056f01af1ba6c20`.
- Tested merge: `4abfa07b2a7b1860358edd88e9572b8fd0810cfb`.
- Independently matched source tree: `3f048ba323fb0a4dc3243b900ac50b9cf7cc6d8c`.
- Artifact: [11658950966](https://github.com/c933103/AN-Paint/actions/runs/38019403273/artifacts/11658950966).
- Verified artifact ZIP SHA-256: `e308b61fe75ed56df887475ac0e3335002ca08083bc94100a1117153dff8eb77`.
- All 98 installed XML cases passed; the 24-method API35 app union and the seed/live-process/force-stop/verify boundary passed.
- The previous attempt failed screenshot collection with `device offline`; its [failure receipt](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6093291604) remains distinct. This controlled retry changed no source, binaries, assertions or timeout.

Every PNG here was copied byte-for-byte from the digest-verified artifact, matched to its original receipt, fully decoded and opened individually. `visual-receipt.json` binds every filename, size, dimension and SHA-256 to the exact source/run/artifact identity.

## Blocking visual result

`en-XV-landscape-format-popup.png` shows the closed Save form. It is byte-for-byte and pixel-identical to `en-XV-landscape-save-initial.png`; both hashes are `afdd1076f74eb23b605c15409060dff8fd6d1d71b6fbbcbcf482b99d3d52c16d`.

The other seven popup images show an open popup. Other states show the retained canvas/sentinels, initial Save forms and JPEG quality controls. Manchu joining, upright Literary Chinese glyphs and displayed emoji are visible in the captured viewports. Neighboring columns and portions of labels may lie outside the current horizontally scrolling viewport. These are bounded observations, not linguistic or physical-device certification.

The complete visual matrix is **not accepted**, despite the successful runtime and valid 32-file inventory. The [PR receipt](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6093408865) preserves this distinction.

## Focused repair

The test previously waited for a shown popup ListView, which can precede the display of its first frame. Before the popup screenshot, the repair waits for stable native-popup geometry, observes a hardware frame commit and the next two animation-frame callbacks, then checks that the same popup remains attached and shown. It invalidates the existing popup to request a redraw; it never reopens it, repeats its tap or changes selection. Callback removal runs in `finally`; the frame wait is bounded to three seconds within the unchanged instrumentation deadline.

A frame commit is submission to the swap chain, not a guarantee that pixels are already visible. The following frame callbacks provide display opportunities; the captured popup is also rejected if it exactly repeats the closed Save image. The host receipt now rejects exact duplicate content anywhere in the 32 required states. Neither check is full semantic image validation, so every new-head image still requires visual review.

References: [Android frame-commit contract](https://developer.android.com/reference/android/view/ViewTreeObserver#registerFrameCommitCallback(java.lang.Runnable)), [View frame callbacks](https://developer.android.com/reference/android/view/View#postOnAnimation(java.lang.Runnable)). The suite already requires API29 and tests API30/API35; no new dependency is added.

The collector, native actions, canvas/Save/PNG assertions, SDK-specific phase union, restart boundary and all existing outer/instrumentation timeouts remain unchanged. Host tests replay both a synthetic duplicate and this exact rejected 32-image set. New exact-head compilation, installed XML and all 32 actual screenshots remain required before accepting the repair.

## Local verification of this repair

- Full host suite: 382 tests passed, no skips, in 55.468 seconds; actual output is retained in `repair-host-checks.log`.
- Focused matrix suite: 11 tests passed, including replay of this exact 32-image failure.
- Bash syntax and whitespace checks passed.
- These are source/host results. The changed Kotlin and fresh 32-state visual matrix have not yet been accepted by exact-head Android CI.
