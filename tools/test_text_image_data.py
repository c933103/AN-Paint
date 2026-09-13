#!/usr/bin/env python3
"""Check text-image primitives against the JDK Base64 implementation and fixed image/ASCII references."""
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Paintroid/src/main/java/org/catrobat/paintroid/classic/TextImageData.java"
JAVA = shutil.which("java") or "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
HARNESS = r'''
import org.catrobat.paintroid.classic.TextImageData;
import java.io.*;
import java.util.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
public class TextImageChecks {
    static void check(boolean yes,String message) {if(!yes)throw new AssertionError(message);}
    static byte[] decode(String text,long maximum)throws Exception {
        ByteArrayOutputStream output=new ByteArrayOutputStream();
        TextImageData.decode(new ByteArrayInputStream(text.getBytes(StandardCharsets.UTF_8)),output,maximum);
        return output.toByteArray();
    }
    static void malformed(String text)throws Exception {
        try {decode(text,1024);throw new AssertionError("Accepted: "+text);}catch(IOException expected) { }
    }
    static void roundTrip()throws Exception {
        Random random=new Random(29471);
        for(int length:new int[]{1,2,3,4,5,17,127,128,129,8193,100000}) {
            byte[] original=new byte[length];random.nextBytes(original);
            ByteArrayOutputStream output=new ByteArrayOutputStream();
            TextImageData.Base64Output encoder=new TextImageData.Base64Output(output);
            for(int p=0;p<length;p+=17)encoder.write(original,p,Math.min(17,length-p));
            encoder.finish();encoder.finish();
            String encoded=output.toString("US-ASCII");
            check(encoded.equals(Base64.getEncoder().encodeToString(original)),"Independent encoder: "+length);
            check(Arrays.equals(original,Base64.getDecoder().decode(encoded)),"Independent decode");
            check(Arrays.equals(original,decode(encoded,length)),"Decode exact bound");
            check(Arrays.equals(original,decode(encoded.replace("=",""),length)),"Canonical unpadded decode");
            String spaced=encoded.replaceAll("(.{5})","$1 \r\n\t");
            check(Arrays.equals(original,decode("\ufeff \nDATA:image/png;charset=utf-8;BASE64,\n"+spaced,length)),"URI/BOM/whitespace");
            try {decode(encoded,length-1);throw new AssertionError("Exceeded cap");}catch(IOException expected) { }
        }
    }
    static void invalid()throws Exception {
        for(String text:new String[]{""," ","A","A===","=AAA","AA=A","AA==A","AAA=AA==","A_AA","AAAA!","AB==","AAB=","AB","AAB","TQ=","T===","T=AA","AA==\u0000","data:text/plain;base64,AA==","data:image/png,AA==","data:image/png;base64,","data:image/png;base64,AB=="})malformed(text);
        StringBuilder large=new StringBuilder("data:image/png;");for(int i=0;i<300;i++)large.append('a');large.append(";base64,AA==");malformed(large.toString());
    }
    static boolean inspect(byte[] bytes)throws Exception {
        File file=File.createTempFile("text-image-",".txt");
        try {Files.write(file.toPath(),bytes);return TextImageData.inspect(file);}finally {file.delete();}
    }
    static void detection()throws Exception {
        byte[] png=Base64.getDecoder().decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aS1cAAAAASUVORK5CYII=");
        check(inspect(Base64.getEncoder().encode(png)),"Raw PNG detected");
        check(inspect(("data:image/png;base64,"+Base64.getEncoder().encodeToString(png)).getBytes("US-ASCII")),"PNG URI detected");
        check(!inspect(png),"Binary PNG is not text");
        check(!inspect("ordinary prose about a sketch".getBytes("US-ASCII")),"Prose is not text image");
        check(!inspect(Base64.getEncoder().encode("This is not an image".getBytes("US-ASCII"))),"Encoded prose rejected");
        check(!TextImageData.imageSignature(new byte[]{0,0,0,24,'f','t','y','p','m','p','4','2'}),"MP4 not misidentified as image");
        check(TextImageData.imageSignature(new byte[]{0,0,0,24,'f','t','y','p','a','v','i','f'}),"AVIF recognized");
    }
    static void ascii()throws Exception {
        check(TextImageData.asciiRows(400,200,80)==20,"Character aspect ratio");
        check(TextImageData.asciiRows(10000,1,40)==1,"Minimum row");
        for(int[] dimensions:new int[][]{{0,1,80},{20,20,39},{20,20,241},{1,10000000,240}}) {
            try {TextImageData.asciiRows(dimensions[0],dimensions[1],dimensions[2]);throw new AssertionError("Invalid ASCII geometry");}catch(IOException expected) { }
        }
        for(boolean invert:new boolean[]{false,true}) {
            ByteArrayOutputStream out=new ByteArrayOutputStream();
            TextImageData.ascii(40,2,(y,row)->Arrays.fill(row,y==0?0xff000000:0xffffffff),out,invert);
            String[] lines=out.toString("UTF-8").split("\n",-1);
            check(lines.length==3 && lines[0].length()==40 && lines[1].length()==40 && lines[2].isEmpty(),"Fixed-width ASCII and newline");
            check(lines[0].charAt(0)==(invert?' ':'@') && lines[1].charAt(0)==(invert?'@':' '),"Luminance and inversion");
        }
        ByteArrayOutputStream out=new ByteArrayOutputStream();
        TextImageData.ascii(40,1,(y,row)->Arrays.fill(row,0x00000000),out,false);
        check(out.toString("US-ASCII").charAt(0)==' ',"Transparency composites on white");
    }
    public static void main(String[] args)throws Exception {
        switch(args[0]) {case "roundtrip":roundTrip();break;case "invalid":invalid();break;case "detection":detection();break;case "ascii":ascii();break;default:throw new AssertionError();}
    }
}
'''


class TextImageDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="text-image-host-")
        cls.folder = pathlib.Path(cls.directory.name)
        harness = cls.folder / "TextImageChecks.java"
        harness.write_text(HARNESS)
        subprocess.run([JAVA, "-m", "jdk.compiler/com.sun.tools.javac.Main", "-d", str(cls.folder), str(SOURCE), str(harness)], check=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def run_case(self, name):
        result = subprocess.run([JAVA, "-cp", str(self.folder), "TextImageChecks", name], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_base64_matches_independent_encoder_and_decoder(self):
        self.run_case("roundtrip")

    def test_malformed_padding_alphabet_uri_and_size_fail(self):
        self.run_case("invalid")

    def test_detection_requires_an_image_signature(self):
        self.run_case("detection")

    def test_ascii_aspect_luminance_inversion_and_size(self):
        self.run_case("ascii")


if __name__ == "__main__":
    unittest.main()
