# PR245 exact accepted translation packet — pre-PR246 verification

Source head: ad69647b3ff884348e61b547fcfbc4d518bad18a
Tree: dd2f9908d583fe3bf2e522750e67ac2236af9a4c
Base: c000194d3f96b89896d679214d2a43889a27356a

90 absent additions + 15 exact existing replacements; historical fixtures and unrelated resources unchanged. Ledger receipt: https://github.com/c933103/AN-Paint/pull/56#issuecomment-6532854518
Ledger SHA-256: 5f89c0c30a828b9a81a0210065b180a4202c599329f4ec7355b84bd8b6a4d666

Normal: python3 -m unittest discover -s tools -p 'test_*.py' -v
2,075 tests, 1705.275 seconds, OK, exit 0, no skips.
Optimized: python3 -O -m unittest discover -s tools -p 'test_*.py'
2,075 tests, 1605.124 seconds, OK, exit 0, no skips.
Logs include expected stderr/output from negative instrumentation-protocol fixtures after unittest's OK; they are not actual device executions.

Original-head hosted run41174357457: only Python failure was stale ARY registration count348!=359, corrected in the source head above. 2,075 tests, one failure, two optional Pillow skips. JVM/lint, APK/source, resource generation and all API35 emulator checks passed. Current-head hosted run41176348903 pending when this evidence was recorded. Neither result resolves PR244's intermittent synthetic IME failure.

The two hosted skips are IcoContainerTest.test_adam7_fixture_pixels_match_independent_pillow_decoder and test_export_opens_with_independent_pillow_ico_decoder. Both run and pass locally (normal verbose log). Optional Pillow skip is explicit ImportError, independent structure/scanline checks remain active.

PR246 must merge first, then PR245 will sync to actual develop and rerun/review the final exact head. No final merge or mainline verification is claimed by this evidence. Projected remaining queue737 missing +2existing only after PR245 merge; develop at this recording remains827/17. No release.
