/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.content.Context
import android.net.Uri
import android.os.Build
import android.text.Html
import android.text.style.URLSpan
import org.catrobat.paintroid.R
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

/** Capture file-specific attribution, not the Commons site footer's unrelated licence. */
internal object CommonsAttribution {
    private const val MAX_RESPONSE = 2 * 1024 * 1024
    private const val MAX_FIELD = 64 * 1024
    private val fields = listOf("ObjectName", "Artist", "Credit", "Attribution", "LicenseShortName",
        "LicenseUrl", "UsageTerms", "Permission", "Copyrighted", "AttributionRequired", "Restrictions")

    data class Record(val source: String, val page: String, val title: String, val metadata: Map<String, String>) {
        fun text(imported: Boolean): String {
            val lines = mutableListOf(ui(R.string.gallery_credit_title, title), "Wikimedia Commons",
                ui(R.string.gallery_credit_source, page), ui(R.string.gallery_credit_source, source))
            // Keep the provider's field identities and values, including custom attribution,
            // multiple creators, permission/copyright notices, and all embedded credit links.
            fields.filter { it != "ObjectName" }.forEach { key ->
                metadata[key]?.takeIf { it.isNotBlank() }?.let { lines.add("$key: $it") }
            }
            if (imported) lines.add(if (Uri.parse(source).path.orEmpty().endsWith(".svg", true))
                "AN Paint: SVG → PNG; original size; antiAlias=false; strokeDashArray=none; background=#FFFFFF."
                else "AN Paint: background=#FFFFFF (alpha compositing).")
            // CommonsMetadata itself warns that machine-readable metadata can be incomplete,
            // especially for multiple licences. Never invent CC0/CC-BY-SA or call this verified permission.
            lines.add(ui(R.string.commons_check_file_licence))
            return lines.joinToString("\n")
        }
    }

    fun requestUrl(page: String): URL {
        val uri = Uri.parse(page)
        require(IllustrationSource.COMMONS.isArtworkPage(uri)) { "Not a Commons file page" }
        val title = if (uri.path == "/w/index.php") uri.getQueryParameter("title")!!
            else uri.path!!.removePrefix("/wiki/")
        require(title.startsWith("File:") && title.length in 6..1024 && !title.contains('|'))
        return URL(Uri.parse("https://commons.wikimedia.org/w/api.php").buildUpon()
            .appendQueryParameter("action", "query").appendQueryParameter("format", "json")
            .appendQueryParameter("formatversion", "2").appendQueryParameter("redirects", "1")
            .appendQueryParameter("prop", "imageinfo").appendQueryParameter("titles", title)
            .appendQueryParameter("iiprop", "url|extmetadata")
            .appendQueryParameter("iiextmetadatafilter", fields.joinToString("|"))
            .appendQueryParameter("iiextmetadatalanguage", "en").build().toString())
    }

    fun fetch(context: Context, source: String, page: String, open: (URL) -> HttpURLConnection,
        checkActive: () -> Unit, active: (HttpURLConnection?) -> Unit): Record {
        checkActive()
        val connection = open(requestUrl(page)); active(connection)
        try {
            connection.instanceFollowRedirects = false
            connection.connectTimeout = 15000; connection.readTimeout = 30000
            val version = context.packageManager.getPackageInfo(context.packageName, 0).versionName ?: "unknown"
            connection.setRequestProperty("User-Agent", "AN-Paint/$version (https://github.com/c933103/AN-Paint; Android)")
            connection.setRequestProperty("Referer", page)
            connection.setRequestProperty("Accept", "application/json")
            val status = connection.responseCode
            if (status != 200) throw IOException("Commons metadata: HTTP $status")
            val bytes = ByteArrayOutputStream()
            connection.inputStream.use { input ->
                val buffer = ByteArray(16384)
                while (true) {
                    checkActive()
                    val count = input.read(buffer); if (count < 0) break
                    if (bytes.size().toLong() + count > MAX_RESPONSE) throw IOException("Commons metadata exceeds the response limit")
                    bytes.write(buffer, 0, count)
                }
            }
            checkActive()
            return parse(bytes.toString("UTF-8"), source)
        } finally { connection.disconnect(); active(null) }
    }

