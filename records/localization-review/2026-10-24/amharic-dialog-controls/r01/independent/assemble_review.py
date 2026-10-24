import collections, hashlib, json, pathlib, re, unicodedata, xml.etree.ElementTree as ET
P = pathlib.Path(__file__).parent.parent/'amharic-dialog-controls-draft-20261024'
O = pathlib.Path(__file__).parent
SHA = '5955bf3fa6f1e3f072b44c56948166446ad91d5c6111576e5bc2b0036db0d944'
COMMIT = '66be61df27c5359bffc32d56db21f3949899f873'
ROOT = f'https://github.com/c933103/AN-Paint/blob/{COMMIT}/Paintroid/src/main/java/org/catrobat/paintroid/classic/'
manifest = json.loads((P/'MANIFEST.json').read_text())
assert hashlib.sha256((P/'MANIFEST.json').read_bytes()).hexdigest() == SHA
assert all(hashlib.sha256((P/n).read_bytes()).hexdigest()==v for n,v in manifest['files'].items())
bindings=json.loads((P/'source-bindings.json').read_text())
for r in bindings.values():
 b=(P/r['local_complete_copy']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob']
occ = json.loads((P/'direct-consumer-occurrences.json').read_text())
actual=[]
for f in (P/'source').rglob('*.kt'):
 for i,line in enumerate(f.read_text().splitlines(),1):
  actual += [(f.relative_to(P/'source').as_posix(),i,'string/'+m[1]) for m in re.finditer(r'R\.string\.(ui_ok|ui_done|ui_cancel|ui_apply)\b',line)]
assert collections.Counter(actual)==collections.Counter((x['path'],x['line'],x['key']) for x in occ)
rs=json.loads((P/'lexical-evidence/exact-records.json').read_text())
for r in rs:
 if r['format']=='paired Android XML resource':
  for lang in ('english_record','amharic_record'):
   e=r[lang];raw=(P/'lexical-evidence'/e['source_file']).read_text().splitlines()
   assert '\n'.join(raw[e['start_line']-1:e['end_line']]).strip()==e['raw_xml_record']
   node=next(x for x in ET.parse(P/'lexical-evidence'/e['source_file']).getroot() if x.tag=='string' and x.get('name')==e['key'])
   assert node.attrib==e['attributes']
   assert ''.join(node.itertext()).strip('"')==r['english' if lang=='english_record' else 'amharic']
 else:
  raw=(P/'lexical-evidence'/r['source_file']).read_text().splitlines()
  assert '\n'.join(raw[r['start_line']-1:r['end_line']])==r['raw_po_record']

# Each entry below was reviewed against the relevant full method and callback chain.
findings = {
 ('SaveOptionsDialog.kt',190,'ui_cancel'): ('Invokes cancel(), then the ordinary negative-button dismissal. The supplied caller clears afterSave and shareAfterSave; no export/save request is confirmed.', ['SaveOptionsDialog.kt#L187-L201','ClassicPaintActivity.kt#L1110-L1121']),
 ('ImageResizeDialog.kt',38,'ui_cancel'): ('The negative button dismisses; onDismiss invokes cancel() while accepted is false. Supplied caller deletes the staged import copy, clears pendingImportFile, and ends I/O. Not deletion of the original provider source.', ['ImageResizeDialog.kt#L35-L61','ClassicPaintActivity.kt#L1299-L1306']),
 ('ImportSelection.kt',96,'ui_cancel'): ('cancel() calls dispose() then cancelled(): disposes this staged file/preview and invalidates the pending generation. ClassicPaintActivity ends I/O; AssemblyActivity advances to the next batch item. Does not universally abort an entire batch.', ['ImportSelection.kt#L69-L96','ClassicPaintActivity.kt#L1281-L1290','AssemblyActivity.kt#L247-L260']),
 ('ImportSelection.kt',116,'ui_cancel'): ('Same cancellation chain as the animation chooser: abandons this staged page selection; AssemblyActivity continues with the next item.', ['ImportSelection.kt#L69-L76','ImportSelection.kt#L113-L117','AssemblyActivity.kt#L247-L260']),
 ('ClassicPaintActivity.kt',239,'ui_done'): ('In the session-restoration exception path, shows the could-not-save-or-restore message. Done has a null positive listener and acknowledges/dismisses it; no save, restore, retry, or success transition occurs in that callback.', ['ClassicPaintActivity.kt#L231-L240']),
 ('ClassicPaintActivity.kt',824,'ui_cancel'): ('Dismisses the tool-option chooser without choosing a new option. A selection instead applies immediately and dismisses, so Cancel is not undo of earlier selections.', ['ClassicPaintActivity.kt#L819-L825']),
 ('ClassicPaintActivity.kt',892,'ui_done'): ('Closes the About/credits chooser via a null negative listener; does not open a selected action or save.', ['ClassicPaintActivity.kt#L877-L892']),
 ('ClassicPaintActivity.kt',909,'ui_cancel'): ('Dismisses the Other images source chooser; the source-selection callback, not Cancel, launches an import or gallery.', ['ClassicPaintActivity.kt#L895-L909']),
 ('ClassicPaintActivity.kt',992,'ui_cancel'): ('Dismisses the palette-slot replacement chooser before a slot is chosen.', ['ClassicPaintActivity.kt#L985-L1001']),
 ('ClassicPaintActivity.kt',1009,'ui_cancel'): ('Dismisses palette-action menu. Does not perform background-colour, edit-colour, or remove-palette action; does not undo previously committed palette work.', ['ClassicPaintActivity.kt#L1003-L1009']),
 ('ClassicPaintActivity.kt',1018,'ui_cancel'): ('Dismisses dimensions form without invoking its positive listener. Existing document changes outside the form are not rolled back.', ['ClassicPaintActivity.kt#L1012-L1027']),
 ('ClassicPaintActivity.kt',1018,'ui_apply'): ('Overrides the positive button: requires dimensions; editAction checks size/budget, applies pending canvas work, creates or resizes the document, fits the canvas, updates status, and dismisses only after that path reaches the end. Validation/failure can prevent dismissal.', ['ClassicPaintActivity.kt#L1012-L1027','ClassicPaintActivity.kt#L924-L930']),
 ('ClassicPaintActivity.kt',1054,'ui_cancel'): ('Runs cancelTrim(), which clears trim, fits, invalidates, and updates status; then hides trim controls. beginTrim() had already called applyPending(). Not blanket Undo of earlier drawing/selection commits.', ['ClassicPaintActivity.kt#L1044-L1057','PaintCanvas.kt#L429-L436']),
 ('ClassicPaintActivity.kt',1162,'ui_cancel'): ('Dismisses the recovery-copy chooser without selecting and exporting one.', ['ClassicPaintActivity.kt#L1152-L1162']),
 ('ClassicPaintActivity.kt',1572,'ui_done'): ('Closes drawing/magnifier settings. Toggle/slider callbacks already update their values, invalidate the canvas, and schedule autosave before Done. Done itself does not newly save or roll back them.', ['ClassicPaintActivity.kt#L1553-L1572']),
 ('ClassicPaintActivity.kt',1587,'ui_ok'): ('Generic informational/error/help acknowledgement: null positive listener closes the message, without a caller-specific mutation or success assertion.', ['ClassicPaintActivity.kt#L1586-L1587']),
 ('NumericSlider.kt',71,'ui_apply'): ('Overrides positive listener; accepts an integer within bounds, sets slider.progress, and dismisses. Changed progress invokes changed(n) through the SeekBar listener. An unchanged value need not trigger a new change; invalid input shows an error and stays open.', ['NumericSlider.kt#L60-L76']),
 ('NumericSlider.kt',71,'ui_cancel'): ('Dismisses exact-entry dialog without applying the typed value. It does not undo prior outer-slider changes.', ['NumericSlider.kt#L60-L76']),
 ('AssemblyPlacementDialog.kt',70,'ui_cancel'): ('Dismisses the exact-position form without assembly.position().', ['AssemblyPlacementDialog.kt#L29-L43','AssemblyPlacementDialog.kt#L64-L72']),
 ('AssemblyPlacementDialog.kt',71,'ui_apply'): ('Overrides positive listener; requires finite, nonnegative integral coordinates within Int range; calls assembly.position and dismisses. Exceptions set error text and leave it open.', ['AssemblyPlacementDialog.kt#L29-L43','AssemblyPlacementDialog.kt#L64-L72']),
 ('LegacyImageCreditsActivity.kt',127,'ui_done'): ('Calls Activity.finish(). Add-to-image and Save-text actions are separate. Ending the view does not assert an earlier export succeeded.', ['LegacyImageCreditsActivity.kt#L102-L127','LegacyImageCreditsActivity.kt#L148-L155']),
 ('LegalInfo.kt',120,'ui_cancel'): ('Dismisses nested Other terms chooser without navigating to another notice.', ['LegalInfo.kt#L104-L120']),
 ('LegalInfo.kt',122,'ui_done'): ('Calls dialog.dismiss(); unregisters the configuration callback through onDismiss. This is notice closure, not consent or save.', ['LegalInfo.kt#L122-L137']),
 ('NormalizeImagesDialog.kt',38,'ui_cancel'): ('Dismisses the normalization form; does not invoke assembly.normalize. Separate Restore original sizes action applies and dismisses directly; Cancel is not rollback of prior completed actions.', ['NormalizeImagesDialog.kt#L37-L48','NormalizeImagesDialog.kt#L68-L84']),
 ('VerticalFeedbackView.kt',73,'ui_done'): ('Both text Done and compact accessible equivalent invoke the supplied dismiss lambda. The independently checked source addendum binds it to LocaleNotification.Notice.dismiss(), which cancels expiry/deferred-dismiss callbacks and removes the notice view. No underlying operation save, retry, or success transition. Instantiation is in the vertical-only branch.', ['VerticalFeedbackView.kt#L67-L87','LocaleTypography.kt#L43-L48','LocaleNotification.kt#L82-L107','LocaleNotification.kt#L175-L183']),
 ('AppLanguage.kt',166,'ui_done'): ('Closes language-settings summary; choosing its current-language row instead opens the picker.', ['AppLanguage.kt#L162-L167']),
 ('AppLanguage.kt',197,'ui_cancel'): ('Dismisses language picker without selecting a locale. Clicking a language applies and closes immediately; Cancel is not a rollback of an already selected language.', ['AppLanguage.kt#L181-L201']),
 ('MediaGalleryActivity.kt',63,'ui_done'): ('In failed credit-session open/create path, Done calls finish(). Existing input is kept for recovery. It does not retry or assert successful save/restore.', ['MediaGalleryActivity.kt#L49-L66','MediaGalleryActivity.kt#L435-L441']),
 ('MediaGalleryActivity.kt',114,'ui_done'): ('Calls finish() to exit gallery. Prior accepted credit edits may already have set a result; lifecycle may preserve a draft or discard an unaccepted empty session. No universal save or rollback claim.', ['MediaGalleryActivity.kt#L107-L114','MediaGalleryActivity.kt#L235-L249','MediaGalleryActivity.kt#L409-L441']),
 ('ImageCropDialog.kt',142,'ui_cancel'): ('Dismisses crop form without invoking apply(crops). Preview/reset/include controls update local prospective selection; actual crop apply is the positive callback.', ['ImageCropDialog.kt#L125-L150']),
 ('AssemblyActivity.kt',120,'ui_ok'): ('Generic message acknowledgement with null positive listener; no application-specific mutation callback. Used for failure messages as well as help.', ['AssemblyActivity.kt#L117-L121','AssemblyActivity.kt#L347']),
 ('AssemblyActivity.kt',308,'ui_cancel'): ('Dismisses output-size form without calling makeOutput. No assertion of file creation/deletion or rollback of assembly edits.', ['AssemblyActivity.kt#L297-L317']),
 ('GalleryCredits.kt',135,'ui_done'): ('OnShow overrides the positive listener: if(save()) dialog.dismiss(). save() validates bounds, snapshots text, runs onEdit, catches validation/I/O errors with false, and updates entries only on success. Dismissal additionally invokes onDismiss unless preserving. This Done is an attempted accept/save-and-close, not close-only and not pre-certified success.', ['GalleryCredits.kt#L100-L116','GalleryCredits.kt#L131-L146','ClassicPaintActivity.kt#L1466-L1479','MediaGalleryActivity.kt#L235-L245']),
 ('AdvancedColourDialog.kt',305,'ui_cancel'): ('Negative/onCancel invokes preview(original); onDismiss repeats preview rollback if not accepted and calls closed(). Does not invoke commit. Explicitly restores preview but does not undo separately saved palette entries.', ['AdvancedColourDialog.kt#L304-L327','AdvancedColourDialog.kt#L338-L345','ClassicPaintActivity.kt#L995-L1001']),
 ('AdvancedColourDialog.kt',345,'ui_cancel'): ('Dismisses palette-slot replacement chooser without selecting a replacement. Does not undo earlier palette saves or close the entire outer colour editor.', ['AdvancedColourDialog.kt#L338-L345']),
 ('TextStyleDialog.kt',99,'ui_cancel'): ('Dismisses text-placement form without commit(settings, face). Form preview is separate; positive action validates and commits.', ['TextStyleDialog.kt#L69-L111']),
}
assert len(findings)==36
ledger=[]
for x in occ:
 f=pathlib.PurePosixPath(x['path']).name;k=x['key'].split('/')[1]
 effect,refs=findings[(f,x['line'],k)]
 ledger.append(dict(x,reviewed_effect=effect,supporting_links=[ROOT+r for r in refs],review_method='Static full-method and supplied callback-chain inspection; not runtime execution.'))

def ev(ids):
 return [{'record_id':r['id'],'english':r['english'],'amharic':r['amharic'],'source_url':r.get('pinned_source_url') or r['amharic_record']['pinned_source_url']} for r in rs if r['id'] in ids]
english={x.get('name'): ''.join(x.itertext()) for x in ET.parse(P/'source/Paintroid/src/main/res/values/strings.xml').getroot() if x.tag=='string'}
amharic={x.get('name') for x in ET.parse(P/'source/Paintroid/src/main/res/values-b+am/strings.xml').getroot()}
for key,value in [('ui_ok','OK'),('ui_done','Done'),('ui_cancel','Cancel'),('ui_apply','Apply')]:
 assert english[key]==value and key not in amharic

common_limit='Independent static evidence review only, not native-reader approval, rendering/speech/accessibility validation, production acceptance, or release authorization.'
rows=[
 {'key':'string/ui_ok','english':'OK','draft':'እሺ','verdict':'retain','replacement':None,'confidence':{'lexical_attestation':'high','fit_to_inspected_callbacks':'high','overall':'high within bounded static review'},'reason':'Exact generic AOSP OK is independently corroborated by LibreOffice stock OK. Neutral acknowledgement fits both supplied null-listener message helpers without adding save, success, or consent meaning.','primary_evidence':ev(['aosp_settings_okay','aosp_gallery2_ok','lo_cui_stock_ok']),'consumer_count':2,'scope_limit':common_limit},
 {'key':'string/ui_done','english':'Done','draft':'ተከናውኗል','verdict':'hold','replacement':None,'confidence':{'lexical_attestation':'high','fit_to_all_inspected_contexts':'unresolved for failed-save/restore notices','hold_decision':'high','overall':'insufficient for unqualified retain'},'reason':'Exact AOSP Done convention is well attested, but that alone does not establish how an Amharic reader interprets the completed-result form beside a failed-save/restore notice. Two real callbacks only acknowledge/exit failure; others close views/live settings; GalleryCredits attempts a validated save before close. Do not describe this as a proven mistranslation or success assertion, and do not invent a Close/OK translation for unchanged English Done.','primary_evidence':ev(['aosp_settings_done','aosp_gallery2_done']),'consumer_count':10,'unblock_condition':'Obtain contextual linguistic evidence that this conventional button is understood as finishing/dismissing the interaction, not as reporting successful save/restore, with the actual failure message and the contrasting save-and-close form. No source edit is mandated by this evidence.','source_gate':'If a genuine English-label/caller defect is established, correct English and flag the affected term across all languages, then review them individually. Do not compensate only in Amharic.','scope_limit':common_limit},
 {'key':'string/ui_cancel','english':'Cancel','draft':'ይቅር','verdict':'retain','replacement':None,'confidence':{'lexical_attestation':'high','fit_to_inspected_callbacks':'high','overall':'high within bounded static review'},'reason':'The generic AOSP Cancel pair is corroborated by Gallery2. It fits abandoning the current interaction across dismissal, staged-item cancellation, colour-preview rollback and trim cancellation. Prefer it over an unsupported global Undo reading and over importing the glossary form ሰርዝ when the same retained AOSP sources use that for Delete. The glossary alternative is not declared wrong in every context.','primary_evidence':ev(['aosp_settings_cancel','aosp_gallery2_cancel','android_settings_delete_contrast','android_gallery2_delete_contrast']),'consumer_count':21,'important_qualifiers':['Assembly import cancellation advances to the next file; it is not whole-batch abort.','Staged temporary file cleanup is not deletion of the original provider file.','Trim entry already applies pending canvas work; cancelling trim is not undo of that prior work.','Colour preview rollback does not undo separately committed palette actions.'],'scope_limit':common_limit},
 {'key':'string/ui_apply','english':'Apply','draft':'ተግብር','verdict':'retain','replacement':None,'confidence':{'lexical_attestation':'high','fit_to_inspected_callbacks':'high','overall':'high within bounded static review'},'reason':'Exact AOSP imperative matches putting selected changes into effect; bounded glossary entry 149 independently corroborates the same form. All three exact-key consumers validate the prospective input and then invoke the relevant change. The label does not promise success, file persistence, or automatic dismissal on invalid input.','primary_evidence':ev(['aosp_settings_apply']),'bounded_additional_evidence':{'record_id':'ict_apply_149','entry':149,'pdf_page_ordinal':12,'english':'apply','amharic':'ተግብር','url':'https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf','independent_verification_limit':'This reviewer used the supplied bounded reference, not a new PDF render or publisher-authentication check; AOSP exact pair is independently checked from retained XML.'},'consumer_count':3,'scope_limit':common_limit+' No acceptance transfers to ui_apply_to_all, ui_apply_crop, ui_apply_bounds, or ui_apply_to_these_images.'}
]
for r in rows:
 assert unicodedata.normalize('NFC',r['draft'])==r['draft']
 ET.fromstring(f'<string name="{r["key"].split("/")[1]}">"{r["draft"]}"</string>')
limits=[
 'Input is the exact sealed packet, not a fresh exhaustive repository crawl. Current-commit/tree claims originate in supplied provenance; this reviewer independently recomputed all 29 Git blob identities but did not re-fetch production branch state.',
 'All 36 direct references in the supplied Kotlin corpus match its ledger: 2 OK, 10 Done, 21 Cancel, 3 Apply across 17 files. Indirect callback effects were followed in the supplied files and two commit-bound addendum files. The omitted original-packet VerticalFeedbackCard caller is resolved by the addendum; this is still not a fresh exhaustive whole-repository search.',
 'Six retained snapshots and all 16 exact lexical records are integrity-checked; external snapshots were reused, not freshly fetched. Settings and Gallery2 are related AOSP sources, not independent translation authorities.',
 'Glossary evidence remains bounded to attributed word pairs/links. Public mirror authorship/revision is unauthenticated; this reviewer did not re-render its PDF. No full glossary or page images are included.',
 'No native-reader consultation, layout/rendering, speech/accessibility, Android lifecycle execution, build, CI, production edit, Work task, deployment or release was performed.',
 'Prior 69 ready and 11 held keys remain separate and are not re-evaluated, merged into these verdicts, or implemented. All four exact target keys remain absent from the supplied production Amharic resource.',
 'A hold is an unresolved evidence gate, not a finding that the English source or existing target convention is wrong. No alternate target wording is recommended without evidence.'
]
result={'title':'Independent review of four Amharic common dialog controls','review_date_utc':'2026-10-24','input_manifest_sha256':SHA,'source_commit':COMMIT,'source_tree':'870c5a584120d92710be516af0dc3b3847b183d9','verdict_counts':{'retain':3,'revise':0,'hold':1},'verdict_meaning':'Retain the proposed wording in this bounded independent review; no production edit or release approval. Hold remains untranslated/unaccepted for implementation pending the stated evidence.','rows':rows,'scope_limits':limits,'source_gate':'No English defect established. Preserve current English semantics; if an actual source defect is later established, correct English first, flag all affected languages, then review individually.','production_state':{'present':12,'missing':705,'canonical_containers':717,'implementation_changes':0,'prior_ready_excluded':69,'prior_holds_excluded':11}}
validation={'input_manifest_sha256':SHA,'input_manifest_files':len(manifest['files']),'input_manifest_file_hashes_verified':True,'source_git_blob_count':len(bindings),'source_git_blobs_verified':True,'direct_reference_count':len(actual),'direct_caller_files':len(set(a[0] for a in actual)),'key_counts':dict(collections.Counter(a[2] for a in actual)),'direct_ledger_matches_supplied_corpus':True,'external_and_project_snapshot_count':6,'exact_lexical_records_verified':len(rs),'candidate_count':4,'candidate_nfc_and_xml_parse':True,'production_resources_modified':False,'source_updates_performed':False,'build_ci_runtime_performed':False,'native_reader_approval':False,'callback_chain_exhaustive':'Resolved for the reviewed 36-reference bounded corpus; not a fresh exhaustive repository search.','callback_chain_limit':'Original packet omitted two indirect sources; the separate commit-bound addendum now resolves them.'}
for n,d in [('review.json',result),('callback-audit.json',ledger),('validation.json',validation)]:
 (O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

# Seal and retain the two independently verified supplemental sources separately.
addendum=P.parent/'amharic-dialog-controls-source-addendum-20261024'
evidence=O/'source-addendum';evidence.mkdir(exist_ok=True)
addendum_records=[]
for name,bind in [('LocaleTypography.kt','binding.json'),('LocaleNotification.kt','locale-notification-binding.json')]:
 r=json.loads((addendum/bind).read_text());b=(addendum/name).read_bytes()
 assert r['commit']==COMMIT and r['tree']==result['source_tree']
 assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 (evidence/name).write_bytes(b)
 addendum_records.append(dict(r,immutable_url=ROOT+name))
validation['supplemental_source_git_blobs_verified']=2
validation['total_source_files_with_verified_git_blob_identity']=31
(O/'source-addendum-bindings.json').write_text(json.dumps(addendum_records,ensure_ascii=False,indent=2)+'\n')
(O/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
