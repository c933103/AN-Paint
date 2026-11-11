# PR 429 final qualification

Thirty independently reviewed active P2 additions are merged as `e2ed367a9459907effcfb5f877c7dd86ef56a8f7`, tree `287767b1e2d5566947d31cb3a3734054ca4835fb`. Serbian Cyrillic 9, Hebrew 8, Armenian 7, Nepali 6. All 1,672 previous XML nodes/attributes remain unchanged.

## Source-bound acceptance
- Exact head `984ae0731e566dda68d25d79feb29eaca153bc19` passed all seven jobs in [42959591225](https://github.com/c933103/AN-Paint/actions/runs/42959591225), attempt 1. Trusted current-head Codex code review completed with no findings; security marker completed with its gate disabled. Zero review threads.
- Actual merge and tested checkout `51552b6af55aae035f2c9e6fea87c99036966d94` have identical complete source trees and the expected ordered base/head parents. Develop matched the actual merge at terminal verification.
- Independently downloaded/hash-verified original APK/source, instrumentation APK, exact-script, regression and composed API35 archives. All 1,280 included tracked source blobs match; the three longstanding bundle exclusions remain unchanged. Embedded and standalone corresponding source match.
- Verified 13 exact-script expected outcomes, Python 865 passes plus 2 optional skips, JVM 1,392 passes (zero failures/errors/skips), clean lint, native API35 74 tests and app API35 50 tests. Re-ran the existing current-source app report validator against the downloaded reports, including the complete source-test identity union. Composed APK/source/test APK identities match independently hashed bytes.

## Actual-develop verification
[Push run 42962455517](https://github.com/c933103/AN-Paint/actions/runs/42962455517) succeeded through bounded same-tree reuse of the original PR experiment. Preflight ran; six downstream jobs were **skipped, not newly executed successes**. Downloaded receipt artifact 13829144857 has SHA-256 `9ce53669190aba90bec0dcb718109d74f48a3d6e2aa8ed1b08903551db8e9497`. Its merge/base/head/tree, original run/checkout/attempt, review identity and all six original artifact records match independently fetched metadata. The workflow checked original core/position bytes; this follow-up did not redownload those separate archives.

## Evidence and limits
`verified-results.zip`: 422,876 bytes, 255 members, SHA-256 `4d56d9535dd9f7ae631cbb161e70824e351eb5d49cc57d39c135b854af9da401`. Preserves raw JVM and phase reports, composed JSON reports, exact-script archive, original postmerge receipt, verifiers, terminal checks, review and source/artifact identities. Large APKs/screenshots are not duplicated in this compact packet.

The original preparation and full independent wording review remain beside this file. Independent review retained 28 and revised two URL-redirect messages. Four Armenian/Nepali redirect clauses and all prior holds remain unchanged.

Merged direct presence: P0 16,074/16,074; P1 46,301/48,393; P2 22,632/46,683; P3 4,777/11,799. Across 171 catalogues: 89,784/122,949, with 33,165 missing, 65 complete and 106 partial. Presence and model/source review do not establish native-human or exhaustive installed layout/glyph/speech/device acceptance. Hebrew mixed RTL/LTR display and vendor app-label limits remain. No API30 run, private upgrade signing or release.
