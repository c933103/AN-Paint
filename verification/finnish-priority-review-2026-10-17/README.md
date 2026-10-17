# Finnish P0/P1 complete-value review, 17 October 2026

## Scope and result

Fresh model-based review of all **341 complete Finnish/English P0/P1 pairs** (92 P0, 249 P1) at develop `b6a99b41c4390ca6a412e3a1938eb913c59509fb`, source tree `f12e3f31420ab23c8edc67d72607150b796b1571`. Complete values, actual source consumers and relevant action chains were read, with an individual rationale for every entry.

- 295 unchanged values accepted in the inspected static context.
- 31 accepted for wording only: no current direct consumer or an uncalled settings/menu branch.
- Six corrected P0/P1 values, independently reviewed in full.
- Nine unchanged uncertainty holds, explicitly described below.
- One separately counted P2 width counterpart corrected with the same unit-consumer family. This does not expand the priority review count or change priorities.

The remaining 375 canonical entries have not received a complete review in this batch. No whole-language, native-speaker, physical-device, TalkBack or installed-layout approval is claimed. Existing withdrawn conclusions are not reinstated. PR56 stays read-only and no counters/receipts are uploaded there. All nine existing Finnish receipts are preserved as historical input; the one overlapping selected entry receives no duplicate tracker credit.

Fresh PR search and all three branch-list pages found no completed Finnish priority batch. Historical PR4 explicitly requires full recheck; its old completion claims were not reused.

## Seven bounded corrections

1. Encoder failure: `Kooderi ei valmistunut.` becomes `Kooderi ei suorittanut koodausta loppuun.` The failure concerns completion of encoding, not whether the encoder itself has been constructed. All three consumers emit it after `Bitmap.compress` returns false.
2. Language picker note: replace the claim that this language includes all translatable UI text with the full maintained-resources and English-fallback explanation, including its heading and paragraph break.
3. Dimension summary: replace fixed `%3$,d pikseliä` with `Pikselimäärä: %3$,d`. This handles both an allowed 1×1 image and larger counts while preserving all format arguments.
4–7. Accessible width/height descriptions: use `Leveys %1$s` / `Korkeus %1$s`, with embedded `pikseleinä` / `prosentteina`. The four complete sentences are natural Finnish. `ui_width_in` is the sole paired P2 correction. Visible `Leveys (%1$s)` / `Korkeus (%1$s)` and standalone `Pikselit` / `Prosentti` remain unchanged.

[Full old/English/new values and consumers](corrections.json) and [independent seven-key review](independent-review.md) preserve the exact proposal. Only seven value spans in Finnish XML change. Three compact host/fixture/Robolectric files accompany the resource correction; no application logic changes.

## Explicit uncertainty and preservation

- `save20_gif_description`: semantics retained; the preferred technical Finnish equivalent of dithering versus broad `Rasterointi` needs specialist/native confirmation. No asserted translation defect.
- `ui_the_draft_is_saving_try_again_shortly`: faithful wording, but the existing generic-busy credit-attachment context remains under PR72's source-context investigation. No contextual acceptance.
- `ui_fg` / `ui_bg`: compact `ET` / `TA` captions remain pending clarity/fit confirmation.
- `ui_left`, `ui_right`, `ui_bottom`: edge labels are intelligible, but accessibility compounds with the shared trim templates need coordinated full-composition review. They remain unchanged; no additional P2 edge/template edits are included.
- `ui_foreground_background_colour_palette`: absent consumer leaves the third argument's composition uncertain.
- `ui_main23`: bare `Pää` lacks a current consumer to establish the intended referent; retained pending context.
- The Save alias remains `@string/ui_save`: its consumer can save directly and does not always open a dialog.
- All four existing held rendering-label values in Indonesian, Malay, Japanese and Hong Kong Chinese remain byte-identical. Other P2/P3 values, catalogues, English source, priorities and application behavior are unchanged.

## Evidence and verification

[Full packet](finnish-review-packet.zip), [test summary](test-summary.json) and [SHA-256 checksum](packet.sha256).

The packet retains all complete English/old/candidate values and attributes, per-entry judgments, uncertainty, confidence limits, actual consumer references, immutable source URLs, value hashes, prior receipts, source/candidate manifests, exact application patch, validation scripts, raw checks and independent assessment.

Seven focused host tests cover exact values/attributes/format syntax, fail-closed fixture inventories, all seven old full values plus malformed variants, complete unit composition, preserved visible labels, count-neutral wording and truthful language note. Four Robolectric tests exercise the actual dimension controls through repeated unit switching and singular/grouped counts; the actual language picker custom title and Cancel; and all three real encoder paths under the existing bounded PNG-failure shadow, including source-pixel preservation, transactional derived destinations and successful PNG control.

The normal full host suite passed all 918 tests. The initial optimized run failed five ICO fixtures because JVM perf-data lock warnings contaminated numeric stdout; a subsequent isolated optimized ICO run passed all 19 tests unchanged. The complete optimized retry passed all 918 tests in 201.036 seconds with only local JVM perf-data collection disabled. The initial full optimized raw log was accidentally overwritten during that retry setup; the observed failure count, timing, five methods and diagnostic are preserved explicitly, without pretending to reconstruct the raw log.

The full canonical catalogues validate structurally. Full AAPT2 resource compilation, exact-script mirrors and resource linking pass. Supplementary Kotlin/API35 compilation of the new test passes with fresh resource symbols and existing dependency classes. This is not a full Gradle/runtime build. Local Gradle stops at the Gradle 8.13 distribution download with `Network is unreachable`; hosted execution remains required.

The evidence ref is additive: its parent is the application commit, every application file and mode is preserved, and only a dedicated evidence directory is added. The application PR remains compact and draft while its initial hosted checks run; parent coordination owns Codex review, readiness, merge and post-merge verification.

Application head: `69fe1495d4468fc028cf1bc30bdac35e70e6cdf0`; tree `c723db3d5e2c3202ea24c021f6a3e3574e840a83`. All 1,203 remote source leaves match the reviewed content, types and modes. [Draft PR126](https://github.com/c933103/AN-Paint/pull/126) and [initial exact-head run 39070781922](https://github.com/c933103/AN-Paint/actions/runs/39070781922) remain runtime-pending at publication.
