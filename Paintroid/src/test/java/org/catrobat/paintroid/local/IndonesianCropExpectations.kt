/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import java.io.File

/** Finite one-correction review binding; retained contexts carry no additional priority credit. */
internal object IndonesianCropExpectations {
    fun fixture(): JSONObject {
        val bytes=File("../tools/fixtures/current_localization/indonesian_crop_followthrough.json").readBytes()
        val actual=java.security.MessageDigest.getInstance("SHA-256").digest(bytes)
            .joinToString("") { "%02x".format(it.toInt() and 0xff) }
        assertEquals("Finite Indonesian crop fixture", "4b9345a8f0c11a706238584870cf97cbd1ccd186200da53ef9d4545e68891805",actual)
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
        val row=locale.getJSONObject(key)
        return JSONObject(row.toString())
    }
}
