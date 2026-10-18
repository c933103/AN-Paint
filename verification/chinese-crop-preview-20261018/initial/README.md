# Bounded TW/CN crop-preview warnings

## Scope and source

Base: `2ad195f1cc79e9190f26581bb1254a88008a28b6` (develop, checked 18 October 2026).
Application head: `fc0e71c30a9bfd0422c134d426535c4d70b96059`.
Application tree: `3b84956dd6427f8a88d71e270922a4477e307bc0`.

Only `plurals/ui_crop_preview_images/other` changes in the TW and CN canonical XML catalogues. The complete old/new values are retained in `reviewed-values.json`. Both old values were checked byte-for-byte before editing. Every preceding preview/apply sentence, all three positional integer arguments, multiplication sign, unit and escaped newline are unchanged. HK, all Help values, other catalogues, production logic, existing tests and workflow caps remain unchanged. Two new test files are added.

The remote tree was compared to every checkout file and executable mode before CI publication: all 1,215 tracked blobs/modes match, exactly four intended files differ from the base, and no existing path was removed. See `source-scope.json`.

## Independent complete-value review

An independent source/linguistic review on 18 October 2026 accepted the complete proposed TW and CN plural values. It compared the current whole plural at resource lines 678–680, the production `ImageCropDialog.kt` consumer at lines 85–94, `ImageAssembly.kt` crop operations at lines 154–159 and layout at lines 197–218, and `AssemblyModelTest.kt` lines 254–272.

The old `也會重新調整` / `也会重新调整` presents readjustment as expected. The replacements `連接到它們的圖片可能會移動。` / `连接到它们的图片可能会移动。` explicitly say the images attached to the cropped images may move. This is consistent with a RIGHT child's unchanged position after an orthogonal crop and changed position after cropping the relevant dimension, while retaining attachment metadata. The existing regression also covers BOTTOM attachments and Undo/Redo.

The Taiwan Ministry of Education dictionary defines 可能 in terms of possibility and illustrates 可能會: https://dict.concised.moe.edu.tw/dictView.jsp?ID=17980&la=0&powerMode=0 . This is supporting lexical evidence, not authority for unrelated catalogue wording.

The independent review inspected source/tests; it did not itself execute tests. It does not establish native-speaker, whole-language, installed glyph/layout, TalkBack or physical-device acceptance.

## Regressions

- Four Python contracts assert both complete values, exact `other` structure, all source placeholder types, escaped newline and Android escaping. Negative controls reject old categorical wording, lost preview text, damaged argument type, removed modality and missing/extra forms.
- `ChineseCropPreviewTest` checks compiled quantities 0, 1, 2, 3, 20, 21 and 101 against independent complete expected values and all formatted arguments.
- Separate TW and CN methods select the exact regional app locale, open the real batch-crop toolbar with two synthetic decoded PNGs placed as a parent/attached child, and compare complete displayed and accessible status text across two/zero/one/all selections, a real text-watcher trim update, reset, Cancel and reopen.
- Cancelling and reopening must preserve assembly metadata, every layout rectangle, persisted project bytes and original image bytes. The 15-second synthetic-preview readiness deadline is unchanged from the established helper pattern.
- Existing full-text, lifecycle, resource, corruption, geometry, CI/device assertions and caps are not relaxed. New test code is not runtime evidence until its exact-source hosted reports are verified.

## Open follow-ups

The CN complete assembly Help value and eight Sinitic varieties remain separate unreviewed work: `yue-Hant`, `yue-Latn`, `hak-Hant-TW`, `hak-Latn-TW`, `nan-Hant-TW`, `nan-Latn-TW`, `wuu-Hans`, `lzh-Hant`. Review must consider selected-versus-placed ambiguity and the specific target variety, rather than mechanically copying Mandarin. HK is already qualified.

These limits are recorded in tracker75: https://github.com/c933103/AN-Paint/pull/75#issuecomment-6249510704 . Existing tracker obligations, PR56 and explicit holds remain unchanged.

## Local results

All 946 host checks passed in ordinary Python and again with `python3 -O`. Four focused Python tests and canonical catalogue structure passed. `--complete` correctly reports the pre-existing untranslated fallback catalogue scope and exits 1; it is not a completeness pass.

Focused JVM execution was attempted with the repository Gradle wrapper and a writable temporary Gradle home. It stopped before compilation because the uncached Gradle distribution could not be downloaded (`SocketException: Network is unreachable`). No local Kotlin/JVM, native build, Android lint, device or render execution is claimed. Exact-source hosted results will provide those gates where applicable.

The raw logs are retained in `local-evidence.zip` with a per-file SHA-256 manifest. Expected negative-fixture errors inside the successful host logs are not actual Android runs; suite summary and process exits establish the host outcomes.
