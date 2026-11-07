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
    /** Application-owned metadata status only; localize at the alive UI boundary. */
    class HttpException(val status: Int): IOException()

    /** Application-owned streaming response limit; localize only at the alive UI boundary. */
    class ResponseLimitException: IOException()

    /** Application-owned API error presence; keep provider error fields out of UI text. */
    class QueryFailureException: IOException()

    private const val MAX_RESPONSE = 2 * 1024 * 1024
    private const val MAX_FIELD = 64 * 1024
    private val fields = listOf("ObjectName", "Artist", "Credit", "Attribution", "LicenseShortName",
        "LicenseUrl", "UsageTerms", "Permission", "Copyrighted", "AttributionRequired", "Restrictions")

    data class Record(val source: String, val page: String, val title: String, val metadata: Map<String, String>) {
        fun text(imported: Boolean): String {
            // Preserve creator and source-mandated legal notices, without
            // presenting API bookkeeping flags or app guidance as attribution.
            val noticeFields=fields.filter {it !in setOf("ObjectName","Copyrighted","AttributionRequired")}
            val notices=noticeFields.mapNotNull {key -> metadata[key]?.takeIf {it.isNotBlank()}?.let {"$key: $it"}}
            val changes=if(!imported) null else if(Uri.parse(source).path.orEmpty().endsWith(".svg",true))
                ui(R.string.commons_import_svg_changes) else ui(R.string.commons_import_raster_changes)
            return PublicationCredit(title,"Wikimedia Commons",page,notices=notices,changes=changes).text()
        }
    }

    fun requestUrl(page: String): URL {
        val uri = Uri.parse(page)
        if (!IllustrationSource.COMMONS.isArtworkPage(uri)) throw CommonsImportFailure.NotFilePage()
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

    fun userAgent(context: Context): String {
        val version = context.packageManager.getPackageInfo(context.packageName, 0).versionName ?: "unknown"
        return "AN-Paint/$version (https://github.com/c933103/AN-Paint; Android)"
    }

    /** File-page selection is resolved by Commons' imageinfo response, never by
     * a WebView thumbnail, its preview URL or untrusted title metadata.
     * Both paths use the same bounded API request and attribution checks.
     */
    fun fetch(context: Context, source: String, page: String, open: (URL) -> HttpURLConnection,
        checkActive: () -> Unit, active: (HttpURLConnection?) -> Unit): Record =
        parse(query(context,page,open,checkActive,active),source)

    fun resolve(context: Context, page: String, open: (URL) -> HttpURLConnection,
        checkActive: () -> Unit, active: (HttpURLConnection?) -> Unit): Record =
        parseResolved(query(context,page,open,checkActive,active))

    internal fun parseResolved(json: String): Record {
        require(json.length<=MAX_RESPONSE)
        val root=JSONObject(json)
        if(root.has("error")) throw QueryFailureException()
        val pages=root.getJSONObject("query").getJSONArray("pages")
        if(pages.length()!=1) throw CommonsImportFailure.AmbiguousFile()
        val entry=pages.getJSONObject(0)
        if(entry.optBoolean("missing") || entry.optInt("ns",-1)!=6) throw CommonsImportFailure.MetadataUnavailable()
        val source=entry.getJSONArray("imageinfo").getJSONObject(0).getString("url")
        if(!IllustrationSource.COMMONS.allowsImage(Uri.parse(source)))
            throw CommonsImportFailure.MetadataOriginalMismatch()
        // parse verifies the API's canonical file-page URL and the exact
        // original identity; retaining its established credit field policy.
        return parse(json,source)
    }

    private fun query(context: Context, page: String, open: (URL) -> HttpURLConnection,
        checkActive: () -> Unit, active: (HttpURLConnection?) -> Unit): String {
        checkActive()
        val connection = open(requestUrl(page)); active(connection)
        try {
            connection.instanceFollowRedirects = false
            connection.connectTimeout = 15000; connection.readTimeout = 30000
            connection.setRequestProperty("User-Agent", userAgent(context))
            connection.setRequestProperty("Referer", page)
            connection.setRequestProperty("Accept", "application/json")
            val status = connection.responseCode
            if (status != 200) throw HttpException(status)
            val bytes = ByteArrayOutputStream()
            connection.inputStream.use { input ->
                val buffer = ByteArray(16384)
                while (true) {
                    checkActive()
                    val count = input.read(buffer); if (count < 0) break
                    if (bytes.size().toLong() + count > MAX_RESPONSE) throw ResponseLimitException()
                    bytes.write(buffer, 0, count)
                }
            }
            checkActive()
            return bytes.toString("UTF-8")
        } finally { connection.disconnect(); active(null) }
    }

    fun parse(json: String, expectedSource: String): Record {
        require(json.length <= MAX_RESPONSE)
        val root = JSONObject(json)
        if (root.has("error")) throw QueryFailureException()
        val pages = root.getJSONObject("query").getJSONArray("pages")
        if (pages.length() != 1) throw CommonsImportFailure.AmbiguousFile()
        val page = pages.getJSONObject(0)
        if (page.optBoolean("missing") || page.optInt("ns", -1) != 6) throw CommonsImportFailure.MetadataUnavailable()
        val image = page.getJSONArray("imageinfo").getJSONObject(0)
        val source = image.getString("url")
        if (!sameOriginal(expectedSource, source)) throw CommonsImportFailure.MetadataOriginalMismatch()
        val pageUrl = image.getString("descriptionurl")
        if (!IllustrationSource.COMMONS.isArtworkPage(Uri.parse(pageUrl))) throw CommonsImportFailure.InvalidAttributionPage()
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
        if (html.length > MAX_FIELD) throw CommonsImportFailure.FieldTooLarge()
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
                .putString(record.source, value.toString()).commit()) throw CommonsImportFailure.CacheFailed()
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
