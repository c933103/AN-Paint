# Recovery notices: Romanized Southern Min

Base commit: 7b2250d0fb339ea21936b2ea14748a580182d698.

Adds two direct nan-Latn-TW notices. Independent review accepted the drafts with sún-hoāi replacing sún-hōai in both notices and pó-chûn replacing chhû-chûn in the preserved notice. These exact corrections were applied to matching semantic segments and regenerated strings. All menu captions and other wording remain unchanged.

Validation passed:
- Exact current base resource identity and offered-option membership; all previous string attributes/text preserved; only the two requested entries added.
- XML parsing, duplicate-name, Android quoting/format, exact menu, placeholder, ZIP and canvas.png checks. One %1$s only in the preserved notice.
- Both notices preserve possible damage OR unreadability, joint ZIP-opening AND readable-image preconditions, and keeping even an unopenable copy. Preserved guidance retains conditional resizing; exported guidance retains unchanged contents and unverified possible settings OR selection.
- 78 host tests passed: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural coverage includes all 171 offered options.

Limits: this is direct Romanized Southern Min coverage, distinct from its Han-script option and inherited fallback. No native-speaker certification, build, device, font/combining-mark rendering or CI result is claimed. Structural checks do not imply whole-catalogue translation completeness.
