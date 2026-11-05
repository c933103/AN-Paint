# Zhuang text input and placement

Base: `c728c9f3d83455d7f609a69439714e85ed9ea700` on `review/nv-bottom-2038-20261103`.

Adds two missing P1 strings: the text-input hint and text-placement dialog title. All 173 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review accepted both compositions at moderate confidence. They use written characters/text as the noun, resolving the two omitted keys from the [previous size batch](zhuang-pixel-size-20261105.md) without relying on its unsupported bare-noun draft. Existing text/add-text labels remain unchanged; this does not establish that their terminology is wrong.

[Contemporary classroom prose](https://www.guangximinzubao.cn/szbzw/html/2025-12/03/content_55130.htm), paragraph 28, directly attests `sij cih` as ordinary writing alongside reading and drawing. [Tang Long's lexical discussion](https://www.guangximinzubao.cn/szbzw/html/2014-12/24/content_11479.htm) explicitly presents the character noun and write verb. The latter evidence was retrieved in indexed article text; direct extraction omitted its body. The dictionary's classifier and word senses alone were not treated as unqualified proof of abstract text.

[Published narrative](https://www.guangximinzubao.cn/zw/f_282584/646040.html), paragraph 27, supports the placement verb through putting bowls in a cupboard. Applying ordinary writing to keyboard entry and placement to written material on a canvas are contextual extensions. No exact placement phrase or established software terminology was independently attested. Bare character wording does not specify a single character, a single line or Chinese-only writing. The stronger direct support for the input phrase should not be confused with proof of the whole digital-placement composition. No native-speaker certification is claimed.

## Consumer and targeted checks

- `TextStyleDialog` uses the input string only as the editable field's hint. It retains the initial text, multiline input, two-line minimum display and 8192-character input limit. The hint is not inserted as document content.
- The placement string is the dialog title. Cancel and add-text action labels remain separate and unchanged.
- The canvas text-tool callback supplies coordinates to `ClassicPaintActivity.showTextDialog()`. Submission passes the complete input and selected settings to `document.text()`; the dialog dismisses only when its commit callback succeeds. Blank document text is a no-op. These are source observations, not executed text insertion or save tests.
- 61 host tests pass: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass structural checks. Four English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks identify both consumers and their actual hint/title roles, multiline settings and document callback. They do not execute Android input, glyph rendering or persistence.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 256 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 175 resources: P0 68/94, P1 107/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,386 to 1,384; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed text operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
