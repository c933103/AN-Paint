/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local
import org.json.JSONObject
import org.json.JSONArray
import org.junit.Assert.*
import java.io.File

/** Finite reviewed wording fixture, complementary to actual consumer tests. */
internal object RegionalPersianJapaneseFrenchExpectations {
    fun fixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/regional_persian_japanese_french_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Complete finite accepted fa-IR/JA/FR fixture", "61875d4abb3c160d62af8ce4b2812d484f57a15d71abc5d810db6ed4fc649a1d",actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }
    fun display(values: JSONObject, key: String): String {
        val seen=mutableSetOf<String>()
        fun resolve(name: String): String {
            require(seen.add(name)) { "Cyclic resource alias: $name" }
            require(values.has(name) && values.get(name) is String) { "Missing string alias target: $name" }
            val raw=values.getString(name)
            if(raw.startsWith("@string/")) return resolve(raw.removePrefix("@string/"))
            return Regex("""\\(.)""").replace(raw.removeSurrounding("\"")) { token ->
                when(token.groupValues[1]) { "n"->"\n"; "t"->"\t"; "r"->"\r"; else->token.groupValues[1] }
            }
        }
        return resolve(key)
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
    fun requireReviewed(data:JSONObject) {same(fixture(),data)}
}
