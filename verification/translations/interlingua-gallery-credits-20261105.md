# Interlingua gallery and attribution resources

Base: `8e71e4285e8988211f9376cd73f253af8aaad833` on `review/nv-bottom-2038-20261103`.

Adds 68 missing priority resources to the canonical Interlingua catalogue: 63 P2 resources and five P3 headings/help passages. All 593 previous typed resources and their attributes remain unchanged; the catalogue now contains 661 typed resources.

## Scope and review

The batch covers Commons blank-map actions and metadata/download failures; copy/edit/save credit controls; previously saved source credits; gallery navigation and import errors; the attribution-panel heading; and Catrobat, Irasutoya and Openclipart help. Independent linguistic and semantic review checked the complete batch against canonical English and available production consumers.

Review clarified the Catrobat gallery help to preserve the credits of each separately named creator, rather than literally instructing readers to preserve the people. The sticker-gallery caption uses the supported noun `autocollantes`, rather than the adjective `collantes`; see the [UMI French–Interlingua dictionary](https://www.interlingua.com/archivos/fr/dfi/dict_fr_ia_a.pdf), PDF page 66.

Attribution help retains named creators, copyright and separate source notices, modification descriptions and the CC BY-SA 4.0 adaptation terms. It does not broaden those terms to unrelated sources. Irasutoya retains its separate conditions and the payment threshold for commercial designs using 21 or more items. Openclipart retains CC0 and its external `Large PNG` link label. Commons import-change notes preserve `background=#FFFFFF`, `antiAlias=false`, `strokeDashArray=none` and `SVG → PNG`. Help paths use the actual localized File, About/credits and Image credits labels.

Sixty-three additions have exact direct production references. Five retained manifest entries have no exact direct production reference: the older Catrobat gallery description and own-artwork licence notice, insert-gallery confirmation, Catrobat-specific source rejection, and generic Catrobat gallery credit passage. Those five were reviewed against canonical English only; no runtime-use claim is made for them. No implementation, English resource, other locale, font or licence body changed. No permanent per-batch test fixture or copied prose approval mirror is introduced.

## Verification

- 98 affected host tests pass: localization contracts, help routes, structure/boundaries, priority follow-through, Commons import and action contracts, and gallery display-data/navigation/task-routing/shutdown regressions. This is an affected subset, not the entire repository suite.
- All 171 offered options and the priority manifest pass structural validation.
- All 136 English/Interlingua Java resource-format checks pass for the 68 additions. Source attributes, ordered argument types, escaped newlines, numerical limits, provider names and technical/licence tokens are preserved.
- All 1,252 materialized base files match the freshly verified remote tree's Git blob hashes and executable modes. Its 233 unmaterialized non-tree entries are retained unchanged.
- Direct priority presence: P0 94/94, P1 249/249, P2 298/305, P3 20/71. Remaining: 58 keys (seven P2 and 51 P3), down from 126. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed-layout, device, accessibility/runtime, CI or native-speaker certification is claimed. Publication uses the exact expected parent and a non-force lease, followed by final remote tree and changed-file readback verification. Remaining work includes seven non-gallery P2 controls, drawing guidance, licence/source headings and the longer help passages.
