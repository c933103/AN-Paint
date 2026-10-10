/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import java.util.concurrent.Executor

/** A startup result has one owner, even if destruction overtakes its main-thread delivery.
 * Loading and disposal never need a main-thread callback to finish. Cancellation does not
 * interrupt a predecessor's durable write or turn a pending recovery into an empty editor.
 */
internal class EditorStartup<T>(
    private val worker: Executor,
    private val main: Executor,
    private val load: () -> T,
    private val release: (T) -> Unit,
    private val receive: (Result<T>) -> Unit
) {
    private val lock=Any()
    private var cancelled=false
    private var pending: Result<T>?=null

    fun start() {
        worker.execute {
            if(synchronized(lock) {cancelled}) return@execute
            val result=try { Result.success(load()) }
                catch(error: Exception) { Result.failure(error) }
                catch(error: OutOfMemoryError) { Result.failure(error) }
            val discard=synchronized(lock) {
                if(cancelled) true else {check(pending==null);pending=result;false}
            }
            if(discard) result.getOrNull()?.let(release)
            else main.execute {
                val delivery=synchronized(lock) {pending.also {pending=null}}
                delivery?.let(receive)
            }
        }
    }

    /** Called on the same main thread that receives results. */
    fun cancel() {
        val discarded=synchronized(lock) {cancelled=true;pending.also {pending=null}}
        discarded?.getOrNull()?.let {value ->worker.execute {release(value)}}
    }
}
