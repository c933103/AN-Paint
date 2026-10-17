/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import java.util.IllegalFormatException
import java.util.Locale

/** A bounded display boundary, not a translation-quality or XML validator.
 * Never truncate a warning or the user's argument text. Reject a bad translated
 * template as a whole and render the complete canonical English source instead.
 */
internal object LocaleText {
    internal const val MAX_TEMPLATE_LENGTH = 65_536
    private const val MAX_TOKENS = 128
    private const val MAX_WIDTH = 1_024
    private const val MAX_PRECISION = 128

    private data class Token(val start: Int, val end: Int, val index: Int?,
        val flags: String, val width: Int?, val precision: Int?, val conversion: String) {
        // Order may change with grammar; types, repeated values and numeric
        // presentation must retain the source contract. %% and %n are literals.
        fun contract() = listOf(index, flags.filterNot { it == '<' }.toCharArray().sorted().joinToString(""),
            width, precision, conversion)
        fun standalone(): String = "%" + flags.filterNot { it == '<' } +
            (width?.toString() ?: "") + (precision?.let { ".$it" } ?: "") + conversion
    }

    private fun tokens(text: String): List<Token>? {
        if (text.length > MAX_TEMPLATE_LENGTH) return null
        val result = ArrayList<Token>()
        var position = 0
        var ordinaryIndex = 0
        var previousIndex: Int? = null
        while (position < text.length) {
            val start = text.indexOf('%', position)
            if (start < 0) break
            if (result.size == MAX_TOKENS) return null
            var cursor = start + 1
            // Optional index and width share a prefix, so inspect at most four
            // digits once, then reset for flags/width if no '$' follows. No
            // backtracking or unbounded numeric-field scan precedes rejection.
            val prefix = cursor
            while (cursor < text.length && text[cursor] in '0'..'9') {
                if (cursor - prefix == 4) return null
                cursor++
            }
            val explicit = if (cursor > prefix && cursor < text.length && text[cursor] == '$') {
                if (text[prefix] == '0') return null
                text.substring(prefix, cursor++).toInt() - 1
            } else { cursor = prefix; null }
            val flagsStart = cursor
            val seen = HashSet<Char>()
            while (cursor < text.length && text[cursor] in "-#+ 0,(<") {
                if (!seen.add(text[cursor])) return null
                cursor++
            }
            val flags = text.substring(flagsStart, cursor)
            if (explicit != null && '<' in flags) return null
            val widthStart = cursor
            while (cursor < text.length && text[cursor] in '0'..'9') {
                if (cursor - widthStart == 4) return null
                cursor++
            }
            val width = if (cursor == widthStart) null else text.substring(widthStart,cursor).toInt()
            if (width != null && width > MAX_WIDTH) return null
            var precision: Int? = null
            if (cursor < text.length && text[cursor] == '.') {
                val precisionStart = ++cursor
                while (cursor < text.length && text[cursor] in '0'..'9') {
                    if (cursor - precisionStart == 3) return null
                    cursor++
                }
                if (cursor == precisionStart) return null
                precision = text.substring(precisionStart,cursor).toInt()
                if (precision > MAX_PRECISION) return null
            }
            val conversionStart = cursor
            if (cursor < text.length && text[cursor] in "tT") cursor++
            if (cursor >= text.length || !(text[cursor] in 'a'..'z' || text[cursor] in 'A'..'Z' || text[cursor] == '%')) return null
            cursor++
            val conversion = text.substring(conversionStart,cursor)
            val index = when {
                conversion == "%" || conversion == "n" -> null
                '<' in flags -> previousIndex ?: return null
                explicit != null -> explicit
                else -> ordinaryIndex++
            }
            if (index != null && index !in 0 until MAX_TOKENS) return null
            if (index != null) previousIndex = index
            result.add(Token(start,cursor,index,flags,width,precision,conversion))
            position = cursor
        }
        return result
    }

    fun resolve(translated: String?, source: String, formatted: Boolean, locale: Locale, values: Array<out Any?>): String {
        val candidate = translated?.takeIf { it.isNotBlank() && it.length <= MAX_TEMPLATE_LENGTH }
        // No formatter is invoked for plain text, so literal percent signs,
        // Unicode direction controls, combining marks and newlines stay data.
        if (!formatted) return candidate ?: source
        val expected = tokens(source)
        if (values.isEmpty() && (expected == null || expected.none { it.index != null })) return candidate ?: source
        if (expected == null) return source
        val actual = candidate?.let(::tokens)
        if (actual != null && actual.all { it.index == null || values.getOrNull(it.index) != null } && actual.map { it.contract() }.groupingBy { it }.eachCount() ==
            expected.map { it.contract() }.groupingBy { it }.eachCount()) {
            try { return String.format(locale, candidate, *values) }
            catch (_: IllegalFormatException) { /* Render the source below. */ }
        }
        // A caller can also omit an argument or pass the wrong type. Preserve
        // every English clause and render only the unavailable slot as '?'.
        return buildString {
            var position = 0
            for (token in expected) {
                append(source, position, token.start)
                val value = token.index?.let { values.getOrNull(it) }
                append(try {
                    if (token.index == null) String.format(locale, token.standalone())
                    else if (value == null) "?"
                    else String.format(locale, token.standalone(), value)
                } catch (_: IllegalFormatException) { "?" })
                position = token.end
            }
            append(source, position, source.length)
        }
    }
}
