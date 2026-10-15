# Japanese PDF error states possible failure causes as certain

**Status:** Open bug; documentation-only issue-style tracking PR. This is not an implementation or fix claim. Keep the PR open/draft until the defect is resolved through separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Verification:** independent linguistic/static-source review only. No runtime, device, rendering, CI, native-speaker or whole-language acceptance is claimed. Repository Issues are disabled; this open PR is the durable bug record. [Project board](https://github.com/c933103/AN-Paint/pull/39).

## Expected and actual

Expected: the Japanese `formats22_pdf_invalid` message preserves the English uncertainty: “PDF could not be read. The file may be damaged or use features unsupported by this Android version.” Generic reader failures do not establish either cause.

Actual Japanese: “PDFを読み込めませんでした。ファイルが破損しているか、このAndroidバージョンで対応していない機能が使われています。” This states that the file is damaged or uses unsupported features, omitting “may”.

Impact: Japanese users receive an unjustifiably definite diagnosis after a generic PDF read failure and may assume corruption or incompatibility has been established. This is a bounded Japanese semantic defect; other catalogues are not asserted defective by this finding.

## Static reproduction and evidence

- [English strings.xml L590](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L590) and [Japanese strings.xml L159](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L159) bind the complete values at the source baseline.
- [PdfCodec.kt L122–141](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PdfCodec.kt#L122-L141) maps a failed PDF signature check and generic `IllegalArgumentException`/`IOException` to this resource. Existing specific `PdfImportException` messages are preserved; `SecurityException` uses the separate encryption/password message.
- [Independent Japanese review and proposed correction](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182427427) confirms the lost uncertainty and exact proposed value. English XML blob `005ec95b25cc816f067b78a073a2b1b8c37b71d6`; Japanese XML blob `401b81161d8e07576a800241b6749a24d4ca4734`.

## Bounded fix and acceptance

Proposed independently reviewed replacement, not yet applied:

> PDFを読み込めませんでした。ファイルが破損しているか、このAndroidバージョンでは対応していない機能が使われている可能性があります。

- Apply the Japanese semantic correction without changing the English meaning or the key's no-placeholder contract.
- Verify the compiled Japanese resource used by the generic PDF failure route retains possibility/uncertainty and the original actionable context.
- Exercise malformed-PDF and representative generic reader-failure paths where supported by the test harness; verify that specific page/size messages remain specific and encryption/password errors retain their separate resource.
- Run structural/resource validation and focused current-source PDF error/resource regression tests. Record runtime/visual results separately if actually executed; do not treat exact string equality as complete UI or linguistic certification.
- Re-review the full changed Japanese entry in its source context and publish a source-bound receipt before updating translation acceptance counts.

## Next action and dependencies

Apply the exact proposed value, add a focused semantic/error-routing regression, and complete current-source code review and applicable repository tests. No dependency on the other two bugs; coordinate with translation PR56 to avoid claiming acceptance for the old rejected value. This tracking PR contains documentation only and does not apply the correction or close the bug.
