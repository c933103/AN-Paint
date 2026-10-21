/* AN Paint, 2026-09-10. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.Application
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import androidx.annotation.PluralsRes
import androidx.annotation.StringRes
import java.text.NumberFormat
import java.text.ParsePosition
import java.util.Locale

/** Application resources follow the selected app language; labels are never used as IDs. */
class PaintApplication : Application() {
    override fun attachBaseContext(base: Context) { super.attachBaseContext(AppLanguage.wrap(base)) }
    override fun onCreate() {
        super.onCreate()
        currentResources = resources
        sourceResources = createConfigurationContext(Configuration().apply {
            fontScale = 0f
            setLocale(Locale.ENGLISH)
        }).resources
    }
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        currentResources = AppLanguage.wrap(this).resources
    }
    companion object {
        internal lateinit var currentResources: Resources
        internal lateinit var sourceResources: Resources
    }
}

/** Display data only. Callers needing invariant numeric/hex output use uiRoot. */
internal fun ui(@StringRes id: Int, vararg values: Any?): String =
    uiText(PaintApplication.currentResources, id, null, null, values)

internal fun uiRoot(@StringRes id: Int, vararg values: Any?): String =
    uiText(PaintApplication.currentResources, id, null, Locale.ROOT, values)

internal fun uiQuantity(resources: Resources, @PluralsRes id: Int, quantity: Int, vararg values: Any?): String =
    uiText(resources, id, quantity, null, values)

@Suppress("DEPRECATION")
internal fun uiText(resources: Resources, id: Int, quantity: Int? = null,
    formatLocale: Locale? = null, values: Array<out Any?> = emptyArray()): String {
    // Entry/type names are compiled identifiers, never translated text.
    val kind = if (quantity == null) "string" else "plurals"
    val name = resources.getResourceEntryName(id)
    val owner = resources.getResourcePackageName(id)
    val sourceId = resources.getIdentifier("anpaint_source_" + name, kind, owner)
    val contractId = resources.getIdentifier("anpaint_source_contract_" + kind + "_" + name, kind, owner)
    // Missing canonical source is a build/programming error, not a translation.
    val source = if (quantity == null) resources.getString(sourceId)
        else PaintApplication.sourceResources.getQuantityString(sourceId, quantity)
    val formatted = (if (quantity == null) resources.getString(contractId)
        else PaintApplication.sourceResources.getQuantityString(contractId, quantity)).toBooleanStrict()
    val translated = try {
        if (quantity == null) resources.getString(id) else resources.getQuantityString(id, quantity)
    } catch (_: Resources.NotFoundException) { null }
    val locale = formatLocale ?: if (android.os.Build.VERSION.SDK_INT >= 24)
        resources.configuration.locales[0] ?: Locale.getDefault()
        else resources.configuration.locale ?: Locale.getDefault()
    return LocaleText.resolve(translated, source, formatted, locale, values)
}

/** Accept the device's decimal separator as well as ordinary decimal-dot input. */
internal fun uiNumber(text: String): Double? {
    val value = text.trim()
    value.toDoubleOrNull()?.let { return it.takeIf { n -> n.isFinite() } }
    val position = ParsePosition(0)
    val number = NumberFormat.getNumberInstance(Locale.getDefault()).parse(value, position)
    return number?.toDouble()?.takeIf { position.index == value.length && it.isFinite() }
}
