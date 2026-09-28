/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

import android.app.Activity
import android.app.AlertDialog
import android.app.Dialog
import android.text.method.LinkMovementMethod
import android.text.util.Linkify
import android.widget.ScrollView
import android.widget.TextView
import android.widget.LinearLayout
import android.widget.Button
import android.widget.Toast
import android.view.Gravity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.ComponentCallbacks
import android.content.res.Configuration
import android.graphics.Color

object LegalInfo {
    fun aboutText(activity: Activity): String {
        val version = activity.packageManager.getPackageInfo(activity.packageName, 0).versionName
        return """
            AN Paint $version
            Package: ${activity.packageName}

            AN Paint is an independently maintained modified distribution of Pocket Paint (Paintroid), based on Catrobat/Paintroid v2.14.1, commit 853ce3c346910ea73aa4de5514f2a76ace1396fb.

            Original code: Copyright © 2010–2022 The Catrobat Team and contributors. Original file-level notices are retained in the source.
            https://github.com/Catrobat/Paintroid
            https://developer.catrobat.org/credits

            Modifications: Copyright © 2026 AN Paint contributors. The drawing workspace, image assembly, import and memory handling, autosave, selection transforms, copyleft icon integration, fonts, export and build changes were made 7–13 September 2026. This version consolidates the remaining editing functions in the new workspace and removes the original editor, layers, transparency controls, Smudge, automatic crop and project-file formats. Full dated changes are in the corresponding source.

            Application code is licensed under the GNU Affero General Public License version 3 or, at your option, any later version (AGPL-3.0-or-later). You may copy, modify and redistribute it under that licence. It is provided WITHOUT ANY WARRANTY, including merchantability or fitness for a particular purpose.

            Tool and action icons (except the original AN Paint Save/Fit glyphs): KDE Breeze Icons, Copyright © 2014 Uri Herrera and others; KDE Community contributors. LGPL-3.0-or-later. Exact SVG sources, revisions, hashes, generated Android resources and conversion scripts are included. Read Icon licences for upstream notices and the complete LGPL/GPL texts.
            https://invent.kde.org/frameworks/breeze-icons

            Interface colours use the Material Design 3 baseline light palette. Palette data: Copyright © 2022 The Android Open Source Project, Apache-2.0. Exact upstream tokens and their licence are preserved in artwork/material3 in the source; full terms are in Third-party notices. Image pixels and colour swatches keep their actual colour values.

            The rounded paintbrush launcher and coral/blue paint stroke are original vector artwork by AN Paint contributors, AGPL-3.0-or-later, with editable source. The Save and Fit shortcut glyphs are also original AN Paint vector artwork under AGPL-3.0-or-later. Colour controls, selection/crop handles and zoom marks are application drawing code. Android supplies platform widget artwork. Imported images and assembly thumbnails belong to their respective creators. Optional online images retain their own source and terms under Image credits: Catrobat original artwork uses CC BY-SA 4.0; Irasutoya is copyright Takashi Mifune under its conditional free-use terms; Openclipart publishes CC0 artwork. No gallery image is bundled in the app.

            Common UI translations: Android Open Source Project (Apache-2.0), with pinned Android 15 action vocabulary, and Catrobat/Paintroid translators and contributors, AGPL-3.0-or-later. The exact upstream revision, unchanged translation source files and reused-key mapping are preserved under translations in the corresponding source. Untranslated terms fall back to English.

            Additional vocabulary comes from GIMP (GPL-3.0-or-later) and selected Krita catalogues (GPL version 3, with original catalogue notices preserved). Exact gettext contexts, original entries, translator credits and source hashes are included. Read Third-party notices for the original headers and full licence text. Krita supplements languages absent from the GIMP import; these additions remain partial. Further selected gaps use LibreOffice command catalogues (MPL-2.0, also offered under AGPL-3.0-or-later under MPL section 3.3) and MediaWiki common actions (GPL-2.0-or-later). Their original translator notices, exact message contexts, source hashes and licences are in Third-party notices and the corresponding source.

            Fonts: unmodified Lato, Alegreya Sans, Bree Serif, Anton, Bangers, Patrick Hand, Sacramento, Sawarabi Gothic, Sawarabi Mincho, Anonymous Pro and Noto Sans Mongolian, SIL Open Font License 1.1. AN Paint Nom UI is a renamed subset of Nom Na Tong (MIT) and Gothic Nguyen (SIL OFL 1.1), distributed under SIL OFL 1.1 with the original MIT notice retained. AN Paint Wu Fallback is a glyph-only subset of Nom Na Tong under MIT. Font licences include the original copyright notices, modification details and full terms. Android system and fallback fonts are supplied by the device; see its open-source licences for their exact attribution. No Dubai or STC/GE SS font binaries are included.

            JPEG XL uses libjxl 0.12.0 by the JPEG XL Project Authors under BSD-3-Clause, with Brotli, Highway and skcms. WebP uses libwebp 1.6.0 and SharpYUV by Google and the WebP project contributors under BSD-3-Clause, with its patent grant and the Android NDK CPU-features Apache-2.0 notice.

            HEIC and AVIF use libheif 1.23.4 and libde265 1.1.2 by Dirk Farin, struktur AG and contributors under LGPL-3.0-or-later; Kvazaar 2.3.2 by Tampere University, ITU/ISO/IEC and project contributors under BSD-3-Clause; and libaom 3.15.0 by the Alliance for Open Media and contributors under BSD-2-Clause and the AOM Patent License 1.0. Image codec licences includes the exact revisions, copyright notices, complete licence texts, patent grants and source/build details for all these components. The same full notices are included in Third-party notices.

            TIFF uses LibTIFF 4.7.2 and libjpeg-turbo 3.2.0, with Android system zlib. This software is based in part on the work of the Independent JPEG Group. The LZW compression software was developed by the University of California, Berkeley. Complete original notices, source archive hashes and build details are in Image codec licences and Third-party notices.

            BMP, DIB and GIF encoders are original AN Paint code under AGPL-3.0-or-later. The Graphics Interchange Format and GIF Service Mark belong to CompuServe Incorporated. Format details and this acknowledgement are also in Image codec licences.

            Complete corresponding source and build scripts are bundled in this APK. File > About, licences & credits > Export this version's source code saves the ZIP offline. Public repository: https://github.com/c933103/AN-Paint
        """.trimIndent()
    }
    fun buildAboutDialog(activity: Activity): Dialog = termsDialog(activity,ui(R.string.ui_about_copyright_licence),aboutText(activity))
    fun showAbout(activity: Activity) { buildAboutDialog(activity).show() }
    fun showAsset(activity: Activity,title: String,asset: String) {
        val text=activity.assets.open(asset).bufferedReader().use { it.readText() }
        termsDialog(activity,title,text).show()
    }
    /** Keep the codec overview identical to the individual, verbatim bundled notices. */
    fun codecNotices(activity: Activity): String = listOf(
        "legal/JPEG_XL_NOTICES.txt", "legal/WEBP_NOTICES.txt", "legal/HEIF_AVIF_NOTICES.txt",
        "legal/TIFF_NOTICES.txt", "legal/NATIVE_RUNTIME_NOTICES.txt", "legal/RASTER_FORMAT_NOTICES.txt"
    ).joinToString("\n\n\n") { asset -> activity.assets.open(asset).bufferedReader().use { it.readText() } }

