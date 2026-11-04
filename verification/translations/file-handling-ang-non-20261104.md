# Old English and Old Norse: image file handling

Base: `9d8e2d79201d9328dbeea5dac3eee6aaf636e399`.

## Scope

- Add five missing strings per catalogue: shared-image label, assembly PNG display filename, missing Android file-picker instruction and BMP/DIB save descriptions. All ten entries are authored translations with direct production consumers.
- Preserve the exact lowercase `.png` extension, 24-bit specification, RGB/Windows/DIB/BMP identifiers, uncompressed encoding, exact colours/larger files and the conditional need for a BMP file header. The assembly filename is an import display name, not an instruction to rename or remove source files.
- Preserve enabling either Android Files or Documents app followed by retrying. The message follows missing picker activities; it does not bypass security failures or request broader permissions.
- Existing resources, application behavior, file payloads, sharing destinations and permissions are unchanged. Canonical Android XML owns the wording.

## Review

Independent linguistic and UI-context review accepted all ten entries unchanged. The reviewer checked the actual ClipData label, assembly-edit filename, missing-picker recovery and BMP/DIB descriptions, including conditional header requirements, bit depth, colour fidelity and file size. No remaining hold.

## Checks

- 78 host tests passed across translation, localized-help, boundaries, current contracts, language note, importance, ordinary-priority followthrough and open-review recovery suites.
- All 171 offered options passed structural validation. XML, typed-key uniqueness, source attributes, Android escaping, placeholders and newline escapes passed. All 687 prior resources per locale are unchanged.
- All 1,276 materialized base files matched remote contents and executable modes before editing. The base tree has 1,453 non-tree entries; its other 177 paths are retained.
- Per locale: P0 94/94; P1 249/249; P2 284→287/305; P3 60→62/71; typed resources 687→692. These are direct-presence counts, not whole-catalogue linguistic acceptance.
- None of the 18 remaining P2 keys has a direct reference in the inspected production Kotlin, Java or non-values XML. This bounded finding does not establish that the keys are globally unused or exclude dynamic/external consumers.

## Limits

No Android build, device, emulator, rendering, accessibility, runtime, CI or native-specialist acceptance is claimed. Historical-language computing terms are modern adaptations. No issue 1 action was attempted.
