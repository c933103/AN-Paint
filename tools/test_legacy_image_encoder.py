#!/usr/bin/env python3
"""Round-trip the production BMP/GIF writer through the JDK's independent ImageIO decoder."""
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = shutil.which("java") or "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
SOURCE = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic/LegacyImageEncoder.java"
COLOUR_SOURCE = SOURCE.with_name("LegacyColourMetadata.java")
HARNESS = r'''
import org.catrobat.paintroid.classic.LegacyImageEncoder;
import org.catrobat.paintroid.classic.LegacyColourMetadata;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.Arrays;
public class LegacyRoundTrip {
    static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    static int colour(int x, int y) {
        int value = (int)((((long)x + y * 2057L) * 1103515245L + 12345L) >>> 16) & 255;
        return 0xff000000 | value << 16 | ((value * 37) & 255) << 8 | ((value * 19) & 255);
    }
    static byte[] encode(int w, int h, boolean gif, boolean dither, boolean gradient) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        LegacyImageEncoder.Rows rows = (y, row) -> {
            for (int x = 0; x < w; x++) row[x] = gradient ?
                0xff000000 | (x * 255 / (w-1)) << 16 | (y * 255 / (h-1)) << 8 | ((x+y) * 255 / (w+h-2)) : colour(x,y);
        };
        if (gif) LegacyImageEncoder.gif(w,h,rows,out,512L*1024*1024,dither);
        else LegacyImageEncoder.bmp(w,h,rows,out,512L*1024*1024);
        return out.toByteArray();
    }
    static BufferedImage decode(byte[] encoded, int w, int h) throws Exception {
        BufferedImage image = ImageIO.read(new ByteArrayInputStream(encoded));
        check(image != null && image.getWidth()==w && image.getHeight()==h, "dimensions / decoding");
        return image;
    }
    static void exact(boolean gif) throws Exception {
        for (int w : new int[]{1,2,3,4,19,2057}) for (int h : new int[]{1,17,69}) {
            byte[] encoded = encode(w,h,gif,true,false); BufferedImage image = decode(encoded,w,h);
            for(int y=0;y<h;y++) for(int x=0;x<w;x++) check(image.getRGB(x,y)==colour(x,y),"exact pixel at "+x+","+y+" in "+w+"x"+h);
            if (!gif) {
                long length = (encoded[2]&255L) | (encoded[3]&255L)<<8 | (encoded[4]&255L)<<16 | (encoded[5]&255L)<<24;
                check(length==encoded.length && encoded[10]==54 && encoded[28]==24,"BMP length/header");
            } else check(encoded[encoded.length-1]==0x3b,"GIF trailer");
        }
    }
    static void gradient() throws Exception {
        int w=257,h=129; byte[] a=encode(w,h,true,false,true),b=encode(w,h,true,true,true);
        check(!Arrays.equals(a,b),"dithering must affect a quantized gradient");
        for(byte[] bytes:new byte[][]{a,b}) {
            BufferedImage image=decode(bytes,w,h); double error=0;
            for(int y=0;y<h;y++) for(int x=0;x<w;x++) {
                int rgb=image.getRGB(x,y);
                int dr=((rgb>>>16)&255)-x*255/(w-1),dg=((rgb>>>8)&255)-y*255/(h-1),db=(rgb&255)-(x+y)*255/(w+h-2);
                error+=dr*dr+dg*dg+db*db;
            }
            check(Math.sqrt(error/(w*h*3))<12,"quantization error: "+Math.sqrt(error/(w*h*3)));
        }
    }
    static void bounds() throws Exception {
        LegacyImageEncoder.Rows never=(y,row)->{throw new AssertionError("read before bounds check");};
        for(int[] size:new int[][]{{65536,1},{1,65536},{0,8},{9,-1},{50000,50000}}) {
            try {LegacyImageEncoder.gif(size[0],size[1],never,new ByteArrayOutputStream(),Long.MAX_VALUE,true);throw new AssertionError("accepted invalid size");}
            catch(IOException expected) { }
        }
        try {LegacyImageEncoder.gif(10,10,never,new ByteArrayOutputStream(),1000,true);throw new AssertionError("GIF budget");} catch(IOException expected) { }
        try {LegacyImageEncoder.bmp(10,10,never,new ByteArrayOutputStream(),1000);throw new AssertionError("BMP budget");} catch(IOException expected) { }
    }
    static byte[] bmpHeader(int header, long space) {
        byte[] bytes=new byte[14+header+4];bytes[0]='B';bytes[1]='M';bytes[14]=(byte)header;
        if(header>=108)for(int i=0;i<4;i++)bytes[70+i]=(byte)(space>>>(i*8));
        return bytes;
    }
    static byte[] gifExtension(boolean icc) throws Exception {
        byte[] original=encode(3,2,true,false,false);
        ByteArrayOutputStream out=new ByteArrayOutputStream();out.write(original,0,original.length-1);
        out.write(0x21);out.write(icc?0xff:0xfe);out.write(11);out.write("ICCRGBG1012".getBytes("US-ASCII"));
        if(icc){out.write(3);out.write(new byte[]{1,2,3});}
        out.write(0);out.write(0x3b);return out.toByteArray();
    }
    static void guard(byte[] bytes, int outcome) throws Exception {
        File file=File.createTempFile("colour-guard-",".bin");
        try {
            try(FileOutputStream out=new FileOutputStream(file)){out.write(bytes);}
            try {LegacyColourMetadata.check(file);check(outcome==0,"accepted unsupported metadata");}
            catch(LegacyColourMetadata.UnsupportedColour expected){check(outcome==1,"wrong unsupported response");}
            catch(IOException expected){check(outcome==2,"unexpected malformed response: "+expected);}
        } finally {file.delete();}
    }
    static void colourAllowed() throws Exception {
        guard(bmpHeader(40,0),0);
        for(int header:new int[]{108,124})for(long space:new long[]{0x73524742L,0x57696e20L})guard(bmpHeader(header,space),0);
        guard(encode(3,2,true,false,false),0);guard(gifExtension(false),0);
    }
    static void colourReject() throws Exception {
        for(int header:new int[]{108,124})for(long space:new long[]{0,0x4c494e4bL,0x4d424544L,99})guard(bmpHeader(header,space),1);
        guard(gifExtension(true),1);
    }
    static void colourTruncated() throws Exception {
        guard(Arrays.copyOf(bmpHeader(124,0x73524742L),70),2);
        byte[] gif=encode(3,2,true,false,false);guard(Arrays.copyOf(gif,gif.length-1),2);
        byte[] broken=gifExtension(false);broken[gif.length+1]=(byte)255;guard(broken,2);
        byte[] huge=bmpHeader(40,0);for(int i=0;i<4;i++)huge[14+i]=(byte)255;guard(huge,2);
    }
    public static void main(String[] args) throws Exception {
        switch(args[0]) {case "bmp":exact(false);break;case "gif":exact(true);break;case "gradient":gradient();break;case "bounds":bounds();break;case "colour-allowed":colourAllowed();break;case "colour-reject":colourReject();break;case "colour-truncated":colourTruncated();break;default:throw new AssertionError();}
    }
}
'''


class LegacyEncoderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="anpaint-legacy-codec-")
        path = pathlib.Path(cls.directory.name)
        (path / "LegacyRoundTrip.java").write_text(HARNESS)
        subprocess.run([JAVA, "-m", "jdk.compiler/com.sun.tools.javac.Main", "-d", str(path), str(SOURCE), str(COLOUR_SOURCE), str(path / "LegacyRoundTrip.java")], check=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def run_case(self, case):
        subprocess.run([JAVA, "-Djava.awt.headless=true", "-cp", self.directory.name, "LegacyRoundTrip", case], check=True, timeout=30)

    def test_bmp_padding_bottom_up_rows_and_exact_rgb(self):
        self.run_case("bmp")

    def test_gif_exact_palette_variable_width_lzw_and_dictionary_resets(self):
        self.run_case("gif")

    def test_gif_adaptive_quantization_and_dithered_gradients(self):
        self.run_case("gradient")

    def test_gif_dimensions_and_both_memory_budgets_before_reading(self):
        self.run_case("bounds")

    def test_legacy_colour_metadata_accepts_untagged_and_explicit_srgb(self):
        self.run_case("colour-allowed")

    def test_legacy_colour_metadata_rejects_profiles_before_decoding(self):
        self.run_case("colour-reject")

    def test_legacy_colour_metadata_bounds_truncated_blocks(self):
        self.run_case("colour-truncated")


if __name__ == "__main__":
    unittest.main()
