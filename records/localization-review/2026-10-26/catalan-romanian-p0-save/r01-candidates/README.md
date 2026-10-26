# Catalan / Romanian: bounded P0 Save, export and share candidates

Source is pinned to merged `05607f0d60131cc9148461ce595155d820748e4e`, tree `16ff3d877650ad4ad3198ce19007e8606fcd080a`. This frozen author packet proposes **10 missing P0 values per locale, 20 total**. Its pending-review fields describe proposal status at authorship; final independent outcomes are a separate review packet. No broader acceptance follows from extraction or author confidence.

Both catalogues already contain 127 values and 9/92 P0 values. This small batch covers the active unsaved-state, save failure/success, Save/Export/Share explanation, export-without-saving notice, two Save-and-share labels and Android chooser-failure consumers. Selection follows actual missing keys, terminology foundations and coherent testable behavior, not popularity or English identity.

All 254 inherited values/attributes remain unchanged, including Catalan `Save changes?`, Romanian `Salvaţi modificările?` and both `Image format` labels. Existing Save/Save-as/export commands are included verbatim for composition checks. The five no-current-consumer identities per locale stay absent; 73 other missing P0 entries per locale remain outside this batch. Existing NN/DA/NO holds, #56 never-merge, #113/#159, paired P1/frozen history, Help callback/archive identity and release pauses remain untouched.

Actual behavior matters: export/share can successfully write a file without clearing the current document's unsaved state or changing ordinary Save's destination. `ui_saved` confirms output writing, not a clean document. `ioFailed` appends a period and space to the translated prefix. The share failure refers to launching Android's chooser after a completed write. No Help/archive work is included.

Fresh validation checked all 1,370 source blobs, 323 context bindings, 26 exact consumer windows and the 322-file production reference inventory. The portable validator independently uses DOM parsing and Git blob hashes; full indexed/unindexed/nonargument token checking also applies to `formatted=false`. One positive packet and **39 refreshed-hash negative controls** pass ordinarily and under optimized Python, with byte-identical control receipts.

```sh
python3 verify_candidates.py --source-root PINNED_CHECKOUT --packet PACKET --out CHECKS
python3 test_verifier.py --source-root PINNED_CHECKOUT --packet PACKET --out CHECKS
python3 -O test_verifier.py --source-root PINNED_CHECKOUT --packet PACKET --out OPTIMIZED_CHECKS
```

These checks establish source/data integrity only. Final whole-value linguistic/source-static judgments, confidence and mixed-language qualifications must be read in the separate independent review receipts. No native-human, physical-device, runtime, layout or whole-language certification.
