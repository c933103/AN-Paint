/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.util.Base64
import org.catrobat.paintroid.classic.GalleryPage
import org.catrobat.paintroid.classic.GalleryTypography
import org.catrobat.paintroid.classic.IllustrationPage
import org.catrobat.paintroid.classic.IllustrationSource
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[28])
class GalleryTypographyTest {
    @Test fun nomAndManchuActionsEmbedTheSameVerifiedFontsAsNativeControls() {
        val context=RuntimeEnvironment.getApplication()
        for((tag,asset) in listOf("vi-Hani" to "fonts/anpaintnomui.ttf","mnc-Mong" to "fonts/notosansmongolian.ttf","wuu-Hans" to "fonts/anpaintwuufallback.ttf")) {
            val css=GalleryTypography.css(context,Locale.forLanguageTag(tag))
            val encoded=css.substringAfter("data:font/ttf;base64,").substringBefore('"')
            assertArrayEquals(context.assets.open(asset).use {it.readBytes()},Base64.decode(encoded,Base64.DEFAULT))
            assertTrue(css.contains("[data-anpaint-action]{font-family:ANPaintAction,sans-serif!important;"))
            assertFalse(css.contains("body{"));assertFalse(css.contains("a{"))
            assertTrue(css.contains("writing-mode:"+(if(tag=="mnc-Mong") "vertical-lr" else "horizontal-tb")+"!important"))
        }
    }
    @Test fun allVerticalLocalesUseScopedWritingDirectionWithoutReplacingPageProse() {
        val context=RuntimeEnvironment.getApplication()
        for((tag,direction) in listOf("mn-Mong" to "vertical-lr","lzh-Hant" to "vertical-rl",
                "en-XV" to "vertical-lr","qaa-Zsye-XV" to "vertical-rl","en-US" to "horizontal-tb")) {
            val css=GalleryTypography.css(context,Locale.forLanguageTag(tag))
            assertTrue(tag,css.contains("writing-mode:$direction!important"))
        }
        for(provider in IllustrationSource.values()) {
            val script=IllustrationPage.script(provider,"Use","Copy")
            assertTrue(provider.name,script.contains("setAttribute('data-anpaint-action','true')"))
        }
        assertEquals(2,Regex("setAttribute\\('data-anpaint-action','true'\\)").findAll(GalleryPage.script("Use","Copy")).count())
    }
}
