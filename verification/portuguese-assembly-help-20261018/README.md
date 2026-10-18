# Portuguese complete assembly Help: bounded placement-mode correction

Base: `3a88bfea931c5fad9b4d8d3d71da34a2a0609376` (`develop`, includes German PR129, Spanish PR130 and Italian PR131).
Corrected English reference: PR122 exact head `0d56dd970c22398f7fa032d1baee4a1b74c83f2b`; develop still has the older English entry.
Tracker: https://github.com/c933103/AN-Paint/pull/75

## Complete-entry review and bounded scope

The implementation independently compared every paragraph with the corrected reference and current resource labels and consumers. A separate model linguistic/source review accepted the exact proposal without replacements; its complete paragraph-by-paragraph assessment and proposed-text SHA-256 are retained in `linguistic-review.md` inside the evidence packet. Neither review is native-speaker sign-off.

Exactly one pt-PT production resource changes: `Paintroid/src/main/res/values-b+pt+PT/strings.xml` / `ui_add_up_to_20_images_with_android_s`. It has four edits:

1. Scope the first-image origin statement to snapping: “Ao encaixar, a primeira imagem começa na origem.”
2. Scope overlap rejection to snapping: “As sobreposições são rejeitadas ao encaixar.”
3. Add the complete Exact position paragraph with the actual “Posição exata” label, top-left X/Y whole pixels from zero, retention of other image positions, and allowed overlap.
4. Replace unconditional gap filling with “As outras imagens continuam colocadas; as imagens ligadas podem deslocar-se para preencher o espaço.”

Five other paragraphs and all remaining sentences in the two modified paragraphs are byte-for-byte preserved: import cap/picker/provider metadata/sorting, dimensions after crop and normalization, complete single/batch/reset/Undo crop guidance, dimensions/proportions/restoration, output and both memory branches, originals/local persistence, and Catrobat/AGPL attribution. The exact complete old, new and English reference values are retained. pt-BR, PR56, existing holds and the wider PR75 scope are unchanged.

## Source semantics and regression coverage

The base and corrected English reference have identical blobs for `AssemblyActivity.kt`, `AssemblyPlacementDialog.kt` and `ImageAssembly.kt`, independently verified against the complete Git trees. The actual Help button consumes the whole resource. The actual selected-image toolbar action opens `AssemblyPositionDialog`, which validates nonnegative whole X/Y values and calls `ImageAssembly.position`. Absolute placement preserves other rectangles and allows overlap; snapping starts at the origin and rejects collisions. Unplacing absolute placement can retain a gap, whereas detaching snapped placement may promote/reflow linked images. The conditional Portuguese wording covers both.

The five-file patch updates only the complete Portuguese fixture value, all-four-locale eight-paragraph guards, dedicated semantic and memory-branch guards, and a Portuguese call to the existing real-toolbar test helper. The pre-Activity locale initialization is reused without change. The new case checks the actual “Posição exata” label and Portuguese invalid-value text; first absolute placement away from origin; negative/fractional rejection and unchanged saved project; Cancel; valid zero; allowed overlap with other coordinates preserved; absolute Unplace retaining a gap; snapping origin/collision rejection; conditional gap closing; and Undo. Synthetic pixels and files avoid user-image/provider access.

The one-time negative control rejects the actual old Help. Scope checks verify all 1,209 blobs and executable modes, five unchanged paragraphs, the exact edits, unchanged crop plural/other-locale fixtures, and every other production byte. The candidate complete remote tree matches the reviewed checkout. These checks are evidence only, not permanent production hash contracts.

## Limits

Local resource/compiler checks are not runtime execution. Local Gradle and exact-head hosted results are reported separately. No whole-language, native-speaker, installed Portuguese glyph/layout, enlarged-font, TalkBack or physical-device acceptance is claimed. Broader PR75 obligations remain open.

## Local results and publication

PR: https://github.com/c933103/AN-Paint/pull/132
Application head: `cadee014aacdc2d3422d533f76e626f3d4433dd9`
Application tree: `c0474eab8fccd272b90fb181d3989862044be7f0`
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39097285470

- 937 full host tests pass normally and 937 with Python optimization.
- 17 focused checks pass in both modes.
- Complete resources/exact-script mirrors/link, structural catalogue validation and supplementary changed-test compilation pass.
- Local Gradle/Robolectric is blocked at its distribution download. Hosted exact-source runtime gates are tracked separately.

`checks.json` is the compact receipt. `local-evidence.zip` contains complete old/new/reference values, both full-entry reviews, immutable source bindings, scope/negative-control receipts, commands, raw local logs and the five-file application patch. This separate evidence ref preserves the complete application source tree. No APK, build output, credential or unrelated private data is included.
