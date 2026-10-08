/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.content.SharedPreferences
import java.security.MessageDigest

/**
 * Credits saved by releases before per-document attribution.
 *
 * This is an installation-wide archive, not a document ledger: the old writer never
 * removed a source when an artwork was replaced, an insertion cancelled, or pixels
 * undone. Reading it must neither attach its entries to an image nor delete the only
 * durable copy. In particular, an absent modern ledger is not proof of association.
 */
internal object LegacyImageCredits {
    internal const val PREFERENCES_NAME = "image-credits"

    fun read(context: Context): List<ImageCredit> = read(
        context.getSharedPreferences(PREFERENCES_NAME,Context.MODE_PRIVATE))

    fun hasRecords(context: Context): Boolean =
        sources(context.getSharedPreferences(PREFERENCES_NAME,Context.MODE_PRIVATE).all).isNotEmpty()

    private fun sources(values: Map<String,*>): Set<String> {
        val indexed=(values["sources"] as? Set<*>)?.filterIsInstance<String>().orEmpty()
        // A missing/partial index must not hide a stored value. The key names its
        // source, but conveys no artwork association; these stay archive-only.
        val unindexed=values.mapNotNull {(key,value) ->
            if(value !is String) null else when {
                key.startsWith("text:") -> key.removePrefix("text:")
                key.startsWith("generated:") -> key.removePrefix("generated:")
                else -> null
            }
        }
        return (indexed+unindexed).toSet()
    }

    /** Stable origin identifier; archive selections additionally identify exact text. */
    fun sourceToken(source: String): String = MessageDigest.getInstance("SHA-256")
        .digest(source.toByteArray(Charsets.UTF_8)).joinToString("") {"%02x".format(it.toInt() and 255)}

    internal fun read(preferences: SharedPreferences): List<ImageCredit> {
        val values=preferences.all
        return sources(values).sorted().map {source ->
            // Empty saved text was an intentional edit in the old editor. Do not use
            // isBlank(), trim, truncate, or regenerate either stored representation.
            val text=values["text:$source"] as? String
                ?: values["generated:$source"] as? String
                ?: GalleryCredits.credit(source)
            ImageCredit(source,text)
        }
    }
}
