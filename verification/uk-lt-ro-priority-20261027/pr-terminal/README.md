# Ukrainian, Lithuanian and Romanian — PR186 terminal evidence

[PR186](https://github.com/c933103/AN-Paint/pull/186), exact reviewed head `728ddd062b4fef9e9440978959d85c199da6dccc`, tree `0ad3a1d8e0fb752571027415d268ac65ab301dd9`. Synthetic PR checkout `7a37c90584769153465d2cb013105cb4cb37eff6` has the identical tree and expected base/head parents.

[Run 40465665783](https://github.com/c933103/AN-Paint/actions/runs/40465665783) completed successfully in all six canonical jobs. Required exact-head Codex review completed with no findings, and the earlier expectation finding is resolved. Optional security metadata is not substituted for required code review or turned into a new gate.

- Local complete host: **1,469 / 1,469 ordinary and optimized**, zero failures.
- Hosted JVM: **1,410 tests across 153 suites**, zero failures/errors/skips; **all eight new actual-consumer methods pass**, as do the repaired legacy cases. Lint: no issues.
- Exact-script: all **13 expected probe outcomes** and raw log hashes verified against the reviewed tree.
- API35: complete source-bound app union **47/47** and native inventory **74/74** pass. Core/position identities agree with independently downloaded main APK, corresponding source and app test APK bytes at attempt 1; native test APK digest is also retained.
- Four native ABIs are present. Embedded and separately delivered corresponding-source ZIPs agree byte-for-byte. All **1,393 packaged tracked source files** match reviewed Git blobs. The only three observed metadata omissions are `.gitignore`, `colorpicker/.gitignore`, and the explicitly excluded `.idea/codeStyles/Project.xml`; there are no differing or unexpectedly missing code, resources or tests. A preliminary whole-Git-inclusion check rejected these metadata omissions and is retained as an assumption correction, not a CI failure.

The full **341 P0/P1 identities per language** and **439 exact resource edits** remain [bound to complete review ledgers and prior-receipt lineage](https://github.com/c933103/AN-Paint/blob/0e4132cc68648a7e038320285a632469f2cf3a5e/verification/uk-lt-ro-priority-20261027/local/README.md). UK/RO each retain five exact no-consumer P0 absences and the one unknown-composition P1 palette hold; 14 new dormant labels per language are wording-only, not active-UI acceptance. Lithuanian's atomic corrections and crop dependencies are applied; historical wording-only limits remain. Polish is historical rebind only.

All 171 rows were recomputed on this exact source: P0 **7,376 present / 8,356 missing**; P1 **20,330 present / 22,249 missing**. Before/after deltas remain +68 P0 and +308 P1, with the other 168 catalogue rows unchanged. Presence is not linguistic certification.

[The initial failed run and three precisely reviewed test-only corrections](https://github.com/c933103/AN-Paint/blob/dca0a8e6d7a93871b952926fd9386ef2b870d8a7/verification/uk-lt-ro-priority-20261027/jvm-repair/README.md) remain recorded as failed history, not relabelled passes. Neither application logic nor reviewed resource values changed in those corrections.

`terminal-evidence.zip` retains original selected JUnit/phase/protocol/summary bytes, artifact digests, exact source/APK identity receipts, complete current structural rows, and a member SHA256 manifest. Generated HTML, screenshots and unrelated device logs are excluded. These bounded checks do not certify target-locale installed layouts, native-speaker fluency, whole-language correctness, physical devices or TalkBack. The APK is CI debug-signed, not private upgrade-key signed. Actual develop merge and its push run require separate verification. **No release.**
