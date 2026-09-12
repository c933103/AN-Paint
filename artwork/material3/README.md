# Material Design 3 colour data

AN Paint uses the baseline light roles from Material Components for Android,
revision `d12048664f383e88148afb18e971aa6dd24ed42e` (retrieved 12 September 2026).
The original `tokens.xml` and Apache 2.0 `LICENSE` are preserved unchanged;
`inventory.json` records exact source URLs and SHA-256 hashes.

`Paintroid/src/main/res/values/material3_colours.xml` resolves the chosen light
role values into app resources. `EditorColours.kt` provides those same roles to
custom-drawn UI controls. Disabled foreground and ripple alpha use Material
state-opacity values. Document pixels, imported thumbnails and colour swatches
are outside the UI theme and retain their actual colours.

This changes the colour scheme. It does not claim that the existing platform
widgets or compact editor geometry implement all Material 3 component layouts.
There is no additional UI runtime dependency.

[Material Design 3 colour roles](https://m3.material.io/styles/color/roles) ·
[Original token file](https://github.com/material-components/material-components-android/blob/d12048664f383e88148afb18e971aa6dd24ed42e/lib/java/com/google/android/material/color/res/values/tokens.xml)
