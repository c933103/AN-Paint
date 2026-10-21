# Czech Fit baseline: measured failure, 21 October 2026

These are NEW synthetic-fixture test outputs, not the original Czech linguistic
review/archive whose separate publication remains pending. They are retained
outside the application PR to preserve the failed measurement after CI expiry.

- Frozen test-only PR: [#159](https://github.com/c933103/AN-Paint/pull/159).
- Head: `9203a6e9fdbdc9a49ba786fe7246ea6a4786e2b6`.
- Initial source base: `1c9b71afb5f5cbde39bc5fff70630bca1a7a3419`.
- [Run 39547438361, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/39547438361).
- [Original regression artifact 12322474961](https://github.com/c933103/AN-Paint/actions/runs/39547438361/artifacts/12322474961),
  SHA256 `f6fa1f00057135c9316847b04c818063bac805951ff711620041f5d23628c9bc`.
- The downloaded archive digest was verified; these nine XML/JSON/PNG files are
  exact extracted bytes, not edited screenshots or reconstructed measurements.

All four Czech Fit native-layout tests fail the complete-caption-height check.
The control is 88 × 88 px at xhdpi, with only 64 px of padded text height. Normal
text needs 186 px across six lines; enlarged text needs 647 px across eleven
lines. Captures establish 640 × 1280 and 1280 × 640 px actual roots. The caption
and accessible text are both the complete “Přizpůsobit obrázek oknu”.

1,268 JVM tests completed with exactly these four failures. Android lint passed.
The unrelated core emulator setup initially failed because the downloaded Google
API35 image was not a ZIP; its single retry is tracked in the same run, without
replacing this failed JVM attempt. The position emulator passed. Neither generic
emulator result establishes an installed Czech workflow pass.

Evidence layer: mounted Robolectric NATIVE Android rendering. Not installed
emulator interaction, physical-device, fluent-native-speaker or TalkBack-service
acceptance. The original 645 bounded static accepts / 72 holds remain unchanged,
and all seven-group Czech workflow acceptance remains open. No release action.

The bounded follow-on [Fit repair #160](https://github.com/c933103/AN-Paint/pull/160)
uses merged #114 source. Its first candidate failed Android compilation on an
inherited LayoutParams name; the correction is a descendant, not a rewritten
baseline. Candidate compilation/native outcomes are reported on that PR and must
not be inferred from these baseline files. Codec findings and the separate
installed-workflow verification job are different checks.
