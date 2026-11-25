# Working on AN Paint

**Localization status reset — 28 September 2026: all previous progress, completion, repair, verification and no-defect conclusions for PRs #2–#9, #12 and #15 are withdrawn. Every item requires a full recheck; no previous progress is accepted.**

See the [individual recheck register](https://github.com/c933103/AN-Paint/blob/review/localization-integration/verification/localization-recheck-register.md). The rejected delivery is additional material to check, not an accepted audit. Historical source, test outputs and evidence classifications remain available as inputs. They carry no current completion credit. The 59 scoped catalogues and 112 fallback catalogues were the 14 October 2026 work split, not the current resource inventory. The 81-locale scope in withdrawn audits refers to the earlier 140-choice inventory.

See [current direct language-resource coverage](TRANSLATING.md#current-catalogue-coverage). The older scope split does not reopen bulk drafting. Track and resolve remaining wording and installed verification separately in [#56](https://github.com/c933103/AN-Paint/pull/56).

- Read `CI.md` before changing or running the Android workflow.
- Long GitHub tests must not block unrelated implementation, source publication,
  or delivery of an accurately labelled development build.
- A request to implement a change in `c933103/AN-Paint` includes publishing the
  task-specific diff to a feature branch in that repository and opening or
  updating its pull request, unless the requester asks for local-only work.
  Review the actual diff and destination. Prior authorization for this workflow
  covers the branch push and PR; merges and releases follow their own criteria.
- Finish relevant local checks, publish the concrete change, link the asynchronous
  run and report its actual pending/passed/failed status. Do not repeatedly poll
  a long emulator run as the only work or hold the conversation open for it.
- Use the current-platform run for routine changes. Run the full Android matrix
  for release verification or a concrete cross-version risk, rather than after
  every edit. Inspect a failure before retrying; do not repeatedly rebuild the
  entire suite without a diagnosed reason.
- Compilation, upgrade signing and matching corresponding source remain required
  for an installable delivery. Pending device checks prevent a “fully verified”
  claim; they do not prevent a clearly identified development delivery.
- Never publish the saved signing key or private build backup to GitHub.
- Build caching may store downloaded dependencies, pinned native source trees
  and ccache's content-checked native compiler objects. Do not restore Java/Kotlin
  classes, APKs, linked native libraries or CMake build directories. Keep compiler
  identity/content checks and strict header checks; do not enable unsafe cache
  sloppiness or depend mode to improve a timing claim.
- Keep patches reviewable: application code, meaningful behavior tests, compact
  resource/font/licence fixtures and concise current documentation belong in
  the application tree. Put bulky generated logs, captures, inventories and
  historical reports in CI artifacts or a dedicated evidence ref.
- Do not add permanent whole-source hashes, recursive inverse adapters or
  historical snapshot reconstruction as substitutes for behavior tests. Preserve
  old evidence once under an immutable reachable ref before migration/removal.
- Test the actual requirement. Preserve independently specified accessibility,
  lifecycle, resource and corruption regressions; complete current-resource
  display checks are control bindings, not freezes of previously approved prose.
  Record exact raster differences without silently
  converting every antialias fringe into a production defect. Unexplained visual
  differences require explicit review; do not conceal them or invent a tolerance.
- Canonical Android resources own current wording. Check that real consumers
  display the complete selected resource and preserve independently specified
  semantic, formatting, script, legal and safety boundaries. Do not recreate
  full-language approval mirrors, predecessor adapters or per-edit test packages.
  The same rule applies to smaller copied sentences and source-spelling guards:
  retain a literal only for an independent semantic/format/script/legal boundary,
  not merely because it was once approved. Prefer existing real consumer tests
  over repeating their behavior in every locale. Keep distinct glyph/layout,
  routing and state regressions; map survivors before removing repetitions.
  Do not duplicate host wording checks in JVM tests whose purpose is compilation
  or selected-resource escaping. Use affected checks and one required exact-head
  CI/review path; do not request a second review when automatic review is active.
  Historical review scopes above are records, not requirements to keep catalogues
  empty or incomplete; immutable source/review history preserves those decisions.
- Audit test work by obligation and inner loops, not only file/fixture bytes or
  JUnit method counts. Inline maps and near-complete clause lists can recreate
  retired approval catalogues. A locale-by-status or repeated-dialog Cartesian
  product needs a distinct routing, formatting, glyph/layout or state reason;
  do not replay the same consumer merely to compare another approved sentence.
  Keep capture-only diagnostics and expected historical defects distinct from
  acceptance. An unmapped structural guard may remain explicitly structural;
  a similarly named runtime test is not evidence that it covers the same path.
- Before publication, compare the remote tree with the reviewed checkout,
  including every intended removal and retained file's content and executable
  mode. A fresh complete Git tree is allowed for an archived migration; do not
  rely on unverified null tree entries. Preserve the expected parent and a
  non-force branch lease. Verify the final remote tree before triggering CI.
