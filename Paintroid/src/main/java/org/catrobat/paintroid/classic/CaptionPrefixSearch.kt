/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

/** Choose only prefixes that the caller has actually measured to fit.
 * Short captions retain exhaustive longest-prefix selection, including unusual
 * nonmonotonic shaping. Long captions use logarithmic probes and a fixed local
 * refinement: their result is a fitting tested prefix, not a claim that every
 * longer prefix fails. The complete text remains in the control and tooltip.
 */
internal object CaptionPrefixSearch {
    private const val REFINEMENT = 64

    fun <T : Any> choose(count: Int, candidate: (Int) -> T, fits: (T) -> Boolean): T? {
        require(count >= 0)
        var bestIndex = -1
        var best: T? = null
        val tested = HashMap<Int, Boolean>()
        fun test(index: Int): Boolean = tested.getOrPut(index) {
            val value = candidate(index)
            fits(value).also { accepted ->
                if (accepted && index > bestIndex) { bestIndex = index; best = value }
            }
        }
        // The full original caption has already failed. Every candidate has
        // fewer whole clusters, followed by the caller's visible ellipsis.
        val last = count - 1
        if (last < 0) return null
        if (count <= REFINEMENT) {
            for (index in last downTo 0) if (test(index)) return best
            return null
        }
        if (test(last)) return best
        var low = 0
        var high = last - 1
        while (low <= high) {
            val middle = low + (high - low) / 2
            if (test(middle)) low = middle + 1 else high = middle - 1
        }
        // This also samples the first 64 prefixes if the probes found no fit.
        // Never return an inferred boundary or assume that fitting is monotone.
        val end = bestIndex + 1
        val start = minOf(last.toLong() - 1, bestIndex.toLong() + REFINEMENT).toInt()
        for (index in start downTo end) if (test(index)) return best
        return best
    }
}
