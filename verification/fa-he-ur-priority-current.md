# Persian, Hebrew and Urdu priority successor

Stacked base: `2e58204c73ff24ea9b73fbaf4d265baa1e0c3fce` (#221); does not mutate that candidate or earlier inputs.

Each locale has a complete 341-row P0/P1 inventory plus 16 necessary companions. Canonical offered options are `fa`, `he`, `ur`; Hebrew uses Android's legacy `values-iw` directory, not an added `iw` option. Persian `fa-IR` is not included.

Independent full source/current/proposed review and author second-check are preserved at [87b6bab](https://github.com/c933103/AN-Paint/tree/87b6babebb85b5507ba860ecf4d7504f2c9d8ff4/verification/fa-he-ur-priority-20261029). Frozen author packets remain at 5953b5ea174c1848b3cd8c2dbcc966ae7d3efe14. All production Kotlin consumers and all three predecessor catalogues are byte-identical between the packet base 246f2bb and this stacked base.

FA and HE have 349 accepted rows and 8 holds each. UR has 345 accepted rows, four exact independently reviewed revisions accepted by the author, and 8 holds. Source edits: FA 255 additions/7 replacements, HE 254/12, UR 310/12. Existing accepted wording is carried without duplicate recovery credit. AI/static linguistic/context review is not native-human fluency, visual RTL certification, or whole-language completion.

Eight holds per locale remain: formats22_derived_exported, ui_save_as, ui_save_as_jpeg, ui_save_as_jpeg_xl, ui_save_as_png, ui_foreground_background_colour_palette, ui_main23, ui_pinch_and_pan_mode. Existing held values remain unchanged; absent holds remain absent. Dormant strings have wording-only acceptance, not live-route claims.

Tests preserve complete typed values, Android attributes, aliases, placeholders, plural quantities and negative mutation checks. JVM coverage exercises real crop reset without apply, both dimension unit compositions, exact compiled plural counts, dirty-document Keep editing without save/discard, fill tolerance slider and squared-ARGB boundary behavior, memory refusals, recovery bytes, export request settings and canvas clipping/Undo. The encoder sentence is covered by the complete compiled-value oracle; this does not claim a newly simulated native encoder failure. Shared memory/SVG/colour expectations use only finite exact absent-predecessor additions; historical combined-input colour checkpoint remains 148 direct/23 fallback, then this trio makes 151 direct/20 missing-source values. Android resolves the absent `fa-IR` key from generic `fa`: runtime accounting is 151 direct + 1 parent-inherited + 19 English. This does not edit or linguistically accept the regional catalogue.

Local JVM execution is not a pass: installed wrapper distribution/SDK are unavailable in this workspace. Hosted exact-head CI and Codex review remain required; local host results and asynchronous run links are reported separately. No release, signing or access change.
