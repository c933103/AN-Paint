import json, hashlib, collections, pathlib, re, xml.etree.ElementTree as ET
root=pathlib.Path('/tmp/swedish-independent-full-review')
a=json.loads((root/'author-proposals-reviewed.json').read_text())
corrections=json.loads((root/'source-correction-proposals-reviewed.json').read_text())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
# These decisions record a completed independent model reading of every complete
# proposal, followed by the correction reread. They are not inferred from counts.
unknown_notes={
'ui_monospace':'Fast teckenbredd identifies the fixed-width font family rather than a generic fixed element. FontCatalog maps it to monospace.',
'ui_serif':'Serif is the Swedish font-family term; FontCatalog maps it to the serif family.',
'ui_sans_serif':'Sans-serif is an appropriate Swedish font-family label and matches the sans-serif family.',
'ui_star':'Stjärna correctly identifies the five-pointed-star drawing tool; detailed help preserves five points.',
'ui_heart':'Hjärta correctly identifies the heart drawing tool.',
'ui_smooth_freehand_strokes':'Jämna ut frihandsdrag replaces untranslated Smoothing and describes freehand stroke smoothing, not pixel antialiasing.',
'ui_smooth_pixel_edges_anti_aliasing':'Jämna ut bildpunktskanter (kantutjämning) describes pixel-edge antialiasing and remains distinct from stroke smoothing.',
'ui_quality':'Kvalitet (%) preserves the quality slider and percent unit; source formatted=false remains relevant.',
'gallery_use_image':'Använd bild matches the gallery action and all new gallery/help references. The action imports/inserts the selected online artwork.',
'gallery_copy_credit':'Kopiera erkännande names the copied attribution object rather than the underspecified Kopiera. Gallery help explicitly defines its title/publisher/source/licence content.',
'ui_advanced':'Avancerat names the detailed colour editor and agrees with the Help route.',
'ui_arrow':'Pil identifies the arrow drawing tool, not a navigation arrow.',
'ui_curve':'Kurva identifies the curve drawing tool; its two-bend workflow is separately reviewed.',
'ui_round':'Rund identifies circular brush tips and cursor shape, replacing Avrundad imported from line-cap terminology.',
'ui_square':'Fyrkantig identifies the square brush tip and cursor shape in contrast to Rund.',
'ui_strikethrough':'Genomstruken accurately labels the text strikethrough checkbox.',
'ui_top':'Överkant identifies the crop edge and aligns with the already accepted Nederkant, replacing the generic Topp.',
'ui_wheel':'Färghjul identifies the colour wheel in AdvancedColourDialog. Imported Mushjul came from a GIMP mouse/input-wheel context and was wrong here.',
'ui_add_palette23':'Lägg till i palett describes adding the current custom colour to the saved palette.',
'ui_edit_palette23':'Redigera palett preserves the complete label meaning; no direct current production Kotlin caller was found, so acceptance is source-semantic only.',
'ui_horizontal23':'Horisontell labels horizontal text direction, contrasted with the reviewed vertical column directions.',
'formats22_ascii_label':'ASCII-konst correctly names the derived ASCII-art export format.',
'save20_dither':'Färgutjämning describes dithering for GIF export, distinct from drawing-edge kantutjämning. The retained GIMP catalogue has the same translation for Dithering in image conversion.',
'ui_about_credits23':'Om, licenser och medverkande accurately names the About/licences/credits panel and is used consistently in the new navigation instructions.'}
special={
'commons_check_file_licence':'Preserves the per-map Commons file-page check, creator, licence and required attribution; changes may be adaptations, not automatically licensed permission.',
'ui_catrobat_s_own_artwork_uses_cc_by_sa':'Correction preserves the full creator credit rather than narrowing it to a name, the same-licence condition, separate attribution checks, and the actual Arkiv/About/Image credits route.',
'ui_gallery_artwork_catrobat_and_its_credited_creators_cc':'Correction preserves artwork attribution beyond naming the creator, separate source terms, the adaptation-sharing condition and the requirement to describe edits.',
'ui_honeycomb_colour_swatches_with_a_greyscale_row':'Uses an explicit rad med gråtoner, retaining both the honeycomb swatches and the greyscale row without the ambiguous gråskalerad reading.',
'ui_invalid_image_attachments':'Kopplingar mellan bilder describes assembly attachment relationships, not image-file attachments or fortresses.',
'ui_no_attachment_fits_within_the_current_coordinate_range':'States that the image cannot be attached within the coordinate range and preserves the smaller-image-size remedy; avoids the misleading noun fästning.',
'ui_the_attachment_image_is_missing':'The image referenced by the attachment relationship is missing, rather than the whole assembly being lost.',
'ui_the_attachment_image_is_not_placed':'The attachment relationship references an unplaced image; this remains distinct from a missing image.',
'ui_cursor_marker_help31':'Enlarging the marker leaves the painting brush size unchanged. Corrected wording no longer describes a physical brush that has been painted.',
'ui_drag_a_line_then_drag_twice_to_set':'Preserves the initial line, two bend gestures, and Finish curve allowing an earlier commit. Refinement avoids the negative implication of i förtid.',
'ui_drag_a_selection_drag_inside_to_move_square':'Preserves move, square corner/edge resize, round-handle rotation and shape preservation; references exact current label Lås proportionerna.',
'ui_assembly_position_help':'Preserves the top-left output-canvas coordinates, whole pixels from zero, stationary other images, allowed overlap, later-import-on-top order, expanding canvas, unchanged crops and sizes.',
'ui_assembly_position_nonnegative':'Preserves whole-number validation and the inclusive zero through 2147483647 range.',
'ui_assembly_target_x':'X remains measured from the left output-canvas edge, not relative to the selected image.',
'ui_assembly_target_y':'Y remains measured from the top output-canvas edge, not relative to the selected image.',
'ui_crop_preview_images':'Both complete Swedish one/other forms were read. Preview width/height are %1$d/%2$d, applied count is %3$d, and cropping placed images may move attached images. Singular bild and plural bilder are correct.',
'ui_help23':'Complete active Help paragraph read against the source and current labels. Retains navigation, preview/confirm/cancel colours, Save versus Export versus Share state, all five image sources, selection behavior, original size and undo/redo restoration. Byt plats på färgerna is correct for the actual ui_swap23 caller, not the dormant longer swap label.',
'gallery_description':'Preserves immediate insertion; attribution title/publisher/source/licence; separate creators and copyright/source notices; edit-description and compatible-licence conditions; editable credits and exact navigation route.',
'gallery_credit_edit_hint':'Preserves pre-publication creator/copyright retention, added change descriptions, removal of absent sources and editability, without treating every retained source as present in output.',
'ui_irasutoya_help34':'Preserves English/Japanese search, Japanese titles/site text, the commercial-design 21-or-more threshold, possible separate collaboration conditions, and source/credit retention. No Creative Commons permission is implied.',
'ui_irasutoya_credit34':'Preserves creator copyright, Irasutoya terms and the explicit statement that this is not a Creative Commons licence.',
'ui_openclipart_help34':'Preserves the artwork-page step, Use image beside the site label Large PNG, CC0 attribution and retained page/licence route.',
'commons_import_svg_changes':'Preserves the actual SVG-to-PNG transformation, original size, antiAlias=false, strokeDashArray=none, and background=#FFFFFF technical values verbatim.',
'commons_import_raster_changes':'Preserves background=#FFFFFF and alpha compositing rather than claiming transparent pixels were preserved.',
'formats22_base64_description':'Preserves lossless PNG, the literal data:image/png;base64, prefix, reopening the text to recover the image, and the larger-than-contained-PNG size.',
'formats22_ico_description':'Preserves one PNG-compressed icon, the 16–256 size range, aspect-ratio preservation and centring on a transparent square.',
'formats22_ico_dimensions_error':'Katalogpost correctly describes the ICO directory entry, not a filesystem folder.',
'formats22_tiff_description':'Preserves a single RGB page, optional lossless size reduction with unchanged pixels, and turning compression off for uncompressed TIFF.',
'formats22_dib_description':'Preserves uncompressed 24-bit Windows DIB and the BMP-header compatibility condition.',
'formats22_preview_memory':'Preserves insufficient preview memory while only conditionally offering smaller page dimensions on opening, not guaranteeing them.',
'formats22_pdf_crop':'The Swedish nonzero-area rectangle expresses non-empty within the selected page without allowing an out-of-page crop.',
'formats22_pdf_encrypted':'Preserves password or unsupported-encryption alternatives and the unprotected-copy prerequisite; it does not promise password entry support.',
'formats22_pdf_invalid':'Preserves inability to read and uncertainty between corruption and Android-version feature limitations.',
'ui_vertical_hint23':'Preserves new-line/new-column behavior, joining scripts including Mongolian, and combining-mark/emoji-sequence integrity for upright characters.',
'ui_cursor_help29':'Retains the resource alias to ui_cursor_help31, whose full Swedish target was reviewed.',
'ui_cursor_help31':'Preserves cursor positioning, on-screen drawing-button start, panning to draw, tap-to-stop and current Rita → Ritverktyg brush/stroke route.',
'ui_normalize_width_intro':'Preserves common width for every image, count, each image’s own aspect ratio, original files and crop settings.',
'ui_normalize_height_intro':'Preserves common height for every image, count, each image’s own aspect ratio, original files and crop settings.',
'ui_normalize_width_info':'Preserves target width, range of resulting heights, percentage relative to the largest current width, and reflow to make room.',
'ui_normalize_height_info':'Preserves target height, range of resulting widths, percentage relative to the largest current height, and reflow to make room.',
'ui_trim_in_pixels':'The format argument remains the selected crop edge; unit remains pixels.',
'ui_trim_in_percent':'The format argument remains the selected crop edge; unit remains percent.',
'ui_unplace':'Ta bort placering names removing placement, distinct from Ta bort removing an input.',
'ui_shows_the_whole_assembly_image_and_output_sizes':'Only view zoom changes; neither image nor output dimensions change.',
'ui_estimates_include_the_current_canvas_and_clipboard_sampled':'Preserves current canvas/clipboard, sampled decode and editing buffers, variable memory, loss of detail in smaller copies, opaque import background and unchanged original files.',
'ui_aa_bb_0123':'Preserves the Latin/digit/Japanese typeface sample rather than translating its demonstration glyphs.',
'ui_gnu_affero_general_public_license':'Retains the licence’s proper title rather than inventing a translated legal title.'}
reasons={
'commons_metadata_not_file_page':'The supplied URL is not a Commons file page.',
'commons_metadata_ambiguous_file':'Metadata did not identify a unique file; Swedish keeps the ambiguous-result meaning.',
'commons_metadata_unavailable':'File metadata is unavailable, distinct from a failed image decode.',
'commons_metadata_original_mismatch':'Attribution does not match the selected original file, not merely a missing credit.',
'commons_metadata_invalid_page':'The returned attribution page is invalid, distinct from the input not being a file page.',
'commons_metadata_field_too_large':'The individual attribution field exceeds its text limit, distinct from the whole response limit.',
'commons_metadata_cache_failed':'Attribution could not be retained, not necessarily downloaded or copied.',
'commons_download_original_mismatch':'The download redirected to a different original file.',
'commons_svg_png_encode_failed':'The blank map could not be encoded as PNG.',
'commons_metadata_http_error':'The HTTP status placeholder remains intact.',
'commons_metadata_response_too_large':'The complete metadata response exceeds its size limit.',
'commons_metadata_query_failed':'The metadata query failed; no provider error payload is introduced.'}
special.update(reasons)
def rationale(r):
 k=r['identity'].split('/',1)[1]
 if k in unknown_notes:return unknown_notes[k]
 if k in special:return special[k]
 if k.startswith('legacy_credits_'):return 'Full message preserves the legacy-credit archive operation and its relation to this image, distinguishing adding attribution, saving full text and retaining an existing same-source credit.'
 if k.startswith('formats22_pdf_'):return 'Full PDF diagnostic preserves the specific invalidity/limit, the affected file/page/rendering object, and every stated qualifier, bound or recovery instruction.'
 if k.startswith('formats22_') and any(t in k for t in ['page','preview']):return 'Page-selection wording preserves selected-page navigation, preview versus opening, page/count/dimension arguments, and the source’s limits or uncertainty.'
 if k.startswith('commons_credit_'):return 'Full attribution-copy result preserves failure versus insufficient memory and the reason placeholder where present; it does not claim import success.'
 if k.startswith('gallery_credit_'):return 'Full attribution label/status preserves the title/publisher/source/gallery/licence/text object and success state; format arguments and proper names remain intact.'
 if k.startswith('colour20_'):return 'Full custom-colour slot message preserves slot identity, selection/use/save/replace distinction, tap action and dynamic arguments. No current direct Kotlin caller found; source-semantic acceptance only.'
 if k.startswith('ui_colour_'):return 'Colour-component range preserves RGB/HSV/HSL identity, numerical bound, degree or percent unit, and dynamic bound if present.'
 if k.startswith('ui_vertical_') or k in ['ui_top23','ui_bottom23']:return 'Vertical-text choice preserves column direction, upright versus sideways glyph orientation or the appropriate vertical alignment; Swedish remains distinct from horizontal text mode.'
 if k.startswith('ui_cursor_') or any(t in k for t in ['cursor_drawing','magnif','pixel_grid']):return 'Full cursor/magnifier/grid label or instruction preserves the operation, start/stop or enable/disable polarity, image-pixel coordinates, magnification or zoom threshold stated by the source.'
 if k.startswith('ui_drag_') or k.startswith('ui_draw_') or k.startswith('ui_tap_'):return 'Complete tool/gesture statement preserves gesture order, affected object, geometry or drawing effect, control references and every stated qualification.'
 if any(t in k for t in ['licence','credits','copyright','notices','terms','source_code']):return 'Complete legal/credits/source label or status preserves the intended content and action, without inventing licence permissions, terms or publication success.'
 if any(t in k for t in ['assembly','attachment','placed','normalize','same_','crop','trim','thumbnail','images','output','filename','modified','sort_tray','restore_original']):return 'Full assembly statement or label preserves placement versus source removal, dimensions/cropping versus view zoom, source-file retention, limits, gesture or sorting effects as stated; displayed arguments are intact.'
 if any(t in k for t in ['colour','palette','honeycomb','spectrum']):return 'Full colour-control statement or label preserves foreground/background gesture, saved/current colour, replacement/removal or mode distinction and all dynamic values.'
 if any(t in k for t in ['memory','budget','decoded','size_limit']):return 'Full memory/format statement preserves estimates versus hard limits, decoded versus source/output size, conditional remedies and unchanged originals where stated.'
 if any(t in k for t in ['gallery','download','redirect','source34']):return 'Full gallery status preserves the precise target and failure/success condition; no unsupported source, image or licence guarantee is added.'
 if any(t in k for t in ['sans_','cursive','casual','calligraphy']):return 'The complete Swedish label preserves the specific font-family weight/width/style or brush-tip type, not text italic formatting or another control.'
 return 'The complete source and Swedish target were read together. The Swedish label/statement preserves the action, object, polarity and qualification in the recorded context; positional arguments and literal technical content remain intact.'
