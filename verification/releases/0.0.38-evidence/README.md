# AN Paint 0.0.38 release metadata evidence

## Exact release identity

- Package: `paint.anpaint.android`; version `0.0.38`; version code `95`.
- Release source: `2c1bd8622eb6c57444eee8f816194b309fff136e`.
- Accepted source tree: `83f46e5d4772e98610bd6eb6fcc5a3964d19cd84`.
- [Full release push run 38095872353](https://github.com/c933103/AN-Paint/actions/runs/38095872353): all five jobs completed successfully.
- CI APK SHA-256: `dafcbea9e33732d6bdccbefb826a287846f13e24d0b5523ce33a40bfe59a80e0`.
- Final signed APK SHA-256: `24ac73d90adac2a77e54989f37386f0405166e2bba74b5a039122c327493f675`.
- Corresponding-source SHA-256: `4e490e5c973ade4dac8a0106b73b5c1dc69893765770260265d60113fa61f874`.
- Original upgrade certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`; exactly one signer.

The metadata commit and publisher-only commits are distinct from the APK's release source. The request intentionally retains the exact tested source and successful full release run above.

## Evidence and bounds

[Immutable postmerge acceptance report](https://github.com/c933103/AN-Paint/blob/89ed520b41a428b0cca97da810b366e8615da9fc/verification/pr43-postmerge-runtime-2026-10-11/REPORT.md) records exact-source, corresponding-source, compiled-resource, JVM, lint, resource-generation and installed-device verification.

- The request records 998 actual passing test identities and fresh report hashes: 804 JVM tests in 85 suites, 95 API-30 tests and 99 API-35 tests. Zero release app lint issues.
- API-30 SDK suppressions and the explicit API-35-only accepted-credit restart exclusions are recorded separately. They are not passes.
- Two obsolete historical selectors are explicitly superseded by six current checks in `metadata-validation.json`. The old selector names are not claimed to pass.
- The acceptance report documents inspection of 192 fresh images on 16 labelled contact sheets and two full-size spot checks. This supports only its bounded vertical JPEG/control reachability scope.
- Initial clipping remains open. No installed TIFF-dialog, accessibility, native-speaker, full-language or physical-device acceptance is claimed. The 475-row localization recheck register and its unresolved findings remain the acceptance record.
- Recorded timing margins apply to this run; no generalized performance guarantee is claimed.

`signing-verification.json` and the public tool reports record the final APK signature, package/version, four native ABIs, non-debuggable status and 16-KB alignment. The certificate subject's historical “Android Debug” label does not establish the app's debuggable flag; the exact original certificate digest and APK metadata are the relevant identity checks. The signature tool's scheme results and warnings are retained verbatim.

`metadata-package-validation.json` records a separate replay of the public signing patch against the exact CI APK. It reproduced all 119,914,458 final bytes and the final APK hash, with unchanged non-signature application payload. Only public signing/alignment bytes are in the patch.

## Publication gate

This commit prepares the release request, notes, public signing patch and receipts atomically. It does not establish that release publication succeeded.

The safe publication-state recovery changes in PR #45 must be merged before this metadata request is merged. Merging `verification/releases/request.json` into `develop` triggers the publication workflow, which must complete successfully and be followed by tag, release-state and downloaded-asset verification. No source or workflow code changes are part of this metadata package. Android CI ignores `verification/**`; the exact-source release run remains the Android verification evidence.

`SHA256SUMS.txt` lists the prepared metadata/evidence file hashes, excluding itself.
