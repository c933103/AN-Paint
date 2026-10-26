# PR174: verified development artifact, required gates still running

Snapshot: 26 October 2026, 06:29:11 UTC. [PR174](https://github.com/c933103/AN-Paint/pull/174), head `3c8123707106dfc991221517e443276f857797db`; [run 40279026132](https://github.com/c933103/AN-Paint/actions/runs/40279026132).

**Build and exact-script jobs passed.** Code review is clean for the exact head; optional Security also completed without findings. JVM/lint and actual API35 jobs remain incomplete in this record, so **merge eligibility is not claimed**. Hosted Python step passed but its counts/skips await the terminal regression artifact; they are not copied from local results. No local Android compilation was executed.

## Exact artifact/source proof

- Artifact 12631542641 archive SHA-256: `d194c6958339da5b8cae73edc3cf0ac8e67a8ac6159ec088a5362b61ac8115bf`.
- APK SHA-256: `2c1dce8ab833c2c90b52fb7c4e0126b5bf8c7b3190a10f48f26537683040552e`.
- Source ZIP SHA-256: `b4ee706a524ed55902b2829cdf2fd66887cc33df908bd4a76e481de49b4fea33`.
- Build-info identifies test merge `ccf60becbb36d17849b907c49bad7d23c17f02cf`. Its verified parents are base 857a201 and head 3c81237; its tree equals reviewed tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251`.
- All 1,364 packaged tracked files match the exact 1,367-file source tree; the three normal dotfile exclusions are explicit. Embedded and external source ZIPs are byte-identical.
- All 72 newly reviewed plus eight previously reviewed compiled `(nn)` values match their complete approved display strings. This is resource-compilation proof, not installed layout or native-language certification.
- APK v1/v2 verification passed. Certificate SHA-256: `0dc8a877bd1ef8ba498423e72e0e1215335e3b195b60a6ecefa6a947337369e4`. It is the CI debug identity, **not private upgrade/release signing**.
- Exact-script artifact 12631161935 passed all 13 expected probes; every log digest and expected exit was independently checked. Its deliberate rejection probe is not hidden as an unexplained failure.

`verify_apk_artifact.py` reproduces archive/build-info/source/compiled-value/signature checks against a pinned source checkout, its Git tree JSON, the downloaded artifact ZIP and Android `aapt2`/`apksigner.jar` tools. It fails on missing or malformed data rather than inferring success. Detailed inputs and tool digests are in the JSON receipts.

All prior scopes and holds remain unchanged. No release. Later terminal results must remain distinct from this pending snapshot.
