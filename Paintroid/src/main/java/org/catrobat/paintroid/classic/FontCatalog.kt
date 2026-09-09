/* AN Paint additions, 2026-09-07. GNU AGPL-3.0-or-later. Font files keep their separate OFL licences. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.graphics.Typeface
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView
import org.json.JSONArray

data class FontChoice(val id: String,val name: String,val asset: String?=null,val family: String="sans-serif")

class FontCatalog(private val context: Context) {
    val fonts: List<FontChoice>
    private val faces=mutableMapOf<String,Typeface>()
    init {
        val system=listOf("Sans serif" to "sans-serif","Serif" to "serif","Monospace" to "monospace",
            "Sans light" to "sans-serif-light","Sans thin" to "sans-serif-thin","Sans condensed" to "sans-serif-condensed",
            "Sans medium" to "sans-serif-medium","Cursive" to "cursive","Casual" to "casual")
        val list=context.assets.open("fonts/inventory.json").bufferedReader().use { JSONArray(it.readText()) }
        fonts=system.map { FontChoice("system_"+it.second,it.first,family=it.second) } + (0 until list.length()).map {
            val row=list.getJSONObject(it);FontChoice(row.getString("id"),row.getString("name"),row.getString("asset"))
        }
    }
    fun face(index: Int,style: Int=Typeface.NORMAL): Typeface {
        val item=fonts[index.coerceIn(fonts.indices)]
        val base=faces.getOrPut(item.id) { item.asset?.let { Typeface.createFromAsset(context.assets,it) } ?: Typeface.create(item.family,Typeface.NORMAL) }
        return if (style==Typeface.NORMAL) base else Typeface.create(base,style)
    }
    fun adapter() = object : ArrayAdapter<FontChoice>(context,android.R.layout.simple_spinner_dropdown_item,fonts) {
        private fun render(view: View,position: Int): View = (view as TextView).apply {
            text=fonts[position].name;typeface=face(position);textSize=18f;tag="font_option_${fonts[position].id}"
            minHeight=(48*context.resources.displayMetrics.density).toInt()
        }
        override fun getView(position: Int,convertView: View?,parent: ViewGroup): View = render(super.getView(position,convertView,parent),position)
        override fun getDropDownView(position: Int,convertView: View?,parent: ViewGroup): View = render(super.getDropDownView(position,convertView,parent),position)
    }
}
