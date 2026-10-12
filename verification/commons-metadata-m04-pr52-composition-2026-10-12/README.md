# M04 query failure composed with PR52

This is the authoritative source and host-verification record for the combined
PR52/M04 candidate. It is not an Android-verified or merge-ready conclusion.

## Exact inputs and evidence boundaries

- PR52 parent: `71f4d288669858e7975ec4c094b7f47a9a1ff145`, tree
  `815e265af5387111dcdaef66efac5d2091bbb56d`.
- Separately published M04 source checkpoint:
  `045004bb23ef762f1731982f7a0152fef0fc5507`, tree
  `892e09280be9d668862ae5efada0ada163cc6bdb`.
- Shared develop baseline: `4231edaac45d89c52f51e2b77d0f94a1176ad88c`, tree
  `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`.
- GitHub reads verified the selected PR52 head and actual develop before
  composition. The separate working checkout began as the exact clean PR52 tree.

The temporary clone contains the develop and PR52 commit objects. The standalone
M04 commit was published after that clone was created and is not a local commit
object; no synthetic commit substitutes for it. Its exact Git tree `892e0928…`
is present locally with all 1,694 leaves. The commit/tree binding was verified
through connected GitHub reads and the checkpoint publication receipt. Every
carried M04 payload was checked against that checkpoint's SHA256 publication
manifest; local immutable reads may use the full tree SHA above. The absence of
the local commit object does not mean the remote path is missing.

The inherited `verification/commons-metadata-m04-2026-10-12/` folder is preserved
**byte-for-byte from standalone checkpoint `045004bb23ef762f1731982f7a0152fef0fc5507`**.
Its historically worded “current”, “final” and “successor” sections describe that
standalone snapshot. Its 583-test result, 85 independent checks and source-manifest
hash `1b29a1008271a5086350b6b6d0ca781bccf79983d068b1017a3e8a143100eb95` do not certify
this combined source. Its partial-53 failures remain historical failures. Likewise,
all inherited PR52 and producer evidence remains bound to its original snapshots.
No old report, fixture, manifest, failure or result was rewritten or relabeled.
Use this new composition report, its fresh manifest/logs and the separate fresh
independent review for the combined candidate.

## Exact combined source

The source-only manifest lists 91 changed/new source, test, tool and fixture paths
relative to PR52; it excludes verification reports and logs.

- `source-manifest.json`: SHA256
  `d23ba36229197b1a2d90849f6cc89a53d7c156de2707756456c088201c2591bc`.
- `source-vs-pr52.diff`: SHA256
  `d29ba081d5c98af5128c3654da7277cb87fcc6ca8378764cfece5eec413faa90`.

The candidate modifies 76 existing PR52 paths: 60 one-entry resource additions,
two production files, the Nôm font and its inventory digest, one prior Kotlin
query-test successor, and 11 exact historical host-test/projection adapters.
It adds 15 source/test/tool/fixture paths. There are no removals.

The only Kotlin production changes are:

1. Add message-less `QueryFailureException : IOException` and raise it for the
   unchanged `root.has("error")` condition.
2. Add one QueryFailureException resource branch to PR52's existing shared
   HTTP/response-limit mapper, retaining its location, comment and fallback.

Both alive-activity UI callbacks, typed HTTP status/ASCII formatting, M03 byte
limit, JSON/field validation, provider hosts and parameters, document/clipboard
semantics, cancellation, temporary-file cleanup, timeouts and other defaults
retain PR52 behavior. Presence of a top-level error still includes null/false/empty
values; nested unrelated error fields do not become the condition. Provider and
framework details remain verbatim; no provider error fields are exposed by M04.

PR52's mixed-script Korean HTTP expectation remains exact. The old query/validation
Kotlin method splits into the reviewed localized query successor and unchanged
validation cases. The new M04 flow test changes only its standalone HTTP oracle
to require PR52's `HttpException`, status 503 and null message. Its other methods,
assertions, thresholds and 112 planned capture states are preserved.

All PR52 UI/layout source, workflow scheduling, SDK partitions, test methods,
45-second dialog interactions, 300-second dialog phase, 180-second ordinary
phase and 43/53-minute execution/job caps are retained. API35's 74 native and
30 app installed methods, API30's 73 native and 22 app methods, and manual-only
API21/API24 omission policy remain unchanged. No device execution is inferred.
PR51 and the stopped PR53 archive producer are not imported or resumed. M02,
producer disposition, archive/device and release holds remain separate.

## Values, fonts and historical preservation

The default and all 59 accepted values are exact copies of the independently
reviewed v4 input, SHA256
`00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d`.
All 140 per-tag dispositions remain unchanged, including 81 open fallback tags.
No translation, normalization, new language review or native-speaker certification
is claimed. Manchu retains all three U+180E characters, and Traditional Mongolian
retains all three U+202F characters, in XML, fixtures and Kotlin expectations.

PR52's font, inventory and licence bytes were verified identical to the standalone
M04 baseline before carrying the font over. `font-input-preflight.json` records
those comparisons. The final font is byte-identical to the reviewed M04 asset,
SHA256 `6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006`.
The exact additions remain 。 U+3002, 問 U+554F and 追 U+8FFD; old outlines,
metrics, mappings and licence metadata remain preserved. Earlier raster reports
remain source-bound historical evidence; fresh independent font/raster checks
must be reported separately. No Android shaping result is inferred.

