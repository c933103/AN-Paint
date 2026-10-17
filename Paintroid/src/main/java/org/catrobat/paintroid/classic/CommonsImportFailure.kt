/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import java.io.IOException

/** Application-authored Commons failures, resolved only by the alive gallery UI callback.
 * Provider/framework exceptions keep their original detail; never classify them by message text.
 * Separate exception classes retain the former argument-versus-I/O failure contract.
 */
internal sealed interface CommonsImportFailure {
    class NotFilePage: IllegalArgumentException(), CommonsImportFailure
    class AmbiguousFile: IOException(), CommonsImportFailure
    class MetadataUnavailable: IOException(), CommonsImportFailure
    class MetadataOriginalMismatch: IOException(), CommonsImportFailure
    class InvalidAttributionPage: IOException(), CommonsImportFailure
    class FieldTooLarge: IOException(), CommonsImportFailure
    class CacheFailed: IOException(), CommonsImportFailure
    class DownloadOriginalMismatch: IllegalArgumentException(), CommonsImportFailure
    class PngEncodeFailed: IOException(), CommonsImportFailure
}
