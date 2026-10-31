/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.content.res.Configuration
import android.os.LocaleList
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File
import java.io.IOException
import java.util.Locale
import java.util.concurrent.AbstractExecutorService
import java.util.concurrent.TimeUnit

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], qualifiers = "en-rGB")
class TaggedColourImportTest {
    private val context get() = RuntimeEnvironment.getApplication()
    private val neutral = "This image uses a colour profile that AN Paint cannot convert yet. Convert it to sRGB PNG in a colour-managed editor before importing."

    private fun dib(space: Int, icon: Boolean = false) = ByteArray(132).apply {
        fun put(offset: Int, value: Int, bytes: Int = 4) {
            repeat(bytes) { this[offset + it] = (value ushr (8 * it)).toByte() }
        }
        put(0, 124); put(4, 1); put(8, if (icon) 2 else 1)
        put(12, 1, 2); put(14, 24, 2); put(56, space)
    }
    private fun ico(space: Int) = byteArrayOf(0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 24, 0,
        132.toByte(), 0, 0, 0, 22, 0, 0, 0) + dib(space, icon = true)

    private fun assertNeutralFailure(expectedMessage: String = neutral, action: () -> Unit) {
        try { action(); fail("Expected unsupported-profile rejection") }
        catch (expected: IOException) {
            assertEquals(expectedMessage, expected.message)
            assertTrue(expected.cause is LegacyColourMetadata.UnsupportedColour)
        }
    }

    @Test fun packedDibAndIcoRejectUnsupportedProfilesThroughSharedImportAndKeepSources() {
        val folder = File.createTempFile("tagged-import-", "", context.cacheDir).apply { delete(); mkdirs() }
        try {
            for ((name, bytes) in listOf("tagged.dib" to dib(0x4d424544), "tagged.ico" to ico(0x4d424544))) {
                val file = File(folder, name).apply { writeBytes(bytes) }
                assertNeutralFailure { ImportedImage(file, name) }
                if (name.endsWith("ico")) {
                    assertNeutralFailure { IcoCodec.dimensions(file) }
                    assertNeutralFailure { IcoCodec.decode(file, ImageDimensions(1, 1), 256L * 1024 * 1024) }
                } else {
                    assertNeutralFailure { DibCodec.withBmpFile(file) { fail("Must reject before decode") } }
                }
                assertArrayEquals(bytes, file.readBytes())
                assertEquals(listOf(name), folder.listFiles()!!.map { it.name })
                file.delete()
            }
        } finally { folder.deleteRecursively() }
    }

    @Test @Config(qualifiers = "en-rUS")
    fun americanEnglishImportsUseTheAmericanResource() {
        val expected = neutral.replace("colour", "color")
        assertEquals(expected, context.getString(R.string.save20_unsupported_image_colour))
        val file = File.createTempFile("tagged-us-", ".bin", context.cacheDir)
        try {
            for (bytes in listOf(dib(0x4d424544), ico(0x4d424544))) {
                file.writeBytes(bytes)
                assertNeutralFailure(expected) { ImportedImage(file, "profile.bin") }
                assertArrayEquals(bytes, file.readBytes())
            }
        } finally { file.delete() }
    }

    @Test fun explicitSrgbControlsAndRecheckedIconEntryKeepProfileProtection() {
        val file = File.createTempFile("srgb-import-", ".bin", context.cacheDir)
        try {
            file.writeBytes(dib(0x73524742))
            DibCodec.withBmpFile(file) { LegacyColourMetadata.check(it) }
            file.writeBytes(ico(0x73524742))
            val entry = IcoContainer.best(file)
            assertArrayEquals(intArrayOf(0xff000000.toInt()), IcoContainer.decodeDib(file, entry))
            // The second ICO guard matters if bytes change after entry selection.
            // Stable unsupported input is already rejected by best(), before decodeDib().
            file.writeBytes(ico(0x4d424544))
            try { IcoContainer.decodeDib(file, entry); fail("Must recheck the selected entry") }
            catch (expected: LegacyColourMetadata.UnsupportedColour) { assertNotNull(expected.message) }
        } finally { file.delete() }
    }

    @Test fun failedSelectionNeverOffersTaggedDibOrIcoToTheDocumentAndDeletesStagedFile() {
        val controller = Robolectric.buildActivity(Activity::class.java).setup()
        val worker = object : AbstractExecutorService() {
            override fun execute(command: Runnable) = command.run()
            override fun shutdown() = Unit
            override fun shutdownNow(): MutableList<Runnable> = mutableListOf()
            override fun isShutdown() = false
            override fun isTerminated() = false
            override fun awaitTermination(timeout: Long, unit: TimeUnit) = true
        }
        try {
            for (bytes in listOf(dib(0x4d424544), ico(0x4d424544))) {
                val staged = File.createTempFile("selection-tagged-", ".bin", context.cacheDir).apply { writeBytes(bytes) }
                var failure: Throwable? = null
                ImportSelection(controller.get(), worker, { 1L },
                    selected = { fail("Rejected input must never reach the document callback") },
                    cancelled = { fail("An unsupported profile is a failure, not cancellation") },
                    failed = { failure = it }).start(staged, "provider.bin")
                assertEquals(neutral, failure?.message)
                assertTrue(failure?.cause is LegacyColourMetadata.UnsupportedColour)
                assertFalse(staged.exists())
            }
        } finally { controller.pause().stop().destroy() }
    }

