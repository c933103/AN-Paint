# Translation compatibility review — 17 October 2026

This review follows PR #114's translation display hardening. It checks whether
previous resource-safety repairs changed wording or whether the new formatter
changes the display of existing translations. Historical localization completion
claims remain withdrawn as documented in `AGENTS.md`; this review does not revive
them or certify every translation's linguistic quality.

## Corrections

### Preserve translated percent symbols

At `6ddc9eaf5baea9dc6f6c1eab1d1877e98bddff50`, `LocaleText` compared literal
`%%` tokens as part of the source argument contract. Eighteen valid translations
therefore fell back to English when their text used `%` but English used the word
"percent". The argument indices, types, flags, widths, precisions and multiplicities
already matched. Commit
[`db076197`](https://github.com/c933103/AN-Paint/commit/db0761974902381a4d6f286d450ed67967e014c0)
corrects the contract comparison while retaining token parsing and bounds. These
catalogue values retain `%%`, the format-template encoding for one displayed `%`.

The affected catalogue pairs were seven keys in each of `ain-Latn` and `ain-Kana`
and four in `mnc-Mong`:

| Key | Ainu Latin / Kana | Manchu | Current consumer |
| --- | --- | --- | --- |
| `ui_each_px_px_percent_is_relative_to_the` | Both | — | Retained entry; no production reference found |
| `ui_percent_of_pixels` | Both | — | Retained entry; no production reference found |
| `ui_trim_in_percent` | Both | — | Crop field accessibility descriptions |
| `ui_normalize_width_info` | Both | Yes | Same-width dialog information |
| `ui_normalize_height_info` | Both | Yes | Same-height dialog information |
| `ui_normalize_width_input_percent` | Both | Yes | Same-width input accessibility description |
| `ui_normalize_height_input_percent` | Both | Yes | Same-height input accessibility description |

The encoding is traceable to
[`2e0d3251`](https://github.com/c933103/AN-Paint/commit/2e0d3251223c07f71c49b09307b968f89cf9c9e1),
which added the explicit percent-validator rule, and
[`a9a7dd88`](https://github.com/c933103/AN-Paint/commit/a9a7dd88f5d75bfc36d1dc0ce68ecd2a3271df2c),
which added the normalization messages. Their history establishes provenance,
not accepted linguistic completion.

### Restore the Japanese crop unit symbol

The resource-safety repairs
[`c6d4b439`](https://github.com/c933103/AN-Paint/commit/c6d4b43940fe6b11038543500f2619d4c4b83cd0)
and [`acbe293b`](https://github.com/c933103/AN-Paint/commit/acbe293b6f813aa323840224e2c8d309b9823ce3)
changed Japanese `ui_trim_in_percent` from `%1$sの切り詰め量（%）` to
`%1$sの切り詰め量（百分率）`. This replaced the intended unit symbol while
repairing an unescaped format-template percent.

The canonical Japanese value is restored to `%1$sの切り詰め量（%%）`.
With the edge label `左`, the intended output is `左の切り詰め量（%）`.
`ImageCropDialog` supplies this string to the four edge fields' accessibility
descriptions when percentage mode is selected. No current wording fixture stores
this Japanese key. Historical audit records are unchanged.

## Other examined repairs

| History / candidate | Disposition |
| --- | --- |
| English "Percent" and "percent of … pixels" | Retain. They already appeared in hardcoded Kotlin interpolation in the [initial imported editor](https://github.com/c933103/AN-Paint/commit/e40ff9aa), before the [resource extraction](https://github.com/c933103/AN-Paint/commit/83b570367f48d34d8789c675dd1beeb8ef8ae7ae). Their presence alone is not evidence of a formatting workaround. |
| Literal-percent resources marked `formatted="false"` in `acbe293b` and related repairs | Retain. This declares literal text; the resource compiler still requires valid resource syntax and the runtime honors the declaration. |
| [Turkish apostrophe escaping](https://github.com/c933103/AN-Paint/commit/c6a193f7a5885434893f528e0ca5ad7a6b8423e5) and shared Android quoting repairs | Retain valid encoding. Escaping an apostrophe preserves its displayed character. The runtime fix does not remove Android XML/string escaping requirements. |
| [Commons source hint](https://github.com/c933103/AN-Paint/commit/2c4acdbb48992449ac0a6cff6bc77a5fd310458f): "Check this file's Commons page" → "Check the Commons file page" | Retain. Both identify the selected file's source page; the author, licence, attribution and adaptation clauses remain. No current loss of meaning was identified that warrants another wording change. |
| [Hakka conversion case](https://github.com/c933103/AN-Paint/commit/53823ab57b4516136611609214d0c91b41ee264f) and [spaces inside format tokens](https://github.com/c933103/AN-Paint/commit/df0618876d84fc517aa2a431f472611d9c81173a) | Retain. These restore actual placeholder syntax, such as `%1$.2f`, without replacing the surrounding translation. |
| [POJ literal identifiers](https://github.com/c933103/AN-Paint/commit/74f19a0be9d1a313942704522a6d03d83a4300af) | Retain intact identifiers such as `CC BY-SA 4.0` and `data:image/png;base64,`. These are meaningful syntax, not prose to remove to satisfy a parser. |
| [Manchu escape preservation](https://github.com/c933103/AN-Paint/commit/9094cf7bc6c81107cc8d747b6c56f97a1a131b6b) and [Nôm protected Android syntax](https://github.com/c933103/AN-Paint/commit/dddf7b36e341c601ff90079a39a10bca6b793ecd) | Retain protected resource syntax. Full before/after resources were inspected for the selected changes; no additional percent-symbol removal or newline loss was identified. This does not certify the full transliterations. |
| [Count-independent English/French labels](https://github.com/c933103/AN-Paint/commit/f47929c5ba142765b3e575161257d287d2dc326a) | Retain. "Number of pages: …" and similar labels preserve the information without an incorrect singular/plural suffix. PR #114 does not change their count grammar. |
| GIMP/Krita/LibreOffice vocabulary adapters | Retain the documented desktop-mnemonic and UI-punctuation adaptations. They remove source-application accelerator syntax; they do not justify stripping punctuation from arbitrary new translations. Canonical XML remains authoritative and is not regenerated from these historical imports. |

Other flagged quotation changes concerned updated control captions, translated
prose or obsolete menu descriptions. The inspected shortened language notices
removed the old assertion that commands used Paintroid translations; they were
not formatter escape repairs. No additional current wording restoration was
established in this targeted pass.

## Scope and evidence limits

- Initial compatibility scan at `6ddc9eaf`: 173 nondefault `strings.xml` files
  (171 offered tags plus the `es` and `ko` base catalogues), containing 47,955
  string/plural values. No empty or over-bound values, double-encoded named XML
  entities, doubled backslashes or child markup were found in those values.
  After integration with develop `38d4cbef`, the same 173 files contain 48,421
  string/plural values. The frozen runtime comparison below remains tied to
  the original head; its counts do not include those later additions.
- A frozen production-Kotlin comparison at the original PR head exercised 5,704
  argument-template values with type-compatible inputs. The former formatter
  succeeded on all of them; 5,686 outputs were unchanged and the 18 percent cases
  fell back to English. The inputs included percent signs, backslashes, quotation
  marks and emoji. This was a formatter comparison, not an installed-device test.
- An independent AAPT2 compile/link/dump of the 18 affected templates confirmed
  that their decoded resource values preserve the expected `%%` encoding.
- Historical discovery covered metadata for 519 non-merge resource/provenance
  commits after the September fork. Detailed review covered 63 candidates selected
  for formatting, escaping, preservation, labels, repairs or shortening, plus
  four origin/extraction/normalization anchors. It inspected 3,138 paired string
  edits in available patches. For 32 changes with omitted patches, both complete
  resource versions were fetched; these supplied 3,198 further changed values.
  Repeated branch copies are included in these history counts.
- This is a targeted compatibility and workaround review, not a sentence-by-
  sentence linguistic review of every historical or current catalogue. It does
  not establish absence of unrelated translation, font, layout or device defects.
