/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.database.DataSetObserver
import android.graphics.Typeface
import android.view.View
import android.view.ViewGroup
import android.view.ViewTreeObserver
import android.widget.TextView
import android.widget.Spinner
import android.widget.SpinnerAdapter
import android.widget.BaseAdapter
import android.widget.ListAdapter
import java.util.Locale

/** Bundled coverage is independent of device fallback fonts and text direction. */
internal object LocaleTypography {
    private val faces=mutableMapOf<String,Typeface>()
    fun asset(locale: Locale=Locale.getDefault()): String? = when {
        locale.script=="Mong" -> "fonts/notosansmongolian.ttf"
        locale.language=="vi" && locale.script=="Hani" -> "fonts/anpaintnomui.ttf"
        locale.language=="wuu" && locale.script=="Hans" -> "fonts/anpaintwuufallback.ttf"
        else -> null
    }
    fun typeface(context: Context,locale: Locale=Locale.getDefault()): Typeface? {
        val asset=asset(locale) ?: return null
        return faces.getOrPut(asset) {Typeface.createFromAsset(context.assets,asset)}
    }
    /** Spinner popups are separate windows, outside the Activity's view tree. */
    private class TypefaceChoices(private val source: SpinnerAdapter,private val font: Typeface): BaseAdapter() {
        override fun getCount()=source.count
        override fun getItem(position: Int)=source.getItem(position)
        override fun getItemId(position: Int)=source.getItemId(position)
        override fun getItemViewType(position: Int)=source.getItemViewType(position)
        override fun getViewTypeCount()=source.viewTypeCount
        override fun hasStableIds()=source.hasStableIds()
        override fun isEmpty()=source.isEmpty
        override fun areAllItemsEnabled()=(source as? ListAdapter)?.areAllItemsEnabled() ?: true
        override fun isEnabled(position: Int)=(source as? ListAdapter)?.isEnabled(position) ?: true
        override fun registerDataSetObserver(observer: DataSetObserver)=source.registerDataSetObserver(observer)
        override fun unregisterDataSetObserver(observer: DataSetObserver)=source.unregisterDataSetObserver(observer)
        override fun getView(position: Int,convertView: View?,parent: ViewGroup): View =
            source.getView(position,convertView,parent).also {apply(it,font)}
        override fun getDropDownView(position: Int,convertView: View?,parent: ViewGroup): View =
            source.getDropDownView(position,convertView,parent).also {apply(it,font)}
    }
    private fun apply(view: View,font: Typeface) {
        // Explicit font previews must continue to show their own selected face.
        val tag=view.tag as? String
        if(view is TextView && tag!="text_content" && tag?.startsWith("font_option_")!=true) {
            val styled=Typeface.create(font,view.typeface?.style ?: Typeface.NORMAL)
            if(view.typeface!==styled) view.typeface=styled
        }
        if(view is Spinner) view.adapter?.takeIf {it !is TypefaceChoices}?.let {source ->
            val selected=view.selectedItemPosition
            view.adapter=TypefaceChoices(source,font)
            if(selected>=0) view.setSelection(selected)
        }
        if(view is ViewGroup) for(i in 0 until view.childCount) apply(view.getChildAt(i),font)
    }
    /** Also cover controls added later by format changes, lists, or expanded sections. */
    fun install(root: View) {
        val font=typeface(root.context) ?: return
        apply(root,font)
        val listener=ViewTreeObserver.OnGlobalLayoutListener {apply(root,font)}
        root.viewTreeObserver.addOnGlobalLayoutListener(listener)
        root.addOnAttachStateChangeListener(object: View.OnAttachStateChangeListener {
            override fun onViewAttachedToWindow(view: View)=Unit
            override fun onViewDetachedFromWindow(view: View) {
                if(view.viewTreeObserver.isAlive) view.viewTreeObserver.removeOnGlobalLayoutListener(listener)
                view.removeOnAttachStateChangeListener(this)
            }
        })
    }
}
