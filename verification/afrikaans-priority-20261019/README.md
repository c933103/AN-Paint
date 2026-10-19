# Afrikaans P0/P1 linguistic review, 19 October 2026

Application PR: [AN Paint #140](https://github.com/c933103/AN-Paint/pull/140). Reviewed application head: `bf56a676a6a59ca791fe8eccf0816d80ed52177e`, tree `e2c9f12a7b3b2c1df47b2520a92b78075f4b010f`. English, priority manifest, before-values and consumer context are bound to develop `798e6159939fa06beb27755700a1320a5970cb7b`.

## Review coverage and changes

All **341 P0/P1 strings** were compared as complete English/Afrikaans pairs: **92 P0 + 249 P1**. Dispositions are **299 retained with inspected static references, 28 wording-only retained, 9 requiring re-review, and 5 corrected**. The 376 P2/P3 identities are outside this batch. Static references do not prove that every branch is currently reachable. Retained decisions are model-based and generally moderate confidence; they do not imply native-speaker acceptance.

The five corrections restore the actual language-picker fallback explanation; add the incomplete encoding operation's object; fix the saved-image sharing-options warning; translate the remaining English lossless term consistently with the existing checkbox; and label pixel count in a count-neutral form. Full before/after values and surrounding source appear in [corrections.json](corrections.json).

Each of the 341 rows in [afrikaans-p0-p1-review.json](afrikaans-p0-p1-review.json) has its priority, full English/before/final text, value hashes, disposition, individual reasoning and discovered consumer references. [entry-dispositions.tsv](entry-dispositions.tsv) is the compact human-authored decision list. [source-binding.json](source-binding.json) records source blobs and the exact four-file application delta. The reviewed manifest and English resource were not changed.

[Independent challenge](independent-review.md) accepted all five proposals with zero required revisions and zero blocking findings. Its two optional alternatives concern encoder repetition and compact lossless terminology. That challenge covers five corrections only. The author's subsequent custom-title location clarification and one-pixel boundary analysis are distinguished from the independent review.

## Unresolved entries

Values remain unchanged for these nine entries:

- `gallery_credit_could_not_save`, `gallery_credit_too_large`, `legacy_credits_unreadable`: attribution-credit terminology needs confirmation.
- `save20_gif_description`: specialist treatment of “Dithering” remains open.
- `ui_sampled_resize_memory_explanation`: subsampled-decoding terminology remains open.
- `ui_the_draft_is_saving_try_again_shortly`: generic busy credit-attachment use may not mean draft saving; source-context hold retained.
- `ui_foreground_background_colour_palette`: no direct consumer establishes the third placeholder's grammatical referent.
- `ui_hex_rrggbb`: terse hexadecimal abbreviation needs terminology confirmation.
- `ui_main23`: bare “Hoof” has no current consumer establishing its noun/referent.

Existing CN Help, Hakka/Wu and processing-label holds remain unchanged. No earlier withdrawn review is restored, no PR56 aggregate counter advances, and no P2/P3, English-source, other-catalogue or application-logic changes are included.

## Verification at this snapshot

- Focused host regression: **7 passed**.
- Complete normal host suite: **992 passed**, 233.976 seconds, exit 0.
- Complete optimized host suite: **992 passed**, 221.454 seconds, exit 0.
- Changed Afrikaans XML compiled successfully with AAPT2.
- Complete remote application tree was compared with the reviewed local files: **1,228 leaf content/type/mode matches**, exactly four intended changes, no removals. Base and final remote tree responses are retained in the raw ZIP.
- Local Gradle stopped before compilation because downloading Gradle 8.13 failed with `Network is unreachable`. This is preserved as blocked, not passed.
- Five authored Robolectric methods cover actual dimension controls, full language-picker explanation and Cancel, three real encoder failure paths with source preservation and a successful PNG control, repeated lossless toggles and Cancel, and compiled sharing-warning formatting. The sharing check does not open an external provider.
- Hosted [run 39240946949](https://github.com/c933103/AN-Paint/actions/runs/39240946949) remains in progress at this snapshot; exact-script generation passed. Hosted JVM execution, lint, APK and API35 checks are pending. Later PR receipts supersede this timestamped status rather than rewriting this historical evidence.
- [Codex code review receipt](https://github.com/c933103/AN-Paint/pull/140#issuecomment-6265607100) completed on exact head `bf56a676a6` with no findings. Any readiness-triggered review is a separate later state.

[checks.json](checks.json) records commands, results and limitations. [raw-checks-and-tree-proof.zip](raw-checks-and-tree-proof.zip) retains focused, normal, optimized, blocked Gradle and AAPT2 logs plus full remote-tree metadata. Synthetic negative-fixture JSON after unittest `OK` is expected diagnostic output, not an aggregate failure. The two whole host processes briefly overlapped; their timings are not isolated performance measurements. [artifact-manifest.json](artifact-manifest.json) supplies byte sizes and SHA-256 values for the source evidence and raw archive.

This record makes **no installed Afrikaans layout, TalkBack, physical-device, native-speaker, whole-language or release acceptance claim**. Test code is not test execution. Machine-format/placeholder and AAPT2 results do not establish linguistic fluency.

## Publication structure

This is an additive evidence ref parented to the reviewed application commit. Bulky review records and logs are kept out of the application PR. The app branch contains only the Afrikaans resource and three compact test/fixture additions. Full retained content/type/mode equality must be checked before publishing the evidence ref as well.
