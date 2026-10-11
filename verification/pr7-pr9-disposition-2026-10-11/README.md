# PR7 and PR9 implementation-branch disposition

11 October 2026. This is existing-PR cleanup while new localization work is paused.
It does not accept translations, complete reset rows, or reinstate withdrawn claims.

## Disposition supported by this evidence

The implemented changes in these two historical PRs are already represented in
accepted develop source, or superseded by the explicit current equivalents below.
The remaining branch-only material consists of withdrawn historical handoff records.
Their immutable objects are indexed below rather than copied into current source.
The appropriate PR disposition is **closed as superseded, not merged**, preserving
both original branches and their evidence. This report is the proof for that
disposition; GitHub's live state and the final PR comments record whether closure
has actually occurred.

- Accepted develop: `79b1f990a98eaf44c28351cd02c20157c70d8dff`, tree
  `e8e9d04caff79b29d4107d870841152d96242b10` (merged PR40).
- PR7: `730319aea40eb205d18c894c496e500d6f660ac6`, branch
  `translation/en-pt-it-el-tr`; develop merge base
  `b528c9d2a1eeb950143386154cedfcd38c4350af`.
- PR9: `a0afe1cfed363b65c3880c9875034b0460f811a2`, branch
  `translation/jeju-manchu-ainu-okinawan`; develop merge base
  `97e511dc63f1b2011300ce49fd1582b4de23ce3d`.
- Both old PRs still target `translation/complete-all-locales`. They are not
  being retargeted, merged, rebased, marked ready or used to overwrite develop.
