# P07-007 bounded pt-BR TIFF/DIB export semantic recheck

Date: 10 October 2026. Parent obligation: **P07-007 remains Pending full recheck**.

## Result and boundary

Two substantive pt-BR changes, `formats22_tiff_description` and `formats22_dib_description`, were individually compared with their consumers and history. The unchanged `formats22_tiff_compression` checkbox is a necessary third contextual disposition. This group is outside the previous clipboard and seven-animation-resource passes.

The DIB description and TIFF checkbox have no translation defect identified in this bounded model linguistic/source review. The TIFF description preserves the English meaning but shares an unqualified file-size assurance: **F01 remains open**. Lossless Deflate does not guarantee that every output is smaller. This finding is a source/specification qualification, not an observed runtime size regression or a pt-BR-specific mistranslation.

No translation, application or test code is changed. No tests, builds, CI dispatches, Android/emulator/device checks or native-speaker review were performed. The register retains **475 rows, 3 structural rechecks completed and 472 pending**. No parent row is closed or narrowed by this supplement.

## Exact identities and nonduplication

- Accepted develop: `80c14372b0504bc44f9f2809ad477247fdc8100b`; tree `d9858229f98068bef9c6194c90d77610c5ecceec`.
- [English resources](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/res/values/strings.xml#L564-L566): blob `576616126cd8b12f5ddfcb4f97e61341b337413c`.
- [pt-BR resources](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/res/values-pt-rBR/strings.xml#L592-L594): blob `1d60f1400d503409c28134ed4460febdcf102008`.
- [Historical correction](https://github.com/c933103/AN-Paint/commit/595bedb6050064a5c37704eac16b3f6f46042c86) versus parent `614f54a5dccfe806f5d8f9fc50d9f722da2f8d93`: the two descriptions changed; the checkbox did not. The exact before/after text is in [dispositions.json](dispositions.json).
- All three resulting values are exactly equal at that correction, PR7 head `730319aea40eb205d18c894c496e500d6f660ac6`, accepted develop, and integration `b60f5830f30af5c243e5a6084e917c9cfd844678`. This verifies only these values, not the whole rewrite or P07-009.
- PR7's retrieved full public discussion contained 10 records through [comment 6095494460](https://github.com/c933103/AN-Paint/pull/7#issuecomment-6095494460). Neither that discussion nor the authoritative register contained a TIFF/DIB/Deflate/key-specific bounded review. Empty repository search results were not treated as proof of absence; unpublished work and other conversations are not covered by this negative finding.

[Source evidence](source-evidence.json) records immutable paths, blob identities, inspected excerpts and primary references. [UI states](ui-states.json) contains three source-composed expectations, not screenshots or Android output.

## Individual contextual dispositions

### TD01: formats22_tiff_compression

Current text: **Compressão sem perdas (Deflate)**

The label distinguishes lossless storage from lossy quality and retains Deflate as the algorithm name. Esri's own [pt-BR GIS glossary](https://support.esri.com/pt-br/gis-dictionary/lossless-compression) attests “compressão sem perdas”; Adobe's [Brazil-localized compression guide](https://helpx.adobe.com/br/photoshop/desktop/save-and-export/export-files-to-different-formats/file-compression-in-photoshop.html) also uses “compactação sem perdas”. These support terminology without requiring AN Paint to copy another product.

[SaveOptionsDialog](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L63-L105) exposes this checkbox only for TIFF, initializes it from `initial.tiffCompressed`, and [passes its checked value](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L187-L197) into the save request. [ImageExporter](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageExporter.kt#L11-L23) forwards that boolean to TiffCodec. [Native encoding](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L499-L516) selects Deflate versus no compression while supplying the same opaque RGB sample values.

**Disposition:** no translation defect identified within this review. This does not establish actual selected-language routing, screen-reader behavior or rendered checkbox layout.

### TD02: formats22_tiff_description

Current text: **Salva uma página RGB. A compressão reduz o tamanho do arquivo sem alterar os pixels; desative-a para criar um TIFF sem compressão.**

“Salva” is supported by [Adobe's Brazil-localized TIFF save wording](https://helpx.adobe.com/br/photoshop/desktop/save-and-export/save-files/save-large-documents.html); it is not necessary to treat the earlier “Guarda” as inherently wrong. In this model review, “uma página” preserves singular output, “desative-a” has the feminine antecedent “compressão”, and “criar um TIFF sem compressão” clearly describes unchecking the checkbox. No placeholders are present.

The description is selected for TIFF regardless of checkbox state. The encoder receives one bitmap, creates one TIFF directory, uses three 8-bit RGB samples, and rejects nonopaque pixels. The lossless claim concerns compression of that opaque RGB input, not preservation of arbitrary original-file metadata, transparency or source bit depth. See [output finalization](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L381-L408) and [encoding](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L480-L521).

**Disposition:** the translation relationship is supported, subject to shared F01 below. Full acceptance is withheld.

### TD03: formats22_dib_description

Current text: **Salva um DIB do Windows de 24 bits sem compressão. Use BMP se o aplicativo de destino exigir um cabeçalho de arquivo BMP.**

The rewrite repairs the earlier “a aplicativo receptora” agreement with “o aplicativo de destino” and preserves conditional advice through “se ... exigir”. “Cabeçalho de arquivo BMP” is the relevant distinction. It does not say a DIB lacks every kind of header.

[DibCodec](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/DibCodec.kt#L27-L41) calls [LegacyImageEncoder.dib](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/LegacyImageEncoder.java#L37-L70). The encoder writes a 40-byte BITMAPINFOHEADER, one plane, 24-bit pixels, BI_RGB=0, bottom-first BGR rows and four-byte row padding. DIB omits the 14-byte BMP file header; BMP emits it before the same DIB payload. Microsoft documents the distinct [BMP file header](https://learn.microsoft.com/pt-br/windows/win32/api/wingdi/ns-wingdi-bitmapfileheader) and [DIB information header/uncompressed RGB](https://learn.microsoft.com/pt-br/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader).

**Disposition:** no translation defect identified in the reviewed statement. Actual compatibility with a receiving application is untested; this does not promise transparency preservation or compatibility with every recipient.

## F01: qualify the shared TIFF file-size assurance

English says “Compression reduces file size” and pt-BR says “A compressão reduz o tamanho do arquivo”. The encoder explicitly [allows for worst-case Deflate growth](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L488-L489), and the inspected encode path does not generate two outputs and select the smaller one. [RFC 1951 section 1.1](https://www.rfc-editor.org/rfc/rfc1951.html#section-1.1) explains that lossless compression cannot shorten every possible input and that Deflate can expand data.

The model/source inference is that the wording should not be read as an unconditional size guarantee. A minimal future wording review could consider **“can reduce” / “pode reduzir”**, preserving lossless compression, singular RGB page and the unchecked/no-compression operation. This is proposed wording, not a translation edit or accepted cross-language repair. Applicable existing language copies still need individual examination; no claim is made here that every locale repeats the same assurance. No whole-TIFF expansion percentage or observed failing fixture is asserted.

F01 is recorded as an open child finding within this supplement. Resolution needs a supported shared wording decision, affected-catalogue review and validation at the actual candidate revision. It does not require promising an automatic smaller-output fallback.

## Existing test evidence versus unperformed validation

Only test definitions were read:

- [ExportFormatDialogTest](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/test/java/org/catrobat/paintroid/local/ExportFormatDialogTest.kt#L207-L237) checks TIFF compression state through format switches, hidden DIB controls, and export/provider state. This does not attest to pt-BR prose rendering.
- [TiffCodecTest](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/androidTest/java/org/catrobat/paintroid/classic/TiffCodecTest.kt#L85-L104) defines uncompressed/Deflate opaque-pixel round trips and compression-tag assertions. It does not assert that compressed output is smaller.
- [Packed-DIB test](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/tools/test_packed_dib.py#L40-L57) defines header/payload equality and pixel decoding assertions, including padded widths. Its “headerless” test naming means omission of the BMP file header, not omission of the DIB information header.

No historical test success is inherited. A feasible later validation should:
1. Recheck the exact candidate's resource values and resolve F01 consistently in default English and individually inspected applicable catalogues.
2. Run relevant existing codec/dialog checks; compare TIFF compression tags, page count and decoded RGB pixels for both options. Measure representative repetitive, very small and high-entropy fixture sizes without asserting an always-smaller result.
3. Verify DIB's 40-byte header, 24-bit BI_RGB layout, BMP/DIB payload relation and opaque pixel round trips across padded widths.
4. Render actual pt-BR TIFF checked/unchecked and DIB dialogs; inspect wrapping, accents, checkbox label/accessibility, hidden controls and selected-language resolution. Exercise format switching, Choose location, provider cancellation/reopen and Cancel without unintended export. Keep emulator, physical-device and linguistic attestations distinct.

These are remaining validation requirements, not actions executed or new engineering tasks launched by this report.

## Original-scope recovery and remaining limits

The [partially recovered original scope](https://github.com/c933103/AN-Paint/blob/548bc966ea062613a0087d1127698ca11ecd9caf/verification/ptbr-animation-recheck-2026-10-10/README.md#partial-original-scope-recovery-10-october-2026) continues to govern: independent review of inherited translations, applicable shared-fix propagation, individual full recheck and no carryforward of rejected progress. PR7 covers English variants, pt-PT, pt-BR, Italian, Greek and Turkish; completion of the other 81 locales is outside this reset.

No owner-specific TIFF/DIB word-choice instruction was recovered in this pass. Complete latest-thread and alternate-branch reconciliation remains open. This report supplies source/model evidence only; it does not assert a native-speaker requirement or attestation, runtime acceptance, full pt-BR acceptance, P07-007 completion or closure of the broader reset.
