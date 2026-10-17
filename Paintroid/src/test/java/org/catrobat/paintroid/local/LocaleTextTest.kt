/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import org.catrobat.paintroid.classic.LocaleText
import org.junit.Assert.*
import org.junit.Test
import java.util.Locale
import kotlin.random.Random

class LocaleTextTest {
    private fun render(translation: String?, source: String = "Image %1\$s is %2\$d px. Close other documents and try again. The document is unchanged.",
        locale: Locale = Locale.ROOT, vararg args: Any?): String =
        LocaleText.resolve(translation, source, true, locale, args)

    @Test fun explicitPlainSourceContractNeverInterpretsIncidentalPercentSequences() {
        val source="Pixel grid appears at 800% zoom or above. Rulers show positions in image pixels."
        for (text in listOf(source,"100% done", "100% satisfied", "%1\$999999999s", "100% %q", "ᠮᠣᠩᠭᠣᠯ 100%")) {
            assertEquals(text,LocaleText.resolve(text,source,false,Locale.ROOT,emptyArray()))
            assertEquals(text,LocaleText.resolve(text,source,false,Locale.ROOT,arrayOf("ignored")))
        }
        assertEquals(source,LocaleText.resolve(null,source,false,Locale.ROOT,emptyArray()))
    }

    @Test fun malformedTemplatesFallBackToTheCompleteSourceWarning() {
        val source = "Image %1\$s is %2\$d px. Close other documents and try again. The document is unchanged."
        val expected = String.format(Locale.ROOT,source,"drawing.png",17)
        val invalid = listOf(null,"", " \n\t", "%", "%q", "%1\$d %2\$s", "%1\$s", "%2\$d %2\$d",
            "%0\$s %2\$d", "%999999999999999999999999999\$s %2\$d", "%3\$s %2\$d", "%1\$s %2\$999999999d",
            "%1\$s %2\$.999999999999f", "%1\$s %2\$-d", "%1\$s %2\$d %", "%1\$s %2\$d 100% ready",
            "%1\$s %2\$d".repeat(1000), "x".repeat(LocaleText.MAX_TEMPLATE_LENGTH+1))
        for (translation in invalid) assertEquals(translation?.take(100),expected,render(translation,source,Locale.ROOT,"drawing.png",17))
    }

    @Test fun reorderedValuesUnicodeAndLiteralPercentAreDisplayData() {
        val source = "%1\$s: %2\$d"
        val translation = "\u202e%2\$d\u202c — ᠮᠣᠩᠭᠣᠯ\u202f%1\$s 👩🏽‍🎨 é 𡨸\n"
        val data = "%1\$999999999s <script> & 100%"
        assertEquals("\u202e9\u202c — ᠮᠣᠩᠭᠣᠯ\u202f$data 👩🏽‍🎨 é 𡨸\n",render(translation,source,Locale.ROOT,data,9))
        assertEquals("100% · %q · \u0000",render("100% · %q · \u0000","Plain text"))
        assertEquals("done 9%",render("done %1\$d%%","done %1\$d%%",Locale.ROOT,9))
    }

    @Test fun missingAndWrongTypedValuesKeepEverySourceClause() {
        val source = "Size %1\$d × %2\$d. Close documents. Try again; the document is unchanged."
        assertEquals("Size ? × ?. Close documents. Try again; the document is unchanged.",render("%q",source))
        assertEquals("Size 42 × ?. Close documents. Try again; the document is unchanged.",render(source,source,Locale.ROOT,42))
        assertEquals("Size null × 9. Close documents. Try again; the document is unchanged.",render(source,source,Locale.ROOT,null,9))
        assertEquals("Size ? × 9. Close documents. Try again; the document is unchanged.",render(source,source,Locale.ROOT,"wrong",9))
    }

    @Test fun formattingLocaleAndSourcePrecisionArePreserved() {
        val source = "%1\$06X · %2\$.2f"
        assertEquals("00ABCD · 1.25",render(source,source,Locale.ROOT,0xabcd,1.25))
        assertEquals("00ABCD · 1,25",render(source,source,Locale.GERMANY,0xabcd,1.25))
        assertEquals("00ABCD · 1.25",render("%1\$1000X · %2\$.120f",source,Locale.ROOT,0xabcd,1.25))
    }

