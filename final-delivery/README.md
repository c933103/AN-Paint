# PR59 final delivery review

Status: PASS, bounded current CI-debug delivery audit. This is not release,
private-upgrade-signer, installed-device, rendering or linguistic acceptance.

## Exact identity

- Repository: https://github.com/c933103/AN-Paint
- PR: https://github.com/c933103/AN-Paint/pull/59
- Final head: `575a23220f5baac57fbfafa26c66bbfbea268c7a`
- Tested merge: `edb7bf96480b2cf3cf44080afca9e2a9aa0bc899`
- Both tree: `5194abcd7521c26b97a3e4bbffec36911272323a`
- Merge parents: develop `b20a827979d5bf9cd9e20898c65dcdc05fc7736a`, then final head.
- Run: https://github.com/c933103/AN-Paint/actions/runs/38325525117
- APK/source artifact: `11780767938`; 139,762,288 bytes;
  SHA256 `965009f58481b75679d5b3ee3ab018ae327ecd8e497ee7c6c137d83f718c0ad0`.
- APK: 167,628,302 bytes;
  SHA256 `0d92f4eb55c9c50a411c77f4df25247ab15dfda68857f19d63dfdcf1ed5c5b94`.
- Corresponding-source ZIP: 48,618,083 bytes;
  SHA256 `d6fa3f1576512b9531379ffd236f157c3f23d5ea2d4c50f41f59a36e929f7cc2`.

The remote commit/tree/parents and artifact metadata were independently fetched
through GitHub. The checkout is bound by its full staged tree and all actual
file bytes/modes, not its temporary synthetic HEAD. Every extracted member of
both current artifacts equals its archive member.

## Passed

- Build and exact-script jobs completed successfully for this run. Their job and
  step receipts are retained separately from the still-independent runtime audit.
- All 1,099 current tracked leaves match the local checkout, including modes.
  All 1,096 bundled tracked leaves match their exact Git blobs and executable
  modes. Only `.gitignore`, `colorpicker/.gitignore` and
  `.idea/codeStyles/Project.xml` are excluded by the existing bundle rules.
- Embedded corresponding source equals the separately delivered ZIP byte for
  byte. The 6,258 extra source files are confined to the four declared native
  source roots; all 11 native revision markers match current fetch-script pins.
- Package `paint.anpaint.android`, version `0.0.38` / code 95, min SDK21,
  target SDK35, debuggable. All four ABIs each contain the expected four codec
  libraries, with ELF class/machine matching their ABI. All 16 native libraries
  satisfy ELF LOAD and uncompressed ZIP 16KB alignment; SDK zipalign also passes.
- Android Build Tools 35.0.0 apksigner verifies v1 and v2 with exactly one CI
  Android Debug signer, certificate SHA256
  `eb32be7d26264e6b8898b173278a29a092b1fa61920fb4aad9ecf752e7f6b568`.
  This differs from the repository's existing upgrade certificate. Raw signer
  output retains its 29 META-INF/JAR metadata warnings; v2 verification passes.
- All 14 font-directory assets (13 fonts plus inventory) and 21 legal assets
  match current source and actual APK inventory. Font hashes, Nôm internal
  names/licence and complete MIT/OFL notice paragraphs are checked. The native
  notice receipt and all 35 runtime dependency coordinates match packaged notices.
- Compiled picker names/tags and platform locale XML retain exactly 167 options,
  22 aliases, the manifest localeConfig binding, 59 scoped catalogues and 108
  explicit open English fallbacks. All 27 added empty catalogues retain their
  documented not-started state. This is not translation-completeness acceptance.
- All 61 compiled M04 configurations, Mongolian/Manchu format controls and the
  three Arabic helper/route string values match the current source.
- Seven fresh exact-script-generation probes have exact source, commands,
  success markers, task ordering, output hashes and unchanged/up-to-date receipts.
  These checks inspect this run's retained receipts; they do not rerun Gradle.
- Picker (15) and platform-binding (33) checker controls pass in both ordinary
  and optimized Python. Delivery and package checks also pass with optimization.

## Preserved scope and limitations

The final tree differs from the develop baseline in 18 colour-related code,
test, evidence-transport and documentation files. The only changed production
application code is AdvancedColourDialog.kt. Full source matching, compiled
resource checks and native/font input checks preserve current package inputs;
they do not substitute for the separate C05/M02/M03/M04 runtime audit.

Ten pre-existing font inventory `licence_file` references name absent individual
APK assets. Their aggregate notices remain in FONT_NOTICES and
THIRD_PARTY_NOTICES. All these source inputs are unchanged from develop. The
unresolved metadata references are listed explicitly in `delivery-result.json`;
this review neither repairs them nor declares blanket legal acceptance.

No Android/Gradle build, installed runtime, hardware screenshot, private signing
or release publication was performed by this audit. Full API30/API35 execution
is reviewed independently. Native upstream archives were not independently
refetched; complete current bundled native bytes, pinned marker identity and
source-root inventory were checked. SDK verification binaries match the retained
Build Tools 35.0.0 hashes and current artifact copies; no new SDK was installed.

## Reproduction and evidence

`github-provenance.json`, `artifact-bindings-result.json`, `delivery-result.json`,
`package-result.json`, the three `compiled-*-result.json` files and
`build-job-status.json` are the compact source of claims above. Checker scripts
were retained with current identities; `checker-provenance.json` distinguishes
reused logic from fresh evidence. No prior acceptance result is reused.

To rerun, place the two current artifacts at `artifact.zip` and `exact-script.zip`
alongside these scripts, extract them to `delivery/` and `exact-script/`, and use
the source checkout whose staged tree and bytes equal the tree above. Use the
existing Android Build Tools 35.0.0 aapt2, apksigner and zipalign binaries, matching
the tool hashes in the artifact member receipt. The scripts accept `--repo`;
delivery/compiled checker options are listed by `--help`. Before the package
checker, generate `apksigner.log`, `zipalign.log` and `apk-badging.log` from that
exact APK using `apksigner verify --verbose --print-certs`,
`zipalign -c -P 16 -v 4` and `aapt2 dump badging` respectively.

`compact-receipts/` is the publication-ready packet, enumerated and hashed by
`RECEIPT-FILES.json`. Outer APK/source ZIPs, extracted APK/tools and duplicate
working files outside that packet are temporary audit inputs, not requested
source-tree additions. Publication and merge are outside this read-only audit.
