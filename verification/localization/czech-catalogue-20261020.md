# Czech catalogue completion, 20 October 2026

Original review base: `d7436b3df842b9be9aa12be622ebc88ed8e8e2b9`, including
the corrected English assembly Help from PR #122. Integrated onto develop
`7243bac3225fa9aa45be919e2eb3332b9fa5a40a` after 0.0.40 publication. This
is a separate unpublished candidate, not a change to the 0.0.40 APK or release
inputs. The work is bounded static translation work, not whole-language,
native-speaker, installed-device or layout certification.

## Application changes

- Add 343 of the 344 missing resource identities, including Czech `one`, `few`
  and `other` crop forms, complete active editor and assembly Help, gallery and
  Commons guidance, image/PDF/export diagnostics, exact position and crop tools.
- Correct eight previously unreviewed labels: freehand smoothing, pixel-edge
  antialiasing, quality with its percent unit, Use image, Copy credit, colour
  wheel, ASCII art and colour dithering. Quality retains `formatted="false"`.
- Preserve the exact 321 prior source/target pairs with bounded acceptance and
  the 31 existing explicit holds. Source/context evidence is not inferred from
  catalogue presence or placeholder checks.
- Catalogue presence becomes **716/717**. The one missing runtime resource is
  the dormant legacy manual `ui_the_arrow_on_the_left_directly_below_the`.
  Its complete Czech proposal is retained against a separately identified
  proposed English correction, not silently installed against stale English.
- Seventy-one identities have no direct current Kotlin/Java/XML consumer. Their
  wording status is separate from context status. The prior `ui_fit` layout
  concern also remains open. No caller, interaction or layout was invented.

## Scope and regression coverage

The global 59-locale historical contract is unchanged. Family-specific fixtures
explicitly add Czech only where full current values are available and reviewed;
this does not accept the whole locale or remove unrelated fallback obligations.

The compact fixture checks complete critical strings, attributes, formatting,
plural forms and key behavioral distinctions. Mutation cases reject missing,
duplicate, truncated, marked-up and format-altered strings. Host checks also
preserve actual menu routes, all eight assembly Help paragraphs, overlap-mode
separation and retained-source/legal identifiers.

The new `CzechExtendedWordingTest` exercises compiled resource resolution, all
12 Commons failure branches with untouched provider details, actual crop-dialog
one/few/other transitions and repeated cancellation, exact-position validation
and state preservation, and PDF/TIFF chooser validation/cancellation. The
existing real editor Help/provider-picker test additionally selects Czech.

## Current-base composition

- All 717 English current-source values and all 716 installed Czech values
  exactly match the original independent review. Its 645 bounded accepts and
  72 holds are preserved without counting repeated review as new acceptance.
- Of 892 recorded consumer lines, 891 are unchanged. Independent narrow
  supplements accept the changed pixel-grid tooltip/Help callback and the new
  shared `Done` dismiss-control context. The latter is production-gated to
  vertical profiles, so it does not establish a new reachable Czech screen.
- Shared message-family fixtures retain Swedish and add Czech. The original
  59-locale/112-fallback global scope and separate SVG review classifications
  remain unchanged. The corrected Commons credit flow oracle is retained.
- Exact-position tests select the real app language and process locale, wait
  for dialog listeners, check both fields and preserve supported invalid input
  verbatim. Negative cases use the actual Czech locale/filter signs; this
  translation change does not claim to fix arbitrary Unicode-minus handling.
- No production code or other-language resources change. Published 0.0.40
  version, request, notes and signing inputs remain byte-for-byte unchanged.

## Verification limits

The Czech resource compiled successfully with aapt2. Full local Android
execution stopped before compilation or JVM tests because downloading
Gradle 8.13 failed with `Network is unreachable`. JVM, lint, APK, emulator,
installed-device, large-font and accessibility acceptance therefore remain
unrun locally; authored test code is not a passing runtime result.

Final independent-review binding, host results and durable evidence are recorded
in the associated PR. Source-only or proposed-source entries retain their
explicit holds; a present string is not automatically a context acceptance.
