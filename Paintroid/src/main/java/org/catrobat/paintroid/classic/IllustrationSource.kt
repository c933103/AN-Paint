/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.net.Uri
import org.catrobat.paintroid.R

/** Source-specific navigation and download rules; a CDN is not an artwork licence. */
internal enum class IllustrationSource(val home: String,val terms: String,val descriptionId: Int) {
    CATROBAT("https://catrobat.org/figures-download/","https://developer.catrobat.org/pages/legal/licenses/catrobat/",R.string.gallery_description),
    IRASUTOYA("https://www.irasutoya.com/","https://www.irasutoya.com/p/terms.html",R.string.ui_irasutoya_help34),
    OPENCLIPART("https://openclipart.org/","https://openclipart.org/share",R.string.ui_openclipart_help34);

    val label: String get()=when(this) {CATROBAT->ui(R.string.ui_catrobat_sticker_gallery);IRASUTOYA->"Irasutoya";OPENCLIPART->"Openclipart"}
    private fun secure(uri: Uri)=uri.scheme=="https" && uri.userInfo==null && uri.port in listOf(-1,443)
    fun allowsPage(uri: Uri): Boolean=secure(uri) && when(this) {
        CATROBAT->uri.host in catrobatHosts
        IRASUTOYA->uri.host in setOf("irasutoya.com","www.irasutoya.com") || (uri.host=="cse.google.com" && uri.path=="/cse")
        OPENCLIPART->uri.host in setOf("openclipart.org","www.openclipart.org")
    }
    fun allowsImage(uri: Uri): Boolean=secure(uri) && when(this) {
        CATROBAT->uri.host in catrobatHosts && raster.matches(uri.path.orEmpty())
        IRASUTOYA->uri.host in irasutoyaImageHosts && raster.matches(uri.path.orEmpty())
        OPENCLIPART->uri.host in setOf("openclipart.org","www.openclipart.org") &&
            (Regex("/image/(400|800|2000)px/[0-9]+/?").matches(uri.path.orEmpty()) || raster.matches(uri.path.orEmpty()))
    }
    fun allowsDownload(uri: Uri)=allowsImage(uri)
    fun isArtworkPage(uri: Uri)=allowsPage(uri) && when(this) {
        CATROBAT->true
        IRASUTOYA->uri.host!="cse.google.com" && Regex("/[0-9]{4}/[0-9]{2}/[^/]+\\.html").matches(uri.path.orEmpty())
        OPENCLIPART->uri.path.orEmpty().startsWith("/detail/")
    }
    companion object {
        val catrobatHosts=setOf("catrobat.org","www.catrobat.org","catrobatblog.files.wordpress.com","catrobatblog.wpcomstaging.com")
        val irasutoyaImageHosts=setOf("blogger.googleusercontent.com","1.bp.blogspot.com","2.bp.blogspot.com","3.bp.blogspot.com","4.bp.blogspot.com")
        private val raster=Regex(".*\\.(png|jpe?g|webp|gif|jxl|bmp|dib|ico|tiff?|heic|avif)$",RegexOption.IGNORE_CASE)
        fun fromId(value: String?)=values().firstOrNull {it.name==value} ?: CATROBAT
    }
}
