# Working on AN Paint

**Localization status reset — 28 September 2026: all previous progress, completion, repair, verification and no-defect conclusions for PRs #2–#9, #12 and #15 are withdrawn. Every item requires a full recheck; no previous progress is accepted.**

See the [individual recheck register](https://github.com/c933103/AN-Paint/blob/review/localization-integration/verification/localization-recheck-register.md). The rejected delivery is additional material to check, not an accepted audit. Historical source, test outputs and evidence classifications remain available as inputs. They carry no current completion credit. The current picker scope (14 October 2026) is 171 locale options: 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback for this bounded work. Completing those 108 catalogues is outside this task. These counts do not claim translation completeness or linguistic acceptance. The 81-locale scope counts in withdrawn historical audits refer to the earlier 140-choice inventory, not the current 167-option scope.

- Read `CI.md` before changing or running the Android workflow.
- Long GitHub tests must not block unrelated implementation, source publication,
  or delivery of an accurately labelled development build.
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
- Test the actual requirement. Keep full-text, accessibility, lifecycle, resource
  and corruption checks; record exact raster differences without silently
  converting every antialias fringe into a production defect. Unexplained visual
  differences require explicit review; do not conceal them or invent a tolerance.
- Before publication, compare the remote tree with the reviewed checkout,
  including every intended removal and retained file's content and executable
  mode. A fresh complete Git tree is allowed for an archived migration; do not
  rely on unverified null tree entries. Preserve the expected parent and a
  non-force branch lease. Verify the final remote tree before triggering CI.
