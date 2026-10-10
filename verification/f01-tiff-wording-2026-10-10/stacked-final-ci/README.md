# F01 exact-stack final CI evidence

**The bounded candidate passes the requested source/build/runtime checks. PR43 stays draft: its PR34 dependency is unmerged, and the single final-head Codex request received a usage-limit response rather than a review. F01 and parent localization obligations remain pending.**

## Exact identities and outcome

- [PR43](https://github.com/c933103/AN-Paint/pull/43) head: `4f9082aa687a5c36b559061bcc10d0e39331610f`.
- Reviewed/tested tree: `04a84df1535297f13a314c521b55647f6d15a678`.
- Tested merge: `73fff41dee17c49a972825c90bdcd88e38287911`.
- Pinned base: unmerged PR34 head `5703a61394791f18e9f2597272d908d9840599af`, tree `f2333d9ee7aa6e55c584b306e7363bde83dbbf43`.
- [Run 38049772357, attempt2](https://github.com/c933103/AN-Paint/actions/runs/38049772357/attempts/2): all five logical jobs successful.

Attempt1's release-APK step hit its unchanged 22-minute deadline. Its [failure, public annotation and raw passing evidence remain preserved](../stacked-attempt-1/README.md). One failure-only retry built the identical source in 15m05s and passed both device jobs. JVM/lint/host and generator results were carried forward from attempt1 with their original timestamps; they were not executed twice. The earlier build's slow underlying cause remains unknown. No source, test oracle, workflow, deadline or permission changed for the retry.

## Executed evidence

- Independent local host: 412 passed without skips. Narrow scope composition has 212 embedded negative cases and three independently rejected Copy-credit value mutations; the earlier 41 resource negatives remain preserved.
- CI host: 410 passed, two optional Pillow ICO/Adam7 checks skipped.
- JVM: 775 unique methods across 82 XML suites, no failures/errors/skips. All nine TIFF methods pass, including both complete 26-locale loops and the original English/pt-BR/vertical/emoji/Welsh-fallback cases, both compression choices, toggle, format switching and cancellation. These are SDK33 Robolectric results.
- Release lint: zero issues. Seven actual Gradle clean/incremental/stale-output/order probes pass.
- Independent APK AAPT2 read:all 695 canonical/private Korean keys and compiled values match; the exact qualified Hanja TIFF value is retained. Generated/canonical XML SHA-256:`9d928efffd75d06b3a8b6016518c6869b407e95a3b6125b69c13a9482f2d6176`.
- APK SHA-256:`5fc2324db6448c1e58932986c1259aac364536d3838d861c501cd411c3b468ad`. Embedded and separately extracted source ZIP SHA-256:`2852a6a6c00974ee3ac9db040e352ab2a288a9ce2f37ed7a234d4ba31dd5ee25`. All 1,386 included reviewed files match; only three repository metadata files are omitted, and 6,258 additional native-source files stay within four pinned dependency directories. All four ABIs are present.
- API30: 73 native/import plus 18 app methods pass, with only source-declared SDK/API35-only exclusions.
- API35: 74 native/import plus 19 ordinary app, one seed and one verify method pass. The abrupt-process-stop boundary retains the live seed PID, resumed Gallery, external force-stop, verified absence and successful fresh-process recovery.
- Both APIs pass all four real Korean picker/rotation phases and public persisted/default identity; API35 also preserves public platform identity. All six raw device protocols were independently reconciled against exact eligible source inventories.

API35 ordinary app execution took 172.0475 of 180 seconds, leaving about 7.95 seconds. This timing margin remains a risk. Device-installed APK identity follows the reviewed exact-merge artifact download/install workflow; device logs do not independently hash the installed APK.

## Review gate and remaining limits

The [single final-head Codex request 6097631408](https://github.com/c933103/AN-Paint/pull/43#issuecomment-6097631408) received [usage-limit response 6097632279](https://github.com/c933103/AN-Paint/pull/43#issuecomment-6097632279). This is not a clean review. No second request, account change or merge followed.

Real Korean device checks assert Save/Copy-credit resources, not installed TIFF dialog screenshots. TIFF wording and state/callback behavior are covered by Robolectric and compiled parity; native-device visual/accessibility and native-speaker requirements remain separate. Welsh fallback does not prove all 81 missing-key locales. Twelve probable and four uncertain F01 cases remain open; seven already-qualified and 81 missing-key cases remain unchanged. Original scope is partially recovered; term-specific history remains unresolved. Parent register states remain **475 total / 3 structural completed / 472 pending**. The CI release APK uses a debug signing key; private upgrade signing/distribution is separate.

The checkbox API-contract correction, original two-method Korean CI failure, first-stack historical scope-guard failure and initial build timeout all remain in the durable history. No failure is erased by the later pass.

## Packet contents and verification

- `final-ci-receipt.json`:exact terminal run/jobs/source/artifact identities, attempt boundaries and limits.
- `codex-review-receipt.json`:exact request and quota response.
- `independent-final-runtime-review.md` and `.json`:bounded independent disposition and detailed evidence references.
- `final-runtime-raw-evidence-scoped.zip`:all six device XML/raw protocol/summary/boundary records; relevant project logcat lines with original line numbers and complete-log digests; all 695 raw paired Korean AAPT2 headers/values; full configuration dump, parity audit/result and build identity; every independent report referenced by the final review.
- `final-runtime-evidence-manifest.json`:all 58 ZIP members and SHA-256 values. Full JVM/generator raw data remains in the prior 115-member attempt1 packet.

Original complete Actions artifact IDs/digests are retained; those service downloads expire on 2026-10-24. The durable scoped packet omits unrelated OS logcat/configurations while preserving the complete evidence for the claims above. Files were inspected before upload for credentials, secrets, signed download URLs and unrelated private data. Repository visibility is unchanged. Remote bytes/tree must be verified before the publication is reported complete.
