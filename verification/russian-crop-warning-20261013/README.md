# Russian crop warning: local evidence, 13 October 2026

Source: https://github.com/c933103/AN-Paint/pull/62
Tested source head: 21f659e2c0a23e10273cdb13efdcf642375eac1f
Base: 6a77442847e385742ab274b059cb4d022c364e08

This evidence ref preserves the initial independent review, its identity manifest,
and local validation logs. It is not intended to be merged into the app branch.
The review describes the pre-fix source; its proposed warning was then implemented.
Corrected-source independent bounded acceptance is recorded at:
https://github.com/c933103/AN-Paint/pull/62#issuecomment-6138662274

Commands and observed results:
- python3 -m unittest discover -s tools -p 'test_*.py' -v: 672 tests, OK, exit 0
- python3 -O -m unittest discover -s tools -p 'test_*.py': 672 tests, OK, exit 0
- python3 tools/translation_catalogues.py: structurally valid, exit 0
- python3 -m unittest discover -s tools -p 'test_translations.py' -v: 32 tests, OK
- python3 -m unittest discover -s tools -p 'test_russian_crop_warning.py' -v: 2 tests, OK
- python3 tools/translation_catalogues.py --complete: exit 1, known outside-scope
  incompleteness; this is NOT a whole-catalogue completion claim.
- Eight negative controls separately restored the old warning and changed count
  format type to %3$s in each of one/few/many/other. All eight were rejected by
  the narrow tests without modifying the tested source on disk.

The aggregate logs contain intentional failing/timeout fixture output from negative
controls. Their unittest summary and exit status are the aggregate result.
Android SDK and Gradle distribution were absent locally; JVM, Android compilation,
lint, native and device checks were not run here. Hosted results are separate:
https://github.com/c933103/AN-Paint/actions/runs/38349567326
At archive creation, that run and exact-head Codex review were still in progress.

No native-speaker certification, whole-language acceptance, installed-layout
acceptance, or release acceptance follows from this evidence.
