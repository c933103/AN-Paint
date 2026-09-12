# Working on AN Paint

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
- Before triggering a build after GitHub publication, compare the remote tree with
  the intended source snapshot, including file removals. Use GitHub's dedicated
  delete-file operation for removed paths and verify their absence; do not assume
  a null tree entry was applied by a connector.
