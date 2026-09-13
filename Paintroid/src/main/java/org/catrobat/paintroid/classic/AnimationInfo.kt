/* AN Paint additions, 2026-09-13. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import java.io.File

/** An import warning: multiple frames, or an incomplete scan with frameCount below two.
 * APNG may have a separate default poster image. */
data class AnimationInfo(
    val format: String,
    val frameCount: Int,
    val frameCountExact: Boolean,
    val pngDefaultImageSeparate: Boolean
) {
    companion object {
        /** Best-effort bounded metadata scan; null also covers malformed/unknown containers. */
        fun inspect(file: File): AnimationInfo? = AnimationMetadata.inspect(file)?.let {
            AnimationInfo(it.format, it.frameCount, it.frameCountExact, it.pngDefaultImageSeparate)
        }
    }
}
