# PR55 installed evidence: SANITIZED DERIVATIVE

This separate packet contains the original bounded functional acceptance and a deliberately sanitized supporting archive. It is **not byte-identical raw CI replay**. Original held evidence has not been changed.

## Source and functional boundary

The source is head `4a35933ff6b6d0013dac8743cc5eeac1c1033e05`, tree `b6bf7626c1d7c4aef669394970046ffc89a5c877`, run `38303992927`. `ACCEPTANCE.json` is retained byte-for-byte as the historical original-input functional result (SHA-256 `e5684bf7b81df201bc02477403e2aae24c3eb0f070da6a6c5d2adb1ce3be8280`). It records API30 95/95 from actual attempt 2 and API35 104/104 from actual attempt 1. API30 attempt 1 remains setup-failed before instrumentation, with all 95 tests unrun.

All unchanged audit reports and `PORTABLE-VERIFICATION.json` describe the original held inputs. Their original raw log, CI ZIP and payload hashes are provenance of those original inputs, not hashes of the sanitized log. `SANITIZED-PROVENANCE.json` lists exact unchanged files and their scope. Do not treat historical raw-archive checks as newly reproduced by this packet.

## Deliberate redaction

`REDACTION-MANIFEST.json` identifies one changed member, `current-inputs/api30/logcat.txt`, and its original/sanitized whole-file hashes. At original line 20476, the entire third-party connectivity-probe response-headers field was replaced with an explicit marker. This removes the response cookie values and associated response-header material while preserving line count and every byte outside that field. It does not remove any instrumentation line or assert that these cookies authenticated a user account.

The other 89 support members, including all phase protocols, XML, native-export ZIPs, and original failed-attempt job log, are unchanged. All 192 current native images remain their original bytes, as are their original reviewed visual results. Four Arabic PNGs had exact-e19 visual reuse in the historical result. No image pixels were edited.

`SUPPORTING-INPUTS.json` binds the sanitized TAR and current member hashes. `DELIVERY-FILES.json` binds this derivative selection. Only this derivative TAR belongs to this selection; no held original log/TAR or APK/source/outer-CI ZIP is included. The original freezing script is retained as historical audit methodology; it is not a command for creating this derivative.

## Verify and replay the sanitized selection

Run `python3 verify_selection.py`, then `python3 verify_support.py --output /fresh/output`. The extraction verifies the sanitized hashes. With the exact source tree, Python 3, Pillow and NumPy, the unchanged matrix, receipt-only prebuilt, platform and native checkers can inspect `/fresh/output/current-inputs`. Their results must be labeled sanitized-log verification. Hash-bearing whole-log results will differ from historical original-input reports, while source, test identities, test outcomes, PNGs and parsed instrumentation evidence should retain their meanings.

`run_audit.py` and outer-archive/payload checks still require the original held ZIP/APK/source downloads and are not reproducible from this sanitized compact packet alone. No new Android or application-test execution occurred. Independent derivative verification and disclosure review are required before publication recommendation; this local artifact does not authorize publication.

## Limits

This remains bounded installed regression and API35 framework LocaleConfig discovery. It does not establish language fluency, Settings-screen visibility, physical-device acceptance, an API33 installed constructor run, private signing, live Commons-provider acceptance, or full translation coverage. Existing short-landscape and pre-click/post-mount limitations remain in the unchanged acceptance. Redaction must not be used to claim universal secret absence or exact raw replay.
