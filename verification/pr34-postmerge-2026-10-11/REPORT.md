# PR34 postmerge verification: debug / API35

Verified 10 October 2026, 23:31 UTC (11 October, 07:31 UTC+08).

## Result and exact identity

[Postmerge run 38093916668, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38093916668) completed successfully at 23:27:44 UTC. It is the `push` run on `develop`, with all four jobs successful: Regression tests and lint (114335766183), Build APK and corresponding source (114335766324), Exact-script resource generation (114335766376), and Emulator API35 (114337453372). GitHub status, job and artifact records are retained in [remote-record.json](remote-record.json).

- Actual [PR34 merge](https://github.com/c933103/AN-Paint/commit/6522ea6857230671847e53e25afd17095ef0f70d): `6522ea6857230671847e53e25afd17095ef0f70d`
- Exact source tree: `ad6cbc4458cc60ec3f0cb3273f6aaed4733bba70`
- Parents: prior develop `a758daceda1d4fc37c605e50715f892557da9fc8` and accepted PR head `2339a73f0842e4026e859742b40960bade7238bf`
- Build variant: **debug**, signed with the CI debug key
- APK SHA-256: `fbc5787f3f7cf13cf2aa222dc064011608c345b1934c97942083b241f0bffb17`
- Matching corresponding-source ZIP SHA-256: `9ea015e02cf62a71a04d96190f4725144354f55bf32d20c0c3909a10d32f0d5a`

This evidence commit adds only this verification directory on a separate evidence branch. It does not move or modify a source branch, signing material, release configuration or the localization acceptance register.

## Independent verification

All four supplied strict receipts were independently replayed against the original downloaded archives/extracted evidence and a source snapshot matching every one of the 1,488 path/blob identities in [manifest.json](manifest.json). Reconstructing the Git tree from that manifest gives the exact remote tree above; the source index has that tree and its worktree is clean relative to the index. The checker results matched the original receipt JSON exactly. [Independent replay results](independent-replay.json) and [checker](verify_ci.py) are retained.

### Build, regression and generator

- APK-embedded corresponding source equals the separately delivered source byte-for-byte. All **1,485 included repository source blobs** match the source manifest. The only three tracked omissions are `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore`.
- The source bundle additionally contains declared native-source prefixes: jxl 1,583 entries, webp 338, heif 2,663 and tiff 1,674. Their individual upstream blobs are not re-certified by this check.
- **793 JVM tests in 83 suites**, with zero failures, errors or skips. Exact testcase identities equal [the accepted-parent union](expected-jvm-union.json), rather than relying on a count alone. Focused integration suites retain 12 numeric-slider, 9 import-selection-title and 6 vertical-redraw cases.
- **Lint: zero issues.** All 83 raw JVM XML suites and the lint XML are retained alongside CI phase logs.
- Python CI: **489 discovered, 487 passed and 2 skipped**, exit 0, 101.740 seconds measured. This is not the earlier local no-skip result. The log's deliberately unsuccessful synthetic instrumentation receipts are negative test fixtures, not failed installed-device phases.
- **Seven real generator probes** passed: clean; clean debug/release merges; unchanged up-to-date run; input mutation plus stale-output removal; restored-input release; second clean; and release-first after clean. Exact source identity, wrapper/root-build hashes, each log hash and generated canonical bytes were checked. Its sole excluded task remains `:Paintroid:bundleCorrespondingSource`; the ordinary build independently verifies APK/source delivery.
- Universal debug APK assembly took **364.982 seconds**, exit 0. The retained diagnostic reports 3,246 / 3,762 cacheable hits (86.28%) and 516 misses. This observed warm-cache duration is not a cold-build guarantee and does not retrospectively validate earlier timed-out runs.

See [build receipt](build-receipt.json), [regression receipt](regression-receipt.json), [generator receipt](generator-receipt.json), and the raw `generator/`, `regression/` and `build-diagnostics/` evidence.

### API35 installed runtime

The fresh API35 artifact passes the strict exact-source/raw-instrumentation/JUnit union check: **74 native + 25 app methods = 99 installed methods**. No app methods are suppressed, excluded, missing, duplicated or substituted.

| Phase | Methods | Measured seconds | Unchanged limit |
| --- | ---: | ---: | ---: |
| Ordinary app | 16 | 128.013 | 180 |
| Gallery draft | 3 | 47.125 | 90 |
| Vertical English / Manchu | 2 | 121.616 | 180 |
| Literary Chinese / vertical emoji | 2 | 114.813 | 180 |
| Accepted-credit seed | 1 | 6.528 | 60 |
| Accepted-credit verify | 1 | 8.551 | 60 |
| Native | 74 | 85.968 | 180 |

Ordinary/gallery retain 51.987 / 42.875 seconds of margin, exceeding the original 30 / 20-second margin targets. The startup log records successful instrumentation completion at 564 seconds, inside the configured 36-minute outer execution ceiling. These are observed timings, not guarantees that every inner maximum can be exhausted simultaneously.

The complete app coverage receipts agree. The accepted-credit restart boundary proves a live gallery-resumed seed process, external force-stop, verified absence of its PID, then separate verification instrumentation. Gallery-draft tests use a process distinct from ordinary app tests. Four exact mixed/ordinary Korean routing and rotation log rows pass, along with French/Mongolian font-scale-2.0 portrait/landscape WebView viewport reserves.

Own-MediaStore export reconstruction verifies the exact 104-file, 7,124,035-byte synthetic evidence inventory against the collected files. The strict image/input checks cover **96 fully decoded PNGs** (32 original states + 64 reachability states), **8 locale/orientation reachability receipts**, and **28 native drags**. All original states have distinct decoded pixels; minimum/maximum endpoint pixels differ. Drag traces prove DOWN/MOVE/UP without CANCEL, correct 1/100 endpoints, stationary scroll ancestors, no dropped observations and clean observer removal.

Full structured results, image and receipt hashes, phase counts, exact method names and extracted log oracles are in [device35-receipt.json](device35-receipt.json). Selected original raw instrumentation/JUnit/summary, boundary, coverage and export metadata files are retained under `device35/`. The logcat extract identifies its original full-file hash and line numbers.

## Scope and retained limits

This run freshly establishes **postmerge debug/API35** checks. It contains no API30 job and does not establish a fresh release-variant run. The separately accepted premerge release/API30+35 evidence remains at [c8852764 / final acceptance](https://github.com/c933103/AN-Paint/blob/c88527645d8d76475797b4514ada70aed09d1cc7/verification/pr34-final-acceptance-2026-10-11/REPORT.md), including its exact source relationships and limits.

Image decoding, hash checking and structured state/input receipts are **not fresh actual-pixel visual review**. No new visual or linguistic acceptance is claimed for these postmerge PNGs. Earlier bounded visual inspection remains at [449e3e82](https://github.com/c933103/AN-Paint/blob/449e3e8241d17e343e0c3b8d08474a4eae83c47e/verification/pr34-cold-build-runtime-2026-10-11/REPORT.md). Initial dialog clipping, full-fit, native-language, accessibility and broader image-format dialog coverage remain open. No language-register item is promoted; earlier failed and incomplete runs retain their original scope. PR43 integration and private upgrade-signed delivery remain separate.

## Artifact retention and reproduction

The repository preserves this report, checker, exact source/JVM manifests, strict receipts, selected original small text logs/XML/JSON, GitHub metadata and publication hashes. **It does not permanently archive the original ZIPs, APKs, screenshots, full logcat or detailed raw drag JSON.** Those binary/full raw inputs remain in the 14-day GitHub Actions artifacts and temporary local copies; hashes alone do not preserve their bytes. Full strict reproduction requires the original artifact inputs before expiry or another retained identical copy.

| Artifact | GitHub ID | ZIP SHA-256 | Expires UTC |
| --- | ---: | --- | --- |
| APK and source | 11685910727 | `bcc64eb37df8e43003c659f425d3ec995f11accd1ae9a2ea03c01ec15a835ca8` | 2026-10-24 23:15:06 |
| Regression and lint | 11684848075 | `e2250a5017a7111e76808d5482923dcdc2db94a208f76e493467d8993d761758` | 2026-10-24 23:16:48 |
| Exact-script generation | 11685360985 | `ac4142e2e34f0d068b54fa2a036e6d6b8f33a5fd26d6a8dbb79f80b661bdaf12` | 2026-10-24 23:09:35 |
| Emulator API35 | 11685662441 | `5b70878eba808eb29aabcc1a9a91b82fa88388b3a0c31f808950923a0ae895d4` | 2026-10-24 23:27:38 |
| Build diagnostics | 11685167290 | `9679d48443ee11a8ee4ce78373443d72f9f889e33d53673db51a5910cf194fc8` | 2026-10-24 23:15:05 |
| Instrumentation APKs | 11685496455 | `11ee8511a5dafc0f6afc7048a0e24af91b5bca0eb5519486641e95de3850c6e8` | 2026-10-24 23:16:49 |

The first five listed ZIP hashes match locally held bytes and GitHub artifact digests. The instrumentation-APK hash is GitHub metadata only; that separate ZIP was not independently downloaded/hashed in this evidence pass.

To reproduce, check out the exact merged source and keep `verify_ci.py` beside `expected-jvm-union.json`. Download the named archives from the run, verify their hashes, and invoke the checker with `--source <exact-source> --manifest manifest.json --directory <fresh-output>` for `build`, `regression`, `generator`, and `device` (the last with `--sdk 35`). Python 3 and Pillow are required for the device image decode. Do not substitute another source head or artifact run. [publication-manifest.json](publication-manifest.json) records the preserved text files and their exact Git-blob/SHA-256 identities.