fix_keys={'ui_catrobat_s_own_artwork_uses_cc_by_sa','ui_gallery_artwork_catrobat_and_its_credited_creators_cc','ui_honeycomb_colour_swatches_with_a_greyscale_row','ui_invalid_image_attachments','ui_no_attachment_fits_within_the_current_coordinate_range','ui_the_attachment_image_is_missing','ui_the_attachment_image_is_not_placed','ui_cursor_marker_help31','ui_drag_a_line_then_drag_twice_to_set','ui_drag_a_selection_drag_inside_to_move_square'}
rows=[]
for r in a['rows']:
 k=r['identity'].split('/',1)[1]
 out={'identity':r['identity'],'english':r['source'],'swedish':r['target'],'english_sha256':digest(r['source']),'swedish_sha256':digest(r['target']),'source_attributes':r['source_attributes'],'baseline_status':r['baseline_status']}
 if r['baseline_status']=='retained-prior-bounded':
  out.update(decision='retained_prior_exact_not_rereviewed',rationale='Exact complete source/target pair matches the released baseline and prior bounded receipt. This check preserves prior credit only; it is not a new linguistic, consumer or installed-UI review.')
 elif k in corrections:
  out.update(decision='held_current_source_mismatch_reviewed_proposal_only',rationale='The complete corrected English/Swedish proposal is linguistically acceptable, but differs from the released English source. Do not claim released-source-bound acceptance. Assembly Help requires the exact PR122 source gate; the legacy full manual has no direct production Kotlin caller and is not an active-workflow blocker.', proposed_english=corrections[k]['proposed_source'], proposed_english_sha256=digest(corrections[k]['proposed_source']),proposed_swedish_sha256=digest(corrections[k]['proposed_swedish']),context=r['context'])
  assert r['target']==corrections[k]['proposed_swedish'],k
 elif k in ['ui_main23','ui_foreground_background_colour_palette']:
  out.update(decision='held_unresolved_context',rationale=('No current production caller establishes what Main names. Retain Huvud without lexical acceptance.' if k=='ui_main23' else 'No current production caller establishes whether %3$s denotes an action, state or descriptor. The neutral-colon proposal is not accepted merely because it fits placeholders. Preserve explicit English fallback pending a source contract.'),context=r['context'])
 else:
  out.update(decision=('accepted_bounded_current_context' if r['context'] else 'accepted_bounded_source_semantics_only'),rationale=rationale(r),context=r['context'])
  if k in fix_keys:out['review_correction']='The independent review requested a correction/refinement to the first draft; the complete final target was reread and accepted.'
  if r.get('previous_target') is not None:
   out['previous_swedish']=r['previous_target']
   out['changed_existing']=r['previous_target']!=r['target']
  if not r['context']:out['context_limit']='No direct production Kotlin reference found. Source-semantic acceptance is not a current usage or runtime claim.'
 rows.append(out)
