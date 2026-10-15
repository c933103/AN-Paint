# Japanese assembly help makes always-shown tray content provider-dependent

**Status:** Open semantic-language bug; documentation-only issue-style tracking PR. No correction is applied. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independent full-entry linguistic/static-source review, not runtime/device, rendering or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56). Issues remain disabled; settings/visibility are unchanged.

## Expected and actual

Expected: Japanese assembly help says the tray displays thumbnails, filenames and adjusted image dimensions, while modification timestamps are available when supplied by the provider.

Actual: the first paragraph of `ui_add_up_to_20_images_with_android_s` moves “提供元から取得できる場合” before the entire list, making thumbnails, filenames, dimensions and timestamps all conditional on provider availability.

Impact: users are told that normal tray content depends on optional provider metadata. This is a clause-scope translation error; no missing thumbnail, filename or dimension rendering is demonstrated or alleged.

## Static evidence and proposed correction

- [Japanese long help L236](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L236) versus [English L21](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L21). English conditions the modification times only.
- [AssemblyActivity.kt L137–157](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L137-L157) creates the thumbnail and filename views, displays placed/cropped/normalized dimensions, and separately uses optional `item.timestamp` with a time-unavailable fallback.
- [Metadata lookup L206–214](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L206-L214) initializes a filename fallback and nullable timestamp, and treats provider metadata as optional.
- The long help is displayed by [AssemblyActivity.kt L341](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L341). Two independent reviewers agree on the full-entry correction; the other paragraphs were retained after source/context review.

Replace this sentence only:

> 下部のトレイには、提供元から取得できる場合、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法、ファイル更新日時が表示されます。

With:

> 下部のトレイには、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法が表示されます。提供元から取得できる場合は、ファイル更新日時も表示されます。

The proposal is not applied here. Preserve every other character/paragraph unless separately reviewed.

## Bounded fix and acceptance

- Correct the conditional's scope without changing tray/provider behavior.
- Verify the actual full Japanese help resource, preserving all unrelated paragraphs, escaping and line breaks.
- Exercise tray content with absent optional modification time/provider metadata: thumbnail/name fallback/dimensions remain available, while the existing timestamp-unavailable behavior remains. Include a present-timestamp control and cropped/normalized dimension checks.
- Run structural/resource and focused assembly tests; independently re-review the entire exact Japanese entry in context before updating its acceptance receipt.

## Next action and dependencies

Apply the bounded Japanese sentence replacement, then whole-entry resource/context validation and current-source review/test gates. Coordinate with the ongoing Japanese review and active assembly PR67 at its eventual source baseline; do not infer acceptance of changed assembly behavior from this historical source check. Distinct from French placement/attachment semantics. This PR is documentation only, with no runtime or correction-completion claim.