    @Test fun longCompleteTextAndArgumentsAreNeverTruncatedOrReinterpreted() {
        val translation = "Long help. ".repeat(4000)+"%1\$s. Cancel to keep the document unchanged."
        val argument = "𡨸 %2\$999999999d ".repeat(10000)
        val result=render(translation,"%1\$s. Cancel to keep the document unchanged.",Locale.ROOT,argument)
        assertEquals(translation.replace("%1\$s",argument),result)
        assertTrue(result.endsWith("Cancel to keep the document unchanged."))
        assertEquals(argument,render("%1\$s".repeat(129),"%1\$s",Locale.ROOT,argument))
    }

    @Test fun longIncompleteNumericAndFlagRunsRejectBeforeAnyFormatting() {
        for (run in listOf("0","1","-","<",".")) for (size in listOf(1000,30000,65000)) {
            val candidate="%"+run.repeat(size)+"!"
            assertEquals("Safe value. Keep the image unchanged.",
                render(candidate,"Safe %1\$s. Keep the image unchanged.",Locale.ROOT,"value"))
        }
        for(candidate in listOf("%1\$"+"0".repeat(60000)+"!", "%1\$."+"0".repeat(60000)+"!")) {
            assertEquals("Safe value.",render(candidate,"Safe %1\$s.",Locale.ROOT,"value"))
        }
    }

    @Test fun seededAdversarialMutationsAndRepeatedCallsRemainBoundedAndStateless() {
        val random=Random(20261017)
        val alphabet="%0123456789\$.-+<sdfXq\u202e\u202cᠠ𡨸👩\n"
        val source="%1\$s %2\$d. Keep the document unchanged."
        val expected="data 7. Keep the document unchanged."
        repeat(2500) {
            val noise=buildString { repeat(random.nextInt(1,100)) {append(alphabet[random.nextInt(alphabet.length)])} }
            val bad="%3\$s"+noise
            assertEquals(expected,render(bad,source,Locale.ROOT,"data",7))
            assertEquals("7 data",render("%2\$d %1\$s",source,Locale.ROOT,"data",7))
        }
    }
    @Test fun literalFormatterTokensCanFollowLocalWordingWithoutChangingArgumentContracts() {
        val source="Value %1\$d percent. Keep the image unchanged."
        for (candidate in listOf("Value %1\$d%%", "%nValue %1\$d%% %%", "Value %1\$d%5%")) {
            assertEquals(String.format(Locale.ROOT,candidate,7),render(candidate,source,Locale.ROOT,7))
            assertEquals(String.format(Locale.ROOT,source,7),render(source,candidate,Locale.ROOT,7))
        }
        for (candidate in listOf("Value %1\$d%999999999%", "Value %1\$d%1025%", "Value %1\$d%.129%",
            "Value %1\$d%--%", "Value %1\$d%1n", "Value %1\$d"+"%%".repeat(128), "Value %1\$s%%")) {
            assertEquals(String.format(Locale.ROOT,source,7),render(candidate,source,Locale.ROOT,7))
        }
    }

