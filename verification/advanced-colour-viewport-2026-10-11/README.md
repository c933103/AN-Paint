# Advanced Colour short-landscape corrective work

## Baseline replay, before production changes

Untouched application source is develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`,
complete tree `040a35f40a6e8e143c6a9b2121e804f0704dd5d1`. The first commit contains
only the installed test harness, host contracts, and this evidence record. No
application production file is changed.

The original positive method from `df214fee4f106c4365325412b4f9d3c8530232d5`
is retained byte-for-byte under its original class/method identity. Its original
fixture, font-transition sequence, native pointer helpers, timeouts and assertions
are retained. The two unrelated About/credit test methods are omitted from this
isolated replay. The current bounded app-owned export rule and the font helper
wrapper are carried over from PR49. A source digest is passed by the ordinary
runner. The existing API 35 app phase includes this additional method; API 30
explicitly suppresses it. All prior app methods remain required.

The only positive-test helper change observes dialog, native panels, holder,
editor, overflowing content and fixed-control bounds at the original viewport
wait boundary. It captures an image before the original method's finally block
can dismiss the dialog, on both success and timeout. Measured dimensions must
match the original API 35 640×320 landscape, density 1, en-US, font 1× configuration.
A timeout remains a failed test. There is no ignored test, longer wait, fallback
oracle or negative characterization substituted for acceptance.

Raw app-owned ZIP evidence is pulled in the EXIT collector after success or
failure, with an additional 15-second command and 3-second kill grace. Existing
36-minute device-step and 46-minute job ceilings still admit the source-bound
controlled path: maximum 2087s + 60s operational allowance = 2147s (< 2160s).
This arithmetic excludes universal filesystem/runtime guarantees. The API 35
composed suite cannot be green unless the unchanged positive case also passes.

Installed baseline result is pending. Source contracts alone do not prove the
native allocation, usability, pointer route, state preservation, or any repair.
The original failed run 38109511511 and its archived fixture remain failures.
Once this untouched-base replay is established, a separate production change
will keep the original positive acceptance requirements and add state/large-text
coverage as supported by actual results.
