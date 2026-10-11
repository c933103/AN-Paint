# PR43 postmerge release verification

Final bounded acceptance at 2026-10-11 00:20 UTC: all five fresh postmerge jobs are green; exact source/build, compiled resources, JVM/lint/generation and both complete installed-device evidence sets independently pass. Actual-pixel checks pass only the stated JPEG/control reachability scope. Premerge acceptance is retained separately at [25186e0a](https://github.com/c933103/AN-Paint/blob/25186e0ad91d4d8c000444f5090b06fa122b8763/verification/pr43-integrated-runtime-2026-10-11/REPORT.md).

This is fresh push run [38095872353](https://github.com/c933103/AN-Paint/actions/runs/38095872353), actual merged develop commit `2c1bd8622eb6c57444eee8f816194b309fff136e`, exact accepted tree `83f46e5d4772e98610bd6eb6fcc5a3964d19cd84`. No source change or evidence from the earlier synthetic checkout is relabelled as this new run.

- Fresh release JVM: exact 804-method union in 85 suites, no failures/errors/skips. This includes every prior 793 method and all 11 F01 additions, both 26-locale loops and both C023 cases.
- Release lint: zero issues. CI Python: 510 total, 508 passed and two inherited optional-Pillow skips.
- Phase seconds: Python159.307, JVM443.832, native preparation329.955/360, lint107.950. Native preparation was slower than premerge and retained only30.045 seconds of its configured phase budget; no new bound or benchmark guarantee is claimed.
- All seven fresh exact-script generation probes pass source identity, hashes and clean/incremental/mutation/stale-output/release-first checks.
- Universal release APK build:1426.887 seconds (23m47s), exit0, under its30-minute cap. The long build is not silently reclassified as a warm-cache result.
- Build identity names merged commit2c1bd862 and run38095872353. APK SHA256 `dafcbea9e33732d6bdccbefb826a287846f13e24d0b5523ce33a40bfe59a80e0`,119,912,892 bytes.
- Embedded/delivered source ZIPs are identical: SHA256 `4e490e5c973ade4dac8a0106b73b5c1dc69893765770260265d60113fa61f874`,55,637,886 bytes. This source ZIP is also byte-identical to the accepted premerge source ZIP.
- All1,501 included tracked source blobs match the intended tree. Exact three exclusions: `.gitignore`, `.idea/codeStyles/Project.xml`, `colorpicker/.gitignore`. Only the four declared native-source prefixes are additional; their individual upstream bytes are not independently re-certified.
- The SDK35 aapt2 verification tools match the prior accepted tool bytes. Fresh compiled-resource replay passes all695 canonical/private Korean resources and all38 bounded TIFF/C023 values.

The CI APK is debug-key-signed despite release configuration. Original-key signing and publication are separate parent-owned work. This report does not establish an original-key release artifact.

Fresh installed verification completed:
- API30 exact source/raw/JUnit union:73 native +22 app methods; API35:74 +25. No missing, unexpected, failing or skipped executed methods. Original explicit API35-only exclusions remain on API30.
- API30 phases(seconds/budget): ordinary83.605/180, gallery34.406/90, vertical100.947/180 and91.688/180, native20.146/180. Complete-script marker+383 seconds.
- API35: ordinary133.039/180, gallery44.270/90, vertical109.447/180 and99.840/180, seed5.729/60, verify8.527/60, native28.565/180. Complete-script marker+476 seconds.
- Both satisfy the ordinary/gallery30-second/20-second remaining-margin targets. No timeout or oracle was changed.
- Each API retains all96 original images,8 exact reachability receipts and28 native drag traces. Raw app-owned transport ZIPs, manifests, member inventory/length/hash bounds, reconstructed host bytes, all native DOWN/MOVE/UP ownership and cleanup assertions pass.
- Both retain the strict four Korean picker/rotation/public/private identity rows with exact strings, four real installed-WebView large-font viewport rows, all navigation methods and a distinct cold gallery process. API35 proves the live seed/top-resumed gallery/external force-stop/PID-absence/normal verification boundary.
- All16 fresh labelled contact sheets covering192 images were inspected, plus two original-size API35 emoji-landscape description and literary-Chinese portrait-maximum images. Controls/description/filename reached by scrolling, endpoint states and editor returns support the existing bounded scope. Initial clipping is still visible in initial frames and remains open. These are vertical JPEG/control images, not TIFF-description screenshots.

Original artifact IDs/digests are retained in `workflow-artifacts.json`; both detailed device receipts and the strict verifier are included. Host raw data is retained in ordered50KB UTF-8 base64 parts described by `host-parts.json`. Complete raw postmerge device packets are retained in ordered50KB UTF-8 base64 parts described by `device-parts.json`. The two retained ZIPs preserve raw instrumentation/JUnit, startup/logcat, process boundary and raw locale transport evidence; only duplicate extracted locale images and the emulator console/probe diagnostic are omitted. `replay_retained.py` reconstructs every packet and image from these parts, checks Git blob/size/SHA256 identities and replays the full host/device/compiled-resource checks. The optional original `--build-archive` enables independent APK/source replay. An isolated reconstruction/replay of all retained parts, including the original build archive, passed. Actual-pixel review remains separately recorded. No installed TIFF-dialog, accessibility, native-speaker or full-language acceptance is claimed. Initial clipping and the unchanged475/3/472 localization register,12 probable and four uncertain findings remain open.

## Retained evidence replay

With the exact source checkout and this evidence directory:

```sh
python3 replay_retained.py --source /path/to/source --directory /path/to/new-output --build-archive /path/to/original-build.zip
```

The source blobs and executable modes are checked before importing any source helper. The original build ZIP is optional and not embedded in the retained evidence; omitting it explicitly leaves fresh APK/source replay unperformed. `publication-payload-review.json` records the public-destination/synthetic-emulator provenance and bounded credential-pattern review before archival. No owner device, account login or personal session data was used.
