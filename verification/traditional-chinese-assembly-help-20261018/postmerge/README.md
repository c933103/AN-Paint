# Traditional Chinese assembly Help: postmerge verification complete

Merged PR: https://github.com/c933103/AN-Paint/pull/134
Develop merge: `2ad195f1cc79e9190f26581bb1254a88008a28b6`
Reviewed PR head: `50307966ebad759e0e66e13fd18706e1b129305e`
Identical application tree: `f7fd3b473e09ec91a8f06cea1e54ec88b0b47da8`
Natural develop run: https://github.com/c933103/AN-Paint/actions/runs/39122019448

All six natural postmerge jobs passed on attempt 1. Actual downloaded artifacts
were digest-checked and independently verified against the exact merged source.
No test failure, manual retry, source repair, weaker assertion, relaxed deadline
or skipped gate was used in either the PR or postmerge run.

## Verified postmerge results

- 1,132 JVM tests across 121 suites, zero failures, errors or skips. The five
  complete HK/TW Help/resource/real-toolbar/position/Unplace methods match source
  identities and pass. The full 20-method AssemblyActivityTest and seven-method
  CropCounterpartGuidanceTest also match source and pass.
- Real Chinese Help is checked through the assembly toolbar/dialog, including
  dismissal/reopening, full accessible text, complete native TextView line
  coverage, no ellipsis/clipping and every-line scroll reachability at normal
  portrait and 2× short landscape. These are native-graphics Robolectric checks.
- 942 hosted Python checks pass. Earlier local evidence retains 56 focused tests
  and both full 942-test ordinary/optimized-Python suites. Local JVM could not
  run because the uncached Gradle download was network-unreachable; its failed
  setup attempts are retained, not converted into runtime passes.
- All nine clean/incremental exact-script probes pass with the merged source
  identity and raw log hashes verified.
- The complete source-bound API35 union passes: 74 native and 45 app methods,
  no missing/unexpected/failed/skipped/timed-out methods. Core and position
  records agree on checkout, run, build variant, APK/source hashes and test
  source inventory.
- The actual APK's embedded source ZIP exactly equals its companion ZIP.
  All 1,210 packaged tracked source blobs and executable modes match the
  reviewed/merged tree. The three omissions are only `.gitignore`,
  `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore`. This is the CI
  debug-signed build; private upgrade signing is separate.
- Independently rerunning the unchanged dialog/vertical transport and inventory
  validators passes 12 dialog cases, 104 vertical data files, 32 matrix
  screenshots, and eight reachability cases with 64 reachability screenshots.
  Their existing bounded acceptance scopes are unchanged; these unrelated
  installed captures do not certify Chinese Help appearance.

Codex Code and Security are both clean on reviewed PR head `50307966...`,
which has exactly the merged source tree. The review is not relabelled as a
separate review of merge commit `2ad195f...`:
https://github.com/c933103/AN-Paint/pull/134#issuecomment-6248890926

## Evidence and scope

[Initial full-entry review and local logs](../initial/README.md) retain complete
old/reviewed HK/TW values, paragraph-by-paragraph meaning/source assessment,
mutation coverage and local environment failures.
[Exact-head PR evidence](../terminal/README.md) retains the independently
verified premerge run. Both remain unchanged and reachable.

`checks.json` binds this postmerge result to the run, jobs, source and artifacts.
`verification-packet.zip` contains all JVM XML, phase logs, complete device
XML/JSON, exact-script logs, verification code and a per-file digest manifest.
The new test XML and four independent transport/inventory receipts are also
separate files. This commit adds evidence while preserving every existing
application blob/mode and all earlier evidence. Application PR #134 remains
six files: two production Help values and four bounded test/fixture files.

The identified complete HK/TW assembly Help correction is complete. This does
not establish whole-language/native-speaker acceptance, installed Chinese glyph
or TalkBack behavior, hardware/physical-device appearance, or a release.
The precise native-graphics Robolectric layout measurements above are the
Chinese-specific layout evidence actually tested.

TW `plurals/ui_crop_preview_images/other` still contains the separately found
unconditional crop-movement warning. It remains open and unchanged outside this
Help-only scope; its eventual correction must preserve the sole `other` form,
`%1$d`, `%2$d`, `%3$d` and newline. Broader tracker #75 obligations remain open.
PR #56, processing labels, French work, language routing and explicit holds are
unaffected.
