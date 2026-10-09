/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.json.JSONArray
import org.json.JSONObject

/** Local provider fixture: no network requests to Wikimedia in automated tests. */
internal object CommonsTestMetadata {
    fun response(source: String,page: String,artist: String="Mapper A"): String {
        val metadata=JSONObject()
        fun field(name: String,value: String) {metadata.put(name,JSONObject().put("value",value))}
        field("ObjectName","Test blank map")
        field("Artist","<a href=\"/wiki/User:Mapper_A\">$artist</a> and <a href=\"https://example.org/mapper\">Mapper B</a>")
        field("Credit","Derived from <a href=\"https://example.org/original-map\">earlier map</a>")
        field("Attribution","Required attribution wording &amp; acknowledgement")
        field("LicenseShortName","CC BY-SA 3.0")
        field("LicenseUrl","https://creativecommons.org/licenses/by-sa/3.0/")
        field("UsageTerms","Creative Commons Attribution-ShareAlike 3.0")
        field("Permission","Retain the authors and original source credit.")
        field("Copyrighted","True");field("AttributionRequired","True")
        val image=JSONObject().put("url",source).put("descriptionurl",page).put("extmetadata",metadata)
        val item=JSONObject().put("ns",6).put("title","File:Test_map.svg").put("imageinfo",JSONArray().put(image))
        return JSONObject().put("query",JSONObject().put("pages",JSONArray().put(item))).toString()
    }
}
