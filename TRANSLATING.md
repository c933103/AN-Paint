# Translating AN Paint

The new editor, its tool names and hints, image assembly, colour and sizing dialogs,
export choices, status messages, accessibility descriptions and licence-viewer
buttons use Android string resources in
`Paintroid/src/main/res/values/strings.xml`. The complete English source is kept in
that single catalogue so translation-service exports map cleanly to one
`strings.xml` catalogue per Android language directory.

Localized `strings.xml` files are generated: edit the matching locale in
`translations/local-translations.json`, or `translations/basic-translations.json`
for a starter catalogue, then run `python3 tools/reuse_upstream_translations.py`.
Do not edit generated XML alone; regeneration would replace those edits. Keep
all generated entries for a locale in its single `strings.xml` (for example,
`values-fr`, `values-ja`, `values-zh-rTW`). When importing Crowdin output, merge
its reviewed entries into the appropriate JSON catalogue before regenerating.
Register language names, aliases and translation bases in
`translations/language-options.json`; new full catalogues may also need a
qualifier in the generator. Missing entries fall back to English. Translation
work does not normally require Kotlin edits. Existing vocabulary and exact
provenance are in `translations/README.md`.
The app language can be chosen under View → Languages independently
of the device language; Android 13 also exposes the same setting in system settings.
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
- Pixel values remain exact. Decimal entry accepts the selected app language's decimal separator
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
and landscape controls under an RTL locale. Shared terms now reuse actual upstream
translations, while new messages retain English fallback.
It checks that the sidebar toggle and colour palette stay attached and that
native submenus still run their commands. This is layout and resource-readiness
coverage, not a complete Arabic translation. `AppLanguageTest` checks persisted
language choice, localized number entry, Android 13 integration, and preserving the
current canvas, undo and selection during a language change. Human review and device
checks at larger font sizes remain part of completing each future translation.


## Action review and vertical foundations (0.0.23)

The shared vocabulary is reviewed by command meaning. AOSP Android 15's pinned
clipboard/Cancel labels supplement Paintroid; explicit Discard changes and Keep
editing labels distinguish the unsaved-change outcomes. See
[translations/ACTION-REVIEW.md](translations/ACTION-REVIEW.md), the exact source
records and Apache-2.0 licence there. The generator retains the corrected Japanese
flip labels and does not edit the pinned upstream files. Host checks reject
resource duplicates and colliding discard/cancel outcomes.

There are 104 offered locale variants, including English, plus device default.
The Literary Chinese (`lzh-Hant`) and traditional Mongolian (`mn-Mong`) resources
are initial foundations with English fallback; native-speaker review remains
welcome. Their ribbon labels and inserted text use the vertical renderer. Native
Android dialogs/edit fields keep platform layout. The Mongolian font is bundled
unmodified with its original OFL; no font licence is inferred from upstream use.
