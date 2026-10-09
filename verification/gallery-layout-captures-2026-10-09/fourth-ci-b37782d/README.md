# Complete host acceptance, installed transition setup failure

[Run 37936204579](https://github.com/c933103/AN-Paint/actions/runs/37936204579)
tested exact tree `7a6a59874d3f8ea6ef68d818b37f3f9620af85b0`, shared by merge
`fe6765124ff084ed6186d75a8ec56e049b7bc70f` and source head
`b37782de025e0994831cce3c19b8615a89092fc8`.

- APK/source and instrumentation compilation passed.
- **706 JVM tests passed**, zero failures/errors/skips. Lint completed with **zero
  issues**. Gradle completed in 10m 38s under the unchanged 12-minute checks deadline.
- All **1,680** catalogue cases completed, 4 JUnit executions in 21.221s.
- All **72** representative gallery scenarios completed, 8 JUnit executions in
  14.071s. Every action/status/query slice is reachable; full simultaneous visibility
  remains required whenever it fits. Live editable accessibility text, native
  semantics, Search action/IME, actual ViewRoot bounds through same-Activity
  French/Mongolian rotation, and orthogonal parent/column gestures all passed.
- Browser host measurement/frame modeling uses only actual parent specs/coordinates.
  `host-window-summary.json` retains all 72 measured post-action browser/window
  records. This host evidence does not replace real Chromium measurements.
- Vertical status/description: 4 passing executions in 3.856s. All 80 PNG/JSON files
  are byte-identical to the previous corrected run, including the ten personally
  reviewed PNGs published in the parent directory. Existing full SVG status tests:
  8 passing executions in 10.547s, with their stronger portrait checks unchanged.
- Installed API35: 74 library cases passed; ordinary 18 completed with 17 passes and
  one new viewport-test setup timeout. French real-browser portrait/landscape
  passed, as recorded in `installed-viewport.json`. The second locale timed out
  waiting for the real 1×→2× transition; Mongolian was not launched in this run.
  Restart seed/verify were not reached. Ordinary duration 174.888s, not a full pass.

The original target-Context-only barrier could advance before the actual global
configuration arrived. `font-transition-diagnostic.txt` preserves the relevant
logcat records, including global 1.0 at 13:36:08.145Z. The next source commit strengthens
the wait to require matching persisted setting, system Resources and target
Resources on the main thread, with before/after diagnostics and unchanged deadlines.

Both ZIPs were hash verified before extraction. The manifest lists all 990 files;
the result inventory retains all 798 cases, including the failure. This evidence
branch preserves this mixed outcome independently of later source revisions.

## Reviewed native screenshots

`reviewed-captures/` preserves 21 personally inspected PNGs and paired original JSON,
with per-file SHA256 and boundaries in `visual-review.json`:
- API35/2× portrait status for all nine representative locales.
- API30/2× landscape edited-search views for the same nine locales.
- API35/2× narrow 240dp search for French, Hakka and Mongolian.

The visible French/Hakka labels naturally wrap, Arabic placement is mirrored,
and Tibetan/Dzongkha labels and native multilingual query are intact in the
inspected search views. Vertical captions use the accepted column mechanism.
The currently focused viewport may show only part of other controls; full endpoint
reachability is proved separately by the passing unchanged scroll assertions.
These 21 are a documented selection, not a claim that all 144 PNGs were inspected.
No selected PNG/JSON duplicates a held PR29 constituent. The blank host browser
area is not a real Chromium capture.
