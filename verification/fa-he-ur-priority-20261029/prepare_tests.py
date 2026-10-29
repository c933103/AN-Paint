from pathlib import Path
P=Path(__file__).parent;old=Path('/tmp/nordic-priority-20261029/next-trio/repo/Paintroid/src/test/java/org/catrobat/paintroid/local/BelarusianAlbanianPriorityWordingTest.kt');s=old.read_text()
s=s.replace('BelarusianAlbanianPriorityWordingTest','PersianHebrewUrduPriorityWordingTest').replace('nynorsk_belarusian_albanian_priority_wording.json','persian_hebrew_urdu_priority_wording.json').replace('RecoveredTrioPriorityExpectations.compiledDisplay(tag,key,raw)','decoded(raw)').replace('listOf("be","sq")','listOf("fa","he","ur")')
a=s.index('    @Test fun inheritedAlbanian');b=s.index('    @Test fun allChangedCompiled',a);s=s[:a]+s[b:]
s=s.replace('// Full Belarusian count-label templates are invariant across all plural children.','// Persian 0/1 share one; Hebrew 2 uses two; other supported counts use other.\n    // Hebrew older many-category counts deliberately use the complete other fallback.')
s=s.replace('getString(if(count==1) "one" else "other")','getString(when {tag=="he" && count==2->"two";count==1 || (tag=="fa" && count==0)->"one";else->"other"})')
# Distinguish standalone radio captions from four composed accessibility outputs.
s=s.replace('val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")','''assertEquals(expected(tag,if(percent) "ui_percent" else "ui_pixels"),
                controls.findViewWithTag<TextView>(if(percent) "size_percent" else "size_pixels").text.toString())
            val unit=expected(tag,if(percent) "ui_percent_fd8671" else "ui_pixels_6ec9c2")''')
extra='''
    @Test fun canonicalPickerTagsStayRtlAndHebrewLegacyResourcesDoNotCreateAnIwOption() = forEachLocale { tag,activity ->
        assertTrue(AppLanguage.tags(activity).containsAll(listOf("fa","fa-IR","he","ur")))
        assertFalse(AppLanguage.tags(activity).contains("iw"))
        assertThrows(IllegalArgumentException::class.java) {AppLanguage.select(activity,"iw")}
        assertEquals(tag,AppLanguage.selectedTag(activity))
        assertEquals(tag,AppLanguage.locale(activity).toLanguageTag())
        assertEquals(tag,AppLanguage.resourceLocale(AppLanguage.locale(activity)).toLanguageTag())
        assertEquals(View.LAYOUT_DIRECTION_RTL,activity.resources.configuration.layoutDirection)
        assertEquals(expected(tag,"save20_file_format"),activity.getString(R.string.save20_file_format))
        if(tag=="he") {
            val config=android.content.res.Configuration(activity.resources.configuration)
            config.setLocale(Locale.forLanguageTag("iw"))
            assertEquals("he",config.locales[0].toLanguageTag())
            assertEquals(expected(tag,"save20_file_format"),activity.createConfigurationContext(config).getString(R.string.save20_file_format))
        }
    }

    @Test fun keepEditingCancelsRepeatedActualReplacementWithoutSavingDiscardingOrLaunching() {
        for(tag in listOf("fa","he","ur")) {
            AppLanguage.select(RuntimeEnvironment.getApplication(),tag)
            val controller=Robolectric.buildActivity(ClassicPaintActivity::class.java);val activity=controller.get()
            try {
                controller.setup();awaitEditorStartup(activity);Locale.setDefault(Locale.US)
                activity.document.newImage(4,3);activity.document.invert();activity.paintCanvas.fit()
                val bitmap=activity.document.bitmap.copy(android.graphics.Bitmap.Config.ARGB_8888,false)
                val history=activity.document.historySnapshot()
                try {repeat(2) {
                    assertTrue(activity.document.dirty)
                    EditorTestNavigation.command(activity,"File",0)
                    val shown=checkNotNull(ShadowAlertDialog.getLatestAlertDialog())
                    assertEquals(expected(tag,"ui_save_your_changes"),shadowOf(shown).title.toString())
                    assertEquals(expected(tag,"ui_your_current_image_has_unsaved_changes"),shadowOf(shown).message.toString())
                    assertEquals(expected(tag,"ui_save_a5d0d9"),shown.getButton(AlertDialog.BUTTON_POSITIVE).text.toString())
                    assertEquals(expected(tag,"ui_discard_changes23"),shown.getButton(AlertDialog.BUTTON_NEUTRAL).text.toString())
                    assertEquals(expected(tag,"ui_keep_editing23"),shown.getButton(AlertDialog.BUTTON_NEGATIVE).text.toString())
                    shown.getButton(AlertDialog.BUTTON_NEGATIVE).performClick();idle()
                    assertFalse(shown.isShowing);assertFalse(activity.isFinishing)
                    assertTrue(activity.document.dirty);assertTrue(bitmap.sameAs(activity.document.bitmap))
                    assertEquals(history,activity.document.historySnapshot())
                    assertNull(shadowOf(activity).nextStartedActivityForResult)
                }} finally {bitmap.recycle()}
            } finally {
                ShadowAlertDialog.getLatestAlertDialog()?.dismiss()
                controller.pause().stop().destroy();AppLanguage.select(RuntimeEnvironment.getApplication(),previousTag)
                PaintApplication.currentResources=previousResources;Locale.setDefault(previousLocale)
            }
        }
    }
'''
pos=s.rfind('\n}');s=s[:pos]+extra+s[pos:]
(P/'test-drafts/PersianHebrewUrduPriorityWordingTest.kt').write_text(s)
print('Prepared',s.count('@Test'),'meaningful JVM method drafts; not compiled, not installed, not accepted source')
