/* AN Paint, 2026. GNU AGPL-3.0-or-later. Run on the API35 emulator stage. */
package org.catrobat.paintroid.classic

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Gainmap
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SdkSuppress
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import kotlin.math.abs

@RunWith(AndroidJUnit4::class)
@SdkSuppress(minSdkVersion=34)
class UltraHdrImportTest {
    @Test fun ultraHdrJpegUsesAuthoredSdrBaseAndRemovesStaleGainmap() {
        val context=InstrumentationRegistry.getInstrumentation().targetContext
        val source=Bitmap.createBitmap(64,32,Bitmap.Config.ARGB_8888)
        val map=Bitmap.createBitmap(16,8,Bitmap.Config.ARGB_8888)
        val file=File.createTempFile("ultrahdr-",".jpg",context.cacheDir)
        try {
            source.eraseColor(Color.rgb(80,140,190));map.eraseColor(Color.WHITE)
            source.setGainmap(Gainmap(map).apply {
                setRatioMin(1f,1f,1f);setRatioMax(4f,4f,4f);setGamma(1f,1f,1f)
                setMinDisplayRatioForHdrTransition(1f);setDisplayRatioForFullHdr(4f)
            })
            file.outputStream().use { assertTrue(source.compress(Bitmap.CompressFormat.JPEG,100,it)) }
            val independent=BitmapFactory.decodeFile(file.path)
            try { assertTrue("The fixture must contain an actual encoded gain map",independent.hasGainmap()) }
            finally { independent.recycle() }
            val imported=ImportedImage(file,"Ultra HDR JPEG")
            val result=imported.decode(ImportPlan.create(imported.dimensions,imported.dimensions),128L*1024*1024)
            try {
                assertEquals(Bitmap.Config.ARGB_8888,result.config);assertTrue(result.colorSpace!!.isSrgb)
                assertFalse(result.hasGainmap())
                val pixel=result.getPixel(32,16)
                assertTrue(abs(Color.red(pixel)-80)<=3);assertTrue(abs(Color.green(pixel)-140)<=3);assertTrue(abs(Color.blue(pixel)-190)<=3)
            } finally { result.recycle() }
        } finally { source.recycle();map.recycle();file.delete() }
    }
}
