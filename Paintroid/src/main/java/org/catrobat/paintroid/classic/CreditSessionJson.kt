/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic

import android.util.AtomicFile
import org.json.JSONArray
import org.json.JSONObject
import java.io.*
import java.nio.charset.CodingErrorAction

/** The session is ordinary version-1 JSON, but its unfinished string has no format-size limit.
 * Never assemble its encoded document in memory. Resource refusal is an I/O failure, not a
 * successful/truncated Save, and never authorizes deleting an earlier session. */
internal object CreditSessionJson {
    private const val BUFFER_CHARS=4096
    private const val NODE_BYTES=256L
    private const val STRING_CHAR_BYTES=12L // builder growth, immutable copy and the restored Editable
    internal var availableHeap: ()->Long = {
        val runtime=Runtime.getRuntime()
        runtime.maxMemory()-(runtime.totalMemory()-runtime.freeMemory())
    }
    internal var usableSpace: (File)->Long = {it.usableSpace}
    internal var blockSize: (File)->Long = {android.os.StatFs(it.absolutePath).blockSizeLong}

    private fun unavailable()=IOException("Insufficient resources to save or restore image credits")
    fun <T> withResources(action: ()->T): T = try {action()} catch(error: OutOfMemoryError) {
        throw IOException("Insufficient memory to save or restore image credits",error)
    }
    private class MemoryBudget {
        private var remaining=availableHeap().coerceAtLeast(0)/2
        fun take(bytes: Long) {if(bytes<0 || bytes>remaining)throw unavailable();remaining-=bytes}
    }
    fun checkText(text: CharSequence) {MemoryBudget().take(text.length.toLong()*STRING_CHAR_BYTES)}
    fun snapshot(source: String,text: CharSequence): GalleryCredits.EditorDraft = withResources {
        // Editable.toString() itself makes a full copy; account for it before touching the field.
        MemoryBudget().take(text.length.toLong()*STRING_CHAR_BYTES+source.length.toLong()*2)
        GalleryCredits.EditorDraft(source,text.toString())
    }
    private class DiskBudget(private val directory: File,private val bytes: Long) {
        private val block=blockSize(directory).takeIf {it>0} ?: throw unavailable()
        // Existing base/.bak bytes are already excluded from usableSpace. The replacement
        // must coexist with them. Two blocks are a best-effort directory-entry/rollback
        // margin, not an exact filesystem guarantee or Android's low-storage threshold.
        private val reserve=if(block<=Long.MAX_VALUE/2)block*2 else throw unavailable()
        private var written=0L
        private fun rounded(size: Long): Long {
            if(size<0 || size>Long.MAX_VALUE-(block-1))throw unavailable()
            val blocks=(size+block-1)/block
            if(blocks>Long.MAX_VALUE/block)throw unavailable()
            return blocks*block
        }
        private fun requireSpace(needed: Long) {
            val free=usableSpace(directory).coerceAtLeast(0)
            if(reserve>free || needed>free-reserve)throw unavailable()
        }
        init {requireSpace(rounded(bytes))}
        fun check(count: Int) {
            if(count<0 || written>bytes-count)throw unavailable()
            // A short final encoder chunk may fit an already allocated block. Charge only
            // new block allocation, while retaining the complete rollback margin.
            requireSpace(rounded(written+count)-rounded(written))
        }
        fun wrote(count: Int) {written+=count}
    }
    private class Counter(private val limit: Long=Long.MAX_VALUE): Writer() {
        var bytes=0L;private set
        private var highSurrogate=false
        private fun add(count: Int) {if(bytes>limit-count)throw TooLong();bytes+=count}
        override fun write(chars: CharArray,offset: Int,count: Int) {
            // Adoption copies may contain literal supplementary characters from old files.
            // Match OutputStreamWriter's UTF-8 encoder, including pairs split across calls.
            for(i in offset until offset+count) {
                val c=chars[i]
                if(highSurrogate) {
                    highSurrogate=false
                    if(Character.isLowSurrogate(c)) {add(4);continue}
                    add(1)
                }
                when {
                    Character.isHighSurrogate(c)->highSurrogate=true
                    Character.isLowSurrogate(c)->add(1)
                    c.code<0x80->add(1)
                    c.code<0x800->add(2)
                    else->add(3)
                }
            }
        }
        override fun flush() {if(highSurrogate) {highSurrogate=false;add(1)}}
        override fun close()=flush()
    }
    private class TooLong: IOException()
    fun fitsInline(value: Any?,limit: Int): Boolean = try {
        emit(value,Counter(limit.toLong()));true
    } catch(_: TooLong) {false}
    fun fitsInline(text: CharSequence,limit: Int): Boolean {
        var bytes=0L;var index=0
        while(index<text.length) {
            val c=text[index++]
            bytes+=when {
                c.code<0x80->1
                c.code<0x800->2
                Character.isHighSurrogate(c) && index<text.length && Character.isLowSurrogate(text[index])->{index++;4}
                Character.isSurrogate(c)->1 // Matches Java's UTF-8 replacement for an unmatched code unit.
                else->3
            }
            if(bytes>limit)return false
        }
        return true
    }
    private fun quoted(text: String,out: Writer) {
        out.write('"'.code)
        var start=0
        for(index in text.indices) {
            val c=text[index]
            val escaped=when(c) {
                '"'->"\\\"";'\\'->"\\\\";'/'->"\\/";'\b'->"\\b";'\u000c'->"\\f";'\n'->"\\n";'\r'->"\\r";'\t'->"\\t"
                else->if(c.code<32 || Character.isSurrogate(c))"\\u"+c.code.toString(16).padStart(4,'0') else null
            }
            if(escaped!=null) {
                chunks(text,start,index,out);out.write(escaped);start=index+1
            } else if(index-start+1==BUFFER_CHARS) {
                chunks(text,start,index+1,out);start=index+1
            }
        }
        chunks(text,start,text.length,out);out.write('"'.code)
    }
    private fun chunks(text: String,start: Int,end: Int,out: Writer) {
        var offset=start
        while(offset<end) {val count=minOf(BUFFER_CHARS,end-offset);out.write(text,offset,count);offset+=count}
    }
    private fun emit(value: Any?,out: Writer) {
        when(value) {
            null,JSONObject.NULL->out.write("null")
            is String->quoted(value,out)
            is JSONObject->{
                out.write('{'.code);val keys=value.keys();var first=true
                while(keys.hasNext()) {
                    val key=keys.next();if(!first)out.write(','.code);first=false
                    quoted(key,out);out.write(':'.code);emit(value.get(key),out)
                }
                out.write('}'.code)
            }
            is JSONArray->{
                out.write('['.code)
                for(i in 0 until value.length()) {if(i>0)out.write(','.code);emit(value.get(i),out)}
                out.write(']'.code)
            }
            is Boolean,is Number->out.write(value.toString())
            else->throw IOException("Invalid image credit session value")
        }
    }
    fun write(atomic: AtomicFile,directory: File,value: JSONObject)=withResources {
        val count=Counter();emit(value,count)
        replace(atomic,directory,count.bytes) {emit(value,it)}
    }
    private fun replace(atomic: AtomicFile,directory: File,bytes: Long,write: (Writer)->Unit) {
        val budget=DiskBudget(directory,bytes)
        val stream=atomic.startWrite()
        try {
            val checked=object: OutputStream() {
                override fun write(value: Int) {budget.check(1);stream.write(value);budget.wrote(1)}
                override fun write(bytes: ByteArray,offset: Int,count: Int) {budget.check(count);stream.write(bytes,offset,count);budget.wrote(count)}
            }
            val writer=OutputStreamWriter(checked,Charsets.UTF_8).buffered(BUFFER_CHARS)
            write(writer);writer.flush();stream.fd.sync();atomic.finishWrite(stream)
        } catch(error: Throwable) {atomic.failWrite(stream);throw error}
    }
    private fun reader(input: InputStream)=InputStreamReader(input,Charsets.UTF_8.newDecoder()
        .onMalformedInput(CodingErrorAction.REPORT).onUnmappableCharacter(CodingErrorAction.REPORT)).buffered(BUFFER_CHARS)
    fun read(atomic: AtomicFile,names: Set<String>?=null): JSONObject = withResources {
        atomic.openRead().use {input->Parser(reader(input)).root(names)}
    }
    /** The worker needs ownership/revision and presence, never the unfinished field's contents. */
    fun receipt(atomic: AtomicFile): JSONObject=read(atomic,setOf("version","revision","adopted_revision","accepted","accepted_snapshot"))
    fun adopt(atomic: AtomicFile,directory: File,revision: Long)=withResources {
        // Keep the old descriptor open before AtomicFile moves it to .bak. The transaction copies
        // the original JSON tokens (including the exact raw field) with fixed buffers.
        val count=Counter()
        atomic.openRead().use {input->Parser(reader(input)).copyWithAdoption(count,revision)}
        atomic.openRead().use {input->
            replace(atomic,directory,count.bytes) {out->Parser(reader(input)).copyWithAdoption(out,revision)}
        }
    }

