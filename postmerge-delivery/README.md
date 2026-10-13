# PR59 postmerge delivery review

Status: PASS, bounded fresh postmerge CI-debug delivery audit. This is not a
release, private-upgrade-signer, installed-device, rendering or linguistic acceptance.

## Identity

- Repository/PR: https://github.com/c933103/AN-Paint/pull/59
- Actual merge/develop commit: `2b144237836a11b4bf42ea037a1ab5b88366e098`
- Tree: `5194abcd7521c26b97a3e4bbffec36911272323a`
- Ordered parents: `b20a827979d5bf9cd9e20898c65dcdc05fc7736a`,
  `575a23220f5baac57fbfafa26c66bbfbea268c7a`.
- Natural develop push run: https://github.com/c933103/AN-Paint/actions/runs/38328484887
- APK/source artifact `11781708543`, 139,762,290 bytes;
  SHA256 `240205d86dc56ccf42d5a63782cd75bacfbdde5624ba8b441ce3299ca7af946d`.
- APK, 167,628,302 bytes;
  SHA256 `4f83079c328ae84c593b28323bf5c2dd86d80d6abfc15dcfee62e0bc9a4ff3c8`.
- Corresponding source ZIP, 48,618,083 bytes;
  SHA256 `d6fa3f1576512b9531379ffd236f157c3f23d5ea2d4c50f41f59a36e929f7cc2`.

GitHub commit/tree/parents, develop push identity, fresh artifact metadata and
successful build/exact-script job receipts were independently fetched. All
extracted members of both new artifacts equal their archive members. The local
checkout is bound by its staged tree and actual bytes/modes, not its synthetic HEAD.

## Passed against these fresh artifacts

- All 1,099 current tracked leaves match local bytes/modes. All 1,096 bundled
  tracked leaves match their Git blobs and executable modes. Only `.gitignore`,
  `colorpicker/.gitignore` and `.idea/codeStyles/Project.xml` are excluded by the
  existing bundle rules. Embedded and separately delivered source ZIPs match.
- The 6,258 extra source files are confined to four declared native-source roots;
  all 11 native revision markers match current pins. No unchanged upstream
  archive was unnecessarily refetched.
- Correct debuggable package `paint.anpaint.android`, version `0.0.38`, code95,
  min SDK21 and target SDK35. Four expected ABIs each contain four expected codec
  libraries; ELF machine/class and both ELF LOAD/ZIP native 16KB alignment pass.
  Android Build Tools 35.0.0 zipalign independently succeeds.
- APK v1/v2 signatures verify with exactly one fresh Android Debug signer:
  `ddf5f24dfc28ce5dadc72f90cbff4742b5e4a8544e6f0755263f9179e102ac41`.
  It differs from the private upgrade certificate. The 29 META-INF/JAR metadata
  warnings remain in raw apksigner output; v2 verification passes.
- All 14 font-directory assets (13 fonts plus inventory), 21 legal assets,
  font hashes, Nôm names/licence, required complete MIT/OFL paragraphs, native
  notice receipt and all 35 runtime dependency notice coordinates match.
- Compiled 167-option picker/platform locales, 22 aliases and manifest
  localeConfig binding match current XML. The 59 scoped/108 fallback split and
  27 empty not-started additions remain explicit, without linguistic acceptance.
- All 61 compiled M04 configurations, Mongolian/Manchu controls and three Arabic
  helper/route strings match current source.
- Seven new exact-script probe receipts pass source, command, ordering,
  success-marker, generated-output hash and up-to-date checks.
- Picker (15) and platform-binding (33) checker controls pass normally and with
  Python optimization. Package/source audits also pass both modes.

## Comparison with the final PR build

`premerge-payload-comparison.json` compares the new APK with run38325525117's
final PR APK. All 660 ZIP entry names match; only `META-INF/CERT.RSA` bytes differ.
Every non-signature decompressed ZIP member is byte-identical. The separately
delivered source ZIP is also byte-identical. This comparison does not cover
signing blocks, ZIP layout or timestamps, and it does not reclassify prior API30
execution as fresh postmerge execution.

## Limits and remaining attribution

No failed gate or blocker was found within this bounded delivery audit.
Postmerge routine API35 and regression results are reviewed independently.
API30 was not selected in this natural postmerge workflow; its final full-matrix
evidence remains attributed to prior run38325525117 on the exact same tree.

Ten unchanged font inventory licence_file references name absent individual APK
assets; their aggregate notices remain exact in FONT_NOTICES/THIRD_PARTY_NOTICES.
The unresolved paths are explicitly listed in delivery-result.json. This audit
does not repair those references or claim blanket legal acceptance.

No source edit, Android/Gradle rebuild, installed execution, hardware rendering,
private signing, extra workflow, publication, merge or Work task was performed.
Native upstream archives were not independently refetched. Current source-root
bytes and markers were verified. SDK verification binaries match the prior
Build Tools35.0.0 hashes and current copies; no new SDK was installed.

The only production application code changed from the pre-PR develop tree remains
AdvancedColourDialog.kt. Source/package/resource checks preserve the unchanged
context typography and other inputs, but do not substitute for the separate
C05/M02/M03/M04 behavior/rendering review.

## Receipts and reproduction

See REVIEW-RESULT.json, github-provenance.json, artifact-bindings-result.json,
delivery-result.json, package-result.json, compiled-*-result.json and the build
job receipts. checker-provenance.json identifies reused checking logic; all
current artifact checks were rerun. Prior acceptance results were not reused.

To rerun, place the two fresh archives alongside the scripts at artifact.zip and
exact-script.zip; extract to delivery/ and exact-script/. Supply the exact-tree
source checkout through --repo. Other checker options are available through
--help. Use the hash-matched Build Tools35.0.0 verification programs to produce
apksigner.log with verify --verbose --print-certs, zipalign.log with
zipalign -c -P 16 -v 4, and apk-badging.log with aapt2 dump badging before running
the package checker.

compact-receipts/ is the publication-ready packet, enumerated in RECEIPT-FILES.json.
Large archives, extracted binaries and other files outside it are temporary audit
inputs. This audit did not publish them or add them to the application source tree.
