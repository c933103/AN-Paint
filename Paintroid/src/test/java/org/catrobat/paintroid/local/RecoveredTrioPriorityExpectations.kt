/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

/** Remaining bounded test support; current catalogue wording is not mirrored here. */
internal object RecoveredTrioPriorityExpectations {
    fun compiledDisplay(tag: String,key: String,raw: String): String {
        val inherited = when(tag to key) {
            "sq" to "ui_new_image" -> "Imazh i ri " to "Imazh i ri"
            "sq" to "ui_watercolor" -> "Akuarel " to "Akuarel"
            else -> null
        }
        if(inherited!=null) {
            require(raw==inherited.first) {"$tag/$key inherited raw whitespace binding differs"}
            return inherited.second
        }
        return Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
            when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
        }
    }
}
