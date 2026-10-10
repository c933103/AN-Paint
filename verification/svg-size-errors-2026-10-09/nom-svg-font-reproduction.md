# Additive Nôm SVG glyph: U+8C6B 豫

This is a font-support change for the Nôm SVG size-error translation. It is not
linguistic acceptance or Android/device rendering verification.

## Inputs and result

- Pinned source: [Nom Na Tong v5.18 release](https://github.com/nomfoundation/font/releases/tag/v5.18), `NomNaTong-Regular.ttf`, 15,927,512 bytes, SHA-256 `37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3`.
- Base: `Paintroid/src/main/assets/fonts/anpaintnomui.ttf` at commit `80f0448f878165213eaa7e9bd5ad286be00e4ce8`, SHA-256 `1c809021f3c74ce27bb7cbe73e63339f46fa66f5b85252db504f4f62405701b9`.
- Result: 275,312 bytes, SHA-256 `797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526`.
- Local toolchain: Python 3.12.14, fontTools 4.61.1, already available. The downloaded font was read as data, not installed.

## Reproduce

Run from the repository root with the pinned source font downloaded separately.
The extension script validates both input hashes and refuses to overwrite them.
It does not download, rebuild unrelated fonts, edit translations or update the inventory.

```sh
git show 80f0448f878165213eaa7e9bd5ad286be00e4ce8:Paintroid/src/main/assets/fonts/anpaintnomui.ttf > /tmp/pre-svg.ttf
python tools/extend_nom_svg_ui_font.py /path/to/NomNaTong-Regular.ttf /tmp/pre-svg.ttf /tmp/nom-svg-a.ttf
python tools/extend_nom_svg_ui_font.py /path/to/NomNaTong-Regular.ttf /tmp/pre-svg.ttf /tmp/nom-svg-b.ttf
cmp /tmp/nom-svg-a.ttf /tmp/nom-svg-b.ttf
sha256sum /tmp/nom-svg-a.ttf
PYTHONPATH=tools python -m unittest test_locale_font_coverage test_font_disclosures_pr12 test_nom_notifications test_nom_ui_application test_svg_error_translations -v
```

Two independent generations were byte-identical. The original helper keeps its
original default base hash and U+651D/U+671D additions; the new wrapper pins the
current base and only U+8C6B. The full two-source builder was not run.

## Preservation and tests

`nom-svg-font-extension.json` records the complete bounded binary audit:

- All 735 existing glyphs keep their order, compiled outlines, advances and bearings.
- All 733 existing codepoints retain their glyph IDs and mappings in both cmap subtables. Format 4 grows from 576 to 577 entries; format 12 grows from 733 to 734.
- The one appended glyph (ID 735) has the exact outline and metrics of U+8C6B in the pinned source, with advance 1000 and left bearing 36.
- Existing `glyf`, `hmtx` and `loca` bytes are identical prefixes of the extended tables.
- `OS/2`, `hhea`, `name` and `post` remain byte-identical. `head` changes only the whole-font checksum adjustment; `maxp` changes only the glyph count from 735 to 736. Existing font timestamps, bounds, global metrics and licence metadata are unchanged.
- Wrong source/base hashes, overwriting a pinned input, an already-present codepoint and duplicate requested codepoints were rejected without creating output or changing input.

The standard-library host regression checks the frozen table prefixes, metadata,
new outline and metrics, exact cmap/output hashes, full Nôm catalogue coverage,
font disclosures and relevant application routing. See `nom-svg-font-tests.log`:
32 tests passed. No new dependency was added to host CI.

Existing combined-font OFL-1.1 distribution and retained Nom Na Tong MIT notices
remain applicable. This adds one glyph from the same pinned MIT source, preserves
the renamed family and embedded licence information, and leaves every bundled
notice unchanged. No unrelated font was rebuilt. Android compilation, emulator
checks, device rendering and linguistic review are separate outcomes.
