# Interlingua assembly and editor help

Base: `48904f43207dc922894957a7e898506af58cab83` on `review/nv-bottom-2038-20261103`.

Adds the three remaining P3 help resources. All 716 previous typed resources and attributes remain unchanged; the Interlingua catalogue now contains 719 typed resources and has no missing priority keys. This closes missing entries, not a re-certification of every earlier translation or restoration of withdrawn localization conclusions.

## Scope and review

The assembly manual and short overall help have direct production consumers in `AssemblyActivity.showHelp()` and `ClassicPaintActivity.showHelp()`. The long editor manual is a retained resource without a direct production consumer; its review does not establish that the application displays it. The existing host regression explicitly preserves this distinction.

Independent full-text linguistic and semantic review checked all three passages against canonical English, existing Interlingua captions and the described implementation. Review clarified modification timestamps as dates and times, stated that cropping leaves the original file unchanged, distinguished Annulla from Reface, and described an empty position within the saved palette more naturally.

The assembly text preserves the 20-image cap, tray-only sorting, crop/reset/undo behavior, right/top and bottom/left snapping alignment, snap-overlap rejection versus Exact position overlap permission, conditional attached-image movement, independent aspect ratios, Unplace versus Remove, view-only Show all, undoable editor replacement, memory chooser versus minimum-size warning, unchanged source files and local reopening.

The editor texts preserve portrait/landscape layouts, color preview/confirm/cancel, canvas opacity versus floating-selection transparency, white Commons backing, zoom behavior, save versus export/share destination and saved-state distinctions, private autosave and source preservation, transformed selections and undo, crop versus resize, shape/cursor/font controls, gallery providers, import memory choices and separate assembly behavior. Help paths use current localized captions. Catrobat/AGPL and asset credits are not conflated into a new licence claim.

No implementation, English resource, other locale, font or licence body changed. No permanent per-batch test fixture or copied prose approval mirror is introduced.

## Verification

- 96 affected host tests pass: localization structure/contracts/boundaries, help and provider routes, priority follow-through, assembly mode/position/memory distinctions, crop guidance and tooltip wiring. This is an affected subset, not the entire repository suite.
- All 171 offered options and the priority manifest pass structural validation.
- Six English/Interlingua Java resource-template checks pass. The assembly manual retains eight paragraphs and 14 escaped newlines; the overview retains one paragraph; the long manual retains ten paragraphs, 18 escaped newlines, `formatted="false"` and its three literal percent signs. Numerical values, four hexadecimal color values, codec/provider names, RGB/HSV/HSL, Ctrl+A and coordinate identifiers are preserved.
- All 1,252 materialized base files match the freshly verified remote tree's Git blob hashes and executable modes. Its 235 unmaterialized non-tree entries are retained unchanged.
- Direct priority presence: P0 94/94, P1 249/249, P2 305/305, P3 71/71. Missing priority keys: zero, down from three. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, installed-layout, device, accessibility/runtime, CI or native-speaker certification is claimed. Publication uses the exact expected parent and a non-force lease, followed by final remote tree and changed-file readback verification. Android verification and any integration review remain separate from this resource/source-review result.
