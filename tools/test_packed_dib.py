#!/usr/bin/env python3
"""Production packed-DIB conversion, decoded independently with Java ImageIO."""
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
JAVA = shutil.which("java") or "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
SOURCE = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic"
HARNESS = r'''
import org.catrobat.paintroid.classic.*;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.Arrays;
public class DibRoundTrip {
    static void check(boolean ok,String message) {if(!ok)throw new AssertionError(message);}
    static void put(byte[] a,int at,long n,int count) {for(int i=0;i<count;i++)a[at+i]=(byte)(n>>>(8*i));}
    static byte[] join(byte[] a,byte[] b) {byte[] n=Arrays.copyOf(a,a.length+b.length);System.arraycopy(b,0,n,a.length,b.length);return n;}
    static byte[] header(int size,int width,int height,int bits,int compression,int colours) {
        byte[] a=new byte[size];put(a,0,size,4);
        if(size==12) {put(a,4,width,2);put(a,6,height,2);put(a,8,1,2);put(a,10,bits,2);}
        else {put(a,4,width,4);put(a,8,height,4);put(a,12,1,2);put(a,14,bits,2);put(a,16,compression,4);put(a,32,colours,4);}
        if(size>=108)put(a,56,0x73524742L,4);return a;
    }
    static byte[] wrap(byte[] dib) throws Exception {
        File file=File.createTempFile("dib-fixture-",".unknown");
        try {try(FileOutputStream out=new FileOutputStream(file)){out.write(dib);}
            check(PackedDib.isDib(file),"sniff DIB without extension");
            ByteArrayOutputStream output=new ByteArrayOutputStream();PackedDib.toBmp(file,output);
            check(Arrays.equals(dib,java.nio.file.Files.readAllBytes(file.toPath())),"source must remain intact");return output.toByteArray();
        } finally {file.delete();}
    }
    static BufferedImage decode(byte[] dib,int width,int height) throws Exception {
        BufferedImage image=ImageIO.read(new ByteArrayInputStream(wrap(dib)));
        check(image!=null && image.getWidth()==width && image.getHeight()==height,"dimensions/decode");return image;
    }
    static void colours(BufferedImage image,int... expected) {
        check(expected.length==image.getWidth()*image.getHeight(),"fixture dimensions");int i=0;
        for(int y=0;y<image.getHeight();y++)for(int x=0;x<image.getWidth();x++)
            check((image.getRGB(x,y)&0xffffff)==(expected[i++]&0xffffff),"pixel "+x+","+y+": "+Integer.toHexString(image.getRGB(x,y)));
    }
    static int colour(int x,int y) {return 0xff000000 | ((x*19+y*37)&255)<<16 | ((x*113+y*41)&255)<<8 | ((x*71+y*17)&255);}
    static byte[] encode(int width,int height,boolean dib,long budget) throws Exception {
        ByteArrayOutputStream out=new ByteArrayOutputStream();LegacyImageEncoder.Rows rows=(y,row)->{for(int x=0;x<width;x++)row[x]=colour(x,y);};
        if(dib)LegacyImageEncoder.dib(width,height,rows,out,budget);else LegacyImageEncoder.bmp(width,height,rows,out,budget);return out.toByteArray();
    }
    static void output() throws Exception {
        for(int width:new int[]{1,2,3,4,19,2057})for(int height:new int[]{1,17}) {
            byte[] dib=encode(width,height,true,256L<<20),bmp=encode(width,height,false,256L<<20);
            check(dib[0]==40 && dib[1]==0 && dib.length==bmp.length-14,"true packed DIB header");
            check(Arrays.equals(dib,Arrays.copyOfRange(bmp,14,bmp.length)),"DIB payload same as BMP");
            BufferedImage image=decode(dib,width,height);
            for(int y=0;y<height;y++)for(int x=0;x<width;x++)check(image.getRGB(x,y)==colour(x,y),"exact round trip");
        }
    }
    static void palette() throws Exception {
        for(int header:new int[]{12,40,108,124})for(int bits:new int[]{1,4,8}) {
            int n=header==12?(1<<bits):2;byte[] table=new byte[n*(header==12?3:4)];
            table[2]=(byte)255;table[(header==12?3:4)+1]=(byte)255;
            byte[] data=new byte[]{(byte)(bits==1?0x40:bits==4?0x01:0),0,0,0};
            if(bits==8)data[1]=1;
            byte[] dib=join(join(header(header,2,1,bits,0,n),table),data);
            colours(decode(dib,2,1),0xff0000,0x00ff00);
        }
    }
    static void orientation() throws Exception {
        for(int header:new int[]{40,108,124}) {
            byte[] top=join(header(header,1,-2,24,0,0),new byte[]{0,0,(byte)255,0,0,(byte)255,0,0});
            colours(decode(top,1,2),0xff0000,0x00ff00);
            put(top,8,2,4);colours(decode(top,1,2),0x00ff00,0xff0000);
        }
    }
    static void bitfields() throws Exception {
        for(int size:new int[]{40,52,56,108,124}) {
            byte[] head=header(size,2,1,16,3,0),masks=new byte[12];
            put(masks,0,0xf800,4);put(masks,4,0x07e0,4);put(masks,8,31,4);
            if(size==40)head=join(head,masks);else System.arraycopy(masks,0,head,40,12);
            colours(decode(join(head,new byte[]{0,(byte)0xf8,(byte)0xe0,7}),2,1),0xff0000,0x00ff00);
        }
        // BI_ALPHABITFIELDS stores four masks after a 40-byte header. Normalization retains alpha.
        byte[] head=join(header(40,2,1,32,6,0),new byte[16]);
        put(head,40,0xff0000,4);put(head,44,0xff00,4);put(head,48,0xff,4);put(head,52,0xff000000L,4);
        byte[] wrapped=wrap(join(head,new byte[]{0,0,(byte)255,(byte)255,0,(byte)255,0,(byte)128}));
        check((wrapped[14]&255)==108 && wrapped[30]==3 && wrapped[66]==0 && (wrapped[69]&255)==255,"normalized alpha mask");
        BufferedImage image=ImageIO.read(new ByteArrayInputStream(wrapped));colours(image,0xff0000,0x00ff00);
        check(image.getColorModel().hasAlpha() && image.getRGB(1,0)>>>24==128,"alpha survives normalization");
    }
    static byte[] rle(int bits,byte[] data) {
        byte[] table=new byte[8];table[2]=(byte)255;table[5]=(byte)255;
        return join(join(header(40,3,2,bits,bits==8?1:2,2),table),data);
    }
    static void rle() throws Exception {
        byte[] rle8=new byte[]{3,1,0,0,0,3,0,1,0,0,0,0,0,1};
        colours(decode(rle(8,rle8),3,2),0xff0000,0x00ff00,0xff0000,0x00ff00,0x00ff00,0x00ff00);
        byte[] rle4=new byte[]{3,0x11,0,0,0,3,0x01,0x00,0,0,0,1};
        colours(decode(rle(4,rle4),3,2),0xff0000,0x00ff00,0xff0000,0x00ff00,0x00ff00,0x00ff00);
    }
    static void reject(byte[] dib) throws Exception {try {wrap(dib);throw new AssertionError("accepted malformed DIB");}catch(IOException expected){}}
    static void malformed() throws Exception {
        byte[] valid=encode(3,2,true,256L<<20);
        for(int size:new int[]{4,12,39,40,valid.length-1})reject(Arrays.copyOf(valid,size));
        for(int offset:new int[]{4,8,12,14}) {byte[] bad=valid.clone();put(bad,offset,0,offset<12?4:2);reject(bad);}
        byte[] bad=valid.clone();put(bad,8,0x80000000L,4);reject(bad);
        bad=valid.clone();put(bad,4,0x7fffffff,4);put(bad,8,0x7fffffff,4);reject(bad);
        bad=valid.clone();put(bad,20,10000,4);reject(bad);
        bad=valid.clone();put(bad,20,1,4);reject(bad);
        bad=valid.clone();put(bad,32,0xffffffffL,4);reject(bad);
        for(int compression:new int[]{4,5,99}) {bad=valid.clone();put(bad,16,compression,4);reject(bad);}
        reject(join(header(40,2,1,8,0,257),new byte[1032]));
        byte[] head=join(header(40,1,1,16,3,0),new byte[16]);
        put(head,40,0xf800,4);put(head,44,0xf800,4);put(head,48,31,4);reject(head);
        put(head,44,0x07d0,4);reject(head);
        put(head,44,0x10000,4);reject(head);
        for(byte[] data:new byte[][]{{3,1},{4,1,0,1},{0,2,4,0,0,1},{0,3,0,1},{3,2,0,1},{0,0,0,0,0,0,0,1}})reject(rle(8,data));
    }
    static void profiles() throws Exception {
        for(int size:new int[]{108,124})for(long space:new long[]{0,0x4c494e4bL,0x4d424544L,99}) {
            byte[] dib=join(header(size,1,1,24,0,0),new byte[4]);put(dib,56,space,4);
            try {wrap(dib);throw new AssertionError("accepted unsupported profile");}
            catch(LegacyColourMetadata.UnsupportedColour expected){}
        }
    }
    static void budget() throws Exception {
        for(int[] size:new int[][]{{0,1},{1,-1},{50000,50000},{10,10}}) {
            try {LegacyImageEncoder.dib(size[0],size[1],(y,row)->{throw new AssertionError("read before budget check");},new ByteArrayOutputStream(),1000);throw new AssertionError("budget accepted");}
            catch(IOException expected){}
        }
    }
    public static void main(String[] args) throws Exception {
        switch(args[0]) {case "output":output();break;case "palette":palette();break;case "orientation":orientation();break;case "bitfields":bitfields();break;case "rle":rle();break;case "malformed":malformed();break;case "profiles":profiles();break;case "budget":budget();break;default:throw new AssertionError();}
    }
}
'''


class PackedDibTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="anpaint-dib-codec-")
        path = pathlib.Path(cls.directory.name)
        harness = path / "DibRoundTrip.java"
        harness.write_text(HARNESS)
        subprocess.run([JAVA, "-m", "jdk.compiler/com.sun.tools.javac.Main", "-d", str(path),
                        *(str(SOURCE / x) for x in ("PackedDib.java", "LegacyImageEncoder.java", "LegacyColourMetadata.java")),
                        str(harness)], check=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def run_case(self, name):
        subprocess.run([JAVA, "-Djava.awt.headless=true", "-cp", self.directory.name,
                        "DibRoundTrip", name], check=True, timeout=30)

    def test_true_headerless_dib_output_padding_and_rgb(self): self.run_case("output")
    def test_core_info_v4_v5_palettes(self): self.run_case("palette")
    def test_top_down_and_bottom_up_scanlines(self): self.run_case("orientation")
    def test_rgb565_all_mask_headers_and_alpha_normalization(self): self.run_case("bitfields")
    def test_rle4_and_rle8_literals_and_runs(self): self.run_case("rle")
    def test_truncated_invalid_sizes_masks_offsets_palettes_and_rle(self): self.run_case("malformed")
    def test_profiles_never_silently_treated_as_srgb(self): self.run_case("profiles")
    def test_invalid_size_and_budget_rejected_before_reading(self): self.run_case("budget")


if __name__ == "__main__":
    unittest.main()
