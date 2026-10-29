# Independently accepted test-only successor

Current PR221 head `2e58204c73ff24ea9b73fbaf4d265baa1e0c3fce`, tree
`de438227d759a2def5fc987600c3c1591f452f9f`, first parent original combined
`49a74322ee12a2bbf442f3b57a43f6f0d2b8d0fd`. Original source candidate heads
remain explicit parents of that initial integration and ancestors of the successor.

Three original PR220 JVM failures were verified from original XML: two real
Save/Export/Share consumers expected English Choose-location after accepted HR/BS
translations; one Croatian protected-draft route expected old Save-as wording.
They are failures, not passes. Original exact source4bab486 run40804963602,
regression job123221586689, artifact12869470777
`regression-and-lint-12b36b8cfa3cb763bc2c563506c0e6a64986a085`, downloaded ZIP
SHA-256 `4921ac1b5af5fdd9e9bcdc68369c4095f7bc6bbea7313e191ddb910a9bbf6396`.
Complete original1,850-case XML (three failures) is preserved in the
[original terminal evidence](https://github.com/c933103/AN-Paint/tree/b743332fe32c5ccac09c1e54fa740edc5fa00aab/verification/hr-bs-mk-priority-20261029/terminal-4bab486).
The three relevant XML files are also retained here for direct inspection.

The parent independently accepted exact patch SHA-256
`73145c9cef2d6464aa8759dad9a7805c2e31a65c1f28429c984fdc0ab27153c0` before
incorporation. Two Kotlin files only: exact full HR/BS Choose-location literals,
English source, explicit prior-member presence/null, changed flag, name-only
attributes and display; the HR warning exact historical/English binding and
exactly one `Save as…` → `Spremi kao…` successor. Bosnian warning unchanged.
All actual decision, warning-route and state assertions remain. No production
resource or fixture edit. The only other successor delta is the concise note.

`successor-preservation.json` verifies all51 remaining exact incoming paths,
all six original shared resolutions, all six #113/#219 paths and all five source
ancestors. The complete final source delta has60 paths:51 exact incoming,
six original shared resolutions, two bounded JVM repair paths and one note.
Local and remote full Git tree identity matches, including modes.

Successor targeted host checks:30 normal in6.905s and30 optimized in4.398s,
both exit0. Raw logs are retained. Fresh complete host modes and fresh exact-head
Codex/required hosted run40809479280 are in progress. Initial49a checks are
historical only. The successor has no failure waiver and no release authority.
