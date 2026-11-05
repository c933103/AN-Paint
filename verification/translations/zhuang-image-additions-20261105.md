# Zhuang: add assembly image inputs

Date: 2026-11-05 (UTC). Base: `30766671f3c107711a95ef82820ddac4907122b5`, tree `301a5f80980bf783b6fddca259707fcd4983f416`.

## Change and review

Added P2 `ui_add_images` and `ui_add_images_first` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 215 previous typed resources are unchanged. Canonical XML owns current wording.

Independent review accepted both with medium-high confidence for their bounded purpose. The verb means add/increase, not place or select; the prerequisite notice puts “first” before that action. The unquantified image noun does not require multiple inputs. These are newly composed UI sentences, not quotations or claims of standardized software phrasing. Residual idiomatic/register uncertainty remains; native-human approval is not a gate or a claimed certification.

Evidence directly checked:
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), D.htm 45/110: `dem` means add/increase and is used transitively. S.htm 29/52 supplies `sien`, first. G.htm 18/110 gives a bulb-changing instruction with `sien gven`, supporting “first” before the verb, not just an isolated gloss. The dictionary warns of incomplete OCR proofreading. Dialect alternatives listed beside these entries do not make the headwords invalid.
- [Guangxi Minzu Bao, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm), the bronze-box description and parallel Chinese prose: `dozsiengq` denotes depicted images/figures. This corroborates the catalogue's established image noun, not an exact digital-UI collocation.

## Actual consumers

`AssemblyActivity` binds the add-images button to `launchAdd()`, which returns while busy, checks the 20-input limit, and launches Android's multiple-document picker. Import completion adds successful `AssemblyImage` inputs. Newly imported items use default null attachment/position fields; `ImageAssembly.add` appends them without placing them. Layout includes only placed items. This command does not promise automatic placement or immediate import success.

The prerequisite notice appears when normalization has no image inputs, and when batch crop has no inputs. Both branches return before opening their dialogs. Single-image crop instead asks for thumbnail selection. Output creation separately requires a placed image. Adding, selecting and placing therefore remain distinct requirements. No control flow, import behavior or model code changes are included.

## Verification

- Fresh remote head/tree reconciled with the preceding verified publication. All **1,256 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,525 base leaves.
- All 215 original resource nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, ordered typed arguments, numerals, newlines and required literal tokens pass. New XML Git blob: `6ecdcd740f88ef94279ce3150ccec05bbb96aad8`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.391 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **Four host Java literal-label cases passed**, covering both entries in English and Zhuang.
- Targeted token-aware source checks passed for the three actual resource bindings, add-button picker route and busy/capacity guards, import-to-input-model path and unplaced defaults, empty-input early returns, and distinct single-selection/output-placement notices. These checks inspect actual source; they do not execute Kotlin or Android behavior.

Zhuang now has **217 typed resources**: P0 **69/94**, P1 **132/249**, P2 **16/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,359, P2 30,113, P3 7,481; 46 options have complete presence. These counts do not certify fluency or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed picker/import/normalization/crop/placement flow, device layout, accessibility or font checks were run. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
