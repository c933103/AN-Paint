/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local
import org.json.JSONObject
import org.json.JSONArray
import org.junit.Assert.*
import java.io.File

/** Finite reviewed wording fixture, complementary to actual consumer tests. */
internal object ThaiPriorityExpectations {
    fun fixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/thai_priority_replacement.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite accepted Thai replacement fixture", "0dffad5b3b729fa57da3feb781b9e97edd12e108200f5e4076356cbc1697d1f6",actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }
    fun same(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject); val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) same(expected.get(key),other.get(key))
            }
            is JSONArray -> {
                assertTrue(actual is JSONArray); val other=actual as JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) same(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }
    fun addTagged(expected: JSONObject, data: JSONObject) {
        same(fixture(),data)
        val key="save20_unsupported_image_colour"
        val source=data.getJSONObject("sources").getJSONObject(key)
        assertEquals("This image uses a colour profile that AN Paint cannot convert yet. Convert it to sRGB PNG in a colour-managed editor before importing.",source.getString("value"))
        for(tag in listOf("th")) {
            assertFalse("Already present predecessor $tag",expected.has(tag))
            val locale=data.getJSONObject("locales").getJSONObject(tag)
            assertTrue(locale.getJSONObject("predecessors").isNull(key))
            assertEquals(setOf("name"),locale.getJSONObject("attributes").getJSONObject(key).keys().asSequence().toSet())
            assertEquals(key,locale.getJSONObject("attributes").getJSONObject(key).getString("name"))
            expected.put(tag,locale.getJSONObject("accepted").getString(key).removeSurrounding("\""))
        }
    }
}
