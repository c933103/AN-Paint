# Translation runtime boundaries

Translation strings are display data. Code continues to use resource IDs, enum
values, provider identities and explicit action/view tags. Normalize's preset
buttons now have `normalize_smallest` and `normalize_largest` tags even when the
captions are identical or change language. Gallery actions continue using JSON
quoted labels and `textContent`; translated labels never select action URLs.

## Guarded resource consumers

`ui`, `uiRoot`, `uiQuantity` and context-specific `uiText` share `LocaleText`.
All nine formerly direct `String.format(..., ui(...))` consumers and the crop
plural consumer use this boundary. `uiRoot` retains invariant numeric/hex
formatting; other callers retain their resource locale. Plain percent signs and
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

## Canonical fallback and builds

The JDK-only `tools/SourceTextResources.java` generator derives reserved
`anpaint_source_` resources from `values/strings.xml` during `preBuild` for all
variants. XML text, attributes and structure are preserved except resource names,
source-to-source alias references and deliberately marking these reserved entries
`translatable="false"`. A second generated resource file carries the source
`formatted` contract, including alias targets and each plural form. `UiText`
passes it explicitly to the formatter; `formatted="false"` text, including
incidental `%d`, `% s` or `%1$s`, is never parsed or interpolated. Source format
templates require explicit argument indices; unmarked literal percent text must
be declared `formatted="false"`. AAPT still decodes escapes/markup and
validates the package. The generator rejects reserved names across every configured application/library
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

Android layout, fonts/shaping, accessibility, finite memory, very large argument
values, the OS, native code and non-translation application defects retain their
own limits. No claim is made that arbitrary text can never cause any error, or
that these tests prove every language/layout/device.
