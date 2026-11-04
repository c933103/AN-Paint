# Image tray and sorting: Old English and Old Norse

Base commit: 3e6e3f8f0ad15f74d90491208b05b8cb98d9b492.

Adds 15 previously absent P2 strings to each offered `ang` (Ænglisc) and `non` (Norrœna) catalogue. Independent semantic review accepted all 30 unchanged. The batch covers image addition and prerequisites, thumbnail dragging/tapping, horizontal tray navigation, filename and modification-time sorting, missing timestamps and fixed/remaining capacity limits.

AssemblyActivity's tray, import checks and sort selector, AssemblyCanvas's empty-workspace prompt and ImageAssembly's sort labels/model limit were inspected. The 20-image limit applies to the whole assembly. The full-capacity instruction removes an image from the assembly before adding another; it does not direct deletion of the original file. The dynamic capacity argument is the number of additional images still allowed, followed by choosing fewer files.

Thumbnail sorting remains distinct from repositioning canvas images. The filename labels preserve both A–Z and Z–A directions. Date labels explicitly refer to modification time rather than image creation, and the unavailable-time caption remains a missing timestamp in its current card context. Thumbnail terminology describes small previews, not resized replacements for originals. Application behavior is unchanged.

Validation passed:
- Exact English and target base Git identities; offered picker entries; XML parsing and duplicate-name checks; exactly 15 additions per locale; all 424 previous entries, attributes and surrounding bytes unchanged.
- Android escaping/formatting, source attributes, exact typed placeholders and newline parity. Literal 20-image bounds, sort-direction markers and the remaining-capacity `%1$s` argument are unchanged. Both limit messages use the same translated first sentence.
- 78 host tests: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery.
- Structural catalogue validation passed for all 171 offered options. All 1,276 materialized tracked base files matched their Git blob identities and executable modes. The 161 unmaterialized research/verification documents are retained unchanged in the publication tree and were not needed by these checks.

Each locale changes from P2 81/305 to 96/305, leaving 209 P2 keys absent. P0 remains 94/94, P1 249/249 and P3 0/71. These are direct-key-presence counts, not whole-catalogue quality ratings. The priority manifest is unchanged.

Vocabulary follows current image, assembly, preview, filename, change, tap, scroll and add terms. [Bosworth-Toller](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/d0188.html) attests endebyrdan for arranging/putting in order. Thumbnail and modification-time expressions are technical adaptations, not claims of historical computing vocabulary or full-sentence attestations.

Limits: no historical-language specialist certification, whole-catalogue linguistic acceptance, Android build, device/rendering check or CI result is claimed. Canonical Android resources own current wording; this evidence is not a wording freeze.
