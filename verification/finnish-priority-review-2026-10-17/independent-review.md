# Independent seven-value Finnish review

Accept all seven proposed values unchanged, limited to these seven keys.

1. ui_the_encoder_did_not_finish
“Kooderi ei suorittanut koodausta loppuun.”
Accept. Faithfully says the encoder did not complete encoding. It corrects the old wording’s implication that the encoder itself was unfinished. Appropriate for all three checked Bitmap.compress failure consumers.

2. language20_translation_note
“Sovelluksen kieli\n\nKäännöksiä ylläpidetään AN Paintin kieliresursseissa. Uusi tai kääntämätön teksti näkyy englanniksi.”
Accept. Natural, accurate Finnish. Preserves the heading, paragraph break, translation-maintenance statement, and exact “new or untranslated text appears in English” meaning. It makes no completeness guarantee. Including the heading is important because this resource supplies the picker’s custom title.

3. ui_d_d_px_d_pixels_2f_mp
“%1$d × %2$d px · Pikselimäärä: %3$,d (%4$.2f MP)”
Accept. “Pikselimäärä” is natural and works for both one and multiple pixels. All argument indexes, conversions, grouping, and precision are preserved.
Illustrative Finnish-locale outputs:
- 1 × 1 px · Pikselimäärä: 1 (0,00 MP)
- 2 × 1 px · Pikselimäärä: 2 (0,00 MP)

4. ui_height_in
“Korkeus %1$s”
Accept with the proposed embedded-unit changes.

5. ui_width_in
“Leveys %1$s”
Accept with the proposed embedded-unit changes. This narrow counterpart is necessary for consistent, grammatical composition.

6. ui_pixels_6ec9c2
“pikseleinä”
Accept. Correct inflected form for dimensions expressed in pixels.

7. ui_percent_fd8671
“prosentteina”
Accept. Correct, idiomatic form for dimensions expressed as percentages.

Complete compositions:
- Korkeus pikseleinä
- Leveys pikseleinä
- Korkeus prosentteina
- Leveys prosentteina

Consumer distinction: these four compositions populate accessibility contentDescription values. Visible dimension labels use separate resources, “Korkeus (%1$s)” and “Leveys (%1$s)”. Standalone unit choices “Pikselit” and “Prosentti” should remain unchanged.

Evidence: I directly inspected both resource files and the consumers in DimensionControls.kt:81–82, ImageImport.kt:15, AppLanguage.kt:149, ImageExporter.kt:25, TextImageCodec.kt:33, and IcoCodec.kt:97 at b6a99b41c4390ca6a412e3a1938eb913c59509fb.

Confidence: high for these seven values and their checked compositions. This is a source-based linguistic review, not a device/TalkBack test, native-speaker certification, or acceptance of the broader Finnish catalogue. No external changes made.
