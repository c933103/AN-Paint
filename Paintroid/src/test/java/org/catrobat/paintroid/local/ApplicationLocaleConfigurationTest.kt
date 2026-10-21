/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.LocaleManager
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Build
import android.os.LocaleList
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.AppLanguage
import org.catrobat.paintroid.classic.PaintApplication
import org.catrobat.paintroid.classic.ui
import org.junit.After
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.util.ReflectionHelpers
import org.robolectric.util.ReflectionHelpers.ClassParameter
import java.util.Locale

/** Framework-operation regression, not a claim to reproduce the installed callback timing. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30], qualifiers="en-rUS-w412dp-h900dp-port-xhdpi")
class ApplicationLocaleConfigurationTest {
    private val application get()=RuntimeEnvironment.getApplication() as PaintApplication
    private val originalDefault=Locale.getDefault()
    private val originalSystem=Configuration(Resources.getSystem().configuration)
    private val originalResources=PaintApplication.currentResources

    @Suppress("DEPRECATION")
    private fun firstTag(configuration: Configuration): String =
        (if(Build.VERSION.SDK_INT>=24) configuration.locales[0] else configuration.locale).toLanguageTag()

    @After @Suppress("DEPRECATION") fun restoreLanguage() {
        if(Build.VERSION.SDK_INT>=33)
            application.getSystemService(LocaleManager::class.java)!!.applicationLocales=LocaleList.getEmptyLocaleList()
        application.getSharedPreferences("app-language",0).edit().clear().commit()
        Resources.getSystem().updateConfiguration(originalSystem,Resources.getSystem().displayMetrics)
        PaintApplication.currentResources=originalResources
        Locale.setDefault(originalDefault)
    }

    @Test fun frameworkLocaleResetAfterActivityRefreshKeepsManchuAndCurrentChoice() {
        // Application was created in en-US before the in-app choice, as in the failed API30 run.
        assertEquals("en-US",application.resources.configuration.locales[0].toLanguageTag())
        val controller=Robolectric.buildActivity(Activity::class.java).setup()
        val activity=controller.get()
        val systemBefore=Configuration(Resources.getSystem().configuration)
        try {
            for(tag in listOf("mnc-Mong","fr","ko-Kore-KR","qaa-Zsye-XV","en-US")) {
                AppLanguage.select(activity,tag)
                AppLanguage.refresh(activity,Configuration(activity.resources.configuration).apply {
                    orientation=Configuration.ORIENTATION_LANDSCAPE
                    screenWidthDp=900;screenHeightDp=412
                })
                val resourceTag=AppLanguage.resourceLocale(Locale.forLanguageTag(tag)).toLanguageTag()
                assertEquals(tag,AppLanguage.selectedTag(activity))
                assertEquals(resourceTag,activity.resources.configuration.locales[0].toLanguageTag())
                assertEquals(tag,Locale.getDefault().toLanguageTag())

                // Invoke Android 11's real operation, including its preferred-locale index and
                // prepend branches. No application/activity callback follows this operation.
                resetDefaultFromApplication(LocaleList.forLanguageTags("en-US,fr"))

                assertEquals("Framework reset must retain the current public choice",tag,Locale.getDefault().toLanguageTag())
                assertEquals(tag,LocaleList.getAdjustedDefault()[0].toLanguageTag())
                assertEquals(tag,application.resources.configuration.locales[0].toLanguageTag())
                assertEquals(resourceTag,activity.resources.configuration.locales[0].toLanguageTag())
                assertEquals(tag,AppLanguage.selectedTag(activity))
                assertSame(activity,controller.get())
                assertEquals(systemBefore,Resources.getSystem().configuration)
            }
        } finally {controller.pause().stop().destroy()}
    }

    private fun resetDefaultFromApplication(systemLocales: LocaleList) {
        val activityThread=ReflectionHelpers.callStaticMethod<Any>(
            Class.forName("android.app.ActivityThread"),"currentActivityThread")
        ReflectionHelpers.callInstanceMethod<Unit>(activityThread,"updateLocaleListFromAppContext",
            ClassParameter.from(Context::class.java,application.applicationContext),
            ClassParameter.from(LocaleList::class.java,systemLocales))
    }

    @Test @Config(sdk=[30,35]) fun applicationReadsCurrentPublicChoiceWhileUiKeepsExactResourceRouting() {
        val systemBefore=Configuration(Resources.getSystem().configuration)
        for(tag in listOf("mnc-Mong","ko-Kore-KR","qaa-Zsye-XV","ja")) {
            AppLanguage.select(application,tag)
            // Reading application resources itself must not change the process default.
            Locale.setDefault(Locale.ITALY)
            assertEquals(tag,application.resources.configuration.locales[0].toLanguageTag())
            assertEquals(Locale.ITALY,Locale.getDefault())
            application.onConfigurationChanged(Configuration(application.baseContext.resources.configuration))
            assertEquals(tag,Locale.getDefault().toLanguageTag())
            val expected=AppLanguage.wrap(application.baseContext).resources
            assertEquals(AppLanguage.resourceLocale(Locale.forLanguageTag(tag)).toLanguageTag(),
                PaintApplication.currentResources.configuration.locales[0].toLanguageTag())
            assertEquals(expected.getString(R.string.ui_save),ui(R.string.ui_save))
            assertEquals(expected.getString(R.string.ui_menu_file),ui(R.string.ui_menu_file))
            assertEquals(systemBefore,Resources.getSystem().configuration)
        }
    }

    @Test @Config(sdk=[21,25,30,35]) fun everyPickerChoiceRemainsPublicWithoutMutatingTheDefaultOnRead() {
        val systemBefore=Configuration(Resources.getSystem().configuration)
        for(tag in AppLanguage.tags(application)) {
            AppLanguage.select(application,tag)
            Locale.setDefault(Locale.ITALY)
            assertEquals(tag,firstTag(application.resources.configuration))
            assertEquals(Locale.ITALY,Locale.getDefault())
            assertEquals(tag,AppLanguage.selectedTag(application))
            assertEquals(systemBefore,Resources.getSystem().configuration)
        }
    }

    @Test @Config(sdk=[21,25,30,35]) @Suppress("DEPRECATION")
    fun returningToSystemFollowDoesNotKeepThePreviousOverride() {
        val system=Resources.getSystem()
        AppLanguage.select(application,"mnc-Mong")
        assertEquals("mnc-Mong",firstTag(application.resources.configuration))
        AppLanguage.select(application,"")
        for(tag in listOf("en-US","ja","fr")) {
            val device=Locale.forLanguageTag(tag)
            system.updateConfiguration(Configuration(originalSystem).apply {
                setLocale(device);setLayoutDirection(device)
            },system.displayMetrics)
            assertEquals("",AppLanguage.selectedTag(application))
            assertEquals(tag,firstTag(application.resources.configuration))
            application.onConfigurationChanged(Configuration(system.configuration))
            assertEquals(tag,Locale.getDefault().toLanguageTag())
            assertEquals(tag,firstTag(PaintApplication.currentResources.configuration))
            assertEquals(tag,firstTag(system.configuration))
            if(Build.VERSION.SDK_INT>=33)
                assertTrue(application.getSystemService(LocaleManager::class.java)!!.applicationLocales.isEmpty)
        }
    }

    @Test @Config(sdk=[33,35]) fun systemAppLanguageChoiceWinsOverTheOldInAppPreference() {
        AppLanguage.select(application,"mnc-Mong")
        val manager=application.getSystemService(LocaleManager::class.java)!!
        manager.applicationLocales=LocaleList.forLanguageTags("ja")
        assertEquals("ja",application.resources.configuration.locales[0].toLanguageTag())
        application.onConfigurationChanged(Configuration(application.baseContext.resources.configuration))
        assertEquals("ja",Locale.getDefault().toLanguageTag())
        assertEquals("保存",ui(R.string.ui_save))
        assertEquals("ja",manager.applicationLocales.toLanguageTags())
    }

    @Test fun applicationLocaleOverrideDoesNotFreezeScreenOrFontConfiguration() {
        AppLanguage.select(application,"mnc-Mong")
        // Prime the application resource path before changing the underlying device config.
        application.resources
        RuntimeEnvironment.setQualifiers("en-rUS-w900dp-h412dp-land-xhdpi")
        RuntimeEnvironment.setFontScale(1.5f)
        val base=application.baseContext.resources.configuration
        val actual=application.resources.configuration
        assertEquals(Configuration.ORIENTATION_LANDSCAPE,actual.orientation)
        assertEquals(900,actual.screenWidthDp)
        assertEquals(412,actual.screenHeightDp)
        assertEquals(base.fontScale,actual.fontScale,0f)
        assertEquals(1.5f,actual.fontScale,0f)
        assertEquals("mnc-Mong",actual.locales[0].toLanguageTag())
    }
}
