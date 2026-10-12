# Independent sanitized-input verification

This compact selection records a separate artifact-only rerun against sanitized inputs. It is not exact original raw-log replay. The reviewed derivative selection is explicitly `6b0720bcf45c0619cb810f5974a9a875ae6a732012803d15e850e232d8621bc4`, as recorded in unchanged `SANITIZED-VERIFICATION.json` (SHA-256 `1c06e64d2fe9cb8f624449eed74839d9db8b7ee06f21860a6e8d70060a84cb07`).

All 95/API30 and 104/API35 methods, 167-locale discovery, source/protocol/terminal/JUnit, restart, natural-update, pixel and native geometry/input assertions pass unchanged. Expected differences are confined to sanitized API30 whole-log hashes, the downstream receipt hash, and explicit receipt-only prebuilt status. All 192 native PNGs and the Arabic records/images remain byte-identical.

`verify_sanitized_inputs.py` is the supporting recipe. It needs an exact source checkout, separately supplied preserved original review, sanitized derivative and verified extracted inputs; output must be fresh. It executes evidence checkers, never Android. It records only whole-file hashes, line numbers and changed report-field names. No header values or value hashes are included.

The frozen first report retains the originally reviewed 77-file derivative selection. A later script-validation run also passed; its only report difference was the then-local selection manifest identity after an unselected metadata amendment. It does not replace the first report or authorize that amendment.

The manifest excludes all extracted raw support, decoded PNGs and duplicate detailed native JSON. `NATIVE-RESULT-REFERENCE.json` pins the latter without duplication. Disclosure approval remains separate.
