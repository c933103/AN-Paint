# Independent PR52 artifact-verifier and vertical screenshot review

## Result

Bounded acceptance of the final temporary verification helpers and the inspected artifact evidence. The normal-mode false-positive report-validation gaps found during this audit were repaired and their negative controls now reject. No remaining blocker was found within this audit's scope.

This is a post-CI evidence-helper audit, not a claim that defects were found in application code or CI execution. The audited helpers are temporary scripts outside the checkout. The author confirmed their real invocations used ordinary Python, not optimized mode; initial bare-assert usage therefore did not invalidate completed checks. Visual byte differences were always intended to require a separate disposition. No previously performed independent visual review is withdrawn by this audit.

Reviewed published identity supplied with the task: head `71f4d288669858e7975ec4c094b7f47a9a1ff145`, tree `815e265af5387111dcdaef66efac5d2091bbb56d`, CI run `38227280656`, CI merge commit `f008d110f83cb6390db941b9177062edb8ea212c`.

## Actual artifacts independently replayed

- Build artifact SHA-256: `9cd38b08fb3199663ac70a9c0b6c51be745c6dc6523b631e6d6137653d1b5416`.
- Regression artifact SHA-256: `e12217e8ed2c53d9af6f1b5bf469096dc4ba0788c03ab4e37b2c28b132a3f845`.
- Emulator artifact SHA-256: `241102a00244ce04fd4a40c2e246f331aec78c7c49031cd3ab0c3a3a79801e8e`.

The build replay matches all 1,802 included tracked source blobs against the publication manifest, permits only the three explicit source-archive exclusions, matches all 14 font assets and proves embedded/sidecar source equality. APK SHA-256 is `ea5c12dce2d25d05f2c2761ac07af1b6868d896b9300a01f49bd0cbbaab960a0`; source ZIP SHA-256 is `0e333d9aa5cf212b63ea801bb3e54017e720de80a7b282ed0f5c80fb516822aa`. Independent nested-archive inspection found no duplicate names, unsafe paths or symlinks in 660 APK members or 8,790 source members. This is debug source/font identity; signing and release decisions remain separate.

The hardened regression replay passes 869 exact JVM identities across 92 XML suites, with zero failures, errors or skips and zero lint issues. All 602 model evidence members, including 288 PNGs, are byte-identical to their accepted source-specific references:

- Localized dialogs: 380 members / 170 PNGs.
- M02: 80 / 40.
- C05: 46 / 30.
- M03: 96 / 48.

The first replay correctly stopped at C05 filename inventory drift. Its 34 About/notice filenames used three resource IDs shifted by one after composition. The final helper admits exactly three old/new ID mappings and exactly 34 substitutions, verifies the corresponding named resources in both APK resource dumps, and records every old/new filename. The explicit APK-versus-Robolectric resource type offset is retained; no general numeric renaming or inventory waiver is used. Member contents remain byte-identical after that exact bijection.

The hardened installed replay independently reconciles original raw protocol, XML, JSON and source-digest-bound union: 16 ordinary + 3 gallery-draft + 4 vertical + 5 dialog + 1 seed + 1 verify = 30 app cases, plus 74 native cases, total 104. Every case passed and phase elapsed times are finite, nonnegative and within their respective limits.

The actual boundary log was separately inspected: a successful seed uses live PID 6849, a verified live-process force-stop exits successfully, explicit PID absence is recorded before verification, and the final status is `COMPLETED`. Its SHA-256 is `d10e3c22f123479716044ecd406f5f500db234f7983fcac156d3846064b35e90`. A synthetic union alone was not used to establish that boundary.

## Findings, corrections and negative controls

Initial tested snapshots already contained the author's newly added explicit optimized-mode guard. Their identities and initial controls are retained:

- Build: `69f52fc5964d758ca76bb6323c2014d384b4e0da7ef85f08ab16183de5816e7b`.
- Regression: `a6792f65332f14d5010f7cbc0093890b8b9220e98b2cdc1ff0b7f7edb0627afa`.
- Installed: `fdada552d309d339e368267fe56665a1f52152c65a9b5769c10e5fbf5ed0fcb9`.

