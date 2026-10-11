#!/usr/bin/env python3
"""R-005: source-bound control/branch distinction check, NOT an Android runtime test.

Replay: python recheck_r005.py --fetch --out replay
Offline: --inputs full connector snapshots JSON (snapshot/ref/path/content/sha).
The Python truth table evaluates only extracted boolean branch expressions. It
does not execute Kotlin, draw pixels, model the entire application or certify Malay.
"""
import argparse, ast, hashlib, itertools, json, pathlib, re, urllib.request
import xml.etree.ElementTree as ET

ROOT = 'https://raw.githubusercontent.com/c933103/AN-Paint/'
REFS = {
 'develop': '691f8870649a1d21d1441f4e3d0e795660b23e9a',
 'pr52': '2755e30573d6ea2c071a128b6fa2940fc675af1a',
 'pr51': '512360bffef3abb393557bce29a30217b03c5ecc',
 'pr3': 'b0f916377353f1c8102ad08c4faf132af4c83a2f',
 'integration': '32d196a8fa1cd085646ae3f81722ac8d317daa49',
}
BASE='Paintroid/src/main/'
PATHS=[BASE+'java/org/catrobat/paintroid/classic/'+p+'.kt' for p in
       ('ClassicPaintActivity','PaintCanvas','PaintDocument')]+[
       BASE+'res/values-ms/strings.xml',BASE+'res/values/strings.xml']
KEYS=('ui_smooth_freehand_strokes','ui_smooth_pixel_edges_anti_aliasing')

def require(ok, why):
 if not ok: raise ValueError(why)

def sha256(s): return hashlib.sha256(s.encode()).hexdigest()
def blob(s):
 b=s.encode(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def method(source, start, end):
 a=source.index(start); b=source.index(end,a)
 return source[a:b].rstrip()

def expression(text, env):
 # Reject unrecognized syntax. No eval or arbitrary code execution.
 tokens=re.findall(r'!=|==|&&|\|\||!|[A-Za-z_][A-Za-z_0-9.]*|[0-9]+',text)
 require(''.join(tokens)==re.sub(r'\s+','',text),'unsupported source expression')
 py=' '.join({'&&':'and','||':'or','!':'not'}.get(t,
     str(env[t]) if t in env else t) for t in tokens)
 node=ast.parse(py,mode='eval').body
 def run(n):
  if isinstance(n,ast.Constant) and type(n.value) in (bool,int): return n.value
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.Not): return not run(n.operand)
  if isinstance(n,ast.BoolOp) and isinstance(n.op,(ast.And,ast.Or)):
   v=[run(x) for x in n.values];return all(v) if isinstance(n.op,ast.And) else any(v)
  if isinstance(n,ast.Compare) and len(n.ops)==1:
   a,b=run(n.left),run(n.comparators[0]); op=n.ops[0]
   if isinstance(op,ast.Eq):return a==b
   if isinstance(op,ast.NotEq):return a!=b
  raise ValueError('unsupported AST')
 return bool(run(node))

def inspect(files):
 activity,canvas,document,ms,en=[files[p] for p in PATHS]
 settings=method(activity,'    private fun showDrawingSettings(', '\n    private fun syncFullscreen')
 stroke=method(canvas,'    private fun stroke(', '\n    private fun spray')
 paint=method(document,'    fun paint(tool:', '\n    fun fill(')
 bindings=re.findall(r'toggle\(ui\(R\.string\.(ui_smooth_[a-z_]+)\),document\.(\w+)\) \{ document\.(\w+)=it \}',settings)
 require(bindings==[(KEYS[0],'strokeSmoothing','strokeSmoothing'),
                    (KEYS[1],'antialiasing','antialiasing')],'cross-wired toggles')
 require('var strokeSmoothing = false' in document and 'var antialiasing = false' in document,'independent defaults')
 require('setOnCheckedChangeListener' in settings and 'change(on)' in settings,'toggle callback absent')
 require('val paint = document.paint(tool)' in stroke,'stroke must obtain document paint')
 conditions=re.findall(r'(?:else )?if \(([^)\n]+)\)',stroke)
 require(len(conditions)==3,'unexpected stroke branch count')
 flat,smooth,point=conditions
 aa=re.search(r'^\s*isAntiAlias = (.+)$',paint,re.M).group(1)
 require('strokeSmoothing' not in paint,'paint AA unexpectedly depends on smoothing')
 require('antialiasing' not in stroke,'path choice unexpectedly depends on AA')
 require('quadTo(from.x,from.y,mid.x,mid.y)' in stroke,'quadratic path missing')
 require('val mid=PointF((from.x+to.x)/2,(from.y+to.y)/2)' in stroke,'midpoint changed')
 require('smoothedPrevious=mid' in stroke,'smoothing history missing')
 require('canvas.drawPoint(to.x, to.y, paint)' in stroke,'point fallback missing')
 require('else canvas.drawLine(from.x, from.y, to.x, to.y, paint)' in stroke,'line fallback missing')
 labels=[]
 for text,expected in [(ms,['Licinkan sapuan bebas','Licinkan tepi piksel (antialias)']),
                       (en,['Smooth freehand strokes','Smooth pixel edges (anti-aliasing)'])]:
  root=ET.fromstring(text);values=[]
  for key,want in zip(KEYS,expected):
   nodes=root.findall("string[@name='%s']"%key)
   require(len(nodes)==1,'missing/duplicate label '+key)
   value=''.join(nodes[0].itertext());require(value==want,'label changed '+key)
   require('%' not in value and '@string/' not in value,'unexpected format or alias')
   values.append(value)
  labels.append(values)
 cases=[]
 for tool_id,smoothing,antialias,flat_tip,finishing,same in itertools.product(range(4),*((False,True),)*5):
  pencil=tool_id==0
  env={'document.strokeSmoothing':smoothing,'antialiasing':antialias,
       'document.brushTip':2 if flat_tip else 0,'tool':tool_id,
       'PaintTool.PENCIL':0,'PaintTool.BRUSH':1,'finishing':finishing,'from':0,'to':0 if same else 1}
  actual=('flat_brush' if expression(flat,env) else 'quadratic' if expression(smooth,env)
          else 'point' if expression(point,env) else 'line')
  expected=('flat_brush' if flat_tip and tool_id==1 else 'quadratic'
            if smoothing and not pencil and not finishing and not same else 'point' if same else 'line')
  actual_aa=expression(aa,env)
  require(actual==expected,'branch truth-table mismatch')
  require(actual_aa==(antialias and not pencil),'AA truth-table mismatch')
  cases.append(dict(tool=('PENCIL','BRUSH','WATERCOLOR','ERASER')[tool_id],smoothing=smoothing,antialias=antialias,pencil=pencil,
                    flat_tip=flat_tip,finishing=finishing,same=same,branch=actual,aa=actual_aa))
 return {'bindings':bindings,'labels_ms_en':labels,'conditions':{'flat':flat,'smooth':smooth,'point':point,'aa':aa},
         'method_sha256':{'settings':sha256(settings),'stroke':sha256(stroke),'paint':sha256(paint)},
         'excerpts':{'settings':settings,'stroke':stroke,'paint':paint},'cases':cases}

