/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.RandomAccessFile;
import java.util.zip.CRC32;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

/** Bounded ICO directory, PNG wrapper and classic icon DIB decoding, without Android dependencies.
 * PNG ICO layout: https://devblogs.microsoft.com/oldnewthing/20101022-00/?p=12473
 * DIB ICO height contains the XOR image and the monochrome AND mask stacked vertically.
 */
public final class IcoContainer {
    private IcoContainer() { }
    public static final int MAX_ENTRIES = 256;
    public static final long MAX_PAYLOAD = 16L * 1024 * 1024;
    private static final byte[] PNG = {(byte)137,80,78,71,13,10,26,10};
    public static final class Entry {
        public final int width, height, bits;
        public final boolean png;
        public final long offset, length;
        private Entry(int width,int height,int bits,boolean png,long offset,long length) {
            this.width=width;this.height=height;this.bits=bits;this.png=png;this.offset=offset;this.length=length;
        }
    }
    private static IOException invalid(String detail) {return new IOException("Invalid or unsupported ICO: "+detail+".");}
    private static long little(RandomAccessFile in,int bytes) throws IOException {
        long n=0;for(int i=0;i<bytes;i++) {int b=in.read();if(b<0)throw invalid("truncated data");n|=(long)b<<(8*i);}return n;
    }
    private static long at(RandomAccessFile in,long offset,int bytes) throws IOException {in.seek(offset);return little(in,bytes);}
    private static void put(OutputStream out,long n,int bytes) throws IOException {for(int i=0;i<bytes;i++)out.write((int)(n>>>(i*8))&255);}
    private static boolean png(RandomAccessFile in,long offset,long length) throws IOException {
        if(length<8)return false;in.seek(offset);for(byte b:PNG)if(in.read()!=(b&255))return false;return true;
    }
    public static boolean isIco(File file) throws IOException {
        try(RandomAccessFile in=new RandomAccessFile(file,"r")) {return in.length()>=4 && little(in,4)==0x00010000L;}
    }
    private static void dimensions(int width,int height) throws IOException {
        if(width<1 || height<1 || width>256 || height>256)throw invalid("icon dimensions must be between 1 and 256 pixels");
    }
    /** Validate the complete zlib stream without retaining the icon's pixels.
     * Android can return a partial/blank bitmap for damaged IDAT data, so checking
     * PNG chunk CRCs alone is insufficient. Adam7 passes each have their own
     * byte-aligned rows and filter bytes; empty passes contain no rows at all.
     */
    private static final class PngPixels {
        final Inflater inflater = new Inflater();
        final byte[] output = new byte[8192];
        final int[] rowBytes;
        int rowCount, rowIndex, rowRemaining;
        PngPixels(int width,int height,int bitsPerPixel,boolean interlaced) {
            rowBytes=new int[height*(interlaced?7:1)];
            int[] x=interlaced?new int[]{0,4,0,2,0,1,0}:new int[]{0};
            int[] y=interlaced?new int[]{0,0,4,0,2,0,1}:new int[]{0};
            int[] dx=interlaced?new int[]{8,8,4,4,2,2,1}:new int[]{1};
            int[] dy=interlaced?new int[]{8,8,8,4,4,2,2}:new int[]{1};
            for(int pass=0;pass<x.length;pass++) {
                int w=width<=x[pass]?0:(width-x[pass]+dx[pass]-1)/dx[pass];
                int h=height<=y[pass]?0:(height-y[pass]+dy[pass]-1)/dy[pass];
                if(w==0 || h==0)continue;
                int length=(w*bitsPerPixel+7)/8;
                for(int row=0;row<h;row++)rowBytes[rowCount++]=length;
            }
        }
        private void pixels(int length) throws IOException {
            int position=0;
            while(position<length) {
                if(rowRemaining==0) {
                    if(rowIndex==rowCount)throw invalid("too much PNG pixel data");
                    if((output[position++]&255)>4)throw invalid("invalid PNG scanline filter");
                    rowRemaining=rowBytes[rowIndex++];
                }
                int count=Math.min(rowRemaining,length-position);
                position+=count;rowRemaining-=count;
            }
        }
        void accept(byte[] bytes,int length) throws IOException {
            if(length==0)return;
            if(inflater.finished())throw invalid("extra compressed PNG pixel data");
            inflater.setInput(bytes,0,length);
            try {
                for(;;) {
                    int count=inflater.inflate(output);
                    pixels(count);
                    if(inflater.finished()) {
                        if(inflater.getRemaining()!=0)throw invalid("extra compressed PNG pixel data");
                        return;
                    }
                    if(inflater.needsDictionary())throw invalid("PNG pixel stream requires a dictionary");
                    if(inflater.needsInput())return;
                    if(count==0)throw invalid("PNG pixel stream cannot make progress");
                }
            } catch(DataFormatException error) {throw invalid("invalid PNG compressed pixels");}
        }
        void finish() throws IOException {
            if(!inflater.finished() || rowIndex!=rowCount || rowRemaining!=0)
                throw invalid("truncated PNG pixel data");
        }
        void close() {inflater.end();}
    }
    /** Checks boundaries, CRCs and all pixel-stream bytes using bounded buffers. */
    private static int pngInfo(RandomAccessFile in,long start,long length,int width,int height) throws IOException {
        if(!png(in,start,length))throw invalid("missing PNG signature");
        long end=start+length;boolean first=true,data=false,dataClosed=false;int depth=0;byte[] buffer=new byte[65536];
        PngPixels pixels=null;
        in.seek(start+8);
        try {
            while(in.getFilePointer()<end) {
                if(end-in.getFilePointer()<12)throw invalid("truncated PNG chunk");
                long size=in.readInt()&0xffffffffL;int type=in.readInt();
                if(size>end-in.getFilePointer()-4)throw invalid("PNG chunk outside its icon entry");
                if(first && (type!=0x49484452 || size!=13))throw invalid("missing PNG IHDR");
                if(type==0x49444154) {
                    if(dataClosed)throw invalid("nonconsecutive PNG IDAT chunks");
                    data=true;
                } else if(data)dataClosed=true;
                CRC32 crc=new CRC32();for(int i=3;i>=0;i--)crc.update(type>>>(i*8)&255);
                long remaining=size;int pos=0;byte[] header=first?new byte[13]:null;
                while(remaining>0) {
                    int n=(int)Math.min(remaining,buffer.length);in.readFully(buffer,0,n);crc.update(buffer,0,n);
                    if(header!=null){System.arraycopy(buffer,0,header,pos,n);pos+=n;}
                    if(type==0x49444154)pixels.accept(buffer,n);
                    remaining-=n;
                }
                if((in.readInt()&0xffffffffL)!=crc.getValue())throw invalid("PNG checksum mismatch");
                if(first) {
                    int w=0,h=0;for(int i=0;i<4;i++){w=w<<8|(header[i]&255);h=h<<8|(header[4+i]&255);}
                    if(w!=width || h!=height)throw invalid("PNG dimensions disagree with the icon directory");
                    int bitDepth=header[8]&255,colourType=header[9]&255;
                    boolean legalDepth=colourType==0?(bitDepth==1 || bitDepth==2 || bitDepth==4 || bitDepth==8 || bitDepth==16):
                        colourType==3?(bitDepth==1 || bitDepth==2 || bitDepth==4 || bitDepth==8):(bitDepth==8 || bitDepth==16);
                    if(!legalDepth || header[10]!=0 || header[11]!=0 || (header[12]&255)>1)throw invalid("unsupported PNG IHDR settings");
                    int channels;switch(header[9]&255) {case 0:case 3:channels=1;break;case 2:channels=3;break;case 4:channels=2;break;case 6:channels=4;break;default:throw invalid("unsupported PNG colour type");}
                    depth=bitDepth*channels;first=false;
                    pixels=new PngPixels(width,height,depth,header[12]!=0);
                } else if(type==0x49484452)throw invalid("duplicate PNG IHDR");
                if(type==0x49454e44) {
                    if(size!=0 || !data || in.getFilePointer()!=end)throw invalid("invalid PNG end chunk");
                    pixels.finish();return depth;
                }
            }
            throw invalid("missing PNG end chunk");
        } finally {if(pixels!=null)pixels.close();}
    }
    private static final class Dib {
        int bits,header;boolean topDown,maskPresent;long pixels,mask,palette,red,green,blue,alpha;int colours;
    }
    private static long validMask(long mask,long allowed,boolean required) throws IOException {
        if(mask==0) {if(required)throw invalid("missing DIB colour mask");return 0;}
        long value=mask>>>Long.numberOfTrailingZeros(mask);
        if((mask&~allowed)!=0 || (value&(value+1))!=0)throw invalid("invalid DIB colour mask");return mask;
    }
    private static Dib dibInfo(RandomAccessFile in,Entry e) throws IOException {
        long end=e.offset+e.length;Dib d=new Dib();d.header=(int)at(in,e.offset,4);
        if(d.header!=12 && d.header!=40 && d.header!=52 && d.header!=56 && d.header!=108 && d.header!=124)throw invalid("unsupported DIB header");
        if(d.header>e.length)throw invalid("truncated DIB header");
        int w,h,planes;long compression=0,colours=0;
        if(d.header==12) {w=(int)little(in,2);h=(int)little(in,2);planes=(int)little(in,2);d.bits=(int)little(in,2);}
        else {w=(int)little(in,4);h=(int)little(in,4);planes=(int)little(in,2);d.bits=(int)little(in,2);compression=little(in,4);colours=at(in,e.offset+32,4);}
        if(w!=e.width || Math.abs((long)h)!=2L*e.height || planes!=1)throw invalid("DIB dimensions disagree with the icon directory");
        d.topDown=h<0;
        if(d.bits!=1 && d.bits!=4 && d.bits!=8 && d.bits!=16 && d.bits!=24 && d.bits!=32)throw invalid("unsupported DIB bit depth");
        if(d.header==12 && d.bits!=1 && d.bits!=4 && d.bits!=8 && d.bits!=24)throw invalid("unsupported OS/2 icon bit depth");
        boolean fields=compression==3 || compression==6;
        if(compression!=0 && !fields || fields && d.bits!=16 && d.bits!=32)throw invalid("unsupported icon DIB compression");
        if(d.header>=108) {
            long space=at(in,e.offset+56,4);
            if(space!=0x73524742L && space!=0x57696e20L)throw new LegacyColourMetadata.UnsupportedColour();
        }
        int extra=fields && d.header==40?(compression==6?16:12):0;
        if(compression==6 && d.header==52)throw invalid("missing DIB alpha mask");
        if(d.bits<=8) {if(colours==0)colours=1L<<d.bits;if(colours>(1L<<d.bits))throw invalid("DIB palette is too large");}
        if(colours>256)throw invalid("DIB optimization palette exceeds 256 entries");
        d.colours=(int)colours;d.palette=e.offset+d.header+extra;
        d.pixels=d.palette+colours*(d.header==12?3:4);
        long stride=((e.width*(long)d.bits+31)/32)*4;
        d.mask=d.pixels+stride*e.height;long maskBytes=((e.width+31)/32)*4L*e.height;
        if(d.mask>end)throw invalid("truncated DIB pixels");
        d.maskPresent=maskBytes<=end-d.mask;
        if(!d.maskPresent && (d.bits!=32 || end!=d.mask))throw invalid("truncated icon AND mask");
        if(fields) {
            long allowed=(1L<<d.bits)-1;
            d.red=validMask(at(in,e.offset+40,4),allowed,true);d.green=validMask(little(in,4),allowed,true);d.blue=validMask(little(in,4),allowed,true);
            d.alpha=d.header>=56 || compression==6?validMask(little(in,4),allowed,compression==6):0;
            if((d.red&d.green)!=0 || (d.red&d.blue)!=0 || (d.green&d.blue)!=0 || (d.alpha&(d.red|d.green|d.blue))!=0)throw invalid("overlapping icon colour masks");
        } else if(d.bits==16) {d.red=0x7c00;d.green=0x3e0;d.blue=31;}
        else {d.red=0xff0000;d.green=0xff00;d.blue=255;d.alpha=d.bits==32?0xff000000L:0;}
        return d;
    }
    /** Largest structurally valid supported image; prefer greater depth and PNG on equal dimensions. */
    public static Entry best(File file) throws IOException {
        try(RandomAccessFile in=new RandomAccessFile(file,"r")) {
            if(in.length()<6 || little(in,4)!=0x00010000L)throw invalid("missing icon directory");
            int count=(int)little(in,2);long table=6L+count*16L;
            if(count==0 || count>MAX_ENTRIES || table>in.length())throw invalid("invalid directory count");
            Entry best=null;IOException failure=null;
            for(int i=0;i<count;i++) {
                in.seek(6L+i*16L);int w=in.read(),h=in.read();in.read();int reserved=in.read();
                int planes=(int)little(in,2);little(in,2);long length=little(in,4),offset=little(in,4);
                try {
                    if(w==0)w=256;if(h==0)h=256;dimensions(w,h);
                    if(reserved!=0 || planes>1 || length<12 || length>MAX_PAYLOAD || offset<table || offset>in.length() || length>in.length()-offset)
                        throw invalid("entry offset, length or plane count");
                    boolean png=png(in,offset,length);Entry entry=new Entry(w,h,0,png,offset,length);
                    int bits=png?pngInfo(in,offset,length,w,h):dibInfo(in,entry).bits;
                    entry=new Entry(w,h,bits,png,offset,length);
                    if(best==null || w*h>best.width*best.height || w*h==best.width*best.height && (bits>best.bits || bits==best.bits && png && !best.png)) {
                        // Palette indices and legacy alpha/mask consistency can make an otherwise
                        // bounded DIB unusable. Check before selecting it over a valid smaller icon.
                        if(!png)decodeDib(file,entry);
                        best=entry;
                    }
                } catch(IOException invalid) {failure=invalid;}
            }
            if(best==null) {if(failure!=null)throw failure;throw invalid("no supported image entry");}return best;
        }
    }
    private static void copy(RandomAccessFile in,long start,long length,OutputStream out) throws IOException {
        byte[] buffer=new byte[65536];in.seek(start);while(length>0){int n=(int)Math.min(length,buffer.length);in.readFully(buffer,0,n);out.write(buffer,0,n);length-=n;}
    }
    public static void extractPng(File file,Entry entry,OutputStream output) throws IOException {
        if(!entry.png)throw invalid("entry is not PNG");
        try(RandomAccessFile in=new RandomAccessFile(file,"r")){pngInfo(in,entry.offset,entry.length,entry.width,entry.height);copy(in,entry.offset,entry.length,output);}
    }
    private static int component(long value,long mask) {
        if(mask==0)return 0;int shift=Long.numberOfTrailingZeros(mask);long maximum=mask>>>shift;
        return (int)((((value&mask)>>>shift)*255+maximum/2)/maximum);
    }
    /** Straight ARGB. A 32-bit legacy icon with every alpha byte zero uses its AND mask instead. */
    public static int[] decodeDib(File file,Entry entry) throws IOException {
        if(entry.png)throw invalid("entry is PNG");
        try(RandomAccessFile in=new RandomAccessFile(file,"r")) {
            Dib d=dibInfo(in,entry);int[] palette=new int[d.colours];in.seek(d.palette);
            for(int i=0;i<palette.length;i++){int b=in.read(),g=in.read(),r=in.read();if(d.header!=12)in.read();palette[i]=0xff000000|r<<16|g<<8|b;}
            int[] output=new int[entry.width*entry.height];int stride=((entry.width*d.bits+31)/32)*4;
            byte[] row=new byte[stride];boolean nonzeroAlpha=false;
            for(int y=0;y<entry.height;y++) {
                in.seek(d.pixels+(d.topDown?y:entry.height-1-y)*(long)stride);in.readFully(row);
                for(int x=0;x<entry.width;x++) {
                    int colour;
                    if(d.bits<=8) {
                        int index=d.bits==8?row[x]&255:d.bits==4?(row[x/2]>>>(x%2==0?4:0))&15:(row[x/8]>>>(7-x%8))&1;
                        if(index>=palette.length)throw invalid("DIB palette index outside the table");colour=palette[index];
                    } else {
                        long value=0;int bytes=d.bits/8;for(int i=0;i<bytes;i++)value|=(long)(row[x*bytes+i]&255)<<(i*8);
                        int alpha=d.alpha==0?255:component(value,d.alpha);nonzeroAlpha|=d.alpha!=0 && alpha!=0;
                        colour=alpha<<24|component(value,d.red)<<16|component(value,d.green)<<8|component(value,d.blue);
                    }
                    output[y*entry.width+x]=colour;
                }
            }
            boolean alpha=d.alpha!=0 && (d.bits!=32 || nonzeroAlpha);
            boolean modernAlpha=d.bits==32 && alpha;
            if(!modernAlpha && !d.maskPresent)throw invalid("legacy icon has no AND mask");
            // Modern alpha icons use alpha compositing; their compatibility AND mask is ignored.
            if(!modernAlpha) {
                int maskStride=((entry.width+31)/32)*4;byte[] mask=new byte[maskStride];
                for(int y=0;y<entry.height;y++) {
                    in.seek(d.mask+(d.topDown?y:entry.height-1-y)*(long)maskStride);in.readFully(mask);
                    for(int x=0;x<entry.width;x++) {
                        int at=y*entry.width+x;output[at]=(mask[x/8]&(128>>>(x%8)))!=0?0:alpha?output[at]:output[at]|0xff000000;
                    }
                }
            }
            return output;
        }
    }
    /** Single PNG-compressed image in a Windows ICO container. */
    public static void writePng(File pngFile,int width,int height,OutputStream output) throws IOException {
        dimensions(width,height);
        try(RandomAccessFile in=new RandomAccessFile(pngFile,"r")) {
            long length=in.length();if(length>MAX_PAYLOAD)throw invalid("PNG payload exceeds 16 MiB");pngInfo(in,0,length,width,height);
            put(output,0,2);put(output,1,2);put(output,1,2);output.write(width==256?0:width);output.write(height==256?0:height);
            output.write(0);output.write(0);put(output,1,2);put(output,32,2);put(output,length,4);put(output,22,4);copy(in,0,length,output);
        }
    }
}
