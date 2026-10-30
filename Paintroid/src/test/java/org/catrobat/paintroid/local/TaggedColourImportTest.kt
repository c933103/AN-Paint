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
        val expected=mapOf("eu-ES" to "35e92a9d308dead05df3d598c691b5b6f46198c18187cc0ebb9bc9403598fa28", "fy" to "646c0baf4a6099f620999d51d1c6da4e67a172eb1b13d3fe37944d8541e36e8b", "uz-Latn" to "346a56385a885c7752399e35bcc195e7f699f569b802305298d4ef2929a3d1d6")
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
        val expected=mapOf("kk" to "53eee9ab1e76ed7eab5c74cffce092a95426fa0cda62c5d28bcf7c63708c0578", "tg" to "8e751faa510cd5cc1e0b01ad7cd8938a1b8ec1be7741276ab8e2f11d3e9f05cd", "ps" to "23e7480ba0ad5942811b29ba870770167cab010fe9492a1c53d31871ab7cb30a")
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
        val expected=mapOf("nds" to "04089cc46e005b1bfa57bf0977190380a9bd8874dcb89ee90e18e6a3a7888899", "csb" to "7a650c37feacd8d94fb29be36fb092da15ab7e7a1a54453dc1701f0f649db629")
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
        val expected=mapOf("wa" to "0adeaf807567246df6591a73d14f94a95f95a0415bac15524a745dbfa52e7974", "se" to "8dd76c550d6b13c527538a05b3672251544cae1d3f011fc66471f7b714da715b", "sa" to "cba05cbbbb8d3abf72a814949277f6dc708bfbcc4c3b2cbda6f136d0958795b7")
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
        val expected=mapOf("sd" to "f840cd827e87041fc42ef8ae5b4b748b860ca62262e79952307dd89b48f28076", "pcm" to "93c36a02dec7c0e1a4e29fbe510077e86fe082dd264c72bca27db764e7aff595", "tpi" to "8f35d511a03521cf92d8f035b1c9cc5548dd7c9abfb0f21234934484e3ab3f11")
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
        val expected=mapOf("ckb" to "272560d87a77afd5d1dd144d299ee86a8d8b3e79a1770b90bea3b634627be65f", "ug" to "a8c128eead2b04cb88a6324068cb2a127a2c2ca076f51fb3c372f6f391ac3bab", "tt-Cyrl" to "bf6e296497aa10dd5f53cd02be0c072c4733b831f134313b96db5752694ff73f")
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
        val expected=mapOf("ca-ES-valencia" to "2637add2d84343eee373372b9b07949d8908b5498b86c56bc13ea2785af2a7e7")
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
        val expected=mapOf("hne" to "f8b8c8231e57836acffd62019573ce74d966c7c89e878484704f5e07b5c19640", "yi" to "15ff376fa0f3893632e40fce7da4d96d886fb53f42e34e89ec080d04429445ff")
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
        addGaGdCy(expected,gaGdCyExpectations())
        assertEquals(99,expected.length())
        addEuFyUz(expected,euFyUzExpectations())
        assertEquals(102,expected.length())
        addKaHyAz(expected,kaHyAzExpectations())
        assertEquals(105, expected.length())
        addGalician(expected,glNlDeExpectations())
        assertEquals(106, expected.length())
        addSoWoHt(expected,soWoHtExpectations())
        assertEquals(109, expected.length())
        addKkTgPs(expected,kkTgPsExpectations())
        assertEquals(112, expected.length())
        addBrAstOc(expected,brAstOcExpectations())
        assertEquals(115, expected.length())
        addCebNdsCsb(expected,cebNdsCsbExpectations())
        assertEquals(117, expected.length())
        addIaLaKu(expected,iaLaKuExpectations())
        assertEquals(120, expected.length())
        addMiSmRw(expected,miSmRwExpectations())
        assertEquals(123, expected.length())
        addWaSeSa(expected,waSeSaExpectations())
        assertEquals(126, expected.length())
        addKabMwwMai(expected,kabMwwMaiExpectations())
        assertEquals(129, expected.length())
        addSdPcmTpi(expected,sdPcmTpiExpectations())
        assertEquals(132, expected.length())
        addCkbUgTt(expected,ckbUgTtExpectations())
        assertEquals(135, expected.length())
        addAryMnTok(expected,aryMnTokExpectations())
        assertEquals(137, expected.length())
        addBoDzVal(expected,boDzValExpectations())
        assertEquals(138, expected.length())
        addHneYiHk(expected,hneYiHkExpectations())
        assertEquals(140, expected.length())
        addExactScript(expected,exactScriptExpectations())
        assertEquals(141, expected.length())
        assertEquals(30, 171 - expected.length()) // exact-script stage, before later reviewed additions
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
        assertEquals(141 + combinedAddedTags.size, expected.length())
        assertEquals(23, 171 - expected.length()) // frozen combined-input stage
        PersianHebrewUrduPriorityExpectations.addTagged(expected,PersianHebrewUrduPriorityExpectations.fixture())
        assertEquals(exactScriptStageTags + combinedAddedTags + setOf("fa","he","ur"), expected.keys().asSequence().toSet())
        assertEquals(151, expected.length())
        assertFalse(expected.has("fa-IR")) // no regional direct wording acceptance
        assertEquals(20, 171 - expected.length()) // direct absences include the parent-inherited option
        assertEquals(19, 171 - expected.length() - inheritedCatalogues.size) // preserved FA/HE/UR runtime checkpoint
        SinhalaBurmeseZhuangPriorityExpectations.addTagged(expected,SinhalaBurmeseZhuangPriorityExpectations.fixture())
        assertEquals(exactScriptStageTags + combinedAddedTags + setOf("fa","he","ur","si","my"), expected.keys().asSequence().toSet())
        assertEquals(153, expected.length())
        val expectedFallbacks = 171 - expected.length() - inheritedCatalogues.size
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
        assertEquals(expectedFallbacks, fallbacks) // 171 offered - 153 direct - 1 explicitly parent-inherited.
    }
}
