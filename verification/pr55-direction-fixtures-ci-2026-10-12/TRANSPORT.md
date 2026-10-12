# Lossless current-run replay transport

Run `python3 reconstruct_replay.py` before the frozen README replay commands. Four ordered parts reconstruct the unchanged 19,349,383-byte regression ZIP. The script verifies the original frozen delivery manifest, each part and the final ZIP hash, and refuses to replace differing existing bytes.

The bounded verdict previously published at bdcc73c5 remains unchanged. The full source-bound replay bundle is added separately from application code; no APK or full source ZIP is duplicated. This acceptance applies to head6d603af9/run38290638790 only, not any develop reconciliation.
