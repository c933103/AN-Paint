# Swedish extension validation

Current application composition uses develop
`d7436b3df842b9be9aa12be622ebc88ed8e8e2b9`, preserving all upstream English Help
and release-note changes. All 1,222 unmodified tracked blobs were compared with
that complete current remote tree; content matched. Publication uses the
original remote executable modes, not modes lost by a downloaded source archive.

Current source-rebound checkout:
- `python3 tools/translation_catalogues.py`: passed structural validation.
- `python3 -m unittest discover -s tools -p 'test_swedish*wording.py'`: 22 passed.
- `python3 -m unittest discover -s tools -p 'test_*.py'`: 1,055 passed in 218.460 seconds.
- `python3 -O -m unittest discover -s tools -p 'test_*.py'`: 1,055 passed in 215.997 seconds.
- `verify_current_source_rebind.py`: all 717 complete current English identities,
  values and attributes; all 714 bounded Swedish values/attributes; named holds.

Pre-rebind checkout, still useful but not claimed as the current run:
- Broad wording family: 223 passed; current-localization contracts: 14 passed.
- Full normal host suite: 1,037 passed in 221.962 seconds.
- Full optimized host suite: 1,037 passed in 218.403 seconds.
- Original independent structural verifier passed separately from linguistic review.

Local Gradle could not start its tests because the distribution download returned
`java.net.SocketException: Network is unreachable`. No local JVM, lint, APK or
installed-device checks are claimed. Hosted CI remains required.

An earlier full host run exposed old Swedish-fallback oracles. Those were updated
only for independently reviewed Swedish family entries, then both full suites
passed. The global 59-locale baseline was not changed. Final normal and earlier
optimized logs, focused current checks and the Gradle failure accompany this
receipt. The current optimized run also completed successfully, as recorded above
and in `host-current-optimized.log`.
