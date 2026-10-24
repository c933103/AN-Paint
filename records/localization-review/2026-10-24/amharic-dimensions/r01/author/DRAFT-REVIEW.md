# Amharic dimensions: original draft dossier

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Eighteen complete source copies are supplied, exact Git blobs checked against freshly retrieved production tree.

No independent acceptance or implementation. Prior60 ready/six held remain separate.

## string/ui_pixels

English: Pixels

Proposed XML: `<string name="ui_pixels">"ፒክሰሎች"</string>`

Status: review

Confidence: medium-high lexical; medium standalone-context transfer; unaccepted

Bare plural selector noun directly drawn from the AOSP 13M/4M pixels token. The same spelling family as the previously reviewed pixel terminology is retained. Amharic has no uppercase/lowercase distinction, but this is the standalone key, not the interpolated key.

Shared unit radio choices in DimensionControls, NormalizeImagesDialog and ImageCropDialog. Dimension percent means percent of each original width/height; normalization percent uses largest current placed size on selected axis; crop percent uses each source image width for left/right margins and height for top/bottom. The shared unit words must not encode one baseline. Pixels are integer image pixels in these controls, not screen dp, resolution DPI or physical units.

['The selected complete standalone noun is an original extraction from an attested compound; direct standalone LibreOffice spellings differ.', 'Shared by resize/assembly dimensions, crop margins and normalization. Do not add a baseline, pixel count, px abbreviation, metric length unit, or singular/plural agreement tied to a value.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L30-L36, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L50-L61, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L96-L108, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L39-L50

## string/ui_percent

English: Percent

Proposed XML: `<string name="ui_percent">"ፐርሰንት"</string>`

Status: review

Confidence: high lexical; medium-high shared unit semantics; unaccepted

Exact nonfuzzy LibreOffice Percent unit/category label. Kept generic because the shared selector does not encode one denominator: consumers supply their own image-dimension or largest-selected-axis baseline.

Shared unit radio choices in DimensionControls, NormalizeImagesDialog and ImageCropDialog. Dimension percent means percent of each original width/height; normalization percent uses largest current placed size on selected axis; crop percent uses each source image width for left/right margins and height for top/bottom. The shared unit words must not encode one baseline. Pixels are integer image pixels in these controls, not screen dp, resolution DPI or physical units.

['መቶኛ is an attested AOSP native alternative; choosing the direct standalone loanword here is not a finding that the alternative is wrong.', 'Do not add original size, width, height, hundred, percent sign, or any one percentage denominator to this shared label.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L30-L36, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L29-L36, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L50-L61, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L96-L108, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L39-L50

## string/ui_pixels_6ec9c2

English: pixels

Proposed XML: `<string name="ui_pixels_6ec9c2">"ፒክሰሎች"</string>`

Status: review

Confidence: medium-high lexical; medium interpolated-morphology confidence; unaccepted

Bare plural unit noun for substitution into Width/Height in %1$s. The በ preposition belongs to the templates, not this resource. Same spelling as the standalone selector is permissible because Amharic has no English case distinction; semantic role and key remain separate.

Lowercase English unit noun substituted into Width in and Height in accessibility content descriptions. Keep exact separate key; Amharic has no English upper/lowercase requirement. Literal px remains separate visible unit. Review full interpolated phrases, not isolated noun alone.

['Must remain a bare unit: adding በ here would duplicate the template preposition.', 'Evaluate the complete forms ስፋት በፒክሰሎች and ቁመት በፒክሰሎች in native/accessibility review; standalone evidence alone does not validate the composed labels.', 'A singular measure-word form ፒክሰል may be preferred by a native reviewer; the plural is selected because English pixels is plural and primary in-pixels prose supports plural usage, not because singular is impossible.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87

## string/ui_percent_fd8671

English: percent

Proposed XML: `<string name="ui_percent_fd8671">"ፐርሰንት"</string>`

Status: review

Confidence: high lexical; medium interpolated-morphology confidence; unaccepted

Bare percent unit for substitution into the two accessibility labels. LibreOffice exact Percent and in percent → በ ፐርሰንት support this noun; the templates provide attached በ. Capitalization does not require a separate Amharic spelling.

Lowercase English unit noun substituted into Width in and Height in accessibility labels. Here relative to original corresponding dimension, not percent of pixel count/area. Keep separate key and review complete resulting phrases.

['Keep bare ፐርሰንት rather than embedding በ or a percent symbol.', 'Evaluate complete ስፋት በፐርሰንት and ቁመት በፐርሰንት; accessibility speech and native label idiom remain unverified.', 'The መቶኛ alternative remains available but requires coordinated contextual review.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87

## string/ui_width

English: Width (%1$s)

Proposed XML: `<string name="ui_width">"ስፋት (%1$s)"</string>`

Status: review

Confidence: high noun evidence; medium-high original format composition; unaccepted

Compose exact AOSP image Width → ስፋት with the unchanged source parentheses and full positional string placeholder. The consumer supplies literal px or %, not the translated unit names.

Visible width label with exactly one string argument, replaced px or %. Also pixel-mode normalization input contentDescription with px. Width is horizontal image dimension. Parentheses and %1$s exact; percent uses original width in DimensionControls. No numeric input value is substituted into this label.

['Preserve exact %1$s once and preserve the parentheses; never replace it with %s, %1, a fixed px/% sign, or a translated unit.', 'DimensionControls uses this as a visible label; NormalizeImagesDialog also uses it as a px contentDescription. The wording must not imply an action, image area, DPI, screen width or percentage denominator.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L50-L61

## string/ui_height

English: Height (%1$s)

Proposed XML: `<string name="ui_height">"ቁመት (%1$s)"</string>`

Status: review

Confidence: high image noun evidence; medium-high original format composition; unaccepted

Compose exact AOSP media/image Height → ቁመት with the unchanged parentheses and positional string placeholder. Prefer the directly paired image-details dimension noun over the LibreOffice graphics alternate እርዝመት, while retaining that alternative explicitly.

Visible height label with exactly one string argument, replaced px or %. Also pixel-mode normalization input contentDescription with px. Height is vertical image dimension, not length of diagonal. Parentheses and %1$s exact; percent uses original height in DimensionControls.

['Preserve exact %1$s once and source parentheses.', 'The ቁመት versus እርዝመት choice needs native contextual review; neither source is treated as universally authoritative.', 'Includes visible labels and normalization px contentDescription; it means image vertical dimension, not person height, text glyph metrics, area, resolution density, or a resize action.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L50-L61

## string/ui_width_in

English: Width in %1$s

Proposed XML: `<string name="ui_width_in">"ስፋት በ%1$s"</string>`

Status: review

Confidence: medium compositional and unit-morphology confidence; unaccepted

Original accessibility label composition using exact image Width noun followed by በ attached to the bare substituted unit. In-pixels/in-percent primary prose supports the unit preposition; the entire Width in template is not an exact quoted translation.

Width-input accessibility label contains translated unit noun via exactly one %1$s. Both resulting forms (pixels and percent) must be grammatically reviewed. Does not include entered numeric value; no screen-reader behavior certification.

['Preserve the complete %1$s exactly once. The argument is translated pixels/percent, not a numeric width and not literal px/%.', 'Check both completed phrases separately: ስፋት በፒክሰሎች; ስፋት በፐርሰንት.', 'The attached በ spacing and noun-first label order are original editorial choices. No exact whole-phrase precedent or native/screen-reader acceptance is claimed.', 'Do not add a metric length unit or an original-image baseline to the label; the unit alone is intended.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87

## string/ui_height_in

English: Height in %1$s

Proposed XML: `<string name="ui_height_in">"ቁመት በ%1$s"</string>`

Status: review

Confidence: medium compositional and unit-morphology confidence; unaccepted

Original accessibility label composition using exact AOSP image Height noun and attached በ plus the bare unit argument. This keeps height separate from width and does not import the LibreOffice alternate without review.

Height-input accessibility label contains translated unit noun via exactly one %1$s. Both resulting forms require grammatical review. Do not convert height into length of whole image, font height or screen coordinates.

['Preserve the complete %1$s exactly once. It receives translated pixels/percent, not a number or literal px/%.', 'Check both completed phrases separately: ቁመት በፒክሰሎች; ቁመት በፐርሰንት.', 'The entire phrase, attached preposition spacing, and noun-first label order are original composition, not exact primary-source bytes.', 'Native review may prefer the retained እርዝመት noun family; no automatic acceptance is implied by exact component evidence.', 'Original AI-authored review draft, not native-reader or release acceptance.', 'No production edit, app build, CI, rendering, UI-fit, accessibility speech, or runtime validation was performed by this lexical task.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87

## Shared scope and evidence limits

DimensionControls is used by main new/canvas-size/image-resize dialog (ClassicPaintActivity1012-1030), large-import resize chooser (ImageResizeDialog31) and assembly output-copy chooser (AssemblyActivity306). Same unit labels also used by normalization and cropping. Complete current consumer files supplied. Main canvas-size copies pixels at top-left; resize scales. Unit conversion maintains canonical target pixels; unrelated memory errors, detailed instructions, result formatters and aspect-lock wording excluded.

No English defect established in these unit/dimension labels. Placeholders and generic unit semantics must be preserved. Any later real source defect must be corrected in English first and flagged across affected languages, not silently compensated only in Amharic.

Exactly one %1$s is preserved in each of four templates. Visible labels substitute literal px/%; accessibility templates substitute translated unit nouns. Unit resources have no placeholders. English upper/lowercase variants retain separate keys, even if Amharic values match.

Full lexical reasoning, exact records, source snapshots and retrieval/reuse limitations are in lexical-evidence/. Nonfuzzy is a record flag, not proof of correctness. Component and cross-context evidence does not establish exact full-phrase native acceptance.

Original drafts only, independent checking required.

No exhaustive repository-wide consumer search claim; discovery in prior cached source then complete current consumers checked.

No native-reader, rendering, screen-reader, numeric-input correctness, lifecycle or release acceptance.

Prior60 ready/sixholds excluded. Aspect lock, prior held Lock proportions and inherited uncertainties remain separate.

Production remains12 present/705 missing of717. No production changes, builds, CI, release or Work task.
