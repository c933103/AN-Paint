/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.util.Locale

/** Later finite disposition; deliberately not part of the frozen residual packet. */
internal object LegacyDiscardExpectations {
    fun successor(tag: String,key: String,previous: String): String {
        require(tag=="ps" && key=="ui_discard" && previous=="رد کړئ") {
            "Outside exact legacy Discard identity/predecessor"
        }
        return "بدلونونه پرېږدئ"
    }
}

/** Compiled values only: no claim that the legacy key is an active dialog caller. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class LegacyDiscardDispositionTest {
    @Test fun refinedPashtoAndUnchangedBasqueResolveExactlyInSelectedLocale() {
        val app=RuntimeEnvironment.getApplication()
        val previousTag=AppLanguage.selectedTag(app)
        val previousResources=PaintApplication.currentResources
        val previousLocale=Locale.getDefault()
        try {
            for((tag,text) in mapOf("ps" to LegacyDiscardExpectations.successor("ps","ui_discard","رد کړئ"),
                "eu-ES" to "Baztertu aldaketak")) {
                val controller=Robolectric.buildActivity(Activity::class.java)
                val activity=controller.setup().get()
                try {
                    AppLanguage.select(activity,tag);AppLanguage.refresh(activity)
                    assertEquals(tag,AppLanguage.selectedTag(activity))
                    assertEquals(text,activity.getString(R.string.ui_discard))
                    assertEquals(text,activity.getString(R.string.ui_discard_changes23))
                    assertNotEquals(text,activity.getString(R.string.ui_keep_editing23))
                } finally {controller.pause().stop().destroy()}
            }
        } finally {
            AppLanguage.select(app,previousTag)
            PaintApplication.currentResources=previousResources
            Locale.setDefault(previousLocale)
        }
    }

    @Test fun successorRejectsUnreviewedIdentityAndHistoricalDisplay() {
        for((tag,key,previous) in listOf(Triple("eu-ES","ui_discard","رد کړئ"),
            Triple("ps","ui_discard_changes23","رد کړئ"),Triple("ps","ui_discard","forged"))) {
            assertThrows(IllegalArgumentException::class.java) {
                LegacyDiscardExpectations.successor(tag,key,previous)
            }
        }
    }
}
