/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.os.Looper
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.CheckBox
import android.widget.EditText
import android.widget.Spinner
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Color
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File
import java.io.IOException
import java.util.Locale

/** Bounded compiled wording and real memory/recovery/encoding consumers, not whole-locale acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], shadows = [CommonsPngFailureShadow::class])
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class SlovakSlovenianP0WordingTest {
    private lateinit var previousResources: Resources
    private lateinit var previousLocale: Locale
    private lateinit var previousTag: String

    // Current compiled labels are used for actual control binding.
    private fun expected(tag: String, key: String) = PriorityWordingExpectations.resourceText(tag,key)

    @Before fun rememberLanguage() {
        previousResources = PaintApplication.currentResources
        previousLocale = Locale.getDefault()
        previousTag = AppLanguage.selectedTag(RuntimeEnvironment.getApplication())
        CommonsPngFailureShadow.resetFailure()
    }

    @After fun restoreLanguage() {
        CommonsPngFailureShadow.resetFailure()
        AppLanguage.select(RuntimeEnvironment.getApplication(), previousTag)
        PaintApplication.currentResources = previousResources
        Locale.setDefault(previousLocale)
    }

    private fun forEachLocale(check: (String, Activity) -> Unit) {
        for (tag in listOf("sk", "sl")) {
            val controller = Robolectric.buildActivity(Activity::class.java)
            val activity = controller.get()
            activity.setTheme(R.style.ClassicPaintTheme)
            controller.setup()
            try {
                AppLanguage.select(activity, tag)
                AppLanguage.refresh(activity)
                assertEquals(tag, AppLanguage.selectedTag(activity))
                Locale.setDefault(Locale.US) // Resource locale must win over a mismatched process locale.
                check(tag, activity)
            } finally {
                CommonsPngFailureShadow.resetFailure()
                AppLanguage.select(activity, previousTag)
                AppLanguage.refresh(activity)
                controller.pause().stop().destroy()
                PaintApplication.currentResources = previousResources
                Locale.setDefault(previousLocale)
            }
        }
    }

    @Test fun realSubstitutionsKeepMixedFrameCountsAndFailureReasonsLiteral() = forEachLocale { tag, _ ->
        val format = "GIF 100%"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_unknown"), format),
            ui(R.string.formats22_animation_unknown, format))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "formats22_animation_message"), format, String.format(Locale.forLanguageTag(tag),PriorityWordingExpectations.resourceText(tag,"formats22_at_least_frames"),2)),
            ui(R.string.formats22_animation_message, format, ui(R.string.formats22_at_least_frames, 2)))
        val filename = "drawing 100%.png"
        val detail = "provider 50% unavailable"
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_saved"), filename), ui(R.string.ui_saved, filename))
        assertEquals(String.format(Locale.forLanguageTag(tag), expected(tag, "ui_the_image_was_saved_but_android_could_not"), detail),
            ui(R.string.ui_the_image_was_saved_but_android_could_not, detail))
        assertEquals(if (tag == "sk") "Uložiť" else "Shrani", ui(R.string.ui_save))
        assertEquals(if (tag == "sk") "Uložiť ako…" else "Shrani kot…", ui(R.string.save20_title))
        assertEquals(PriorityWordingExpectations.resourceText(tag,"ui_save_your_changes"), ui(R.string.ui_save_your_changes))
        assertEquals(expected(tag, "ui_save_and_share_41edb4") + "…", ui(R.string.ui_save_and_share))
    }

}
