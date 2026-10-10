# PR43 integrated release-runtime verification

Status at 2026-10-10 23:29 UTC: host, generator and APK/source checks passed; installed API30/35 work is still running. No installed or visual acceptance is claimed by this interim report.

## Exact identity

- PR: https://github.com/c933103/AN-Paint/pull/43
- CI: https://github.com/c933103/AN-Paint/actions/runs/38094001589
- Head: `0c782ef533f246ee5b6676451e09c51a00e4ae61`.
- Tree: `83f46e5d4772e98610bd6eb6fcc5a3964d19cd84`.
- Actual checkout/artifacts: synthetic merge `5b2b0a4c64ca22980f47a450f43d146045d8bc5f`, parents `2339a73f0842e4026e859742b40960bade7238bf` and current head.
- Live develop-target synthetic merge: `6b6c2345fe29f61ec5f59ded89c9f4d54333739d`, parents actual PR34 merge `6522ea6857230671847e53e25afd17095ef0f70d` and current head.

Both synthetic commits have the identical tree above. The run captured the earlier target ancestry, and is not relabelled as execution of the later synthetic SHA. The current source head already preserves the actual merged dependency as a parent.

## Independently replayed completed checks

All 202 inherited JVM/instrumentation source files remain byte- and mode-identical to the final dependency. Its original 793 JUnit identities were verified from prior raw XML. The two new F01 source files add exactly 11 non-overlapping methods, producing an expected union of 804. Fresh raw XML contains that exact union in 85 suites, with zero failures, errors or skips.

`TiffDescriptionDialogTest` contributes nine methods, including the two separate Cyrillic Mongolian C023 cases. `TiffDescriptionLocaleTest` contributes both full 26-locale loops: 52 compression-choice confirmation flows, plus 26 toggle/format-switch/cancel flows. The latter alternates cancellation routes by locale; it does not prove both routes for every locale. All method names and locale tags are retained in `host-raw-evidence.zip` / `source-inventory.json`.

Release lint has zero issues. CI Python ran 510 tests: 508 passed and two inherited optional-Pillow guards were skipped. Phase elapsed seconds: Python 136.463, JVM 404.887, native preparation 67.774, lint 90.649. Fresh execution, not inherited CI results.

All seven real Gradle resource-generator probes pass exact identity, log digest, clean/debug/release/incremental, input mutation, stale-output and canonical-byte checks. Only the documented corresponding-source bundler exclusion occurs.

The release-configured APK's embedded and delivered corresponding-source archives are byte-identical. All 1,501 included tracked source blobs match the exact tree; only `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore` are excluded. Native source entries occur only under the four declared build prefixes; their individual upstream contents are not independently re-certified here.

- APK SHA256: `638e6adc2d8e8e486033a58a4f78ad675dfec58362bc5a1eeae049fddf232c00`
- Corresponding source SHA256: `4e490e5c973ade4dac8a0106b73b5c1dc69893765770260265d60113fa61f874`
- Universal APK build: 809.348 seconds, exit 0.
- Signing: temporary CI debug key. Private upgrade signing/distribution is separate.

## Pending and limits

Both installed API jobs are running. Expected unions remain API30: 73 native plus 22 app methods; API35: 74 native plus 25 app methods. Raw protocols/JUnit, resource/navigation/viewport/process boundaries, screenshots/reachability and timing still require fresh replay.

Robolectric TIFF wording/state checks are not installed TIFF-dialog visual, accessibility, native-language or full-language acceptance. Original initial-state clipping questions remain separate from endpoint reachability. No localization register status changes: 475 total, 3 structural completions and 472 pending; 12 probable and four uncertain linguistic findings stay open.

## Retained evidence

`host-raw-evidence.zip` includes all 85 raw JVM XML suites, lint XML, four CI phase logs/timings, seven generator probes, exact source/inventory manifests and host receipts. `verify_ci.py` is the strict replay implementation. Build and regression receipts name the original artifact SHA256 values. GitHub Actions retains the full original artifacts separately; this compact packet does not pretend to include APK bytes or all unrelated host screenshots.