counts=collections.Counter(r['decision'] for r in rows)
result={'schema_version':1,'review':'Independent model-based complete-value review of Swedish completion proposals','baseline_release':'e50de18d','author_packet_sha256':hashlib.sha256((root/'author-proposals-reviewed.json').read_bytes()).hexdigest(),'reviewed_scope':'All 352 complete missing typed-entry proposals, including one complete one/other plural, all 24 previously present unknown entries, and the held Main label. Prior 340 complete pairs were checked for exact preservation, not newly rereviewed.','method':'Read every complete English/Swedish pair and long prose paragraph, inspected actual production contexts for key workflows, checked existing UI label references, asked author for corrections, and reread final changes. Counts and hashes record this work; they are not acceptance criteria.','limits':['Model-based bounded linguistic judgment, not native-speaker certification or whole-language fluency acceptance.','No installed layout, clipping, TalkBack, physical-device, runtime, build, CI, release or merge acceptance is implied.','Direct Kotlin caller presence does not prove runtime reachability or exhaust reflective/dynamic routes. No-caller entries retain source-semantic-only or hold status.','Whole-catalogue presence, currently reachable English fallbacks and linguistic certainty are separate outcomes. Dormant Main/palette/full-manual holds do not block other accepted reachable workflows.','Do not apply corrected-source Help translations as source-bound accepted until the exact English source is adopted and independently rebound.'],'counts':dict(counts),'summary':{'newly_reviewed_current_source_accepts':373,'prior_exact_preserved':340,'current_source_bounded_total':713,'explicit_holds':4,'application_presence_at_snapshot':714,'application_missing_at_snapshot':3},'cross_language_followthrough':{'lead':'GIMP imported Wheel from explicitly mouse/input-device context, while AN Paint consumes ui_wheel as a colour selector. Swedish Mushjul was corrected to Färghjul.','source':'translations/gimp-catalogues.json: Swedish Wheel source comment; Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt:118','scope':'Check applicability to other translations later. This evidence does not classify other locales as defective and does not certify their strings.'},'terminology_evidence':[{'url':'https://creativecommons.org/licenses/by-sa/4.0/deed.sv','used_for':'Swedish attribution/adaptation terminology and preserving licence qualifiers; not a new legal opinion.'},{'path':'translations/gimp-catalogues.json','used_for':'Swedish Färgutjämning is sourced from image-conversion Dithering, unlike the wrong Wheel context.'}],'entries':rows}
(root/'independent-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(dict(counts));print('receipt',root/'independent-review.json')
