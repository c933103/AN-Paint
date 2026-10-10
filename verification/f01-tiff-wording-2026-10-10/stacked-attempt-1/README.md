# F01 exact-stack CI attempt 1: retained failure and verified increments

Run [38049772357, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38049772357/attempts/1) ended in **failure**. Head `4f9082aa687a5c36b559061bcc10d0e39331610f`, tested merge `73fff41dee17c49a972825c90bdcd88e38287911`, and accepted source tree `04a84df1535297f13a314c521b55647f6d15a678` are pinned in the receipt and independent review. PR43 remains draft and stacked on unmerged PR34 `5703a61394791f18e9f2597272d908d9840599af`.

## Verified increments

- 775 unique JVM methods across 82 XML suites passed, with no failure, error or skip. All nine new TIFF methods compiled and passed, including both complete 26-locale loops with the strict mixed Korean oracle and public selection unchanged.
- Dialog checks cover English variants, pt-BR, vertical/emoji resources, Welsh fallback, both compression choices, toggles, format switching, callbacks and cancellation. These are SDK33 Robolectric results, not installed-device visual or native-speaker acceptance.
- Release lint has zero issues. Host CI discovered 412 tests, passed 410 and skipped only the two optional Pillow ICO/Adam7 decoder checks. The independent local host run previously passed all 412 without skips.
- All seven actual Gradle clean/incremental/stale-output generation probes passed. Canonical/generated mixed Korean XML SHA-256 is `9d928efffd75d06b3a8b6016518c6869b407e95a3b6125b69c13a9482f2d6176`. Final APK resource-table parity is still unproved.

## Retained failure and diagnosis limits

The universal APK step failed after 22m13s, from 11:51:05 through 12:13:18 UTC. The unchanged workflow deadline is 22 minutes. The initial read could only establish timing. A subsequent public-browser read at 12:20:48 UTC confirmed [GitHub’s exact annotation](https://github.com/c933103/AN-Paint/actions/runs/38049772357/job/114206384771#annotation:8:220724): **“The action 'Build universal APK' has timed out after 22 minutes.”** The failure mode is now confirmed; **the underlying reason the build exceeded that limit remains unknown**. The supported job-log read returned `Transport closed` on its initial request and one read retry. Generic annotation/log URLs were unsupported, and the public web run/job pages returned cache misses. The cloud browser could read the public annotation; full logs required sign-in, which was not attempted. Neither the timeout nor those retrieval failures establish a source defect or an infrastructure-only cause. `attempt1-timeout-annotation.json` preserves the timestamp, exact text and URL. The earlier independent report inside the immutable raw ZIP retains its pre-annotation diagnostic limit.

APK/source extraction/upload and test-APK compilation were skipped. The dependent API30/API35 matrix did not execute. There is no current-stack APK/source identity chain, 695-entry compiled canonical/private parity or device picker/rotation/public-identity result from this attempt. Prior PR34 and original PR43 results do not replace those missing results.

A single failure-only retry was requested after verifying the same draft PR head/base and terminal attempt-1 failure. GitHub accepted it; attempt 2 began at 12:15 UTC on the unchanged head. Successful regression/generator job results were carried forward with their original timestamps. This packet records attempt 1; it does not predict attempt 2's outcome. No source, oracle, workflow, deadline or permission changed for the retry.

## Reproducible evidence

`attempt1-raw-evidence.zip` contains all 82 JUnit XML files, release lint XML, all four phase logs/timings, the seven generator logs and summary, and eight independent review/metadata files. `attempt1-evidence-manifest.json` records every member's byte length and SHA-256. `terminal-receipt.json` preserves job/step timestamps, artifact metadata and the retrieval limitation.

The original Actions artifacts were downloaded and their digests verified:

- Regression/lint artifact `11668997775`: SHA-256 `9e504c5ff800a27214e726138ed4d6e889a1a706bbcfb349b53383773c6f4bdf`.
- Generator artifact `11669116173`: SHA-256 `8d2666fa4ad2596b9195f13a3bb48cdd72376036107c6f00b9c6c5d3d768edef`.

The packet was inspected before publication. It contains project source/test evidence only, without credentials, secret values, signed download URLs or private conversation transcripts. Repository visibility is unchanged.

## Open scope

The original two-method Korean failure and first-stack whole-catalogue guard failure remain preserved. F01's 12 probable and four uncertain language cases remain open; seven already-qualified catalogues and 81 missing-key cases remain unchanged. The 81 fallback paths are not individually runtime-proved. Term-specific original history, native-speaker and installed visual/accessibility requirements remain unresolved. Parent register counts remain **475 total / 3 structural completed / 472 pending**; no parent row is closed. PR34's unmerged dependency and review-quota limits remain explicit. No clean final-head Codex review is claimed.
