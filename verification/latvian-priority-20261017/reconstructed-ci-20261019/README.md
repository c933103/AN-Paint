# Latvian PR128: reconstructed terminal CI receipts, 19 October 2026

[PR128](https://github.com/c933103/AN-Paint/pull/128) is merged as `d47ae81a7dca1ab562ab0e8b276b13c24a374cee`. Original reviewed head: `d72b43478c020f55faae9e358f57ff88b3254b0d`. Both have application tree `ff1b183c1449a10f55d43489ef8d41541f11ff5c`.

## Verified terminal results

- [Original run39076034363](https://github.com/c933103/AN-Paint/actions/runs/39076034363) and [natural postmerge run39078309138](https://github.com/c933103/AN-Paint/actions/runs/39078309138): all six jobs passed, each on attempt1.
- Each run's recovered regression artifact contains **120 suites / 1,123 JVM tests**, zero failures, errors or skips. All **six Latvian actual-consumer methods passed**.
- Each run's recovered API35 artifact contains **119/119 tests across ten phases** (74 native plus 45 app), no missing/unexpected cases, errors or timeouts. Core and position identities record attempt1.
- Device identity records bind the original run to checkout `5f699f3ade3264b77b3e795d2c98fde51fbf9797`, and the postmerge run to `d47ae81a7dca1ab562ab0e8b276b13c24a374cee`; both Git commits have the reviewed tree. Their APK/source hashes are retained identity observations. This recovery did not download large APK/source build ZIP bytes.
- Regression, API35 and exact-script artifacts for both runs were re-downloaded and independently matched against all six GitHub SHA-256 artifact digests before parsing.

## Reconstruction and interrupted upload

The earlier hosted-evidence upload did not produce a published followup ref. Its README exists as Git blob `96c9da7da1215b639ecfda03ffb24fdefbf315af`, verified by complete readback. The original manifest/ZIP object identities have no receipt and remain unresolved. The original local ZIP bytes became unavailable with the old workspace. Its historically recorded SHA-256 was `2a0deac5f2208d5d40cfbb7065f44eec4f739bfbecc9a68caee89d457e55df97`; this is not the hash of the new packet.

[New reconstructed packet](reconstructed-ci-receipts.zip), SHA-256 `b3d1bbbaf9800e7f9975d23bf7b197f5cab872e0fe1f481b14601cfe87f18b97`, is explicitly newly assembled from the original GitHub artifacts on 19 October. It preserves complete JUnit XML, lint output, exact-script outputs, API35 phase reports/runner logs, source identities and artifact inventories. Large global logcat, screenshot/export binaries and APK/source ZIPs are not duplicated; the inventories identify exactly what is preserved. [Manifest](manifest.json) hashes every enclosed file. The proposed old README is included as historical input only; its relative archive links are not publication receipts.

## Linguistic scope remains unchanged

[Original complete linguistic ledger and independent review](https://github.com/c933103/AN-Paint/blob/d9e4d1f1198ad2641f27ddc4d21166c6561f37f1/verification/latvian-priority-20261017/README.md) remain intact: **341 P0/P1 pairs; 285 bounded accepted, 28 wording-only, 10 corrected, 18 uncertain unchanged**. One historical priority receipt overlaps; 340 had no prior tracker receipt. Ten priority values plus one required P2 width-template companion changed. This technical recovery adds no linguistic review credit and makes no native-fluency, installed-Latvian or TalkBack claim. PR56 and all other explicit holds remain untouched.

The original independent report's `remote_base_tree_sha` field contains the base commit identifier; the correct base tree is `d87d0431f5ebf2e0c01f7d4d0f716b89df7c1aea`, already recorded in the main ledger and validation. Original reports are preserved rather than rewritten.
