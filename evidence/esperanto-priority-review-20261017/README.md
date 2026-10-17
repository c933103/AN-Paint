# Esperanto P0/P1 full-value review, 17 October 2026

Download the [complete review packet](esperanto-review-packet.zip), [test summary](test-summary.json), and [archive checksum](packet.sha256). Detailed files named below are inside the packet.

## Hosted follow-up

[Run39063156079 completed successfully: all three Esperanto consumers, the full JVM suite, lint and all six jobs passed](runtime-39063156079/README.md). This later receipt supersedes the pending hosted-execution status in the original review below; it does not expand linguistic or layout acceptance.

## Scope and result

All **341 complete English/Esperanto pairs** were read individually: 92 P0 and 249 P1, against develop `5dba779c904a25bde2ec6d6f8f48eb3cad901a1e` (tree `2f15510fa46894e9a372ee58f2bf2b1ffeb4f691`). This is a fresh model-based linguistic/static-source pass, not restoration of the withdrawn PR5 conclusions. Current PRs, branch names, PR56's read-only historical material and earlier bounded receipts were checked to avoid duplicating another full Esperanto priority batch.

- 289 unchanged values accepted within inspected static consumer context.
- 27 unchanged values accepted for catalogue wording only, with no direct consumer found.
- 16 complete correction proposals accepted after an independent full-pair review: 15 crop-root spelling fixes and one count-neutral pixel-count message.
- Nine entries remain explicit holds.

Thirty entries have no direct consumer: the 27 wording-only values, two held composition entries and the corrected retained trim/expand action. No active-flow claim is made for these entries. The remaining 376 canonical catalogue entries were not reviewed in full. PR56 and its aggregate counters are unchanged. Existing ms/id/ja/zh-HK processing holds remain unchanged.

## Accepted corrections

The resource diff changes exactly 16 complete values, preserving names, types, attributes, all printf arguments and every other resource byte outside the replaced value spans.

1. `ui_d_d_px_d_pixels_2f_mp`: the former fixed plural produced `1 bilderoj` for a valid 1×1 image. `Nombro de bilderoj: %3$,d` follows the count-neutral source construction and works for singular and plural totals. Width, height, grouping and MP precision stay unchanged. `ImageDimensions.describe()` is the actual consumer, also displayed by `DimensionControls`.
2. Fifteen priority crop messages: `stuĉ-` becomes `stuc-`, consistent with the already-correct `Stuci bildon` and `Stuci al elekto` commands. Complete instructions and conditions are otherwise untouched. Fourteen have direct production consumers; `ui_trim_expand_canvas_by_touch` is a retained wording-only correction.

Primary spelling evidence: [ReVo official source at immutable commit c57161bc](https://github.com/revuloj/revo-fonto/blob/c57161bc944c57ab03abf7d6cd34c955ca8af9c8/revo/stuc.xml), retrieved and compared with the current official file through the GitHub connector. The `stuc.0i.TIP` sense explicitly defines image-margin removal: “Forigi la marĝenojn de bildo”. Its note recommends `pritranĉi` under La Bona Lingvo; **stuci is attested, not claimed to be the uniquely preferred term**. This bounded repair follows existing product terminology.

The initial question about `Punktismo` in the GIF explanation was resolved without changing it: [GIMP's Esperanto catalogue](https://mail.gnome.org/archives/commits-list/2019-December/msg09544.html) and [Komputada Leksikono](https://www.bertilow.com/div/komputada_leksikono/INDD.html) attest this technical usage. The existing separate control `Kolora punktado` was inspected as context, not counted as a newly reviewed priority entry.

## Explicit open holds and scope limits

- `gallery_credit_could_not_save`, `gallery_credit_too_large`, `legacy_credits_unreadable`: failure/preservation meaning is retained, but `agnoskoj` may suggest general acknowledgements rather than author/source metadata; review the attribution terminology family together.
- `ui_bg`, `ui_fg`: FK/AK compact-label comprehension, correspondence to full `fona`/`malfona` labels and fit remain open.
- `ui_foreground_background_colour_palette`: third-argument composition cannot be accepted without its intended consumer.
- `ui_main23`: the implied noun/context behind `Ĉefa` is absent.
- `ui_solid_fill`: technical suitability of `Solida plenigo` remains open; no style-only replacement is introduced.
- `ui_tolerance`: `Toleremo` needs confirmation for the numeric colour-difference threshold sense.

Thirteen additional resources outside this priority batch still contain `stuĉ-`. Their exact full values are preserved in `outside-priority-crop-followup.json` solely as a follow-up inventory, not complete linguistic acceptance or a new correction claim. They remain unchanged. Previous bounded Esperanto receipts are retained in the ledger as prior records without advancing their status or awarding duplicate credit.

## Validation and evidence

`esperanto-p0-p1-review.json` contains all complete source/target values, XML attributes, per-entry authored judgments, confidence, immutable source binding, direct consumer locations and SHA-256 scalar hashes. `corrections.json` includes all 16 complete English/old/new values. Supporting consumer snippets are in `context/`; their presence is evidence availability, not a claim of executing those consumers.

The compact application change comprises the Esperanto XML, a 16-value bilingual regression fixture, eight host contract tests and three Robolectric consumer tests. The latter cover live dimension labels, actual crop-margin validation, and native crop-dialog actions/incomplete-input rejection. Their source compiles with fresh AAPT-generated symbols; execution belongs to the hosted exact-head suite and is not claimed locally.

See `test-summary.json` for actual results. Full resource AAPT compile/link and supplementary new Kotlin-test compilation passed. Both focused host modes pass (8 tests each), and both full host modes pass (905 tests each); each former value is rejected by the complete-value contract. The standalone Java locale probe confirms Esperanto decimal-comma rendering, but is not an Android test.

`validate_evidence.py` rechecks inventory, full-value hashes, exact source/candidate spans, resource attributes, the four-file application delta, all baseline Git blob identities/modes and old-value negative controls. Run from this directory with the complete baseline restored under `source/` and the application patch applied there. The evidence archive itself includes only relevant originals/candidates, manifests, ledgers, scripts and logs; it is not a full repository checkout.

No whole-language, native-speaker, physical-device, layout, TalkBack, Gradle/JVM execution, lint or APK-delivery certification is claimed. The PR stays draft; exact-head independent code/security review and required hosted CI remain separate gates.
