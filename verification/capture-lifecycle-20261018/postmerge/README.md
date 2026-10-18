# PR138 natural postmerge verification

Accepted source is merge commit `248d5d41e4114f9252c858c3ac08f2bb124746dc`, tree `f2870b51aba6c8290e929c7fa176c4d14c802d52`, identical to reviewed PR138 head `81404c63c54b47a7cc3f55bacaee93e14d98eb9b`. This includes #123, #133, #135, #136 and #137. Later #139/source `798e6159` has separate verification ownership and is not covered by this report.

[Workflow 39140653627](https://github.com/c933103/AN-Paint/actions/runs/39140653627) completed successfully on attempt 2. Final independent artifact verification was completed on 18 October 2026 at 19:45 UTC. Required exact-head Code review and all six premerge jobs had passed before the parent merged #138; [the immutable premerge receipt](https://github.com/c933103/AN-Paint/blob/2e91f457f76f656915f56b24c8ed55bdbec28cb8/verification/capture-lifecycle-20261018/premerge-integrated/README.md) records those results. Advisory Security was clean on earlier head a569e08, not exact final head 81404c63.

## Actual execution and the targeted retry

Attempt 1 passed build, regression, core, position and composition. Exact-script setup alone failed installing NDK 27.2.12479018 (“Archive is not a ZIP archive”); its nine probes never ran and it uploaded no artifact. [The original failure](https://github.com/c933103/AN-Paint/blob/dfed7d929b42fccc5d2232f2cb6aa172ed529e2d/verification/capture-lifecycle-20261018/postmerge-exact-attempt-1-failure/README.md) remains preserved. Terminal attempt-1 metadata and full failed log are also in this final packet.

After that run was terminal, one targeted unchanged-source retry was requested for job 117714218072. Only exact-script actually executed afresh:

| Job | Original job | Latest API job | Actual UTC execution |
|---|---:|---:|---|
| Build | 117714217962 | 117719764484 | 15:28:45–15:38:37 |
| Regression | 117714218065 | 117719764061 | 15:28:45–15:47:22 |
| Core API35 | 117716422023 | 117719795534 | 15:38:39–15:52:39 |
| Position API35 | 117716422056 | 117719788490 | 15:38:39–15:43:36 |
| Composer API35 | 117719467813 | 117719765091 | 15:52:41–15:52:55 |
| Exact-script retry | 117714218072 (failed setup) | 117719763077 | 15:54:03–15:56:39 |

All six latest records succeeded. The five copied records have new IDs/attempt fields but retain their original successful execution intervals. Complete raw histories contain 12 jobs and 8 artifacts; collection counts and unchanged terminal attempt were checked. The embedded composition receipt still correctly identifies attempt 1. A separate scratch verifier recomputes original and current selection using the unchanged production selector, binds original/current intervals and combined artifact creation/update bounds, and rejects stale/fresh/failed/ambiguous/wrong-source metadata. Its 12 synthetic tests passed normally and with Python optimization. These scratch checks do not modify production behavior, assertions or deadlines.

## Actual downloaded evidence

- 1,142 JVM tests across 123 suites, no failures/errors/skips; all six crop-preview JVM methods and complete relevant French/Japanese/model suites match the declared source methods.
- 985 hosted Python tests; the same 985 normal and optimized local tests passed on the final integrated source.
- All nine exact-script probes and log hashes match this exact commit/tree.
- 1,222 packaged tracked source files and modes match the 1,225-file source tree, with only the three documented source-packaging metadata omissions. Embedded/companion source ZIP, main APK and prebuilt test APK identity bindings pass.
- Complete exact-source API35 union: 74 native plus 45 app methods.
- Downloaded original core and position ZIPs were recomposed using the unchanged composer. All 248 composed files match byte-for-byte; the additional original selection receipt is independently verified.
- Mandatory capture transports were replayed using the unchanged real validators: 12 dialog cases; 4 vertical exports with 104 data files; 32 matrix screenshots; 8 reachability cases with 64 screenshots. All 168 extracted files and receipts match byte-for-byte.
- Both mandatory pulls and best-effort logcat returned zero. Required exports were collected before logcat. There was no automatic screenshot recapture, pull retry, ADB restart or relaxed validator/deadline.

Key exact artifact identities:
- Core 12141448766, created 15:52:37, SHA256 `b350b665b807035ccbb6dea628fc590cdf5bf0b2d8165d3c7f57860d4b6af642`.
- Position 12142001512, created 15:43:34, SHA256 `aff1436d812f58012aa3841c46cecbdaa7b934709837aaa8e5e2c9c15b1c3704`.
- Combined 12141458563, created 15:52:52, SHA256 `aa85904637d74a9315ae184501b4f69faef63afa94ece8149e8d05d7e2a43fcc`.
- Exact-script 12141869197, created 15:56:35, SHA256 `211bce9f0deb45551077b4c3dd0770c7188c8bf97cf7386789d88dd46942a2ad`.
All artifact metadata and remaining digests are in checks.json and the packet.

## Durable files and limitations

- `verification-packet.zip`: 393,622 bytes; SHA256 `337e7573de9aac40262c8a9e8823613b7ccc7e8b6e85b4c8bc1ea88b9da3772b`. Contains 249 manifest-listed files: raw run/job/artifact/review metadata, complete JVM XML, host logs, actual collector logs, capture receipts, original setup failure, and the independent verification scripts/tests/receipts.
- `capture-exports.zip`: 4,282,939 bytes; SHA256 `fa4a5d0ee5374ce4b1bfab9756e3abdab50e207c0b07f161272869ca804bd248`. Preserves the exact 16 original installed export ZIPs with individual hashes and source/artifact identities.
- `checks.json`: 64,754 bytes; SHA256 `75bee2a0d1abbd589eb7264c1920e4ca8a736890d7d81a25a0a2f27f48aaf3b5`.

The underlying historical ADB disconnect cause remains unknown. #138 mitigates collection ordering risk; this successful run does not prove that cause was solved. Original #135 stale-composer and #136 setup/capture failures remain failures on their existing immutable refs. This report does not claim independent pixel/glyph/linguistic review, whole-language acceptance, physical-device coverage, private upgrade signing or a release. The source-preserving evidence ref adds only these four report/data files and retains all earlier source and evidence blobs/modes.
