# AN Paint 0.0.40: final publication verification

Verified 20 October 2026 (UTC). [Public release](https://github.com/c933103/AN-Paint/releases/tag/v0.0.40), release ID 418637745, published at 16:47:51 UTC.

## Exact identities

- Release source and tag: `d664b3e72ea3261dba662119a429b0bb3914c04a`; source tree `409a41191173f98d10155b8058b232efa1a527fc`.
- Version-preparation PR: [#153](https://github.com/c933103/AN-Paint/pull/153). Natural release build [39452992495](https://github.com/c933103/AN-Paint/actions/runs/39452992495) passed all nine release/API30/API35 gates. Prior build, SDK inventories, report hashes, signing and reconstruction evidence is in [the terminal build receipt](../release-build-0.0.40-20261020/TERMINAL-README.md).
- Publication-input PR: [#154](https://github.com/c933103/AN-Paint/pull/154), reviewed exact head `c88c4e49e5696d04bf31e14e2f9045670faf9b77`, tree `0d889c8b13996f0b0afb3963939f6ca0d33d5231`; merged as `7243bac3225fa9aa45be919e2eb3332b9fa5a40a`.
- Exact-head Codex Code and Security review reported no findings. The three publication-input files were path-filtered from Android PR CI as designed; 61 normal and 61 optimized release-contract tests passed locally. Both complete logs are preserved here.
- Natural publisher [39460180541](https://github.com/c933103/AN-Paint/actions/runs/39460180541), attempt 2, job 118758497207, completed successfully.

## Preserved first failure and reconciliation

Attempt 1, job 118757306003, failed at the existing release-identity verification after creating draft release 418637745 with no assets. The original masked job log and its public verification artifact are retained. A later readback found every expected predicate and the exact 4,336-character notes body matching; the unmodified verifier passed. One normal failed-job rerun then succeeded. No release or asset overwrite, replacement, deletion, publisher relaxation or manual dispatch was used. The original mismatch's cause is not established; later equality does not identify its cause.

## Independent public-byte checks

`final-publication-verification.json` records the completed checks; `final-publication-metadata.json` preserves release/tag/run/job/review metadata and the unchanged v0.0.39 comparison. `public-asset-download-verification.json` records eight fresh unauthenticated HTTP 200 downloads, using exactly the release API's public `browser_download_url` values with ordinary redirects.

- All four v0.0.40 public assets have the exact expected names, sizes and SHA-256 hashes. The checksum manifest contains exactly the expected three entries and each hash matches its freshly downloaded bytes.
- Public APK SHA-256: `b2e6243583ad7a4b6a4b5c3dfb6211cc747fbb2f6b4ad926a18370da72ebcf14` (113,983,450 bytes).
- The fresh public APK independently passes signature verification with the sole existing upgrade certificate SHA-256 `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`; package `paint.anpaint.android`, version 0.0.40/code 97, non-debuggable, four ABIs and 16 KB alignment.
- Embedded corresponding-source bytes exactly equal the freshly downloaded standalone source ZIP, SHA-256 `fa07c7111fe0dd8144c340d6366d095d6b7721398d6949837466deb69b77c62e`. Earlier exact-source validation and non-signature payload equality remain in the terminal build/signing receipts.
- The public verification JSON matches the reviewed request and exact successful source run. The published body equals the reviewed notes, and the release is neither draft nor prerelease. Existing unmodified release identity and job verifiers passed independently.
- All four v0.0.39 public assets were freshly downloaded, match the established hashes and are byte-equal to the previous local downloads. Its checksum manifest, tag, release metadata and asset identities remain unchanged. Cached bytes were comparisons, not substitutes for these fresh public downloads.

## Scope remains bounded

Publication does not close the three unrelated Swedish holds, nine Afrikaans terminology/context holds, wider language/UI/font/device/accessibility work or documented SDK-specific exclusions. The corrected Swedish Curve hint has only its stated independent current-context model review. The newer unpublished Czech batch remains excluded. No native-speaker, whole-locale, universal device or physical TalkBack acceptance is claimed.

Only public repository work, public release bytes/metadata and masked workflow output are recorded here. No private key, password, alias, credential or access change is included.
