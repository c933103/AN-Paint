/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.util.Base64
import org.json.JSONObject
import java.util.Locale

/** Style only AN Paint's injected artwork actions; publisher content keeps its own styles. */
internal object GalleryTypography {
    private val dataFonts=mutableMapOf<String,String>()
    internal fun css(context: Context,locale: Locale=Locale.getDefault()): String {
        val asset=LocaleTypography.asset(locale)
        val font=asset?.let {path -> dataFonts.getOrPut(path) {
            "data:font/ttf;base64,"+context.assets.open(path).use {Base64.encodeToString(it.readBytes(),Base64.NO_WRAP)}
        }}
        val direction=when(VerticalText.uiDirection(locale)) {
            TextDirection.VERTICAL_LR -> "vertical-lr"
            TextDirection.VERTICAL_RL -> "vertical-rl"
            TextDirection.HORIZONTAL -> "horizontal-tb"
        }
        val face=if(font==null) "" else "@font-face{font-family:ANPaintAction;src:url(\"$font\") format(\"truetype\");font-style:normal;font-weight:400;}"
        val family=if(font==null) "sans-serif" else "ANPaintAction,sans-serif"
        return face+"[data-anpaint-action]{font-family:$family!important;-webkit-writing-mode:$direction!important;writing-mode:$direction!important;text-orientation:mixed;white-space:normal;line-height:1.35;}"
    }
    fun script(context: Context,locale: Locale=Locale.getDefault()): String = """
        (function(){
          var css=${JSONObject.quote(css(context,locale))};
          var style=document.getElementById('anpaint-action-typography');
          if(!style){style=document.createElement('style');style.id='anpaint-action-typography';(document.head||document.documentElement).appendChild(style);}
          if(style.textContent!==css)style.textContent=css;
        })();
    """.trimIndent()
}
