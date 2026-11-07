# Colour-profile import error misidentifies ICO and DIB as BMP/GIF

**Status:** Open bug; documentation-only issue-style tracking PR. This is not an implementation or fix claim. Keep the PR open/draft until the defect is resolved through separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Verification:** independent linguistic/static-source review only. No runtime, device, rendering, CI, native-speaker or whole-language acceptance is claimed. Repository Issues are disabled; this open PR is the durable bug record. [Project board](https://github.com/c933103/AN-Paint/pull/39).

## Expected and actual

Expected: when an imported image has a colour profile AN Paint cannot convert, the error accurately describes the input format or uses format-neutral language while retaining the colour-managed sRGB PNG workaround.

Actual: `save20_unsupported_tagged_colour` says “This BMP or GIF uses a colour profile that AN Paint cannot convert yet. Convert it to sRGB PNG in a colour-managed editor before importing.” ICO and DIB import paths also emit that resource, so those inputs can be misidentified as BMP/GIF.

Impact: misleading format identification during a real import failure can confuse diagnosis and conversion. This report concerns the explanation, not a demonstrated failure of the rejection or colour-conversion protection. No claim is made that every arbitrary image format uses this error. The same source-scope defect is shared across faithful localizations.

## Static reproduction and evidence

- [English resource L637](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L637); [French L653](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L653); [Japanese L656](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L656). The [French independent review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182425420) records the full pairs and this source-context blocker.
- [DibCodec.kt L13–24](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/DibCodec.kt#L13-L24) wraps a packed DIB as a temporary BMP, checks its colour metadata, and translates `UnsupportedColour` into this message at L20–21. The user's selected input remains a DIB.
- [IcoCodec.kt L19–21](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/IcoCodec.kt#L19-L21) catches unsupported colour metadata from selecting an ICO entry; [L47–50](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/IcoCodec.kt#L47-L50) does the same during DIB-entry decoding. Both use the BMP/GIF wording for the ICO input.
- [PlatformImageColour.kt L112–117](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PlatformImageColour.kt#L112-L117) also wraps `LegacyColourMetadata.UnsupportedColour` with this shared resource.
- [ImageImport.kt L120–124](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageImport.kt#L120-L124) routes detected DIB input through `DibCodec.withBmpFile`. ICO is handled by `IcoCodec`.

## Bounded fix and acceptance

- Use a format-neutral message (“This image …”) or correctly pass the actual input format at every emitter. Do not name only BMP/GIF when ICO/DIB paths share the message.
- Preserve profile rejection and its original exception cause; do not silently import with incorrect colours or remove the colour-managed sRGB PNG recovery instruction.
- Add representative unsupported-profile BMP/GIF, packed-DIB and ICO-entry import cases. Verify the actual error path and correct/neutral description, including both ICO entry selection and DIB-entry decoding where independently reachable.
- Keep supported-profile/sRGB import controls working. Verify error propagation and that failed imports do not replace the current document.
- Enumerate all call sites and localized instances. Update and independently review each affected supplied locale, including English/French/Japanese and fallback behavior; test any introduced format placeholder end to end.

## Next action and dependencies

Choose neutral wording or a correctly parameterized actual-format design, enumerate all localized values and emitters, implement the bounded change, then verify source-bound codec/import regressions and the repository's current-source review/test gates. Coordinate the exact English/localized re-review with translation PR56 before adding accepted-current credit. This bug is independent of the New-image and Japanese PDF wording bugs. This tracking PR changes no app code, codec behavior, resources or tests.
