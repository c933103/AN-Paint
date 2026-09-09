/* Pocket Paint Local additions, 2026-09-07. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.app.Dialog
import android.text.method.LinkMovementMethod
import android.text.util.Linkify
import android.widget.ScrollView
import android.widget.TextView
import android.widget.LinearLayout
import android.widget.Button
import android.widget.PopupMenu
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
            Formerly distributed as Pocket Paint Local.

            A modified distribution of Pocket Paint (Paintroid), based on Catrobat/Paintroid v2.14.1, commit 853ce3c346910ea73aa4de5514f2a76ace1396fb.

            Original Paintroid code and colour picker:
            Copyright © 2010–2022 The Catrobat Team and contributors. Original file-level notices are retained in the source.

            Original project: https://github.com/Catrobat/Paintroid
            Original contributor credits: https://developer.catrobat.org/credits

            Local modifications dated 7–9 September 2026: drawing workspace and copyleft icon integration, classic drawing/selection tools with double-tap polygon completion, pixel corner-radius control, corner/edge resizing and rotation handles for rectangular and free-form selections, centred 100% zoom and Fit, direct Android file picking, image import fixes, full-resolution loading, disk undo, local scanline bucket fill, icon controls, zoom slider, honeycomb and advanced RGB/HSV/HSL colour selectors, memory-based size checks and user-approved import downsizing, pixel/percentage sizing with optional aspect locks, touch canvas trimming/expansion, accurate Undo availability and a two-column edit-action grid, a 20-image assembly workspace with sorting, reversible individual/batch crops, width/height normalization, single-image unplacing with gap closure and direct-drag edge snapping, atomic autosave, compact/collapsible toolbars and colour controls, pinch-and-pan navigation, an opaque main editor, named custom colours, bundled font previews and text options, copyable licence text with fixed actions, in-app licence/source access and build changes. The original editor and its additional tools are retained under View.

            AN Paint is an independently maintained, modified distribution of Catrobat's Pocket Paint.

            The covered application code, including these modifications, is licensed under GNU Affero General Public License version 3 or, at your option, any later version (AGPL-3.0-or-later). You may copy, modify and redistribute it under that licence. It is provided WITHOUT ANY WARRANTY, including merchantability or fitness for a particular purpose.

            Icons and artwork: all 16 classic tool icons, Undo/Redo, Cut/Copy/Paste, Select all, zoom/navigation controls, reversible panel arrows and the assembly attachment glyph use KDE Breeze Icons. Copyright © 2014 Uri Herrera and others; KDE Community contributors. These icons and the generated PNG resources are licensed under GNU Lesser General Public License version 3 or any later version (LGPL-3.0-or-later). The previous locally drawn icon geometry was removed on 9 September 2026. Read Icon licences for the full LGPL/GPL texts and upstream notice. Original SVGs, exact revision, hashes and conversion script are included in the bundled source. https://invent.kde.org/frameworks/breeze-icons

            Dynamic colour displays, spectrum/wheel controls, honeycomb swatches, crop and selection-transform handles, zoom tick marks and selection boundaries remain application drawing code under AGPL-3.0-or-later. The new AN monogram launcher is geometric vector artwork, Copyright © 2026 AN Paint contributors, under AGPL-3.0-or-later, with editable SVG and generation code in the source. No font is used for the monogram. Inherited Pocket Paint retained-editor artwork retains Catrobat attribution; Android/Material assets retain their Apache-2.0 notices. Android supplies the landscape submenu indicators. Assembly thumbnails come from the user's imported images.

            Fonts: AN Paint bundles unmodified Lato, Alegreya Sans, Bree Serif, Anton, Bangers, Patrick Hand, Sacramento, Sawarabi Gothic, Sawarabi Mincho and Anonymous Pro fonts under SIL Open Font License 1.1. Font licences contains each original copyright notice and full licence text. The app also offers Android system sans-serif, serif, monospace and related faces; these and fallback fonts are supplied by the device. Their exact files and copyright holders depend on the Android build; see the device's open-source licences. No Dubai or STC/GE SS font binaries are included.

            Help › Icons, fonts & artwork credits contains the asset inventory and attribution. Other included components retain their respective licences and copyright notices. Read Third-party notices below.

            Complete corresponding source and build scripts for this version are bundled in this APK. In the classic workspace, choose Help › Export this version's source code to save the ZIP. The source contains the full licence and dated change report. No network connection is needed.
        """.trimIndent()
    }
    fun buildAboutDialog(activity: Activity): Dialog = termsDialog(activity,"About, copyright & licence",aboutText(activity))
    fun showAbout(activity: Activity) { buildAboutDialog(activity).show() }
    fun showAsset(activity: Activity,title: String,asset: String) {
        val text=activity.assets.open(asset).bufferedReader().use { it.readText() }
        termsDialog(activity,title,text).show()
    }
    fun termsDialog(activity: Activity,title: String,text: String): Dialog {
        fun dp(n: Int)=(n*activity.resources.displayMetrics.density+.5f).toInt()
        val dialog=Dialog(activity).apply { requestWindowFeature(android.view.Window.FEATURE_NO_TITLE) }
        val body=LinearLayout(activity).apply { orientation=LinearLayout.VERTICAL;setBackgroundColor(Color.WHITE);setPadding(dp(12),dp(8),dp(12),dp(8)) }
        body.addView(TextView(activity).apply { this.text=title;textSize=18f;setTextColor(Color.BLACK);maxLines=2;gravity=Gravity.CENTER_VERTICAL },LinearLayout.LayoutParams(-1,dp(52)))
        val scroll=ScrollView(activity).apply { tag="terms_scroll" }
        scroll.addView(TextView(activity).apply {
            tag="terms_text";this.text=text;textSize=14f;setTextColor(Color.BLACK);setTextIsSelectable(true);setPadding(dp(4),dp(6),dp(4),dp(12))
            Linkify.addLinks(this,Linkify.WEB_URLS);movementMethod=LinkMovementMethod.getInstance()
        })
        body.addView(scroll,LinearLayout.LayoutParams(-1,0,1f))
        val actions=LinearLayout(activity).apply { tag="terms_actions";gravity=Gravity.CENTER_VERTICAL }
        fun action(label: String,tagName: String,run: (Button) -> Unit) {
            val b=Button(activity).apply { this.text=label;tag=tagName;isAllCaps=false;textSize=12f;minWidth=0;minimumWidth=0;setPadding(dp(3),0,dp(3),0);setOnClickListener { run(this) } }
            actions.addView(b,LinearLayout.LayoutParams(0,dp(48),1f))
        }
        action("Copy all","terms_copy") {
            (activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).setPrimaryClip(ClipData.newPlainText(title,text))
            Toast.makeText(activity,"Full text copied",Toast.LENGTH_SHORT).show()
        }
        action("Other terms","terms_more") { anchor ->
            val options=listOf("About & copyright","AGPL licence","Third-party notices","Font licences","Icons & artwork","Icon licences")
            val popup=PopupMenu(activity,anchor)
            options.forEachIndexed { i,label -> popup.menu.add(0,i,i,label) }
            popup.setOnMenuItemClickListener {
                dialog.dismiss()
                when (it.itemId) {
                    0 -> showAbout(activity)
                    1 -> showAsset(activity,"GNU AGPL v3","legal/AGPL-3.0.txt")
                    2 -> showAsset(activity,"Third-party notices","legal/THIRD_PARTY_NOTICES.txt")
                    3 -> showAsset(activity,"Font licences","legal/FONT_NOTICES.txt")
                    4 -> showAsset(activity,"Icons, fonts & artwork credits","legal/ASSET_CREDITS.txt")
                    else -> showAsset(activity,"Icon licences — KDE Breeze","legal/ICON_NOTICES.txt")
                };true
            };popup.show()
        }
        action("Done","terms_done") { dialog.dismiss() }
        body.addView(actions,LinearLayout.LayoutParams(-1,dp(48)))
        dialog.setContentView(body)
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
