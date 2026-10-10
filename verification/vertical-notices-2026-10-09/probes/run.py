#!/usr/bin/env python3
"""Opt-in, resource-isolated native measurement. Does not alter or run normal app gates.

Supply the compiler/runtime JAR classpaths and both uninstrumented Android framework
JARs listed in ../dependencies.json. AndroidX monitor/idling AAR classes are extracted
as JARs in that inventory. No cached application classes are required or accepted.
"""
from pathlib import Path
import argparse,base64,hashlib,json,os,re,subprocess,sys,xml.etree.ElementTree as ET,zipfile
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--compiler-classpath',required=True)
p.add_argument('--runtime-classpath',required=True)
p.add_argument('--android-jars',type=Path,required=True)
p.add_argument('--suite',choices=['all','measurement','host','transitions','lifecycle'],default='all')
a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();here=Path(__file__).resolve().parent
if out.exists() and any(out.iterdir()):p.error('--out must be a new or empty directory; cached classes/results are not accepted')
out.mkdir(parents=True,exist_ok=True)
for name in ['classes','logs','previews','generated']:(out/name).mkdir(exist_ok=True)
# A precompiled app/class directory could silently replace a missing source input.
for raw in (a.compiler_classpath+os.pathsep+a.runtime_classpath).split(os.pathsep):
 if not raw:p.error('Empty classpath components are forbidden; Java would interpret them as the current directory')
 if not Path(raw).is_file() or Path(raw).suffix!='.jar':p.error('Classpaths must contain existing JAR files only: '+raw)
inventory_path=here.parent/'dependencies.json'
inventory=json.loads(inventory_path.read_text());expected={item['file']:item['sha256'] for item in inventory}
if len(expected)!=len(inventory):p.error('Dependency inventory contains duplicate filenames')
supplied={}
for raw in (a.compiler_classpath+os.pathsep+a.runtime_classpath).split(os.pathsep):
 if raw:supplied.setdefault(Path(raw).name,[]).append(Path(raw))