    /** Streaming JSON parser. Only requested values consume the heap budget; skipped raw strings
     * and adoption copies use constant space, even for sessions saved by older versions. */
    private class Parser(private val input: Reader) {
        private val memory=MemoryBudget()
        private var next=input.read()
        private var copy: Writer?=null
        private fun invalid(): Nothing=throw IOException("Invalid image credit session")
        private fun take(): Int {val value=next;if(value<0)invalid();copy?.write(value);next=input.read();return value}
        private fun whitespace() {while(next==32 || next==9 || next==10 || next==13)take()}
        private fun expect(value: Char) {if(next!=value.code)invalid();take()}
        private fun string(keep: Boolean): String? {
            expect('"');val result=if(keep)StringBuilder() else null
            while(next!='"'.code) {
                var c=take();if(c<32)invalid()
                if(c=='\\'.code) {
                    c=when(val escaped=take()) {
                        '"'.code,'\\'.code,'/'.code->escaped
                        'b'.code->8;'f'.code->12;'n'.code->10;'r'.code->13;'t'.code->9
                        'u'.code->{var code=0;repeat(4) {val digit=Character.digit(take().toChar(),16);if(digit<0)invalid();code=code*16+digit};code}
                        else->invalid()
                    }
                }
                if(keep) {memory.take(STRING_CHAR_BYTES);result!!.append(c.toChar())}
            }
            take();return result?.toString()
        }
        private fun value(keep: Boolean,depth: Int): Any? {
            if(depth>32)invalid() // The known document/history/session schema is much shallower.
            whitespace();if(keep)memory.take(NODE_BYTES)
            return when(next) {
                '"'.code->string(keep)
                '{'.code->{
                    take();val result=if(keep)JSONObject() else null;whitespace()
                    if(next!='}'.code)while(true) {
                        if(keep)memory.take(NODE_BYTES)
                        val key=string(keep);whitespace();expect(':');val child=value(keep,depth+1)
                        if(keep)result!!.put(key!!,child ?: JSONObject.NULL)
                        whitespace();if(next!=','.code)break;take();whitespace()
                    }
                    expect('}');result
                }
                '['.code->{
                    take();val result=if(keep)JSONArray() else null;whitespace()
                    if(next!=']'.code)while(true) {
                        val child=value(keep,depth+1);if(keep)result!!.put(child ?: JSONObject.NULL)
                        whitespace();if(next!=','.code)break;take();whitespace()
                    }
                    expect(']');result
                }
                't'.code->{for(c in "true")expect(c);true}
                'f'.code->{for(c in "false")expect(c);false}
                'n'.code->{for(c in "null")expect(c);JSONObject.NULL}
                else->{
                    val text=StringBuilder()
                    while(next=='-'.code || next=='+'.code || next=='.'.code || next=='e'.code || next=='E'.code || next in '0'.code..'9'.code) {
                        if(text.length>=64)invalid();text.append(take().toChar())
                    }
                    if(!NUMBER.matches(text))invalid()
                    if(keep)JSONObject("{\"n\":$text}").get("n") else null
                }
            }
        }
        fun root(names: Set<String>?): JSONObject {
            whitespace();expect('{');whitespace();val result=JSONObject();var hasDraft=false
            if(next!='}'.code)while(true) {
                memory.take(NODE_BYTES);val key=string(true)!!;whitespace();expect(':');whitespace()
                if(key=="draft")hasDraft=next!='n'.code
                val keep=names==null || key in names
                val child=value(keep,1);if(keep)result.put(key,child ?: JSONObject.NULL)
                whitespace();if(next!=','.code)break;take();whitespace()
            }
            expect('}');whitespace();if(next>=0)invalid()
            if(names!=null)result.put("has_draft",hasDraft)
            return result
        }
        fun copyWithAdoption(out: Writer,revision: Long) {
            whitespace();expect('{');whitespace();out.write('{'.code);var first=true
            if(next!='}'.code)while(true) {
                memory.take(NODE_BYTES);val key=string(true)!!;whitespace();expect(':');whitespace()
                if(key=="adopted_revision")value(false,1) else {
                    if(!first)out.write(','.code);first=false;quoted(key,out);out.write(':'.code)
                    copy=out;try {value(false,1)} finally {copy=null}
                }
                whitespace();if(next!=','.code)break;take();whitespace()
            }
            expect('}');whitespace();if(next>=0)invalid()
            if(!first)out.write(','.code)
            out.write("\"adopted_revision\":$revision}")
        }
        companion object {private val NUMBER=Regex("-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?")}
    }
}
