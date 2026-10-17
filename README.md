# English assembly Help: snapping and Exact position

Tracker: [AN Paint PR75](https://github.com/c933103/AN-Paint/pull/75).
Application commit: [fcdb417dddd5cba516eea661e917f0183ed61d46](https://github.com/c933103/AN-Paint/commit/fcdb417dddd5cba516eea661e917f0183ed61d46).
Base: develop `44ad5ce2156fef79baae3ef5650b9ac5eac06202`.
Verified application tree: `c34f14d55fcb590066522d50be077cf6968430e5`.

## Complete bounded change

Ten English assembly Help values now distinguish snapping from Exact position. Origin and overlap rejection explicitly apply when snapping; a separate paragraph explains selected-image, zero-based whole-pixel top-left coordinates, unchanged other positions, and allowed overlaps. Unplace guidance now says that other images stay placed and attached images may move to fill the gap. Qualified crop guidance remains intact.

Inventory: default English; en-001; AU/CA/GB/IN/SG/US; en-XV plain-English vertical test; qaa-Zsye-XV emoji-English. The two vertical variants also receive the missing same-entry crop-plus-normalization dimension and conditional memory-floor guidance. Emoji-English references the full current decorated control labels. No other resource key or application/model/crop/placement code changed. Help remains P3.

[Complete-entry review](review-complete-help.md) records the meanings and consumers of all eight paragraphs. The ZIP contains complete old/new values, source comparisons, tests/logs and validation details.

## Separate source-binding re-review receipt

[other-language-source-bindings.json](other-language-source-bindings.json) explicitly records 50 other-language Help overrides requiring complete-entry/source-binding re-review, plus 112 English-fallback routing rechecks. Previous full-Help acceptance is not carried across the changed English source. The values remain unchanged pending their own review. Bounded unchanged crop plural and unrelated-key evidence is neither enlarged nor silently withdrawn. Held PR56 and existing language/rendering holds are untouched. No whole-language approval is claimed.

## Checks

- 898 host tests passed normally (203.010 s) and optimized (201.925 s).
- 65 focused tests passed normally and optimized, including five new mode/full-value host tests, 120 malformed/old-claim controls and existing affected contracts.
- All ten restored old complete English values are rejected by the new oracle.
- Canonical catalogue structural validation passed; git diff whitespace checks passed.
- AAPT2 compiled and linked all resources plus supplementary mirrors of the two existing exact-script generation inputs.
- Changed AssemblyActivityTest and its existing helper sources compiled with Kotlin 1.9.24/API35, freshly generated resource symbols and previously compiled dependency classes. This is supplementary compilation, not a clean Gradle build or Robolectric execution.
- Full local Gradle unit/lint execution was attempted but stopped at the Gradle 8.13 distribution download with `Network is unreachable`. APK/native/lint/device execution is not claimed locally. Exact-head hosted CI remains required.
- Initial host runs failed five assertions because existing tests still assumed the English output paragraph index and Korean/English Help newline parity. Their failures are retained. English source indexes were updated; Korean seven-paragraph values remain exactly guarded while their new full-Help/source-binding re-review requirement is explicitly recorded. The subsequent whole suites passed without dropping assertions or changing translated resources.
- Initial supplementary compile omitted an existing helper source. The failure is retained and resolved by including EditorStartupTestSupport.kt; production/test logic was not weakened.

New actual consumer tests exercise full native/vertical Help and toolbar labels, nonzero first exact placement, overlap while preserving others, exact-parent Unplace/Remove, snapping origin and overlap rejection, possible snap gap filling, Undo/Redo and original bytes. Existing model, invalid input, cancellation and reopening controls remain. The tests are authored and compiled; hosted execution is still pending. Full pixel visibility, glyph shape, TalkBack and physical-device rendering are not certified.

All 1,191 base blobs were verified by content/mode; all 1,193 final remote leaves match the candidate. The entire application diff is 17 paths: ten Help resources, one existing Android test, four existing host-test source-binding adjustments, one new whole-value fixture and one new host test. No removals, priority changes, production-code changes, PR56 changes, credentials or unrelated private data are included.
