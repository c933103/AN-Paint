# P07-004 / P07-005 / P07-006: completed structural rechecks

Recorded 10 October 2026. These three narrowly worded requirements have been
independently rechecked against accepted develop
`80c14372b0504bc44f9f2809ad477247fdc8100b`, tree
`d9858229f98068bef9c6194c90d77610c5ecceec`. Their relevant implementation and tests
already exist on develop. Neither PR37's new guards/evidence nor its pending
Code review is a prerequisite for these existing structural facts.

Only these three authoritative register rows are completed. The register now
contains **475 rows: 3 completed structural rechecks and 472 pending rows**.
The companion evidence register is unchanged. Original PR7 and PR9 remain open;
Portuguese wording/clipboard review, other languages, menu routes and every
other reset obligation retain their separate status. No original review thread
is resolved by this record. PR37 remains unmerged and review-blocked; this record
does not grant it Code acceptance or reinterpret its evidence snapshot.

## Source and history binding

The original register was read again before this update: blob
`441b952db21c210d8bb06535ddcbae1637078a91`; unchanged companion blob
`47d736a334a9100d79e3dacab0026a7a994c3f23`. The working-register branch was
`review/localization-integration` at `280df39de10004d74e1b7af8edc6e1265ab71477`.
This documentation-only continuation preserves that branch's source; it does
not merge develop or PR37 into the historical integration branch.

The read-only probe exports and executes each snapshot's own resource validator:

| Context | Pinned revision |
| --- | --- |
| Original PR7 head | `730319aea40eb205d18c894c496e500d6f660ac6` |
| Integration source | `280df39de10004d74e1b7af8edc6e1265ab71477` |
| Accepted develop | `80c14372b0504bc44f9f2809ad477247fdc8100b`, exact tree `d9858229f98068bef9c6194c90d77610c5ecceec` |

Remote GitHub file/tree identities and local source bytes were independently
compared before running tests. Accepted develop has these exact Git blobs:

| File | Git blob |
| --- | --- |
| `Paintroid/src/main/res/values-b+pt+PT/strings.xml` | `8d3a7e50c288db7f9aa45d85edefb7b395e47952` |
| `Paintroid/src/main/res/values/app_language_names.xml` | `bc3a97c30f135065d240a045aab20f67d7e65440` |
| `Paintroid/src/main/res/xml/app_locales.xml` | `efacbcaeb4cb1d0caf12056fe5e4fed6463ff25e` |
| `tools/translation_catalogues.py` | `165f8ccebaeb268865548f80e77fcd81bdd850b5` |
| `tools/test_translations.py` | `ea68ce780f6ac52f9708ca35c6a07820f2f55386` |

The complete accepted resource subtree is
`2686a3f03f8515a93c43ff18bffe6ce732afe3ca`. The probe regenerates this manifest
from Git objects; source/results are not inferred from commit ancestry.

