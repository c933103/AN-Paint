# Swedish priority review, 19 October 2026

## Bounded result

Source baseline: [`798e6159939fa06beb27755700a1320a5970cb7b`](https://github.com/c933103/AN-Paint/commit/798e6159939fa06beb27755700a1320a5970cb7b). Implementation: `33ba9f34dfa39aa2780635818edb2a98dc9d4f8b`, tree `51a1e991e0125ba61384b1e35142dedf7f1569e5`. Its parent `01e0af12` has the identical Swedish wording; the successor only makes the host test explicitly require every expected fixture key.

193 complete English/Swedish values were read and challenged individually:

- 103 existing P0/P1 values: 18 corrected, 84 retained, one left uncertain.
- 90 new translations: all 83 missing P0 values, six P1 route/accessibility companions, one P2 lower-bound animation-count dependency.
- Exact priority coverage after this bounded patch: P0 92/92 present; P1 100/249 present. The 149 remaining P1 entries are explicit English fallbacks and were not linguistically reviewed here. Presence is not acceptance.
- `string/ui_main23` retains `Huvud`: no production consumer determines whether Main means main menu, start, or general. This is an open context/idiom question, not accepted-current credit.
- Other entries with no found production consumer have wording-only judgments, recorded individually. `FG` and `BG` remain compact conventions with full Swedish colour labels elsewhere; no broad terminology certification is claimed.

The [per-entry ledger](review-ledger.json) binds the exact source SHA, English and before/final Swedish value hashes, correction/new/re-review counts, reasons and static consumer lines. Whole-language and native-speaker acceptance are false on every entry. The historical PR56 checkpoint records zero Swedish receipts; its counters and held tracker branch were not changed. All conclusions withdrawn by the September reset remain withdrawn.

## Actual changes

`Rad` (row) becomes geometric `Linje`; untranslated Watercolor/Outline become `Akvarell`/`Kontur`; Solid fill becomes `Enfärgad fyllning`. `Fortsätt redigera` now names the dirty-document continuation rather than generic Cancel. Swap wording explicitly exchanges colours. App-language and fit-view labels are clarified. File format is `Filformat`, covering both image formats and Base64/ASCII text exports.

New safety text preserves saved/export destination distinctions, draft/recovery preservation, uncertainty, memory limits, no-automatic-resize statements, only-first-frame import, PNG poster selection, and irreversible loss cautions. Recovery routes match `Arkiv`, `Exportera återställningskopia`, `Spara som` and `Öppna bild` exactly.

Independent challenge corrected terminology consistency and idiom in proposed GIF, clipboard, share-dialog, cache and encoding-process wording. `Gitter` is an attested Swedish dithering term, not a mistranslation; this patch uses `Färgutjämning` to match the existing option in the same AN Paint dialog. The [Adobe Swedish documentation](https://helpx.adobe.com/se/animate/using/save-for-web-options.html) confirms the former term. These lexical references do not substitute for the complete-value review or certify this UI.

The application branch changes seven files: one Swedish XML, one compact current-wording fixture, one Swedish Python contract test, one six-case real-consumer JVM test, and three existing tagged-colour test/oracle files. Translating the P0 colour-profile warning required replacing Swedish's old explicit-English expectation with its exact reviewed Swedish value. All other locale expectations and fallback checks remain enforced.

All 1,228 final application leaves were compared by path, content Git SHA and executable mode with the remote tree. The 1,225 baseline leaves are retained, one production XML is modified, and three new fixture/test files are added; other modifications are tests/oracles. No CN Help, Hakka/Wu or paused processing-label resource is touched.

## Checks and limitations

- Eight focused Swedish host checks pass, including complete statements, all placeholders/attributes, mutation rejection, command-reference consistency, localized lower-bound frame counts and preserved safety qualifications.
- Fourteen existing localization-contract checks pass after adding the Swedish tagged-colour expectation.
- Initial normal and optimized full-host attempts each ran 993 tests and had exactly two errors in the old Swedish-English tagged-colour oracle. Both raw attempts are retained. They were not successful aggregate runs.
- After the bounded oracle repair, 993 normal and 993 optimized host checks passed. Those runs loaded the test module before the later test-only explicit-inventory tightening; the final eight focused checks passed after that tightening. New exact-head full-suite runs are in progress and will have separate receipts. The successful earlier aggregates are not relabelled as exact-final-test-source runs.
- Local Gradle stopped while downloading the official Gradle 8.13 distribution with `java.net.SocketException: Network is unreachable`, before compilation. No local JVM, AAPT, lint, APK or device execution is claimed.
- Six authored JVM cases exercise real tool-category descriptions, picker Cancel, repeated Save/Export/Share open-and-Cancel flows, exact/lower-bound animation warnings and cancellation, the actual New-image unsaved guard, and the actual shape-style chooser. They are not runtime evidence until their hosted source run passes.
- No installed Swedish layout, TalkBack, physical-device, native-speaker, full-language or release certification. No merge is implied by source publication.

Historical tracker: [PR56](https://github.com/c933103/AN-Paint/pull/56), read only. [PR75](https://github.com/c933103/AN-Paint/pull/75) is the distinct crop-guidance tracker and receives no unrelated Swedish counter update.
