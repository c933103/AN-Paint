# PR32 corrected-head acceptance receipt

Accepted source head: `29cbe495b79231df6c1c5e93928fb9821cb6b9e6`.
Accepted tree: `ab5ff7fe6d04d5e22348b979c9e0054eef9b1c0f`.
CI synthetic merge `f5d2d3ac79864c5b91a502f24df93b62bdbe4718` was fetched independently
and has that exact tree. Actual develop base: `0b3d737e19448c47d36deee8cebfffd5d40c1ea3`.

[Run 37957075692](https://github.com/c933103/AN-Paint/actions/runs/37957075692),
attempt 1, completed successfully in all three jobs.

## Hash-verified results

- 348 Python contracts passed; phase wall 56.726 seconds.
- 723 JVM/Robolectric executions in 75 suites; zero failures, errors or skips.
- All seven Help cases passed in 5.726 seconds. The complete Japanese provider
  sentence is checked on both API30/35 JVM configurations. The real Help/picker
  Activity route is exercised under the API35 Robolectric configuration.
- Lint: zero issues. Universal APK, matching source and test APK build passed.
- API35 installed: 74 library + 18 ordinary app + 1 restart seed + 1 restart verify
  = 94 completed checks. App coverage union: all 20 declared app methods complete.
- Ordinary installed suite: 157.270448600 seconds / 180, margin 22.729551400 seconds.
- JVM wall: 338.801 seconds / 720; lint/native wall: 217.218 / 360.
  Complete regression job: 683 / 1,200 seconds, margin 517 seconds.

The installed checks are regression coverage, not new Help-specific device tests.
API30/35 Help checks are JVM/Robolectric configurations, not two installed runs.
Profile spans may overlap and are not exclusive CPU time. Per-phase ceilings do
not guarantee all phases and artifact upload fit inside the outer job deadline.

## Review and exact correction

Current-head [Code review](https://github.com/c933103/AN-Paint/pull/32#issuecomment-6084770602)
completed with no major issues. The prior Japanese boundary finding is resolved,
with the original finding and fix reply retained in the PR. The new host oracle
failed against the prior text and passed after removing one ASCII separator.
Both host and JVM oracles now include the complete resulting provider sentence.
An independent reread checked all 60 quote/particle/punctuation boundaries and
verified the exact correction and hashes. No other concrete join issue was found;
full-sentence native fluency remains outside this evidence.

Actual Security review completed on `80914c9`, before the Japanese correction.
One later manual Security request appeared as Code review; no Security run on
`29cbe49` is claimed. `security-review-boundary.json` proves the complete ten-file
delta: exactly one byte 0x20 removed from the Japanese XML, all other bytes in
that file identical, plus two tests and seven evidence files. No production
Kotlin, Android manifest, permission, dependency, workflow, provider or credit
behavior changed. The recorded merge gate assessed this bounded review boundary;
no state cycling or repeated requests were used to change a summary label.

## Durable evidence

Original artifacts were independently downloaded and SHA-256 checked:

- Regression/lint 11631225564, 30,537,610 bytes:
  `2c3179518b738226d84ae0c01b2c857ba9119d5657a5568cf6ec38be74b65e10`.
- API35 11631106111, 1,905,435 bytes:
  `208f5df132c234589c82980777f63564eb95880423a37d62a550f04629c81e6d`.
- Preserved ZIP, 286,087 bytes:
  `5bd750707d6f9679f836ed653537316fffc5f6042dfe8265f77766ee4ff2b4c2`.

The ZIP preserves all JUnit XML/identities, lint reports, phase/profile logs,
installed invocation/restart records, raw job logs and original artifact
inventories. Rendered previews and system logcat are inventoried, not duplicated.
APK/source metadata and successful CI identity/extraction logs are retained; the
142 MB binary archive was not separately downloaded or independently unpacked.

PR32 merged as `43148951ac6bd23687e66685855909ac538ba004`. Its independently fetched
actual merge tree equals the accepted tree exactly, with parents `0b3d737e` and
`29cbe495`. This is the premerge acceptance evidence. The automatic real-develop
push run 37959160542 is a separate check and was still running when this receipt
was preserved; no postmerge pass is pre-claimed here.
