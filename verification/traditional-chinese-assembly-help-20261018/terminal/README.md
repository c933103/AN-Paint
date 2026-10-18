# Traditional Chinese assembly Help: verified final-head gates

PR: https://github.com/c933103/AN-Paint/pull/134
Application head: `50307966ebad759e0e66e13fd18706e1b129305e`
Application tree: `f7fd3b473e09ec91a8f06cea1e54ec88b0b47da8`
Run: https://github.com/c933103/AN-Paint/actions/runs/39120393383

All six exact-head CI jobs passed on attempt 1. Codex Code and Security reviews
both completed on this same head with no findings or unresolved findings:
https://github.com/c933103/AN-Paint/pull/134#issuecomment-6248890926
There are no review threads. This record does not itself merge the PR.

## Actual artifacts verified

- 1,132 JVM tests across 121 suites, with zero failures, errors or skips. All
  five source-declared TraditionalChineseAssemblyHelpTest methods passed:
  complete compiled HK/TW Help; actual Help toolbar/dialog dismissal and
  reopening in ordinary portrait; complete accessible text, all native lines,
  no ellipsis/clipping and every-line scroll reachability at 2× short landscape;
  and each locale's actual Exact position/Unplace controls and behaviors.
- All 20 source-declared AssemblyActivityTest and seven CropCounterpartGuidanceTest
  methods also passed. The existing French complete-value oracle is unchanged
  on this branch and passed. No assertion was removed to obtain green results.
- 942 hosted Python checks passed. Locally, 56 focused checks and both complete
  942-test ordinary/optimized-Python suites passed. Local JVM execution was
  blocked before compilation by the unavailable Gradle distribution/network;
  its raw failures remain preserved in the initial evidence.
- All nine clean/incremental exact-script generation probes passed, with the
  exact application tree and verified raw log hashes. Resource routing,
  production mirrors and test deadlines are unchanged.
- The complete source-bound API35 union passed: 74 native and 45 app methods,
  with no missing, unexpected, failed, skipped or timed-out methods. Core and
  position identities bind to the same checkout, run, variant, APK/source
  hashes and source test inventory.
- The actual APK embeds exactly the companion source ZIP. All 1,210 packaged
  tracked source files match the reviewed head's blob content and executable
  modes. The only omitted tracked files are repository/editor metadata:
  `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`.
  The build uses the CI debug key; upgrade signing is a separate step.

The PR test checkout `9dc4f4abe4014f1df602a48c386f100eedeb927b` has exactly the
reviewed application's tree. Every downloaded artifact was digest-checked
against GitHub before inspecting its contents. No source repair, weakened
assertion, changed deadline, manual rerun or ignored failure was needed.

## Durable evidence

The [initial complete-entry review and raw local checks](../initial/README.md)
retain both original and reviewed full values, paragraph-by-paragraph source
assessment, exact scope, full host logs and local JVM environment failures.
`checks.json` records final run/job/review/source/artifact identities and the
verified results. Related test XML is separate. `verification-packet.zip`
retains every final JVM XML, CI phase logs, complete device XML/JSON receipts,
exact-script raw logs, verification code, and a per-file SHA-256 manifest.

This evidence commit adds files to the previous evidence ref and preserves
every application blob/mode and every initial evidence file. Generated evidence
is not added to the application branch.

## Limits and separately open work

This is bounded full HK/TW assembly Help verification. Native-graphics
Robolectric layout/accessibility/scroll checks are not installed-device Chinese
glyph, TalkBack or physical-device acceptance. Ordinary API35 regression does
not independently establish the Chinese Help's installed appearance. No
whole-language completion or native-speaker certification is claimed.

TW `plurals/ui_crop_preview_images/other` still contains the separately
identified unconditional crop-movement warning; it remains outside this
Help-only correction and unchanged. PR #56, processing labels, French work,
locale routing and broader localization obligations are outside this patch.
