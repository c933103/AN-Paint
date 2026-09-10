/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Color

/** Four distinct recent choices, newest first. Merely rebuilding the UI adds nothing. */
class RecentColours(context: Context) {
    private val prefs=context.getSharedPreferences("recent-colours",Context.MODE_PRIVATE)
    val colours: List<Int> get()=(0 until prefs.getInt("count",0).coerceIn(0,4)).map { prefs.getInt("colour_$it",Color.BLACK) or Color.BLACK }
    fun add(colour: Int) {
        val opaque=colour or Color.BLACK
        val next=(listOf(opaque)+colours.filter { it!=opaque }).take(4)
        prefs.edit().apply { putInt("count",next.size);next.forEachIndexed { i,c -> putInt("colour_$i",c) } }.apply()
    }
}
