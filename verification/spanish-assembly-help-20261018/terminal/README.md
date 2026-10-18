# es-ES assembly Help: exact-head verification

PR: https://github.com/c933103/AN-Paint/pull/130
Application head: `94869be423441fc943ff0b2eeb8dfe76036c83bb`.
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39089294725

All six jobs passed: APK/corresponding source, exact-script resources, regression/lint, position API35, core API35 and the combined API35 gate. The actual PR checkout `d6b66a352eb8baf7cb5ebba98d86861b3fdbb02d` has tree `e3ba7b23a38230f7820d148d5e99eaf364f7c20c`, identical to the reviewed head.

## Actual regression result

All 1,125 JVM tests pass across 120 suites, with zero failures, errors or skips. All five CropCounterpartGuidanceTest methods passed, including the new Spanish toolbar/position case (0.235 seconds), the existing German case, whole compiled Help/plural values, actual complete Help dialog and real crop-warning controls. The readable affected XML is included separately; the packet preserves every JUnit XML.

The Spanish case verifies the initial “Posición exacta” toolbar label, non-origin first exact placement, negative/fractional X/Y rejection, unchanged saved project after invalid input and Cancel, valid zero, allowed overlap with other positions unchanged, absolute Unplace leaving a gap, snapping origin/collision rules, conditional snapped gap filling and Undo. It inherits the existing pre-Activity app-wide locale refresh; no production workaround or weakened translated assertion was needed.

The downloaded regression artifact SHA-256 is `1a89ed89692eaf3f251d1942f1ef76ec2d5c4654f9e425cf9d73d6613de8d003`, matching GitHub's digest. `checks.json` records the exact artifact/run/job IDs and affected method durations.

## Review and local evidence

[Codex Code and Security reviews](https://github.com/c933103/AN-Paint/pull/130#issuecomment-6244609369) both completed with no findings on this exact head. [The initial full-entry/local evidence](https://github.com/c933103/AN-Paint/blob/c2983bd2b05cd6c418e4681bbc8b0de58920259e/verification/spanish-assembly-help-20261018/README.md) remains intact: the full old/new/reference text, exact four-edit/five-file scope, source bindings, old-value negative control, 933+933 host passes, 13+13 focused passes, full resource/link and supplementary compilation receipts. Local Gradle was network-blocked; the hosted runtime execution above supplies the JVM result.

This separate evidence ref retains the entire application tree. The packet contains exact terminal run/job/review snapshots, source checkout binding, all 120 JUnit XML and a per-file SHA-256 manifest.

## Scope limits

This is bounded resource and real-consumer verification. It does not certify a complete Spanish catalogue, native-speaker acceptance, installed Spanish glyph/layout, enlarged-font or TalkBack behavior. Passing the ordinary API35 suite does not add Spanish-specific installed-device claims. There are no generic-es/es419 routing changes. PR75's broader obligations remain open, while PR56 and existing holds stay untouched.
