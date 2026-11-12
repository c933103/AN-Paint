/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import android.net.Uri
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.util.Locale

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class SharedUiStateTest {
    @Test fun legacyPlaceholderMigrationRequiresExplicitProvenance() {
        val label=ui(R.string.ui_untitled)
        val metadata=JSONObject().put("filename",label).put("filename_is_placeholder",true)
        assertSame(DocumentName.Untitled,DocumentName.read(metadata,null))
        metadata.put("filename_is_placeholder",false)
        assertEquals(DocumentName.Named(label),DocumentName.read(metadata,null))
        metadata.put("filename_is_placeholder",true)
        val saved=SavedTarget(Uri.parse("content://example.test/drawing"),label,ExportOptions())
        assertEquals("An explicit save target establishes a real name",
            DocumentName.Named(label),DocumentName.read(metadata,saved))
        assertSame(DocumentName.Recovered,DocumentName.read(JSONObject(),null))
    }

    @Test fun generatedNamesAndMessagesResolveInEveryOfferedLocaleWithoutStoringDisplayText() {
        val context=RuntimeEnvironment.getApplication() as Context
        val previous=AppLanguage.selectedTag(context)
        val oldResources=PaintApplication.currentResources
        val oldLocale=Locale.getDefault()
        val unnamed=JSONObject().also {DocumentName.Untitled.writeTo(it)}
        val recovered=JSONObject().also {DocumentName.Recovered.writeTo(it)}
        val named=JSONObject().also {DocumentName.Named("Untitled").writeTo(it)}
        val status=UiMessage.Resource(R.string.ui_draft_restored)
        val reason=UiMessage.Resource(R.string.ui_the_previous_draft_could_not_be_restored)
        val recovery=UiMessage.Resource(R.string.ui_recovery_copy_preserved_unverified,listOf(reason))
        val external=UiMessage.Literal("100% · %1\$s · 👩🏽‍🎨")
        assertFalse(unnamed.has("filename"));assertFalse(recovered.has("filename"))
        assertEquals("untitled",unnamed.getJSONObject("document_name").getString("kind"))
        assertEquals("recovered",recovered.getJSONObject("document_name").getString("kind"))
        try {
            // This is one resource-identity invariant, not a replay of activities
            // or an assertion that catalogue presence certifies language quality.
            for(tag in AppLanguage.tags(context)) {
                AppLanguage.select(context,tag)
                PaintApplication.currentResources=AppLanguage.wrap(context).resources
                assertEquals(tag,ui(R.string.ui_untitled),DocumentName.read(unnamed,null).text())
                assertEquals(tag,ui(R.string.ui_recovered_image),DocumentName.read(recovered,null).text())
                assertEquals(tag,"Untitled",DocumentName.read(named,null).text())
                assertEquals(tag,ui(R.string.ui_draft_restored),status.text())
                assertEquals(tag,ui(R.string.ui_recovery_copy_preserved_unverified,
                    ui(R.string.ui_the_previous_draft_could_not_be_restored)),recovery.text())
                assertEquals(tag,"100% · %1\$s · 👩🏽‍🎨",external.text())
            }
        } finally {
            AppLanguage.select(context,previous);PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }
}