The original task distinguished European and Brazilian Portuguese. The original
[P1 finding](https://github.com/c933103/AN-Paint/pull/7#discussion_r4079350287)
identified the equivalent Portuguese resource directories. Its exact reviewed
commit was `f709df3dfb91054a6411d9e545af644899979b6a`; reinspection finds both XML
files and **170 overlapping resource names**. Their hashes and the shared-name
list hash are rederived in the JSON. The later
[8 October review](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6050390585)
reported no major issues at `730319aea4`; that is latest discussion context,
not inherited acceptance. The original P1 thread remains unresolved/outdated.

## P07-004: European Portuguese configuration identity

Original requirement: **Recheck European Portuguese configuration identity.**

In all three source snapshots, independent XML/validator inspection establishes:

- Exactly one canonical pt-PT catalogue: `values-b+pt+PT/strings.xml`.
- `pt-PT` occurs once in the application picker and once in Android's platform
  locale configuration. `pt-BR` separately occurs once in each.
- Bare `pt` is absent from offered picker/platform lists; its legacy preference
  alias points to `pt-PT`.
- Legacy `values-pt-rPT/strings.xml` and ambiguous `values-pt/strings.xml` are absent.
- Global resource-directory and catalogue validation report no clean-source errors.

The per-snapshot Portuguese XML hashes differ because later translation edits
exist. That difference does not change configuration identity and is not hidden
by an equivalence claim. This check accepts structural identity only, without
certifying European Portuguese wording.

**Disposition: full structural recheck completed.** See the identity fields in
all three contexts of [verified-results.json](verified-results.json).

## P07-005: duplicate configuration removal

Original requirement: **Recheck duplicate Portuguese configuration removal.**

The actual bad two-file state at reviewed commit `f709df3d` was inspected anew.
Commit `614f54a5dccfe806f5d8f9fc50d9f722da2f8d93` has exactly one path change:
deletion of `Paintroid/src/main/res/values-pt-rPT/strings.xml`. The probe checks
that deletion directly. Original-final, integration and accepted-develop
snapshots independently lack the duplicate while retaining the BCP-47 catalogue.

The applicable accepted-main [build job](https://github.com/c933103/AN-Paint/actions/runs/38018126008/job/114112885320)
succeeded, including universal APK resource compilation and test APK compilation.
Its exact run head is `80c14372`, without a PR37 merge ref. That actual successful
resource build complements the direct identity/absence checks; a historical
review or ancestor commit alone is not the completion evidence.

**Disposition: full structural recheck completed.** See `historical_finding`
and each context's canonical-directory/absence results. This does not close
other, broader review-reconciliation rows by proxy.

## P07-006: equivalent-qualifier guard

Original requirement: **Recheck the equivalent-qualifier guard and its relevant cases.**

The probe executes all six relevant cases separately against each snapshot's
actual normalization implementation:

| Pair | Required and observed result |
| --- | --- |
| `values-b+pt+PT` / `values-pt-rPT` | Equal |
| `values-b+id` / `values-in` | Equal |
| `values-b+he+IL-v21` / `values-iw-rIL-v21` | Equal |
| `values-fr` / `values-fr-night` | Distinct |
| `values-b+mn+Mong` / `values-b+mn+Cyrl+MN` | Distinct |
| `values-en-rUS` / `values-en-rGB` | Distinct |

Two independent temporary controls verify that global `validate_all` consumes
the configuration guard in each context:

1. Copy the snapshot's canonical Portuguese XML into the equivalent legacy
   directory. The only new error is the expected equivalent-directory collision.
2. Restore the actual Portuguese XML from the original reviewed bad commit.
   The same collision is detected in all three contexts. The integration/main
   validators also report sixteen literal-percent-format diagnostics in this
   deliberately restored obsolete fixture; the original validator reports no
   additional diagnostics. All are recorded individually in JSON. They are not
   present in the clean retained catalogues and are not silently discarded.

The original PR head's `TranslationCatalogueTests.test_canonical_catalogues_are_structurally_valid`
invokes global validation. Integration and accepted develop additionally contain
`AndroidResourceValidationTests.test_equivalent_locale_qualifiers_share_a_configuration`
with the six exact cases above. Both actual methods were independently executed
on the accepted-main bytes and passed; the full clean-main suite below also
executes them. This is assertion/behavior/execution evidence, not name matching.

**Disposition: full structural recheck completed.** Each equality/distinction
case, global clean result and negative-control result is recorded per context.

## Applicable execution evidence and limits

A clean temporary export of exact accepted tree `d9858229` was used, without
PR37 files or other workers' proposed tests. Recorded local commands/results:

```text
PYTHONPATH=tools python3 -m unittest \
  test_translations.AndroidResourceValidationTests.test_equivalent_locale_qualifiers_share_a_configuration \
  test_translations.TranslationCatalogueTests.test_canonical_catalogues_are_structurally_valid
Ran 2 tests in 1.003s — OK

python3 -m unittest discover -s tools -p 'test_*.py'
Ran 366 tests in 52.046s — OK (zero failures, errors or skips)
```

The source/input hashes above bind these recorded results. They do not claim a
fixed test count for future checkouts. Independent probe replay exactly matched
the initial accepted-main JSON; the published probe additionally records the
verified source-blob/resource-tree manifest.

[Main run 38018126008](https://github.com/c933103/AN-Paint/actions/runs/38018126008)
(attempt 1) has **overall conclusion failure**, despite successful APK build,
Python and JVM steps, and API35 job. Lint/native dependency and API30 stages
failed. This report does not turn that release run green, claim completed release
verification or accept unrelated app/runtime behavior. Those failures do not
negate the directly observed Portuguese identity/removal/qualifier results.

The regression artifact **11656814954** is independently bound to the same run
and head by live GitHub metadata. The already-downloaded ZIP was independently
SHA-256 checked against that metadata:
`7ca70a6a0ac3754d809eef345d06f58e3ba64c73b2963444bea7122fbf64e575`.
Its `build/reports/ci-phases/python.log` bytes were verified against the ZIP member
(SHA-256 `6bfacb94b066b169358654c9e8a61f0ef2af7b201cd5b0419e6f7ccea7cf3688`).
The actual log reports **366 discovered, 364 passed, two skipped**, in 66.304s.
Matching the 366 discovery IDs against its progress sequence identifies only
`test_adam7_fixture_pixels_match_independent_pillow_decoder` and
`test_export_opens_with_independent_pillow_ico_decoder` as skipped. Both are
optional Pillow independent-decoder checks; the two relevant translation
structural methods executed. Local clean-main discovery had Pillow and passed
all 366. This separates source coverage, actual CI execution and local execution.

The run's build artifact metadata names exact head `80c14372` and artifact
`11658095018`, digest
`59866bf7bc45aa45bca966b60cec135d458dcc7de82b916da5eed06567497e0c`.
The successful build-step conclusion is verified from GitHub; this report does
not claim an independent APK download, signing or binary-content audit.

## Reproduce the structural probe

Use a full clone, or unshallow an existing shallow clone first with
`git fetch --unshallow --no-tags origin`. The following live branch refs were
verified during this recheck; fetch them to obtain the pinned objects:

```sh
git fetch --no-tags origin \
  refs/heads/develop:refs/remotes/origin/develop \
  refs/heads/review/localization-integration:refs/remotes/origin/review/localization-integration \
  refs/heads/translation/en-pt-it-el-tr:refs/remotes/origin/translation/en-pt-it-el-tr
git cat-file -e 80c14372b0504bc44f9f2809ad477247fdc8100b^{commit}
git cat-file -e 280df39de10004d74e1b7af8edc6e1265ab71477^{commit}
git cat-file -e 730319aea40eb205d18c894c496e500d6f660ac6^{commit}
git cat-file -e f709df3dfb91054a6411d9e545af644899979b6a^{commit}
git cat-file -e 614f54a5dccfe806f5d8f9fc50d9f722da2f8d93^{commit}
python3 verification/p07-structural-recheck-2026-10-10/verify_portuguese_structure.py \
  > /tmp/p07-structural-results.json
cmp /tmp/p07-structural-results.json \
  verification/p07-structural-recheck-2026-10-10/verified-results.json
```

`origin` must be the AN Paint repository. If future rewriting removes a pinned
object, stop rather than substitute a different revision. Separate full local
object stores can be supplied via `--history-repository` and
`--current-repository`; both are read-only. The latter supplies accepted-main
objects, not an assertion about that checkout's working files. The probe exports
only named Git content into temporary directories and never modifies resources,
source checkouts, Git refs or authoritative statuses.
