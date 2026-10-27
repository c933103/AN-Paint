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

    private fun boundSoWoHtFixture(bytes: ByteArray = File("../tools/fixtures/current_localization/somali_wolof_haitian_creole_priority_wording.json").readBytes()): JSONObject {
        val digest = java.security.MessageDigest.getInstance("SHA-256").digest(bytes)
            .joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical Somali/Wolof/Haitian Creole fixture", "601d60e5fb772bc7bdfebc6774492fb1b0a3f84454937c4f29711cb2080319eb", digest)
        return JSONObject(String(bytes, Charsets.UTF_8))
    }

    @Test fun canonicalFixtureRejectsCoordinatedTargetReplacement() {
        val key = "save20_unsupported_image_colour"
        for (tag in listOf("so", "wo", "ht")) {
            val forged = boundSoWoHtFixture()
            forged.getJSONObject("locales").getJSONObject(tag).getJSONObject("accepted").put(key, "forged complete target")
            assertThrows("$tag coordinated fixture/target replacement", AssertionError::class.java) {
                boundSoWoHtFixture(forged.toString().toByteArray(Charsets.UTF_8))
            }
        }
    }

    private fun soWoHtExpectations() = boundSoWoHtFixture()

    private fun requireSameSoWoHtJson(expected: Any?, actual: Any?) {
        when (expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject)
                val other = actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(), other.keys().asSequence().toSet())
                for (key in expected.keys()) requireSameSoWoHtJson(expected.get(key), other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray)
                val other = actual as org.json.JSONArray
                assertEquals(expected.length(), other.length())
                for (index in 0 until expected.length()) requireSameSoWoHtJson(expected.get(index), other.get(index))
            }
            else -> assertEquals(expected, actual)
        }
    }

    private fun addSoWoHt(expected: JSONObject,reviewed: JSONObject) {
        requireSameSoWoHtJson(soWoHtExpectations(), reviewed)
        val key="save20_unsupported_image_colour"
        val source=reviewed.getJSONObject("sources").getJSONObject(key)
        assertEquals("string",source.getString("type"));assertEquals(neutral,source.getString("source"))
        assertEquals(setOf("name"),source.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals(key,source.getJSONObject("attributes").getString("name"))
        val canonical=soWoHtExpectations().getJSONObject("locales")
        for(tag in listOf("so","wo","ht")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject("locales").getJSONObject(tag)
            assertFalse("Historical resource must be absent $tag",row.getJSONObject("predecessors").has(key))
            assertTrue("Explicit previous-target key required $tag",row.getJSONObject("previous_targets").has(key))
            assertTrue("Explicit null predecessor required $tag",row.getJSONObject("previous_targets").isNull(key))
            assertTrue("Must be an explicit changed value $tag",(0 until row.getJSONArray("changed").length()).any {
                row.getJSONArray("changed").getString(it)==key })
            assertFalse("Exact name-only target attributes $tag",row.getJSONObject("target_attribute_exceptions").has(key))
            val raw=row.getJSONObject("accepted").getString(key)
            assertTrue(raw.isNotEmpty());assertFalse(raw.startsWith("@"))
            assertEquals("Exact complete raw target $tag",canonical.getJSONObject(tag).getJSONObject("accepted").getString(key),raw)
            val display=Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            expected.put(tag,display)
        }
    }

    @Test fun finiteSoWoHtAdditionRejectsSourceAttributesHistoryAndTargetCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("so","wo","ht")) for(mutation in listOf("source","sourceAttributes","sourceType","previous","missingNull","nonNull","attributes","changed","empty","target","alias","alreadyPresent")) {
            val data=soWoHtExpectations();val expected=JSONObject()
            val source=data.getJSONObject("sources").getJSONObject(key)
            val row=data.getJSONObject("locales").getJSONObject(tag)
            when(mutation) {
                "source" -> source.put("source","forged")
                "sourceAttributes" -> source.getJSONObject("attributes").put("formatted","false")
                "sourceType" -> source.put("type","plurals")
                "previous" -> row.getJSONObject("predecessors").put(key,"forged")
                "missingNull" -> row.getJSONObject("previous_targets").remove(key)
                "nonNull" -> row.getJSONObject("previous_targets").put(key,"forged")
                "attributes" -> row.getJSONObject("target_attribute_exceptions").put(key,JSONObject().put("name",key).put("formatted","false"))
                "changed" -> row.put("changed",org.json.JSONArray())
                "empty" -> row.getJSONObject("accepted").put(key,"")
                "target" -> row.getJSONObject("accepted").put(key,"forged")
                "alias" -> row.getJSONObject("accepted").put(key,"@string/ui_save")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addSoWoHt(expected,data) }
        }
    }

    @Test fun everyOfferedLanguageResolvesItsScopedMessageOrExplicitEnglishFallback() {
        // This family has 59 baseline catalogues plus reviewed Amharic/Czech/Polish/Swedish/Bulgarian/Bengali/Nynorsk/Danish/Norwegian/Catalan/Romanian/Slovak/Slovenian/Serbian Cyrillic/Serbian Latin values.
        // Global review scope is unchanged. The Valencian option inherits the ca resource;
        // this is routing evidence, not an independently reviewed Valencian value.
        val expected = javaClass.getResourceAsStream("/tagged-colour/expected.json")!!
            .bufferedReader().use { JSONObject(it.readText()) }
        assertEquals(76, expected.length()) // Frozen predecessor remains unchanged.
        assertFalse(expected.has("uk"))
        expected.put("uk", PriorityWordingExpectations.display("uk","save20_unsupported_image_colour"))
        assertEquals(77, expected.length())
        val indianPriority=JSONObject(File("../tools/fixtures/current_localization/marathi_tamil_telugu_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("mr","ta","te")) {
            assertFalse(expected.has(tag))
            expected.put(tag,indianPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(80, expected.length())
        val nextPriority=JSONObject(File("../tools/fixtures/current_localization/kannada_malayalam_filipino_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("kn","ml-IN")) {
            assertFalse(expected.has(tag))
            expected.put(tag,nextPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(82, expected.length())
        val nePaPriority=JSONObject(File("../tools/fixtures/current_localization/nepali_punjabi_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("ne","pa-IN")) {
            assertFalse(expected.has(tag))
            expected.put(tag,nePaPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(84, expected.length())
        val asKmLoPriority=JSONObject(File("../tools/fixtures/current_localization/assamese_khmer_lao_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("as","km","lo")) {
            assertFalse(expected.has(tag))
            expected.put(tag,asKmLoPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(87, expected.length())
        val jvSuKyPriority=JSONObject(File("../tools/fixtures/current_localization/javanese_sundanese_kyrgyz_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("jv","su","ky")) {
            assertFalse(expected.has(tag))
            expected.put(tag,jvSuKyPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(90, expected.length())
        val haIgLnPriority=JSONObject(File("../tools/fixtures/current_localization/hausa_igbo_lingala_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("ha","ig","ln")) {
            assertFalse(expected.has(tag))
            expected.put(tag,haIgLnPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(93, expected.length())
        val yoZuXhPriority=JSONObject(File("../tools/fixtures/current_localization/yoruba_zulu_xhosa_priority_wording.json").readText()).getJSONObject("locales")
        for(tag in listOf("yo","zu","xh")) {
            assertFalse(expected.has(tag))
            expected.put(tag,yoZuXhPriority.getJSONObject(tag).getJSONObject("accepted").getString("save20_unsupported_image_colour"))
        }
        assertEquals(96, expected.length())
        addSoWoHt(expected,soWoHtExpectations())
        assertEquals(99, expected.length())
        assertTrue(expected.has("bg")); assertTrue(expected.has("bn")); assertTrue(expected.has("nn"))
        assertTrue(expected.has("da")); assertTrue(expected.has("no"))
        assertTrue(expected.has("ca")); assertTrue(expected.has("ro"))
        assertTrue(expected.has("sk")); assertTrue(expected.has("sl"))
        assertTrue(expected.has("sr-Cyrl")); assertTrue(expected.has("sr-Latn"))
        assertTrue(expected.has("hr")); assertTrue(expected.has("bs"))
        assertTrue(expected.has("am")); assertTrue(expected.has("cs")); assertTrue(expected.has("pl")); assertTrue(expected.has("sv"))
        assertEquals(171, AppLanguage.tags(context).size)
        val inheritedCatalogues = mapOf("ca-ES-valencia" to "ca")
        assertTrue(inheritedCatalogues.keys.none { expected.has(it) })
        var inherited = 0
        var fallbacks = 0
        assertTrue(AppLanguage.tags(context).containsAll(expected.keys().asSequence().toList()))
        for (tag in AppLanguage.tags(context)) {
            val configuration = Configuration(context.resources.configuration).apply {
                setLocales(LocaleList(AppLanguage.resourceLocale(Locale.forLanguageTag(tag))))
            }
            val message = context.createConfigurationContext(configuration).getString(R.string.save20_unsupported_image_colour)
            assertFalse(tag, message.contains("BMP"))
            assertFalse(tag, message.contains("GIF"))
            assertTrue(tag, message.contains("sRGB"))
            assertTrue(tag, message.contains("PNG"))
            val parent = inheritedCatalogues[tag]
            val expectedMessage = when {
                expected.has(tag) -> expected.getString(tag)
                parent != null -> expected.getString(parent).also { inherited++ }
                else -> neutral.also { fallbacks++ }
            }
            assertEquals("Direct, parent-inherited or explicit English family value for $tag",
                expectedMessage, message)
        }
        assertEquals(1, inherited)
        assertEquals(71, fallbacks) // 171 offered - 99 exact current values - 1 inherited.
    }
}
