/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import org.catrobat.paintroid.classic.CommonsAttribution
import org.catrobat.paintroid.classic.GalleryCredits
import org.catrobat.paintroid.classic.IllustrationSource
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.IOException
import org.json.JSONObject

@RunWith(RobolectricTestRunner::class)
@Config(sdk=[33])
class CommonsAttributionTest {
    private val source="https://upload.wikimedia.org/wikipedia/commons/a/ab/Test_map.svg"
    private val page="https://commons.wikimedia.org/wiki/File:Test_map.svg"
    private val context get()=RuntimeEnvironment.getApplication() as Context
    @Before fun clear() {
        context.getSharedPreferences("image-credits",0).edit().clear().commit()
        context.getSharedPreferences("commons-attribution-v1",0).edit().clear().commit()
    }
    @Test fun keepsCreatorsCreatorLinksLicenceVersionAndCustomAttribution() {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        val text=record.text(false)
        for(expected in listOf("Mapper A","Mapper B","https://commons.wikimedia.org/wiki/User:Mapper_A",
            "https://example.org/mapper","https://example.org/original-map","CC BY-SA 3.0",
            "https://creativecommons.org/licenses/by-sa/3.0/","Required attribution wording & acknowledgement",
            "Retain the authors",page,source)) assertTrue("Missing $expected",text.contains(expected))
        assertFalse(text.contains("CC0"));assertFalse(text.contains("by-sa/4.0"));assertFalse(text.contains("<a"))
        assertFalse(text.contains("antiAlias=false"))
        assertTrue(record.text(true).contains("antiAlias=false"))
    }
    @Test fun rejectsAttributionBelongingToADifferentFile() {
        assertTrue(runCatching {CommonsAttribution.parse(CommonsTestMetadata.response(source.replace("Test_","Other_"),page),source)}
            .exceptionOrNull() is IOException)
    }
    @Test fun acceptsEquivalentPercentEncodedSourceNames() {
        val input=source.replace("Test_map","Test%20map")
        val response=CommonsTestMetadata.response(input,page)
        assertEquals(input.replace("%20"," "),CommonsAttribution.parse(response,input.replace("%20"," ")).source)
    }
    @Test fun absentOrNullMetadataIsNotInventedAsAnAuthorOrLicence() {
        val json=JSONObject(CommonsTestMetadata.response(source,page))
        val metadata=json.getJSONObject("query").getJSONArray("pages").getJSONObject(0)
            .getJSONArray("imageinfo").getJSONObject(0).getJSONObject("extmetadata")
        metadata.put("Artist",JSONObject().put("value",JSONObject.NULL))
        metadata.remove("LicenseShortName");metadata.remove("LicenseUrl")
        val text=CommonsAttribution.parse(json.toString(),source).text(false)
        assertFalse(text.contains("Artist: null"));assertFalse(text.contains("LicenseShortName:"))
        assertFalse(text.contains("CC0"));assertFalse(text.contains("by-sa/4.0"))
    }
    @Test fun unsafeLinksAreNotPreservedOrExecuted() {
        val plain=CommonsAttribution.plain("<a href=\"javascript:alert(1)\">Author</a> <a href=\"//example.org/name\">Name</a>")
        assertTrue(plain.contains("Author"));assertTrue(plain.contains("https://example.org/name"))
        assertFalse(plain.contains("javascript:"));assertFalse(plain.contains("<a"))
    }
    @Test fun snapshotAloneDoesNotClaimAnInsertionAndRememberPreservesUserEdits() {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        CommonsAttribution.cache(context,record)
        assertTrue(GalleryCredits.sources(context).isEmpty())
        GalleryCredits.remember(context,source,IllustrationSource.COMMONS,page,"Test")
        assertEquals(record.text(true),GalleryCredits.text(context))
        val edited="Edited attribution\nÉmilie · かな\n"+record.text(true)
        context.getSharedPreferences("image-credits",0).edit().putString("text:$source",edited).commit()
        CommonsAttribution.cache(context,CommonsAttribution.parse(CommonsTestMetadata.response(source,page,"Updated Mapper"),source))
        GalleryCredits.remember(context,source,IllustrationSource.COMMONS,page,"Test")
        assertEquals(edited,GalleryCredits.text(context));assertEquals(setOf(source),GalleryCredits.sources(context))
    }
    @Test fun sourceMetadataSurvivesReopeningFromPreferences() {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        CommonsAttribution.cache(context,record)
        assertEquals(record,CommonsAttribution.cached(context,source))
        assertNull(CommonsAttribution.cached(context,source.replace("Test_","Other_")))
    }
    @Test fun metadataRequestsSupportIndexFilePagesWithoutBroadQueries() {
        val url=CommonsAttribution.requestUrl("https://commons.wikimedia.org/w/index.php?title=File%3ATest_map.svg&oldid=123")
        val uri=android.net.Uri.parse(url.toString())
        assertEquals("File:Test_map.svg",uri.getQueryParameter("titles"))
        assertEquals("url|extmetadata",uri.getQueryParameter("iiprop"))
        assertEquals("commons.wikimedia.org",uri.host)
        assertTrue(runCatching {CommonsAttribution.requestUrl("https://commons.wikimedia.org/wiki/Category:Blank_maps")}.isFailure)
    }
}
