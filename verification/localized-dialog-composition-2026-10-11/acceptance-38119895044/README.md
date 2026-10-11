# PR52 bounded composed acceptance

Exact source: [2755e30573d6ea2c071a128b6fa2940fc675af1a](https://github.com/c933103/AN-Paint/commit/2755e30573d6ea2c071a128b6fa2940fc675af1a), tree `8e92977c026be27c6e6b75d04467d2b818fb3681`. [Draft PR52](https://github.com/c933103/AN-Paint/pull/52) composes PR49, PR48 (C05), and PR47 (M02). [CI 38119895044, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38119895044) completed successfully against merge `7be43e63f80882f14761c114687ddf6b99d2204e`, with the identical source tree. [Code review](https://github.com/c933103/AN-Paint/pull/52#issuecomment-6106499616) found no major issues at the exact head. This evidence-only descendant changes no source or test contract and does not authorize merge, release, or ready-for-review transition.

## Results and preserved boundaries

- All 608 host tests passed locally. Fresh CI ran 608 host tests: 606 passed and two optional checks were skipped (the original log reports `OK (skipped=2)`). The original 90 JVM XML suites contain exactly 853 expected unique identities, without failure, error, skip, missing or extra cases. The expected union is separate from the actual fresh XML proof.
- Installed API35 has exactly 104 successful source-bound identities across eight phases: 74 native, 16 ordinary, three gallery-draft, two English/Manchu vertical, two Literary Chinese/emoji vertical, five dialogs and two separate credit-restart tests. API30's preserved source inventory is 95; it is not a fresh installed-runtime claim here.
- The five installed dialog cases retain their 45-second case limits; the dedicated dialog phase took 99.513 seconds within 300, and ordinary app phase 120.474 seconds within 180. Outer caps remain 43/53 minutes. Five original source-bound ZIPs contain ten inspected original PNGs and seven verified pre-cleanup Back outcomes. Installed notices are French; installed credit is Hungarian at 2x.
- The exact original 17-entry C05 fixture is unchanged, plus M02's exactly one additional Hungarian entry. All 18 compiled Hungarian values match their pinned fixtures. The compiled dump also preserves 696 canonical/private Korean values and all 38 F01/C023 descriptions.
- C05/M02: 126 fresh original files (30 C05 PNGs + 16 JSONs; 40 M02 PNGs + 40 JSONs). All 70 original images were inspected. Eight C05 editor and all 40 M02 PNGs are byte-identical to their accepted standalone originals, while fresh source-bound checks establish coexistence.
- Shared-dialog models: all 380 fresh files were compared independently: 312 byte-identical, 68 changed. The only semantic changes are C05 Hungarian captions and dependent geometry in 20 JSONs, 20 PNGs and two Hungarian pointer streams. Other 26 changed pointer streams differ only by timestamps. All 2,632 pointer records were checked. The 42 semantic-change originals are included here. Ten representative fresh Hungarian model images were independently inspected; four were also inspected by the producer coordinator. These are separate from the 70 C05/M02 and ten installed images.
- Unchanged actual-resource tests reveal each line of current Hungarian About and all three notice titles/bodies and every footer action at API30/35, portrait/landscape and 1x/2x. Only the first notice receives a model PNG. The repeated long-title fixture is an additional check, not a substitute for current resources.
- Long titles and vertical rails can exceed their viewport; individual line/edge reachability is not simultaneous visibility. C05 whole-view reveal flags alone are not scroll proof. The editor's final model frame can show only part of Copy with Save outside the viewport; the executed individual reveal assertions remain the behavioral proof. Unchanged C05 2x Copy whole-view false reflects lower padding, not lost caption glyphs.
- No linguistic, glyph-quality, physical-device, TalkBack, all-language or retained-guide live-reachability acceptance. PR51 colour repair remains separate. PR49's explicit baseline-limitation diagnostic is retained without positive colour-usability acceptance.

The source diff has 261 paths: 66 production (six Kotlin and 60 XML), 12 JVM/installed-test sources, 28 tools/CI/documentation, and 155 evidence paths. The exact producer union is 251 paths plus ten focused additions. All 247 nonconflicting producer paths and 116 Kotlin test files remain byte-identical. Narrow reversible transformations commute, restoring original source/resource hashes, including C04's whole-file guard. No historical fixture, assertion or endpoint was replaced or waived. Full source inventory and original failed attempts are preserved in the pinned source's verification directory and selected archive.

## Deterministic archive

`archive.json` pins 201 ordered parts: 200 × 50,000 bytes plus 36,470 bytes. Reconstructed ZIP: 10,036,470 bytes, SHA256 `6d2b8804e1bebf6b36df578a20b279a44416588567d1a1c21c19e05bdd14886a`. Every member has a fixed 1980 timestamp and regular-file mode. `members.json` pins all 368 selected member paths, sizes and SHA256 values (16,408,003 uncompressed bytes).

Groups: 126 C05/M02 originals; 42 changed Hungarian model originals; 107 regression files (90 JVM XML, 16 phase logs/timing markers, lint XML); 43 installed files (five original ZIPs, 32 phase protocol/XML/summary/install files, four coverage receipts and two restart-boundary files); eight generator originals; 25 compiled/source/terminal/log receipts; four independent runtime receipts; five replay/inspection scripts; eight source-verification reports and original failures.

The parts preserve exact selected originals. They are not the full original CI artifact ZIPs. `receipts/unarchived-originals.json` records sizes/hashes for full regression, emulator, APK/source, generation and build-diagnostic artifacts, plus the APK, corresponding-source ZIP and aapt2. In particular, the 157,864,159-byte APK/source artifact is SHA256 `4a210dff7263cfc850d8f4cfd08b868d9b349ecc99dffc0bb4bbfd146edd558f`. The APK itself is `46f67da30c49e5bcfff201ef26da8d49b4c86b2fc45fc512f5689423d59fd5bd`; its embedded source equals the sidecar ZIP (`201042b67b67d5bff032f799ba53d16427212d4e7dd3257b453b95cafda358b5`), and all 1,689 delivered tracked Git blobs were checked against the source tree. This bounded archive retains the compiled dump and binding receipts, not the large APK/source binaries; re-deriving the APK binding requires obtaining those exact original binaries while available.

Unselected model/native/vertical captures, full emulator logcat, raw signature-warning diagnostics, temporary aapt2 executable, derivative contact sheets and unrelated historical evidence are excluded. The held historical 50,000-byte object with SHA256 `3517c39a016128fcf23ed707e2227b70d02a35c59cc58810fd3b4c8768ff82aa` was not read, copied, repacked or retransmitted. No current archive member or part matches it; a current part sharing an ordinal has no relationship to that historical object.

## Reproduce the selected-subset gate

Download this directory, then run:

```sh
python3 verify_archive.py . --extract ./selected
```

This fails closed on changed/missing parts or members, unsafe paths, duplicate names, wrong digests, unexpected XML identities or changed installed export bytes. It rechecks 853 JVM identities, 104 installed XML identities, five exports and ten PNGs. `replay.json` records the successful run. `initial-verify-archive.py` and `initial-subset-replay-failure.txt` preserve a reproducible initial packaging-check mistake: the export manifest was omitted from the expected member set. The corrected verifier explicitly requires and validates that manifest; the original native collector independently passes unchanged.

For stronger source-bound installed protocol and native dialog replay, obtain the exact source commit and set `SOURCE` to that checkout:

```sh
python3 selected/scripts/installed_replay.py --checkout "$SOURCE" --artifacts selected/emulator --head 2755e30573d6ea2c071a128b6fa2940fc675af1a --tree 8e92977c026be27c6e6b75d04467d2b818fb3681 --run 38119895044 --output installed-replay.json
python3 "$SOURCE/tools/dialog_evidence_transport.py" selected/emulator/dialog-export --dialog-summary selected/emulator/app-dialog/androidTest-results/summary.json --output dialog-replay --receipt dialog-replay.json
```

The included `selected-installed-replay.json` and `selected-dialog-replay.json` are successful runs on the reconstructed selected archive. Compiled-resource verification scripts additionally accept the original dump and exact source checkout; Hungarian verification also hashes the original APK. The independent full-original audit script documents the initial investigation and needs its named original/baseline artifacts; it is not advertised as a standalone subset replay. Visual assessment remains a human inspection record, not something checksum/XML replay alone proves.
