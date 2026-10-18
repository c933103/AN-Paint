# Portuguese assembly Help: exact-head verification

PR: https://github.com/c933103/AN-Paint/pull/132
Application head: `cadee014aacdc2d3422d533f76e626f3d4433dd9`
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39097285470

All six jobs passed on attempt 1: regression/lint, APK/corresponding source, exact-script resources, position API35, core API35 and combined API35. The actual PR checkout `6fddf1ed3a753d7e977c90cfaa5e09e14af96e8e` has tree `c0474eab8fccd272b90fb181d3989862044be7f0`, identical to the reviewed head. No production source repair, assertion weakening or deadline change was made.

## Actual artifacts checked

- All 1,127 JVM tests pass across 120 suites, with zero failures, errors or skips. All seven source-declared CropCounterpartGuidanceTest methods pass, including the Portuguese Exact position case, the German/Spanish/Italian cases, complete compiled Help/plurals, actual complete Help dialog and real crop-warning controls. The affected XML is included separately; the packet retains every JUnit XML.
- The Portuguese case verifies “Posição exata”, non-origin first absolute placement, negative/fractional rejection with unchanged project state, Cancel, valid zero, allowed overlap with other positions unchanged, absolute Unplace retaining a gap, snapping origin/collision rules, conditional snapped gap filling and Undo. It reuses pre-Activity locale initialization and preserves every other translated assertion.
- Artifact hashes match GitHub. The actual APK embeds exactly the companion source ZIP. All 1,206 packaged tracked source files match reviewed blobs/modes; `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore` are explicitly omitted metadata. This build uses a CI debug key; upgrade signing remains separate.
- All nine clean/incremental exact-script probes pass on the identical source tree, and their raw log hashes match the summary.
- The complete source-bound API35 union passes: 74 native methods and 45 app methods. The compact receipt records exact identities, no missing/unexpected/failed/timed-out methods, shared build/source identity, and actual core/position attempts. This is ordinary suite coverage, not Portuguese-specific installed layout acceptance.

## Review and preserved local evidence

[Codex Code and Security reviews](https://github.com/c933103/AN-Paint/pull/132#issuecomment-6245664458) both completed without findings on the exact head. [Initial full-entry/local evidence](https://github.com/c933103/AN-Paint/blob/8f67189b3b333a2abf2fcb707f3f00c3ab341851/verification/portuguese-assembly-help-20261018/README.md) preserves complete old/new/corrected-English text, two independent complete-entry source reviews including linguistic assessment, exact four-edit/five-file scope, consumer bindings, old-value rejection, 937+937 host passes, 17+17 focused passes, full resource/link and supplementary compiler receipts. Local Gradle was network-blocked; hosted artifacts supply actual runtime results.

This separate evidence ref preserves every application blob/mode and prior evidence. `checks.json` contains compact run/job/review/artifact/source receipts. `verification-packet.zip` retains terminal snapshots, all JVM and device XML/JSON, exact-script logs, verification scripts and per-file hashes. Bulky APKs and captures remain in the linked Actions artifacts.

## Scope limits

This is bounded complete pt-PT Help and real-consumer verification. It does not certify the whole Portuguese catalogue, native-speaker acceptance, installed Portuguese glyph/layout, enlarged-font, TalkBack or physical-device behavior. Ordinary API35 passes do not add Portuguese-specific installed claims. No production model or locale routing was changed. PR75’s broader obligations remain open; pt-BR, PR56 and existing holds remain untouched.
