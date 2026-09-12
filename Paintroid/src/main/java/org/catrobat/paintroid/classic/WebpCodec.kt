/* AN Paint, 2026-09-12. GNU AGPL-3.0-or-later.
 * libwebp: Google and contributors, BSD-3-Clause; see WEBP_NOTICES.txt.
 */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import java.io.File

/** Opaque still-image export with consistent lossless behaviour on Android 5+. */
object WebpCodec {
    private object Native {
        init { System.loadLibrary("anpaint_webp") }
        external fun encode(image: Bitmap, path: String, quality: Int, lossless: Boolean, budget: Long)
    }

    /**
     * The budget includes the source bitmap and native encoding allocations.
     * A failed encode leaves an existing destination file and the bitmap intact.
     * Lossless always preserves RGB exactly; quality controls lossy output only.
     */
    fun encode(image: Bitmap, file: File, quality: Int, lossless: Boolean, budget: Long) {
        Native.encode(image, file.path, quality.coerceIn(1, 100), lossless, budget)
    }
}
