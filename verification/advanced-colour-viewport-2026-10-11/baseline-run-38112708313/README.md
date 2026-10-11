# Untouched-base installed reproduction

The original positive Advanced Colour method failed on untouched application
source in [run 38112708313](https://github.com/c933103/AN-Paint/actions/runs/38112708313).
All 487 tracked application production files in the matching source ZIP were
read back and matched the original production snapshot byte-for-byte. The APK,
source ZIP, outer artifact and nested evidence export hashes were verified.

At API 35, 640 × 320 landscape, density 1, en-US and font scale 1×, the native
custom holder is 384 × 138, but the editor viewport is 360 × 0 with 470px content.
The native title is 46px and action area 56px. The Add button is 48px tall with
only 25px visible. This is a reproduced baseline defect, not a usability pass.
The original assertion is the only failed completed test; 97 other methods pass.
The two restart methods are correctly not run by the existing failure gate.
Build, JVM/regression, lint and resource-generation jobs passed.

The focused archive preserves the raw app-owned ZIP, its entire receipt/manifest
and all three actual images, original emulator job log, all completed suite
reports, build identity and the complete production-source comparison. Concatenate
the numbered parts in order and verify the SHA-256 in source-binding.json before
opening the ZIP. APK/source binaries remain referenced by their exact verified
hashes and original Actions artifact; they are not duplicated in repository history.
The Actions artifacts have their original retention limits.
