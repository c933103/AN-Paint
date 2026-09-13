/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.app.AlertDialog
import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.RectF
import android.text.SpannableString
import android.text.Spanned
import android.text.TextWatcher
import android.text.Editable
import android.text.style.ReplacementSpan
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.*
import kotlin.math.ceil

/** Vertical controls use columns and intrinsic sizes, not the horizontal layout's fixed rectangles. */
internal object VerticalUi {
    private fun dp(view: View,n: Int)=(n*view.resources.displayMetrics.density+.5f).toInt()
    private class Caption(private val value: String,private val height: Float,private val direction: TextDirection,private val font: android.graphics.Typeface?=null): ReplacementSpan() {
        private fun styled(paint: Paint)=if(font==null) paint else Paint(paint).apply {typeface=font}
        private fun label(paint: Paint)=VerticalText.wrapLabel(value,paint,height,direction)
        private fun box(paint: Paint)=VerticalText.bounds(label(paint),paint,direction,GlyphOrientation.MIXED,1f)
        override fun getSize(paint: Paint,text: CharSequence,start: Int,end: Int,fm: Paint.FontMetricsInt?): Int {
            val b=box(styled(paint));fm?.let {it.ascent=-ceil(b.height()).toInt();it.top=it.ascent;it.descent=0;it.bottom=0;it.leading=0}
            return ceil(b.width()).toInt()
        }
        override fun draw(canvas: Canvas,text: CharSequence,start: Int,end: Int,x: Float,top: Int,y: Int,bottom: Int,paint: Paint) {
            val ink=styled(paint)
            canvas.save();canvas.translate(x,y-box(ink).height());VerticalText.draw(canvas,label(ink),ink,direction,GlyphOrientation.MIXED);canvas.restore()
        }
    }
    fun caption(view: TextView,heightDp: Int=144,direction: TextDirection=VerticalText.uiDirection()) {
        if(direction==TextDirection.HORIZONTAL || view is EditText || view is FlowButton || view is FlowTextView) return
        if(view.getTag(org.catrobat.paintroid.R.id.vertical_caption_installed)==true) return
        view.setTag(org.catrobat.paintroid.R.id.vertical_caption_installed,true)
        view.setSingleLine(false);view.maxLines=Int.MAX_VALUE;view.ellipsize=null
        VerticalText.uiTypeface(view.context)?.let {view.typeface=it}
        if(view is Button) view.isAllCaps=false
        var changing=false
        fun update() {
            if(changing) return
            changing=true
            val value=view.text.toString()
            view.text=SpannableString(value).apply {if(isNotEmpty()) setSpan(Caption(value,dp(view,heightDp).toFloat(),direction),0,length,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)}
            changing=false
        }
        view.addTextChangedListener(object: TextWatcher {
            override fun beforeTextChanged(s: CharSequence?,start: Int,count: Int,after: Int)=Unit
            override fun onTextChanged(s: CharSequence?,start: Int,before: Int,count: Int)=Unit
            override fun afterTextChanged(s: Editable?)=update()
        });update()
    }
    fun languageChoice(view: TextView) {
        val autonym="ᠮᠣᠩᠭᠤᠯ ᠬᠡᠯᠡ"
        val value=autonym+"  Mongolian\n[mn-Mong]"
        // Only the autonym uses Mongolian glyphs. A dedicated second line keeps
        // the language code visible even at narrow widths and large font sizes.
        view.typeface=android.graphics.Typeface.DEFAULT
        view.setSingleLine(false);view.maxLines=Int.MAX_VALUE;view.ellipsize=null
        // The dialog theme's single-choice row can have a fixed 48 dp height.
        // Let the real ListView measure the vertical autonym and code together.
        view.layoutParams=AbsListView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT)
        view.setPaddingRelative(view.paddingStart,dp(view,8),view.paddingEnd,dp(view,8))
        val font=android.graphics.Typeface.createFromAsset(view.context.assets,"fonts/notosansmongolian.ttf")
        view.text=SpannableString(value).apply {setSpan(Caption(autonym,dp(view,120).toFloat(),TextDirection.VERTICAL_LR,font),0,autonym.length,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)}
    }
    private class VerticalChoices(private val source: SpinnerAdapter,private val height: Int): BaseAdapter() {
        override fun getCount()=source.count
        override fun getItem(position: Int)=source.getItem(position)
        override fun getItemId(position: Int)=source.getItemId(position)
        override fun getView(position: Int,convertView: View?,parent: ViewGroup): View = source.getView(position,convertView,parent).also {
            if(it is TextView) caption(it,height)
            it.layoutParams=ViewGroup.LayoutParams(-2,-2)
        }
        override fun getDropDownView(position: Int,convertView: View?,parent: ViewGroup): View = source.getDropDownView(position,convertView,parent).also {
            if(it is TextView) caption(it,height)
            it.layoutParams=AbsListView.LayoutParams(-1,-2)
        }
    }
    fun spinner(view: Spinner,heightDp: Int=144) {
        if(!VerticalText.uiVertical() || view.adapter is VerticalChoices) return
        view.minimumWidth=dp(view,112)
        val position=view.selectedItemPosition
        view.adapter=VerticalChoices(view.adapter,heightDp);view.setSelection(position)
    }
    fun panel(panel: LinearLayout,heightDp: Int=112) {
        panel.orientation=LinearLayout.HORIZONTAL;panel.isBaselineAligned=false;panel.gravity=Gravity.TOP
        panel.layoutDirection=if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) View.LAYOUT_DIRECTION_RTL else View.LAYOUT_DIRECTION_LTR
        for(i in 0 until panel.childCount) {
            val child=panel.getChildAt(i)
            if(child is FlowButton) child.columnHeightDp=heightDp
            if(child is FlowTextView) child.columnHeightDp=heightDp
            if(child is TextView) caption(child,heightDp)
            if(child is Spinner) spinner(child,heightDp)
            if(child is LinearLayout && child !is NumericSlider) panel(child,heightDp)
            val spatial=child !is TextView && child !is ViewGroup
            val previousHeight=child.layoutParams?.height ?: -2
            child.layoutParams=LinearLayout.LayoutParams(if(spatial) dp(child,240) else if(child is NumericSlider || child is EditText) dp(child,176) else -2,
                if(spatial) previousHeight.takeIf {it>0} ?: dp(child,180) else -2).apply {
                setMargins(dp(child,5),dp(child,4),dp(child,5),dp(child,4))
            }
        }
    }
    fun detach(view: View): View { (view.parent as? ViewGroup)?.removeView(view);return view }
}

