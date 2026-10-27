# Kannada, Malayalam-India and Filipino: exact-head hosted verification

[Application PR191](https://github.com/c933103/AN-Paint/pull/191) head `d2a33572b7b19505c2442fd58b12d54629220048`, tree `d5cbf99fad6357b6424307878f32d94e1742d813`, carries the reviewed PR190 parent `0bbecc9eed1feeccdec6170af44076b408509b3a` without new credit for that earlier unit. This unit contains **655 typed edits**. Complete independent value/fixture reviews and source accounting remain immutable at [a999b821](https://github.com/c933103/AN-Paint/blob/a999b821af5d4ea081b1ca7e5caa9e947914f0c1/records/localization-review/2026-10-27/kn-ml-fil-priority/README.md).

## Terminal results

Natural [run 40508177249](https://github.com/c933103/AN-Paint/actions/runs/40508177249) completed successfully: all six jobs passed, with no source repair or manual rerun. The [exact-head Codex review](https://github.com/c933103/AN-Paint/pull/191#issuecomment-6442738640) completed without findings.

- Both local host aggregates: **1,515 passed**, ordinary and optimized.
- Hosted Python: **1,515 discovered; 1,513 passed and two optional Pillow-dependent skips**. Expected negative-fixture diagnostics after unittest `OK` are not an aggregate failure.
- Original JUnit artifacts: **1,450 tests in 158 suites, zero failures/errors/skips**, including all twelve new actual-consumer methods.
- Android lint: **zero issues**. Exact-script resource generation passed; every original probe-log checksum and expected positive/negative outcome was independently checked.
- API35: **47 app and 74 native methods** match exact current source inventories and pass. Mandatory dialog/vertical/logcat/result collection all returned zero. Original same-run core and position artifacts were re-composed locally; dialog export, vertical export, screenshot matrix and reachability validators all passed.

## APK and corresponding source

Original artifact 12735284583 SHA-256: `487318176359ffd3aeab19ce915de38464833d3827dc19824ad49207dfe05890`.

- APK SHA-256: `171260c37f783222cf74309651acc276c481c065b7c0ed24bd6b28f288b9c2a7`.
- Corresponding source ZIP SHA-256: `1cb387956a5d03848239d8a487e4d43b691a6e4908e7e81cdb563732173a11f6`.
- APK signature verified; embedded and separately delivered source match.
- All **1,413 included repository blobs** match the reviewed tree. Only `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore` are omitted repository metadata.
- Build synthetic commit `19877339b951b247567046bf5c188601f90d09ba` has the same application tree and ordered parents `1126b650216478c422997dcd1236ca6cc780e4e3`, `d2a33572b7b19505c2442fd58b12d54629220048`.

The [archive binding](archive-binding.json) identifies the compact, checksummed [terminal evidence archive](terminal-hosted-evidence.tar.xz), containing selected original JUnit/lint/phase/device reports, exact Codex receipt and independent verification records. Original archive digests remain recorded; sanitized local machine paths do not replace original downloads.

This is a CI-debug development build, not a privately upgrade-signed delivery or release. No native-speaker, whole-device, every-locale layout or all-recovery-scenarios acceptance is claimed. Fixed present/absent and wording-only holds remain unchanged. No merge is claimed by this record.
