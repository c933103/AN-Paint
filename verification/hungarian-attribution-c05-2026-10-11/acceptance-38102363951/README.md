# C05 first exact-head CI and bounded visual findings

Source head: `d8132ede62bf50a0bd972588703bc6a86222e7f0`; tree: `29b3a691199cc0f07e546836c0019a53f69a6900`. Tested merge: `58c444149bf0165edaa131257fd5c472eee62311`. [Run 38102363951](https://github.com/c933103/AN-Paint/actions/runs/38102363951) completed successfully. This packet refers only to that original source, not a later test/layout change.

## Independent execution and source checks

- All four normal-current-platform jobs succeeded. This is a debug/API35 run, not release verification.
- Exact 812-case JVM union: all 804 inherited identities plus eight C05 API30/API35 cases; zero failures/errors/skips across 86 XML suites. All original JVM XML is retained in `all-jvm-xml.zip`.
- Lint: zero issues; original XML retained. CI host tests: 552 passed plus two explicitly optional Pillow skips out of 554; the local source run passed all 554. Original CI Python output and phase timing receipts are retained.
- API35 raw protocol, XML, SDK/source inventory, disjoint phase union, restart boundary and declared deadlines independently agree: native 74, ordinary 16, gallery 3, vertical 2+2, restart 1+1, total 99. Ordinary/gallery time was 128.006/47.677 seconds, inside the retained 150/70-second targets. Script completion was +529 seconds.
- The inherited 96-image archive and 28 native drag receipts decode and verify against their strict inventory, endpoint and parent-scroll assertions. This validates their data; no new independent visual acceptance of all inherited images is claimed here.
- APK/source identity, exact tested merge/run, identical embedded/delivered corresponding source and all expected tracked source blobs verified. All 17 Hungarian compiled replacements match, along with all 695 Korean canonical/private resource pairs and 38 frozen F01/C023 descriptions.
- All seven exact-script generation probes and their original log digests verified. Code review of this head reported no major issues; it is not linguistic or layout acceptance.

The JSON receipts and rerunnable verifier preserve the exact head/tree/run and expectations. To replay the raw artifacts, use `verify_ci.py` with `--source` at the source head above, the corresponding artifact and the retained `manifest.json`; supported kinds are generator, regression, build and device (`--sdk 35`). For compiled resource replay, run AAPT2 `dump resources` on the APK, then both retained compiled-resource verifiers against that dump and the pinned source. AAPT2 outputs values by default; it does not accept `--values`. The C05 verifier decodes AAPT's six-space continuation indentation and Android escaped newlines, rather than treating dump formatting as a resource mutation.

The original full build/regression/device ZIPs remain GitHub Actions artifacts and are **not durably archived in this bounded packet**. Their hashes are retained in each receipt. This packet durably retains the complete JVM XML, lint XML, selected phase evidence and all 16 original C05 PNG/JSON pairs. Do not claim a complete raw-archive copy from the presence of these receipts.

## What the pixels actually establish

All 16 C05 original PNG/JSON pairs were decoded and reviewed, using byte identity for repeated About captures. [capture-review.json](capture-review.json) contains every exact string, measured width/height/layout height, API, font scale and original PNG/pixel hash.

Reproduction: select Hungarian; use a 320×640dp portrait configuration at xhdpi; open the attribution editor or File → About and the corresponding notice. These captures are **Robolectric NATIVE at APIs 30 and 35**, not installed Hungarian-device screenshots.

### C05-L01: About heading ellipsis, confirmed

At 2× text, the title `Névjegy, licencek és forrásmegjelölések` visibly ends in an ellipsis on both APIs. The ellipsis is intrinsic to the title, separate from the scrollable menu. The three per-API About PNGs are byte-identical because this first harness captures before selecting the menu row. They do **not** establish that every About row is visible or reachable.

Representative originals: [API30](captures/api30-font2.0-about-2131493303.png), [API35](captures/api35-font2.0-about-2131493303.png).

### C05-L02: notice heading clipping, confirmed

All three titles are cut inside their own fixed-height heading area; scrolling the separate legal body does not reveal the heading remainder.

- Translation: `Fordítások forrásmegjelölései és licencei`.
- Assets: `Ikonok, betűtípusok és alkotások forrásmegjelölései`.
- Open source: `Nyílt forráskódú összetevők forrásmegjelölései és közleményei`.

The title view is 104px high (52dp). API30 text-layout heights are 267, 352 and 522px; API35 heights are 223, 294 and 294px respectively. `LegalInfo.termsDialog` places this `FlowTextView` outside the body scroll, with `maxLines=2` and a 52dp horizontal-layout height. The underlying complete strings and legal bodies are preserved; the visible title is truncated.

Originals: [translation API30](captures/api30-font2.0-notice-2131493275.png), [translation API35](captures/api35-font2.0-notice-2131493275.png), [assets API30](captures/api30-font2.0-notice-2131493303.png), [assets API35](captures/api35-font2.0-notice-2131493303.png), [open source API30](captures/api30-font2.0-notice-2131493377.png), [open source API35](captures/api35-font2.0-notice-2131493377.png).

### C05-L03: editor action visibility, unresolved reachability

The 1× editor title and Copy/Save/Done actions fit on both APIs. At 2×, Copy (`Forrásmegjelölés másolása`) and Save (`Mentés`) lie partly/beyond the initial viewport. The first harness calls actions programmatically and did not attempt ancestor scrolling. This establishes **initial off-screen content**, not that those actions are impossible to reach. Keep scroll/native-input acceptance open; do not count these as confirmed unreachable-control defects from a Boolean alone.

Originals: [API30 1×](captures/api30-font1.0-editor.png), [API35 1×](captures/api35-font1.0-editor.png), [API30 2×](captures/api30-font2.0-editor.png), [API35 2×](captures/api35-font2.0-editor.png).

### C05-L04: unchanged notice footer wording, confirmed visual clipping / geometry incomplete

The Copy all and Other terms footer captions visibly truncate/wrap below their fixed footer cells in the notice PNGs at 2× on both APIs; Done fits. These labels are unchanged by C05. The first harness measured the notice heading only, so it has no per-footer-action bounds or scrolling trace. A successor must record those separately. This is a shared localization-related UI follow-through, not a reason to shorten the corrected attribution wording or alter the legal text.

## Acceptance and next action

There are two passing initial-fit captures and 14 false flags. These are **not 14 equivalent production defects**: About captures repeat the same title state, notice headings are genuinely clipped, and editor action scroll reachability remains unresolved. Green behavioral CI is not layout acceptance.

Keep C05 draft and its 17-string production scope intact. Track the shared heading/footer layout correction separately with cross-language applicability, including long horizontal, RTL and vertical-script cases. The C05 test-only successor adds real About-row materialization, footer measurements, separate text-fit/initial-visibility/rectangle-reveal outcomes and ancestor geometry. It must receive new exact-head execution; this packet does not accept it in advance. No linguistic, physical-device, TalkBack or whole-localization completion is claimed.
