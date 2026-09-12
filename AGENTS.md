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
