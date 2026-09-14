/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Build
import android.os.LocaleList
import android.widget.TextView
import org.catrobat.paintroid.R
import java.util.Locale

/** One app-wide preference; Android 13's system App languages page uses the same value. */
internal object AppLanguage {
    private const val PREFS = "app-language"
    private const val LANGUAGE = "language-tag"

    fun tags(context: Context): List<String> = context.resources.getStringArray(R.array.app_language_tags).toList()

    private fun supportedTag(context: Context,tag: String): String {
        val index=context.resources.getStringArray(R.array.app_language_aliases).indexOf(tag)
        return if(index<0) tag else context.resources.getStringArray(R.array.app_language_alias_targets)[index]
    }

    fun selectedTag(context: Context): String {
        val preferences = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        if (Build.VERSION.SDK_INT >= 33) {
            context.getSystemService(LocaleManager::class.java)?.let { manager ->
                // Migrate the preference once when a device upgrades from Android 12.
                if (!preferences.getBoolean("platform-initialized", false)) {
                    val saved = supportedTag(context,preferences.getString(LANGUAGE, "").orEmpty())
                    if (manager.applicationLocales.isEmpty && saved in tags(context))
                        manager.applicationLocales = LocaleList.forLanguageTags(saved)
                    preferences.edit().putBoolean("platform-initialized", true).apply()
                }
                val current=if(manager.applicationLocales.isEmpty) "" else manager.applicationLocales[0].toLanguageTag()
                val selected=supportedTag(context,current)
                if(selected!=current) {
                    manager.applicationLocales=LocaleList.forLanguageTags(selected)
                    preferences.edit().putString(LANGUAGE,selected).apply()
                }
                return selected
            }
        }
        val current=preferences.getString(LANGUAGE, "").orEmpty()
        return supportedTag(context,current).also {if(it!=current) preferences.edit().putString(LANGUAGE,it).apply()}
    }

    private fun deviceLocale(context: Context): Locale {
        if (Build.VERSION.SDK_INT >= 33) context.getSystemService(LocaleManager::class.java)?.let {
            if (!it.systemLocales.isEmpty) return it.systemLocales[0]
        }
        val config = Resources.getSystem().configuration
        return if (Build.VERSION.SDK_INT >= 24) config.locales[0] else @Suppress("DEPRECATION") config.locale
    }

    fun locale(context: Context): Locale = selectedTag(context).takeIf { it.isNotEmpty() }
        ?.let(Locale::forLanguageTag) ?: deviceLocale(context)

    fun wrap(context: Context): Context {
        val chosen = locale(context)
        // An override is a delta: copying the current screen configuration would
        // pin orientation, window size and font scale for this context's lifetime.
        val config = Configuration().apply {
            fontScale = 0f
            if (Build.VERSION.SDK_INT >= 24) setLocales(LocaleList(chosen)) else setLocale(chosen)
            setLayoutDirection(chosen)
        }
        Locale.setDefault(chosen)
        return context.createConfigurationContext(config)
    }

    /** Updating the current Activity avoids throwing away undo or an unfinished selection. */
    @Suppress("DEPRECATION")
    fun refresh(activity: Activity, configuration: Configuration = activity.resources.configuration) {
        val chosen = locale(activity)
        val config = Configuration(configuration).apply {
            if (Build.VERSION.SDK_INT >= 24) setLocales(LocaleList(chosen)) else setLocale(chosen)
            setLayoutDirection(chosen)
        }
        activity.resources.updateConfiguration(config, activity.resources.displayMetrics)
        PaintApplication.currentResources = activity.resources
        Locale.setDefault(chosen)
    }

    fun select(context: Context, tag: String) {
        require(tag.isEmpty() || tag in tags(context))
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString(LANGUAGE, tag)
            .putBoolean("platform-initialized", true).apply()
        if (Build.VERSION.SDK_INT >= 33) context.getSystemService(LocaleManager::class.java)?.let {
            it.applicationLocales = LocaleList.forLanguageTags(tag)
        }
    }

    fun name(tag: String): String {
        val resources=PaintApplication.currentResources
        val index=resources.getStringArray(R.array.app_language_tags).indexOf(tag)
        if(index>=0) return "${resources.getStringArray(R.array.app_language_names)[index]} [$tag]"
        val locale = Locale.forLanguageTag(tag)
        return "${locale.getDisplayName(locale)} [$tag]"
    }

    fun showSettings(activity: Activity, changed: () -> Unit) {
        val current = selectedTag(activity).let { if (it.isEmpty()) ui(R.string.language20_device_default) else name(it) }
        AlertDialog.Builder(activity).setTitle(ui(R.string.language20_settings))
            .setItems(arrayOf(ui(R.string.language20_current, current))) { _, _ -> showPicker(activity, changed) }
            .setNegativeButton(ui(R.string.ui_done), null).show()
    }

    fun showPicker(activity: Activity, changed: () -> Unit): AlertDialog {
        val choices = listOf("") + tags(activity)
        val labels = choices.map { if (it.isEmpty()) ui(R.string.language20_device_default) else name(it) }
        val note = TextView(activity).apply {
            text = ui(R.string.language20_translation_note)
            val padding = (20 * resources.displayMetrics.density).toInt()
            setPadding(padding, padding, padding, padding / 2)
        }
        return AlertDialog.Builder(activity).setTitle(ui(R.string.language20_app_language))
            .setCustomTitle(note)
            .setSingleChoiceItems(object: android.widget.ArrayAdapter<String>(activity,android.R.layout.simple_list_item_single_choice,labels) {
                override fun getView(position: Int,convertView: android.view.View?,parent: android.view.ViewGroup): android.view.View {
                    // Script-specific rows are never recycled as ordinary horizontal rows.
                    val view=super.getView(position,null,parent) as TextView
                    if(choices[position]=="mn-Mong") VerticalUi.languageChoice(view)
                    return view
                }
            }, choices.indexOf(selectedTag(activity))) { dialog, which ->
                dialog.dismiss()
                if (choices[which] != selectedTag(activity)) {
                    select(activity, choices[which]); refresh(activity); changed()
                }
            }.setNegativeButton(ui(R.string.ui_cancel), null).show()
    }
}
