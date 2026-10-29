/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import java.io.File

/** Finite delta/context binding. Retained context does not acquire linguistic acceptance. */
internal object SerbianPriorityDeltaExpectations {
    fun fixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/serbian_priority_delta_wording.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes)
            .joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Finite Serbian delta/context fixture", "c4805743cc2dcc04c6a0bea1fa28fbd7e323876dbc6d51f967a42206c22ed876",actual)
        return JSONObject(String(bytes,Charsets.UTF_8))
    }
    fun same(expected: Any?, actual: Any?) {
        when(expected) {
            is JSONObject -> {
                assertTrue(actual is JSONObject);val other=actual as JSONObject
                assertEquals(expected.keys().asSequence().toSet(),other.keys().asSequence().toSet())
                for(key in expected.keys()) same(expected.get(key),other.get(key))
            }
            is JSONArray -> {
                assertTrue(actual is JSONArray);val other=actual as JSONArray
                assertEquals(expected.length(),other.length())
                for(i in 0 until expected.length()) same(expected.get(i),other.get(i))
            }
            else -> assertEquals(expected,actual)
        }
    }
    fun row(data: JSONObject,tag: String,key: String): JSONObject {
        same(fixture(),data)
        val locale=data.getJSONObject("locales").getJSONObject(tag)
        val row=locale.getJSONObject("values").optJSONObject(key) ?: locale.getJSONObject("context").getJSONObject(key)
        return JSONObject(row.toString())
    }
}
