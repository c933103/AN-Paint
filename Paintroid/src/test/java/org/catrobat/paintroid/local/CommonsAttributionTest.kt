/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.content.Context
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.catrobat.paintroid.R
import java.util.Locale
import org.catrobat.paintroid.classic.CommonsAttribution
import org.catrobat.paintroid.classic.CreditEditContext
import org.catrobat.paintroid.classic.CreditEditSession
import org.catrobat.paintroid.classic.GalleryCredits
import org.catrobat.paintroid.classic.ImageCredit
import org.catrobat.paintroid.classic.ImageCreditArchive
import org.catrobat.paintroid.classic.IllustrationSource
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.IOException
import java.io.File
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
    private fun withLanguage(tag: String,check: ()->Unit) {
        val previousTag=AppLanguage.selectedTag(context)
        val previousLocale=Locale.getDefault()
        val previousResources=PaintApplication.currentResources
        try {
            AppLanguage.select(context,tag)
            PaintApplication.currentResources=AppLanguage.wrap(context).resources
            check()
        } finally {
            AppLanguage.select(context,previousTag)
            PaintApplication.currentResources=previousResources
            Locale.setDefault(previousLocale)
        }
    }
    @Test fun importedNotesUseWholeLocalizedMessagesAndLeaveProviderValuesUntouched() = withLanguage("fr") {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        val metadataOnly=record.text(false)
        val imported=record.text(true)
        val expected="AN Paint: SVG → PNG; taille d’origine; antiAlias=false; strokeDashArray=none; background=#FFFFFF."
        assertEquals(1,imported.lines().count {it==expected})
        assertEquals(metadataOnly,imported.lines().filterNot {it==expected}.joinToString("\n"))
        for((key,value) in record.metadata.filterKeys {it!="ObjectName"}.filterValues {it.isNotBlank()}) {
            assertTrue("Provider field $key must remain verbatim",imported.contains("$key: $value"))
        }
        assertEquals(source,record.source);assertEquals(page,record.page)
        CommonsAttribution.cache(context,record)
        assertEquals(record,CommonsAttribution.cached(context,source))
    }
    @Test fun svgNoteClassificationUsesCaseInsensitiveUriPathNotQueryOrFragment() = withLanguage("en-US") {
        val metadata=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source).metadata
        for((url,svg) in listOf(source to true,source.replace(".svg",".SVG?download=1#preview") to true,
            source.replace(".svg",".png?name=file.svg#file.svg") to false,source.replace(".svg",".svg.png") to false)) {
            val record=CommonsAttribution.Record(url,page,"Map",metadata)
            val expected=PaintApplication.currentResources.getString(if(svg) R.string.commons_import_svg_changes
                else R.string.commons_import_raster_changes)
            val unexpected=PaintApplication.currentResources.getString(if(svg) R.string.commons_import_raster_changes
                else R.string.commons_import_svg_changes)
            assertEquals(1,record.text(true).lines().count {it==expected})
            assertFalse(record.text(true).lines().contains(unexpected))
            assertFalse(record.text(false).lines().any {it==expected || it==unexpected})
        }
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
    @Test fun metadataSnapshotDoesNotClaimInsertionOrOverwriteDocumentCreditEdits() {
        val record=CommonsAttribution.parse(CommonsTestMetadata.response(source,page),source)
        val folder=File(context.filesDir,"commons-credit-${java.util.UUID.randomUUID()}").apply {mkdirs()}
        var retained: String?=null
        try {
            val empty=CreditEditSession.create(folder,emptyList(),CreditEditContext.ledgerOnly(emptyList()))
            CommonsAttribution.cache(context,record)
            assertTrue(CreditEditSession.open(folder,empty.token).credits.isEmpty())
            val original=ImageCredit(source,record.text(true))
            val session=CreditEditSession.create(folder,listOf(original),CreditEditContext.ledgerOnly(listOf(original)))
            assertEquals(record.text(true),ImageCredit.text(session.credits))
            val edited="Edited attribution\nÉmilie · かな\n"+record.text(true)
            session.edit(source,edited) {ImageCreditArchive.retainAccepted(context,it).also {token ->retained=token}}
            CommonsAttribution.cache(context,CommonsAttribution.parse(CommonsTestMetadata.response(source,page,"Updated Mapper"),source))
            withLanguage("ja") {
                val reopened=CreditEditSession.open(folder,session.token)
                assertEquals(listOf(original.copy(text=edited)),reopened.credits)
                assertEquals(edited,ImageCredit.text(reopened.credits));assertEquals(listOf(source),reopened.credits.map {it.source})
                assertTrue(reopened.accepted);assertTrue(CreditEditSession.open(folder,empty.token).credits.isEmpty())
            }
        } finally {retained?.let {ImageCreditArchive.releaseAccepted(context,it)};folder.deleteRecursively()}
    }
    @Test fun commonsFallbackNeverInventsTheLicenceOfAnotherGallery() {
        val text=GalleryCredits.credit(source,"Test map",IllustrationSource.COMMONS,page)
        assertTrue(text.contains(source));assertTrue(text.contains(page));assertTrue(text.contains("Wikimedia Commons"))
        for(invented in listOf("CC0",GalleryCredits.CC_BY_SA,"Irasutoya","Openclipart"))
            assertFalse("Invented Commons attribution: $invented",text.contains(invented))
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
