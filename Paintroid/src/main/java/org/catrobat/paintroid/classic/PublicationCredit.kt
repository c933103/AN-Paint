/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import org.catrobat.paintroid.R

/** Publication attribution contains creator/source/licence notices, not download
 * plumbing or instructions addressed to the app user. A download URI is not an
 * input to this renderer. Source-mandated attribution links remain in notices.
 */
internal data class PublicationCredit(
    val title: String,
    val publisher: String,
    val sourcePage: String,
    val creators: List<String> = emptyList(),
    val licences: List<String> = emptyList(),
    val notices: List<String> = emptyList(),
    val changes: String? = null
) {
    fun text(): String = (listOf(ui(R.string.gallery_credit_title,title),publisher,
        ui(R.string.gallery_credit_source,sourcePage)) + creators + licences + notices + listOfNotNull(changes))
        .filter {it.isNotBlank()}.distinct().joinToString("\n")
}