1. Regression accepted malformed lint roots, including a nested Error issue, as zero lint issues. It also silently collapsed duplicate visual archive names. Fixed by validating archive uniqueness and the actual lint schema/empty issue inventory. Valid evidence still passes; the malformed inputs now reject.
2. Installed verification accepted an unrelated XML root, contradictory suite counters and negative elapsed time. Fixed by requiring testsuite/direct case structure, exact counters and finite nonnegative duration within the limit. Raw-protocol failures and wrong coverage were already rejected and remain rejected.
3. A failed ordinary replay left a previous success receipt intact. Fixed by removing the designated receipt before validation; a positive-installed replay followed by a raw-failure replay now exits nonzero and leaves no success receipt. The regression stale-output control also passes.
4. All final helpers explicitly reject `python -O`. Real acceptance was not run with optimization. Consumers must always check the command exit status, including an invocation rejected before normal processing.
5. Invalid PNG bytes remain listed as a visual difference rather than being independently certified by the regression helper. This behavior is explicit and requires separate visual disposition; the helper is not a standalone visual acceptance gate. The actual 288 model PNGs are byte-identical to the accepted references, so this is not an unresolved current-artifact difference.

Final helper SHA-256 values:

- `verify_build.py`: `f43bd62f0d4b9aaf12381780531bfde688bd5a56df469825508afa912bb8e2e3`.
- `verify_regression.py`: `01237d28cfac072657106885a89c95af98f0060fcc65d861b116f9d54fd216b0`.
- `verify_installed.py`: `16d60686ca6ef61088834fde209c958406a943b50c804a4b2e5913d4868e61ea`.

Final controls establish valid-positive acceptance plus rejection of malformed/nested lint, duplicate visual members, wrong JUnit roots, incorrect JUnit counters, negative elapsed time, failed raw protocol, wrong coverage and optimized mode. Ordinary failed replays clear stale success. Exact scripts, commands, exits and JSON results are included. Synthetic controls are clearly named and are not real CI pass evidence.

## Independent fresh vertical image review

All 64 requested reachability PNGs were visually inspected at their original pixel resolution in eight labeled contact sheets: English vertical, Literary Chinese, Manchu and Emoji, each portrait and landscape. Their hashes match the original emulator artifact exactly; the contact sheets only arrange those original pixels and add labels.

The eight frames in every case cover initial state, minimum, maximum, filename, description, Cancel readiness, Choose readiness and returned editor. The inspected evidence shows distinct 1/100 slider states, full filename exposure in the filename frame, readable description exposure in its dedicated reveal frame, visible action regions and an unobstructed returned editor. English/Manchu and Literary-Chinese/Emoji slider directions differ consistently with the displayed reading direction. Manchu joining and Chinese/Emoji glyphs render visibly without replacement-box artifacts in the inspected controls; this does not establish linguistic correctness.

No new visual blocker was observed in these 64 frames. Neighboring content is partly outside the finite scroll viewport in several intermediate frames; the later reveal frames expose the target being checked. This is bounded native reachability evidence, not a claim that all content fits simultaneously or a new all-screen aesthetic acceptance.

The 10 dialog PNGs were assigned separately to the author and are not claimed as independently inspected by this reviewer. Broader device matrices, physical devices, TalkBack, language quality, unrelated colour usability and upgrade-signing acceptance remain outside this review.

## Reproduction and evidence

`regression_negative_controls.py` and `installed_negative_controls.py` reproduce the original normal-mode gaps against their preserved guarded snapshots. `final_regression_controls.py` and the final control JSONs demonstrate corrected behavior. They use local copies/fixtures and the recorded accepted/develop artifact inputs; no hosted state is changed.

`final-build-verification.json`, `final-regression-verification.json` and `final-installed-verification.json` are actual-artifact replay results. `actual-boundary-and-image-bindings.json` binds the real process boundary and the 64 reviewed image hashes. `vertical-images-reviewed-manifest.json` and the eight contact sheets identify every image visually inspected.

No tracked application/test source was changed, no remote writes were performed and no merge/release action was taken by this reviewer.