def main():
 p=argparse.ArgumentParser();p.add_argument('--inputs');p.add_argument('--fetch',action='store_true');p.add_argument('--out',default='receipt')
 a=p.parse_args();require(bool(a.inputs)!=a.fetch,'choose --inputs or --fetch')
 if a.fetch:
  rows=[]
  for name,ref in REFS.items():
   for path in PATHS:
    content=urllib.request.urlopen(ROOT+ref+'/'+path,timeout=60).read().decode()
    rows.append(dict(snapshot=name,ref=ref,path=path,content=content,sha=blob(content)))
 else:rows=json.loads(pathlib.Path(a.inputs).read_text())
 require(len(rows)==25,'expected 25 source files')
 manifest=[];results={}
 for name,ref in REFS.items():
  selected=[x for x in rows if x['snapshot']==name]
  require(len(selected)==5 and {x['path'] for x in selected}==set(PATHS),'incomplete snapshot')
  for x in selected:
   require(x['ref']==ref and blob(x['content'])==x['sha'],'source blob/ref mismatch')
   manifest.append({k:x[k] for k in ('snapshot','ref','path','sha')}|{
    'sha256':sha256(x['content']),'bytes':len(x['content'].encode()),'url':ROOT+ref+'/'+x['path']})
  results[name]=inspect({x['path']:x['content'] for x in selected})
 # Independent controls are not established by a green count: all these causal
 # mutations must fail the same source checker.
 base={x['path']:x['content'] for x in rows if x['snapshot']=='develop'}
 mutations=[('crosswire',PATHS[0],'document.strokeSmoothing=it','document.antialiasing=it'),
            ('conflate_aa',PATHS[2],'tool != PaintTool.PENCIL && antialiasing','tool != PaintTool.PENCIL && strokeSmoothing'),
            ('remove_pencil_exception',PATHS[2],'tool != PaintTool.PENCIL && antialiasing','antialiasing'),
            ('conflate_geometry',PATHS[1],'document.strokeSmoothing && tool','document.antialiasing && tool')]
 rejected=[]
 for name,path,old,new in mutations:
  require(old in base[path],'mutation target absent');changed=base.copy();changed[path]=changed[path].replace(old,new,1)
  try:inspect(changed)
  except ValueError as e:rejected.append({'name':name,'rejection':str(e)})
  else:raise ValueError('mutation unexpectedly passed '+name)
 case_count=sum(len(x['cases']) for x in results.values())
 table=results['develop']['cases']
 for result in results.values():
  require(result['cases']==table,'source snapshots no longer have identical branch truth tables')
  result['case_count']=len(result.pop('cases'))
 summary={'kind':'source-contract and Python branch-expression model only','snapshots':5,
   'verified_source_blobs':len(manifest),'truth_table_cases':case_count,
   'mutation_controls_rejected':rejected,'kotlin_executed':False,'android_runtime_executed':False,
   'production_files_changed':0,'results':results}
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (out/'results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 (out/'branch-truth-table.json').write_text(json.dumps(table,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))

if __name__=='__main__':main()
