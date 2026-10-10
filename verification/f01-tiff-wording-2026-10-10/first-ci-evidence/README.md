# PR43 first-head CI: retained failure and routing dependency

10 October 2026. [Run38047199955](https://github.com/c933103/AN-Paint/actions/runs/38047199955), attempt1, is **completed / failure**. Source head `d3ada3e55fb60a6926e7f6c8eede242f3c1f140e` and tested merge `a8825ce33460372fb2888f9d49830f80df38d9cd` have the same reviewed tree `bde13ca4bbd9a45198ab4da9cadd85d900aaa594`. The merge parents are develop80c and that head.

## Actual results

- Python:374 discovered,372 passed,two optional Pillow checks skipped. These are separate from the earlier374 local passes without skips.
- JVM:79 XML suites,746 unique methods,744 passed,two failures,zero errors/skips.
- All seven `TiffDescriptionDialogTest` methods pass, including English variants, pt-BR, vertical/emoji fixtures, Welsh fallback, checked/unchecked choices, toggling, format switches and cancellation.
- Both `TiffDescriptionLocaleTest` methods fail at the fixed ko-Kore-KR description oracle: expected `貯藏`/`壓縮`, actual `저장`/`압축`. Public selected-tag assertions passed. The ninth locale stops each loop; the following17 locale cases are not runtime-proved by these invocations. No expected string, assertion or locale resource is weakened.
- Full lint passes; retained lint XML contains zero issues.
- Universal APK/source and test-APK compilation pass. APK SHA256 `6fa72c774c7bd2e05963955389d801ad59478ed72e156444cfcde7c5880eb2e3`; independent review verifies build-info, all four ABIs and byte-identical embedded/extracted source. All1,291 included repository files match the reviewed tree; only the existing three metadata exclusions are absent. The6,258 extra files are confined to the four pinned native-source directories.
- Installed API35:74 native/import +18 ordinary app +one restart seed +one restart verify pass. Independent source inventories and raw protocols match all94 eligible methods without missing/duplicate/unexpected/suppressed outcomes; all17 TIFF codec methods pass. These existing device methods do not establish localized TIFF-dialog rendering or the new description oracles.

See [independent complete review](independent-ci-review.json), [terminal identities/artifact digests](terminal-source-artifacts.json), and [retained raw evidence ZIP](retained-raw-evidence.zip). The [ZIP manifest](retained-raw-manifest.json) records all108 members and hashes: all79 JVM XML suites, four API35 XML suites and their raw instrumentation/summary/coverage/boundary records, exact Python/JVM/lint phase logs/timings, lint XML and build-info. The archive was inspected before publication; credentials, private chat and signed download URLs are excluded. Mocked negative instrumentation outputs in the Python log are host-test fixtures, not actual device failures.

## Confirmed existing dependency

PR34's prior [persisted-route diagnosis](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6092984243) established the same mixed-Korean resolution defect. Its current head `5703a61394791f18e9f2597272d908d9840599af` adds `AppLanguage.resourceLocale`, mapping only resource selection to `ko-Kore-KR-anpaint` while retaining public identity. Its Gradle Sync mirrors the complete canonical mixed-script catalogue into that build-only qualifier. Both mapping and generation are absent from current develop80c/this first PR43 head. [PR34's exact prior release-configured result](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6094006470) proves its own correction, not a combined F01 result.

The failure therefore remains a genuine unmerged routing dependency. A strict test bypass is not justified. The [read-only stack proposal](../integration-proposal/README.md) and per-file compatibility assessment preserve all37 modal-only edits and four tests on the pinned dependency, without whole-file overwrites, new generated sources or copied unrelated production changes. Any future combined tree requires independent review and its own generation/JVM/lint/build/API30/API35 evidence. The historical failed run remains failed.

PR43 and PR34 remain draft/unmerged. No PR43 Codex request has yet been made; PR34's existing quota-limited request is not a clean review. Native-speaker/full-language/rendering acceptance, F01's12 probable/four uncertain cases and original term-specific history remain open. All475 register rows and3/472 states remain unchanged.
