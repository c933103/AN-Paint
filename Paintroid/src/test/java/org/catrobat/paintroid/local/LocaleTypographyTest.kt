/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.graphics.Paint
import android.graphics.Typeface
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Spinner
import android.widget.ArrayAdapter
import org.catrobat.paintroid.classic.LocaleTypography
import org.catrobat.paintroid.classic.VerticalText
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class LocaleTypographyTest {
    @Test fun nomFontReachesNativeControlsButPreservesExplicitTextFonts() {
        val context=RuntimeEnvironment.getApplication()
        val old=Locale.getDefault()
        try {
            Locale.setDefault(Locale.forLanguageTag("vi-Hani"))
            val font=LocaleTypography.typeface(context)!!
            val paint=Paint().apply {typeface=font;textSize=32f}
            for(text in listOf("𡨸","𥻂","𦻳","𮞶")) assertTrue(text,paint.hasGlyph(text))
            val root=LinearLayout(context)
            val label=TextView(context).apply {text="𡨸喃"}
            val field=EditText(context).apply {text.append("𡨸");tag="ordinary_field"}
            val bold=TextView(context).apply {typeface=Typeface.DEFAULT_BOLD}
            root.addView(bold)
            val explicit=EditText(context).apply {tag="text_content";typeface=Typeface.MONOSPACE}
            val preview=TextView(context).apply {tag="font_option_monospace";typeface=Typeface.MONOSPACE}
            for(view in listOf(label,field,explicit,preview)) root.addView(view)
            LocaleTypography.install(root)
            assertSame(font,label.typeface);assertSame(font,field.typeface)
            assertEquals(Typeface.BOLD,bold.typeface.style)
            assertSame(Typeface.MONOSPACE,explicit.typeface);assertSame(Typeface.MONOSPACE,preview.typeface)
            val added=TextView(context);root.addView(added)
            root.viewTreeObserver.dispatchOnGlobalLayout()
            assertSame(font,added.typeface)
            assertSame(font,VerticalText.uiTypeface(context))
            val spinner=Spinner(context).apply {
                adapter=ArrayAdapter(context,android.R.layout.simple_spinner_dropdown_item,listOf("𡨸","𮞶"))
                setSelection(1)
            }
            root.addView(spinner);root.viewTreeObserver.dispatchOnGlobalLayout()
            assertEquals(1,spinner.selectedItemPosition)
            val popupRow=spinner.adapter.getDropDownView(1,null,root) as TextView
            assertSame(font,popupRow.typeface)
            assertEquals("𮞶",popupRow.text.toString())
        } finally {Locale.setDefault(old)}
    }
}
