/* AN Paint additions, 2026-09-13. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.graphics.Color
import android.util.Base64
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File

/** The warning must describe the image that the real Android static decoder imports. */
@RunWith(AndroidJUnit4::class)
class AnimationImportTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext
    private val assets get() = InstrumentationRegistry.getInstrumentation().context.assets

    private fun checkImport(name: String, format: String, poster: Boolean, firstPixel: Int) {
        val file = File.createTempFile("animated-import-", ".unknown", context.cacheDir)
        try {
            val encoded = assets.open("animation-fixtures/$name.b64").bufferedReader().use { it.readText() }
            file.writeBytes(Base64.decode(encoded, Base64.DEFAULT))
            val info = checkNotNull(AnimationInfo.inspect(file))
            assertEquals(format, info.format)
            assertEquals(3, info.frameCount)
            assertTrue(info.frameCountExact)
            assertEquals(poster, info.pngDefaultImageSeparate)
            val source = ImportedImage(file, name)
            assertEquals(ImageDimensions(1, 1), source.dimensions)
            val bitmap = source.decode(ImportPlan.create(source.dimensions, source.dimensions), 64L * 1024 * 1024)
            try { assertEquals(firstPixel, bitmap.getPixel(0, 0)) }
            finally { bitmap.recycle() }
        } finally { file.delete() }
    }

    @Test fun gifImportsTheFirstFrame() = checkImport("three-frame.gif", "GIF", false, Color.BLACK)
    @Test fun webpImportsTheFirstFrame() = checkImport("three-frame.webp", "WebP", false, Color.RED)
    @Test fun apngImportsTheFirstFrameWhenItIsTheDefaultImage() = checkImport("three-frame.png", "APNG", false, Color.RED)
    @Test fun apngImportsItsSeparateDefaultPoster() = checkImport("three-frame-poster.png", "APNG", true, Color.GREEN)
}
