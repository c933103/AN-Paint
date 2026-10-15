# Japanese language-picker note omits fallback guidance and adds a coverage claim

**Status:** Open active semantic-language bug; documentation-only issue-style tracking PR. No correction is applied. Keep open/draft until a separately reviewed resource change and acceptance evidence resolve it.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. Two independent reviewers agree on the complete-entry source/translation mismatch. Verification is linguistic/static source only; no runtime/device, layout, whole-language completeness or translation-quality certification is claimed. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56).

## Expected and actual

Expected: `language20_translation_note` identifies “App language” and explains that translations are maintained in AN Paint's language resources and that new or untranslated text appears in English.

Actual Japanese: “この言語では、AN Paint の翻訳対象となるすべてのインターフェース文字列を収録しています。” It replaces the title and both source explanations with a statement that this language contains every translatable interface string.

Impact: the actual app-language picker omits the explanation users need when English fallback appears and substitutes an unrelated coverage assertion. This report does not establish that the current Japanese catalogue lacks keys; key presence, translation quality and faithful rendering of this note are separate matters. The defect is the unsupported semantic substitution/omission, not a measured missing-string count.

## Source evidence

- [English values/strings.xml L625](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L625): `App language\n\nTranslations are maintained in AN Paint’s language resources. New or untranslated text appears in English.`
- [Japanese values-ja/strings.xml L648](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L648): the complete current coverage statement above, with no placeholders.
- [AppLanguage.kt L135–149](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt#L135-L149) constructs this note as the actual custom title for the in-app language chooser. It is not an unused resource. Android's separate system picker is outside this finding.

## Proposed correction and acceptance

Independently agreed complete replacement, not applied:

> アプリの言語\n\n翻訳は AN Paint の言語リソースで管理されています。新しいテキストや未翻訳のテキストは英語で表示されます。

- [ ] Apply the exact Japanese title/explanation while retaining literal Android `\n\n` paragraph escaping and the no-placeholder contract.
- [ ] Verify the actual in-app language-picker custom-title branch selects the complete Japanese text with heading, resource-maintenance explanation and English-fallback explanation.
- [ ] Keep language selection, device-default behavior, saved preference and locale recreation unchanged; do not alter the catalogue or fallback implementation to make the old sentence true.
- [ ] Run structural/resource and focused picker-title tests; inspect wrapping/accessibility only if those checks are actually executed and record their limits.
- [ ] Independently re-review the entire final value/context and source-bound receipt before updating translation acceptance counts.

## Next action and dependencies

Apply the bounded resource correction and verify the actual custom-title use against the current integration source. Coordinate with the Japanese review and active language-choice work; this historical baseline does not certify new locale inventories. This PR changes only this documentation, with no application/resource/test edits, merge or release.
