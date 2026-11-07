/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import androidx.annotation.StringRes

/** Hold message meaning through worker/lifecycle changes; resolve only when displayed. */
internal sealed class UiMessage {
    data class Resource(@StringRes val id: Int,val arguments: List<Any?>=emptyList()): UiMessage()
    /** External text is data and must never be translated or treated as a format string. */
    data class Literal(val value: String): UiMessage()
    fun text(): String = when(this) {
        is Resource -> ui(id,*arguments.map {if(it is UiMessage) it.text() else it}.toTypedArray())
        is Literal -> value
    }
}
