# AN-W05-C04: Commons metadata-only Copy credit failures

Base: `43148951ac6bd23687e66685855909ac538ba004`, verified exact tree
`ab5ff7fe6d04d5e22348b979c9e0054eef9b1c0f`.

## Bounded correction

The real Commons WebView Copy credit action calls `copyCommonsCredit`, which
fetches file metadata, caches the returned snapshot and copies its attribution.
It does not download/render an image or register an insertion. Its three catch
routes nevertheless referred to image loading, image inspection or the image
colour converter.

This patch gives those routes three complete resource messages:

- `commons_credit_copy_failed`: “Could not copy image credit.”
- `commons_credit_copy_failed_reason`: “Could not copy image credit: %1$s”
- `commons_credit_copy_out_of_memory`: “Not enough memory to copy image credit.”

Exceptions with a nonblank message keep that message verbatim as the argument,
including whitespace, percent signs and provider/framework text. Null, empty and
whitespace-only messages use the reasonless message. Linkage errors use the same
reasonless message; no unverified converter cause or exception class is exposed.
Allocation errors name the copy action.

Clipboard rejection retains the existing localized operation-failed notice.
Metadata success still copies `record.text(imported=false)`, keeps source/licence
links and the provider's field identities/values, and does not rewrite existing
edited credits. All download/import catches, image validation, attribution
validation, storage behavior, cancellation and duplicate-action guards remain
unchanged. No live provider requests, credentials, fonts or Work tasks are used.

## Translation disposition

`translations.json` contains the three full messages in the default resource and
the established 59 exact catalogues, plus an explicit list of the remaining 81
picker tags. Those 81 retain genuine default-English fallback and are incomplete.
The 59-tag set includes existing English variants and two layout fixtures; it is
not a claim of 59 independently reviewed natural languages.

Wording reuses the repository's established credit/attribution, copy and memory
terminology. The candidate received assistant review for meaning, placeholders,
script consistency and Android quoting. Independent competent-language review is
not available and native fluency/acceptance is not claimed, particularly for the
minority-language and historical-script variants. Structural checks cannot supply
that review. No added character is new relative to its previous full catalogue.

The complete translated wrapper does not translate appended English reasons.
`remaining-english-reasons.json` individually retains the ten Commons metadata
reasons (including the guarded defensive precondition), the original-file redirect
reason and the PNG-encoding reason. Those twelve original application-authored
reasons remain open. PR29 already translated the two SVG-size reasons; PR31's
import notes and PR32's Help are unchanged.

## Verification and limitations

- `tools/test_commons_copy_credit_errors.py` checks exact values, the 59+81
  disposition, unchanged pre-existing resource strings, placeholder/quoting
  rules, unchanged semantic source files, catch confinement and regression routes.
- `CommonsCopyCreditTranslationTest`: Android resource resolution for all 140
  picker tags at APIs 30 and 35, including literal percent/placeholder-looking
  text inside the runtime reason.
- `CommonsCopyCreditErrorTest`: API35 actual WebView Copy credit route with fake
  HTTP, malformed JSON, response/field limits and metadata-validation failures, provider/framework detail, absent/blank
  reasons, allocation/linkage failures, clipboard rejection, duplicate taps,
  destruction during a pending metadata failure, and retry success. Each failure/retry verifies metadata-only
  requests, unchanged edited credits, no insertion result or image-file creation.
- The same route measures French, Arabic, Nôm, Mongolian and Manchu messages at
  320×640 dp and font scales 1×/2×, including accessibility text, horizontal/RTL
  wrapping, vertical column reachability and persistence. It emits 30 diagnostic
  host-rendered screenshots and geometry records under
  `Paintroid/build/reports/commons-copy-credit-errors/` when run successfully.
  These are Robolectric NATIVE host captures, not installed-device screenshots.

Local Android execution is **blocked before compilation**: Gradle 8.13 is not
cached, its distribution download fails with “Network is unreachable”, and no
Android SDK is installed. The supplied Android tests are unrun locally, not
passed. GitHub CI is required to establish compilation, actual-route results and
readability. `host-results.txt` records the independently run Python contracts;
`local-gradle-blocker.txt` records the bootstrap failure. No claim of a complete
language audit or full installed-device verification is made.

## Coordination

The only shared production file with PR33 is `MediaGalleryActivity.kt`: PR33
changes the navigation arrow; this patch changes only the Copy credit catches.
No PR33 test or evidence file is edited. Root owns integration and merges.

## Separate inherited follow-up: AN-W05-C05

The Hungarian `gallery_copy_credit` label is currently `Jóváírás másolása` in
`Paintroid/src/main/res/values-hu/strings.xml`. Independent review identified
`Jóváírás` as financial-credit wording rather than attribution/source credit.
This is an inherited label issue, left unchanged here and recorded as a separate
open terminology correction. The new C04 failure messages correctly use
`forrásmegjelölés`; they should not be changed to match that inherited label.
