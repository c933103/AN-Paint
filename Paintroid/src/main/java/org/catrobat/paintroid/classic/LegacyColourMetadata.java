/* AN Paint, 2026. GNU AGPL-3.0-or-later. */
package org.catrobat.paintroid.classic;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;

/** Metadata-only guard: never accept a known colour profile as untagged RGB. */
public final class LegacyColourMetadata {
    private LegacyColourMetadata() { }
    public static final class UnsupportedColour extends IOException {
        UnsupportedColour() { super("This BMP/GIF colour profile is not supported."); }
    }
    private static int octet(RandomAccessFile input) throws IOException {
        int n=input.read(); if(n<0) throw new IOException("Truncated BMP/GIF metadata."); return n;
    }
    private static long little(RandomAccessFile input) throws IOException {
        long result=0; for(int i=0;i<4;i++) result|=(long)octet(input)<<(i*8); return result;
    }
    private static void skip(RandomAccessFile input,long count) throws IOException {
        if(count<0 || count>input.length()-input.getFilePointer()) throw new IOException("Truncated BMP/GIF metadata.");
        input.seek(input.getFilePointer()+count);
    }
    private static void subBlocks(RandomAccessFile input) throws IOException {
        // Each iteration advances within the finite file; no image or profile data is allocated.
        while(true) {int size=octet(input);if(size==0)return;skip(input,size);}
    }
    public static void check(File file) throws IOException {
        try(RandomAccessFile input=new RandomAccessFile(file,"r")) {
            if(input.length()<3)return;
            int first=octet(input),second=octet(input),third=octet(input);
            if(first=='B' && second=='M') {
                if(input.length()<18) throw new IOException("Truncated BMP header.");
                input.seek(14);long headerSize=little(input);
                if(headerSize>input.length()-14) throw new IOException("Truncated BMP header.");
                if(headerSize>=108) {
                    if(headerSize!=108 && headerSize!=124) throw new UnsupportedColour();
                    input.seek(14+56);long space=little(input);
                    // BITMAPV4/V5: only explicit sRGB / Windows default sRGB needs no conversion.
                    if(space!=0x73524742L && space!=0x57696e20L) throw new UnsupportedColour();
                }
            } else if(first=='G' && second=='I' && third=='F') {
                byte[] version=new byte[3];input.readFully(version);
                String value=new String(version,StandardCharsets.US_ASCII);
                if(!value.equals("87a") && !value.equals("89a")) throw new IOException("Unsupported GIF version.");
                skip(input,4);int flags=octet(input);skip(input,2);
                if((flags&128)!=0)skip(input,3L*(2<<(flags&7)));
                while(true) {
                    int kind=octet(input);
                    if(kind==0x3b)return;
                    if(kind==0x2c) {
                        skip(input,8);int local=octet(input);
                        if((local&128)!=0)skip(input,3L*(2<<(local&7)));
                        skip(input,1);subBlocks(input);
                    } else if(kind==0x21) {
                        int label=octet(input);
                        if(label==0xff) {
                            int size=octet(input);
                            if(size!=11)throw new IOException("Invalid GIF application extension.");
                            byte[] id=new byte[11];input.readFully(id);
                            // ICC.1:2010 Annex B.5 defines ICCRGBG1 with authentication code 012.
                            // Reject that identifier even if its authentication/profile bytes are malformed.
                            if(new String(id,0,8,StandardCharsets.US_ASCII).equals("ICCRGBG1")) throw new UnsupportedColour();
                        }
                        subBlocks(input);
                    } else throw new IOException("Invalid GIF metadata block.");
                }
            }
        }
    }
}
