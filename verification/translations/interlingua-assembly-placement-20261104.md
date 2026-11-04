# Interlingua assembly tray and placement

Base: `c2d1105729e8f25f0056fcc6c9b6e7d3e1518b72` on `review/nv-bottom-2038-20261103`.

Added 36 missing canonical Interlingua resources: 32 P2 and four P3. Independent source-and-consumer review accepted the existing unpublished draft unchanged. All 483 previous typed resources and their attributes remain unchanged; the catalogue now contains 519.

## Scope and review

Image addition, the 20-image limit, remaining capacity, filename/date sorting and tray accessibility captions are translated. Placement guidance distinguishes thumbnail hold-and-drag from moving an already placed image, right/top and below/left edge alignment, and pan/zoom from image geometry changes. Unplace removes placement rather than the source image.

Exact placement preserves top-left coordinates, whole pixels starting at zero, the maximum 2147483647, unchanged positions of other images, allowed overlap, later-imported images on top, canvas expansion and unchanged crops/sizes. These clauses were checked against `ImageAssembly.position`, `AssemblyCanvas`, `AssemblyPlacementDialog` and their activity consumers. All 36 additions have direct production references. No runtime code, source-language wording, other locales, font files or licence bodies changed.

Canonical Android resources own the wording. No full-prose approval mirror or permanent per-batch test fixture is introduced.

## Verification

- 78 host tests pass: translations, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary priority follow-through and open-review recovery.
- Structural validation passes for all 171 offered options and the priority manifest.
- All 72 English/Interlingua resource-render checks pass. XML/Android escaping, source attributes, argument order/types and numerals are preserved.
- All 1,254 materialized base files match the freshly read remote Git tree's blob hashes and executable modes. The base tree retains 228 unmaterialized non-tree entries unchanged.
- Direct priority presence: P0 94/94, P1 249/249, P2 167/305, P3 9/71. Remaining: 200 keys (138 P2 and 62 P3), down from 236. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed layout, device, accessibility/runtime, CI or native-speaker certification is claimed. Publication uses the exact expected parent and a non-force lease; final remote tree and changed-file readback checks remain required before reporting success. Next localization work should address another coherent group among the remaining keys without replacing existing wording.
