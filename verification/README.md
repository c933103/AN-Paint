# Verification records

Routine CI tests current behavior and compact product fixtures. Historical raw
logs, captures, source snapshots, inverse adapters and one-time preservation
checks live outside the active application tree.

## Immutable archive

The complete pre-migration checkout, including every removed verification file,
is preserved at commit
[04b128889a4ff9159f199d1737bd07d41e22162d](https://github.com/c933103/AN-Paint/tree/04b128889a4ff9159f199d1737bd07d41e22162d),
reachable through `archive/pr55-before-evidence-migration-20261012`.
The [old handoff](https://github.com/c933103/AN-Paint/blob/04b128889a4ff9159f199d1737bd07d41e22162d/HANDOFF.md)
and [old CI history](https://github.com/c933103/AN-Paint/blob/04b128889a4ff9159f199d1737bd07d41e22162d/CI.md)
retain their original claims and limits; archiving them grants no new acceptance.

Distinct PR55 failure checkpoints:
- [Original advance-guard failure](https://github.com/c933103/AN-Paint/tree/946e5378cf3f75a8047dc42a46a3b3dbe62c9327/verification/commons-metadata-m04-pr55-initial-ci-2026-10-12).
- [Ainu diagnostic advance/painted-ink mismatch](https://github.com/c933103/AN-Paint/tree/746d41107b8251d2b288a62931da5c1e80810b08/verification/commons-metadata-m04-pr55-diagnostic-ci-2026-10-12).
- [Arabic strict-ink failure](https://github.com/c933103/AN-Paint/tree/04b128889a4ff9159f199d1737bd07d41e22162d/verification/commons-metadata-m04-glyph-bounds-2026-10-12/failed-painted-ink-run).
- [Compiler failure and installed same-height failure](https://github.com/c933103/AN-Paint/tree/94b91c4eb04d856853e29bdf7c90c61d52405bff/verification/commons-metadata-m04-glyph-bounds-ci-2026-10-12).
- [Natural-relayout authoring review](https://github.com/c933103/AN-Paint/tree/82bd9bc0e8e4c7a47784fa157a22e2bd9b52c72c/verification/commons-metadata-m04-status-remeasure-2026-10-12).

[Full immutable04 CI review, raw receipts and pixel disposition](https://github.com/c933103/AN-Paint/tree/8a7dd2b59b491e8fc401072a9d8dd0d93f6aee17/verification/commons-metadata-m04-natural-relayout-ci-2026-10-12).

The subsequent [04 source run](https://github.com/c933103/AN-Paint/actions/runs/38269993000)
executed 892 JVM identities: 891 passed; the mixed-paragraph Arabic reset failed
its exact-alpha guard. All 112 original render pairs passed. Its 155/181 ink
triplets and 60/72 mutation controls are incomplete, not a complete pass. The
reviewed difference consists of two antialias fringe samples (alpha 7 and 1),
with no demonstrated glyph, mark or line loss; this is a specific disposition,
not a universal pixel tolerance. API30's 95 and API35's 104 scheduled installed
methods passed, including both Arabic natural-update/full-raster checks.

## Language-option evidence

The accepted language-option records remain reachable at immutable develop
[484d1b31](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834):
- [Six-option registration and review](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834/verification/language-options-2026-10-12).
- [Twenty-one concrete identities and principal-variety decision](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834/verification/language-options-second-2026-10-12).
- [Superseded unpublished 162-choice candidate](https://github.com/c933103/AN-Paint/tree/484d1b31cb113c88351e6d0dbdaa0d503e5dd834/verification/language-options-superseded-162-2026-10-12).
These records do not certify translated UI or current runtime behavior. The
compact identity/status fixtures and explicit 59-scoped/112-fallback contract
remain active; routine CI does not require the historical files.

## Files intentionally retained here

- `legacy-font-metadata.json`: licensing/provenance input cited by the packaged
  asset notices and font licence review.
- `releases/request.json` and its selected version's signing patch/notes:
  operational inputs to the separately authorized release publisher. The patch
  contains public signatures and copy ranges, never the private signing key.

New raw evidence belongs in CI artifacts or a dedicated evidence ref, with a
short exact-source summary linked from the relevant PR. Normal CI must not
fetch or reconstruct the historical archive.


## Active priority contracts versus historical review bookkeeping

The following staged records describe their own immutable source revisions.
The family-wide catalogue retirement below supersedes their statements about
which copied wording fixtures remain active; it does not change their evidence.

The eight per-locale priority cohorts (Basque/Frisian/Uzbek; Cebuano/Low German/
Kashubian; Chhattisgarhi/Yiddish/Hong Kong Chinese; Kazakh/Tajik/Pashto;
Sindhi/Nigerian Pidgin/Tok Pisin; Sorani/Uyghur/Tatar; Tibetan/Dzongkha/Valencian;
Walloon/Northern Sami/Sanskrit) retain current expected resources, not a second
live copy of every historical review disposition.

Original 24 fixtures remain recoverable at immutable commit
[`f3d617d0`](https://github.com/c933103/AN-Paint/tree/f3d617d0ec83dcab20d9fd5287272207c17c8d51/tools/fixtures/current_localization),
under the same family directories and locale filenames. No historical archive is
fetched or reconstructed by CI, and no second 6 MB archive is added here.

| Responsibility | Active coverage / archival disposition |
| --- | --- |
| Historical 8,184 `priority_rows` tier/decision records | Archived above; 6,178 edited values, 1,801 retained values and 205 absences map exactly to retained `values`, `original_catalogue` and held-absence contracts. All present historical value/attribute fields match those retained contracts. |
| Accepted current wording, source, attributes, quantities, aliases and display | Every remaining fixture field is unchanged. All 6,451 edited-resource positive checks, retained-resource checks, complete compiled-value/formatting checks remain; distinct real consumer behavior is preserved as mapped below. |
| Generic missing/text/attribute rejection | Each locale's string/plural and current-successor validation paths are exercised once: 54 representatives / 162 negative probes instead of 19,353 copies of the same three probes. This does not sample the positive wording checks. |
| Fixture tampering | Existing coordinated fixture/target and source/predecessor corruption tests still reject altered fixture data through the shared digest validator. Eight repeated historical-disposition mutation methods are removed. |
| Structural and special behavior | Existing duplicate/root/nested-child/plural-quantity/tail checks and finite successor, script, sampled-warning and option-specific cases are retained. |

The 24 active fixture payloads shrink from 6,051,757 to 4,333,287 bytes by removing
historical disposition duplication, not by minifying previously formatted data.
This is a bounded reduction in active data and redundant test work, not a claim
that the broader translation/test expansion has been resolved. Required CI and
all app behavior remain unchanged; measured affected-run timings belong in the
exact-source PR evidence, not an unqualified speedup claim.


### Repeated animation integration checks

The six removed instances of
`realAnimationWarningsHandleArbitraryAndLowerBoundCountsAndCancelWithoutImporting`
are in `CebuanoLowGermanKashubianPriorityWordingTest`,
`ChhattisgarhiYiddishHongKongPriorityWordingTest`,
`KazakhTajikPashtoPriorityWordingTest`,
`SindhiNigerianPidginTokPisinPriorityWordingTest`,
`TibetanDzongkhaValencianPriorityWordingTest` and
`WalloonNorthernSamiSanskritPriorityWordingTest`. Their bodies are identical to
the surviving Basque/Frisian/Uzbek (LTR) and Sorani/Uyghur/Tatar (RTL) instances.

- All 24 locales retain complete compiled checks for `formats22_at_least_frames`,
  `formats22_animation_message`, `formats22_animation_still`,
  `formats22_animation_title` and `formats22_open_still`, including typed `ui()`
  formatting arguments. The source fixtures and every accepted value are intact.
- The two representative methods retain the actual scanner, thread worker,
  arbitrary exact counts 2/21 and lower-bound count 21, complete dialog text,
  no selection before a decision, cancellation, staged-file deletion and worker
  shutdown. Removing six repeated instances avoids 54 dialog/scanner executions.
- `ImportSelectionTitleTest` independently retains exact GIF/WebP, capped/lower-
  bound GIF, APNG poster/default-image distinctions, uncertain 0/1 states,
  cancellation/dismissal, selected-file ownership transfer, single confirmation,
  queued-disposal and default/fallback/localized consumer behavior.
- These removed methods had no clipping, geometry or screenshot assertions. No
  rendered-layout coverage is claimed. Five non-identical cohort variants and
  all other product/locale tests are untouched.


## Retiring translation approval-history machinery (seven priority cohorts)

Canonical Android XML now owns current wording for Marathi/Tamil/Telugu,
Nepali/Punjabi, Hausa/Igbo/Lingala, Yoruba/Zulu/Xhosa, Kannada/Malayalam/Filipino,
Javanese/Sundanese/Kyrgyz and Assamese/Khmer/Lao. This does **not** certify
linguistic correctness or establish new translation acceptance.

The seven `tools/fixtures/current_localization/*_priority_wording.json` mirrors,
matching Python expectation/read-only review-test modules and matching Kotlin
cohort classes are recoverable at commit
`0acbc50da25a7ef3b4b55de0a6b25290e60f9fe8`, unchanged paths. All 28 removed
file blob identities were checked against that immutable remote tree. No archive
payload is copied into the active tree.

| Removed responsibility | Current responsibility / reason for retirement |
| --- | --- |
| 65 cohort Python methods enforcing accepted copies, changed/retained partitions, predecessor text, edit counts and priority statuses | Review and source history preserve prior decisions. These are intentionally no longer active text-freeze rules. Current catalogue structure, duplicate identities, escapes, placeholders and plural shape remain in `TranslationCatalogueTests` / `translation_catalogues.validate_all`. |
| Six empty-option successor mutation methods | Historical absence is still in the original option record. Current catalogues are structurally validated; an old empty catalogue no longer demands a complete successor snapshot after every edit. |
| Seven JVM full-catalogue equality methods | Retired copied approval text, not replaced with self-equality. The existing `AppLanguageResourceRoutingTest` gains one all-offered-language public selection/wrap and compiled resolution/typed formatting check using configuration contexts, not Activities per string. Existing fixed malformed-template, percent/Unicode, alias and fallback-plural cases remain. |
| 82 JVM consumer methods | Exact normalized bodies survive outside these seven classes. Locale-independent tool, memory, crop, animation, save/cancel, alignment and undo behavior does not need one copy per translation batch. |
| Seven cohort crop-plural variants | Generic compiled plural checks cover counts 0/1/2/3/21/101 for all offered languages. Existing crop-dialog tests retain actual inclusion/None/cancel/accessibility behavior. Copied per-locale full text and hard-coded CLDR expectations are intentionally retired, not claimed as preserved. |
| Filipino return-to-drawing method | The same previous-tool, two zoom→drawing cycles, BRUSH restoration, unchanged pixels and dirty state survive `BretonAsturianOccitanPriorityWordingTest.returnToDrawingRestoresThePreviousToolWithoutRedrawing`; `PaintDocument.historySnapshot()` contains both undo and redo lists, preserving those state invariants; the survivor’s `forEachEditor` waits for startup, drains completion and destroys the Activity. Generic routing includes Filipino. Its copied full caption is retired. |
| Shared SVG/memory/tagged-colour fixture successors | Current XML replaces the seven review loaders. Tagged-colour runtime checks retain sRGB/PNG and exclusion of misleading BMP/GIF labels for every offered language; existing nonretired exact/parent/fallback cases remain. |
| Command references, percent labels and Save alias/action distinctions | One current-resource semantic test preserves command references, existing bounded ellipsis handling, canvas.png, literal `(%)`/formatted=false, aliases and distinct Save actions. No full translated sentence is copied. |

Production/resource/workflow files are unchanged. Normal focused tests and
required hosted compilation remain mandatory; no all-language layout or new
linguistic approval claim follows from structural/compiled coverage.

The first hosted retirement run exposed one remaining exact-script source guard
that pinned historical tagged-colour counts 140/141/30. Those three count
fragments and their mutation cases are also retired; actual Tatar binding,
coordinated-row rejection, `addExactScript` and missing-consumer guards remain.
A source-wide search found no other Python count/source guards for that retired
bookkeeping. The original failed run is retained; a corrected head requires its
own CI/review rather than a waiver or same-source retry.


## Family-wide catalogue-mirror retirement

The remaining 47 full-catalogue/cohort JSON mirrors are retired together, not
replaced with smaller copies of the same approved sentences. Their exact original
paths and Git blob identities remain recoverable at immutable
[develop 5367fe1e9703593bf464e1dd7f1aab2eab750868](https://github.com/c933103/AN-Paint/tree/5367fe1e9703593bf464e1dd7f1aab2eab750868).
The same source preserves removed helper/test implementations. No archive
payload is copied, fetched or reconstructed by routine CI.

This covers the eight per-locale families above and the remaining top-level
catalogue cohorts (Breton/Asturian/Occitan; Croatian/Bosnian/Macedonian; Galician/
Dutch/German; Georgian/Armenian/Azerbaijani; Hindi/Gujarati; Interlingua/Latin/
Kurdish; Irish/Gaelic/Welsh; Italian/Greek/Turkish; Kabyle/Hmong Daw/Maithili;
Maori/Samoan/Kinyarwanda; Moroccan Arabic/Mongolian/Toki Pona; Nordic;
North Korean/Australian; Nynorsk/Belarusian/Albanian; Persian/Hebrew/Urdu;
Portuguese/Spanish; regional Persian/Japanese/French; Serbian; Sinhala/Burmese/
Zhuang; Slovak/Slovenian/Catalan; Somali/Wolof/Haitian Creole; Thai; Ukrainian/
Lithuanian/Romanian).

| Retired responsibility | Surviving product responsibility |
| --- | --- |
| Complete accepted/held/source/predecessor/display copies, counts and digest mutation checks | Canonical resource XML and immutable review/source history own current wording and historical decisions. These approval freezes are intentionally retired, not claimed as equivalent runtime coverage. |
| Repeated catalogue-wide token, XML and plural probes | Existing `translation_catalogues.validate_all` / `TranslationCatalogueTests` cover current catalogue structure, duplicate identities, Android escaping, placeholders and plural shape. |
| Per-cohort full compiled-value equality loops | Existing `AppLanguageResourceRoutingTest.everyOfferedLanguageResolvesCompiledBoundariesWithoutPerStringActivities` exercises real selection/wrap for every offered tag, with restored application/locale state; existing fixed `LocaleTextBoundaryTest` cases retain independent format/Unicode/fallback boundaries. This is not direct-translation-presence, linguistic or all-language layout certification. |
| 202 repeated cohort consumer bodies | Exact normalized bodies survive in the existing representative tests; the per-method evidence map identifies each survivor. Locale-specific copied approval labels are retired; actual control bindings use current compiled labels. |
| 52 cohort variants | Operations/state assertions map to existing representatives after inspecting locale lists, helper behavior and assertions. The 20-image crop sequence and Nordic unit-button bindings are explicitly preserved rather than sampled away. Copied per-locale plural/text oracles are retired. |
| 58 cohort approval/history/adapter methods | Intentionally retired; tests of deleted JSON adapters are not new product regressions requiring replacement machinery. |
| Distinct real consumers | Eight existing representative classes retain 46 methods: Belarusian/Albanian (7), Georgian/Armenian/Azerbaijani (6), Italian/Greek/Turkish (6), North Korean/Australian (9), Persian/Hebrew/Urdu (5), Portuguese/Spanish (4), regional Persian/Japanese/French (4), Sinhala/Burmese/Zhuang (5). Existing exact-script/Latin-Sinitic and other real-consumer suites remain. |
| Additional TaggedColour and sampled-warning history mutations | Removed adapter-only corruption checks; all-offered sRGB/PNG/not-BMP-or-GIF semantics and actual importer/memory/state failures remain. |
| Old bounded P0/save successor comparisons | Pure approval loops are retired instead of converted into resource-to-itself assertions. Actual save/import/recovery/dialog/cancel/file-ownership and independent argument/alias relations remain. Bounded fixture payloads outside the 47 mirrors are unchanged. |
| Current wording semantics | Existing generic host tests retain command references, distinct actions, percent formatting, conditional crop semantics and attribution concepts. A proposed copied exact-label table was rejected: historical approval alone is not an independent executable obligation. Metadata/copy-credit/Hungarian constraints keep their original locale scope. |

The cohort source changes reduce 358 declared methods to 46 in eight existing
classes. Across all affected Kotlin files, declared `@Test` methods fall from
1,501 to 1,160; this is a source count, not a hosted execution count.
The 47 mirrors account for 12,484,429 bytes. Current-localization fixtures fall
from 131 / 15,124,016 bytes to 84 / 2,639,587 bytes, including the separately
merged Swedish manual successor. No production resource, workflow or new test
package/framework is added.

Focused validation, exact remote-source identity, hosted case counts and any
observed timing differences belong to this batch's PR/evidence receipt. Local
Android compilation is unavailable; static scans are not compilation. No
duplicate full normal/optimized aggregate or benchmark run is required.

### Remaining bounded scope

Cross-cutting residual/review adapters, exact-script and Latin-Sinitic approval
payloads, and bounded feature/delta fixtures still need their own product-
obligation review. Genuine native layout/font, provider, format and consumer
regressions must remain. Upstream catalogue/licence inputs have separate
provenance/build responsibilities. This batch does not declare project-wide
cleanup, linguistic acceptance or translation completion.

## Cross-cutting approval-payload retirement

The next coherent stage removes the six exact-script/Latin-Sinitic catalogue
mirrors, residual successor and reviewed-priority packets, and unconsumed
wording-provenance packet.
Original paths, wording and historical decisions remain recoverable in immutable
[develop 0ae074295045aaa794c755b5ff548067ccbfdfa5](https://github.com/c933103/AN-Paint/tree/0ae074295045aaa794c755b5ff548067ccbfdfa5).
Routine tests neither fetch that history nor reconstruct predecessor snapshots.
No substitute per-language miniature approval catalogue is introduced.

| Retired responsibility | Retained responsibility |
| --- | --- |
| Six complete accepted/held/raw/display/plural mirrors and their JSON/cache mutation tests | Canonical XML owns current wording; generic catalogue XML/escaping/placeholder/plural checks and real all-offered `AppLanguage.select`/`wrap` boundary tests remain. Exact approved sentences are intentionally no longer frozen. |
| Residual row counts, predecessor/source coordinates, packet review links and successor adapters | Immutable source/review history preserves acceptance decisions. Current source structure and independently specified product semantics remain active; adding a legitimate translation does not require an approval-table successor. |
| Four reconstructed device-language caption histories in the script routing test | All 28 public requested-tag/resource-tag/preference/platform/locale routing observations and fixed Save/File script boundaries remain. Those four old device-caption literal comparisons retire, not the real route. |
| Full compiled equality loops in the two script families | All 25 actual consumer methods remain, with current compiled labels used only as control-binding expectations. Native tooltip corruption/accessibility/layout, menu state, pixels, undo, memory admission and cancellation assertions are preserved. Their setup/teardown/lifecycle blocks are unchanged. |
| NAN Latin complete-warning mirror/digest mutation adapter | Real batch-crop selection/trim/reset/cancel/reopen and independent POJ combining-dot glyph/raster/layout checks remain. NAN captions bind to the current compiled plural; generic independent formatting boundaries remain. |
| RemainingAcceptedWording catalogue equality, per-option copied successor captions, and isolated residual brush/palette approved-caption assertions | All 21 additional-option identity/name/platform round trips, generic all-offered selection/formatting and existing actual editor/palette consumers remain; historical literal approval equality is explicitly retired. Registration records no longer force current catalogues to remain empty or incomplete. |

Nine JSON packets totaling **3,185,528 bytes** are retired. All host fixture
JSON falls from **95 files / 5,275,735 bytes** to **86 / 2,090,207 bytes**;
current-localization JSON falls from **84 / 2,639,587** to **81 / 2,066,409**.
Host discovery falls from **1,529 to 1,464** methods (zero import errors);
declared JVM test methods fall from **1,160 to 1,144**. These are source/data
counts, not a timing or hosted execution claim.

The method-level responsibility/preservation map and focused/hosted evidence
belong to this stage's PR and evidence ref. No production resources or workflow
are changed. Hosted compilation remains necessary; static preservation is not a
compile/runtime pass. Remaining bounded feature/delta fixtures and upstream
licence/catalogue inputs have separate obligations and are not silently removed.

### Current offered-option source coverage

A cheap inventory of unchanged develop `0ae074295045` using the existing
`translation_catalogues` readers finds **171 offered options and 171 exact
canonical catalogues**, against **716 translatable string keys and one plural
resource**. **60 catalogues contain every key directly; 111 lack one or more.**
This includes English variants. Six options (`chr`, `nch`, `nhe`, `nhw`, `quy`,
`zgh`) contain no direct translatable string keys; Czech lacks only
`ui_the_arrow_on_the_left_directly_below_the`. Runtime inheritance/fallback is
not counted as direct presence. This inventory supersedes stale source-coverage
counts, not the scope or acceptance status of historical reviews. Direct keys,
nonempty values or differences from English do **not** establish linguistic
correctness, fluency, full UI/layout coverage or translation completion.

## Final approval/feature-payload retirement

This final mapped stage retires the remaining priority/orphan, full AssemblyHelp
and feature approval copies, rather than moving their literals into Python or
another fixture format. All prior paths and bytes remain recoverable in immutable
[develop 25f678d2a784ffe096a0eeaf92494c02637e6cc7](https://github.com/c933103/AN-Paint/tree/25f678d2a784ffe096a0eeaf92494c02637e6cc7).
No application resource, production code, workflow or new test framework changes.

| Retired machinery | Surviving independent obligation / intentional limit |
| --- | --- |
| 39 priority/orphan approval packets and their held/predecessor/value mutation wrappers; three orphan Python scope tables | Canonical XML, generic all-offered structure/escaping/plural/typed-placeholder checks, real selection/wrap routing and the existing independent semantic regressions. Exact historical approved wording is intentionally no longer an executable freeze. |
| 23 AssemblyHelp packets, six JVM full-prose mirrors and the remaining whole-Help SHA oracles | Current control-caption bindings, source-language distinctions between snap/exact-position, overlap/origin/zero/movement, conditional attached/gap movement, own aspect ratio, memory branches, crop/normalization/undoable replacement/provider timestamp; genuine Tibetan instrumental, Hakka reading/script and existing narrow language regressions. Real geometry, help UI, crop, vertical/font and cancellation consumers remain. Repeated translated paragraph mutations retire, not become a translated clause database. |
| 19 feature packets | One unchanged font contract plus five reduced constraint-only packets retain independent protocol/legal identifiers, financial-credit prohibition, typed placeholders/formatted flags, live-label references, NFC and special-codepoint contracts. Actual provider/privacy/clipboard/redirect/disconnection/native cleanup, progress, crop and save/export consumers remain. Other packets contained only copied wording/history and retire. |
| Historical 59/112 approval partitions, empty/partial/full-catalogue status freezes and per-edit successor adapters | All 171 offered options still receive current structural checks and efficient public selection/wrap formatting boundaries. Registry identity/name/platform/fallback inputs remain. Direct coverage is reported, not a requirement to remain untranslated or to duplicate an approved catalogue. |
| Four memory-warning queue/successor packets (258,315 bytes) and their historical adapters | Independent import-current-limit versus combined estimated-assembly predicates, remedies, scalar formatting and real admission/recovery consumers; fixed memory-modality boundary inputs remain. Outstanding linguistic review and withdrawn acceptance status remain documented in `translations/source-review/README.md`; retirement grants no acceptance. |
| Twelve duplicated Croatian/Bosnian, Slovak/Slovenian and Catalan/Romanian consumer methods | Byte-identical memory-admission, failed-draft exact-byte recovery, dirty/bitmap/floating-selection recovery and atomic-encoding/file-ownership methods remain in `SerbianP0WordingTest` for both scripts. Unique Croatian layout/panel/dither consumers remain. Removed setup variants were not all textually identical; the retained methods do not depend on those focus/font differences. |
| Copied compiled approval equality and repeated gallery loops | Current selected compiled resources bind real controls; independent formatter/script boundaries and actual dialog/menu/state/bitmap/history/provider failures remain. Current-to-current binding is not claimed as independent wording approval. The direct Android unsupported-`zxx` full-Help comparison intentionally retires; offered English routing and malformed/missing-template boundaries remain, not that exact unsupported route. |

The retained eleven host fixture JSON files are genuine constraint/font,
registry and small crop/Hakka contextual inputs, not full current catalogues.
Upstream GIMP/Krita/LibreOffice/MediaWiki/Android catalogue and licence inputs
retain source attribution/import provenance responsibilities and are not current
wording oracles. Fixed script, memory-modality and vertical-notice boundary
resources remain independently specified inputs.

Exact file/data counts, method identities, focused checks and hosted execution
results are recorded with this stage's PR/evidence receipt. Declaration or
discovery reductions are not runtime results. No additional full normal/optimized
local aggregate or benchmark is needed. Earlier hosted timing varied and the
last actual-develop regression job was slower despite less test work; no reliable
overall wall-clock speedup is claimed. Linguistic completeness and unrelated
application-test optimization are not implied by completing this mapped cleanup.

Final source inventory for this stage: host fixture JSON falls **86 / 2,090,207
bytes → 11 / 47,965 bytes**; current-localization alone **81 / 2,066,409 →
6 / 24,167**. Four separately located memory-history JSON packets remove another
**258,315 bytes**; three orphan Python scope tables remove **269,664 bytes**.
Host test discovery is **1,464 → 1,018**, with zero import errors; declared JVM
`@Test` methods are **1,144 → 1,112**. The latter is not the hosted execution
count because SDK variants can execute a method more than once. Across touched
Kotlin files, 115 of 123 retained method bodies are byte-identical; eight change
current-resource binding or retire copied mirrors, and all retained setup/teardown
bodies are unchanged. Actual hosted results remain required for qualification.

## Residual sufficiency correction

The earlier "final mapped" description was too broad as a sufficiency claim.
Retiring whole catalogues and JSON approval packets did not remove smaller copied
sentences, source-spelling assertions or every repeated locale consumer. The
measured byte reductions remain valid; they do not prove that every remaining
test is justified or that routine verification is proportionate.

A subsequent current-source audit found full recovery/language-note comparisons
in Greek, Portuguese and Dutch host tests and in several compiled locale tests.
These are approval copies even without JSON. It also found repeated consumer
bodies in the Latin-Sinitic and other priority classes. The residual correction
retires copied prose and source-spelling guards only where actual behavior is
already covered, preserves independent semantic/grammar/format/script/legal
constraints and retains any source binding whose runtime replacement is not
established. Whole sentences must not merely become near-complete clause tables.

The Latin-Sinitic consumer class repeats the stronger ExactScript representative:
real category accessibility, dimension controls, crop, animation cancellation,
memory admission, draft preservation, dither, canvas/editor state and scaling.
Distinct POJ glyph/raster, native script/layout, selection routing and fixed
format boundaries remain elsewhere. Equivalent method text is not by itself
proof: locale loops, memory budgets, focus and teardown must be checked. Three
Belarusian duplicates map to existing ExactScript or Italian/Greek consumers.
The initial exact-body subset of 17 executions totaled only 4.7 seconds in the
already-produced actual-develop artifact; maintenance reduction is the principal
claim, not a large pipeline speedup.

PR256's dormant Czech manual host test owns direct-entry, paragraph-escape and
navigation/safety wording checks. Its per-edit JVM method retires entirely:
ordinary AAPT compiles the resource and the existing all-offered public
select/wrap test covers Czech routing. This dormant key has no distinct runtime
consumer or new formatter path needing another Activity-backed wording case.
PR257 added only two resources, no test/helper/fixture package. Both used a single
automatic ready-triggered Codex review. These demonstrate better recurrence
control, not proof that all future wording changes require new test cases.

### Remaining pipeline cost — audit only

The workflow still runs all jobs for resource-only pull requests and again on
`develop` pushes, with separate concurrency groups. PR256's existing observations
were 42m04s for the PR run and 22m19s for the subsequent push (combined elapsed
observations, not CPU time or a controlled benchmark). Avoiding equivalent-source
rebuilds needs a separate plan for exact tree/parents, required-check applicability,
trusted artifact/source identity and genuinely changed combined sources. This
correction does not change workflow triggers, gates, caching or release policy.

The default suite also includes `AdvancedColourLayoutDiagnosticTest`, which
records screenshots/geometry explicitly without fit acceptance; its prior actual
case-time sum was 18.808 seconds. Existing positive viewport/device regressions
must be distinguished from that diagnostic before changing its default execution.
Heavier actual UI/state/layout tests are not automatically redundant because
translation work originally motivated them. These remaining cost questions are
not claimed solved by the residual source cleanup, and no new benchmark suite or
replacement audit framework is introduced.

Residual source inventory: host discovery 1,019 → 1,014 with zero import errors;
declared JVM test methods 1,113 → 1,093. These are declarations/discovery, not
hosted execution counts or a speedup prediction. No production wording changes.
