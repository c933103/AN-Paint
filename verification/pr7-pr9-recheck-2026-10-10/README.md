# PR7 / PR9 bounded normalization and reset recheck

Date: 10 October 2026. Original resource/Android evidence base:
`eab28203893ffba45f14a7f96df6d19cf4d19d3b`, tree
`537185be479023d1567ab583d808ffaa7a4d3db8`. The candidate now incorporates
current develop `80c14372b0504bc44f9f2809ad477247fdc8100b` (PR36), including
its SDK-aware inventory fixes. The host log below was rerun on that integrated
checkout with the receipt-validation repair; the archived Android XML remains
explicitly historical exact-eab2820 evidence.

This continuation adds the two missing normalization-resource scope tests to the
current source. It preserves all current translations, app behavior and numeric
input fixes. It does not transplant the old PR branches or reinstate withdrawn
translation conclusions. PR7 and PR9 remain subject to their individual reset
obligations. Their descriptions and three unresolved review threads are unchanged.

## Concrete changes and independently replayed results

- `tools/test_normalization_scope_pr7.py` is byte-identical to the file at PR7
  head `730319aea40eb205d18c894c496e500d6f660ac6`.
- `tools/test_normalization_scope_pr9.py` is byte-identical to the file at PR9
  head `a0afe1cfed363b65c3880c9875034b0460f811a2`.
- Each test requires the six width/height normalization intro, information and
  percentage-input resources in the default XML and each scoped canonical XML.
  These are presence guards, not meaning, rendering or numeric-input tests.
- Both guards pass. Removing each required key individually from each locale
  read and from the default read makes the corresponding guard fail:
  PR7 has 78 negative controls; PR9 has 36. All 114 are recorded individually.
- Full Python discovery on the recorded repair snapshot passed **371 tests**, zero failures,
  errors or skips. The regenerated `host-tests.log` includes PR36's eight added
  test methods and this repair's three receipt-validation methods. It includes
  intentional failure diagnostics from runner tests; its unittest result is
  `OK`. The original eab2820-based candidate had 360 tests; that earlier count
  is not presented as the integrated checkout's result. The original focused
  subsets passed 32 translation tests, eight localized-help tests and both guards.
- The existing Android workflow already discovers `tools/test_*.py`. No workflow
  edit, new bypass or reduced gate is needed for these guards.
- Fresh serialized-element comparisons confirm all **135** historical PR7
  changed resource elements and all **97** PR9 elements equal current source.
  No removed resource keys occur in those baseline-to-head comparisons. Each
  element's two SHA-256 hashes is included in `source-results.json`. This proves
  retention of those specific deltas, not every earlier translation claim.
- All **17** scoped catalogues independently validate against the current
  **691 translatable strings and one plural**. Each is registered exactly once;
  each catalogue's path/hash/counts/missing-key results are recorded separately.
  The old final replies' 669-string counts describe an older snapshot.
- Current pt-PT uses exactly one `values-b+pt+PT/strings.xml` catalogue.
  `values-pt-rPT` is equivalent but absent. A fresh fixture containing both
  directories is rejected by the current global duplicate-configuration checker.
  The historical final PR7 reply's `values-pt-rPT` statement must not be repeated
  as a description of current source.

## Exact-base Android evidence and limits

