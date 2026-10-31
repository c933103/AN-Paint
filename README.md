# PR245 exact accepted translation packet — final synchronized verification

Source head: aad55c3a2c362cd2ae183e18d122cd31c9b56e44
Tree: a05f9c3648f884470e2694006d64b68ace65f1a8
Base: fa78546e03ebf3e13f4d722104323d850a019315

90 absent additions + 15 exact existing replacements; historical fixtures and unrelated resources unchanged. Ledger receipt: https://github.com/c933103/AN-Paint/pull/56#issuecomment-6532854518
Ledger SHA-256: 5f89c0c30a828b9a81a0210065b180a4202c599329f4ec7355b84bd8b6a4d666

Normal: python3 -m unittest discover -s tools -p 'test_*.py' -v
2,075 tests, 1453.973 seconds, OK, exit 0, no skips.
Optimized: python3 -O -m unittest discover -s tools -p 'test_*.py'
2,075 tests, 1457.530 seconds, OK, exit 0, no skips.
Logs include expected stderr/output from negative instrumentation-protocol fixtures after unittest's OK; they are not actual device executions.

Original-head hosted run41174357457: only Python failure was stale ARY registration count348!=359, corrected in the source head above. 2,075 tests, one failure, two optional Pillow skips. JVM/lint, APK/source, resource generation and all API35 emulator checks passed. Final-head hosted run41178906410: APK/source, resource generation and all API35 emulator jobs pass; regression/lint pending when this evidence was recorded. Neither result resolves PR244's intermittent synthetic IME failure.

The two hosted skips are IcoContainerTest.test_adam7_fixture_pixels_match_independent_pillow_decoder and test_export_opens_with_independent_pillow_ico_decoder. Both run and pass locally (normal verbose log). Optional Pillow skip is explicit ImportError, independent structure/scanline checks remain active.

PR246 actually merged as the Base above. PR245 includes its exact five fixture-fix leaves; full host suites were rerun against the final synchronized tree. Final-head Codex code review is complete with no findings. No final merge or mainline verification is claimed by this evidence. Projected remaining queue737 missing +2existing only after PR245 merge; develop at this recording remains827/17. No release.
