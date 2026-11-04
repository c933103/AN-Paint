# Old English and Old Norse: About, licence navigation and source export

Base: `455cbc971e44854623c8887456bbeb5016ebcca8`.

## Scope

- Add 21 missing string resources to each catalogue, with no existing resource or application-code changes. Each locale has 20 authored translations and one unchanged official GNU licence title.
- Cover the About/licence menus, codec and asset licence captions, translation credits, and this-version source-code export action, success and failure feedback. All 21 keys have production consumers in `LegalInfo.kt` or `ClassicPaintActivity.kt`. Both locales cover all 18 direct `LegalInfo` string references after these additions.
- Preserve format/product names and the full official GNU Affero General Public License title. Original legal asset contents and the About body are unchanged. This work localizes navigation, not licence agreements.
- Canonical Android XML owns the wording. The historical languages use transparent modern computing adaptations; this report does not claim historical attestation of computer terms.

## Review

Independent linguistic and UI-context review accepted all 42 entries unchanged. The review checked version-specific source export, build scripts and licence notices, exact official titles, actual menu bindings and completed-copy success versus failure. No remaining hold.

## Checks

- 78 host tests passed: translation, localized-help, boundaries, current contracts, language note, importance, ordinary-priority followthrough and open-review recovery suites.
- Structural validation passed for all 171 offered locale options. XML, duplicate typed keys, existing entry/byte preservation, source attributes, Android escaping, placeholders and newline escapes passed.
- Before edits, all 1,276 materialized base files matched their remote blob hashes and executable modes; the remote tree contained 1,451 non-tree entries. The remaining 175 paths are retained from the verified base tree.
- Per locale: P0 94/94; P1 249/249; P2 281→283/305; P3 38→57/71; typed resources 662→683. These are direct-presence counts, not whole-catalogue linguistic acceptance.

## Limits

No Android build, device, emulator, rendering, accessibility, runtime or CI acceptance is claimed. The unchanged bundled legal text remains outside this translation batch. No issue 1 action was attempted.
