/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.net.Uri
import org.catrobat.paintroid.classic.*
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.json.JSONObject

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30])
class SavedImageSettingsTest {
    @Test fun reopeningRestoresEveryOrdinaryFormatAndItsCompressionSettings() {
        for(format in ImageFormat.values().filter {!it.isDerivedExport}) for(lossless in listOf(false,true)) {
            val options=ExportOptions(format,27,lossless,dither=false,tiffCompressed=false)
            val target=SavedTarget(Uri.parse("content://documents/image/42"),"Drawing${format.extension}",options)
            // Reparse serialized draft data, as after an application restart.
            assertEquals(target,SavedTarget.read(JSONObject(target.json().toString())))
        }
    }
    @Test fun derivedExportsCannotReplaceTheRememberedSaveDestination() {
        for(format in listOf(ImageFormat.ICO,ImageFormat.BASE64,ImageFormat.ASCII_ART)) {
            val target=SavedTarget(Uri.parse("content://documents/export/7"),"Export${format.extension}",ExportOptions(format))
            assertNull(SavedTarget.read(target.json()))
        }
    }
}
