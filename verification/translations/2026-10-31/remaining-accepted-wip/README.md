# WIP remaining accepted wording — 31 October 2026

Source branch: `wip/remaining-accepted-wording-20261031`; commit `3c0a0bb9ff49fc4394dd377cb5d9c3bd7c15ae19`, tree `ebec3b497c0d2d6b88ed95ed91079e058e2b556d`. Its temporary parent is PR245 head `0f802aa5d099fe0ff122755222966fbb85a549a0`, tree `bf1e145f0c509b632b635a77cc423141ace94d18`, not final develop. Final base sync must follow actual PR246/245 integration. No PR or merge-readiness claim is made by this preservation ref.

The exact remaining delta is 737 missing values plus two replacements in eight catalogues, disjoint from all 781 prior successor decisions. Only the authorized 739 XML identities changed; other resources remain identical to the temporary parent. Historical fixtures are preserved. Source doc `docs/remaining-accepted-wording.md` links the exact acceptance receipts and immutable ledgers. This does not republish or reroute the separately pending frozen 982-file archive.

## Passed focused checks

On the frozen source above, command:

```sh
PYTHONPATH=tools python3 -m unittest test_remaining_accepted_wording test_residual_parse_reuse test_current_localization_contracts test_exact_script_priority_wording test_breton_asturian_occitan_priority_wording test_swedish_remaining_p1_wording test_memory_warning_source_review test_language_option_additions_second test_language_option_additions_third test_animation_warning_title
```

Result: 102 tests passed, exit 0, 489.980 seconds. The captured output is `focused-normal.log`. Separate optimized checks passed for exact-script (28 tests) and parse-reuse (3 tests). These focused results are not a full host or Android acceptance.

Content-keyed parser reuse stores validated immutable tuples, rereads exact current bytes on every call and returns fresh mutable rows and attributes; scope checks and mocked loaders remain observable. Adversarial tests cover changed content with restored size/mtime, duplicate keys, caller mutation and monkeypatched loaders.

## Unfinished gates and next actions

- Synchronize against actual latest develop after the dependencies merge, preserving unrelated fixes and rechecking source/target disjointness.
- Freeze that final source, then run both complete normal and optimized host suites. Earlier diagnostic runs were intentionally stopped after known stale-fixture failures or to avoid executor contention; none is counted as passing final evidence.
- Compiled-resource/JVM, lint, APK and API35 checks are unrun for this candidate; new JVM tests in source are not executed outcomes.
- Publish a draft final-base PR, request exact-head Codex review, fix findings, pass required CI, merge only under the standing exact-head authorization, and verify the resulting develop state.

No release is requested or published. Wording review remains bounded independent model review, not native-human, installed-UI or whole-language certification.