    fun parse(json: String, expectedSource: String): Record {
        require(json.length <= MAX_RESPONSE)
        val root = JSONObject(json)
        if (root.has("error")) throw IOException("Commons metadata query failed")
        val pages = root.getJSONObject("query").getJSONArray("pages")
        if (pages.length() != 1) throw IOException("Commons metadata returned an ambiguous file")
        val page = pages.getJSONObject(0)
        if (page.optBoolean("missing") || page.optInt("ns", -1) != 6) throw IOException("Commons file metadata is unavailable")
        val image = page.getJSONArray("imageinfo").getJSONObject(0)
        val source = image.getString("url")
        if (!sameOriginal(expectedSource, source)) throw IOException("Commons attribution does not match the selected original file")
        val pageUrl = image.getString("descriptionurl")
        if (!IllustrationSource.COMMONS.isArtworkPage(Uri.parse(pageUrl))) throw IOException("Invalid Commons attribution page")
        val title = page.getString("title").removePrefix("File:")
        val metadata = image.optJSONObject("extmetadata") ?: JSONObject()
        val text = fields.associateWith { key ->
            val field = metadata.optJSONObject(key)
            plain(if (field == null || field.isNull("value")) "" else field.optString("value"))
        }
        return Record(expectedSource, pageUrl, text["ObjectName"].orEmpty().ifBlank { title }, text)
    }

    internal fun sameOriginal(first: String, second: String): Boolean {
        val a = Uri.parse(first); val b = Uri.parse(second)
        return IllustrationSource.COMMONS.allowsImage(a) && IllustrationSource.COMMONS.allowsImage(b) &&
            a.path == b.path
    }

    /** HTML is decoded as text, never loaded or executed. Preserve safe credit URLs separately. */
    @Suppress("DEPRECATION")
    internal fun plain(html: String): String {
        if (html.length > MAX_FIELD) throw IOException("Commons attribution field exceeds the text limit")
        val spanned = if (Build.VERSION.SDK_INT >= 24) Html.fromHtml(html, Html.FROM_HTML_MODE_LEGACY) else Html.fromHtml(html)
        val text = spanned.toString().trim()
        val links = spanned.getSpans(0, spanned.length, URLSpan::class.java).mapNotNull { span ->
            val raw = span.url
            val value = when {
                raw.startsWith("//") -> "https:$raw"
                raw.startsWith("/") -> "https://commons.wikimedia.org$raw"
                else -> raw
            }
            val uri = Uri.parse(value)
            value.takeIf { uri.scheme in setOf("http", "https") && !uri.host.isNullOrBlank() && uri.userInfo == null }
        }.distinct().filterNot { text.contains(it) }
        return (listOf(text) + links).filter { it.isNotBlank() }.joinToString("\n")
    }

    /** Cache a metadata snapshot without claiming an image was inserted. The editor records use later. */
    fun cache(context: Context, record: Record) {
        val value = JSONObject().put("source", record.source).put("page", record.page).put("title", record.title)
            .put("metadata", JSONObject(record.metadata))
        if (!context.getSharedPreferences("commons-attribution-v1", Context.MODE_PRIVATE).edit()
                .putString(record.source, value.toString()).commit()) throw IOException("Could not retain Commons attribution")
    }

    fun cached(context: Context, source: String): Record? {
        val saved = context.getSharedPreferences("commons-attribution-v1", Context.MODE_PRIVATE).getString(source, null) ?: return null
        return try {
            val data = JSONObject(saved)
            if (!sameOriginal(source, data.getString("source"))) return null
            val page = data.getString("page")
            if (!IllustrationSource.COMMONS.isArtworkPage(Uri.parse(page))) return null
            val metadata = data.getJSONObject("metadata")
            Record(source, page, data.getString("title"), fields.associateWith { metadata.optString(it) })
        } catch (_: Exception) { null }
    }
}
