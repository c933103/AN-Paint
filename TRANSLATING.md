# Translating AN Paint

The new editor, its tool names and hints, image assembly, colour and sizing dialogs,
export choices, status messages, accessibility descriptions and licence-viewer
buttons use Android string resources in
`Paintroid/src/main/res/values/strings.xml`.

Add a language by creating `res/values-<Android language qualifier>/strings.xml`
with the same resource names. Examples: `values-fr`, `values-ja`, `values-b+zh+Hant`.
Missing entries fall back to English. A translation does not require Kotlin edits.
`crowdin.yml` is available for a maintainer's own translation project; automated
uploads to the upstream Catrobat translation project are not enabled.

- Preserve positional placeholders such as `%1$s`, `%2$d` and `%3$.2f`. They can
  move within a sentence; their number and type must stay unchanged.
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

Run `:Paintroid:testDebugUnitTest` and `:app:lintDebug`, then check both orientations,
short screens, collapsed panels, dialogs and screen-reader labels on Android.
For right-to-left languages, also check directional gestures, aligned toolbar
controls and filename/path display. Translation readiness does not mean that
human translations or every language's layout have already been verified.
