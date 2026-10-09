# Final passing PR #30 CI receipt

[Run 37938647587](https://github.com/c933103/AN-Paint/actions/runs/37938647587)
verified source `9bbfad58ff8a8784240a12db4ec96085c030fc05` through merge
`7ed64dd458a1948ed569204c96569b67762770d5`. Both have exact tree
`f26e39a340d5e258f5c448cc453178b4d301e7a4`; base develop was
`8a75b825131f0b24c55a40a3636e9e70792037a8`.

## Terminal outcome

- APK/source and instrumentation compilation passed.
- **706 JVM tests passed**, zero failures/errors/skips.
- **Lint completed with zero issues.**
- **94 installed API35 tests passed**: 74 library +18 ordinary +1 external-restart
  seed +1 fresh-process verification. No missing/unexpected cases or runner timeout.
- Ordinary instrumentation: **151.133s**; full runner elapsed **152.318s** within
  the unchanged **180s** budget. Library runner 64.598s; seed 5.950s; verify 7.649s.
- Local combined Python suite: 326 passed in 51.014s, recorded on the source branch.
- All original workflow deadlines and assertions remain unchanged.

`test-results.json` inventories all 800 JVM/installed cases. Both artifact ZIPs were
SHA256 verified before safe extraction; `artifact-manifest.json` records all 1,000
constituent paths/sizes/hashes. Actions artifact links are retained, but their
finite retention is not represented as permanent ZIP archival.

## Scoped native acceptance

- All **1,680** native control cases: 140 catalogues ×2 scales ×3 widths ×API30/35.
  Four JUnit executions took 11.264s; completed counts/timings are in the matrix JSON.
- All **72** representative Activity reachability scenarios passed: 8 executions,
  10.098s. Includes complete per-slice reachability, simultaneous visibility when
  it fits, native button/editability semantics, live edited accessibility text,
  Search action/IME, actual window bounds through same-Activity French/Mongolian
  rotation, and independent parent/column drag behavior.
- Vertical status/description: 4 executions, 2.338s. Existing full SVG-status checks:
  8 executions, 6.566s. Original stronger portrait assertions remain.
- Installed real Chromium retains the entire **320×120px portrait** and
  **640×90px landscape** browser for French/Mongolian at actual system 2×, with no
  controls overlap and the same Activity/browser/query across rotation.
- All requested font transitions, including cleanup to 1×, log matching persisted
  setting, system Resources and target Resources before the next change. The
  exact preference presence/value restoration assertions also pass.

`installed-viewport.json` and `font-transition-diagnostic.txt` preserve the real
provider/configuration records. Host browser measurement/frame is a parent-driven
model and remains explicitly separate from this installed provider evidence.

## Reviewed pixels carry over exactly

All **424** action/window files and **80** vertical files are byte-identical to
`b37782d`, including every personally reviewed PNG published in the preceding
record. `capture-equivalence.json` gives counts and deterministic inventory hashes;
the original manifests identify individual hashes. No duplicate binary upload is
needed. The evidence covers 21 reviewed action/search images and 10 corrected
vertical images; it does not claim personal review of every generated PNG.

Historical failures, including the prior installed transition timeout, remain in
[the preceding record](../fourth-ci-b37782d/README.md). This final passing receipt
does not overwrite or reclassify them. No held PR29 constituent was republished.
No physical-device, TalkBack or fluent-language acceptance is claimed. Final
configured Code/Security review and the root merge decision remain separate gates.
