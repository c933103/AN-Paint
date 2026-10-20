# Swedish remaining-P1 independent review

Repository source: c933103/AN-Paint, develop
0134e79c588a027bbd239f7685fff52b0771819f.

This evidence-only snapshot records all 149 previously missing exact Swedish P1
strings. The independent model-based review accepts 148 complete messages and
withholds `ui_foreground_background_colour_palette` because no current caller
establishes the meaning of `%3$s`. Of the accepted messages, 134 have production
call-site context and 14 have source-semantic review only. This is not native-
speaker, installed-layout, runtime or whole-language acceptance. Prior uncertainty,
including `ui_main23`, and withdrawn historical conclusions remain unchanged.

- `author-proposals.json`: complete English/Swedish proposals and source context;
  SHA-256 c115cd0f4d53fbeb4b28ac02ce3ec78a3306e1aadd5010499446fb4177b253f4.
- `independent-review.json`: per-entry final decisions and reasons;
  SHA-256 f770b0b99dcd911f66b15c96a5589c2bf9a6b5358db1c9327f19bf337b0d9b8d.
- `accepted-values.json`: exact 148 accepted values, including the revised
  “bilddata som Base64-text”.
- `structural-parity.json`: source/attributes/placeholders/newlines/Android/XML
  checks for all 149 proposals. Structural parity does not accept the held entry.

No application, runtime, CI, merge, deployment or release result is claimed here.
The integration PR must bind these exact accepted values to its source and report
its own local and hosted checks. This evidence ref is not an application branch.
