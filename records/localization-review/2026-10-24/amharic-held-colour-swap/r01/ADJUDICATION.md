# Amharic "Swap colors": independent adjudication

**Decision: READY as a reviewed translation candidate, unchanged.**

- Resource: `string/ui_swap23`
- English: **Swap colors**
- Amharic: **ቀለሞችን ያለዋውጡ**
- Scope: this label's translation readiness only. No production implementation or release acceptance.

## Why the evidence is sufficient

The [actual control](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L415-L424) exchanges the two current foreground/background values next to their swatches. It does not select arbitrary new colours, cycle a palette, invert pixels or perform the separately offered black/white reset.

The decisive lexical evidence is not a dictionary inference from a related stem. Android uses the exact command verb **ያለዋውጡ** with a plural object for [swapping left and right mouse-button roles](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml#4603), rendered as [የግራ እና የቀኝ አዝራሮችን ያለዋውጡ](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml#1984). That is reciprocal reassignment between two existing roles, not generic change. The colour operation has the same relevant relationship. This Android evidence is reused, not newly discovered and not a native-reader vote.

[LibreOffice's colour-control translation](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po#L8249-L8253) supplies **ቀለሞች**. Combining that noun with the object marker and the already-attested exchange verb is a justified productive construction. [Leslau's direct-object discussion](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=64) supports the marking; [his command discussion](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=193) supports respectful third-person-plural jussive orders. The respectful register is therefore defensible, although not compulsory. [Microsoft's singular-command preference](https://download.microsoft.com/download/6/2/a/62a993f1-d3b2-4f28-b3e7-22965eb91426/amh-eth-styleguide.pdf#page=40) is a different product convention, not a grammatical prohibition.

[The dictionary's related forms](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=12) have a broader change/variation/interchange range and do not attest this exact causative command. They neither independently prove the candidate nor establish a contrary colour-specific meaning. The judgment instead rests on the exact exchange-verb use, supported noun/object construction and matching two-role context. It does not assume that reduplication or causative morphology universally means "swap."

The Android label names its pair explicitly; this shorter source label relies on the two-colour control context. That difference does not establish a translation defect. The evidence is sufficient for the contextual exchange reading at candidate-review level. No exact whole-phrase corpus match is required, and none is claimed. No English source defect or evidence-backed replacement is established.

## Author dissent and remaining uncertainty

The proposal author recommends **HOLD unchanged** because the whole colour command has not received an independently validated naturalness/reader-interpretation assessment. That dissent remains recorded; this is not unanimous approval.

The adjudicator gives greater weight to the structurally matching, exact-verb role-exchange example and productive composition. The remaining uncertainty is whether proficient users find the complete displayed or spoken label natural, particularly when encountered without nearby control context. That is an untested usability/idiom question, not evidence of a specific wrong sense requiring continued translation HOLD. Confidence in complete contextual idiom is **medium**, not native-speaker certification.

No fluent-human assessment, app rendering, isolated spoken-label comprehension, TalkBack pronunciation, build, CI or runtime validation was performed. Those results remain unclaimed. No production text, existing review record or other candidate was changed by this adjudication.
