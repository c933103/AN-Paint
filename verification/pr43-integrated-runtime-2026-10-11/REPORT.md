# PR43 integrated release-runtime verification

Final bounded acceptance at 2026-10-10 23:38 UTC: all five CI jobs passed and independent host/build/device/artifact replay passed. Actual-pixel review supports the existing vertical JPEG/control reachability scope only. This accepts the exact integrated change for the stated merge gates; it is not full F01 localization or installed TIFF-dialog visual acceptance.

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

## Fresh installed-device and compiled-resource results

- API30: exact source/raw-protocol/JUnit union of 73 native plus 22 app methods; no missing, unexpected, failing or skipped executed methods. Ordinary 81.804/180 seconds; gallery 34.777/90; vertical shards 99.489/180 and 90.284/180; native 18.555/180. Complete script marker at +377 seconds.
- API35: exact union of 74 native plus 25 app methods; ordinary 125.379/180 seconds; gallery 44.011/90; vertical shards 107.191/180 and 101.535/180; seed 5.043/60; verify 6.300/60; native 23.045/180. Complete script marker at +449 seconds.
- Both APIs meet the ordinary/gallery 30-second/20-second remaining-margin targets. No timeout changes, oracle reductions or test exclusions were introduced. API30 retains its explicit existing API35-only exclusions.
- Each API has all 96 original screenshots, eight exact reachability receipts and 28 native drag traces. Bounded raw transport manifests, archive members and hashes reconstruct the host evidence byte-for-byte. Every drag has DOWN/MOVE/UP, no CANCEL, stationary scroll ancestors, correct 1/100 endpoints and clean observer removal.
- Strict log replay verifies all four Korean picker/rotation phases and exact strings/public/private identities, four real WebView large-font locale/orientation viewport rows, a distinct cold gallery process and API35's live-seed/top-resumed-gallery/external force-stop/PID-absence/normal-verify sequence. App navigation methods remain in the exact successful union.
- Independent `aapt2 dump resources` replay verifies all 695 compiled canonical/private Korean keys and values against each other, with exact XML key union, plus all 38 bounded original TIFF/C023 description values. The SDK35 verification tool bytes match the prior verified dependency artifact; tool version is aapt 2.19-11948202.

Actual pixels were inspected in all 16 labelled contact sheets, covering every one of the 192 source images, plus original-size focused checks of API35 emoji landscape description, literary-Chinese portrait maximum, and API30 Manchu portrait filename. The reviewed frames show the expected quality endpoint states, controls/description/filename reached by scrolling, and editor return states. Initial clipped labels and off-viewport content remain visible in the initial frames; reachability does not certify initially unclipped layout. These are vertical JPEG/control images, not installed TIFF-description screenshots.

## Review and remaining limits

Final-head [Codex summary](https://github.com/c933103/AN-Paint/pull/43#issuecomment-6099018290) binds `0c782ef5`: Code completed at 23:10:23Z and Security at 23:10:52Z; the Codex bot added its no-findings PR thumbs-up at 23:10:55Z. No submitted review findings or inline threads were present on the readback. Security metadata says merge-gate enforcement is disabled; a completed/no-findings review is not an enforced server gate.

Robolectric TIFF wording/state checks are not installed TIFF-dialog visual, accessibility, native-language or full-language acceptance. Original initial-state clipping questions remain separate from endpoint reachability. No localization register status changes: 475 total, 3 structural completions and 472 pending; 12 probable and four uncertain linguistic findings stay open.

## Retained evidence

`host-raw-evidence.zip` includes all 85 raw JVM XML suites, lint XML, four CI phase logs/timings, seven generator probes, exact source/inventory manifests and host receipts. `verify_ci.py` is the strict replay implementation. Build, regression and both device receipts name original artifact SHA256 values. `workflow-artifacts.json` preserves exact IDs, digests and expiry. GitHub Actions retains the full original artifacts separately; the compact packet does not include APK bytes or unrelated host screenshots. Both complete raw device transport/log packets are being added in bounded parts to the same evidence branch; the verified receipts here already report the downloaded full artifacts, not a partial run.
