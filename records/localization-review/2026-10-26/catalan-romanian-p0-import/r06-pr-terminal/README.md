# PR177 exact-head terminal evidence

[PR177](https://github.com/c933103/AN-Paint/pull/177), reviewed head `10acbff912812b938bf2626be1e8a9e84e7aa7bc`, passed all six checks in [run40323966400](https://github.com/c933103/AN-Paint/actions/runs/40323966400). Exact-head Code review is clean. Optional Security from the previous head is historical and is not a required merge gate or current-head claim. This is PR evidence, not actual develop integration or postmerge evidence.

The tested synthetic merge `fb6b356d6fd87ecbdf79ddc816a92fd87fbfda17` has ordered parents `6a42948a3ac7bad241d502f3b6c18ebf1c0327d8` plus the reviewed head and exact tree `f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c`. All 1,376 source blobs and 1,373 packaged tracked files were verified, with the same three explicit dotfile exclusions; embedded and external source ZIPs match. Extra generated/vendor members are counted, not authenticated by the project Git tree.

Actual hosted results:
- JUnit: **1361 tests** in 147 reports, zero failures/errors/skips. All eight focused source-method sets match: CA/RO Import2, prior CA/RO Save2, DA/NO4, NN remaining4, NN Save2, DerivedExport7, ImportSelection12, TaggedColour5.
- Hosted Python: **1389 run = 1387 passed + 2 skipped**, 264.288 seconds. Nonverbose skip identities are not guessed. Local ordinary and optimized 1,389/zero-skip results remain separate in r05.
- Lint: **0 issues**; all four phase exit codes zero.
- API35: **45 app + 74 native** exact source-case sets passed; prebuilt main/test APK and source identities revalidated.
- All **13 exact-script probes**, including expected reserved-variant rejection, have matching hashes and expected exits.
- All **282 scoped compiled values** match: 13 ca +13 ro new, 10 ca +10 ro +78 da +78 no +80 nn prior. CI-debug signature v1/v2 verifies.

APK SHA-256: `1508e1789f00eaafae1febc52ab053679b26c5237224dd8f694ba23691eb839a`. Corresponding-source ZIP SHA-256: `f476a42f7b94b2826df8e6a5d173386fdd3fb82317011934f9d06a7624701f29`.

Four synthetic positives and 33 negatives pass in both Python modes; synthetic mocks are not actual hosted/runtime evidence. The first local full-suite two-error stale direct-value oracle result is retained in r03. The actual original-head one-failure JVM parent-inheritance oracle result is retained in r04, and its two-test repair/local evidence in r05. A clean but commit-unbound Code receipt is preserved separately and is not counted as exact-head proof; the necessary receipt-repair request is recorded.

All 26 missing-only values retain bounded independent AI whole-value linguistic/static acceptance. All 274 inherited values, ten explicit held absences, mixed English frame counts and Image format labels, paired P1/frozen history, global59/112 scope and #56/#113/#159 plus Help/archive/release pauses remain unchanged. Current tagged-colour structural70/101 is separate from runtime70direct+1parent-inherited+100English; no Valencian acceptance. Actual new tests exercise scanner/dialog ownership, frame/poster wording, Save option transitions, invalid-name rejection and cancellation. PDF and unsupported-colour decoder branches retain compiled/static checks and are not newly runtime-exercised by this scope. No native-human, physical-device, layout, whole-locale, private-signing or release claim. Final live base/head lease remains required at merge.
