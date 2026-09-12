/* AN Paint test infrastructure, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Bitmap
import android.os.Build
import org.catrobat.paintroid.classic.PlatformImageColour
import org.junit.Assert.assertTrue
import java.io.File

/** Geometry/picker tests use ordinary unprofiled sRGB images. Robolectric's
 * encoder writes a redundant sRGB ICC profile into JPEGs, but this host JVM
 * cannot load Android JNI colour converters. Remove that metadata without
 * changing JPEG pixels; these source bitmaps are explicitly checked as sRGB.
 * Actual ICC transforms remain covered by Android PlatformColourImportTest.
 */
internal fun writeSrgbFixture(image: Bitmap,file: File,format: Bitmap.CompressFormat) {
    assertTrue("This helper only accepts sRGB source fixtures",Build.VERSION.SDK_INT<26 || image.colorSpace?.isSrgb==true)
    file.outputStream().use { assertTrue(image.compress(format,100,it)) }
    if(format==Bitmap.CompressFormat.JPEG) {
        PlatformImageColour.read(file).withDecodeFile(file) { unprofiled ->
            if(unprofiled!=file)unprofiled.copyTo(file,overwrite=true)
        }
    }
}