- [PR15](https://github.com/c933103/AN-Paint/pull/15) merge
  `cfb592e9a47aee0a737fb49496f438689b719512` and
  [PR37](https://github.com/c933103/AN-Paint/pull/37) merge
  `699f3cb0d3e0fe932fbf39779f852c2b5e9dbf3c` are verified ancestors of this develop.

## Complete changed-path accounting

`full-pr-path-inventory.json` records every path returned by GitHub's paginated
changed-file API: 36 for PR7 and 87 for PR9, including nontranslation source,
tests, documentation and deleted resources. Each row retains the exact mode/blob
at the original head, its develop merge base and accepted develop.

PR7 has 34 paths changed after its common ancestor with develop; PR9 has 32.
The other 2/55 paths belong to the already-common source snapshot. Common
ancestry is not treated as linguistic acceptance, nor as proof that an old file
must remain unchanged forever. Current replacements relevant to this disposition
are explicitly accounted for below.

### Resource and application changes

- Fresh element-by-element comparison rederived **135 PR7 and 97 PR9 changed
  resource elements**, all equal to accepted develop. There are no removed keys
  in either merge-base-to-head resource delta. `current-scope-replay.json`
  records every path/key and both serialized-element SHA-256 hashes.
- All six axis-specific normalization sentences and their real dialog call sites
  are retained. Accepted commit
  [`f3528d0779ebe2ff6a4e8de202133c96c8764839`](https://github.com/c933103/AN-Paint/commit/f3528d0779ebe2ff6a4e8de202133c96c8764839)
  supplies the shared complete-sentence implementation. The current dialog differs
  from both old heads only by the later locale-aware numeric-input configuration
  from accepted commit
  [`a9b757704c077ac218f70d56e62549b64dff1505`](https://github.com/c933103/AN-Paint/commit/a9b757704c077ac218f70d56e62549b64dff1505).
  Both commits are verified develop ancestors. Reapplying old files would regress
  these newer numeric-input fixes.
- Older PR9 AppLanguage, vertical UI, catalogue registration and migration changes
  are in the common accepted history. Current source retains the Jeju alias and
  script-based Manchu handling described under the exact historical findings below.
- The old generic Portuguese catalogue and mistaken `cju` resource identity are
  not restored. Current canonical regional catalogues and the legacy `cju` to
  `jje` preference migration supersede those historical paths.

### Tests and document changes

- `tools/test_normalization_scope_pr7.py` and `test_normalization_scope_pr9.py`
  are byte-identical to the original heads and present through merged PR37.
- The old `tools/test_localization_repairs_pr7.py` and
  `tools/test_localization_repairs_pr9.py` filenames are absent from develop.
  Their assertions remain in `tools/test_translations.py`: the identical
  `validate_all(require_complete=False)` assertion, and
  `validate_catalogue(tag, require_complete=True)` for a superset including all
  twelve PR7 and five PR9 tags. This is structural/key-coverage equivalence, not
  semantic equivalence of translations. The fresh focused run executes these
  consolidated assertions along with the two retained normalization guards.
- `nonresource-inventory.json` covers all 15/20 post-common-ancestor nonresource
  paths: PR7 has 8 whole-file matches, 5 changed current equivalents and 2 archived
  branch-only files; PR9 has 13 matches, 5 changed equivalents and 2 archived files.
- `AGENTS.md`, the root README, shared action/source audits, shared caption/cursor
  evidence, PR7's mainstream/Himalayan handoff and all five PR9 language audits
  match their original-head blobs exactly where listed in that inventory.
- CI.md retains the reset warning and the correction from completed to scoped
  localization. Its additional current changes document later accepted build,
  instrumentation and compatibility work. TRANSLATING.md retains the reset,
  pending-independent-check wording and structural-only qualification; its newer
  source-file/export and Sinitic-convention guidance is preserved.
- Current translations/README.md retains its withdrawal wrapper, and immutable
  links to the shared-base and PR9-specific original histories. Its integration
  record supersedes the old branch-local inline history without accepting it.
  PR9's `verification/pr9-history-link-recheck-2026-10-06.md` is byte-identical.
- The old seven-line register pointer is superseded by the separate canonical
  [register](../localization-recheck-register.md). This pass changes no row or
  acceptance state. The canonical register's latest counts, rather than the older
  develop copy or historical comments, remain authoritative.

## Immutable withdrawn handoff archive

These are the only remaining branch-only nonresource files from the post-common-
ancestor delta. Each is headed **claims withdrawn**, requires full recheck of all
earlier progress/completion/repair/verification/no-defect assertions, links the
canonical register and encloses the earlier record in a withdrawn-history block.
The old catalogue and 20/22-test statements inside them are historical assertions,
not new results. Preserve the full file bytes and links; do not promote them into
accepted current documentation.

- [PR2 shared historical handoff at PR7 head](https://github.com/c933103/AN-Paint/blob/730319aea40eb205d18c894c496e500d6f660ac6/verification/localization-handoff-pr2.md),
  blob `b1a4262902bbd8c807a35a1fbcfcbff0fedfa037`. PR9 contains the same blob.
- [PR7 historical handoff](https://github.com/c933103/AN-Paint/blob/730319aea40eb205d18c894c496e500d6f660ac6/verification/localization-handoff-pr7.md),
  blob `9d9a16a41666497b6d4d1f7eade1e24eb49099b1`.
- [PR9 historical handoff](https://github.com/c933103/AN-Paint/blob/a0afe1cfed363b65c3880c9875034b0460f811a2/verification/localization-handoff-pr9.md),
  blob `864d9cb9128952cf1485cbb93931e06d6ccb84ee`.

The canonical register's archival supplement links these objects. No original
branch, object, PR discussion or test evidence is deleted by the disposition.

## Three historical Codex source findings

These are narrow code-review dispositions, separate from the still-pending
GH-018, GH-022 and GH-023 historical-reset obligations.

1. [PR7 duplicate pt-PT resources](https://github.com/c933103/AN-Paint/pull/7#discussion_r4079350287):
   current source has exactly one `values-b+pt+PT/strings.xml`; equivalent
   `values-pt-rPT` is absent. The fresh verifier also creates both configurations
   in an isolated fixture and confirms the current checker rejects the duplicate.
2. [PR9 stale cju test expectation](https://github.com/c933103/AN-Paint/pull/9#discussion_r4079424343):
   current AppLanguageTest uses `cju` only as an alias to `jje`, puts `jje` in
   `completeLowResourceTags`, and does not expect `cju` in starterTags. Fresh XML
   checks confirm one offered `jje`, no offered `cju`, and the alias mapping.
3. [PR9 Manchu vertical routing](https://github.com/c933103/AN-Paint/pull/9#discussion_r4079424347):
   VerticalText uses `locale.script == "Mong"` for VERTICAL_LR, LocaleTypography
   uses that script for the bundled Mongolian font, and AppLanguage delegates
   picker rows to VerticalUi.languageChoice, which handles Mongolian-script
   autonym columns. Current unit source explicitly checks `mnc-Mong` direction,
   shared font and the Manchu glyph; the picker test exercises its joined autonym.

The receipt-bound archived AppLanguageTest XML in accepted PR37 evidence has 19
passes, including the Jeju migration/catalogue and Manchu picker methods. The
fresh verifier checks its exact receipt/XML binding. It was executed at
`eab28203893ffba45f14a7f96df6d19cf4d19d3b`, not at today's develop. Its original
overall run failed for a separate API30 inventory problem; no run is relabelled.
No new Android, installed-device or native-language validation is claimed here.

The current old heads separately have exact-head clean Code reviews:
[PR7](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6050390585) and
[PR9](https://github.com/c933103/AN-Paint/pull/9#issuecomment-6050403820).
No new review request is necessary for this metadata/evidence-only disposition.
Resolving the three source-finding flags does not complete their reset rows or
grant broader language, runtime, history or original-discussion acceptance.

## Fresh execution and reproduction

The source tree above was materialized from the clean PR40 head
`1d000d7425696bb773cf0ead8048ea10d8b5cdbf`, whose complete tree is identical to
develop `79b1f990`. All **1,532 tracked file bytes** were independently checked
against their Git blob identities before execution. An initial incomplete
partial-clone materialization could not run the checks because catalogue files
were missing. That setup failure was corrected with the verified complete tree;
it is not treated as a source test failure or a pass.

- `verify_scope.py --history-repository <verified-history-checkout>` exits 0:
  135/97 element comparisons; 78/36 separate omitted-key negative controls;
  17 unique scoped catalogues with 694 translatable strings plus one plural;
  Portuguese duplicate rejection; Jeju registration; historical guard identity;
  and archived Android receipt integrity.
- `PYTHONPATH=tools python3 -m unittest test_normalization_scope_pr7
  test_normalization_scope_pr9 test_translations -v`: **34 passed**, no skips.
  Exact output is `current-focused-tests.log`.

Run those commands from an exact checkout of develop `79b1f990` with the named
original heads and merge bases available. The existing replay tool is at
`verification/pr7-pr9-recheck-2026-10-10/verify_scope.py`. It is read-only for
source/catalogues and uses isolated/mock negative controls. The result JSON's
inherited scope wording means this replay closes no additional acceptance row;
it does not undo the four already-completed canonical register rows.

## Acceptance remains independent

The canonical reset remains **475 rows: 3 completed structural rows + 1 completed
bounded R-005 distinction row + 471 pending**. Every P07/P09 language/history
obligation and GH-018/GH-022/GH-023 state is unchanged. The companion evidence
register is unchanged. Closing these obsolete implementation branches does not
close those tasks, revive rejected delivery claims, or authorize new translation
work while it is paused.
