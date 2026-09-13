/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Color

/** Shared by the Color tab and every selector; retains earlier saved palettes. */
internal class CustomColours(context: Context) {
    private val prefs=context.getSharedPreferences("classic-custom-colours",Context.MODE_PRIVATE)
    private val defaults=listOf(0xff5b67ff.toInt(),0xffffd700.toInt(),0xffc0c0c0.toInt(),0xffb87333.toInt())
    fun has(index: Int)=!prefs.getBoolean("removed_$index",false) && (index<defaults.size || prefs.contains("colour_$index"))
    fun colour(index: Int)=prefs.getInt("colour_$index",defaults.getOrNull(index) ?: Color.WHITE) or Color.BLACK
    fun entries()=(0 until 16).filter {has(it)}.map {it to colour(it)}
    fun add(colour: Int): Boolean {
        if(entries().any {it.second==colour}) return true
        val index=(0 until 16).firstOrNull {!has(it)} ?: return false
        replace(index,colour);return true
    }
    fun replace(index: Int,colour: Int) {require(index in 0..15);prefs.edit().putInt("colour_$index",colour or Color.BLACK).remove("removed_$index").remove("next").apply()}
    fun remove(index: Int) {require(index in 0..15);prefs.edit().remove("colour_$index").putBoolean("removed_$index",true).apply()}
}
