"""Independent host fixture probes; executes Java scanner, never Kotlin or Android UI."""
from pathlib import Path
import re, base64, struct, zlib, tempfile, subprocess, json
ROOT=Path(__file__).resolve().parents[1]/'candidate'
text=(ROOT/'Paintroid/src/test/java/org/catrobat/paintroid/local/ImportSelectionTitleTest.kt').read_text()
constants={name:base64.b64decode(data) for name,data in re.findall(r'private const val (\w+) = "([^"]+)"',text)}
fixtures=[]
def add(name,data,expect):fixtures.append((name,data,expect))
for name, expected in [('GIF','GIF|3|true|false'),('WEBP','WebP|3|true|false'),('APNG','APNG|3|true|false'),('APNG_POSTER','APNG|3|true|true'),('STILL_GIF','none'),('STILL_PNG','none')]:add(name,constants[name],expected)
gif_junk=b'\x21\xfe\x01\x78\x00'*100001
for n in range(3):
 add(f'cappedGIF{n}',constants['GIF_HEADER']+constants['GIF_FRAME']*n+gif_junk+constants['GIF_FRAME']*max(2-n,0)+b';',f'GIF|{n}|false|false')
add('exactGIF2',constants['GIF_HEADER']+constants['GIF_FRAME']*2+b';','GIF|2|true|false')
def png_chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
png_junk=png_chunk(b'tEXt',b'')*100001
still=constants['STILL_PNG'];add('cappedPNG',still[:33]+png_junk+still[33:],'PNG|0|false|false')
for name,poster in [('APNG',False),('APNG_POSTER',True)]:
 data=constants[name]; p=8; controls=[]
 while p<len(data):
  size=struct.unpack('>I',data[p:p+4])[0];kind=data[p+4:p+8]
  if kind==b'fcTL':controls.append(p)
  p+=12+size
 for count in (0,1,2):
  # After acTL for count zero; before next frame control for counts one/two.
  at=53 if count==0 else controls[count]
  known_poster=poster and count>0
  add(f'capped{name}{count}',data[:at]+png_junk+data[at:],f'APNG|{count}|false|{str(known_poster).lower()}')
 # Remove final frame controls/data and update the CRC-checked declared count.
 two=data[:controls[2]]+png_chunk(b'IEND',b'')
 two=two[:33]+png_chunk(b'acTL',struct.pack('>II',2,0))+two[53:]
 add(f'exact{name}2',two,f'APNG|2|true|{str(poster).lower()}')
def riff(payload):return b'RIFF'+struct.pack('<I',len(payload)+4)+b'WEBP'+payload
webp=constants['WEBP'];p=12;ends=[]
while p<len(webp):
 size=struct.unpack('<I',webp[p+4:p+8])[0];kind=webp[p:p+4];p+=8+size+(size&1)
 if kind==b'ANMF':ends.append(p)
add('exactWEBP2',riff(webp[12:ends[1]]),'WebP|2|true|false')
for count,at in [(0,30),(1,ends[0]),(2,ends[1])]:
 add(f'cappedWEBP{count}',riff(webp[12:at]+(b'JUNK'+b'\x00'*4)*100001+webp[at:]),f'WebP|{count}|false|false')
add('malformedGIF',constants['GIF'][:-1],'none')
add('unknownContainer',b'not a supported animation container','none')
harness='''import java.io.File;import org.catrobat.paintroid.classic.AnimationMetadata;public class ReviewScan {public static void main(String[] paths){for(String p:paths){AnimationMetadata.Result r=AnimationMetadata.inspect(new File(p));System.out.println(r==null?"none":r.format+"|"+r.frameCount+"|"+r.frameCountExact+"|"+r.pngDefaultImageSeparate);}}}'''
with tempfile.TemporaryDirectory(prefix='a01-independent-scanner-') as tmp:
 folder=Path(tmp);(folder/'ReviewScan.java').write_text(harness)
 subprocess.run(['java','-m','jdk.compiler/com.sun.tools.javac.Main','-d',tmp,str(ROOT/'Paintroid/src/main/java/org/catrobat/paintroid/classic/AnimationMetadata.java'),str(folder/'ReviewScan.java')],check=True,capture_output=True)
 paths=[]
 for name,data,expected in fixtures:
  f=folder/(name+'.bin');f.write_bytes(data);paths.append(str(f))
 actual=subprocess.run(['java','-cp',tmp,'ReviewScan',*paths],check=True,capture_output=True,text=True,timeout=30).stdout.splitlines()
 assert len(actual)==len(fixtures)
 results=[]
 for (name,data,expected),result in zip(fixtures,actual):
  assert result==expected,(name,expected,result)
  results.append({'fixture':name,'expected':expected,'actual':result,'bytes':len(data)})
 out={'scope':'Production Java scanner only. Base64 constants taken directly from new Kotlin source; capped fixtures constructed equivalently in Python. Kotlin helpers, dialogs and image decoding were not executed.','passed':len(results),'results':results}
 Path(__file__).with_name('scanner-extra-results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