    @Test fun allEighteenReviewedLiteralPercentTranslationsRetainTheirCompleteText() {
        // Exact existing source/translation pairs: seven per Ainu script and four Manchu.
        // Kept literal so a catalogue edit cannot silently rewrite the regression oracle.
        val pairs=listOf(
            Triple("values-b+ain+Kana/ui_each_px_px_percent_is_relative_to_the",
                "Each %1\$s: %2\$s px\n%3\$s: %4\$s–%5\$s px\nPercent is relative to the largest current %6\$s: %7\$s px. Placed images reflow to make room.",
                "シネㇷ゚ シネㇷ゚ コㇿ %1\$s: %2\$s px\n%3\$s: %4\$s–%5\$s px\n%% アナㇰ タネ イヨッタ ポロ %6\$s: %7\$s px アニ アカㇻ. アアヌ ノカ アナㇰ ウㇱケ アカㇻ クス スイ アアヌ."),
            Triple("values-b+ain+Kana/ui_percent_of_pixels",
                "percent of %1\$s pixels",
                "%1\$s px コㇿ %%"),
            Triple("values-b+ain+Kana/ui_trim_in_percent",
                "%1\$s trim in percent",
                "%1\$s アトゥイェ パㇰノ %% アニ"),
            Triple("values-b+ain+Kana/ui_normalize_width_info",
                "Width of each image: %1\$d px\nHeights: %2\$d–%3\$d px\nPercent is relative to the largest current width: %4\$d px. Placed images reflow to make room.",
                "ノカ シネㇷ゚ シネㇷ゚ セリ: %1\$d px\nケウェリヒ: %2\$d–%3\$d px\n100%% アナㇰ タネ イヨッタ ポロ セリ, %4\$d px, ネ. アアヌ ノカ アナㇰ ウㇱケ アカㇻ クス スイ アアヌ."),
            Triple("values-b+ain+Kana/ui_normalize_height_info",
                "Height of each image: %1\$d px\nWidths: %2\$d–%3\$d px\nPercent is relative to the largest current height: %4\$d px. Placed images reflow to make room.",
                "ノカ シネㇷ゚ シネㇷ゚ ケウェリヒ: %1\$d px\nセリ: %2\$d–%3\$d px\n100%% アナㇰ タネ イヨッタ ポロ ケウェリヒ, %4\$d px, ネ. アアヌ ノカ アナㇰ ウㇱケ アカㇻ クス スイ アアヌ."),
            Triple("values-b+ain+Kana/ui_normalize_width_input_percent",
                "Common width as a percentage of %1\$d px",
                "ウパㇰノ アカㇻ セリ, %% アニ. 100%%: %1\$d px."),
            Triple("values-b+ain+Kana/ui_normalize_height_input_percent",
                "Common height as a percentage of %1\$d px",
                "ウパㇰノ アカㇻ ケウェリヒ, %% アニ. 100%%: %1\$d px."),
            Triple("values-b+ain+Latn/ui_each_px_px_percent_is_relative_to_the",
                "Each %1\$s: %2\$s px\n%3\$s: %4\$s–%5\$s px\nPercent is relative to the largest current %6\$s: %7\$s px. Placed images reflow to make room.",
                "Sinep sinep kor %1\$s: %2\$s px\n%3\$s: %4\$s–%5\$s px\n%% anak tane iyotta poro %6\$s: %7\$s px ani a=kar. A=anu noka anak uske a=kar kusu suy a=anu."),
            Triple("values-b+ain+Latn/ui_percent_of_pixels",
                "percent of %1\$s pixels",
                "%1\$s px kor %%"),
            Triple("values-b+ain+Latn/ui_trim_in_percent",
                "%1\$s trim in percent",
                "%1\$s a=tuye pakno %% ani"),
            Triple("values-b+ain+Latn/ui_normalize_width_info",
                "Width of each image: %1\$d px\nHeights: %2\$d–%3\$d px\nPercent is relative to the largest current width: %4\$d px. Placed images reflow to make room.",
                "Noka sinep sinep seri: %1\$d px\nKewerihi: %2\$d–%3\$d px\n100%% anak tane iyotta poro seri, %4\$d px, ne. A=anu noka anak uske a=kar kusu suy a=anu."),
            Triple("values-b+ain+Latn/ui_normalize_height_info",
                "Height of each image: %1\$d px\nWidths: %2\$d–%3\$d px\nPercent is relative to the largest current height: %4\$d px. Placed images reflow to make room.",
                "Noka sinep sinep kewerihi: %1\$d px\nSeri: %2\$d–%3\$d px\n100%% anak tane iyotta poro kewerihi, %4\$d px, ne. A=anu noka anak uske a=kar kusu suy a=anu."),
            Triple("values-b+ain+Latn/ui_normalize_width_input_percent",
                "Common width as a percentage of %1\$d px",
                "Upakno a=kar seri, %% ani. 100%%: %1\$d px."),
            Triple("values-b+ain+Latn/ui_normalize_height_input_percent",
                "Common height as a percentage of %1\$d px",
                "Upakno a=kar kewerihi, %% ani. 100%%: %1\$d px."),
            Triple("values-b+mnc+Mong/ui_normalize_width_info",
                "Width of each image: %1\$d px\nHeights: %2\$d–%3\$d px\nPercent is relative to the largest current width: %4\$d px. Placed images reflow to make room.",
                "ᠶᠠᠶᠠ ᠨᡳᡵᡠᡤᠠᠨ ᡳ ᠣᠨᠴᠣ ᡴᡝᠮᡠᠨ: %1\$d px\nᡩᡝᠨ ᡴᡝᠮᡠᠨ: %2\$d–%3\$d px\n%% ᠪᡝ ᡨᡝ ᡠᠮᡝᠰᡳ ᠠᠮᠪᠠ ᠣᠨᠴᠣ ᡴᡝᠮᡠᠨ (%4\$d px) ᡳ ᠰᠣᠩᡴᠣᡳ ᠪᠣᡩᠣᠮᠪᡳ. ᠰᡳᠨᡩᠠᡥᠠ ᠨᡳᡵᡠᡤᠠᠨ ᠪᡝ ᡩᠠᡥᡡᠮᡝ ᠰᡳᠨᡩᠠᡶᡳ ᠪᠠ ᠪᡝ ᠰᡠᠯᠠ ᠣᠪᡠᠮᠪᡳ."),
            Triple("values-b+mnc+Mong/ui_normalize_height_info",
                "Height of each image: %1\$d px\nWidths: %2\$d–%3\$d px\nPercent is relative to the largest current height: %4\$d px. Placed images reflow to make room.",
                "ᠶᠠᠶᠠ ᠨᡳᡵᡠᡤᠠᠨ ᡳ ᡩᡝᠨ ᡴᡝᠮᡠᠨ: %1\$d px\nᠣᠨᠴᠣ ᡴᡝᠮᡠᠨ: %2\$d–%3\$d px\n%% ᠪᡝ ᡨᡝ ᡠᠮᡝᠰᡳ ᠠᠮᠪᠠ ᡩᡝᠨ ᡴᡝᠮᡠᠨ (%4\$d px) ᡳ ᠰᠣᠩᡴᠣᡳ ᠪᠣᡩᠣᠮᠪᡳ. ᠰᡳᠨᡩᠠᡥᠠ ᠨᡳᡵᡠᡤᠠᠨ ᠪᡝ ᡩᠠᡥᡡᠮᡝ ᠰᡳᠨᡩᠠᡶᡳ ᠪᠠ ᠪᡝ ᠰᡠᠯᠠ ᠣᠪᡠᠮᠪᡳ."),
            Triple("values-b+mnc+Mong/ui_normalize_width_input_percent",
                "Common width as a percentage of %1\$d px",
                "ᠠᡩᠠᠯᡳ ᠣᠨᠴᠣ ᡴᡝᠮᡠᠨ (%1\$d px ᡳ %%)"),
            Triple("values-b+mnc+Mong/ui_normalize_height_input_percent",
                "Common height as a percentage of %1\$d px",
                "ᠠᡩᠠᠯᡳ ᡩᡝᠨ ᡴᡝᠮᡠᠨ (%1\$d px ᡳ %%)")
        )
        assertEquals(18,pairs.size)
        for ((label,source,translation) in pairs) {
            val args: Array<out Any> = if (source.contains("%1\$d")) arrayOf(20,10,40,80)
                else arrayOf("width","20","height","10","40","width","80")
            val expected=String.format(Locale.ROOT,translation,*args)
            assertNotEquals(label,String.format(Locale.ROOT,source,*args),expected)
            assertEquals(label,expected,LocaleText.resolve(translation,source,true,Locale.ROOT,args))
            assertEquals(label,String.format(Locale.ROOT,source,*args),LocaleText.resolve(source,translation,true,Locale.ROOT,args))
        }
    }

