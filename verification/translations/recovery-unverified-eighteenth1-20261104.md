# Recovery notices: Kabyle

Base commit: 6bd0a7fcc29ebcfdca2680c461ff9f60dca45b4d.

Adds two direct Kabyle notices. Independent review accepted them with the shared uncertainty clause changed to: Ahat agbur-is yerreẓ, neɣ ahat ur yezmir ara ad yettwaɣer. The correction explicitly marks both damage and unreadability as possibilities and is applied to both notices and their matching semantic segment.

Validation passed:
- Exact base resource identity and offered-option membership; old string attributes/text unchanged; exactly two requested entries added.
- XML parsing, duplicate-name, Android quoting/format, exact menu, placeholder, ZIP and canvas.png checks. One %1$s only in the preserved notice.
- Possible damage OR unreadability, joint ZIP-opening AND readable-image preconditions, and keeping even an unopenable copy preserved in both notices. Conditional resizing remains in preserved guidance; unchanged export and unverified possible settings OR selection remain in exported guidance.
- 78 host tests passed: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural coverage includes all 171 offered options.

Limits: direct coverage is separate from inherited fallback. No native-speaker certification, Android build, device, rendered UI or CI result is claimed. Structural checks do not imply whole-catalogue translation completeness.