All original M02, M03, C05, dialog-composition and M04 scope fixtures and pins are
unchanged. The separate `commons_metadata_m04_pr52_successor_scope.json` records
explicit reversible hunks and both full-file endpoints. It covers 75 text overlaps
and the font's separate strict binary reversal; 1,729 PR52 leaves remain exact.
Together these account for every one of PR52's 1,805 leaves. The M04 view has
seven exact inverse projections: both production files, the prior Copy-credit
Kotlin test, the new M04 HTTP oracle, and the three PR52 changes that overlap
M04's old protected manifest (workflow and two unrelated Kotlin tests).
The original 205-path manifest is unchanged.

Direct combined contracts verify all 24 C05/M02/M03/M04 reversal orders across
all 60 catalogues, preserve each original producer endpoint and check all PR52
leaves. Missing, duplicate, changed, unrelated or expanded deltas and altered
pins fail closed, including under optimized Python. No original oracle or
completeness threshold was relaxed.

## Fresh executed checks

`local-verification.json` binds these logs to the frozen combined source:

- Full host aggregate: **660/660 pass**, 184.672 seconds, process exit 0.
  Raw log: `all-host.log`. Its unittest summary is at lines 665–667; later
  unsuccessful instrumentation JSON is deliberate negative-control output.
- Focused combined preservation/M02/M03/M04/font/C05 contracts:
  **89/89 pass**, 10.695 seconds, `focused-host.log`.
- Same focused contracts with `python -O`: **89/89 pass**, 9.217 seconds,
  `focused-host-optimized.log`.
- Canonical catalogue structure: pass, `catalogue-structure.log`.
- Python compilation and source-only staged/unstaged `git diff --check`: pass.
  The whole evidence-inclusive diff flags two immutable historical Gradle-log
  trailing spaces and context-only blank lines inside the saved patch. Those
  original evidence bytes are retained; this is not a source whitespace defect.
- The frozen 91-path source manifest was rechecked after these runs.

Initial 80 focused and nine new direct-contract runs are retained separately.
They are not substitutes for the final full/focused runs above.

Replay from the repository root:

```sh
python -m unittest discover -s tools -p 'test_*.py' -v
PYTHONPATH=tools python -m unittest -v \
  test_commons_metadata_m04 test_commons_metadata_m04_font \
  test_commons_metadata_m04_composition test_commons_metadata_composition \
  test_localized_dialog_composition test_commons_metadata_m02 \
  test_commons_metadata_m03 test_commons_metadata_m03_font \
  test_locale_font_coverage test_commons_copy_credit_errors \
  test_svg_error_translations test_tiff_c023_wording test_hungarian_attribution_c05
```

Use `python -O -m unittest` with the same focused list for the optimized check.

## Unrun gates and publication boundary

The temporary native cloud workspace has no configured Android SDK, Gradle command
or adb. `current-environment.json` records the observed state. Android/Kotlin
compilation, AAPT/compiled-resource binding, Robolectric execution and all 112 new
captures, lint, APK/native compilation and exact-head installed-device checks
remain **UNRUN for this composition**. TalkBack, physical-device, competent-language
and broad all-language acceptance remain separate.

`expected-jvm-identities.json` is a future-check inventory, not an execution result:
890 expected identities, preserving PR52's 869 identities except the explicitly
recorded one-to-two query-case split, plus 20 M04 executions. Actual JUnit XML must
match the exact identity set; a green count alone is insufficient.

### Planned CI source binding (not an executed result)

The preserved workflow has `pull_request` without branch or activity-type filters
and no checkout-ref override. Subject to its existing path filters, default
opened/synchronize/reopened events therefore test the synthetic PR merge commit.
Artifact names use `github.sha`, and `build-info.json` records `GITHUB_SHA`.
A future verifier must check that merge commit and its full source tree, actual
PR head/base, embedded corresponding source and all reports agree. A PR head SHA
alone is not the tested commit. Base-only edited events are not default triggers;
retargeting a stacked PR alone cannot be assumed to produce fresh CI.
See the [GitHub pull-request event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request).

Publication should use actual current develop after PR52 merges. If PR52 remains
open when the combined source is published, one stacked draft may explicitly
depend on PR52; after its merge, the combined candidate must be freshly reconciled
against actual develop and retested. Standalone or pre-retarget results cannot
silently become evidence for a different merge tree. These are verification
requirements, not assertions that publication, retargeting or CI has occurred.

The composition producer made no GitHub write, pull-request creation or CI trigger.
The standalone M04 checkpoint branch remains frozen. Fresh independent review,
remote tree equality, the actual publication base, exact-source hosted checks,
compiled-resource/source binding and inspection of actual new Android images are
required before broader technical acceptance. Draft publication, readiness, merge,
release and upgrade signing are separate decisions owned by the parent task.

## Final independent source review

The [fresh independent composition review](independent-review/README.md) finds no blocking defect for bounded source publication. Its complete source manifest SHA256 is `b02ad5fdcf6c687c11a27f56bc4614549f812dabcd537db47c1cda84a6f19827`. It independently executes 89 focused, 32 translation and nine optimized composition checks, verifies the producer aggregate of 660 passing methods, and rebuilds/inspects the font. Android compilation, 890 expected JVM identities and 112 planned render captures remain unrun. This is not a merge-ready or release conclusion.

## Local mirror provenance

[Mirror provenance](local-mirror-provenance.json) separates materialized immutable trees from commit objects available in each temporary clone. The standalone M04 commit/tree binding is independently verified on GitHub; local preservation checks use the exact tree and file hashes, not a substituted commit.
