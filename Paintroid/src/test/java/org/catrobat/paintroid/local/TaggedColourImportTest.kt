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

    @Test fun recoveredHiGuTaggedAdditionsRejectCoordinatedFixtureAndDuplicateMutations() {
        for(tag in listOf("hi","gu")) for(field in listOf("accepted","attributes","predecessors")) {
            val data=HiGuPriorityExpectations.fixture()
            data.getJSONObject("locales").getJSONObject(tag).getJSONObject(field).put("save20_unsupported_image_colour","forged")
            assertThrows(AssertionError::class.java) { HiGuPriorityExpectations.addTagged(JSONObject(),data) }
        }
        for(tag in listOf("hi","gu")) {
            val expected=JSONObject().put(tag,"already present")
            assertThrows(AssertionError::class.java) { HiGuPriorityExpectations.addTagged(expected,HiGuPriorityExpectations.fixture()) }
        }
    }

    @Test fun replacementThaiTaggedAdditionsRejectCoordinatedFixtureAndDuplicateMutations() {
        for(tag in listOf("th")) for(field in listOf("accepted","attributes","predecessors")) {
            val data=ThaiPriorityExpectations.fixture()
            data.getJSONObject("locales").getJSONObject(tag).getJSONObject(field).put("save20_unsupported_image_colour","forged")
            assertThrows(AssertionError::class.java) { ThaiPriorityExpectations.addTagged(JSONObject(),data) }
        }
        for(tag in listOf("th")) {
            val expected=JSONObject().put(tag,"already present")
            assertThrows(AssertionError::class.java) { ThaiPriorityExpectations.addTagged(expected,ThaiPriorityExpectations.fixture()) }
        }
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

    private fun gaGdCyBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/irish_gaelic_welsh_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite GA/GD/CY reviewed fixture", "1aa3267e9234866e23d38350d56a3793b15942f6070e837caed0a9116005034c", actual)
        return JSONObject(String(bytes,Charsets.UTF_8)).getJSONObject("locales")
    }

    private fun gaGdCySameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) gaGdCySameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) gaGdCySameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun gaGdCyExpectations() = gaGdCyBoundFixture()

    private fun addGaGdCy(expected: JSONObject, reviewed: JSONObject) {
        gaGdCySameJson(gaGdCyBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        assertEquals(setOf("ga","gd","cy"),reviewed.keys().asSequence().toSet())
        for(tag in listOf("ga","gd","cy")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject("string/$key")
            assertEquals(neutral,row.getString("source"))
            for(field in listOf("source_attributes","attributes")) {
                assertEquals(setOf("name"),row.getJSONObject(field).keys().asSequence().toSet())
                assertEquals(key,row.getJSONObject(field).getString("name"))
            }
            assertTrue(row.has("previous_target") && row.isNull("previous_target"))
            assertTrue(row.has("previous_attributes") && row.isNull("previous_attributes"))
            val target=row.getString("target").removeSurrounding("\"").replace("\\'","'").replace("\\\"","\"").replace("\\n","\n")
            assertEquals(target,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteGaGdCyAdditionsRejectSourceAttributesAndPredecessorCorruption() {
        for(tag in listOf("ga","gd","cy")) for(mutation in listOf("source","source_attributes","previous_target","previous_attributes","attributes","display","target","alreadyPresent","missing_previous_target","missing_previous_attributes","coordinated_target_display")) {
            val data=gaGdCyExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject("string/save20_unsupported_image_colour")
            when(mutation) {
                "coordinated_target_display" -> {row.put("target","\"forged\"");row.put("display","forged")}
                "source_attributes","attributes" -> row.getJSONObject(mutation).put("formatted","false")
                "alreadyPresent" -> expected.put(tag,"forged")
                "missing_previous_target","missing_previous_attributes" -> row.remove(mutation.removePrefix("missing_"))
                else -> row.put(mutation,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) {addGaGdCy(expected,data)}
        }
    }

    private fun kaHyAzBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/georgian_armenian_azerbaijani_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite KA/HY/AZ reviewed fixture", "6672b568ad8919285db2ed87ce13f2578a6f29a651a10c885d4ca5ac4dbd9247", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun kaHyAzSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) kaHyAzSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) kaHyAzSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun kaHyAzExpectations() = kaHyAzBoundFixture()

    private fun addKaHyAz(expected: JSONObject, reviewed: JSONObject) {
        kaHyAzSameJson(kaHyAzBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        val source=reviewed.getJSONObject("sources").getJSONObject(key)
        assertEquals(neutral,source.getString("value"))
        assertEquals(setOf("name"),source.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals(key,source.getJSONObject("attributes").getString("name"))
        for(tag in listOf("ka","hy","az")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject("locales").getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Historical resource must be absent $tag",row.has("previous") && row.isNull("previous"))
            assertEquals(setOf("name"),row.getJSONObject("attributes").keys().asSequence().toSet())
            assertEquals(key,row.getJSONObject("attributes").getString("name"))
            assertEquals(row.getString("target"),row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteKaHyAzAdditionRejectsSourceAttributesAndPredecessorCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("ka","hy","az")) for(mutation in listOf("source","sourceAttributes","previous","attributes","display","target","coordinatedTargetDisplay","missingPrevious","alreadyPresent")) {
            val data=kaHyAzExpectations();val expected=JSONObject()
            val row=data.getJSONObject("locales").getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "source" -> data.getJSONObject("sources").getJSONObject(key).put("value","forged")
                "sourceAttributes" -> data.getJSONObject("sources").getJSONObject(key).getJSONObject("attributes").put("formatted","false")
                "previous" -> row.put("previous","forged")
                "attributes" -> row.getJSONObject("attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "target" -> row.put("target","forged")
                "coordinatedTargetDisplay" -> {row.put("target","forged");row.put("display","forged")}
                "missingPrevious" -> row.remove("previous")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addKaHyAz(expected,data) }
        }
    }

    private fun glNlDeBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/galician_dutch_german_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite GL/NL/DE reviewed fixture", "b41b2203f862653c81c4b265a2ba502e5fc089df505ce592b4fdd6201accb9bd", actual)
        return JSONObject(String(bytes,Charsets.UTF_8)).getJSONObject("locales")
    }

    private fun glNlDeSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) glNlDeSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) glNlDeSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun glNlDeExpectations() = glNlDeBoundFixture()

    private fun addGalician(expected: JSONObject, reviewed: JSONObject) {
        glNlDeSameJson(glNlDeBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        assertEquals(setOf("gl","nl","de"),reviewed.keys().asSequence().toSet())
        assertFalse("Exact prior absence for gl",expected.has("gl"))
        val row=reviewed.getJSONObject("gl").getJSONObject("values").getJSONObject("string/$key")
        assertEquals(neutral,row.getString("source"))
        for(field in listOf("source_attributes","attributes")) {
            assertEquals(setOf("name"),row.getJSONObject(field).keys().asSequence().toSet())
            assertEquals(key,row.getJSONObject(field).getString("name"))
        }
        assertTrue(row.has("previous_target") && row.isNull("previous_target"))
        assertTrue(row.has("previous_attributes") && row.isNull("previous_attributes"))
        val target=row.getString("target").removeSurrounding("\"").replace("\\'","'").replace("\\\"","\"").replace("\\n","\n")
        assertEquals(target,row.getString("display"))
        expected.put("gl",row.getString("display"))
    }

    @Test fun finiteGalicianAdditionRejectsSourceAttributesMissingFieldsAndPredecessorCorruption() {
        for(mutation in listOf("source","source_attributes","previous_target","previous_attributes","attributes","display","target","alreadyPresent","missing_previous_target","missing_previous_attributes","coordinated_target_display")) {
            val data=glNlDeExpectations();val expected=JSONObject()
            val row=data.getJSONObject("gl").getJSONObject("values").getJSONObject("string/save20_unsupported_image_colour")
            when(mutation) {
                "coordinated_target_display" -> {row.put("target","\"forged\"");row.put("display","forged")}
                "source_attributes","attributes" -> row.getJSONObject(mutation).put("formatted","false")
                "alreadyPresent" -> expected.put("gl","forged")
                "missing_previous_target","missing_previous_attributes" -> row.remove(mutation.removePrefix("missing_"))
                else -> row.put(mutation,"forged")
            }
            assertThrows("gl/$mutation",AssertionError::class.java) {addGalician(expected,data)}
        }
    }

    private fun brAstOcBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/breton_asturian_occitan_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite BR/AST/OC reviewed fixture", "f45f54e4428d438907514b0d54ef267f2b5dce5003fb7a68657c2159b44e2c9d", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun brAstOcSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) brAstOcSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) brAstOcSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun brAstOcExpectations() = brAstOcBoundFixture()

    private fun addBrAstOc(expected: JSONObject, reviewed: JSONObject) {
        brAstOcSameJson(brAstOcBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        val source=reviewed.getJSONObject("sources").getJSONObject(key)
        assertEquals("string",source.getString("type"))
        assertEquals(neutral,source.getString("source"))
        assertEquals(setOf("name"),source.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals(key,source.getJSONObject("attributes").getString("name"))
        for(tag in listOf("br","ast","oc")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject("locales").getJSONObject(tag)
            assertFalse("Historical resource must be absent $tag",row.getJSONObject("predecessors").has(key))
            assertTrue("Must be an explicit changed value $tag",(0 until row.getJSONArray("changed").length()).any {
                row.getJSONArray("changed").getString(it)==key })
            assertFalse("Exact name-only target attributes $tag",row.getJSONObject("target_attribute_exceptions").has(key))
            val raw=row.getJSONObject("accepted").getString(key)
            assertTrue(raw.isNotEmpty());assertFalse(raw.startsWith("@"))
            val display=Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            expected.put(tag,display)
        }
    }

    @Test fun finiteBrAstOcAdditionRejectsSourceAttributesAndPredecessorCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("br","ast","oc")) for(mutation in listOf("source","sourceAttributes","sourceType","previous","attributes","changed","empty","nonemptyTarget","coordinatedSourceTarget","alreadyPresent")) {
            val data=brAstOcExpectations();val expected=JSONObject()
            val source=data.getJSONObject("sources").getJSONObject(key)
            val row=data.getJSONObject("locales").getJSONObject(tag)
            when(mutation) {
                "source" -> source.put("source","forged")
                "sourceAttributes" -> source.getJSONObject("attributes").put("formatted","false")
                "sourceType" -> source.put("type","plurals")
                "previous" -> row.getJSONObject("predecessors").put(key,"forged")
                "attributes" -> row.getJSONObject("target_attribute_exceptions").put(key,JSONObject().put("name",key).put("formatted","false"))
                "changed" -> row.put("changed",org.json.JSONArray())
                "empty" -> row.getJSONObject("accepted").put(key,"")
                "nonemptyTarget" -> row.getJSONObject("accepted").put(key,"forged target")
                "coordinatedSourceTarget" -> {source.put("source","forged source");row.getJSONObject("accepted").put(key,"forged target")}
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addBrAstOc(expected,data) }
        }
    }

    private fun iaLaKuBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/interlingua_latin_kurdish_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite IA/LA/KU reviewed fixture", "ed6303b7679210398cf56f555ab86ce6793322a871ce05d63e3fb799a0456b37", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun iaLaKuSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) iaLaKuSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) iaLaKuSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun iaLaKuExpectations() = iaLaKuBoundFixture()

    private fun addIaLaKu(expected: JSONObject, reviewed: JSONObject) {
        iaLaKuSameJson(iaLaKuBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        val source=reviewed.getJSONObject("sources").getJSONObject(key)
        assertEquals("string",source.getString("type"))
        assertEquals(neutral,source.getString("source"))
        assertEquals(setOf("name"),source.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals(key,source.getJSONObject("attributes").getString("name"))
        for(tag in listOf("ia","la","ku")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject("locales").getJSONObject(tag)
            assertFalse("Historical resource must be absent $tag",row.getJSONObject("predecessors").has(key))
            assertTrue("Must be an explicit changed value $tag",(0 until row.getJSONArray("changed").length()).any {
                row.getJSONArray("changed").getString(it)==key })
            assertFalse("Exact name-only target attributes $tag",row.getJSONObject("target_attribute_exceptions").has(key))
            val raw=row.getJSONObject("accepted").getString(key)
            assertTrue(raw.isNotEmpty());assertFalse(raw.startsWith("@"))
            val display=Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            expected.put(tag,display)
        }
    }

    @Test fun finiteIaLaKuAdditionRejectsSourceAttributesAndPredecessorCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("ia","la","ku")) for(mutation in listOf("source","sourceAttributes","sourceType","previous","attributes","changed","empty","nonemptyTarget","coordinatedSourceTarget","alreadyPresent")) {
            val data=iaLaKuExpectations();val expected=JSONObject()
            val source=data.getJSONObject("sources").getJSONObject(key)
            val row=data.getJSONObject("locales").getJSONObject(tag)
            when(mutation) {
                "source" -> source.put("source","forged")
                "sourceAttributes" -> source.getJSONObject("attributes").put("formatted","false")
                "sourceType" -> source.put("type","plurals")
                "previous" -> row.getJSONObject("predecessors").put(key,"forged")
                "attributes" -> row.getJSONObject("target_attribute_exceptions").put(key,JSONObject().put("name",key).put("formatted","false"))
                "changed" -> row.put("changed",org.json.JSONArray())
                "empty" -> row.getJSONObject("accepted").put(key,"")
                "nonemptyTarget" -> row.getJSONObject("accepted").put(key,"forged target")
                "coordinatedSourceTarget" -> {source.put("source","forged source");row.getJSONObject("accepted").put(key,"forged target")}
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addIaLaKu(expected,data) }
        }
    }

    private fun miSmRwBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/maori_samoan_kinyarwanda_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite MI/SM/RW reviewed fixture", "efaa8682d929a670acc3915e14941f9099513437df5874d2c16958e63182bc01", actual)
        return JSONObject(String(bytes,Charsets.UTF_8)).getJSONObject("locales")
    }

    private fun miSmRwSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) miSmRwSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) miSmRwSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun miSmRwExpectations() = miSmRwBoundFixture()

    private fun addMiSmRw(expected: JSONObject, reviewed: JSONObject) {
        miSmRwSameJson(miSmRwBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        assertEquals(setOf("mi","sm","rw"),reviewed.keys().asSequence().toSet())
        for(tag in listOf("mi","sm","rw")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject("string/$key")
            assertEquals(neutral,row.getString("source"))
            for(field in listOf("source_attributes","attributes")) {
                assertEquals(setOf("name"),row.getJSONObject(field).keys().asSequence().toSet())
                assertEquals(key,row.getJSONObject(field).getString("name"))
            }
            assertTrue(row.has("previous_target") && row.isNull("previous_target"))
            assertTrue(row.has("previous_attributes") && row.isNull("previous_attributes"))
            val target=row.getString("target").removeSurrounding("\"").replace("\\'","'").replace("\\\"","\"").replace("\\n","\n")
            assertEquals(target,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteMiSmRwAdditionsRejectSourceAttributesAndPredecessorCorruption() {
        for(tag in listOf("mi","sm","rw")) for(mutation in listOf("source","source_attributes","previous_target","previous_attributes","attributes","display","target","alreadyPresent","missing_previous_target","missing_previous_attributes","coordinated_target_display")) {
            val data=miSmRwExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject("string/save20_unsupported_image_colour")
            when(mutation) {
                "coordinated_target_display" -> {row.put("target","\"forged\"");row.put("display","forged")}
                "source_attributes","attributes" -> row.getJSONObject(mutation).put("formatted","false")
                "alreadyPresent" -> expected.put(tag,"forged")
                "missing_previous_target","missing_previous_attributes" -> row.remove(mutation.removePrefix("missing_"))
                else -> row.put(mutation,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) {addMiSmRw(expected,data)}
        }
    }

    private fun kabMwwMaiBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/kabyle_hmong_daw_maithili_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite KAB/MWW/MAI reviewed fixture", "5c1d98d2398a4e1ae7b7cdf20262bc48218598740580298fd2ab8279d9f05950", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun kabMwwMaiSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) kabMwwMaiSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) kabMwwMaiSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun kabMwwMaiExpectations() = kabMwwMaiBoundFixture()

    private fun addKabMwwMai(expected: JSONObject, reviewed: JSONObject) {
        kabMwwMaiSameJson(kabMwwMaiBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        val source=reviewed.getJSONObject("sources").getJSONObject(key)
        assertEquals("string",source.getString("type"))
        assertEquals(neutral,source.getString("source"))
        assertEquals(setOf("name"),source.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals(key,source.getJSONObject("attributes").getString("name"))
        for(tag in listOf("kab","mww","mai")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject("locales").getJSONObject(tag)
            assertFalse("Historical resource must be absent $tag",row.getJSONObject("predecessors").has(key))
            assertTrue("Must be an explicit changed value $tag",(0 until row.getJSONArray("changed").length()).any {
                row.getJSONArray("changed").getString(it)==key })
            assertFalse("Exact name-only target attributes $tag",row.getJSONObject("target_attribute_exceptions").has(key))
            val raw=row.getJSONObject("accepted").getString(key)
            assertTrue(raw.isNotEmpty());assertFalse(raw.startsWith("@"))
            val display=Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            expected.put(tag,display)
        }
    }

    @Test fun finiteKabMwwMaiAdditionRejectsSourceAttributesAndPredecessorCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("kab","mww","mai")) for(mutation in listOf("source","sourceAttributes","sourceType","previous","attributes","changed","empty","nonemptyTarget","coordinatedSourceTarget","alreadyPresent")) {
            val data=kabMwwMaiExpectations();val expected=JSONObject()
            val source=data.getJSONObject("sources").getJSONObject(key)
            val row=data.getJSONObject("locales").getJSONObject(tag)
            when(mutation) {
                "source" -> source.put("source","forged")
                "sourceAttributes" -> source.getJSONObject("attributes").put("formatted","false")
                "sourceType" -> source.put("type","plurals")
                "previous" -> row.getJSONObject("predecessors").put(key,"forged")
                "attributes" -> row.getJSONObject("target_attribute_exceptions").put(key,JSONObject().put("name",key).put("formatted","false"))
                "changed" -> row.put("changed",org.json.JSONArray())
                "empty" -> row.getJSONObject("accepted").put(key,"")
                "nonemptyTarget" -> row.getJSONObject("accepted").put(key,"forged target")
                "coordinatedSourceTarget" -> {source.put("source","forged source");row.getJSONObject("accepted").put(key,"forged target")}
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addKabMwwMai(expected,data) }
        }
    }

    private fun euFyUzBoundFixture(tag: String): JSONObject {
        val expected=mapOf("eu-ES" to "f8ac4b2651c28c054246727316ba971f95b344b6c5eac44619f11ba90b7b0df3", "fy" to "76efeb2aa73b0e5944c6d06a8c9e8d2a1dc4dc87b5bf06829c7b81c569cdf5da", "uz-Latn" to "af7c285c390e5ea7fdb09c8f7bb18bc97f4e67f87228bc554521d0782d94a029")
        val bytes=File("../tools/fixtures/current_localization/basque_frisian_uzbek_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun euFyUzSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) euFyUzSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) euFyUzSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun euFyUzExpectations()=JSONObject().apply {
        for(tag in listOf("eu-ES","fy","uz-Latn")) put(tag,euFyUzBoundFixture(tag))
    }

    private fun addEuFyUz(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=euFyUzExpectations()
        for(tag in listOf("eu-ES","fy","uz-Latn")) {
            euFyUzSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            assertTrue(raw.startsWith("\"") && raw.endsWith("\""))
            assertFalse(raw.substring(1,raw.length-1).contains('\\'))
            assertEquals(raw.substring(1,raw.length-1),row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteEuFyUzAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("eu-ES","fy","uz-Latn")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=euFyUzExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addEuFyUz(expected,data) }
        }
    }

    private fun boundSoWoHtFixture(bytes: ByteArray = File("../tools/fixtures/current_localization/somali_wolof_haitian_creole_priority_wording.json").readBytes()): JSONObject {
        val digest = java.security.MessageDigest.getInstance("SHA-256").digest(bytes)
            .joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical Somali/Wolof/Haitian Creole fixture", "cbd9e458561e044f52f6c5c4622574b3f27e72dd50a1b04ec26c3d45494fb836", digest)
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

    private fun kkTgPsBoundFixture(tag: String): JSONObject {
        val expected=mapOf("kk" to "90e829ec8eb3bdf492a8616287a48fa4e261252e920beef4636d750cb28f2137", "tg" to "80753300ee2423eecf383f14c76a7f77d4cb17fb4c3b53226c4cc717c78782bb", "ps" to "5703f57937a040db53e3b75075b3859022bbfa31ff44aad797213707f73b4077")
        val bytes=File("../tools/fixtures/current_localization/kazakh_tajik_pashto_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun kkTgPsSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) kkTgPsSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) kkTgPsSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun kkTgPsExpectations()=JSONObject().apply {
        for(tag in listOf("kk","tg","ps")) put(tag,kkTgPsBoundFixture(tag))
    }

    private fun addKkTgPs(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=kkTgPsExpectations()
        for(tag in listOf("kk","tg","ps")) {
            kkTgPsSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            assertTrue(raw.startsWith("\"") && raw.endsWith("\""))
            assertFalse(raw.substring(1,raw.length-1).contains('\\'))
            assertEquals(raw.substring(1,raw.length-1),row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteKkTgPsAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("kk","tg","ps")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=kkTgPsExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addKkTgPs(expected,data) }
        }
    }

    private fun cebNdsCsbBoundFixture(tag: String): JSONObject {
        val expected=mapOf("nds" to "31a3ec04ad9d5baddbb2bf60e2d40f69a7ab3d1b8876f8675ef97c35f99ac725", "csb" to "02e92485a16550eb8a975006ef143df21d9b441665f7bad2ff88b61bf13fe5fd")
        val bytes=File("../tools/fixtures/current_localization/cebuano_low_german_kashubian_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun cebNdsCsbSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) cebNdsCsbSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) cebNdsCsbSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun cebNdsCsbExpectations()=JSONObject().apply {
        for(tag in listOf("nds","csb")) put(tag,cebNdsCsbBoundFixture(tag))
    }

    private fun addCebNdsCsb(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=cebNdsCsbExpectations()
        for(tag in listOf("nds","csb")) {
            cebNdsCsbSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            val unquoted=if(raw.startsWith("\"") && raw.endsWith("\"")) raw.substring(1,raw.length-1) else Regex("\\s+").replace(raw," ").trim()
            val decoded=Regex("""\\(.)""").replace(unquoted) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            assertEquals(decoded,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteCebNdsCsbAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("nds","csb")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=cebNdsCsbExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addCebNdsCsb(expected,data) }
        }
    }

    private fun waSeSaBoundFixture(tag: String): JSONObject {
        val expected=mapOf("wa" to "f243c1efa767fc09f8ca5a777948319c4047003cf0af39b575244985bbef9e3c", "se" to "9fb78e8e98c3b9a3a2b94cec9459665e6cc004d722a76c908bdc4d3a188c8459", "sa" to "bc093ed9d6a6b699ce72d434a36faa435c31b91abe2ca287ef0d39c659047446")
        val bytes=File("../tools/fixtures/current_localization/walloon_northern_sami_sanskrit_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun waSeSaSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) waSeSaSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) waSeSaSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun waSeSaExpectations()=JSONObject().apply {
        for(tag in listOf("wa","se","sa")) put(tag,waSeSaBoundFixture(tag))
    }

    private fun addWaSeSa(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=waSeSaExpectations()
        for(tag in listOf("wa","se","sa")) {
            waSeSaSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            val unquoted=if(raw.startsWith("\"") && raw.endsWith("\"")) raw.substring(1,raw.length-1) else Regex("\\s+").replace(raw," ").trim()
            val decoded=Regex("""\\(.)""").replace(unquoted) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            assertEquals(decoded,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteWaSeSaAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("wa","se","sa")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=waSeSaExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addWaSeSa(expected,data) }
        }
    }

    private fun sdPcmTpiBoundFixture(tag: String): JSONObject {
        val expected=mapOf("sd" to "e4ee8b86958733647c2c99d6a9584c0bc359ad518a70fa50bb74b8cd064ca815", "pcm" to "7420157c4b55993d389992d499e61f954088f9f4dbcc64ea526aa21d27fb836c", "tpi" to "8755958e111d5f9cdd2720aeb1a178106e46cae0029771a115417cc4ded87385")
        val bytes=File("../tools/fixtures/current_localization/sindhi_nigerian_pidgin_tok_pisin_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun sdPcmTpiSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) sdPcmTpiSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) sdPcmTpiSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun sdPcmTpiExpectations()=JSONObject().apply {
        for(tag in listOf("sd","pcm","tpi")) put(tag,sdPcmTpiBoundFixture(tag))
    }

    private fun addSdPcmTpi(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=sdPcmTpiExpectations()
        for(tag in listOf("sd","pcm","tpi")) {
            sdPcmTpiSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            assertFalse(raw.startsWith("\"") || raw.endsWith("\""))
            assertFalse(raw.contains('\\'))
            assertEquals(raw,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteSdPcmTpiAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("sd","pcm","tpi")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=sdPcmTpiExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addSdPcmTpi(expected,data) }
        }
    }

    private fun ckbUgTtBoundFixture(tag: String): JSONObject {
        val expected=mapOf("ckb" to "a708e9f78a84386a601e1b68d55ac4057cb5a450e7f72577a00b375bd3b0806f", "ug" to "4110353522a52589ea13e1ecc8b471e9fc00e4ce9063812a7708966defa5982c", "tt-Cyrl" to "59878042f6e7bdd383ac5211921f2e5ecd8648059fb1ac0171583130febfcd22")
        val bytes=File("../tools/fixtures/current_localization/sorani_uyghur_tatar_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun ckbUgTtSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) ckbUgTtSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) ckbUgTtSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun ckbUgTtExpectations()=JSONObject().apply {
        for(tag in listOf("ckb","ug","tt-Cyrl")) put(tag,ckbUgTtBoundFixture(tag))
    }

    private fun addCkbUgTt(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=ckbUgTtExpectations()
        for(tag in listOf("ckb","ug","tt-Cyrl")) {
            ckbUgTtSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            assertFalse(raw.startsWith("\"") || raw.endsWith("\""))
            assertFalse(raw.contains('\\'))
            assertEquals(raw,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteCkbUgTtAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("ckb","ug","tt-Cyrl")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=ckbUgTtExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addCkbUgTt(expected,data) }
        }
    }

    private fun aryMnTokBoundFixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/moroccan_arabic_mongolian_toki_pona_priority_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite ARY/MN/TOK reviewed fixture", "02b4dcb288d76cc53c7d50e2e91375cd6aecffbf9a404a3d0a61987e86197f62", actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun aryMnTokSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) aryMnTokSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) aryMnTokSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun aryMnTokExpectations() = aryMnTokBoundFixture()

    private fun addAryMnTok(expected: JSONObject, reviewed: JSONObject) {
        aryMnTokSameJson(aryMnTokBoundFixture(),reviewed)
        val key="save20_unsupported_image_colour"
        val source=reviewed.getJSONObject("sources").getJSONObject(key)
        assertEquals("string",source.getString("type"))
        assertEquals(neutral,source.getString("source"))
        assertEquals(setOf("name"),source.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals(key,source.getJSONObject("attributes").getString("name"))
        for(tag in listOf("ary","tok")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject("locales").getJSONObject(tag)
            assertFalse("Historical resource must be absent $tag",row.getJSONObject("predecessors").has(key))
            assertTrue("Must be an explicit changed value $tag",(0 until row.getJSONArray("changed").length()).any {
                row.getJSONArray("changed").getString(it)==key })
            assertFalse("Exact name-only target attributes $tag",row.getJSONObject("target_attribute_exceptions").has(key))
            val raw=row.getJSONObject("accepted").getString(key)
            assertTrue(raw.isNotEmpty());assertFalse(raw.startsWith("@"))
            val display=Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            expected.put(tag,display)
        }
    }

    @Test fun finiteAryMnTokAdditionRejectsSourceAttributesAndPredecessorCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("ary","tok")) for(mutation in listOf("source","sourceAttributes","sourceType","previous","attributes","changed","empty","nonemptyTarget","coordinatedSourceTarget","alreadyPresent")) {
            val data=aryMnTokExpectations();val expected=JSONObject()
            val source=data.getJSONObject("sources").getJSONObject(key)
            val row=data.getJSONObject("locales").getJSONObject(tag)
            when(mutation) {
                "source" -> source.put("source","forged")
                "sourceAttributes" -> source.getJSONObject("attributes").put("formatted","false")
                "sourceType" -> source.put("type","plurals")
                "previous" -> row.getJSONObject("predecessors").put(key,"forged")
                "attributes" -> row.getJSONObject("target_attribute_exceptions").put(key,JSONObject().put("name",key).put("formatted","false"))
                "changed" -> row.put("changed",org.json.JSONArray())
                "empty" -> row.getJSONObject("accepted").put(key,"")
                "nonemptyTarget" -> row.getJSONObject("accepted").put(key,"forged target")
                "coordinatedSourceTarget" -> {source.put("source","forged source");row.getJSONObject("accepted").put(key,"forged target")}
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addAryMnTok(expected,data) }
        }
    }

    private fun boDzValBoundFixture(tag: String): JSONObject {
        val expected=mapOf("ca-ES-valencia" to "79efe19b460ef7b3c8be720a601e7940276daffb91815231fdc9944005f22f36")
        val bytes=File("../tools/fixtures/current_localization/tibetan_dzongkha_valencian_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun boDzValSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) boDzValSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) boDzValSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun boDzValExpectations()=JSONObject().apply {
        for(tag in listOf("ca-ES-valencia")) put(tag,boDzValBoundFixture(tag))
    }

    private fun addBoDzVal(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=boDzValExpectations()
        for(tag in listOf("ca-ES-valencia")) {
            boDzValSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            val unquoted=if(raw.startsWith("\"") && raw.endsWith("\"")) raw.substring(1,raw.length-1) else Regex("\\s+").replace(raw," ").trim()
            val decoded=Regex("""\\(.)""").replace(unquoted) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            assertEquals(decoded,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteBoDzValAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("ca-ES-valencia")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=boDzValExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addBoDzVal(expected,data) }
        }
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

    private fun hneYiHkBoundFixture(tag: String): JSONObject {
        val expected=mapOf("hne" to "6679246bf3864d50be47df816468d269abc03ee3de2e3ff5c490cdeab89ecba0", "yi" to "c67c7042dfeacbc046da732086eb704c154cac801b6373e95a3e93661c9f6433")
        val bytes=File("../tools/fixtures/current_localization/chhattisgarhi_yiddish_hong_kong_priority_wording/$tag.json").readBytes()
        val digest=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete canonical fixture $tag",expected.getValue(tag),digest)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }

    private fun hneYiHkSameJson(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) hneYiHkSameJson(expected.get(key),other.get(key))
            }
            is org.json.JSONArray -> {
                assertTrue(actual is org.json.JSONArray);val other=actual as org.json.JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) hneYiHkSameJson(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }

    private fun hneYiHkExpectations()=JSONObject().apply {
        for(tag in listOf("hne","yi")) put(tag,hneYiHkBoundFixture(tag))
    }

    private fun addHneYiHk(expected: JSONObject, reviewed: JSONObject) {
        val key="save20_unsupported_image_colour"
        val canonical=hneYiHkExpectations()
        for(tag in listOf("hne","yi")) {
            hneYiHkSameJson(canonical.getJSONObject(tag),reviewed.getJSONObject(tag))
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val row=reviewed.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            assertTrue("Explicit absent predecessor $tag",row.has("previous_target") && row.isNull("previous_target"))
            assertEquals("string",row.getString("type"))
            val source=row.getJSONObject("source")
            assertEquals(setOf("value","attributes"),source.keys().asSequence().toSet())
            assertEquals(neutral,source.getString("value"))
            for(attributes in listOf(source.getJSONObject("attributes"),row.getJSONObject("reviewed_attributes"))) {
                assertEquals(setOf("name"),attributes.keys().asSequence().toSet())
                assertEquals(key,attributes.getString("name"))
            }
            val raw=row.getString("reviewed_value")
            val unquoted=if(raw.startsWith("\"") && raw.endsWith("\"")) raw.substring(1,raw.length-1) else Regex("\\s+").replace(raw," ").trim()
            val decoded=Regex("""\\(.)""").replace(unquoted) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
            assertEquals(decoded,row.getString("display"))
            expected.put(tag,row.getString("display"))
        }
    }

    @Test fun finiteHneYiHkAdditionRejectsMissingHistorySourceAttributesAndDisplayCorruption() {
        val key="save20_unsupported_image_colour"
        for(tag in listOf("hne","yi")) for(mutation in listOf("source","sourceAttributes","missingPrevious","previous","attributes","display","raw","alreadyPresent","type","coordinated")) {
            val data=hneYiHkExpectations();val expected=JSONObject()
            val row=data.getJSONObject(tag).getJSONObject("values").getJSONObject(key)
            when(mutation) {
                "type" -> row.put("type","plurals")
                "coordinated" -> { row.put("reviewed_value","\"forged\"");row.put("display","forged") }
                "source" -> row.getJSONObject("source").put("value","forged")
                "sourceAttributes" -> row.getJSONObject("source").getJSONObject("attributes").put("formatted","false")
                "missingPrevious" -> row.remove("previous_target")
                "previous" -> row.put("previous_target","forged")
                "attributes" -> row.getJSONObject("reviewed_attributes").put("formatted","false")
                "display" -> row.put("display","forged")
                "raw" -> row.put("reviewed_value","forged")
                "alreadyPresent" -> expected.put(tag,"forged")
            }
            assertThrows("$tag/$mutation",AssertionError::class.java) { addHneYiHk(expected,data) }
        }
    }

    @Test fun everyOfferedLanguageResolvesItsScopedMessageOrExplicitEnglishFallback() {
        // This family has 59 baseline catalogues plus reviewed Amharic/Czech/Polish/Swedish/Bulgarian/Bengali/Nynorsk/Danish/Norwegian/Catalan/Romanian/Slovak/Slovenian/Serbian Cyrillic/Serbian Latin values.
        // Global review scope is unchanged. The Valencian option inherits the ca resource;
        // this is routing evidence, not an independently reviewed Valencian value.
        val expected = javaClass.getResourceAsStream("/tagged-colour/expected.json")!!
            .bufferedReader().use { JSONObject(it.readText()) }
        assertFalse(expected.has("uk"))
        expected.put("uk", PriorityWordingExpectations.display("uk","save20_unsupported_image_colour"))
        // Current XML owns wording for these catalogues. Historical approval
        // checkpoints are in source history, not a second active text oracle.
        val currentCatalogues = setOf("mr","ta","te","kn","ml-IN","ne","pa-IN",
            "as","km","lo","jv","su","ky","ha","ig","ln","yo","zu","xh")
        addGaGdCy(expected,gaGdCyExpectations())
        addEuFyUz(expected,euFyUzExpectations())
        addKaHyAz(expected,kaHyAzExpectations())
        addGalician(expected,glNlDeExpectations())
        addSoWoHt(expected,soWoHtExpectations())
        addKkTgPs(expected,kkTgPsExpectations())
        addBrAstOc(expected,brAstOcExpectations())
        addCebNdsCsb(expected,cebNdsCsbExpectations())
        addIaLaKu(expected,iaLaKuExpectations())
        addMiSmRw(expected,miSmRwExpectations())
        addWaSeSa(expected,waSeSaExpectations())
        addKabMwwMai(expected,kabMwwMaiExpectations())
        addSdPcmTpi(expected,sdPcmTpiExpectations())
        addCkbUgTt(expected,ckbUgTtExpectations())
        addAryMnTok(expected,aryMnTokExpectations())
        addBoDzVal(expected,boDzValExpectations())
        addHneYiHk(expected,hneYiHkExpectations())
        addExactScript(expected,exactScriptExpectations())
        assertTrue(expected.has("bg")); assertTrue(expected.has("bn")); assertTrue(expected.has("nn"))
        assertTrue(expected.has("da")); assertTrue(expected.has("no"))
        assertTrue(expected.has("ca")); assertTrue(expected.has("ro"))
        assertTrue(expected.has("sk")); assertTrue(expected.has("sl"))
        assertTrue(expected.has("sr-Cyrl")); assertTrue(expected.has("sr-Latn"))
        assertTrue(expected.has("hr")); assertTrue(expected.has("bs"))
        assertTrue(expected.has("am")); assertTrue(expected.has("cs")); assertTrue(expected.has("pl")); assertTrue(expected.has("sv"))
        assertEquals(171, AppLanguage.tags(context).size)
        val historicalInheritedCatalogues = mapOf("ca-ES-valencia" to "ca")
        assertEquals("ca", historicalInheritedCatalogues["ca-ES-valencia"])
        val inheritedCatalogues = historicalInheritedCatalogues.filterKeys { it != "ca-ES-valencia" } + mapOf("fa-IR" to "fa")
        assertEquals(mapOf("fa-IR" to "fa"),inheritedCatalogues)
        assertTrue(inheritedCatalogues.keys.none { expected.has(it) })
        val exactScriptStageTags = expected.keys().asSequence().toSet()
        val nordic=JSONObject(File("../tools/fixtures/current_localization/nordic_priority_wording.json").readText())
        val nordicKey="save20_unsupported_image_colour"
        assertEquals(neutral,nordic.getJSONObject("sources").getJSONObject(nordicKey).getString("source"))
        assertFalse(expected.has("is"))
        assertFalse(nordic.getJSONObject("locales").getJSONObject("is").getJSONObject("predecessors").has(nordicKey))
        expected.put("is",NordicPriorityExpectations.display("is",nordicKey))
        val recovered=JSONObject(File("../tools/fixtures/current_localization/nynorsk_belarusian_albanian_priority_wording.json").readText())
        val recoveredKey="save20_unsupported_image_colour"
        assertEquals(neutral,recovered.getJSONObject("sources").getJSONObject("string/$recoveredKey").getString("source"))
        for(tag in listOf("be","sq")) {
            assertFalse(expected.has(tag))
            assertFalse(recovered.getJSONObject("locales").getJSONObject(tag).getJSONObject("predecessors").has("string/$recoveredKey"))
            expected.put(tag,RecoveredTrioPriorityExpectations.display(tag,recoveredKey))
        }
        val macedonian=JSONObject(File("../tools/fixtures/current_localization/croatian_bosnian_macedonian_priority_wording.json").readText())
            .getJSONObject("locales").getJSONObject("mk").getJSONObject("values").getJSONObject("save20_unsupported_image_colour")
        assertFalse(expected.has("mk"))
        assertTrue(macedonian.has("previous") && macedonian.isNull("previous"))
        assertEquals(neutral,macedonian.getString("source"))
        assertEquals(setOf("name"),macedonian.getJSONObject("attributes").keys().asSequence().toSet())
        assertEquals("save20_unsupported_image_colour",macedonian.getJSONObject("attributes").getString("name"))
        assertEquals(macedonian.getString("target").removeSurrounding("\""),macedonian.getString("display"))
        expected.put("mk",macedonian.getString("display"))
        // Finite recovered HI/GU additions after all existing checkpoints.
        HiGuPriorityExpectations.addTagged(expected,HiGuPriorityExpectations.fixture())
        ThaiPriorityExpectations.addTagged(expected,ThaiPriorityExpectations.fixture())
        // The five candidates add this disjoint union, not five standalone totals.
        val combinedAddedTags = setOf("is", "hi", "gu", "be", "sq", "th", "mk")
        assertEquals(7, combinedAddedTags.size)
        assertTrue(combinedAddedTags.intersect(exactScriptStageTags).isEmpty())
        assertEquals(exactScriptStageTags + combinedAddedTags, expected.keys().asSequence().toSet())
        PersianHebrewUrduPriorityExpectations.addTagged(expected,PersianHebrewUrduPriorityExpectations.fixture())
        assertEquals(exactScriptStageTags + combinedAddedTags + setOf("fa","he","ur"), expected.keys().asSequence().toSet())
        assertFalse(expected.has("fa-IR")) // no regional direct wording acceptance
        SinhalaBurmeseZhuangPriorityExpectations.addTagged(expected,SinhalaBurmeseZhuangPriorityExpectations.fixture())
        assertEquals(exactScriptStageTags + combinedAddedTags + setOf("fa","he","ur","si","my"), expected.keys().asSequence().toSet())
        val expectedFallbacks = AppLanguage.tags(context).size - expected.length() - inheritedCatalogues.size - currentCatalogues.size
        assertEquals(17, expectedFallbacks)
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
            if (tag in currentCatalogues) continue // Semantic assertions above still run.
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
        assertEquals(expectedFallbacks, fallbacks) // Current-catalogue semantics, frozen remaining values and explicit parent routing are disjoint.
    }
}