/** Native horizontal dialogs; a separate column-based shell for vertical scripts.
 * Native fields, choice lists and button objects are retained, including validation and accessibility.
 */
internal class EditorDialogBuilder(context: Context): AlertDialog.Builder(context) {
    private var heading: CharSequence?=null
    private var prose: CharSequence?=null
    private var content: View?=null
    override fun setTitle(title: CharSequence?): AlertDialog.Builder {heading=title;return super.setTitle(title)}
    override fun setTitle(titleId: Int): AlertDialog.Builder=setTitle(context.getText(titleId))
    override fun setMessage(message: CharSequence?): AlertDialog.Builder {prose=message;return super.setMessage(message)}
    override fun setMessage(messageId: Int): AlertDialog.Builder=setMessage(context.getText(messageId))
    override fun setView(view: View?): AlertDialog.Builder {content=view;return super.setView(view)}
    override fun create(): AlertDialog {
        val dialog=super.create()
        if(VerticalText.uiVertical()) dialog.window!!.decorView.addOnAttachStateChangeListener(object: View.OnAttachStateChangeListener {
            override fun onViewDetachedFromWindow(view: View)=Unit
            override fun onViewAttachedToWindow(view: View) {
                view.removeOnAttachStateChangeListener(this)
                view.post {if(dialog.isShowing) mount(dialog)}
            }
        })
        return dialog
    }
    private fun mount(dialog: AlertDialog) {
        fun dp(n: Int)=(n*context.resources.displayMetrics.density+.5f).toInt()
        val height=(context.resources.configuration.screenHeightDp-200).coerceIn(120,320)
        val shell=LinearLayout(context).apply {orientation=LinearLayout.VERTICAL;tag="vertical_dialog";setPadding(dp(12),dp(12),dp(12),dp(8))}
        val columns=LinearLayout(context).apply {
            orientation=LinearLayout.HORIZONTAL;isBaselineAligned=false;gravity=Gravity.TOP
            layoutDirection=if(VerticalText.uiDirection()==TextDirection.VERTICAL_RL) View.LAYOUT_DIRECTION_RTL else View.LAYOUT_DIRECTION_LTR
        }
        fun add(view: View) {columns.addView(VerticalUi.detach(view),LinearLayout.LayoutParams(-2,-2).apply {setMargins(dp(8),0,dp(8),0)})}
        heading?.let {add(FlowTextView(context).apply {text=it;textSize=20f;columnHeightDp=height})}
        prose?.let {add(FlowTextView(context).apply {text=it;textSize=16f;columnHeightDp=height})}
        var body=content
        if(body is ScrollView && body.childCount==1) body=VerticalUi.detach(body.getChildAt(0))
        body?.let {
            if(it is LinearLayout && it.tag !in listOf("vertical_save_form","vertical_colour_form")) VerticalUi.panel(it,height)
            add(it)
        }
        dialog.listView?.let {list ->
            VerticalUi.detach(list)
            // List navigation remains scrollable; each item's text reads down its own column.
            val original=list.adapter
            val checked=(0 until list.count).filter {list.isItemChecked(it)}
            list.adapter=object: BaseAdapter() {
                override fun getCount()=original.count
                override fun getItem(position: Int)=original.getItem(position)
                override fun getItemId(position: Int)=original.getItemId(position)
                override fun getView(position: Int,convertView: View?,parent: ViewGroup): View {
                    val row=original.getView(position,convertView,parent)
                    if(row is TextView) VerticalUi.caption(row,height.coerceAtMost(128))
                    row.layoutParams=AbsListView.LayoutParams(dp(200),-2);return row
                }
            }
            checked.forEach {list.setItemChecked(it,true)}
            columns.addView(list,LinearLayout.LayoutParams(dp(212),dp(height)))
        }
        shell.addView(ColumnScrollView(context).apply {tag="vertical_dialog_columns";addView(columns)},LinearLayout.LayoutParams(-1,-2))
        val actions=LinearLayout(context).apply {isBaselineAligned=false;gravity=Gravity.END;tag="vertical_dialog_actions"}
        listOf(AlertDialog.BUTTON_NEUTRAL,AlertDialog.BUTTON_NEGATIVE,AlertDialog.BUTTON_POSITIVE).forEach {which ->
            dialog.getButton(which)?.takeIf {it.visibility==View.VISIBLE}?.let {button ->
                VerticalUi.detach(button);VerticalUi.caption(button,96)
                actions.addView(button,LinearLayout.LayoutParams(-2,-2).apply {setMargins(dp(4),dp(8),dp(4),0)})
            }
        }
        shell.addView(HorizontalScrollView(context).apply {isFillViewport=true;addView(actions)},LinearLayout.LayoutParams(-1,-2))
        dialog.setContentView(LimitedScrollView(context,dp((context.resources.configuration.screenHeightDp*.85).toInt())).apply {addView(shell)})
        dialog.window!!.setLayout(dp((context.resources.configuration.screenWidthDp*.94).toInt()),ViewGroup.LayoutParams.WRAP_CONTENT)
    }
}
