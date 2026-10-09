# Second complete PR #30 CI run

[Run 37929847403](https://github.com/c933103/AN-Paint/actions/runs/37929847403)
tested merge `e7344d010af9bcdd4af411070dd4a735bc48b71e`, tree
`a720e10cd6d9ca2720b5a958dbe0d4d346aa35f7`, exactly matching source
`47208ff518f3ddd990e152ae2395f9887aade18a`.

- APK/source/instrumentation compilation passed.
- JVM: 706 tests, 12 failures, zero errors/skips; lint not reached. These are
  later checks than the first run, not repeat failures of the corrected setup.
- Attached nodes now expose native Button/EditText classes and live values.
  Normal-scale matrix executions completed 6 cases each before the Ainu hint
  check; large-scale executions reached an English-search-hint check before
  completing the first case. Full catalogue coverage/runtime remains unverified.
- All eight real-Activity executions completed French same-Activity rotation and
  action/query reachability. Captured ViewRoot, Display and decor bounds agree
  after each resize/restoration, including 640×1280 ↔ 1280×640 and 480×960 ↔
  960×480. They later stopped at the no-op host WebView's visibility assertion;
  later representative languages/gestures were not reached.
- Installed API35: all 93 passed. Ordinary app 17 cases took 154.401 seconds under
  the unchanged 180-second deadline. Other groups: 74/65.420s, seed 1/6.352s,
  verify 1/7.510s. This precedes the added installed browser-viewport case.

The complete case inventory/failure details and hash-verified artifact manifests
are retained here. Original ZIPs were also retained; Actions retention is finite.
The [native drawing/measurement contract correction](../review-native-contracts.md)
documents the next bounded test changes and their explicit limitations.
