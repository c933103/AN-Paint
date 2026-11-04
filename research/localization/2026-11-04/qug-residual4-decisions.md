# Review of four residual controls

Retain all four authored contextual proposals without value changes. The three ratio entries form one atomic terminology group. Main and left arrow remain held as instructed. This is an independent contextual review, not native Chimborazo certification.

## Same percentage is the correct operation

Scaling starting width W and height H by the same percentage p gives W*p/100 and H*p/100; their ratio remains W/H. The description does not assert that both resulting dimensions are equal or that pixel sizes are frozen. In pixel mode the same effect is obtained by multiplying the edited dimension by the original other/base ratio. The app need not switch to percentage-input mode for the description to be valid.

Verified DimensionControls.kt:61–73: when locked, percent mode copies the entered percentage to the other field; pixel mode uses n*otherBase/base and rounds the other dimension. This preserves the original ratio up to integer rounding. The label does not promise lossless exact arithmetic. Turning the lock on after independent edits can restore the original ratio rather than preserving the newly distorted one; nothing in the new label promises otherwise.

Verified SelectionGeometry.kt:36–41 and :56–58: corner and edge resizing apply one scale to both width and height when locked. The selection operation changes geometry, not the stored source pixels immediately. The label says dimensions change and does not claim source-pixel resampling.

## Language and quoted control

Pataktapash aksitapash identifies the two dimensions together, kikin marks the shared amount, and patsak pitiwan uses the existing percentage expression instrumentally. Tikrachina describes change rather than fixing dimensions. This is a transparent operational alternative to the previously unresolved tupunakuy noun; no further terminology hold is needed merely because the exact full phrase lacks dictionary attestation.

The help retains separate changes to width and height when unlocked and quotes the checkbox verbatim. Akllayta anchuchiy targets removal of the selection/check state in this checkbox context, not removing the control or deleting the image. Retain it. Do not shorten the quoted label independently of either checkbox.

## Italic

Retain Wiksuyachishka killka as an authored description of text made slanted. The derived-state wording plus explicit text noun and style-checkbox context makes the intended typographic effect clear enough for this batch; it is not a claim that this is the established regional technical word. Morphological expansion alone is not dictionary evidence: earlier wiksu/wistu evidence supports bent/crooked senses, not a separately attested italic term.

TextStyleDialog.kt:49 creates the italic checkbox; :69 includes Typeface.ITALIC independently of bold; :71 applies the resulting face; :106 stores the italic flag independently of underline and strike. Thus this is a typeface style, not glyph rotation, paragraph direction, broken text or canvas skew.

## Concrete layout risk, not a rendered failure

The proportional-selection checkbox in ClassicPaintActivity.kt:761–764 is fixed at 48dp height with 11sp text. The long new label can wrap, and large accessibility font settings may overflow. The italic checkbox in TextStyleDialog.kt:51–52 occupies half a row with fixed 48dp height, likewise needing wrap/large-font checks. DimensionControls uses natural checkbox height and the explanatory text is inside a scrolling dialog, so those have fewer fixed-height constraints. No actual Android/device/TalkBack layout was executed; do not claim either a visual pass or confirmed clipping.

## Independent validation

Parsed source/base/proposed XML and checked every proposed value, source attributes, placeholder and literal newline parity. All previous entries are unchanged. Ratio labels match exactly and the explanatory quotation is exact. Main and left arrow remain absent. All checks passed. No branch or original input file was edited.
