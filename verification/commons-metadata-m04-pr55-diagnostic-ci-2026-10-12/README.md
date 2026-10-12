# PR55 diagnostic CI checkpoint

## Result: failure retained

This evidence-only checkpoint preserves run [38244193872](https://github.com/c933103/AN-Paint/actions/runs/38244193872), PR55 head `dc46abc2add7984358565a88fe65c5278212dcf6`, tested merge `56e7891852a2da201bf10ad99c486e659da2e6c5`, and tree `4ff7f479ffc73964fa8756b6c7e3202f624ad0f1`. Its source parent is the exact diagnostic head; no application source is changed here.

- JVM: 890 exact identities, 889 passes and one failure in normal-landscape M04 readability.
- Successful render receipts: 111/112 PNG/JSON pairs. The failing Ainu Kana COPY profile has separately labelled pre-check images and metrics, not a passing receipt.
- All 28 normal-landscape diagnostic profiles completed; their line metrics and actual alpha pixels were independently recomputed.
- Python: 666 passed. Native preparation, lint, APK/source delivery, exact-script probes and compiled M04 values passed their scoped checks.
- API35 installed tests: 104 exact source-bound identities passed (74 native and 30 app). Raw protocol, XML, deadline and coverage-union checks passed. This is separate from visual and release acceptance.

## Observed advance/ink discrepancy

Only Ainu Kana COPY at 640x320 DP/font1.0 violates the retained original horizontal advance guard. Line0 right/max advance is 1,233.043 px for a 1,232 px layout; it exceeds the existing width+1 bound by approximately0.043 px. Independently recomputed painted ink occupies x3..1231, right-exclusive1,232, with zero outside-layout pixels and no expanded-canvas edge contact. All63 UTF-16 units remain laid out over two lines, matching full accessibility text. The actual root crop matches the expanded raster composited on its background within one color-channel level everywhere.

The captured pixels do not demonstrate clipping. They do not establish Android's underlying advance discrepancy, universal oracle validity or cross-device behavior. The old guard is still failed in this checkpoint. No production, translation, font or tolerance change is claimed. The separately authorized painted-ink oracle repair is future work and must prove independent real clipping/overflow controls before fresh exact-source CI.

The two vertical emoji diagnostic profiles each contain one alpha pixel outside logical layout width. They are outside the original horizontal guard's route; this checkpoint does not generalize Ainu's zero-overflow finding to them or alter vertical acceptance. New sampled enlarged Manchu/Mongolian captures correctly show reading-start columns after the diagnostic capture-order correction.

## Durable contents and limits

`diagnostic-ci-evidence.zip` contains 481 original or explicitly derived evidence files: all111 successful M04 PNG/JSON pairs, all28 diagnostic root/expanded/JSON triples plus outcomes, all actual JVM XML, phase logs, exact-script raw probes, installed raw protocol/XML/coverage, source/build receipts, verifier scripts and the frozen independent review. The archive manifest records every file's size and SHA256. The independent report labels its derived white-background forensic image and directly inspected samples; it does not claim all-image visual acceptance.

Archive SHA256: `bb6da18a9af21b9e6047b6b47b3dbcad4bad75fdafb868038e05a2b353d90924`; Git blob: `16c94fa6c6f000d20bd11fc6a81cd05fbc94a570`; bytes:10,710,770. The ZIP is a bounded evidence bundle, not the APK or complete CI download. Full artifact IDs/digests are preserved in `verification/diagnostic-ci-metadata.json` inside it.

The [original failed CI checkpoint](https://github.com/c933103/AN-Paint/tree/docs/m04-pr55-initial-ci-20261012/verification/commons-metadata-m04-pr55-initial-ci-2026-10-12) remains unchanged. PR55 remains draft and depends on PR52; any successor needs fresh source pins, review and CI, followed by actual-base integration after PR52 merge. No merge, release, full-language or native-certification claim is made.
