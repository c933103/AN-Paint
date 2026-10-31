# Final local aggregate evidence

Head: 4358919e4bedb1d9641be08b83707750113bff67
Tree: 71c2c50b624a0f730aa28c00eca99c9768cb2227
Actual base: c120c378ee1edc54193b6358b8a1cc5d59d05559

Normal: python3 -m unittest discover -s tools -p 'test_*.py' -v
2082 tests, 1687.468 seconds, OK, exit 0, no skips.
Optimized: python3 -O -m unittest discover -s tools -p 'test_*.py' -v
2082 tests, 1664.089 seconds, OK, exit 0, no skips.
Started 2026-10-31 08:36 UTC; both terminal by09:05. Separate temporary paths. Complete tracked-source SHA256 manifest compared after runs: zero changed files. The current 36-leaf candidate manifest is in racefix-candidate-manifest.json.

Negative-control tests intentionally print simulated unsuccessful adb/device receipts after unittest's OK summary; these are not failed tests or real device collection. Actual result is the unittest aggregate and exit status above.

The earlier optimized empty-PID failure is preserved separately, not relabeled passed. Atomic readiness publication fixes only the fake-process test handshake. Real signalling, owned-client reaping, timeout and no-promotion assertions remain intact.

Exact-head Codex receipt: https://github.com/c933103/AN-Paint/pull/247#issuecomment-6541298174 (no findings).
Hosted CI: https://github.com/c933103/AN-Paint/actions/runs/41185740273 still running at publication. No merge or release claimed.