    fun showCodecLicences(activity: Activity) {
        termsDialog(activity,ui(R.string.ui_image_codec_licences),codecNotices(activity)).show()
    }
    fun termsDialog(activity: Activity,title: String,text: String): Dialog {
        fun dp(n: Int)=(n*activity.resources.displayMetrics.density+.5f).toInt()
        val dialog=Dialog(activity).apply { requestWindowFeature(android.view.Window.FEATURE_NO_TITLE) }
        val body=LinearLayout(activity).apply { orientation=LinearLayout.VERTICAL;setBackgroundColor(EditorColours.surface);setPadding(dp(12),dp(8),dp(12),dp(8)) }
        body.addView(FlowTextView(activity).apply { this.text=title;textSize=18f;setTextColor(EditorColours.onSurface);maxLines=2;gravity=Gravity.CENTER_VERTICAL;columnHeightDp=96 },LinearLayout.LayoutParams(-1,if(VerticalText.uiVertical()) -2 else dp(52)))
        val scroll=ScrollView(activity).apply { tag="terms_scroll" }
        scroll.addView(TextView(activity).apply {
            tag="terms_text";this.text=text;textSize=14f;setTextColor(EditorColours.onSurface);setTextIsSelectable(true);setPadding(dp(4),dp(6),dp(4),dp(12))
            Linkify.addLinks(this,Linkify.WEB_URLS);movementMethod=LinkMovementMethod.getInstance()
        })
        body.addView(scroll,LinearLayout.LayoutParams(-1,0,1f))
        val actions=LinearLayout(activity).apply { tag="terms_actions";gravity=Gravity.CENTER_VERTICAL }
        fun action(label: String,tagName: String,run: (Button) -> Unit) {
            val b=FlowButton(activity).apply { columnHeightDp=96;this.text=label;tag=tagName;isAllCaps=false;textSize=12f;minWidth=0;minimumWidth=0;setPadding(dp(3),0,dp(3),0);setOnClickListener { run(this) } }
            actions.addView(b,LinearLayout.LayoutParams(0,if(VerticalText.uiVertical()) -2 else dp(48),1f))
        }
        action(ui(R.string.ui_copy_all),"terms_copy") {
            (activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(ClipData.newPlainText(title,text))
            Toast.makeText(activity,ui(R.string.ui_full_text_copied),Toast.LENGTH_SHORT).show()
        }
        action(ui(R.string.ui_other_terms),"terms_more") { _ ->
            val options=listOf(ui(R.string.ui_about_copyright),ui(R.string.ui_agpl_licence),ui(R.string.ui_third_party_notices),ui(R.string.ui_font_licences),ui(R.string.ui_icons_artwork),ui(R.string.ui_icon_licences),ui(R.string.ui_jpeg_xl_codec_licences),ui(R.string.ui_webp_codec_licences),ui(R.string.ui_heic_avif_codec_licences))
            EditorDialogBuilder(activity).setTitle(ui(R.string.ui_other_terms))
                .setItems(options.toTypedArray()) { _, index ->
                dialog.dismiss()
                when (index) {
                    0 -> showAbout(activity)
                    1 -> showAsset(activity,"GNU AGPL v3","legal/AGPL-3.0.txt")
                    2 -> showAsset(activity,ui(R.string.ui_third_party_notices),"legal/THIRD_PARTY_NOTICES.txt")
                    3 -> showAsset(activity,ui(R.string.ui_font_licences),"legal/FONT_NOTICES.txt")
                    4 -> showAsset(activity,ui(R.string.ui_icons_fonts_artwork_credits),"legal/ASSET_CREDITS.txt")
                    5 -> showAsset(activity,ui(R.string.ui_icon_licences_kde_breeze),"legal/ICON_NOTICES.txt")
                    6 -> showAsset(activity,ui(R.string.ui_jpeg_xl_codec_licences),"legal/JPEG_XL_NOTICES.txt")
                    7 -> showAsset(activity,ui(R.string.ui_webp_codec_licences),"legal/WEBP_NOTICES.txt")
                    else -> showAsset(activity,ui(R.string.ui_heic_avif_codec_licences),"legal/HEIF_AVIF_NOTICES.txt")
                }
            }.setNegativeButton(ui(R.string.ui_cancel),null).show()
        }
        action(ui(R.string.ui_done),"terms_done") { dialog.dismiss() }
        body.addView(actions,LinearLayout.LayoutParams(-1,if(VerticalText.uiVertical()) -2 else dp(48)))
        dialog.setContentView(body)
        LocaleTypography.install(body)
        fun resize() {
            val m=activity.resources.displayMetrics
            dialog.window?.setLayout((m.widthPixels*.94f).toInt(),(m.heightPixels*.88f).toInt())
        }
        val callback=object : ComponentCallbacks {
            override fun onConfigurationChanged(config: Configuration) { resize() }
            override fun onLowMemory() = Unit
        }
        dialog.setOnShowListener { resize();activity.registerComponentCallbacks(callback) }
        dialog.setOnDismissListener { activity.unregisterComponentCallbacks(callback) }
        return dialog
    }
}
