# Third complete PR #30 CI run

[Run 37933455983](https://github.com/c933103/AN-Paint/actions/runs/37933455983)
tested merge `dd859613417ef8c851ac994d7a7add93111d426e`, whose tree
`86adf24e80c9acc6f0908549bd6d79b3fa1c55ee` exactly matches source head
`9043849728a6a8075b19fc2f98208612721f2c14`.

- APK/source and instrumentation APK compilation passed.
- JVM: **706 tests, 8 failures, zero errors/skips**. All failures are the host
  reachability browser-visibility assertion, at the first French scenario.
- All **1,680 control-layout cases** passed: 140 catalogues × 3 widths × 2 scales
  × API30/35. Four JUnit executions took 22.003 seconds; per-matrix counts and
  measured loop times are retained in `matrix-summary.json`.
- The 4 vertical status/description executions and 8 existing full SVG status
  checks passed. Other representative reachability languages were not reached.
- Lint analysis started, but the unchanged **12-minute step deadline** expired
  before a report was produced. This run has no completed lint result. In contrast,
  both earlier complete runs did finish lint with zero issues under `--continue`;
  their previous narrative saying it was not reached has been corrected.
- API35 installed: **74 library + 18 ordinary app + 1 restart seed + 1 restart
  verification = 94 passed**. The ordinary suite took **154.988s / 180s**, including
  the new real-browser font/rotation test. Seed/verify took 4.596s/6.659s.
- Actual installed French/Mongolian browser dimensions at system 2×: 320×120px in
  portrait, 640×90px in landscape, with the entire browser visible, no controls
  overlap, preserved query/objects, and exact language preference cleanup.
  `installed-viewport.json` preserves the actual four logcat records.

`test-results.json` inventories all 800 JVM/installed cases. The two downloaded
ZIPs were SHA256 verified before safe extraction; `artifact-manifest.json` records
all 645 constituent files. These historical failures are retained, not overwritten
with later results. No physical-device or TalkBack acceptance is claimed.

## Remaining host-provider boundary

The original host proxy does not apply `WebView.setFrame` coordinates. It returns
false without calling the superclass, so actual width/height remain zero despite
measurement and correctly sized windows. The test-only correction forwards only
the parent's supplied frame through the framework's `PrivateAccess.super_setFrame`.
It records the frame, MeasureSpecs and measured/actual size, and keeps all original
visibility, reserve, rotation and reachability assertions. See the exact platform
references in [the framework evidence](../review-native-contracts.md).
