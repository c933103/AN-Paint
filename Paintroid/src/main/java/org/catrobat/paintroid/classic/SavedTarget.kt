/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.net.Uri
import org.json.JSONObject

/** Only a successful Save as establishes the destination of subsequent Save commands. */
internal data class SavedTarget(val uri: Uri, val name: String, val options: ExportOptions) {
    fun json() = JSONObject().apply {
        put("uri",uri.toString());put("name",name);put("format",options.format.name)
        put("quality",options.quality);put("lossless",options.lossless);put("tiff_compressed",options.tiffCompressed);put("dither",options.dither)
    }
    companion object {
        fun read(value: JSONObject?): SavedTarget? {
            if(value==null) return null
            val uri=Uri.parse(value.optString("uri"))
            val format=ImageFormat.values().firstOrNull {it.name==value.optString("format")} ?: return null
            val lossless=value.optBoolean("lossless",true)
            if(uri.scheme!="content" || format.isDerivedExport) return null
            return SavedTarget(uri,value.optString("name"),ExportOptions(format,value.optInt("quality",95),lossless,
                dither=value.optBoolean("dither",true),tiffCompressed=value.optBoolean("tiff_compressed",true)))
        }
    }
}
