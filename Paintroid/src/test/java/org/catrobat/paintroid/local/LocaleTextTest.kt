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

    @Test fun missingNullAndWrongTypedValuesKeepEverySourceClause() {
        val source = "Size %1\$d × %2\$d. Close documents. Try again; the document is unchanged."
        assertEquals("Size ? × ?. Close documents. Try again; the document is unchanged.",render("%q",source))
        assertEquals("Size 42 × ?. Close documents. Try again; the document is unchanged.",render(source,source,Locale.ROOT,42))
        assertEquals("Size ? × 9. Close documents. Try again; the document is unchanged.",render(source,source,Locale.ROOT,null,9))
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
}
