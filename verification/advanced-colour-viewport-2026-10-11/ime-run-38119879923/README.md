# Row-alignment trial: native captions pass, IME oracle failure retained

Run [38119879923](https://github.com/c933103/AN-Paint/actions/runs/38119879923)
tested head `b56d769fc280ca2bbd5854d3bf92e69463adf1f6` through merge
`9019baccd405ff1918468d21ae1e86fa9546e7a0`; both have tree
`1c2da1417bc970fa939ddf546d9c90eac5ddac79`.

## Observed results

- All 814 JVM methods, including the formerly clipped API30/35 portrait bounds,
  passed across 87 suites. Lint found zero issues. Build/test-APK compilation and
  exact-script generation passed. All 487 production files match the source ZIP,
  which exactly matches the APK-embedded bytes; see `source-binding.json`.
- The installed original positive viewport case passed in 2.468s, with native
  gutter scrolling, complete fixed controls, Cancel and zero commit.
- The installed Hungarian portrait/landscape intrinsic-caption and Cancel case
  passed in 2.099s. The landscape image is clean. The portrait image has a temporary
  system clipboard preview over lower controls: it does not prove unobscured
  portrait control use. The English retained-state portrait image is unobscured.
- The sole state-case failure is `Timed out: actual IME occupies a stable positive
  inset` after 17.895s. Its original failure image visibly shows Android's actual
  full-screen landscape extract editor and keyboard, with synthetic `#13579B`
  and the selection. Logcat records native `onShown` at 07:13:41.767. Native Back,
  subsequent Cancel/reopen and final invalid/valid commit checks remain unrun.
- Ordinary 19/19 methods completed in 134.711s without timeout (18 passed, one
  failed). Native74, gallery3 and vertical4 passed; restart checks were withheld.
  The earlier blank startup did not recur; read-only startup snapshots now show
  successful gate conditions. No startup production fix or proven root cause is
  claimed, and the prior run remains failed.

## Test-only successor and source diagnosis

Android 15 InputMethodService explicitly leaves the underlying app unchanged in
fullscreen extract mode. A positive dialog IME inset is therefore an invalid
universal visibility requirement. `ime-window-source-diagnosis.json` pins the
primary source, exact UiAutomator2.2.0 source JAR, and the public clipboard-overlay
window title; `ime-window-excerpt.txt` retains relevant original log lines.

The successor observes the configured native TYPE_INPUT_METHOD window, visible
nonempty root/bounds stable for 250ms, then injects exactly one Back and retains
all exact dialog/field/value/selection and zero-callback predicates. Stable native
IME absence is required as well. It records actual window/inset facts and captures
success or failure before the method's dialog-dismiss cleanup. No production
input flag, IME mode, permission, startup or deadline changes are made. Actual
pixels and completed outcomes still require a fresh exact-head installed run.

The Hungarian caption capture waits for the known ClipboardOverlay window to
leave naturally within the existing bounded wait. It does not clear clipboard,
dismiss another window or use an arbitrary delay. A new clean portrait image is
still required. Large-text 2× remains unaccepted.

## Preserved evidence

The focused ZIP contains three unchanged raw app-owned exports, every original
native image/receipt, 24 model PNGs/eight reports, all 87 JVM XML, lint XML,
installed summaries/XML, public CI log, exact APK/source binding and source
explanation. Every nested manifest/member is hash-verified. Direct images and
receipts are convenience copies; none replaces or edits a failure.

The archive inspection covers every text/PNG/nested export and high-confidence
credential indicators. Clipboard suggestions visible in the original failed IME
image are the synthetic `Artwork 作品` and public credit URL fixtures from
`EditorDeviceTest.kt:562` and related tests, not unrelated private clipboard data.
No full-device logcat or credentials are copied into this focused public archive.

```sh
cat row-focused-evidence.zip.part* > row-focused-evidence.zip
sha256sum row-focused-evidence.zip
unzip -t row-focused-evidence.zip
```

Compare the resulting size/hash with `source-binding.json` before extracting.