for filename in ['android-all-11-robolectric-6757853.jar','android-all-15-robolectric-12650502.jar']:supplied.setdefault(filename,[]).append(a.android_jars/filename)
if set(supplied)!=set(expected):p.error('Dependency inventory mismatch; missing='+str(sorted(set(expected)-set(supplied)))+' extra='+str(sorted(set(supplied)-set(expected))))
for name,paths in supplied.items():
 for path in paths:
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected[name]:p.error('Dependency digest mismatch: '+name)
java=repo/'Paintroid/src/main/java/org/catrobat/paintroid/classic';res=repo/'Paintroid/src/main/res' 
rows=[];inputs=[]
def read(path):
 b=path.read_bytes();inputs.append({'path':str(path.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest()});return b.decode()
editor=read(java/'ClassicPaintActivity.kt')
assert 'ui(R.string.ui_cursor_pan_move32)+"\\n"+ui(R.string.ui_cursor_tap_hint37)' in editor, 'Recheck combined fixture against actual cursor caller'
for tag in ['mn-Mong','mnc-Mong','lzh-Hant','en-XV','qaa-Zsye-XV']:
 vs={e.attrib['name']:''.join(e.itertext()) for e in ET.fromstring(read(res/('values-b+'+tag.replace('-','+'))/'strings.xml')) if e.tag=='string'}
 def val(k):return vs[k].replace('\\n','\n').replace("\\'","'").replace('\\"','"')
 for key in ['ui_cursor_pan_move32','ui_cursor_pan_draw32','ui_cursor_tap_hint37','ui_undo','ui_redo','ui_assembly_saved','ui_added_palette23','ui_full_text_copied']:rows.append((tag,key,val(key)))
 rows.append((tag,'combined',val('ui_cursor_pan_move32')+'\n'+val('ui_cursor_tap_hint37')))
 rows.append((tag,'blank-paragraph-stress',val('ui_cursor_pan_move32')+'\n\n'+val('ui_cursor_tap_hint37')))
 for key,name in [('short-file','𠲎🖌️绘画.png'),('long-file','a'*200+'.png'),('joined-word','ᠮᠣᠩᠭᠣᠯ'*45),('mixed-file','ᠮᠣᠩᠭᠣᠯ_𡨸_🧑🏽‍🎨_drawing.png'),('joined-short-file','ᠮᠣᠩᠭᠣᠯ.png'),('unsupported-zwj-file','😀‍😀‍😀‍😀‍😀‍😀.png')]:rows.append((tag,key,val('ui_saved').replace('%1$s',name).replace('%s',name)))
(out/'fixtures.tsv').write_text('\n'.join('\t'.join([tag,key,base64.b64encode(text.encode()).decode()]) for tag,key,text in rows)+'\n')
(out/'fixture-ledger.json').write_text(json.dumps([{'tag':tag,'key':key,'text':text} for tag,key,text in rows],ensure_ascii=False,indent=2)+'\n')
tags=ET.fromstring(read(res/'values/app_language_tags.xml')).find("string-array[@name='app_language_tags']")
(out/'tags.txt').write_text('\n'.join(x.text for x in tags)+'\n')
with zipfile.ZipFile(out/'font-assets.apk','w') as z:
 for asset in ['anpaintnomui.ttf','anpaintwuufallback.ttf','notosansmongolian.ttf']:
  path=repo/'Paintroid/src/main/assets/fonts'/asset;b=path.read_bytes();inputs.append({'path':str(path.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest()});z.writestr('assets/fonts/'+asset,b)
production=[java/n for n in ['LocaleTypography.kt','LocaleNotification.kt','VerticalText.kt']]
for path in production:read(path)
original=read(repo/'Paintroid/src/test/java/org/catrobat/paintroid/local/LocaleNotificationTest.kt')
assert original.count('@Config(sdk=[30,35])')==1
lifecycle=original.replace('@Config(sdk=[30,35])','@Config(sdk=[30,35],manifest=Config.NONE)')
lifecycle=lifecycle.replace('activity.setContentView(FrameLayout(activity))','''org.robolectric.util.ReflectionHelpers.callInstanceMethod<Int>(activity.assets,"addAssetPath",
            org.robolectric.util.ReflectionHelpers.ClassParameter.from(String::class.java,System.getProperty("probe.dir")+"/font-assets.apk"))
        activity.setContentView(FrameLayout(activity))''',1)
(out/'generated/LocaleNotificationTest.kt').write_text(lifecycle)
# Compile the exact current enum/validator fragment. Their UI label getters are not invoked.
names_source=read(java/'SaveOptionsDialog.kt')
fragment=names_source[names_source.index('enum class ImageFormat('):names_source.index('/** One options panel')]
(out/'generated/ExportNamesProbe.kt').write_text('package org.catrobat.paintroid.classic\nimport org.catrobat.paintroid.R\n'+fragment+'\ninternal fun ui(id: Int): String=error("UI resource lookup is outside this diagnostic")\n')
ids={}
for kind,name in re.findall(r'R\.(\w+)\.(\w+)',original+fragment):ids.setdefault(kind,set()).add(name)
(out/'generated/R.kt').write_text('package org.catrobat.paintroid\nobject R {\n'+''.join(' object '+kind+' {\n'+''.join('  const val '+name+'='+str(i+1)+'\n' for i,name in enumerate(sorted(names)))+' }\n' for kind,names in sorted(ids.items()))+'}\n')
methods=['wuDialogAnchorAndBackgroundFallbackRetainTheirWindowBoundaries','aPreviousTimeoutCannotRemoveTheReplacement','hiddenWindowsClearMessagesAndUseSystemToastsInstead','attachedTimeoutAndExternalRemovalDoNotReenterViewGroupDetach','replacementBeforeDeferredVisibilityRemovalKeepsExactlyOneNotice','detachedAndApplicationContextsUseOnlyNormalTextToasts','recreationDetachesOldMessageAndItsTimeoutDoesNotAffectNewWindow','overlayDoesNotConsumeDrawingInputOrKeyboardFocus','dialogDismissAndReshowReattachesTheSameContentWithoutNotifications','dialogDismissAndReshowCannotRetainAnUntimedNotice','edgeToEdgeAndAlreadyFittedWindowsRespectBarsCutoutsAndImeWithoutDoubleInsets','ordinaryLocalesKeepTheirSystemToastBehavior']
ledger=[]
suites=['measurement','host','transitions','lifecycle'] if a.suite=='all' else [a.suite]
plan=['compile']+[f'{suite}-api{sdk}' for sdk in [30,35] for suite in suites]
(out/'run-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
def status(state):
 (out/'run-status.json').write_text(json.dumps({'state':state,'planned_stages':len(plan),'completed_stages':sum(x['state']=='passed' for x in ledger)},indent=2)+'\n')
def run(name,command):
 import time
 stage={'stage':name,'state':'running','exit_code':None};ledger.append(stage)
 def save():
  (out/'execution.json').write_text(json.dumps(ledger,indent=2)+'\n')
 save();status('running');started=time.monotonic()
 try:
  with (out/'logs'/f'{name}.log').open('w') as log:result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=900)
  stage.update(state='passed' if result.returncode==0 else 'failed',exit_code=result.returncode)
 except subprocess.TimeoutExpired:
  stage.update(state='timed_out',exit_code=124)
 except OSError as error:
  stage.update(state='execution_error',exit_code=127,error=type(error).__name__)
 except KeyboardInterrupt:
  stage.update(state='interrupted',exit_code=130)
 stage['duration_seconds']=round(time.monotonic()-started,3);save()
 print(name,stage['state'],stage['exit_code'],flush=True)
 if stage['state']!='passed':
  status(stage['state'])
  log=out/'logs'/f'{name}.log'
  if log.exists():print(log.read_text()[-5000:],flush=True)
  sys.exit(stage['exit_code'])
android35=a.android_jars.resolve()/'android-all-15-robolectric-12650502.jar'
cp=os.pathsep.join([str(out/'classes'),a.runtime_classpath,str(android35)])
sources=production+list(here.glob('*.kt'))+list((out/'generated').glob('*.kt'))
(out/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
(out/'probe-sources.json').write_text(json.dumps([{'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path in [*sources,Path(__file__).resolve(),inventory_path]],indent=2)+'\n')
status('prepared')
run('compile',['java','-Xmx768m','-cp',a.compiler_classpath,'org.jetbrains.kotlin.cli.jvm.K2JVMCompiler','-no-stdlib','-no-reflect','-Xnullability-annotations=@android.annotation:ignore','-jvm-target','17','-Xstring-concat=inline','-classpath',cp,'-d',str(out/'classes'),*map(str,sources)])
for sdk in [30,35]:
 prefix=['java','-Xmx768m','--add-opens=java.base/java.io=ALL-UNNAMED','-Drobolectric.usePreinstrumentedJars=false',f'-Drobolectric.dependency.dir={a.android_jars.resolve()}',f'-Drobolectric.enabledSdks={sdk}',f'-Dprobe.dir={out}','-cp',cp]
 for suite,cls in [('measurement','VerticalNoticeMeasurementProbe'),('host','VerticalNoticeHostProbe'),('transitions','NoticeTransitionProbe'),('lifecycle','LocaleNotificationTest')]:
  if a.suite not in ('all',suite):continue
  runner=['ProbeSubsetRunner','org.catrobat.paintroid.local.'+cls,*methods] if suite=='lifecycle' else ['org.junit.runner.JUnitCore','org.catrobat.paintroid.local.'+cls]
  run(f'{suite}-api{sdk}',prefix+runner)

status('completed')
