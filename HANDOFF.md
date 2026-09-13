# AN Paint 0.0.26

Package `paint.anpaint.android`; version code `79`.

This update adds visible empty saved-palette slots, Add colour and a direct
Advanced editor beside Black / white; top/left pixel rulers; live cursor x/y;
View before Draw, with Navigate first in View; anti-aliasing off by default;
and the revised regional/name-only language choices. See
[the change details](verification/UI_0.0.26.md) and
[language catalogue notes](translations/README.md).

The classic panel icons, centered captions, compact first-row shortcuts,
filename subtitle, vertical landscape ribbon, and dedicated vertical-script
layouts remain. All earlier format support, page selection, animation warnings,
Save/export behavior, gallery credits and Japanese flip corrections remain.

## Verification and delivery

The source is prepared for the universal development build and independent
regression/lint and API 35 emulator checks. This source snapshot does not claim
that an asynchronous build has passed. The final signed APK handoff and CI link
are recorded in `verification/HANDOFF_0.0.26.md` after packaging.

Installable updates must use the existing certificate:
`f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`.
The private backup includes the signing key and must never be published to GitHub.

## Previous task completed

The complete [0.0.25 workflow](https://github.com/c933103/AN-Paint/actions/runs/34767059225)
has now passed, including the API 35 emulator job that was pending at packaging.
The universal build, all 240 regression tests and lint had already passed.
The original [0.0.25 handoff](verification/HANDOFF_0.0.25.md) retains the accurate
packaging-time snapshot and now includes this later completion update.
