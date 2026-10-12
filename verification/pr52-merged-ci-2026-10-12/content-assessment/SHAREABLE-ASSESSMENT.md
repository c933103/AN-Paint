# PR52 merged-head evidence: bounded content and provenance assessment

The exact selection passes the described checks. This is a bounded technical assessment, not publication permission or a universal secret-absence guarantee.

## Exact selection

- Main `DELIVERY-FILES.json` SHA-256: `ca659b5479112d522ae5a2da60ca7cd766ed2dbba1dd78cb8504154eb8e44a36`.
- All **162 selected files / 7,405,630 bytes**, plus their manifest, matched before and after the complete review.
- Installed subpacket manifest: `fc412a23c18da18aac6083710165b99da1bea0437f30300611cca51cd0687d6f`.
- Head `eb7451d320ba56e1ece6b1b55797da653966051d`, tree `b6bf7626c1d7c4aef669394970046ffc89a5c877`, run [38308218307](https://github.com/c933103/AN-Paint/actions/runs/38308218307).

## Exact prepared transport

Transport map `4055c0257e983fa06aabf3bdac4be121cec90196b93774e44268fb2e3a652cb4` contains **163 paths / 7,433,729 bytes**. Every entry matches the selected source bytes, SHA-256, Git blob ID and declared mode; the unchanged selection manifest is included. There are no additions, omissions, split parts or repackaging. This verifies local prepared transport, not remote publication.

## Findings

Recursive inspection covered **683 text leaves / 35,172,237 text bytes** and **658 PNGs**, including the 912 exact e19 members selected for current reuse. No flagged or unresolved explicit credential-pattern location, signed-URL pattern, URL-user-info hit, unknown binary leaf, archive parsing error, PNG text/EXIF metadata or PNG integrity error was identified. Archive comments/extra fields and TAR owner/PAX metadata were checked within the documented procedure.

All **52 current raw support members** match current CI bytes exactly. The additional derived native report is separately labeled and hash-bound, not represented as primary CI. Current evidence contains **API35 only**, no current API30 raw inputs, and no redactions. Historical API30 evidence keeps its original run attribution outside this fresh raw selection.

All **1,023 regression members** match fresh primary CI: 111 fresh delta members and 912 exact hash-reused e19 members. All 1,094 source leaves/modes match the explicit target tree; seven relevant synthetic-fixture source files are unchanged from e19. The unrelated local checkout HEAD is not used as current source identity.

The packet retains public commit-provenance contact fields, public upstream software-author contact notices, and emulator/runtime/network metadata. It is not described as devoid of personal-shaped or operational information. Two representative current native UI frames were manually viewed; they show localized editor/Save UI with the source-defined synthetic canvas fixture. No full-image OCR or hidden-payload analysis is claimed.

Ten scanner-only controls passed. The reproducible procedure reads inputs without changing them and emits values-suppressed results. Remote receipt authenticity remains coordinator-supplied and locally consistency-checked. No application edits, new Android execution, GitHub writes, publication or permissions decision occurred.
