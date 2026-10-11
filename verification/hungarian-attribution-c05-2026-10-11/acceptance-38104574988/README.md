# C05 test-observation successor: exact CI and actual capture receipt

## Exact source and outcome

- Source: `826eeaa9f4c2960eca3958ae63d673e4d87fe05a`, tree `f0b4b757e265ec5b176d9b7431533ae74080deaa`.
- Base: develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`.
- Tested synthetic merge: `b0fef63a6f316aa7bff65e176ef9080407a3c893`, the identical source tree.
- [Normal current-platform CI 38104574988](https://github.com/c933103/AN-Paint/actions/runs/38104574988): all four jobs successful.
- [Exact-head Code review](https://github.com/c933103/AN-Paint/pull/48#issuecomment-6104552336): no major issues reported.
- [Draft PR48](https://github.com/c933103/AN-Paint/pull/48) remains open. This receipt is published separately so its reviewed source is not advanced by evidence-only work.

The only production delta from develop remains the original **17 Hungarian resource values**. The successor changed two observation-test files and added evidence; no production layout, translation fixture, C03/C04/F01/C023 historical endpoint, legal text, locale routing, workflow or release setting changed. All 1,586 source-tree leaves were independently compared before CI publication.

## Fresh execution and artifact replay

Downloaded archives were matched to GitHub artifact digests before extracting and replaying their raw evidence. `artifact-metadata.json` records IDs, full digests and expiration times. The rerunnable verifier rejects wrong source/head/merge/run pins, duplicate or unexpected test identities, failures/skips, source-archive mismatches, changed deadlines and incomplete raw protocols.

- **812 JVM identities in 86 suites**, exactly 804 inherited plus eight C05 identities; zero failure/error/skip. The two target APIs are 30 and 35. All original JVM XML is retained in `all-jvm-xml.zip`.
- CI Python: **554 total, 552 passed, two inherited optional-Pillow skips**. The final local suite had 554 passes, zero skips (148.163 seconds); normal and optimized focused suites both passed eight tests.
- Lint: zero issues; original XML retained.
- Timed CI phases: Python 158.651/240 seconds, JVM 486.861/720, native dependencies 76.934/360, lint 109.668/360. No budget changed.
- Seven exact-script generation stages and their actual log hashes pass.
- The debug APK's embedded corresponding-source ZIP equals the delivered source ZIP. **1,583 tracked source blobs** match; the only three deliberate tracked exclusions are `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore`. Four declared bundled native-source build prefixes remain separately identified, not individually re-certified upstream here.
- APK SHA256 `9b5529573d5aadc6b3ea17e00b7755016769bac6fb4fe88bb01d046054ca46b4`.
- Corresponding-source SHA256 `0cdf47995f42e87ea69d876e67646dceb0e311deeefaa07d99ed0dd14a9dc01b`.
- Exact compiled Hungarian resources: all 17. Inherited compiled checks: all 695 canonical/private Korean resources and all 38 bounded F01/C023 descriptions pass.
- Installed API35 exact union: **99 methods**. Native 74 (48.153 seconds); ordinary 16 (115.315); gallery 3 (44.859); vertical English/Manchu 2 (110.417); vertical literary-Chinese/emoji 2 (101.771); seed 1 (5.428); verify 1 (8.454). All raw protocols, source identity, process/restart boundaries and declared method unions pass. Ordinary/gallery are below their original 150/70-second targets.
- Inherited 96 PNG files decoded and matched their capture inventories; 28 native drag traces replayed with the original transport and reachability checks. This is **not a fresh actual-pixel acceptance of those inherited 96 images**. Actual-pixel review in this receipt concerns the 20 C05 originals below.

## Actual C05 observations

All **16 JSON and 20 PNG originals** are retained under `captures/`, including four additional scroll-reveal PNGs. All 20 PNGs were visually inspected. `capture-review.json` records per-image dispositions and SHA256 identities; the original JSON retains the full before/after view and ancestor geometry.

Reproduction profile: **Robolectric NATIVE rendering, API30 and API35, Hungarian, 320×640 dp portrait, xhdpi, 1×/2× font scale**. These are not installed Hungarian screenshots, physical-device or native-speaker results. List selection and rectangle requests exercise actual model views/ancestors. Item/button callbacks preserve behavior evidence but do not establish physical-finger, keyboard or TalkBack activation.

### C05-L01: About heading truncation, confirmed; selected rows fit

At 2×, `Névjegy, licencek és forrásmegjelölések` ellipsizes in its two-line heading on both APIs. The heading bounds are x80/y68/480×182 px on API30 and x80/y68/480×152 px on API35. Rectangle requests do not recover omitted heading text.

In contrast, all **six actual selected rows** are intrinsically complete and fully visible after list selection:

| Actual selected string | API30 view/layout height | API35 view/layout height |
| --- | ---: | ---: |
| `Fordítások forrásmegjelölései és licencei` | 236/236 px | 208/208 px |
| `Ikonok, betűtípusok és alkotások forrásmegjelölései` | 311/311 px | 274/274 px |
| `Harmadik felek közleményei` | 161/161 px | 142/142 px |

Row width is 576 px on both APIs. Other nonselected rows may be partially outside the viewport in a given PNG. That does not demonstrate clipping intrinsic to those rows or inability to scroll to them. The measured selected rows have actual attachment, matching text and visible-rectangle checks before their real item callback.

### C05-L02: notice headings truncate inside their own fixed view, confirmed

All three selected notice headings occupy **489×104 px (52 dp high)** at screen x56/y48, outside the legal body's independent scroll container. Their text layouts need:

| Heading | API30 layout height | API35 layout height |
| --- | ---: | ---: |
| `Fordítások forrásmegjelölései és licencei` | 267 px | 223 px |
| `Ikonok, betűtípusok és alkotások forrásmegjelölései` | 352 px | 294 px |
| `Nyílt forráskódú összetevők forrásmegjelölései és közleményei` | 522 px | 294 px |

The views themselves are on-screen, but their text is cut off. Ancestor rectangle requests cannot recover text outside the view's own height. Original legal body bytes still equal their packaged assets exactly. Production source: `LegalInfo.kt::termsDialog`, its fixed `dp(52)` title height and `maxLines = 2`; actual locations remain in the pinned source.

### C05-L03: editor actions scroll-reveal; no demonstrated inaccessible label

At 1×, the editor title and Copy/Save/Done actions are intrinsically complete and initially fully visible on both APIs. At 2×, Copy and Save begin below the viewport. The successor performs actual ancestor rectangle requests and captures the resulting pixels:

- Copy: `Forrásmegjelölés másolása`. API30 view 528×182 px with 142 px text layout moves from y1196 to y1072. Its local visible rectangle is `[0,0,528,176]`. API35 view 528×171 px with 131 px text layout moves from y1196 to y1078; visible rectangle `[0,0,528,170]`.
- Both Copy reveal PNGs show the **complete two-line label**. The strict whole-view result remains false because **6 px (API30) / 1 px (API35) of lower padding** lies outside the 176/170 px footer viewport. This is not lost label text. Do not report the false flag as an inaccessible Copy action.
- Save: `Mentés`. API30 267×116 px and API35 252×110 px become fully visible at y1132/y1138 respectively; their actual labels are visibly complete.
- Done: `Kész` and the editor heading `Képek forrásmegjelölései` have complete intrinsic text. The footer scrolls between actions, so no claim is made that all actions are visible simultaneously.

The full-view predicate remains deliberately strict and unchanged. Visual interpretation qualifies it rather than replacing it with a false all-green value. Native pointer activation remains separate work.

### C05-L04: notice footer captions truncate inside fixed controls, confirmed

The measured controls are each **163×96 px**, at y982. `Összes másolása` needs 236 px of layout; `Egyéb feltételek` needs 179 px. Both captions are visibly cut off in all six notice PNGs and do not recover through ancestor rectangle requests. `Kész` needs 65 px and fits. The controls are on-screen; this is caption clipping, not a demonstrated missing callback.

### Scope of repair and acceptance

[Separate draft PR49, AN-W04-DIALOG](https://github.com/c933103/AN-Paint/pull/49) owns shared production layout correction with cross-language applicability and stronger pointer/reveal tests. This receipt does not accept that future tree or combine it with C05. C05's 17 words remain unchanged. Confirmed defects are the About heading, notice headings and notice footer captions. The original 14 false capture-level flags are **not 14 independent production defects**.

Native-language fluency, physical devices, TalkBack, HU-12/HU-17 retained-resource live routes and broader localization/reset acceptance remain open. The register remains 475 total / three structurally completed / 472 pending. M02/PR47 remains independent; its earlier offline resource preflight is not runtime composition acceptance.

## Reproduce and inspect

1. Check out exact source `826eeaa9f4c2960eca3958ae63d673e4d87fe05a`.
2. Run `python -m unittest discover -s tools -p 'test_*.py'`, `python -m unittest discover -s tools -p 'test_hungarian_attribution_c05.py'` and its `python -O` form.
3. In an environment with the documented pinned Android toolchain, run `bash gradlew :Paintroid:testDebugUnitTest --tests org.catrobat.paintroid.local.HungarianAttributionC05Test`. The class pins API30/API35 and the profile above; outputs are under `Paintroid/build/reports/hungarian-attribution-c05`.
4. Download the exact artifacts named in `artifact-metadata.json`. Run `verify_ci.py KIND ARCHIVE --source CHECKOUT --directory OUTPUT --manifest manifest.json` for `generator`, `regression`, `build` and `device`; add `--sdk 35` to the last. Keep `expected-jvm-union.json` beside the verifier. The verifier's source/head/merge/run pins are explicit.
5. Extract the debug APK from the build archive, run pinned `aapt2 dump resources app-debug.apk > compiled-resources.txt`, then `verify_c05_compiled.py --source CHECKOUT --dump compiled-resources.txt` and `verify_inherited_compiled.py --source CHECKOUT --dump compiled-resources.txt --output inherited.json`.
6. Compare all original PNGs with their corresponding geometry. `-reveal-1.png` is Copy and `-reveal-2.png` is Save for each 2× editor.

`SHA256SUMS.json` covers every file in this packet except itself. Complete large raw build/regression/device Actions archives are **not durably copied by this packet**; they expire on 25 October 2026 at the metadata times. This packet preserves the complete original C05 captures, all JVM XML, lint and phase logs, plus independent replay receipts. It does not imply a full raw-archive backup, installable release, merge readiness or native-language acceptance.

Raw phase logs are preserved byte-for-byte, including their original trailing spaces. Whitespace checks on these archived logs are not source-formatting failures.
