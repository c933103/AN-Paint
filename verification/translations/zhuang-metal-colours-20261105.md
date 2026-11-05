# Zhuang: named metallic palette colours

Date: 2026-11-05 (UTC). Base: `3096581e7bdbd17f4e235e43b0449b210c593011`, tree `59f794b30054a3e03f1afeec1a853a71a06a1a42`.

## Change and independent review

Added missing P2 `ui_gold`, `ui_silver` and `ui_copper` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 222 previous typed resources remain unchanged. Canonical XML owns current wording.

Independent review retained all three colour terms. Gold has direct dictionary attestation, silver has direct published colour usage, and copper is a transparent composition with narrower confidence in idiomaticity and compound spelling. Native-human approval is not a gate or a claimed certification.

Sources checked directly:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): S.htm 6/52 explicitly gives the fused `saekgim` as golden colour and `saek` as colour; G.htm 41/110 gives `gim` as gold. N.htm 37/72 gives `ngaenz` as silver and also money; D.htm 82/110 gives `doengz` as copper. The OCR's proofreading limitation remains relevant.
- [Guangxi Minzu Bao, 27 September 2023, page 5](https://www.guangximinzubao.cn/szbzw/page/21/2023-09/27/05/2023092705_pdf.pdf), the article *Bet Nyied Cibngux Ngonz Ronghndwen* / 中秋赏月, uses the fused `saekngaenz` to describe silvery moonlight. This directly supports the colour sense, rather than relying on the money sense or a search snippet.
- [The Guangxi language commission's ninth terminology announcement, 3 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), entry 155, independently uses the gold and silver nouns. It does not standardize these palette labels.

The gold/silver compounds retain their attested fused spelling. The copper compound follows that parallel construction using the independently supported copper noun. A bounded search did not establish direct fused or spaced copper-colour attestation; that absence is not proof of an error or a reason to substitute bronze. Copper's compound usage remains the specific linguistic uncertainty.

## Actual consumer boundaries

`AdvancedColourDialog` associates zero-based custom slots 1/2/3 with gold `#FFD700`, silver `#C0C0C0` and copper `#B87333`. `CustomColours` independently has the same default order and numeric values. These are names for flat RGB swatches, not metallic texture or shine effects.

`customLabel` uses the translated default name only when both slot and stored colour exactly match its corresponding default. Otherwise it uses the separate numbered custom-colour resource. The entire name is followed by a colon and six-digit uppercase hexadecimal value. This full label supplies each occupied custom swatch's accessibility description and the replacement list shown when the palette is full. The saved-palette heading is generic and does not display these individual names. Basic swatches also use a different, hex-based description.

Selecting a stored swatch loads its numeric colour and refreshes the editor. Palette persistence and replacement use slot indices and numeric colours, not translated names. Removed slots use the empty-slot description; a named colour stored in a different slot does not acquire a metal name merely by RGB equality. Separate custom/empty/heading resources remain unchanged and may still use English fallback. No palette, persistence, layout or rendering implementation changes are included.

## Verification

- Fresh remote head and complete tree matched the preceding verified publication. All **1,259 materialized files** matched base Git blob hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,528 base leaves.
- All 222 existing nodes, attributes and prefix bytes are preserved; three missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literal tokens pass. New XML Git blob: `2c545acb6f87920ac67c537e20f80f5b895dca10`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 8.697 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Six host Java literal-label cases passed**, covering these three entries in English and Zhuang.
- Targeted token-aware source checks passed for the three live resource bindings, matching numeric defaults, exact slot/colour naming predicate, full name-plus-hex return, swatch accessibility and replacement-list consumers, generic heading, and numeric selection/persistence boundaries. These inspect source; they do not execute Kotlin/Android flows. A temporary harness assertion initially treated tokenized Kotlin as a string; it was corrected to use the token matcher and rerun successfully, without changing production code.
- Existing `ANPaintControlsTest` cases for selecting the silver default, saved-slot persistence and replacement were inspected, not executed in this batch.

Zhuang now has **225 typed resources**: P0 **69/94**, P1 **132/249**, P2 **24/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,359, P2 30,105, P3 7,481; 46 options have complete presence. Presence does not establish fluency or runtime coverage. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback.

## Limits

No Android SDK was configured and no Kotlin compiler was available in this executor. Android build/AAPT, executed palette selection/replacement/persistence, device rendering/layout, font and accessibility checks were not run. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and wording mirrors are not published.
