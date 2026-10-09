# PR #30 native vertical-caption comparison

These are **new PR #30-specific original captures**, not the historical PR #29
archive. Twenty personally inspected PNGs and their twenty paired JSON records
are preserved byte-for-byte. `manifest.json` gives source heads, Actions runs,
artifact SHA256, original paths and every constituent hash. The downloaded source
ZIP hashes were verified before extraction. None of these PNG/JSON bytes matches
any held PR #29 capture constituent; that separate archive is not duplicated or
claimed complete here.

## What changed

The first PR #30 source head `0a2d19d` painted the entire provider/help description
twice because one atomic vertical ReplacementSpan crossed a native paragraph
break. [Correction 79dd199](https://github.com/c933103/AN-Paint/commit/79dd199d6ee9dc19af67ecd67ce806f26c1d0274)
uses one space at that separator only for the vertical caption. Every word and
accessible source text remains, and horizontal descriptions retain their newline.
No shared renderer, font or translation changes were made.

The corrected captures come from exact head `9043849`, whose vertical regressions
passed on both API30/35. They visibly show a single description sequence and the
single status sequence. The regression also requires the exact description text,
one native paragraph, the shared vertical span, full source accessibility text,
column reachability endpoints and reset after message replacement.

## Paired images

For each of these five shared vertical profiles, both folders preserve:
- API35, 2× text, `commons_svg_original_size_unavailable`
- API30, 1× text, `commons_svg_original_size_too_large`

Profiles: `mn-Mong`, `mnc-Mong`, `lzh-Hant`, `en-XV`, `qaa-Zsye-XV`.
They cover shared left-to-right and right-to-left columns, native and pseudo
captions, and both real SVG error paths. Images were inspected for the duplicate
painting correction and unrelated/private content. No fluent-language acceptance
is claimed; existing genuine translation fallback is retained.

Example before/after:

| Sample | Before | Corrected |
|---|---|---|
| Mongolian API35 2× | [PNG](pre-correction-0a2d19d/api35-mn-Mong-font2.0-commons_svg_original_size_unavailable.png) | [PNG](corrected-9043849/api35-mn-Mong-font2.0-commons_svg_original_size_unavailable.png) |
| English vertical pseudo API30 1× | [PNG](pre-correction-0a2d19d/api30-en-XV-font1.0-commons_svg_original_size_too_large.png) | [PNG](corrected-9043849/api30-en-XV-font1.0-commons_svg_original_size_too_large.png) |

## Boundaries

These are Robolectric NATIVE host captures, not installed-device screenshots.
Scrollable columns and lower controls can extend beyond the initial viewport.
Their static appearance alone does not establish complete action reachability.
The separate all-catalogue matrix passed 1,680 cases, but the full representative
reachability gate was still failing at a no-op host WebView frame and is being
corrected in the test fixture. Real-provider evidence is the installed French/
Mongolian 2× portrait/landscape test, not the blank browser area in these PNGs.

The source branch remains separate from this evidence branch. This record is
provenance and scoped visual evidence; it does not authorize PR #30 merge.

[Fourth-run complete host evidence and installed transition failure](fourth-ci-b37782d/README.md)
adds 21 reviewed action/search captures, all case identities and artifact hashes.

[Final passing exact-head receipt](final-ci-9bbfad5/README.md): 706 JVM tests, lint
zero issues and 94 installed tests, with verified capture equivalence and real
font transition/browser records. Historical failures remain preserved.

[Validated keyboard-action correction and exact reviewed-head boundary](ime-ci-03abccd/README.md)
preserves the new current-head CI, real EditorInfo records and precise delta since
the Security-reviewed head, without claiming an unverified distinct Security result.
