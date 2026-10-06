/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

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
import java.util.Locale

/** API21 binding checks. Glyph rasterization still requires an API21 device/emulator. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[21])
class LocaleTypographyApi21Test {
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
            val toastView=LocaleTypography.toast(context,"𪮻 𡳒",Toast.LENGTH_LONG).view!!
            assertEquals(face,toastView.findViewById<TextView>(android.R.id.message).typeface)
            val fonts=FontCatalog(context)
            assertFalse(fonts.fonts.any {it.id=="anpaintnomui"})
            val lato=fonts.fonts.indexOfFirst {it.id=="lato"}
            assertTrue(lato>0)
            assertEquals(fonts.face(lato),fonts.faceForText(lato,"𡨸喃"))
        } finally {Locale.setDefault(previous)}
    }
}
