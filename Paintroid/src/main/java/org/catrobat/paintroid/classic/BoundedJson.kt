/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import java.io.ByteArrayOutputStream
import java.io.InputStream

/** Bound the actual uncompressed input as well as checking the ZIP directory's size. */
internal object BoundedJson {
    fun read(input: InputStream, limit: Int): String {
        val output=ByteArrayOutputStream()
        val buffer=ByteArray(8192)
        while(true) {
            val count=input.read(buffer)
            if(count<0) break
            require(count<=limit-output.size()) { ui(org.catrobat.paintroid.R.string.ui_invalid_autosave_metadata) }
            output.write(buffer,0,count)
        }
        return output.toString(Charsets.UTF_8.name())
    }
}
