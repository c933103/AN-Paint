/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.local

import android.app.Activity
import android.app.AlertDialog
import android.app.Dialog
import android.content.ClipboardManager
import android.content.ClipData
import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Rect
import android.os.Looper
import android.os.SystemClock
import android.view.KeyEvent
import android.view.InputDevice
import android.view.MotionEvent
import android.view.View
import android.widget.EditText
import android.widget.ScrollView
import android.widget.ListView
import android.widget.TextView
import org.catrobat.paintroid.R
import org.catrobat.paintroid.classic.*
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode
import org.robolectric.shadows.ShadowAlertDialog
import org.robolectric.shadows.ShadowDisplayManager
import org.robolectric.shadows.ShadowViewRootImpl
import org.robolectric.shadow.api.Shadow
import org.robolectric.util.ReflectionHelpers
import java.io.File
import java.time.Duration
import java.util.Locale

/** Actual mounted geometry + scroll reveal + root-dispatched pointer input.
 * NATIVE captures are not physical-device or native-language acceptance. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk=[30,35],qualifiers="w320dp-h640dp-port-xhdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@LooperMode(LooperMode.Mode.PAUSED)
class LocalizedDialogLayoutTest {
    private val languages=listOf("en-US","hu","de","fr","pt-BR","ar","he","hi","th","ja","ko-Kore-KR","zh-TW","mn-Cyrl-MN","vi-Hani","wuu-Hans")
    private val noticeKeys=listOf(R.string.ui_icons_fonts_artwork_credits,R.string.ui_open_source_credits_and_notices,R.string.ui_gimp_translations31)
    // Long pending C05 wording is integration input only; production resources are untouched.
    private val c05Title="Nyílt forráskódú összetevők forrásmegjelölései és közleményei"
    private fun idle()=shadowOf(Looper.getMainLooper()).idle()
    private fun <T> withActivity(tag: String,block: (Activity)->T): T {
        val app=RuntimeEnvironment.getApplication() as Context
        val oldLocale=Locale.getDefault();val oldTag=AppLanguage.selectedTag(app);val oldResources=PaintApplication.currentResources
        AppLanguage.select(app,tag)
        val controller=Robolectric.buildActivity(Activity::class.java)
        controller.get().setTheme(R.style.ClassicPaintTheme)
        controller.setup().visible().windowFocusChanged(true)
        val activity=controller.get();AppLanguage.refresh(activity)
        try {return block(activity)} finally {
            controller.pause().stop().destroy();idle()
            AppLanguage.select(app,oldTag);PaintApplication.currentResources=oldResources;Locale.setDefault(oldLocale)
        }
    }
    private fun intrinsic(view: TextView) {
        val label=view.text.toString();val layout=requireNotNull(view.layout) {"No layout for $label"}
        val transformed=view.transformationMethod?.getTransformation(view.text,view)?.toString() ?: label
        assertTrue(label,layout.lineCount>0)
        assertEquals(label,transformed.length,layout.getLineEnd(layout.lineCount-1))
        for(line in 0 until layout.lineCount) {
            assertEquals("Ellipsized $label line $line",0,layout.getEllipsisCount(line))
            assertTrue("Horizontal clip $label",layout.getLineLeft(line)>=-1 && layout.getLineRight(line)<=layout.width+1)
        }
        assertTrue("Vertical clip $label: ${layout.height} > ${view.height}",layout.height<=view.height-view.totalPaddingTop-view.totalPaddingBottom)
    }
    /** Read every line through real ancestors; do not resize views or treat isShown as reachability. */
    private fun reveal(view: TextView) {
        intrinsic(view)
        val layout=view.layout
        for(line in 0 until layout.lineCount) {
            val lineRect=Rect(view.totalPaddingLeft,view.totalPaddingTop+layout.getLineTop(line),
                view.width-view.totalPaddingRight,view.totalPaddingTop+layout.getLineBottom(line))
            view.requestRectangleOnScreen(Rect(lineRect),true);idle()
            val visible=Rect();assertTrue("Not visible ${view.text}",view.getLocalVisibleRect(visible))
            assertTrue("Line $line not revealed: $lineRect in $visible: ${view.text}",visible.contains(lineRect))
        }
    }
    private fun tap(dialog: Dialog,view: TextView) {
        reveal(view);tapVisible(dialog,view)
    }
    private fun pointerState(root: View,view: View,phase: String,x: Float,y: Float) {
        val row=JSONObject().put("phase",phase).put("time",SystemClock.uptimeMillis()).put("text",(view as? TextView)?.text ?: view.contentDescription)
            .put("x",x).put("y",y).put("attached",view.isAttachedToWindow).put("touch_mode",view.isInTouchMode)
            .put("explicit_focusable",view.hasExplicitFocusable()).put("parent",view.parent?.javaClass?.name)
        val visible=Rect();view.getLocalVisibleRect(visible);row.put("visible",visible.toShortString())
        (view.parent as? ListView)?.let {list ->
            val target=IntArray(2);val origin=IntArray(2);list.getLocationOnScreen(target);root.getLocationOnScreen(origin)
            row.put("hit_position",list.pointToPosition((x+origin[0]-target[0]).toInt(),(y+origin[1]-target[1]).toInt()))
                .put("row_position",list.getPositionForView(view)).put("first",list.firstVisiblePosition).put("last",list.lastVisiblePosition)
            for(field in listOf("mTouchMode","mMotionPosition","mDataChanged","mIsDetaching")) {
                row.put(field,try {ReflectionHelpers.getField<Any>(list,field)} catch(_: RuntimeException) {"unavailable"})
            }
        }
        val directory=File("build/reports/localized-dialog-layout").apply {mkdirs()}
        File(directory,"pointer-api${RuntimeEnvironment.getApiLevel()}-${Locale.getDefault().toLanguageTag()}.jsonl").appendText(row.toString()+"\n")
    }
    private fun tapVisible(dialog: Dialog,view: View) {
        val visible=Rect();assertTrue(view.getLocalVisibleRect(visible))
        val root=dialog.window!!.decorView;val target=IntArray(2);val origin=IntArray(2)
        view.getLocationOnScreen(target);root.getLocationOnScreen(origin)
        val x=(target[0]-origin[0]+visible.centerX()).toFloat();val y=(target[1]-origin[1]+visible.centerY()).toFloat()
        pointerState(root,view,"before-down",x,y)
        val time=SystemClock.uptimeMillis()
        for(action in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP)) {
            if(action==MotionEvent.ACTION_UP) shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(40))
            val event=MotionEvent.obtain(time,SystemClock.uptimeMillis(),action,x,y,0).apply {source=InputDevice.SOURCE_TOUCHSCREEN}
            try {assertTrue("Pointer event was not handled for ${view.tag}",root.dispatchTouchEvent(event))} finally {event.recycle()}
            pointerState(root,view,"after-$action",x,y)
        }
        // ListView retains its real pressed-state delay before delivering an item click.
        shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(200))
        pointerState(root,view,"after-click-delay",x,y)
    }
    private fun back(dialog: Dialog) {
        dialog.dispatchKeyEvent(KeyEvent(KeyEvent.ACTION_DOWN,KeyEvent.KEYCODE_BACK))
        dialog.dispatchKeyEvent(KeyEvent(KeyEvent.ACTION_UP,KeyEvent.KEYCODE_BACK));idle();assertFalse(dialog.isShowing)
    }
    private fun capture(dialog: Dialog,name: String,labels: List<TextView>) {
        val root=dialog.window!!.decorView;val rows=JSONArray()
        labels.forEach {view ->
            reveal(view);val visible=Rect();view.getLocalVisibleRect(visible)
            rows.put(JSONObject().put("text",view.text).put("width",view.width).put("height",view.height)
                .put("layout_height",view.layout.height).put("line_count",view.lineCount).put("visible_rect",visible.toShortString()))
        }
        val directory=File("build/reports/localized-dialog-layout").apply {mkdirs()}
        val config=root.resources.configuration
        val prefix="api${RuntimeEnvironment.getApiLevel()}-${config.screenWidthDp}x${config.screenHeightDp}-font${config.fontScale}-${Locale.getDefault().toLanguageTag()}-$name"
        val bitmap=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
        try {root.draw(Canvas(bitmap));File(directory,"$prefix.png").outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {bitmap.recycle()}
        File(directory,"$prefix.json").writeText(JSONObject().put("evidence_kind","Robolectric NATIVE; no physical-device or linguistic acceptance")
            .put("intrinsic_fit_asserted",true).put("each_line_scroll_reveal_asserted",true).put("labels",rows).toString(2)+"\n")
    }
    private fun noticeAndChooser(tags: List<String>) {
        for(tag in tags) withActivity(tag) {activity ->
            val text="VERBATIM body: 100% %1\$s\nhttps://example.org/?x=a&y=b\n"+(1..18).joinToString("\n") {"Clause $it: source text remains unchanged."}
            for(key in noticeKeys) {
                val dialog=LegalInfo.termsDialog(activity,ui(key),text);dialog.show();idle()
                try {
                    val root=dialog.window!!.decorView
                    val heading=root.findViewWithTag<TextView>("terms_title")
                    val body=root.findViewWithTag<TextView>("terms_text")
                    assertEquals(text,body.text.toString());reveal(heading);reveal(body)
                    val copy=root.findViewWithTag<TextView>("terms_copy");val more=root.findViewWithTag<TextView>("terms_more");val done=root.findViewWithTag<TextView>("terms_done")
                    for(action in listOf(copy,more,done)) reveal(action)
                    tap(dialog,copy)
                    assertEquals(text,(activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip!!.getItemAt(0).text.toString())
                    assertTrue(dialog.isShowing)
                    if(key==noticeKeys.first()) {
                        capture(dialog,"notice",listOf(heading,copy,more,done))
                        tap(dialog,more)
                        val options=ShadowAlertDialog.getLatestAlertDialog();assertTrue(options.isShowing)
                        tap(options,options.getButton(AlertDialog.BUTTON_NEGATIVE));assertFalse(options.isShowing);assertTrue(dialog.isShowing)
                    }
                    tap(dialog,done);assertFalse(dialog.isShowing)
                } finally {dialog.dismiss()}
            }
            var chosen=-1;var choiceCalls=0
            val labels=noticeKeys.map {ui(it)}.toTypedArray()
            val chooser=EditorDialogBuilder(activity).setScrollableTitle(ui(R.string.ui_about_credits23)).setItems(labels) {_,index->chosen=index;choiceCalls++}
                .setNegativeButton(ui(R.string.ui_done),null).show();idle()
            try {
                val heading=chooser.window!!.decorView.findViewWithTag<TextView>("dialog_title");reveal(heading)
                for(index in labels.indices) {
                    chooser.listView.setSelectionFromTop(index,0);idle()
                    val row=chooser.listView.getChildAt(index-chooser.listView.firstVisiblePosition) as TextView
                    assertEquals(labels[index],row.text.toString());reveal(row)
                }
                chooser.listView.setSelectionFromTop(labels.lastIndex,0);idle()
                val last=chooser.listView.getChildAt(labels.lastIndex-chooser.listView.firstVisiblePosition) as TextView
                capture(chooser,"chooser",listOf(heading,last,chooser.getButton(AlertDialog.BUTTON_NEGATIVE)))
                tap(chooser,last);assertEquals(labels.lastIndex,chosen);assertEquals(1,choiceCalls);assertFalse(chooser.isShowing)
            } finally {chooser.dismiss()}
            val repeated=EditorDialogBuilder(activity).setScrollableTitle(c05Title).setMessage(text).setNegativeButton(ui(R.string.ui_cancel),null).show();idle()
            reveal(repeated.window!!.decorView.findViewWithTag("dialog_title"));back(repeated)
        }
    }
    @Test @Config(fontScale=1f) fun normalNarrowPortrait()=noticeAndChooser(listOf("en-US","hu"))
    @Test @Config(fontScale=2f) fun largeNarrowPortrait()=noticeAndChooser(languages)
    @Test @Config(fontScale=1f,qualifiers="w640dp-h320dp-land-xhdpi") fun normalShortLandscape()=noticeAndChooser(listOf("en-US","hu"))
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi") fun largeShortLandscape()=noticeAndChooser(languages)


    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun verticalNoticeColumnsAndActionsRemainUnclippedAndReachable() {
        for(tag in listOf("mn-Mong","mnc-Mong","lzh-Hant","en-XV","qaa-Zsye-XV")) withActivity(tag) {activity ->
            val text="Verbatim licence body\n100% %1\$s\nhttps://example.org/source"
            val dialog=LegalInfo.termsDialog(activity,ui(R.string.ui_icons_fonts_artwork_credits),text);dialog.show();idle()
            try {
                val root=dialog.window!!.decorView
                val controls=listOf("terms_title","terms_copy","terms_more","terms_done").map {root.findViewWithTag<TextView>(it)}
                val rows=JSONArray()
                for(view in controls) {
                    val caption=VerticalText.wrapLabel(view.text.toString(),view.paint,96*view.resources.displayMetrics.density)
                    val bounds=VerticalText.bounds(caption,view.paint,VerticalText.uiDirection(),GlyphOrientation.MIXED,1f)
                    assertTrue("Column width ${view.text}",view.width>=kotlin.math.ceil(bounds.width()).toInt()+view.paddingLeft+view.paddingRight)
                    assertTrue("Column height ${view.text}",view.height>=kotlin.math.ceil(bounds.height()).toInt()+view.paddingTop+view.paddingBottom)
                    for(x in listOf(0,(view.width-16).coerceAtLeast(0))) for(y in listOf(0,(view.height-16).coerceAtLeast(0))) {
                        val tile=Rect(x,y,minOf(view.width,x+16),minOf(view.height,y+16))
                        view.requestRectangleOnScreen(Rect(tile),true);idle()
                        val visible=Rect();assertTrue(view.getLocalVisibleRect(visible));assertTrue("Column edge $tile in $visible",visible.contains(tile))
                    }
                    rows.put(JSONObject().put("text",view.text).put("width",view.width).put("height",view.height).put("column_bounds",bounds.toString()))
                }
                val directory=File("build/reports/localized-dialog-layout").apply {mkdirs()}
                val name="api${RuntimeEnvironment.getApiLevel()}-vertical-$tag"
                val bitmap=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
                try {root.draw(Canvas(bitmap));File(directory,"$name.png").outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {bitmap.recycle()}
                File(directory,"$name.json").writeText(JSONObject().put("evidence_kind","Robolectric NATIVE vertical intrinsic bounds and edge reveal; not physical-device acceptance")
                    .put("controls",rows).toString(2)+"\n")
                val copy=controls[1];copy.requestRectangleOnScreen(Rect(0,0,minOf(16,copy.width),minOf(16,copy.height)),true);idle();tapVisible(dialog,copy)
                assertEquals(text,(activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip!!.getItemAt(0).text.toString())
                val feedback=requireNotNull(root.findViewWithTag<VerticalFeedbackCard>("locale_notification_card"))
                val copied=activity.getString(R.string.ui_full_text_copied)
                assertEquals(copied,feedback.viewport.message.text.toString())
                assertEquals(copied,feedback.viewport.message.createAccessibilityNodeInfo().text.toString())
                // At 2×, an indivisible localized word can overflow even this
                // short confirmation. Such a card intentionally owns inside
                // touches: dismiss it once before pressing the underlying Done.
                if(feedback.persistent) {
                    assertFalse(feedback.deferred)
                    val dismiss=feedback.dismissControl
                    assertEquals(View.VISIBLE,dismiss.visibility)
                    val visible=Rect();assertTrue(dismiss.getLocalVisibleRect(visible))
                    assertTrue(visible.contains(Rect(0,0,dismiss.width,dismiss.height)))
                    val minimum=(44*dismiss.resources.displayMetrics.density).toInt()
                    assertTrue(dismiss.width>=minimum);assertTrue(dismiss.height>=minimum)
                    val node=dismiss.createAccessibilityNodeInfo()
                    assertEquals(activity.getString(R.string.ui_done),
                        (if(dismiss is TextView) node.text else node.contentDescription).toString())
                    tapVisible(dialog,dismiss)
                    assertNull(root.findViewWithTag<View>("locale_notification"))
                    assertTrue(dialog.isShowing)
                } else assertFalse(feedback.hasOverflow)
                // Fitting feedback stays in place: this also proves its touch
                // transparency, without waiting for or shortening its timeout.
                val done=controls[3];done.requestRectangleOnScreen(Rect(0,0,minOf(16,done.width),minOf(16,done.height)),true);idle();tapVisible(dialog,done);assertFalse(dialog.isShowing)
            } finally {dialog.dismiss()}
        }
    }

    @Test @Config(fontScale=2f)
    fun noticeColumnsClampOffsetsAcrossContentAndViewportChanges() {
        for(tag in listOf("lzh-Hant","mn-Mong")) withActivity(tag) {activity ->
            val columns=ResponsiveDialogColumns(activity)
            val child=View(activity)
            columns.addView(child,android.widget.FrameLayout.LayoutParams(1200,120))
            val rightToLeft=VerticalText.uiDirection()==TextDirection.VERTICAL_RL
            assertEquals(tag=="lzh-Hant",rightToLeft)
            fun range()=(child.width-columns.width).coerceAtLeast(0)
            fun offset()=if(rightToLeft) range()-columns.scrollX else columns.scrollX
            fun layout(width: Int,contentWidth: Int=1200) {
                // HorizontalScrollView measures its child with an unspecified width.
                // A bare View needs intrinsic content; LayoutParams alone yield zero width.
                child.minimumWidth=contentWidth
                child.layoutParams=child.layoutParams.apply {this.width=contentWidth}
                columns.requestLayout()
                columns.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(120,View.MeasureSpec.EXACTLY))
                columns.layout(0,0,width,120)
                assertEquals("Synthetic child's intrinsic width",contentWidth,child.width)
                assertEquals((contentWidth-width).coerceAtLeast(0),range())
            }
            layout(400);assertEquals(0,offset())
            layout(160);assertEquals(0,offset())
            layout(400);assertEquals(0,offset())
            assertTrue("The offset fixture must actually overflow",range()>73)
            columns.scrollTo(if(rightToLeft) range()-73 else 73,0)
            assertEquals("Reader offset must be established before resize",73,offset())
            layout(160);assertEquals(73,offset())
            layout(500);assertEquals(73,offset())
            layout(500);assertEquals("Same-size layout must retain reader position",73,offset())
            layout(500,680);assertEquals(73,offset())
            layout(500,520);assertEquals("Clamp to the shorter content range",20,offset())
            layout(500,120);assertEquals(0,offset())
            layout(500,1200);assertEquals(0,offset())

            // Native deferred focus navigation on a same-range layout must win over anchoring.
            val focusColumns=ResponsiveDialogColumns(activity).apply {isSmoothScrollingEnabled=false}
            val row=android.widget.LinearLayout(activity)
            val first=android.widget.Button(activity).apply {text="First";isFocusableInTouchMode=true}
            val last=android.widget.Button(activity).apply {text="Last";isFocusableInTouchMode=true}
            row.addView(first,android.widget.LinearLayout.LayoutParams(200,120))
            row.addView(View(activity),android.widget.LinearLayout.LayoutParams(800,120))
            row.addView(last,android.widget.LinearLayout.LayoutParams(200,120))
            focusColumns.addView(row)
            fun focusLayout(width: Int=400) {
                focusColumns.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),View.MeasureSpec.makeMeasureSpec(120,View.MeasureSpec.EXACTLY))
                focusColumns.layout(0,0,width,120)
            }
            focusLayout()
            val target=if(rightToLeft) first else last
            focusColumns.requestLayout();assertTrue(target.requestFocus());focusLayout()
            assertSame(target,focusColumns.findFocus())
            assertTrue(target.left>=focusColumns.scrollX)
            assertTrue(target.right<=focusColumns.scrollX+focusColumns.width)
            focusColumns.requestLayout();focusLayout(240)
            assertSame(target,focusColumns.findFocus())
            assertTrue("Focused control wins over reader anchoring on resize",target.left>=focusColumns.scrollX)
            assertTrue(target.right<=focusColumns.scrollX+focusColumns.width)
        }
    }

    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun retainedVerticalNoticeKeepsReadingOffsetAcrossRotation() {
        for(tag in listOf("lzh-Hant","mn-Mong")) withActivity(tag) {activity ->
            // Deliberately overflowing captions stress the real notice rails, not production wording.
            val dialog=LegalInfo.termsDialog(activity,ui(R.string.ui_icons_fonts_artwork_credits).repeat(20),"Unchanged body")
            for(name in listOf("terms_copy","terms_more","terms_done")) {
                val action=dialog.window!!.decorView.findViewWithTag<TextView>(name)
                action.text=action.text.toString().repeat(20)
            }
            dialog.show();idle()
            val root=dialog.window!!.decorView
            val rails=listOf("terms_title_scroll","terms_actions_scroll").map {root.findViewWithTag<ScrollView>(it).getChildAt(0) as ResponsiveDialogColumns}
            val selectedLocales=activity.resources.configuration.locales
            val expectedDirection=if(tag=="lzh-Hant") TextDirection.VERTICAL_RL else TextDirection.VERTICAL_LR
            val rightToLeft=tag=="lzh-Hant"
            fun assertSelectedResources() {
                assertEquals(tag,AppLanguage.selectedTag(activity))
                assertEquals(tag,selectedLocales[0].toLanguageTag())
                for(context in listOf(activity,dialog.context,root.context)+rails.map {it.context}) {
                    assertEquals("Retained notice keeps the selected resource locales",selectedLocales,context.resources.configuration.locales)
                    assertEquals("Retained notice keeps its reading direction",expectedDirection,VerticalText.uiDirection(context))
                }
            }
            assertSelectedResources()
            fun range(rail: ResponsiveDialogColumns)=(rail.getChildAt(0).width-rail.width+rail.paddingLeft+rail.paddingRight).coerceAtLeast(0)
            fun offset(rail: ResponsiveDialogColumns)=if(rightToLeft) range(rail)-rail.scrollX else rail.scrollX
            try {
                for(readerOffset in listOf(0,47)) {
                    rails.forEach {assertTrue(range(it)>47);it.scrollTo(if(rightToLeft) range(it)-readerOffset else readerOffset,0)}
                    for((index,qualifiers) in listOf("w320dp-h640dp-port-xhdpi","w640dp-h320dp-land-xhdpi").withIndex()) {
                        resizeDisplay(activity,root,qualifiers)
                        assertSelectedResources()
                        // API35 can scope callbacks to the Activity; older APIs delegate to Application.
                        activity.onConfigurationChanged(activity.resources.configuration)
                        activity.application.onConfigurationChanged(activity.resources.configuration);idle()
                        assertSelectedResources()
                        assertTrue(dialog.isShowing)
                        assertEquals((activity.resources.displayMetrics.widthPixels*.94f).toInt(),dialog.window!!.attributes.width)
                        val rows=JSONArray()
                        for((railIndex,rail) in rails.withIndex()) {
                            assertSame(rail,root.findViewWithTag<ScrollView>(if(railIndex==0) "terms_title_scroll" else "terms_actions_scroll").getChildAt(0))
                            assertTrue(range(rail)>47);assertEquals(readerOffset,offset(rail))
                            rail.requestLayout();idle();assertEquals(readerOffset,offset(rail))
                            rows.put(JSONObject().put("range",range(rail)).put("scroll_x",rail.scrollX).put("reading_offset",offset(rail)).put("viewport_width",rail.width))
                        }
                        assertEquals("Unchanged body",root.findViewWithTag<TextView>("terms_text").text.toString())
                        val directory=File("build/reports/localized-dialog-layout").apply {mkdirs()}
                        val name="api${RuntimeEnvironment.getApiLevel()}-retained-vertical-$tag-offset$readerOffset-$index"
                        val bitmap=Bitmap.createBitmap(root.width,root.height,Bitmap.Config.ARGB_8888)
                        try {root.draw(Canvas(bitmap));File(directory,"$name.png").outputStream().use {assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG,100,it))}} finally {bitmap.recycle()}
                        File(directory,"$name.json").writeText(JSONObject().put("evidence_kind","Retained Robolectric NATIVE notice rotation and programmatic reader-offset preservation; oversized test captions; not installed input acceptance")
                            .put("rails",rows).toString(2)+"\n")
                    }
                }
                back(dialog)
                val dismissedWidth=dialog.window!!.attributes.width
                RuntimeEnvironment.setQualifiers("w320dp-h640dp-port-xhdpi")
                @Suppress("DEPRECATION")
                activity.resources.updateConfiguration(Resources.getSystem().configuration,Resources.getSystem().displayMetrics)
                activity.onConfigurationChanged(activity.resources.configuration)
                activity.application.onConfigurationChanged(activity.resources.configuration);idle()
                assertEquals("Dismissed notice must unregister its resize callback",dismissedWidth,dialog.window!!.attributes.width)
            } finally {dialog.dismiss();RuntimeEnvironment.setQualifiers("w640dp-h320dp-land-xhdpi")}
        }
    }


    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun pointerSwipesScrollTitleAndFooterWithoutInvokingActions()=withActivity("hu") {activity ->
        val clipboard=activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("sentinel","Swipe must not copy"))
        val previousAlert=ShadowAlertDialog.getLatestAlertDialog()
        val dialog=LegalInfo.termsDialog(activity,c05Title+" "+c05Title,"Unchanged body")
        // Oversized-caption stress fixture on the real controls/listeners; production wording is unchanged.
        for(tag in listOf("terms_copy","terms_more","terms_done")) dialog.window!!.decorView.findViewWithTag<TextView>(tag).text=c05Title
        dialog.show();idle()
        try {
            val root=dialog.window!!.decorView
            for(tag in listOf("terms_title_scroll","terms_actions_scroll")) {
                val scroll=root.findViewWithTag<ScrollView>(tag)
                assertTrue(tag,scroll.getChildAt(0).height>scroll.height)
                val before=scroll.scrollY;val location=IntArray(2);val origin=IntArray(2)
                scroll.getLocationOnScreen(location);root.getLocationOnScreen(origin)
                val x=location[0]-origin[0]+scroll.width*.5f
                val start=location[1]-origin[1]+scroll.height*.85f
                val end=location[1]-origin[1]+scroll.height*.15f
                val time=SystemClock.uptimeMillis()
                for(step in 0..10) {
                    val action=when(step) {0->MotionEvent.ACTION_DOWN;10->MotionEvent.ACTION_UP;else->MotionEvent.ACTION_MOVE}
                    if(step>0) shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(20))
                    val event=MotionEvent.obtain(time,SystemClock.uptimeMillis(),action,x,start+(end-start)*step/10,0).apply {source=InputDevice.SOURCE_TOUCHSCREEN}
                    try {assertTrue(root.dispatchTouchEvent(event))} finally {event.recycle()}
                }
                // Let the real fling finish; a DOWN during a fling is a stop gesture, not a button tap.
                shadowOf(Looper.getMainLooper()).idleFor(Duration.ofSeconds(3))
                val settled=scroll.scrollY
                shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(250))
                assertEquals("Scroll must settle before the independent tap",settled,scroll.scrollY)
                assertTrue("Native swipe did not scroll $tag",scroll.scrollY>before);assertTrue(dialog.isShowing)
                assertEquals("Swipe must not copy",clipboard.primaryClip!!.getItemAt(0).text.toString())
                assertSame("Swipe must not open Other terms",previousAlert,ShadowAlertDialog.getLatestAlertDialog())
            }
            tap(dialog,root.findViewWithTag("terms_done"));assertFalse(dialog.isShowing)
        } finally {dialog.dismiss()}
    }

    @Test @Config(fontScale=2f)
    fun retainedAboutTitleResizesWithoutReplacingItsNativeList()=withActivity("hu") {activity ->
        var chosen=-1;var choiceCalls=0
        val dialog=EditorDialogBuilder(activity).setScrollableTitle(c05Title)
            .setItems(arrayOf(ui(R.string.ui_done),ui(R.string.ui_cancel))) {_,index->chosen=index;choiceCalls++}.show();idle()
        val root=dialog.window!!.decorView;val list=dialog.listView;val adapter=list.adapter;val before=root.width
        try {
            for((index,qualifiers) in listOf("w640dp-h320dp-land-xhdpi","w320dp-h640dp-port-xhdpi").withIndex()) {
                resizeDisplay(activity,root,qualifiers)
                assertSame(list,dialog.listView);assertSame(adapter,list.adapter)
                if(index==0) assertTrue(root.width>before) else assertEquals(before,root.width)
                val title=root.findViewWithTag<TextView>("dialog_title");reveal(title)
                assertTrue(root.findViewWithTag<ScrollView>("dialog_title_scroll").height<root.height/2)
                assertTrue(list.height>0);capture(dialog,"retained-about-$index",listOf(title))
            }
            val row=list.getChildAt(0) as TextView;tap(dialog,row)
            assertEquals(list.firstVisiblePosition,chosen);assertEquals(1,choiceCalls);assertFalse(dialog.isShowing)
        } finally {dialog.dismiss();RuntimeEnvironment.setQualifiers("w320dp-h640dp-port-xhdpi")}
    }

    private fun resizeDisplay(activity: Activity,root: View,qualifiers: String) {
        val selectedLocales=activity.resources.configuration.locales
        RuntimeEnvironment.setQualifiers(qualifiers)
        // This plain Activity has no app-locale callback. setQualifiers replaces
        // resources after its first display notification; restore the selected
        // locale before changeDisplay drains the next resize-triggered traversal.
        @Suppress("DEPRECATION")
        activity.resources.updateConfiguration(Configuration(Resources.getSystem().configuration).apply {
            setLocales(selectedLocales)
        },Resources.getSystem().displayMetrics)
        fun assertSelectedResources() {
            assertEquals(selectedLocales,activity.resources.configuration.locales)
            assertEquals(selectedLocales,root.context.resources.configuration.locales)
        }
        assertSelectedResources()
        ShadowDisplayManager.changeDisplay(root.display.displayId,qualifiers)
        // Resources-only changes leave Robolectric 4.14's ViewRoot frame stale.
        // Deliver its supported resize callback; never directly measure a child.
        Shadow.extract<ShadowViewRootImpl>(root.parent).callDispatchResized();idle()
        assertSelectedResources()
        root.dispatchConfigurationChanged(activity.resources.configuration);idle()
        assertSelectedResources()
    }

    @Test @Config(fontScale=2f)
    fun configurationDispatchResizesAnOpenEditorWithoutLosingDraftOrCallbacks()=withActivity("hu") {activity ->
        val original=ImageCredit("https://example.org/rotate.png","Original")
        var calls=0
        val dialog=GalleryCredits.showEditor(activity,listOf(original)) {_,_->calls++}!!.dialog;idle()
        val root=dialog.window!!.decorView
        val field=root.findViewWithTag<EditText>("gallery_credit_text");field.setText("Unsaved rotation draft");field.setSelection(3,8);idle()
        val before=root.width
        try {
            for((index,qualifiers) in listOf("w640dp-h320dp-land-xhdpi","w320dp-h640dp-port-xhdpi").withIndex()) {
                resizeDisplay(activity,root,qualifiers)
                assertSame(field,root.findViewWithTag<EditText>("gallery_credit_text"))
                assertEquals("Unsaved rotation draft",field.text.toString());assertEquals(index,calls)
                assertEquals(3,field.selectionStart);assertEquals(8,field.selectionEnd)
                if(index==0) assertTrue(root.width>before)
                else assertEquals(before,root.width)
                reveal(field)
                tap(dialog,root.findViewWithTag("gallery_credit_save"));assertEquals(index+1,calls);assertTrue(dialog.isShowing)
            }
            back(dialog);assertEquals(2,calls)
        } finally {dialog.dismiss();RuntimeEnvironment.setQualifiers("w320dp-h640dp-port-xhdpi")}
    }

    @Test @Config(fontScale=1f,qualifiers="w640dp-h320dp-land-xhdpi")
    fun advancedColourRetainsItsBoundedHolderAndFixedControls()=withActivity("en-US") {activity ->
        var committed=0;var closed=0
        val dialog=AdvancedColourDialog(activity,android.graphics.Color.RED,false,closed={closed++},initialMode=1) {committed++}.show();idle()
        try {
            val root=dialog.window!!.decorView
            val holder=root.findViewWithTag<View>("colour_dialog_holder")
            assertFalse("Retain native bounded custom holder",holder.parent is ScrollView)
            val inner=root.findViewWithTag<ScrollView>("colour_editor_scroll")
            assertTrue(inner.height>0);assertTrue(inner.getChildAt(0).height>inner.height)
            val fixed=listOf("colour_advanced_tab","custom_colours_panel","add_custom_colour").map {root.findViewWithTag<View>(it)}
            fun bounds(view: View): Rect {
                val position=IntArray(2);view.getLocationOnScreen(position)
                val full=Rect(position[0],position[1],position[0]+view.width,position[1]+view.height)
                val visible=Rect();assertTrue(view.getGlobalVisibleRect(visible));assertEquals(full,visible)
                return full
            }
            val before=fixed.map {bounds(it)}
            inner.fullScroll(View.FOCUS_DOWN);shadowOf(Looper.getMainLooper()).idleFor(Duration.ofMillis(500));assertTrue(inner.scrollY>0)
            assertEquals(before,fixed.map {bounds(it)})
            tap(dialog,dialog.getButton(AlertDialog.BUTTON_NEGATIVE));assertFalse(dialog.isShowing)
            assertEquals(0,committed);assertEquals(1,closed)
        } finally {dialog.dismiss()}
    }

    @Test fun outsideDismissalCallsCancelOnceAndNeverRunsAnAction()=withActivity("en-US") {activity ->
        var cancelled=0;var actions=0
        val dialog=EditorDialogBuilder(activity).setTitle("Cancel fixture").setMessage("Unchanged")
            .setPositiveButton("Accept") {_,_->actions++}.setOnCancelListener {cancelled++}.show();idle()
        dialog.setCanceledOnTouchOutside(true)
        val time=SystemClock.uptimeMillis()
        var handled=false
        for(action in listOf(MotionEvent.ACTION_DOWN,MotionEvent.ACTION_UP)) {
            val event=MotionEvent.obtain(time,time+if(action==MotionEvent.ACTION_UP) 40 else 0,action,-1000f,-1000f,0)
            try {handled=dialog.dispatchTouchEvent(event)||handled} finally {event.recycle()}
        }
        idle();assertTrue(handled);assertFalse(dialog.isShowing);assertEquals(1,cancelled);assertEquals(0,actions)
    }

    private fun creditEditor()=withActivity("hu") {activity ->
        val original=ImageCredit("https://example.org/fixture.png","Original author\nCC BY 4.0")
        var saved=original;var dismissed=0;var saves=0;var reject=false
        fun open()=GalleryCredits.showEditor(activity,listOf(saved),null,{source,text->saves++;if(reject) throw java.io.IOException("Fixture rejection");saved=ImageCredit(source,text)},{dismissed++})!!.dialog.also {idle()}
        val dialog=open()
        try {
            val root=dialog.window!!.decorView
            val field=root.findViewWithTag<EditText>("gallery_credit_text")
            val value="Unmodified 100% %1\$s\nCreator\nhttps://example.org/source?a=1&b=2"
            field.setText(value);idle();reveal(field)
            val copy=root.findViewWithTag<TextView>("gallery_credit_copy");val save=root.findViewWithTag<TextView>("gallery_credit_save");val done=root.findViewWithTag<TextView>("gallery_credit_done")
            tap(dialog,copy);assertEquals(1,saves);assertEquals(value,saved.text)
            assertEquals(value,(activity.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager).primaryClip!!.getItemAt(0).text.toString())
            field.setText("$value\nEdited");idle();tap(dialog,save);assertEquals(2,saves);assertEquals("$value\nEdited",saved.text);assertTrue(dialog.isShowing)
            capture(dialog,"editor",listOf(copy,save,done))
            reject=true;tap(dialog,done);assertEquals(3,saves);assertTrue(dialog.isShowing);assertEquals(0,dismissed)
            reject=false;tap(dialog,done);assertEquals(4,saves);assertFalse(dialog.isShowing);assertEquals(1,dismissed)
            val reopened=open();assertEquals(saved.text,reopened.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").text.toString())
            reopened.window!!.decorView.findViewWithTag<EditText>("gallery_credit_text").setText("Unsaved draft")
            back(reopened);assertEquals(4,saves);assertEquals("$value\nEdited",saved.text);assertEquals(2,dismissed)
        } finally {dialog.dismiss()}
    }
    @Test @Config(fontScale=2f) fun editorPointerCopySaveDoneAndBackAtLargeText()=creditEditor()
    @Test @Config(fontScale=2f,qualifiers="w640dp-h320dp-land-xhdpi") fun editorPointerCopySaveDoneAndBackInShortLandscape()=creditEditor()
}
