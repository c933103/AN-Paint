# Translation runtime boundaries

Translation strings are display data. Code continues to use resource IDs, enum
values, provider identities and explicit action/view tags. Normalize's preset
buttons now have `normalize_smallest` and `normalize_largest` tags even when the
captions are identical or change language. Gallery actions continue using JSON
quoted labels and `textContent`; translated labels never select action URLs.

## Guarded resource consumers

`ui`, `uiRoot`, `uiQuantity` and context-specific `uiText` share `LocaleText`.
Formerly direct `String.format(..., ui(...))` consumers and the crop plural
consumer use this boundary. The current numeric-display callers retain their
selected resource locale; `uiRoot` remains available only for intentionally
invariant formatting. Plain percent signs and
Unicode text (including RTL controls, Mongolian separators and supplementary
characters) are data, not a format program.

For formatted messages, the translated template must preserve the source's
argument indices, types, multiplicities, flags, width and precision. Argument
order may change. Literal `%%` and `%n` may vary with the wording; they do not
consume arguments, but still undergo syntax, token-count and expansion bounds.
Missing/blank translations, malformed formats, mismatched
contracts and oversized translated templates fall back to the complete English
source. No warning/action clauses or user arguments are truncated. If the caller
itself omits a required value or supplies the wrong type, only that source slot
becomes `?`; the rest of the English message remains intact. A present null
retains Java Formatter's existing conversion behavior; an omitted argument is
detected by its index rather than being confused with null.

Templates are limited to 65,536 UTF-16 units, 128 formatting tokens, width 1,024
and precision 128 before formatting. These limits exceed the current default
catalogue's needs. Source formatting contracts are checked during generation;
a legitimate future source change outside them needs an explicit bound review.
Arguments are not reinterpreted as format strings. Their size is not capped or
silently modified, so this is not a universal heap/output-size guarantee.

`tools/check_translation_boundaries.py` checks production Kotlin and Java across
packages and source sets, including present generated trees. Raw printf calls
outside `LocaleText` must use code-owned literal templates; dynamic aliases must
go through the shared boundary. Formatted Android string access and raw plural
access belong in `UiText`. The guard handles multiline calls, callable/import
aliases and Kotlin string interpolation. It distinguishes string-key storage
access from Android resource formatting. This is a conservative lexical policy,
not interprocedural type analysis; custom source roots outside the conventional
trees must be supplied with `--source-root`.

## Long vertical labels

Cluster, sideways-run and word assembly copy completed text with builders or
substring boundaries instead of repeatedly concatenating a growing string.
Vertical wrapping retains measured completed runs while continuing to shape
adjacent sideways text together, including Mongolian suffix separators. This
removes the identified repeated copying and completed-run processing without
changing the text supplied to drawing or the existing cluster rules.

Fixed ribbon tiles already shorten their drawn captions when necessary. Captions
of at most 64 clusters retain exhaustive prefix fitting. Longer captions use
logarithmic probes and at most 64 local refinement probes, and only return a
candidate actually measured to fit. With nonmonotonic shaping this may select a
shorter prefix than an exhaustive search. If even a tested ellipsis cannot fit,
the tile draws no caption ink. The complete control text, accessibility text and
tooltip remain available. Fitted captions are cached by text, geometry, direction
and the paint's text-measurement settings. Shaping cost inside Android remains a
platform limit; these changes do not claim a universal runtime or heap bound.

## Canonical fallback and builds

The JDK-only `tools/SourceTextResources.java` generator derives reserved
`anpaint_source_` resources from string/plural entries across `values/*.xml` during `preBuild` for all
variants. XML text, attributes and structure are preserved except resource names,
source-to-source alias references and deliberately marking these reserved entries
`translatable="false"`. A second generated resource file carries the source
`formatted` contract, including alias targets and each plural form. `UiText`
passes it explicitly to the formatter; `formatted="false"` text, including
incidental `%d`, `% s` or `%1$s`, is never parsed or interpolated. Source format
templates require explicit argument indices; unmarked literal percent text must
be declared `formatted="false"`. AAPT still decodes escapes/markup and
validates the package. Format validation recognises four-digit Android Unicode
escapes in a separate view of the text, including encoded percent signs and
numeric fields. Escaped backslashes are consumed once; a backslash produced by
a Unicode escape is not decoded again. This closes the encoded-format bypass
without rewriting resource text. It is not a complete AAPT whitespace/quoting
decoder: the source validator retains conservative spelling rules and requires
four hex digits even where AAPT accepts a shorter trailing escape.

The generator rejects reserved names across every configured application/library
Android source-set resource root, including variant overlays. Discovery runs after
all projects are configured, tracks absent/new roots and XML inputs, excludes only
its own generated directory, and orders the existing mirror producer before
validation. It also rejects dangling/cyclic aliases, unsupported source references, malformed or
unbounded source format contracts, and incomplete English plural forms.

Only English plural selection uses an English configuration context, and it
looks up the reserved source resource ID. No selectable English catalogue,
private emoji catalogue or test locale supplies fallback wording. Source aliases
and plural references cannot resolve back into translated resources. Generated
resources are build output, not translation inventory, priority or completion
entries. There is no manually maintained second catalogue.

Missing source IDs, invalid resource IDs, corrupted packaging and invalid XML
remain build/programming errors. The runtime fallback does not make invalid XML
packageable or weaken any existing full-text, linguistic, layout or build gate.
A syntactically valid translation can still be wrong or omit an important clause;
only the independent translation reviews and complete-text contracts can assess
that. Fallback does not grant linguistic acceptance.

## Verification and remaining limits

Pure JVM tests cover malformed placeholders, unsupported conversions, indices,
types/null/missing values, percent signs, long text and arguments, preserved
numeric locales, Unicode and 2,500 seeded mutations. The production JDK generator
is executed by host tests, including alias/plural/reserved-name negative controls.
The existing hosted resource-graph probe also checks source generation ordering,
unchanged builds, clean debug/release, release-first, derivation, input changes and
stale-output removal, plus an expected failed build for a reserved ID in an
application debug/English overlay.

Robolectric boundary tests inject malformed text *after resource decoding* in
English/Arabic/French/Japanese/Mongolian contexts and exercise actual formatting,
plural and dialog consumers. Repeated preset changes, cancel, reopen and apply
preserve action identity. These injections are distinct from installing an APK
with deliberately malformed translations. The gallery DOM fixture and Android
JSON checks cover quote/backslash/newline/U+2028/U+2029 labels and repeated setup.

Real packaged resources exercise all 18 existing Ainu/Manchu escaped-percent
templates. The Japanese crop consumer checks the restored single `%` in each
edge's accessibility description. The targeted historical wording audit and
retained encoding repairs are recorded in
[the compatibility review](TRANSLATION_COMPATIBILITY_REVIEW.md).

Android layout, fonts/shaping, accessibility, finite memory, very large argument
values, the OS, native code and non-translation application defects retain their
own limits. No claim is made that arbitrary text can never cause any error, or
that these tests prove every language/layout/device.
