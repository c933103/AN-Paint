/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic;

import java.io.*;
import java.util.Locale;

/** Streaming text-image primitives; independent of Android and the platform Base64 decoder. */
public final class TextImageData {
    private TextImageData() { }
    private static final byte[] ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".getBytes(java.nio.charset.StandardCharsets.US_ASCII);
    public static final int MAX_ASCII_CHARACTERS = 4 * 1024 * 1024;
    private static final String RAMP = "@%#*+=-:. ";
    private static boolean whitespace(int c) { return c == 32 || c == 9 || c == 10 || c == 13; }
    private static int value(int c) {
        if (c >= 'A' && c <= 'Z') return c - 'A';
        if (c >= 'a' && c <= 'z') return c - 'a' + 26;
        if (c >= '0' && c <= '9') return c - '0' + 52;
        if (c == '+') return 62;
        if (c == '/') return 63;
        return -1;
    }
    private static IOException malformed() { return new IOException("Invalid Base64 image text."); }
    private static final class Body {
        final BufferedInputStream input; final boolean dataUri;
        Body(BufferedInputStream input, boolean dataUri) { this.input = input; this.dataUri = dataUri; }
    }
    private static Body body(InputStream source) throws IOException {
        BufferedInputStream input = new BufferedInputStream(source, 65536);
        input.mark(3);
        if (input.read() == 0xef) {
            if (input.read() != 0xbb || input.read() != 0xbf) throw malformed();
        } else input.reset();
        for (;;) {
            input.mark(1); int c = input.read();
            if (!whitespace(c)) { input.reset(); break; }
        }
        input.mark(512);
        byte[] start = new byte[5]; int count = 0;
        while (count < start.length) { int n = input.read(start, count, start.length - count); if (n < 0) break; count += n; }
        boolean uri = count == 5 && new String(start, java.nio.charset.StandardCharsets.US_ASCII).equalsIgnoreCase("data:");
        if (!uri) { input.reset(); return new Body(input, false); }
        StringBuilder header = new StringBuilder();
        for (int i = 0; i < 256; i++) {
            int c = input.read();
            if (c == ',') {
                String type = header.toString().toLowerCase(Locale.ROOT);
                if (!type.matches("image/[a-z0-9.+-]+(?:;charset=[a-z0-9._-]+)?;base64")) throw malformed();
                return new Body(input, true);
            }
            if (c < 0 || c > 127) throw malformed();
            if (!whitespace(c)) header.append((char)c);
        }
        throw malformed();
    }
    /** Decodes standard Base64, allowing ASCII whitespace and canonical unpadded final groups. */
    public static long decode(InputStream source, OutputStream destination, long maxBytes) throws IOException {
        if (maxBytes < 0) throw new IOException("Invalid decoded-image size limit.");
        InputStream input = body(source).input;
        int[] group = new int[4]; int count = 0; long written = 0; boolean finished = false;
        for (;;) {
            int c = input.read(); if (c < 0) break; if (whitespace(c)) continue;
            if (finished) throw malformed();
            int v = c == '=' ? -2 : value(c); if (v == -1) throw malformed();
            group[count++] = v;
            if (count == 4) {
                if (group[0] < 0 || group[1] < 0 || (group[2] == -2 && group[3] != -2)) throw malformed();
                int n = group[2] == -2 ? 1 : group[3] == -2 ? 2 : 3;
                if ((n == 1 && (group[1] & 15) != 0) || (n == 2 && (group[2] & 3) != 0)) throw malformed();
                if (n > maxBytes - written) throw new IOException("Decoded image exceeds the import file-size limit.");
                destination.write(group[0] << 2 | group[1] >>> 4);
                if (n >= 2) destination.write(group[1] << 4 | group[2] >>> 2);
                if (n == 3) destination.write(group[2] << 6 | group[3]);
                written += n; count = 0; finished = n != 3;
            }
        }
        if (count != 0) {
            if (count == 1 || group[0] < 0 || group[1] < 0 || (count == 3 && group[2] < 0)) throw malformed();
            if ((count == 2 && (group[1] & 15) != 0) || (count == 3 && (group[2] & 3) != 0)) throw malformed();
            int n = count - 1;
            if (n > maxBytes - written) throw new IOException("Decoded image exceeds the import file-size limit.");
            destination.write(group[0] << 2 | group[1] >>> 4);
            if (n == 2) destination.write(group[1] << 4 | group[2] >>> 2);
            written += n;
        }
        if (written == 0) throw malformed();
        return written;
    }
    private static boolean starts(byte[] bytes, int... signature) {
        if (bytes.length < signature.length) return false;
        for (int i = 0; i < signature.length; i++) if ((bytes[i] & 255) != signature[i]) return false;
        return true;
    }
    public static boolean imageSignature(byte[] b) {
        if (starts(b,137,80,78,71,13,10,26,10) || starts(b,255,216,255) || starts(b,71,73,70,56,55,97) || starts(b,71,73,70,56,57,97) || starts(b,66,77)) return true;
        if (starts(b,73,73,42,0) || starts(b,77,77,0,42) || starts(b,73,73,43,0) || starts(b,77,77,0,43)) return true;
        if (starts(b,255,10) || starts(b,0,0,0,12,74,88,76,32,13,10,135,10)) return true;
        if (b.length >= 12 && starts(b,82,73,70,70) && b[8]=='W' && b[9]=='E' && b[10]=='B' && b[11]=='P') return true;
        if (b.length >= 12 && b[4]=='f' && b[5]=='t' && b[6]=='y' && b[7]=='p') {
            for(int offset=8;offset+4<=b.length;offset+=4) {
                if(offset==12)continue; // Minor version, not a compatible brand.
                String brand=new String(b,offset,4,java.nio.charset.StandardCharsets.US_ASCII);
                if(brand.matches("heic|heix|hevc|hevx|heim|heis|hevm|hevs|mif1|msf1|avif|avis"))return true;
            }
        }
        if (b.length >= 6 && (starts(b,0,0,1,0) || starts(b,0,0,2,0)) && (b[4]!=0 || b[5]!=0)) return true;
        // Packed DIB; its complete dimensions, planes, palettes and scanlines are validated on import.
        if (b.length >= 12 && b[1]==0 && b[2]==0 && b[3]==0) {
            int n=b[0]&255; if(n==12 || n==40 || n==52 || n==56 || n==108 || n==124) return true;
        }
        return false;
    }
    /** Bounded detection: ordinary prose and binary files are never treated as raw Base64. */
    public static boolean inspect(File file) throws IOException {
        byte[] prefix = new byte[4096]; int n = 0;
        try (InputStream input = new FileInputStream(file)) {
            while (n < prefix.length) { int k=input.read(prefix,n,prefix.length-n); if(k<0)break; n+=k; }
        }
        try {
            Body parsed=body(new ByteArrayInputStream(prefix,0,n));
            if(parsed.dataUri)return true;
            ByteArrayOutputStream encoded=new ByteArrayOutputStream();
            int c;
            while(encoded.size()<128 && (c=parsed.input.read())>=0) {
                if(whitespace(c))continue;
                if(c!='=' && value(c)<0)return false;
                encoded.write(c);
            }
            byte[] sample=encoded.toByteArray();
            int length=sample.length;
            if(length==128)length-=length%4;
            ByteArrayOutputStream decoded=new ByteArrayOutputStream();
            decode(new ByteArrayInputStream(sample,0,length),decoded,128);
            return imageSignature(decoded.toByteArray());
        } catch(IOException invalid) {return false;}
    }
    /** Streaming standard Base64 encoder. finish() writes padding without closing the destination. */
    public static final class Base64Output extends OutputStream {
        private final OutputStream output; private int count, pending; private boolean finished;
        public Base64Output(OutputStream output) {this.output=output;}
        @Override public void write(int b) throws IOException {
            if(finished)throw new IOException("Base64 stream is already finished.");
            pending=(pending<<8)|(b&255);count++;
            if(count==3) {
                output.write(ALPHABET[(pending>>>18)&63]);output.write(ALPHABET[(pending>>>12)&63]);
                output.write(ALPHABET[(pending>>>6)&63]);output.write(ALPHABET[pending&63]);count=0;pending=0;
            }
        }
        @Override public void write(byte[] b,int offset,int length) throws IOException {
            if(offset<0 || length<0 || offset>b.length-length)throw new IndexOutOfBoundsException();
            for(int i=offset;i<offset+length;i++)write(b[i]);
        }
        public void finish() throws IOException {
            if(finished)return;
            if(count==1) {output.write(ALPHABET[(pending>>>2)&63]);output.write(ALPHABET[(pending<<4)&63]);output.write('=');output.write('=');}
            else if(count==2) {output.write(ALPHABET[(pending>>>10)&63]);output.write(ALPHABET[(pending>>>4)&63]);output.write(ALPHABET[(pending<<2)&63]);output.write('=');}
            finished=true;output.flush();
        }
        @Override public void close() throws IOException {finish();}
    }
    public static int asciiRows(int width,int height,int columns) throws IOException {
        if(width<=0 || height<=0 || columns<40 || columns>240)throw new IOException("ASCII width must be 40 to 240 characters.");
        long rows=Math.max(1,Math.round(height*(double)columns/(width*2.0)));
        if(rows>MAX_ASCII_CHARACTERS/(columns+1))throw new IOException("ASCII output exceeds the text-size limit; choose fewer columns.");
        return (int)rows;
    }
    public interface Rows {void read(int y,int[] row) throws IOException;}
    /** Bright pixels use sparse marks on a light background; inversion reverses the ramp. */
    public static void ascii(int columns,int rows,Rows pixels,OutputStream destination,boolean invert) throws IOException {
        if(columns<40 || columns>240 || rows<1 || (long)(columns+1)*rows>MAX_ASCII_CHARACTERS)throw new IOException("ASCII output exceeds the text-size limit.");
        int[] row=new int[columns];byte[] text=new byte[columns+1];text[columns]='\n';
        for(int y=0;y<rows;y++) {
            pixels.read(y,row);
            for(int x=0;x<columns;x++) {
                int c=row[x],alpha=c>>>24;
                double r=((c>>>16)&255)*alpha/255.0+255-alpha;
                double g=((c>>>8)&255)*alpha/255.0+255-alpha;
                double b=(c&255)*alpha/255.0+255-alpha;
                // Rec.709 luma weights on the editor's sRGB samples match displayed brightness.
                double level=(.2126*r+.7152*g+.0722*b)/255.0;
                int index=(int)Math.round(level*(RAMP.length()-1));
                text[x]=(byte)RAMP.charAt(invert?RAMP.length()-1-index:index);
            }
            destination.write(text);
        }
    }
}
