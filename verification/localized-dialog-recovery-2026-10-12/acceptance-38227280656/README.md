# PR52 exact-head current-develop acceptance

**Bounded technical acceptance: passed.** This report concerns head `71f4d288669858e7975ec4c094b7f47a9a1ff145`, tree `815e265af5387111dcdaef66efac5d2091bbb56d`, with ordered parents accepted PR52 `2755e30573d6ea2c071a128b6fa2940fc675af1a` and develop `4231edaac45d89c52f51e2b77d0f94a1176ad88c`. It is not a ready/merge, security-review or release decision.

- [Exact-head CI 38227280656, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38227280656): all four jobs passed. GitHub's tested merge `f008d110f83cb6390db941b9177062edb8ea212c` has exactly the published tree.
- [Exact-head Codex Code review](https://github.com/c933103/AN-Paint/pull/52#issuecomment-6121172937): no major issue found, reviewed `71f4d28866`.
- [Original source-composition and local evidence](https://github.com/c933103/AN-Paint/tree/71f4d288669858e7975ec4c094b7f47a9a1ff145/verification/localized-dialog-develop-integration-2026-10-12): develop baseline 568; final frozen local 636, zero failures/skips. Earlier failed historical-oracle runs are retained. Independent source review passed 105 ordinary/89 optimized tests plus strict reversal/mutation checks.
- [Recovery checkpoint](../publication-complete.json): all 1,805 remote leaves matched; all 1,776 reviewed files recovered with exact SHA256; the final tree adds only 29 verification files to reviewed tree `cad5e3ba`. The single missing diff was reconstructed from verified Git objects and matched its original Git SHA, SHA256 and length before publication.

## Fresh hosted results

- Python: 636 discovered, 634 passed, two optional independent Pillow decoder checks skipped. Their identities and original progress-to-discovery mapping are recorded. The original local 636-test run had zero skips; the hosted skips are not counted as passes.
- JVM: the exact 869-identity union, 92 original JUnit files, zero errors/failures/skips; lint has zero issues. The already-merged M03 test rename remains explicit in the source-bound expected inventory.
- Model evidence: 602 original reports/images, including 288 PNGs, are byte-identical to accepted PR52 for dialog/M02/C05 and current develop for M03. The only naming adjustment is a bijection over 34 C05 About/notice filenames, using three resource IDs shifted by one when M03 adds a string. Both APK resource tables name the same three strings, and all contents remain byte-identical. APK resource type `0x0d` and library/Robolectric type `0x0c` are explicitly distinguished. No content normalization or broad filename waiver was used.
- Installed API35: exactly 104 successful identities, 74 native and 30 app. The app partition is 16 ordinary + 3 gallery-draft + 5 dialogs + 4 vertical + 1 restart seed + 1 restart verify. Each original raw protocol and JUnit report was revalidated against exact source digests and selectors. All four coverage receipts equal the computed complete disjoint union.
- Restart: original live PID 6849 was checked three times; Gallery was resumed; external force-stop succeeded; explicit absence preceded normal fresh-process verification. Both original methods passed. This is not inferred merely from two green phase summaries.
- Dialogs: all five source-bound exports and ten PNGs verified; seven exact single native-Back injections. Phase duration 93.876s of 300s. Longest interaction 22.634s of 45s. Setup/interaction/teardown remain separately timed. All ten fresh PNGs were visually inspected; caption line geometry/native pointer/Back evidence passed unchanged strict transport validation.
- Vertical evidence: all four export manifests, 104 extracted files, eight reachability cases and 64 reachability screenshots passed the original verifiers. Independent visual review covers all 64 reachability PNGs. Fresh replays equal all three original hosted transport/reachability receipts byte-for-JSON-value.
- Korean routing: four original logcat records show mixed Korean, actual rotation, ordinary Korean, mixed Korean again; public/persisted tags remain public while only the mixed-script resource configuration has the internal variant.

## APK and resource identity

The artifact ZIP digest, APK digest and source digest match GitHub metadata/build-info. The APK-embedded source equals the sidecar ZIP. All 1,802 source-archive-included tracked files match the 1,805-leaf publication; only `.gitignore`, `colorpicker/.gitignore` and `.idea/codeStyles/Project.xml` are documented build-archive metadata exclusions. All 14 font assets match develop. APK strings match both metadata entries in all 60 catalogues, all 19 Hungarian scoped values, and all 696 mixed-Korean/generated-variant string or reference pairs. Seven clean/incremental resource-generation probes and their original log hashes pass.

The APK verifies with its CI debug signature and 16-KiB alignment. It is not upgrade-signed with the user's private key. No release or installable upgrade delivery is claimed.

## Independent post-CI review

[Independent artifact/helper and 64-image review](independent-artifact-review/REVIEW.md) found no remaining blocker in its bounded scope. Its checksums preserve the exact negative controls, final helpers and original-pixel contact sheets.

## Evidence and limitations

`hosted-provenance.json` records artifact IDs, digests, expiry dates and job steps. Full build/test ZIPs remain the original GitHub artifacts; this checkpoint retains selected original raw reports, all 74 scoped installed PNGs, their original receipts, generation logs, exact source binding and verification results. No full raw archive producer is resumed. `raw-jvm-results.json` preserves each original XML string, path and digest; `scoped-model-files.json` lists all 602 original model hashes. `SHA256SUMS.json` binds the retained files.

The standalone replay helpers are supporting evidence scripts, not application changes. Independent negative controls found and fixed fail-open report handling: optimized Python now rejects, duplicate ZIP members reject, lint/JUnit schemas/counters are strict, elapsed time must be finite/nonnegative, and stale success receipts are removed before validation. Actual artifacts were replayed after the fixes. Visual differences require a separate disposition; the actual scoped model comparison has none after the explicit resource-ID bijection.

Scrollable initial screenshots intentionally do not show every title/body/control simultaneously. Reachability is established through original successive native input and geometry, not a claim of all-content-at-once fit. The inherited advanced-colour short-landscape limitation remains characterized, not fixed or positively accepted. No PR51 or stopped PR53 work is incorporated. No fresh API30/21/24 installed run, physical device, TalkBack, competent-speaker, all-language or release acceptance is inferred. Root retains the ready/security/merge and producer-supersession decisions.
