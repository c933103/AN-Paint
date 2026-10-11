# Bounded 1× colour viewport acceptance, run 38124009781

The source-bound installed repair now passes the original positive viewport requirements, both native input routes, retained-state/IME/Back/commit coverage, and clean Hungarian portrait interaction.

- [Draft PR51](https://github.com/c933103/AN-Paint/pull/51), source head `512360bffef3abb393557bce29a30217b03c5ecc`.
- [Successful Actions run](https://github.com/c933103/AN-Paint/actions/runs/38124009781), tested merge `58a88ecc5bd67945afc9f6f0657331197254cf85`; source/merge share complete tree `61b0205749e5633f4dd5838c7236a8b4427a3bad`.
- Fixture: installed API 35 emulator, density 1, font 1×, 640 × 320 landscape / 320 × 640 portrait, English and Hungarian. The exact preserved original positive method body remains unchanged; only its documented successor swipe helper uses the native scrollbar gutter rather than the colour surface's editing route.
- All **102 installed methods**, **814 unique JVM methods / 87 suites**, lint, build and exact-script generation pass. All **552 host tests**, 15 focused and six optimized source-contract checks pass. App union is all 28 methods, with no suppressed or excluded methods.

## Actual native evidence

1. **Original positive viewport case, 2.947s.** Native holder 608 × 138px, editor 364 × 86px and content 326 × 470px. A real vertical gutter swipe at x373 moves scrollY **0 → 44**; Advanced tab, saved palette and Add stay fully visible and stationary. Native Cancel closes once without commit. The baseline measured a 360 × 0px editor with only 25px of its 48px Add control visible; its unchanged failed assertion is preserved separately.
2. **Hungarian captions and portrait interaction, 4.028s.** All five tab captions and Add fit their actual native line boxes with no ellipsis, and their full controls remain inside ancestors in both orientations. The two actual PNGs are visibly clean. Landscape→portrait native rotation removes the transient clipboard preview seen in the preceding trial; no guard result substitutes for these pixels. Final native Cancel at `[113,560]` occurs in portrait and satisfies the unchanged close/no-commit assertions. Portrait editor is 264 × 230px with overflowing content; all sixteen saved slots are visible.
3. **Retained state, 16.905s.** A native colour-surface drag changes selected colour (`-15509605 → -6619041`) while scrollY stays zero. Rotation retains the same controls, mode, value and field selection; the sixteen portrait swatches have finite geometry and the last landscape swatch is natively reachable. The actual configured fullscreen extract keyboard shows synthetic `#13579B` with selection. Its TYPE_INPUT_METHOD window is visible with nonempty root/bounds for 262ms, despite the legitimate zero dialog bottom inset. One native Back hides the keyboard and preserves the exact dialog/value/selection with zero close/commit callbacks; native IME absence remains stable for 274ms and the hidden PNG shows retained selection. Cancel restores the initial red. One Back closes a reopened picker with editor focus restored and no commit. Invalid hex is rejected; valid `#2468AC` commits exactly once, with three total closes.
4. **Complete existing installed union.** Native 74/74, ordinary 19/19 (155.848s under 180s), gallery 3/3, vertical 4/4, restart seed/verify 2/2. The real external force-stop boundary verified the live target PID became absent before the normal verify instrumentation. `coverage.json`, original summaries/XML and boundary log are retained.

`acceptance.json` extracts these facts without changing the raw receipts. Each raw export is manifest-bound to source-test digest `95fa05fecacbbf60f63a987e76385e9d22fc825db7092f98207db309af335609`, also found in the exact APK-embedded source and ordinary suite receipt. Actual images and intrinsic geometry are complementary evidence, not universal pixel or accessibility guarantees.

## Binary/source binding

- APK SHA-256: `4b394c47cad77f19feacb7436e6c0e963247f9a66a42b0f76f1c246f304a90be`.
- Matching source ZIP SHA-256: `d7599260607e9c9365cf7ef1f39b45178018829ac4fbf1f34217f0b38f7f4067`.
- The separately delivered ZIP equals the APK-embedded ZIP byte-for-byte; every one of 487 tracked production files matched the reviewed source snapshot. Original Actions artifact IDs, sizes and hashes are in `source-binding.json`.

## Retained failures and scope

The [untouched-base failure](https://github.com/c933103/AN-Paint/tree/8096234be003cd6a287660d32884c2541c518e65/verification/advanced-colour-viewport-2026-10-11/baseline-run-38112708313), original centre-route source, first responsive trial, caption/startup failure and fullscreen-inset failure remain unchanged in their historical archives. The preceding [c711 state run](../state-run-38122366555/) preserves its actual portrait-overlay limitation and ineffective title-guard result. No historical failure is retroactively relabelled as passing.

Only AdvancedColourDialog production layout changes from develop; input configuration, colour math, validation and callbacks remain retained. The final successor changed test orientation order, not production. **Font 2× short landscape remains diagnostic and unaccepted**, with known caption/preview clipping. No simultaneous IME/footer visibility, physical-device, TalkBack, linguistic, merge or release acceptance is claimed. APK signing is CI-debug only. PR stays a draft. Composing with the separate notice-dialog repair requires explicit supersession of its colour baseline-only guard/negative characterization and fresh combined verification.

## Archive reconstruction

```sh
cat accepted-focused-evidence.zip.part* > accepted-focused-evidence.zip
sha256sum accepted-focused-evidence.zip
unzip -t accepted-focused-evidence.zip
```

Expected **1,595,906 bytes**, **149 outer members**, SHA-256 `ea4c0f348d3326fff286898e417fc1f9d3e005fe9eb11b7ac28969a5a0bb726e`. The 33 parts preserve all three original app-owned raw exports and their 13 native PNGs/receipts, 24 model PNGs/eight reports, all JVM XML, lint, installed phase results, union/boundary evidence, public CI job log and exact source binding. Direct PNG/receipt copies are convenient excerpts; the original raw manifests are authoritative.

Every outer and nested text member was inspected for credential indicators, every nested member verified against its manifest, and all actual native PNGs visually inspected. Only project data and synthetic emulator UI are included, including existing synthetic `Artwork作品` clipboard content and public credit URLs. No full-device logcat, credentials, secret values or unrelated private data are included.
