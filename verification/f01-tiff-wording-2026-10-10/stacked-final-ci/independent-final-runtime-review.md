# Independent final review: F01 TIFF wording stack

**PASS within the bounded source, test and runtime scope. No blocking finding remains. F01 and broader language acceptance stay open.**

## Exact source and run

- PR43 head: `4f9082aa687a5c36b559061bcc10d0e39331610f`.
- Reviewed and tested tree: `04a84df1535297f13a314c521b55647f6d15a678`.
- Tested merge: `73fff41dee17c49a972825c90bdcd88e38287911`, on pinned PR34 `5703a613…`.
- [Run 38049772357](https://github.com/c933103/AN-Paint/actions/runs/38049772357), attempt 2: **all five logical jobs successful**.

Attempt 1 genuinely hit the unchanged 22-minute release-build deadline. The one authorized failure-only retry built in 15m05s and passed both device jobs without source, oracle or deadline changes. JVM/lint/host and generator successes were carried forward from attempt 1; they were not executed twice. The cause of the initial build slowness remains unknown.

## Verified coverage

- Local independent host: **412 passed, no skips**. The repaired scope guard passed 212 negative controls; three separate Copy-credit value corruptions were also rejected. Earlier 41 unchanged resource negative controls remain preserved.
- CI host: 410 passed and two optional Pillow checks skipped.
- **775 unique JVM methods across 82 suites passed**, zero failures/errors/skips. All nine TIFF methods compiled and passed. Both 26-locale loops complete with unchanged strict Hanja expectations, plus the original English/pt-BR/vertical/emoji/default-fallback checks and compression, format-switch and cancellation behavior.
- Release lint: zero issues.
- Seven real Gradle clean/incremental/stale-output/resource-order probes passed.
- Independent AAPT2 execution confirmed the exact **695-key** canonical/private Korean set and equal compiled values, including the qualified Hanja TIFF description.
- APK embedded/extracted source ZIPs are identical. All **1,386 included reviewed files** match exactly; only three repository metadata files are omitted. Extra bundled native source is confined to the four expected source directories. All four APK ABIs are present.
- API30: **73 native/import + 18 app methods passed**, with only source-declared SDK and API35-only exclusions.
- API35: **74 native/import + 21 app methods passed** across 19 ordinary, one seed and one verify phase. All six raw device protocol logs were independently reparsed against exact eligible source inventories. The live seed PID, resumed Gallery, external force-stop and verified absence precede successful fresh-process verification.
- Both Android versions passed all four real Korean picker phases, live orientation/dimension changes and public persisted/default identities; API35 also preserved the public platform identity.

## Limits retained

API35 ordinary tests took 172.05 of 180 seconds, leaving about 7.95 seconds of margin. Timing variability remains a risk; no timeout waiver was used. Device artifact identity follows the reviewed workflow’s exact-merge artifact downloads and installation; device logs do not independently hash the installed APK.

Real Korean device routing checks assert Save and Copy-credit resources. They are not TIFF dialog screenshots. TIFF wording/state behavior is established by Robolectric and compiled parity, while native-device visual/accessibility review and native-speaker acceptance remain separate. Welsh fallback does not prove all 81 missing-definition locales.

Twelve probable and four uncertain F01 entries remain open; parent counts remain 475/3/472. The CI release APK uses a debug signing key, so private upgrade signing and distribution remain separate. The PR is still stacked on PR34.

The original Korean CI failure, checkbox API-contract correction, first-stack historical scope-guard failure and initial build timeout remain preserved. See `stacked-final-runtime-review.json` for artifact digests, precise identities and linked independent evidence.
