# Validated keyboard-action correction and explicit review boundary

Source head `03abccd771c9f3ee3632340e2ce3d3b205274427`, tree
`e2c632d27c90d24e85bbe728e4bf766922fb3cd1`, passed
[run 37942672106](https://github.com/c933103/AN-Paint/actions/runs/37942672106).
Tested merge `72b4f9c29b306e6e2e697241dab6b850dc3594a5` has the identical tree;
base develop was `8a75b825131f0b24c55a40a3636e9e70792037a8`.

## Verified CI

- APK/source and instrumentation compilation passed.
- **706 JVM tests passed**, zero failures/errors/skips; **lint zero issues**.
- **94 installed API35 tests passed**: 74 library +18 ordinary +1 restart seed
  +1 fresh-process verification. No missing/unexpected cases or runner timeout.
- Ordinary instrumentation: **160.208s**; full runner: **161.681s /180s**.
- All **1,680** catalogue cases passed, including actual EditorInfo checks for
  empty and wrapped queries. Matrix JUnit time: 18.526s.
- All **72** Activity reachability scenarios passed, now invoking Search through
  the native InputConnection. Eight executions took 11.691s. Vertical/status
  checks also pass; their four executions took 3.035s.
- The four installed French/Mongolian EditorInfo records show **imeOptions=3**
  (Search), no NO_ENTER_ACTION flag, **inputType=131073** (multiline text), and
  **6 portrait /3 landscape query lines**. Native wrapping/editability remains.
- Real browser geometry is unchanged: full-visible 320×120px portrait and 640×90px
  landscape, actual system 2×, same Activity/browser/query across rotation, exact
  preference cleanup and font restoration.
- Python: 326 local checks passed in 51.107s; CI Python passed in 51.145s.
  Gradle JVM/lint completed in 8m 12s under the unchanged checks deadline.

Both ZIP hashes were verified before extraction. The manifest preserves all 1,000
files and the result inventory all 800 JVM/installed cases. Real installed viewport,
EditorInfo and font-transition diagnostics are retained. Every 504 action/window/
vertical capture file is byte-identical to the earlier reviewed host run, as
recorded in the equivalence JSON. No new binary upload is needed.

## Exact reviewed-head boundary

The configured Security Review is verified at **9bbfad58ff**, completed 14:03:13Z.
After the keyboard correction, Codex returned clean **Code Review** responses at
**03abccd771** (linked in `review-boundary.json`). The two explicit Security
requests produced Code-labelled responses; the Security summary row still names
the older head. A distinct current-head Security result is **not verified**.

The complete six-file delta since that Security-reviewed head is preserved in
`delta-since-security-reviewed-head.patch`, with its SHA256 and scope in the JSON.
The production change only clears the conflicting NO_ENTER_ACTION flag after
creating the real native connection. The remaining delta adds two host regressions,
one installed regression and documentation/log. No provider, proxy, storage,
permission, translation/font resource or deadline changes are introduced.

The Code P2 is fixed, CI-validated, re-reviewed and resolved. Root assesses this
explicit reviewed-head boundary under the authorized merge workflow and controls
integration sequencing. No additional review requests or PR-state changes are
made merely to alter the summary label. Historical failures and previous green
heads remain preserved. No physical-device, TalkBack, every-keyboard or
fluent-language acceptance is claimed; no held PR29 constituent is republished.

The raw delta patch is preserved byte-for-byte, including the single-space context
markers required for blank lines in unified diff format. A whitespace checker run
on the artifact text can flag those markers; they are not whitespace defects in
the source patch, whose own `git diff --check` passed before publication.
