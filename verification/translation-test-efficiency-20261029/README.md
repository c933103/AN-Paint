# AN Paint: translation-test duplication, bounded read-only inventory

## Finding

There is substantial repeated test/oracle code, not just a large legitimate test set. A one-item wording correction should not normally require cloning another Python oracle, Kotlin oracle and complete per-language test package. Consolidation can preserve every accepted value and negative control; it need not weaken consumer behavior checks. No source, test, fixture, workflow or acceptance policy was changed in this inventory.

## Source boundary and counts

The full inventory reads Git blobs at **b05a4463e03683f92c2b3ebe21905e0420362a42**, tree **0f5961b48f686b0c04748517e095eaa349cfa0a0**. Current develop subsequently became **2cb90dbd7a7060978b90498a61f7bc285ad66a25**, tree **dc3443a88702500716f852dc9131c559d745a95d**: exactly the already-reviewed #227 six-file delta on b05a. Current counts below apply that known delta, not another full historical rebuild. Unadopted #226 is separate and **not in develop**.

| Measure | Inspected b05a | Current develop, known #227 delta |
|---|---:|---:|
| Top-level `tools/test_*.py` files | 232 | 233 |
| Literal Python class `test_` methods | 1,951 | 1,959 |
| Executed full host cases | 2,023 verified | 2,031 verified |
| Current-localization fixture files | 132 | 133 |
| Fixture bytes | 17,745,892 | 17,749,077 |
| Paintroid JVM test classes | 194 | 195 |
| Literal JVM `@Test` methods | 1,571 | 1,575 |
| Executed JVM cases | 1,933 verified | 1,937 verified |

Current #227 counts are bound to artifact 12883209167 (84,702,424 bytes), SHA256 `56ad9a8c01636c6d62be361ee37cb2bce284a48fdaa1817b66acb436089f97c1`; hosted Python 2,031 / 1,207.820 s passed with two documented skips, JVM 1,937 / 195 suites passed. Its four new Indonesian consumer methods total only 0.170 s. The compact terminal receipt is [preserved here](https://github.com/c933103/AN-Paint/blob/6d9a887ae860963325ca4e384fb8c47569fc3b4d/verification/indonesian-context-followthrough-20261029/terminal-receipt-compact.json).

Literal and executed counts differ: Python has dynamically generated methods; Robolectric repeats some methods across SDKs. For example `UiTypographyContextTest` has five source methods and twenty executed cases. These are not translation-completion or linguistic-quality totals. App/native instrumentation is a different layer and is not included in these source-count tables.

The **explicit name-classified b05a priority/wording slice** contains 86 Python test files / 832 literal methods, 41 support modules, and 60 JVM classes / 576 executed cases. A broader translation/locale-name slice contains 160 Python test files / 1,307 literal methods, 50 support modules, and 103 JVM classes / 1,022 executed cases. That broader slice includes genuinely distinct routing/layout/consumer behavior and is **not a count of redundant tests**. `translation-test-inventory.json` records every path, classification rule and method count so this boundary is inspectable rather than presented as an exhaustive semantic classification.

## Concrete repeated families

1. **The immediate #225/#227 finite-fixture pair.** `ordinary_priority_expectations.py` and `indonesian_crop_expectations.py` are 110 lines, byte-identical after only one fixture filename, its SHA256 and one docstring sentence are substituted. Their 39-line Kotlin counterparts differ only in filename/hash, object name, description and assertion label. No whitespace or broad normalization was needed. `ordinary-indonesian-clone-proof.json` records the exact substitutions and source hashes. #227 changes one XML item but adds 507 lines across six files: 506 non-production lines plus the replacement XML line. It adds eight Python and four JVM methods.
2. **Assembly Help:** sixteen locale-specific modules share identical AST bodies for setup, corruption helper, complete eight-paragraph comparison, paragraph omission/duplication/reorder, and resource-shape checks. Examples: `test_dutch_assembly_help.py`, `test_brazilian_portuguese_assembly_help.py`, `test_cantonese_assembly_help.py`. Locale-specific accepted texts, sentence segmentation, caption quoting and route punctuation remain different data/contracts—not redundant language coverage.
3. **Priority cohort validators:** eight modules (Basque/Frisian/Uzbek; Cebuano/Low German/Kashubian; Chhattisgarhi/Yiddish/Hong Kong; Kazakh/Tajik/Pashto; Sindhi/Pidgin/Tok Pisin; Sorani/Uyghur/Tatar; Tibetan/Dzongkha/Valencian; Walloon/Northern Sami/Sanskrit) duplicate exact function ASTs for fixture binding, resource shape, edited-resource and catalogue validation. Seven other cohort helpers duplicate `current_row` logic. Nine normalization-scope modules repeat the same six-message catalogue check.