`AppLanguageTest-eab2820.xml` is copied byte-for-byte from regression artifact
`11654898336` in [release run 38013637833](https://github.com/c933103/AN-Paint/actions/runs/38013637833).
The downloaded ZIP's SHA-256 was independently checked against live GitHub
artifact metadata: `8834a80a9d7fb6bb34ad66cefe662e04d3daf6262183bd70679d4229bca0a21a`.
See `ci-receipt.json` for the artifact/run/head binding.

The XML contains 19 passed tests, zero failures, errors or skipped tests. The
following exact cases were inspected against their current source assertions:

- `regionalLabelsLegacyMigrationsAndStarterChoicesUseTheirCatalogues`: tests
  `cju` only as a legacy preference alias to `jje`; the completed low-resource
  list contains `jje`, `mnc-Mong`, `ryu`, `ain-Kana`, `ain-Latn`. Current XML
  registration is checked separately: `jje` occurs once and `cju` is absent.
  This class-level case uses Robolectric API30; a different Hakka-only API33
  migration case is not evidence for the Jeju platform-backend alias.
- `manchuPickerUsesItsOwnJoinedVerticalAutonym`: invokes the picker helper with
  `mnc-Mong`. The helper checks the actual name/code, adjacent vertical columns,
  no ellipsis, mounted-row fit, and radio alignment, then renders a bitmap.
  It does not certify glyph coverage of the complete Manchu catalogue or every
  installed-device control/orientation.

The recorded run's overall conclusion is **failure**, caused by the separate
API30 source-inventory mismatch corrected by the now-merged PR36. We do not relabel
that run green. The copied XML is exact-base unit evidence, not a new candidate
CI run, new installed-device test execution, or linguistic certification.
PR18's separately owned installed vertical matrix remains separate work.

## Individual reset dispositions

[`dispositions.tsv`](dispositions.tsv) contains one row for each of:

- P07-001 through P07-016 (16 rows)
- P09-001 through P09-023 (23 rows)
- CAT-032 through CAT-043 and CAT-048 through CAT-052 (17 rows)
- GH-018, GH-022, GH-023, TY-002, R-019 and DOC-006 (six related rows)

Every row separates the original requirement, unchanged acceptance status,
fresh bounded finding, evidence and specific remaining work. **All 62 acceptance
statuses remain pending full recheck.** This is an evidence supplement, not a new
authoritative reset register. Unlisted shared claims also remain subject to the
original register's unlisted-claim rule.

The exact integration-branch register contents were fetched before this work:

- `verification/localization-recheck-register.md`, Git blob
  `441b952db21c210d8bb06535ddcbae1637078a91`
- `verification/localization-evidence-rechecks.md`, Git blob
  `47d736a334a9100d79e3dacab0026a7a994c3f23`

These match the source-base copies. Neither register was edited.

### History recovered, and what is still missing

The original PR7 discussion's user scope (22 September 07:08 UTC), and its
23 September 05:24 UTC final visible reply were recovered directly. The final
reply lists seven English variants plus pt-PT, pt-BR, Italian, Greek and Turkish.
It claims completion and a particular Portuguese path; both are historical
claims subject to the reset. The original default-note intermediate search hit
could not be read as an exact message. The public withdrawn handoff is not a
substitute for that missing original.

The original PR9 discussion's five-catalogue request (22 September 06:11 UTC)
and 23 September 08:53 UTC final visible reply were recovered directly. The
final reply's newline/transliteration repairs and fully-green statement remain
claims to recheck. A search excerpt contains the original 625/669 complete,
44 remaining progress statement, but exact-message retrieval reports unavailable.
It therefore remains unverified as a full historical-count disposition.

The final visible replies have no later messages in their returned leaf context.
That does not prove every intermediate message, alternate branch, later
integration correction or outside-review finding was recovered. Private
conversation contents/links are not copied into this public evidence bundle.

### Remaining work is substantive

PR7 still needs original default-note deferral reconciliation, full regional
English review, Brazilian Portuguese rewrite and clipboard-context recheck,
Italian/Greek/Turkish semantic coverage, and every complete menu-route claim.

PR9 still needs independent Jeju clause/predicate/memory review, complete Ainu
Latin/Kana source-assisted and paired-script review (including file count versus
size and Select all placement), Manchu lexical/Unicode/newline/transliteration
and complete-text glyph recheck, and Okinawan full/short-action/polygon/caption
review. Existing audit documents are withdrawn inputs. No sentence is declared
correct merely because it uses the expected script or survives a structural test.

Do not close or merge the original reset-scoped PRs merely because their resource
deltas are retained. This bounded test/evidence continuation can be reviewed and
validated separately from the outstanding language acceptance work.

## Evidence index used by individual rows

- **R1:** the unchanged main and companion reset registers listed above.
- **H1/H2:** original PR7/PR9 history recovery described above, including exact
  retrieval limitations. These sources establish scope/history only.
- **S1:** `Paintroid/src/main/res/values/strings.xml` (`language20_translation_note`),
  `AppLanguage.showPicker`, `TRANSLATING.md`, and `tools/translation_catalogues.py`.
- **S2:** `source-results.json` → `catalogues` and `source_counts`, independently
  generated from current XML, picker registration and completeness validation.
- **S3:** `source-results.json` → `portuguese_configuration`; current
  `resource_configuration`/`validate_resource_directories` and their fixture.
- **S4:** `source-results.json` → `historical_resource_deltas`, explicitly naming
  baselines, old heads, keys and full serialized-element hashes.
- **S5:** pt-BR `ui_estimates_include_the_current_canvas_and_clipboard_sampled`
  in `values-pt-rBR/strings.xml`; presence is not a complete terminology review.
- **S6:** `app_language_tags.xml`, alias arrays in `app_language_names.xml`,
  `AppLanguage.selectedTag`, current `AppLanguageTest.kt`, and JSON registration.
- **S7:** `VerticalText.uiDirection` is script-based (`Mong` → `VERTICAL_LR`),
  `LocaleTypography` supplies the Mong font and `AppLanguage.showPicker` delegates
  each row to `VerticalUi.languageChoice`.
- **T1:** `host-tests.log`, recorded 371-test repair-snapshot discovery including the 32 translation and
  eight localized-help cases. This is host execution only.
- **T2:** two original guard files plus the individually recorded 114 missing-key
  negative controls in `source-results.json`.
- **T3:** copied exact-base XML, `ci-receipt.json` and current test-source review.
- **J1:** `translations/JEJU_GRAMMAR_REVIEW.md`, a withdrawn historical input.
- **A1:** `translations/AINU_SEMANTIC_AUDIT.md`, a withdrawn historical input.
- **M1:** `translations/MANCHU_SEMANTIC_AUDIT.md` and
  `MANCHU_COLOUR_TYPOGRAPHY_AUDIT.md`, withdrawn historical inputs.
- **O1:** `translations/OKINAWAN_GRAMMAR_REVIEW.md`, a withdrawn historical input.
- **G1:** [PR7 original Portuguese finding](https://github.com/c933103/AN-Paint/pull/7#discussion_r4079350287).
- **G2:** [PR9 original stale-cju finding](https://github.com/c933103/AN-Paint/pull/9#discussion_r4079424343).
- **G3:** [PR9 original Manchu vertical finding](https://github.com/c933103/AN-Paint/pull/9#discussion_r4079424347).

## Reproduce

From this source checkout, run:

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 verification/pr7-pr9-recheck-2026-10-10/verify_scope.py
git diff --check
```

The verifier needs the named old commit objects. Use a full clone, or first
unshallow an existing shallow checkout with `git fetch --unshallow --no-tags origin`.
The following original branch refs were verified on GitHub during this recheck;
fetch them into the history checkout before invoking the verifier:

```sh
git fetch --no-tags origin \
  refs/heads/translation/en-pt-it-el-tr:refs/remotes/origin/translation/en-pt-it-el-tr \
  refs/heads/translation/jeju-manchu-ainu-okinawan:refs/remotes/origin/translation/jeju-manchu-ainu-okinawan
git cat-file -e 730319aea40eb205d18c894c496e500d6f660ac6:tools/test_normalization_scope_pr7.py
git cat-file -e a0afe1cfed363b65c3880c9875034b0460f811a2:tools/test_normalization_scope_pr9.py
git cat-file -e b528c9d2a1eeb950143386154cedfcd38c4350af^{commit}
git cat-file -e 97e511dc63f1b2011300ce49fd1582b4de23ce3d^{commit}
```

Here `origin` must be the AN Paint GitHub repository. If a later history rewrite
removes one of these objects, the checks must stop rather than substitute another
baseline. A second full local checkout holding the verified objects can instead
be supplied with `--history-repository /path/to/checkout`; that option is read-only.
The verifier compares those historical objects with current working XML,
verifies guard identity, tests omission sensitivity, checks current catalogue
identity/structure and inspects the archived exact-base XML. A later replay
reports its current file hashes rather than declaring them the recorded base.
It performs no network calls or Android execution and changes no resource files.

## Receipt integrity follow-up

The delayed exact-head review of the first candidate correctly found that the
verifier originally assigned the recorded base to the XML result without reading
the receipt. The original archive had been externally downloaded and checked,
but that relationship was not enforced by the replay script.

The repaired verifier now validates the receipt's source base, GitHub run URL,
artifact ID/digest, workflow run/repository/head identity, and exact XML archive
member. The XML SHA-256 is bound to the receipt and to the independently verified
archive's pinned extracted-file hash. Substituting both XML and its receipt hash
therefore also fails. The emitted head comes from the validated artifact receipt.
This is offline integrity checking of that recorded evidence, not a fresh GitHub
query or a new Android execution.

`tools/test_pr7_pr9_evidence_receipt.py` is included in ordinary CI discovery.
It checks valid evidence, separately rejects edits to twelve identity/binding
fields, and rejects changed XML both with and without a changed receipt hash.
The three test methods exercise fourteen negative cases. Original catalogue
results, original guard bytes and reset acceptance statuses remain unchanged.

## Integrated host-log correction

The subsequent exact-head review correctly identified that the original bundled
360-test log did not cover the eight host methods added by PR36. The log has
been regenerated from the recorded repair snapshot on parent
`2bff92308143e2fb9e9711e6e309bd5d700cf18f` plus the three executable/input
changes identified below. That run passed 371 methods, including the eight PR36
checks and all three new receipt tests. All other test/implementation/resource
files are identical to that parent. README, regenerated source-results and host
log changes are evidence documentation. This is an immutable recorded result,
not a claim about the test count of any later checkout.

| Changed test source/input | Git blob SHA |
| --- | --- |
| `tools/test_pr7_pr9_evidence_receipt.py` | `30852224a2f109ace267b947bac5218c90ce1d56` |
| `verification/pr7-pr9-recheck-2026-10-10/verify_scope.py` | `f33baad8d880a90ef23b169e3426ab2d065d5436` |
| `verification/pr7-pr9-recheck-2026-10-10/ci-receipt.json` | `a8b7d5c733397671b1aca709ff8f43764673beab` |

The exact discovery command and this source/input manifest are also in the log.
Python and optional Pillow versions are recorded in the log. CI may omit Pillow
and report its two independent-decoder tests as skipped; a CI skip must be
reported as such rather than relabelled as a pass.