    private fun exactScriptBoundFixture(tag: String): JSONObject {
        require(tag in listOf("tt-Latn","ain-Latn","mn-Mong"))
        val data=JSONObject(File("../tools/fixtures/exact_script_priority_wording/$tag.json").readText(Charsets.UTF_8))
        assertEquals(1,data.getInt("schema_version"))
        assertEquals(tag,data.getString("locale"))
        assertEquals("Paintroid/src/main/res/values-b+${tag.replace('-', '+')}/strings.xml",data.getString("catalogue_path"))
        return data
    }

    private fun exactScriptSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) exactScriptSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) exactScriptSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun addExactScript(expected: JSONObject, supplied: JSONObject) {
        val key="save20_unsupported_image_colour"
        assertEquals(setOf("tt-Latn"),supplied.keys().asSequence().toSet())
        for(tag in listOf("tt-Latn")) {
            val current=exactScriptBoundFixture(tag).getJSONObject("rows").getJSONObject(key)
            val row=supplied.getJSONObject(tag).getJSONObject("rows").getJSONObject(key)
            exactScriptSameJson(current,row)
            assertEquals("string",row.getString("type"))
            assertEquals("edited",row.getString("decision"))
            assertEquals("This image uses a colour profile that AN Paint cannot convert yet. Convert it to sRGB PNG in a colour-managed editor before importing.",row.getJSONObject("source").getString("value"))
            assertFalse(expected.has(tag));assertTrue(row.isNull("previous_target"))
            expected.put(tag,row.getString("compiled_display"))
        }
    }
    private fun exactScriptExpectations()=JSONObject().apply {
        for(tag in listOf("tt-Latn")) put(tag,exactScriptBoundFixture(tag))
    }
    @Test fun exactScriptTaggedRejectsCoordinatedFixtureAndPredecessorMutations() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("tt-Latn")) for(mutation in listOf("coordinated","source","previous","attributes","presence")) {
            val data=exactScriptExpectations()
            val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("rows").getJSONObject(key)
            when(mutation) {
                "coordinated" -> {row.put("reviewed_value","forged");row.put("reviewed_display","forged");row.put("compiled_display","forged")}
                "source" -> row.getJSONObject("source").put("value","forged")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("attributes").put("formatted","false")
                "presence" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addExactScript(expected,data) }
        }
    }

    @Test fun exactScriptTaggedIgnoresUnrelatedFixtureMetadata() {
        val data=exactScriptExpectations()
        data.getJSONObject("tt-Latn").put("limits","Caller note does not redefine the tagged message")
        val expected=JSONObject()
        addExactScript(expected,data)
        assertEquals(exactScriptBoundFixture("tt-Latn").getJSONObject("rows")
            .getJSONObject("save20_unsupported_image_colour").getString("compiled_display"),expected.getString("tt-Latn"))
    }

    @Test fun everyOfferedLanguageResolvesItsScopedMessageOrExplicitEnglishFallback() {
        val expected = javaClass.getResourceAsStream("/tagged-colour/expected.json")!!
            .bufferedReader().use { JSONObject(it.readText()) }
        // Current catalogues use semantic assertions, not copied approval-history text.
        val currentCatalogues = setOf("ary", "as", "ast", "az", "be", "bo", "br", "bs", "ca", "ca-ES-valencia", "ceb", "ckb", "csb", "cy", "da", "de", "dz", "el", "en-AU", "es-ES", "eu-ES", "fa", "fa-IR", "fr", "fy", "ga", "gd", "gl", "gu", "ha", "he", "hi", "hne", "hr", "ht", "hy", "ia", "ig", "is", "it", "ja", "jv", "ka", "kab", "kk", "km", "kn", "ko-KP", "ku", "ky", "la", "ln", "lo", "lt", "mai", "mi", "mk", "ml-IN", "mn-Cyrl-MN", "mr", "mww", "my", "nds", "ne", "nl", "nn", "no", "oc", "pa-IN", "pcm", "ps", "pt-PT", "ro", "rw", "sa", "sd", "se", "si", "sk", "sl", "sm", "so", "sq", "sr-Cyrl", "sr-Latn", "su", "ta", "te", "tg", "th", "tok", "tpi", "tr", "tt-Cyrl", "ug", "uk", "ur", "uz-Latn", "wa", "wo", "xh", "yi", "yo", "za", "zh-HK", "zu")
        addExactScript(expected,exactScriptExpectations())
        val expectedFallbacks = AppLanguage.tags(context).count { it !in currentCatalogues && !expected.has(it) }
        var fallbacks = 0
        for (tag in AppLanguage.tags(context)) {
            val configuration = Configuration(context.resources.configuration).apply {
                setLocales(LocaleList(AppLanguage.resourceLocale(Locale.forLanguageTag(tag))))
            }
            val message = context.createConfigurationContext(configuration).getString(R.string.save20_unsupported_image_colour)
            assertFalse(tag, message.contains("BMP"))
            assertFalse(tag, message.contains("GIF"))
            assertTrue(tag, message.contains("sRGB"))
            assertTrue(tag, message.contains("PNG"))
            if (tag in currentCatalogues) continue
            val expectedMessage = if(expected.has(tag)) expected.getString(tag) else neutral.also { fallbacks++ }
            assertEquals("Remaining fixed boundary or explicit English fallback for $tag",expectedMessage,message)
        }
        assertEquals(expectedFallbacks,fallbacks)
    }
}
