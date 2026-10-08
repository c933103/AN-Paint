/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

/** Presentation-only pages. Stored/exported attribution is never shortened. */
internal class ImageCreditTextPages(private val value: String) {
    companion object {const val PAGE_CHARS=4096}
    private val offsets=mutableListOf(0).apply {
        while(last()<value.length) {
            var end=last()+minOf(PAGE_CHARS,value.length-last())
            if(end<value.length && Character.isHighSurrogate(value[end-1]) && Character.isLowSurrogate(value[end]))end--
            add(end)
        }
        if(size==1)add(0)
    }
    val count get()=offsets.size-1
    fun text(page: Int): String {
        require(page in 0 until count)
        return value.substring(offsets[page],offsets[page+1])
    }
}
