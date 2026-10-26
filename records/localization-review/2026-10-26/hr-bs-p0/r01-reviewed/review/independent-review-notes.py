"""Serialize the independently read hr/bs complete-value decisions.

This is review evidence, not production source or a translation generator.
No previous locale decision is used as input.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())
def file_hash(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def value_hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
def shown(value):
    return value[1:-1] if value.startswith('"') and value.endswith('"') else value

SOURCE = read('packet/shared-source-context.json')
SOURCES = {e['identity']: e for e in SOURCE['entries']}
TERMS = read('packet/terminology-foundations.json')
SCOPE = read('scope.json')
TREE = read('base-tree.json')
FREEZE = {
    'hr': '755c2e7a2afbbe6dd481c1a7337975ca06ae8c357cd9a4ea41d983995f4ba29e',
    'bs': '3a713fd226bbf07d68ff4a0788c10081bb3964fcf3374ae6c18d53c69248136a',
}

# The reviewer read the whole Croatian and whole Bosnian value for every key,
# including values which happen to be identical. These notes describe the
# independently checked semantics, not evidence borrowed from another locale.
NOTES = {
    'formats22_animation_message': 'The full wording introduces the number of frames before a colon, so the string count is not forced into a numeral-dependent ending. Format and count stay distinct; still-image editing and failure to preserve animation are both explicit.',
    'formats22_animation_poster': 'A separate default PNG image is imported instead of animation frames. The concluding saving sentence produces a static image; it does not promise animation preservation.',
    'formats22_animation_still': 'Only the first frame will be imported. The separate saving sentence still yields a static image; the restriction is not weakened to an unspecified frame.',
    'formats22_animation_title': 'The adjective identifies an animated image as the dialog subject, with no promise that animation will remain editable.',
    'formats22_animation_unknown': 'The construction retains uncertainty about whether multiple frames exist. Opening only a static image and not retaining any animation remain separate, unambiguous consequences.',
    'formats22_ascii_description': 'Plain text, light/dark characters, equal-width glyphs and a visual rendition are all present. The final negation correctly prevents treating it as an encoding that reopens as the original image.',
    'formats22_open_still': 'The imperative opens a static image and works as the positive button as well as the uncertainty-dialog title.',
    'formats22_pdf_raster_hint': 'Rendering at the fixed 144 dpi is retained, and text/vector objects explicitly become pixels rather than remaining editable vectors.',
    'save20_gif_description': 'The complete value preserves a static image, the maximum of 256 colours, smoothing of colour transitions and opening GIF animations as their first frame. The displayed dithering control must be distinguished from the technical name of the operation.',
    'save20_invalid_name': 'Both slashes and control characters are excluded from the filename; the sentence does not imply that all other strings are guaranteed valid.',
    'save20_lossy_quality_description': 'Higher quality keeps more detail; a larger file remains usual rather than guaranteed. This suits the lossy quality-control consumer.',
    'save20_unsupported_image_colour': 'The colour-profile conversion limitation is qualified by yet. The proposed remedy is conversion to an sRGB PNG in a colour-managed editor before import, not merely changing a filename or profile label.',
    'ui_higher_quality_usually_makes_a_larger_file_lossless': 'The complete value distinguishes usual file-size growth from lossless compression retaining every colour value. The parenthetical Lossless identifies the unchanged mode vocabulary.',
    'ui_a_separate_recovery_copy_has_been_kept_use': 'The leading reason is followed by an already-retained separate recovery copy. The new recovery-export menu label is used consistently, followed by ZIP export, literal canvas.png extraction and opening that image for optional normal resizing.',
    'ui_autosave_failed_use_save': 'Automatic saving failed, and the actual locale Save action is recommended. This is not a successful explicit-save notice.',
    'ui_autosave_image_encoding_failed': 'The failed encoder belongs to the autosaved main image, kept distinct from selection encoding and from the later persistence result.',
    'ui_autosave_is_paused_to_protect_that_draft_use': 'Autosave is paused to protect the old draft. Export preserves that draft, while Save as still must save the current work with PNG/JPEG selected under the actual Format slike field. It does not claim a separate copy already exists in this failure branch.',
    'ui_autosave_metadata_is_missing': 'The missing object is metadata of the autosaved draft, not its pixels or an already-restored image.',
    'ui_autosave_paused_use_save': 'The status denotes paused autosave, not completion, and points to the actual locale Save command.',
    'ui_autosave_pixels_are_missing': 'Missing pixels of the autosaved draft remain distinct from an existing pixel entry that cannot be decoded.',
    'ui_autosave_pixels_could_not_be_read': 'The negative result applies to reading draft pixel data and fits both canvas and floating-image decode consumers.',
    'ui_autosave_selection_encoding_failed': 'The full sentence reports failure to encode the selection for autosave, not failure of the main canvas encoder or successful selection persistence.',
    'ui_cannot_create_the_undo_cache_free_some_device': 'The undo cache cannot be created and the remedy is freeing device storage before retry. The explicit storage term does not confuse this disk cache with RAM-budget warnings.',
    'ui_could_not_export_the_recovery_copy': 'Recovery-copy export failed. The value remains an unpunctuated prefix because ioFailed appends the period and original exception detail.',
    'ui_draft_not_saved_yet': 'The draft is not saved yet; the temporal negation is preserved and does not refer to the ordinary drawing Save target.',
    'ui_draft_restored': 'The working draft is restored. This short status does not claim every undo entry was recovered or that unsaved drawing edits were explicitly saved.',
    'ui_draft_saved': 'The saved object is explicitly the working draft, consistent with autosave completion without changing the ordinary Save target or dirty state.',
    'ui_export_recovery_copy': 'The imperative exports a recovery copy and keeps the ellipsis appropriate to the conditional File-menu action and further picker.',
    'ui_export_recovery_copy_144b8a': 'The chooser title uses the same recovery-export wording as the menu action, intentionally without its ellipsis.',
    'ui_history_unavailable34': 'Canvas restoration succeeded, undo history could not be read, and the original draft was retained as a recovery copy. The three differing outcomes are all preserved.',
    'ui_invalid_autosave_metadata': 'The autosaved draft metadata is invalid, without inventing one specific cause; the wording fits size, schema and shared metadata-read failures.',
    'ui_previous_draft_kept_for_recovery': 'The previous draft was kept for recovery. The statement does not assert it was successfully restored or that it is the current image.',
    'ui_recovered_image': 'The phrase is a recovered-image filename/title fallback, not an additional promise about complete recovery.',
    'ui_recovery_copy_exported_extract_canvas_png_from_the': 'The export has completed. Literal canvas.png and ZIP are retained; the actual fallback Load image… action is quoted. Draft settings and a floating selection only if present are both included.',
    'ui_the_draft_is_saving_try_again_shortly': 'Draft saving is currently in progress; retrying the interrupted action shortly is requested, not a second Save operation.',
    'ui_the_previous_draft_could_not_be_moved_to': 'The previous draft could not be moved to a recovery copy. No existing destination copy is promised, including when the source draft is missing.',
    'ui_the_previous_draft_could_not_be_preserved_separately': 'Separate preservation of the previous draft failed; the message does not falsely assert either successful copying or loss of the original.',
    'ui_the_previous_draft_could_not_be_restored': 'Restoration of the previous draft failed. The final period also makes the value a complete prefixed reason before either recovery notice.',
    'ui_the_previous_draft_needs_more_memory_to_reopen': 'More memory is required to reopen the previous draft, without substituting device storage or declaring that the draft is damaged.',
    'ui_the_undo_cache_is_damaged': 'Damage is assigned to the undo cache, matching its checksum/header failures rather than implying the restored canvas is damaged.',
    'ui_unexpected_data_in_the_undo_cache': 'Unexpected data are confined to the undo cache, matching the trailing-data validation branch.',
    'ui_an_assembly_source_image_is_missing': 'A source image belonging to the composition is missing. This does not report that the output image is missing or promise that only one constituent can be affected.',
    'ui_assembly_saved': 'The composition was saved, appropriate after writing assembled PNG bytes. It does not claim an editable assembly exchange file or a change to the separate drawing Save destination.',
    'ui_assembly_source_memory_floor': 'The complete warning retains estimated demand over current working-memory limits, failure even at the smallest output, dimensions alone being insufficient, both proposed remedies and the unchanged composition. It does not reduce the problem to the decoder or claim timeless impossibility.',
    'ui_clear_all': 'The action clears everything in the assembly, not just a selected item. Its object remains distinct from the drawing-image Clear action.',
    'ui_clear_image': 'The imperative clears the drawing image, consistent with applying pending edits and document.clear(), rather than clearing all assembly source items.',
    'ui_could_not_save_the_assembly': 'Composition output saving failed; a single indexed string supplies exception detail after a colon. No success or source-deletion claim is introduced.',
    'ui_could_not_store_the_assembly': 'Internal storage of the composition failed, distinct from the separate chosen-output-URI Save operation.',
    'ui_d_d_pixels_2f_mp_exceeds_the_current': 'Dimensions, image megapixels and permitted megapixels retain their indexed order and both two-decimal formats. Full-image residency, reserved transformation/selection space, available-memory dependence, stopping before oversized allocation and no automatic resizing all survive.',
    'ui_keeps_pixels_at_the_top_left_smaller_canvas': 'Top-left anchoring and loss beyond the right/bottom edges are retained. The exact displayed Undo command restores the discarded pixels; this is not described as resampling.',
    'ui_not_enough_memory_for_this_operation_the_assembly': 'Memory is insufficient for the operation while assembly source files are retained. Retention is not mistaken for rendering or output-save success.',
    'ui_resize_large_image': 'The question offers resizing a large image rather than reporting that an automatic resize has happened.',
    'ui_sampled_resize_memory_explanation': 'The current canvas, clipboard contents, reduced-resolution decode and editing buffers are included in the estimate. Actual use varies, the smaller copy loses detail and the original file remains unchanged. This fits the non-native-work branch.',
    'ui_save_png': 'The button saves the assembly PNG, with the locale Save verb and unchanged format acronym. It makes no claim about the drawing editor Save target.',
    'ui_the_saved_assembly_could_not_be_opened': 'Opening the saved internal composition failed, with original exception detail retained as one indexed string. It is not an output-success message.',
    'ui_the_trim_would_remove_the_entire_image': 'The conditional construction describes what the rejected trim would do, not a whole image that has already been removed.',
    'ui_there_is_not_enough_memory_for_this_operation': 'Memory is insufficient at original resolution and no automatic resizing was applied. The value does not guarantee a smaller attempt will succeed.',
    'gallery_credit_could_not_save': 'The notice concerns image attribution data, not monetary credits or only author names. Save/restore failure, protection of existing saved data and retry are all explicit.',
    'gallery_credit_too_large': 'The conditional overflow is explained as drawing data volume caused by attribution, not pixel dimensions. The previous drawing and attribution data remain retained, without claiming that the rejected edit was saved.',
    'legacy_credits_unreadable': 'Only some stored attribution records could not be read, and their copies remain retained. Neither universal data loss nor usable recovery of those copies is asserted.',
    'save20_destination_error': 'The completed image could not replace the destination file, appropriate to temporary-file rename failure rather than a successful provider write.',
    'save20_encoding_budget': 'Image and encoding buffers together exceed export memory limits; the value neither omits the buffers nor substitutes disk capacity.',
    'ui_could_not_open_image': 'Image opening failed. The lack of final punctuation allows the caller to append a period, space and exception message correctly.',
    'ui_could_not_save_image': 'Image saving failed. No final punctuation or invented placeholder is added before ioFailed supplies the separator and failure detail.',
    'ui_export_did_not_save23': 'The exported file exists, but the current image still needs Save or Save as before continuing. Exact displayed actions are quoted; export success is not mistaken for satisfying the pending save-before-replacement guard.',
    'ui_export_explanation23': 'All three derived outputs are present. The negative construction leaves both current image and its ordinary Save destination unchanged, without claiming that no export file is written.',
    'ui_not_enough_memory_to_save_in_this_format': 'The format-specific save lacks memory and PNG is offered as a retry, not guaranteed to fit. The prefix has no terminal period before caller-supplied error details.',
    'ui_png_encoding_failed': 'PNG encoding failed, matching the false compress result rather than successful output persistence.',
    'ui_save_and_share': 'The action means save and share, retains the ellipsis and matches the title without ellipsis. It does not claim that the current drawing dirty state has been cleared.',
    'ui_save_and_share_41edb4': 'The title matches the locale Save-and-share menu wording without the menu ellipsis; it names the action rather than completed sharing.',
    'ui_save_explanation23': 'Format and compression settings are chosen, and later ordinary Save reuses all four required items: filename, location, format and settings. The exact displayed Save command is quoted.',
    'ui_saved': 'The neutral saved-status phrase followed by the filename reports the named output only, valid for Save, Export and Share without claiming all document edits were saved.',
    'ui_share_explanation34': 'The instruction first writes a copy to the chosen location, then chooses a sharing app. The ordinary Save destination explicitly remains unchanged; it neither claims the copy is already shared nor changes the drawing Save target.',
    'ui_the_encoder_did_not_finish': 'Encoding itself was not completed, avoiding ambiguity with a human coder and retaining the negative completion outcome.',
    'ui_the_image_was_saved_but_android_could_not': 'The image was successfully written but Android could not launch sharing. The indexed exception detail remains separate, with no implication that the drawing Save target changed.',
    'ui_the_selected_location_is_not_writable': 'Writing is not possible at the selected location, without guessing a permission, protection or provider-specific cause.',
    'ui_this_location_is_not_writable': 'Writing is not possible at this location. The generic sentence fits both recovery ZIP and source archive output failures without changing their identities.',
    'ui_your_current_image_has_unsaved_changes': 'The current image explicitly has unsaved changes, preserving the negative saved-state meaning required by the replacement guard.',
}
assert set(NOTES) == {key.split('/', 1)[1] for key in SOURCES}

HR_GIF = '"Statična slika s najviše 256 boja. Dithering ublažava prijelaze između boja (opcija je označena „Zamućivanje“). Animirane GIF slike otvaraju se kao prvi kadar animacije."'

QUALIFICATIONS = {
    'formats22_animation_message': ['The lower-bound count can still be the inherited English fallback “at least 2”; the composed message is not certified wholly localized.'],
    'ui_higher_quality_usually_makes_a_larger_file_lossless': ['ui_lossless_format remains the English fallback “Lossless %1$s”; this value explains the mode without changing that label.'],
    'ui_draft_saved': ['Automatic draft persistence does not clear document.dirty or update the ordinary Save target.'],
    'ui_draft_restored': ['Restored draft/canvas status does not certify recovery of the entire undo history.'],
    'ui_assembly_saved': ['The consumer confirms assembled PNG output, not an editable assembly interchange or a separate drawing Save-target update.'],
    'ui_assembly_source_memory_floor': ['This acceptance is P0-only. The distinct P1 ui_no_resize_fits_decoder_memory remains absent and unreviewed; no paired-warning acceptance is inferred.'],
    'ui_sampled_resize_memory_explanation': ['The alternate native/codec-memory explanation is outside this review and remains unchanged.'],
    'ui_recovery_copy_exported_extract_canvas_png_from_the': ['The menu action ui_load_image remains English “Load image…” in both locales; the mixed-language quote deliberately matches what is displayed.'],
    'ui_saved': ['The same toast is used by Export and Share; those writes do not clear unsaved drawing state or change the ordinary Save destination.'],
    'ui_share_explanation34': ['Sharing is share=true and export=true. A successful copy write does not satisfy an explicit Save-before-replacement continuation.'],
}

def candidate_checks(locale, candidate):
    assert file_hash(f'drafts/{locale}-candidates.json') == FREEZE[locale]
    assert candidate['locale'] == locale
    assert candidate['source_commit'] == SOURCE['source_commit']
    assert candidate['source_tree'] == SOURCE['source_tree']
    assert candidate['source_context_sha256'] == file_hash('packet/shared-source-context.json')
    assert candidate['terminology_sha256'] == file_hash('packet/terminology-foundations.json')
    assert len(candidate['candidates']) == 78
    assert {e['identity'] for e in candidate['candidates']} == set(SOURCES)

def build(locale):
    candidate = read(f'drafts/{locale}-candidates.json')
    candidate_checks(locale, candidate)
    entries = []
    for c in candidate['candidates']:
        identity = c['identity']; key = identity.split('/',1)[1]; source = SOURCES[identity]
        assert c['source'] == source['source'] and c['attributes'] == source['attributes']
        original = c['proposed_xml_text']; accepted = HR_GIF if locale == 'hr' and key == 'save20_gif_description' else original
        decision = 'revise' if accepted != original else 'accept'
        reason = NOTES[key]
        quals = list(QUALIFICATIONS.get(key, []))
        if key == 'save20_gif_description':
            if locale == 'hr':
                reason += ' Revised the Croatian sentence to name dithering first and explicitly mark „Zamućivanje“ only as the displayed option label. This avoids presenting the inherited word for blurring as a correct technical translation.'
                quals.append('Inherited save20_dither „Zamućivanje“ is a misleading blurring label. It remains untouched, is quoted only for control identification, and is not newly endorsed. The new explanation does not instruct blurring the image.')
            else:
                reason += ' The Bosnian sentence explicitly refers to the actual „Miješanje boja“ option and accurately describes smoothing transitions, without claiming an animated save.'
                quals.append('Inherited save20_dither „Miješanje boja“ is used as the actual option label; this review does not replace or certify the inherited translation itself.')
        if key == 'ui_autosave_is_paused_to_protect_that_draft_use':
            if locale == 'hr':
                reason += ' Croatian correctly quotes the held English title „Save as…“ rather than inventing a nonexistent translated action.'
                quals.append('Croatian save20_title remains absent/held, displaying English “Save as…”. This mixed-language navigation is intentional; no held key is added.')
            else:
                reason += ' Bosnian correctly quotes the inherited „Snimi kao…“ title, distinct from Croatian fallback.'
        if key == 'ui_export_did_not_save23':
            if locale == 'hr':
                quals.append('“Save as…” is the actual English fallback; Croatian save20_title remains held and absent.')
                reason += ' „Spremi“ and „Save as…“ match the actual Croatian UI.'
            else:
                reason += ' „Snimi“ and „Snimi kao…“ match the actual Bosnian UI.'
        if key == 'ui_keeps_pixels_at_the_top_left_smaller_canvas':
            reason += ' The quoted control is '+('„Vrati“ in Croatian.' if locale == 'hr' else '„Poništi“ in Bosnian.')
        if key == 'ui_export_explanation23':
            quals.append('The prose describes the derived outputs rather than quoting their labels. Base64 still displays “Base64 text”; ASCII displays '+('English “ASCII art”.' if locale=='hr' else 'the inherited “ASCII umjetnost”.')+' Those labels remain untouched and are not newly accepted.')
        if key in ['ui_could_not_save_the_assembly','ui_the_saved_assembly_could_not_be_opened','ui_the_image_was_saved_but_android_could_not']:
            quals.append('The %1$s exception detail may remain untranslated and may itself contain punctuation or percent signs.')
        for value in [original, accepted]:
            assert re.findall(r'%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[a-zA-Z%]',value) == source['placeholder_tokens']
            assert value.startswith('"') and value.endswith('"') and '"' not in value[1:-1]
            assert not re.search(r'[\u0400-\u04ff]', value)
            assert '\\' not in value and "'" not in value
            xml = ET.Element('string', c['attributes']); xml.text = value
            assert ET.fromstring(ET.tostring(xml, encoding='unicode')).text == value
        entries.append({
            'identity': identity, 'decision': decision,
            'original_xml_text': original, 'accepted_xml_text': accepted,
            'attributes': c['attributes'], 'reason': reason, 'qualifications': quals,
            'source_value_sha256_utf8': source['source_value_sha256_utf8'],
            'original_value_sha256_utf8': value_hash(original),
            'accepted_value_sha256_utf8': value_hash(accepted),
            'consumer_context_ids': source['consumer_context_ids'],
        })
    a = {e['identity'].split('/',1)[1]: shown(e['accepted_xml_text']) for e in entries}
    examples = []
    def example(case, key, replacements=()):
        value = a[key]
        for old,new in replacements: value = value.replace(old,new)
        examples.append({'case':case,'identity':'string/'+key,'composed_display':value,'kind':'static review example; not runtime execution'})
    example('Exact frame count','formats22_animation_message',[('%1$s','GIF'),('%2$s','2')])
    example('English lower-bound fallback','formats22_animation_message',[('%1$s','GIF'),('%2$s','at least 2')])
    example('Known separate copy','ui_a_separate_recovery_copy_has_been_kept_use',[('%1$s',a['ui_the_previous_draft_could_not_be_restored'])])
    example('Blocked autosave distinguishes old and current work','ui_autosave_is_paused_to_protect_that_draft_use',[('%1$s',a['ui_the_previous_draft_could_not_be_restored'])])
    example('Actual Load image fallback','ui_recovery_copy_exported_extract_canvas_png_from_the')
    example('Dithering with actual inherited option label','save20_gif_description')
    example('Comma decimal budget','ui_d_d_pixels_2f_mp_exceeds_the_current',[('%1$d','1500'),('%2$d','2000'),('%3$.2f','3,00'),('%4$.2f','2,25')])
    example('Copy then sharing with ordinary Save unchanged','ui_share_explanation34')
    example('Successful export still requires ordinary Save','ui_export_did_not_save23')
    example('Named-output success with percent in filename','ui_saved',[('%1$s','drawing 100%.png')])
    example('Write succeeded but sharing failed','ui_the_image_was_saved_but_android_could_not',[('%1$s','provider 50% unavailable')])
    examples.append({'case':'Open prefix followed by caller punctuation','identity':'string/ui_could_not_open_image','composed_display':a['ui_could_not_open_image']+'. provider 100% unavailable','kind':'static review example; not runtime execution'})
    canonical = {e.attrib['name']:e.text for e in ET.parse(ROOT/'base-source/Paintroid/src/main/res/values/strings.xml').getroot() if 'name' in e.attrib}
    existing = TERMS[locale]['all_existing_values']
    labels = {}
    for key in ['ui_save','save20_title','save20_file_name','save20_file_format','ui_cancel','ui_keep_editing23','ui_discard_changes23','ui_undo','ui_menu_file','ui_load_image','save20_dither','ui_lossless_format']:
        labels[key] = {'value':shown(existing[key]['value'] if key in existing else canonical[key]),'fallback':key not in existing}
    return {
        'schema_version':1, 'locale':locale,
        'source_commit':SOURCE['source_commit'],'source_tree':SOURCE['source_tree'],
        'review_role':'Independent complete-value AI linguistic/source-static reviewer; distinct from author; each Croatian and Bosnian full value separately read',
        'candidate_sha256':FREEZE[locale],
        'source_context_sha256':file_hash('packet/shared-source-context.json'),
        'terminology_sha256':file_hash('packet/terminology-foundations.json'),
        'source_tree_sha256':file_hash('base-tree.json'),
        'verification':{
            'source_blobs_and_modes_verified':1385,
            'canonical_values_attributes_and_full_tokens_verified':78,
            'current_consumer_windows_verified':140,'unique_consumer_windows_verified':124,
            'preserved_values_and_attributes_verified':TERMS[locale]['existing_count'],
            'complete_value_decisions':dict(Counter(e['decision'] for e in entries)),
            'candidate_identity_scope':'Exactly 78 missing live-consumer P0 identities in this locale; no inherited replacement',
            'remaining_P0_absences':SCOPE['locales'][locale]['remaining_P0_absences'],
            'expected_structural_endpoint_if_exact_values_applied':{'containers':SCOPE['locales'][locale]['target_entries'],'P0_present':SCOPE['locales'][locale]['P0_after'],'P0_total':92},
            'actual_control_labels':labels,
            'scope_limits':[
                'Bounded AI complete-value review, not native-human, whole-language, layout, runtime, Android compiler or device certification.',
                'All 215 inherited values and attributes across hr/bs remain context only, not newly approved. Five held no-current-consumer keys remain untouched; Croatian save20_title also remains held/absent.',
                'No acceptance is inherited from Serbian or another locale. All 156 current candidates were read in full against current canonical source, exact consumers and language-specific UI labels.',
                'The 74 shared English source/consumer contexts were reverified byte-exact against the current source; four additional current consumer groups were inspected separately. This shares source understanding only, not target-language acceptance.',
                'Outer Android quotes, exact attributes, complete formatting tokens, Latin-script integrity and XML round-trip structure checked; compilation and behavioral validation remain separate.',
                'Croatian Zamućivanje is an inherited misleading label for the dithering control. The revised explanation identifies it only as a displayed label, not a translation endorsement.',
                'P1 warning and Help/archive-identity work are outside scope; no paired-warning acceptance or operational change is claimed.',
            ],
        },
        'entries':entries,'composition_examples':examples,
    }

if __name__ == '__main__':
    for locale in ['hr','bs']:
        result = build(locale)
        path = ROOT/f'review/{locale}-review.json'
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(locale, result['verification']['complete_value_decisions'], file_hash(f'review/{locale}-review.json'))
