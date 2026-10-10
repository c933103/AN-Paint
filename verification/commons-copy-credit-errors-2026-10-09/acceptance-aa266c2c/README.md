# PR34 standalone acceptance: aa266c2c

[Exact-head CI run 38064577479](https://github.com/c933103/AN-Paint/actions/runs/38064577479) passed all five jobs.
[Current-head Codex review](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6099261326) reports no major issues for `aa266c2cc8`.

This receipt is on a separate evidence-only branch. It does not change the reviewed PR34 source head, merge anything or publish a release. PR43 remains untouched. Later current-develop/PR18/PR41 integration requires its own composed union and exact-source validation.

## Source and build identity

- Head: `aa266c2cc8538a04724d06d3b207873c89c342d1`.
- Tested merge: `217df53066451776f8e8cb0f72e09add915c0a34`.
- Identical source tree: `3afb65999fceff0a1ce53eb20fcb9b7920ae0ca5`; all 1,391 blob paths/modes/SHAs were read back before publication.
- Parents: previous PR34 `5703a61394791f18e9f2597272d908d9840599af` and then-current accepted develop `165a6a503529736527c689e3ac1b5432253d19ee` (PR42).
- Actual `build-info.json`: **release**, run `38064577479`, matching tested merge. This is CI debug signing; private upgrade signing and release publication remain separate.
- APK SHA-256: `1d59d4fe8cc50bbfabb0fe9f3240b5ff8d740b4f8fb0cf32e72866ed549fac7e`.
- Corresponding-source ZIP SHA-256: `ea4c35d4185b43b8e6608813194add7d17ed28ede75c757480b2ec4d01f48ed5`. The APK embeds that identical ZIP. All 1,388 included tracked source blobs match the source tree; the only three excluded tracked paths are development metadata (`.gitignore`, `.idea/codeStyles/Project.xml`, `colorpicker/.gitignore`). No included tracked file differs. Four ABIs are present.
- Main APK comes from the APK/source artifact; the separate instrumentation artifact contains exactly the release app/library test APKs. Artifact digests and test-APK hashes are retained.

## Measured deadline margins

| API | Ordinary methods | Ordinary elapsed / ceiling | Gallery methods | Gallery elapsed / ceiling |
| --- | ---: | ---: | ---: | ---: |
| 30 | 15 | 79.770s / 180s | 3 | 33.308s / 90s |
| 35 | 16 | 132.727s / 180s | 3 | 46.404s / 90s |

API35 ordinary margin is **47.273s**, with **43.596s** gallery margin. API30 margins are **100.230s / 56.692s**. Both platforms satisfy the predeclared review targets of ordinary ≤150s and gallery ≤70s. Summary elapsed includes wrapper setup/install/discovery, making this comparison to the instrumentation ceiling conservative.

API35 seed and verify also passed, in **5.760s / 60s** and **7.144s / 60s**. The full emulator script reached successful completion at **171s (API30)** and **271s (API35)**, before bounded cleanup, within the unchanged 900-second execution step.

This is margin established by an explicit partition, not a claimed aggregate speedup or a controlled performance benchmark. The two API35 ordinary/gallery wrapper durations total 179.131s, versus the historical single ordinary wrapper's 178.579s. Extra aggregate budget is explicit: ordinary coverage 180→270s; total app API30 180→270s / API35 300→390s. Existing native/ordinary 180s, seed/verify 60s, outer step 15min/job 25min ceilings are unchanged. No retry or test omission was used.

## Coverage and raw-evidence checks

- Native: **73 API30 / 74 API35**, exact source methods, no missing/unexpected/failed/skipped cases.
- API30 app: **15 ordinary + 3 gallery = 18**. Its one SDK-ineligible language-picker case and two explicit API35 restart omissions are separately recorded, never counted as passes.
- API35 app: **16 ordinary + 3 gallery + 1 seed + 1 verify = 21**, an exact disjoint union of every declared eligible method. Native + app totals are 91 and 95 respectively.
- All instrumentation logs were independently reparsed against the checked-out SDK-aware inventories. Coverage receipts were independently recomputed using the exact test-source digest `6f34350fead673b45e55438011631217c4e0b75202b988b32c348bd9c6614f3c`. Completed cases, selectors, original deadlines, source hashes and device SDKs match.
- Each platform retains four exact Korean picker/rotation phases. Fixed `複寫`/`貯藏` mixed-script and ordinary Korean strings, unchanged public preference/Java/platform identity, internal resource variant and actual orientation/dimension change all match.
- Each platform retains four real French/Mongolian gallery viewport records (two orientations each) at font scale 2, satisfying the unchanged required viewport reserve. Original font synchronization records are retained as well.
- TestRunner logs prove gallery methods executed in a process distinct from ordinary editor methods on both platforms. All three unchanged real gallery draft flows passed their own setup/cleanup.
- API35 seed report and boundary log prove original live PID 5586, resumed Gallery, a successful externally issued force-stop, positive PID absence and successful fresh-process verification. No restart coverage was substituted with ordinary recreation.
- JVM: **775/775**, zero failures/errors/skips. CI Python: **418 passed + 2 skips / 420**; local host run: **420/420 with no skips**. Full release lint and app/test-APK compilation passed.
- Both 59-row Copy-credit tables, both 28-row routing tables and both 140-locale navigation reports are complete and exact. All seven independent pinned-Gradle resource-generation probes passed, and each retained generator-log hash matches its summary.

## Durable evidence

`acceptance.json` is the machine-readable outcome. `verified-evidence.zip` contains 90 hashed retained evidence files plus their manifest: source-tree manifest, build identity, original artifact digests, all native/app instrumentation summaries/protocols/JUnit reports, exact app union receipts, startup/boundary logs, targeted original logcat records and parsed Korean/viewport/process records, generator reports/logs, host phase logs, all 775 JVM identities/outcomes, and resource/navigation tables. It excludes APK binaries and unrelated full-device logcat.

Archive SHA-256: `a02b8b4ad77ca6193ea6fdc4b447fa98b186b723f2df1bfca57fc11d43bba93a` (1,670,775 bytes). The original GitHub artifact digests were verified before extraction. A credential-pattern scan found no matches in retained files; this synthetic test evidence contains no private signing key or user account data.

## Remaining integration boundary

This accepts the standalone PR34 timing repair on the source above. Develop advanced afterward through PR37; this receipt does not accept that later combined source. Keep PR34 draft until the parent coordinates the stack.

The future composed verifier must cover ordinary + gallery-draft + both PR41 vertical shards + seed/verify. Neither existing partition checker can replace the other. Distinct receipt names alone are insufficient. Their combined native/app inner ceilings total 930s, exceeding the unchanged 900s outer step before setup; simultaneous exhaustion is not promised. Combined runtime, complete unions and every retained oracle must be measured and reviewed after integration. PR43 remains dependent and unchanged.
