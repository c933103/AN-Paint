/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.graphics.Typeface
import android.widget.ArrayAdapter
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import org.catrobat.paintroid.classic.FontCatalog
import org.catrobat.paintroid.classic.LocaleTypography
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.Implementation
import org.robolectric.annotation.Implements
import org.robolectric.shadows.ShadowToast
import java.util.Locale

/** API21 binding checks with a view-backed Toast shadow, not device glyph rasterization. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[21],shadows=[Api21ViewBackedToast::class])
class LocaleTypographyApi21Test {
    @Test fun tooltipSetterDoesNotLinkApi26MethodsOrChangeApi21Interactions() {
        val previous=Locale.getDefault()
        try {
            Locale.setDefault(Locale.forLanguageTag("vi-Hani"))
            val view=android.view.View(RuntimeEnvironment.getApplication()).apply {contentDescription="original"}
            var clicks=0
            view.setOnLongClickListener {clicks++;true}
            for(text in listOf("𡨸喃",null,"")) org.catrobat.paintroid.classic.LocaleTooltip.set(view,text)
            assertEquals("original",view.contentDescription)
            assertTrue(view.performLongClick());assertEquals(1,clicks)
        } finally {Locale.setDefault(previous)}
    }

    @Test fun nomFaceReachesApi21ControlsAndToastWithoutReplacingDrawingChoices() {
        val previous=Locale.getDefault()
        try {
            Locale.setDefault(Locale.forLanguageTag("vi-Hani"))
            val context=RuntimeEnvironment.getApplication()
            // The API21 legacy shadow compares font family/style, not object identity.
            val face=Typeface.createFromAsset(context.assets,"fonts/anpaintnomui.ttf")
            val root=LinearLayout(context)
            val label=TextView(context).apply {text="𮞶"}
            val explicit=EditText(context).apply {tag="text_content";typeface=Typeface.MONOSPACE}
            val preview=TextView(context).apply {tag="font_option_monospace";typeface=Typeface.MONOSPACE}
            listOf(label,explicit,preview).forEach {root.addView(it)}
            LocaleTypography.install(root)
            assertEquals(face,label.typeface)
            assertSame(Typeface.MONOSPACE,explicit.typeface)
            assertSame(Typeface.MONOSPACE,preview.typeface)
            val spinner=Spinner(context).apply {
                adapter=ArrayAdapter(context,android.R.layout.simple_spinner_dropdown_item,listOf("𡨸","𮞶"))
                setSelection(1)
            }
            root.addView(spinner)
            root.viewTreeObserver.dispatchOnGlobalLayout()
            assertEquals(1,spinner.selectedItemPosition)
            val row=spinner.adapter.getDropDownView(1,null,root) as TextView
            assertEquals(face,row.typeface)
            @Suppress("DEPRECATION")
            val plainMessage=Toast.makeText(context,"plain",Toast.LENGTH_LONG).view!!.findViewById<TextView>(android.R.id.message)
            assertFalse(face==plainMessage.typeface)
            val toast=LocaleTypography.toast(context,"𪮻 𡳒",Toast.LENGTH_LONG)
            assertEquals(Toast.LENGTH_LONG,toast.duration)
            @Suppress("DEPRECATION")
            val toastMessage=toast.view!!.findViewById<TextView>(android.R.id.message)
            assertEquals("𪮻 𡳒",toastMessage.text.toString())
            assertEquals(face,toastMessage.typeface)
            val fonts=FontCatalog(context)
            assertFalse(fonts.fonts.any {it.id=="anpaintnomui"})
            val lato=fonts.fonts.indexOfFirst {it.id=="lato"}
            assertTrue(lato>0)
            assertEquals(fonts.face(lato),fonts.faceForText(lato,"𡨸喃"))
        } finally {Locale.setDefault(previous)}
    }
}

/** Robolectric 4.14.1's default Toast shadow omits the view created by API21 Android.
 * Supply an unstyled message view so the real app wrapper must install its typeface.
 * This intentionally does not model framework toast inflation or native rendering.
 */
@Implements(Toast::class)
class Api21ViewBackedToast : ShadowToast() {
    companion object {
        @JvmStatic
        @Implementation(methodName="makeText")
        @Suppress("DEPRECATION")
        fun makeTextWithView(context: Context,text: CharSequence,duration: Int): Toast =
            Toast(context).apply {
                this.duration=duration
                view=TextView(context).apply {id=android.R.id.message;this.text=text}
            }
    }
}
