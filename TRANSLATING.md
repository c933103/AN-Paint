# Translating AN Paint

The new editor, its tool names and hints, image assembly, colour and sizing dialogs,
export choices, status messages, accessibility descriptions and licence-viewer
buttons use Android string resources in
`Paintroid/src/main/res/values/strings*.xml`. `strings.xml` contains the main
catalogue; smaller companion files contain later additions and follow the same
resource rules. Include all of them when preparing a translation.

Add a language by creating `res/values-<Android language qualifier>/strings.xml`
with the same resource names. Matching companion filenames may be kept or merged
into that locale's `strings.xml`. Examples: `values-fr`, `values-ja`, `values-b+zh+Hant`.
Missing entries fall back to English. A translation does not require Kotlin edits.
`crowdin.yml` is available for a maintainer's own translation project; automated
uploads to the upstream Catrobat translation project are not enabled.

- Preserve positional placeholders such as `%1$s`, `%2$d` and `%3$.2f`. They can
  move within a sentence; their number and type must stay unchanged.
- Translate every applicable Android plural category (`one`, `other`, and any
  additional categories required by the language); keep the count placeholders.
- Keep escaped newlines (`\n`), escape apostrophes (`\'`) and XML characters, and
  preserve `%%` where a formatted message contains a literal percent sign.
- Translate complete menu labels and messages. Menu routing, tool names in saved
  drafts, view tags, filenames, MIME types and asset paths remain stable identifiers.
- Entries marked `translatable="false"` are fixed export filenames. Font brand
  names come from the licensed font inventory and should remain recognizable.
- Legal licence texts and copyright notices are preserved verbatim. Translate
  their navigation labels; keep the original legal notices available.
- Pixel values remain exact. Decimal entry accepts the device's decimal separator
  as well as a decimal point. Test numeric fields in the target locale.
- Numeric slider labels use a complete positional format string rather than
  concatenating a setting name, punctuation and a number. A translator can change
  their order; Android formats the number for the locale.

Run `:Paintroid:testDebugUnitTest` and `:app:lintDebug`, then check both orientations,
short screens, collapsed panels, dialogs and screen-reader labels on Android.
For right-to-left languages, also check directional gestures, aligned toolbar
controls and filename/path display. The image workspace keeps physical left/right
geometry: landscape tools stay left with options opening right; portrait tools
run across the top with options opening below. The colour palette stays attached
to its indicator and opens to the right.
Canvas coordinates, image rotation, assembly attachments and direction arrows
must not be mirrored just because the surrounding text is right-to-left.

`TranslationReadinessTest` exercises Arabic-digit numeric entry and the portrait
and landscape controls under an RTL locale, using English fallback resources.
It checks that the sidebar toggle and colour palette stay attached and that
native submenus still run their commands. This is layout and resource-readiness
coverage, not an Arabic translation. No particular human translation was requested
for this update. Human translation review and device checks at larger font sizes
remain part of adding each future language.