The clone inventory preserves names and constants; it removes only AST source locations and function docstrings. Same code operating on different accepted data is a consolidation opportunity, **not permission to remove those rows or corruption cases**.

## Distinct behavior to retain

- Raw XML complete values, quantity sets, attributes, predecessor/source bindings, held fallbacks and independent fixture corruption checks are different from Android-compiled runtime resolution.
- Actual quantity selection, alias resolution and unsupported-resource fallback; layout/direction/vertical-script routing and accessible/native input behavior; crop attachment movement and apply/undo; resident-memory rejection and real warning/chooser state are meaningful consumer contracts.
- #227's actual apply/undo coverage adds value. Its finite typed oracle need not be reimplemented to obtain that coverage.
- Existing `test_crop_movement_translations.py` already demonstrates a data-driven complete plural-form table for Lithuanian, Arabic, Russian and Japanese. It is an example of organization, not a substitute for stronger current fixture/source/structure guards.

## Costs established by existing evidence—not guessed savings

Actual b05a natural-run regression artifact **12882793690**, run **40836724809**, SHA256 **6bd174a13c1ca3598b95274b8bb843025698fd9bad1d1285422016c8f772ad93**:

- Full Python: 2,023 cases / **1,268.928 s**, two documented skips.
- JVM: 1,933 cases / 194 classes, zero failures/errors/skips; **1,162.687 s phase wall time**. XML suite-time sum **947.592 s**.
- The named priority/wording slice sums **286.146 s** across 60 classes/576 cases; the broader translation/locale slice sums **490.677 s** across 103 classes/1,022 cases. These are suite-time sums, not additive wall-time savings available by deleting tests.
- #225's eight new JVM methods take only **0.699 s** in this natural artifact (**0.585 s** suite time in its accepted premerge artifact). Therefore the cloned scaffolding/review burden is demonstrated, but these eight methods are **not** demonstrated as the dominant runtime cost.
- Existing Python receipts contain whole-suite timing, not trustworthy per-method durations. No claim is made that any particular Python clone family consumes a measured share of the twenty-minute run.

That natural run's first attempt failed device-evidence collection separately; the successful regression artifact does not turn that whole attempt into a pass. Its later authorized failed-job recovery succeeded and remains a separately labelled attempt. Repeated full verification and bespoke review packages amplify effort even where marginal test execution is small.

#226 added 497 lines across seven files, including twelve host controls, for a two-fork/observer experiment. Its exact 1,933-case run took 969.688 s versus #225's comparable premerge one-fork observation of 968.815 s; different runs are not controlled speedup evidence. The experiment is unadopted and must not be sold as a successful speed fix.

## One small consolidation proposal, not another framework

**Only the current #225/#227 Python helper clone family first.** Extract their byte-identical, stateless typed-value/resource-shape functions (`_same_type_and_value`, `_blank`, `typed`, `_resource_map`) into one shared implementation. Keep the existing small fixture-specific entry modules and their public call surfaces. Crucially, retain each module's `FIXTURE`, digest and `_baseline` cache/clear behavior: both existing negative suites deliberately patch `FIXTURE` and clear `_baseline`, so a new captured-path/cache abstraction could silently weaken them.

Keep both JSON fixtures byte-exact with their existing digests, all accepted source/previous/target/display/attribute values, every current positive/negative case, and every JVM consumer assertion. Reuse the existing two test packages; do not add another generic gate suite. Do not alter Kotlin consumer behavior, JVM class layout, timeouts, CI or release. The Kotlin 39-line clone and other families are observations for later review, not this first change.

Before any edit, parent reviews the small extraction boundary. Afterwards the review must map old functions/callers to the common implementation and show no data/control loss. This proposal claims maintainability reduction only; no unmeasured runtime saving. Any change to when normal/optimized modes are required needs separate reviewed policy clarification—this inventory does not waive them.

## Policy references

At the inspected current experiment source, [CI.md lines49–62](https://github.com/c933103/AN-Paint/blob/d8f1840ac60ec9c2134f6a01439fac35433d349c/CI.md#L49-L62) lists both full local modes and makes the workflow canonical; [android.yml lines80–87](https://github.com/c933103/AN-Paint/blob/d8f1840ac60ec9c2134f6a01439fac35433d349c/.github/workflows/android.yml#L80-L87) executes normal Python and full JVM. [AGENTS.md7–16](https://github.com/c933103/AN-Paint/blob/d8f1840ac60ec9c2134f6a01439fac35433d349c/AGENTS.md#L7-L16) requires relevant checks and cautions against repeating the whole suite without a diagnosed reason. The proposed extra host-modes workflow remains unpublished and is not part of this consolidation.
