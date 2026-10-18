# Italian assembly Help: exact-head verification

PR: https://github.com/c933103/AN-Paint/pull/131
Application head: `13cdaf6f8cbf8a764c36aba6bd227f455cbaef8d`
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39093113728

All six jobs passed on attempt 1: regression/lint, APK/corresponding source, exact-script resources, position API35, core API35 and the combined API35 gate. No source repair, weakened assertion, deadline change or rerun was needed. The actual PR checkout `b5f74d85436e33326d75dc1fdf2a8cbd52016312` has tree `38f4130f0452db1fab1477d0362cee0304d2fced`, identical to the reviewed head.

## Actual artifacts checked

- All 1,126 JVM tests pass across 120 suites, with zero failures, errors or skips. All six source-declared CropCounterpartGuidanceTest methods pass, including the Italian Exact position case (0.271 seconds), German/Spanish cases, complete compiled Help/plurals, actual complete Help dialog and real crop-warning controls. The readable affected XML is included separately; the packet retains every JUnit XML.
- The Italian case verifies “Posizione esatta”, non-origin first absolute placement, negative/fractional rejection with unchanged project state, Cancel, valid zero, allowed overlap with other positions unchanged, absolute Unplace retaining a gap, snapping origin/collision rules, conditional snapped gap filling and Undo. It preserves the pre-Activity locale refresh and every translated assertion.
- Artifact hashes match GitHub. The actual APK embeds exactly the companion source ZIP. All 1,206 packaged tracked source files match reviewed blobs/modes; `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore` are explicitly omitted metadata. This build uses a CI debug key; upgrade signing remains separate.
- All nine clean/incremental exact-script probes pass on the identical source tree, and their raw log hashes match the summary.
- The complete source-bound API35 native/app union passes. The compact receipt records exact method identities, no missing/unexpected/failed/timed-out methods, shared build/source identity and core/position attempt 1. This is ordinary suite coverage, not Italian-specific installed layout acceptance.

## Review and preserved local evidence

[Codex Code and Security reviews](https://github.com/c933103/AN-Paint/pull/131#issuecomment-6245112258) both completed without findings on the exact head. [Initial full-entry/local evidence](https://github.com/c933103/AN-Paint/blob/fb28e12722440882fb17a9386275c45cadc677b9/verification/italian-assembly-help-20261018/README.md) remains intact: full old/new/corrected-English text, exact four-edit/five-file scope, consumer bindings, old-value rejection, 935+935 host passes, 15+15 focused passes, full resource/link and supplementary compiler receipts. Local Gradle was network-blocked; hosted artifacts supply actual JVM/device results.

This separate evidence ref preserves every application blob/mode and prior evidence. `checks.json` contains compact run/job/review/artifact/source receipts. `verification-packet.zip` preserves terminal snapshots, all JVM and device XML/JSON, exact-script logs, independent verification scripts and per-file hashes. Bulky APKs and captures remain in the linked Actions artifacts.

## Scope limits

This is bounded complete Italian Help and real-consumer verification. It does not certify the whole Italian catalogue, native-speaker acceptance, installed Italian glyph/layout, enlarged-font, TalkBack or physical-device behavior. Ordinary API35 passes do not add Italian-specific installed claims. No locale routing was changed. PR75’s broader obligations remain open; PR56 and existing holds remain untouched.
