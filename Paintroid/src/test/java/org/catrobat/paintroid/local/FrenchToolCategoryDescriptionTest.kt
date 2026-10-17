/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import org.catrobat.paintroid.classic.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.util.Locale

/** Selection wording must agree with the fixed noun "outil", not a variable tool label. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class FrenchToolCategoryDescriptionTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var french: Context

    @Before fun useFrenchResources() {
        previousResources=PaintApplication.currentResources
        previousLocale=Locale.getDefault()
        val application=RuntimeEnvironment.getApplication() as Context
        val configuration=Configuration(application.resources.configuration).apply {setLocale(Locale.FRENCH)}
        french=application.createConfigurationContext(configuration)
        PaintApplication.currentResources=french.resources
        Locale.setDefault(Locale.FRENCH)
    }

    @After fun restoreResources() {
        PaintApplication.currentResources=previousResources
        Locale.setDefault(previousLocale)
    }

    private fun expected(category: ToolCategory,tool: PaintTool,expanded: Boolean): String =
        "${ui(category.labelId)}. Outil sélectionné : ${tool.label}. " +
            if(expanded) "Réduire les outils et options" else "Développer les outils et options"

    private fun assertCaption(button: ToolCategoryButton,expected: String) {
        assertEquals(expected,button.contentDescription.toString())
        assertEquals(expected,button.tooltipText.toString())
    }

    @Test fun actualCategoryControlsKeepEveryToolGrammaticalInBothExpansionStates() {
        // These assertions establish that the loop covers both noun genders in compiled resources.
        assertEquals("Brosse",PaintTool.BRUSH.label)
        assertEquals("Ellipse",PaintTool.ELLIPSE.label)
        assertEquals("Sélection rectangulaire",PaintTool.SELECT.label)
        assertEquals("Crayon",PaintTool.PENCIL.label)
        for(down in listOf(false,true)) for(category in ToolCategory.values()) {
            for(tool in category.tools) {
                val button=ToolCategoryButton(french,category,tool,down)
                for(expanded in listOf(false,true)) {
                    button.expanded=expanded
                    button.refresh()
                    assertEquals(ui(category.labelId),button.text.toString())
                    assertCaption(button,expected(category,tool,expanded))
                }
            }
        }
    }

    @Test fun selectionRefreshReplacesBothAccessibilityAndTooltipWithoutStaleToolText() {
        val button=ToolCategoryButton(french,ToolCategory.BRUSH,PaintTool.PENCIL,false)
        assertCaption(button,"Dessin. Outil sélectionné : Crayon. Développer les outils et options")
        button.selectedTool=PaintTool.BRUSH
        button.refresh()
        assertCaption(button,"Dessin. Outil sélectionné : Brosse. Développer les outils et options")
        button.selectedTool=PaintTool.WATERCOLOR
        button.expanded=true
        button.refresh()
        assertCaption(button,"Dessin. Outil sélectionné : Aquarelle. Réduire les outils et options")
        button.expanded=false
        button.refresh()
        assertCaption(button,"Dessin. Outil sélectionné : Aquarelle. Développer les outils et options")
    }
}