    @Test fun presentNullMatchesFormatterForEverySourceConversionButMissingSlotsRemainMissing() {
        // All canonical conversion types, with their numeric precision/padding forms.
        for (format in listOf("%1\$s", "%1\$d", "%1\$,d", "%1\$06X", "%1\$.0f", "%1\$.1f", "%1\$.2f")) {
            val source="Value $format. Keep the document unchanged."
            val translated="Translated $format. Keep the document unchanged."
            val args=arrayOf<Any?>(null)
            assertEquals(String.format(Locale.ROOT,translated,*args),LocaleText.resolve(translated,source,true,Locale.ROOT,args))
            assertEquals(String.format(Locale.ROOT,source,*args),LocaleText.resolve("%99\$s",source,true,Locale.ROOT,args))
            assertEquals("Value ?. Keep the document unchanged.",LocaleText.resolve(translated,source,true,Locale.ROOT,emptyArray()))
        }
        assertEquals("null / ?",render("%1\$s / %2\$s","%1\$s / %2\$s",Locale.ROOT,null))
        assertEquals("? / null",render("%2\$s / %1\$s","%2\$s / %1\$s",Locale.ROOT,null))
        assertEquals("null / null",render("%2\$s / %1\$s","%2\$s / %1\$s",Locale.ROOT,null,null))
    }

}
