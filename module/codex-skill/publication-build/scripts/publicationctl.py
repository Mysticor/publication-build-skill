#!/usr/bin/env python3
"""Stage 4 orchestration. Compilation/conversion are delegated, never reimplemented."""
import argparse, collections, hashlib, json, os, re, shutil, subprocess, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path

# Internal project executor; no separately installed skill entry is required.
EXECUTOR = Path(__file__).resolve().parents[2]/'academic-typesetting'
PHASES = ['intake','guideline_refresh','template_validation','compliance_profile','publication_mapping','latex_generation','compile_repair','reference_display_si_qa','pdf_visual_qa','content_integrity','source_package','final_compliance','ready']
AUDITS = ['journal','mapping','figures','tables','references','supplementary','anonymity','content','visual','submission']
FIELDS = 'journal publisher article_type manuscript_type scope template anonymity title_page abstract_limit keywords main_word_limit page_limit reference_style figure_formats figure_resolution figure_sizes figure_colors table_rules graphical_abstract highlights supplementary data_availability code_availability conflicts funding credit ethics ai_disclosure source_requirements upload_layout'.split()
# Shared project coordination; stage logic remains local.
import sys as _coord_sys
_coord_sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'workflow-contract'))
import project_contract as _coord

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text())
def write(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def files(root):
    root=Path(root)
    result={}
    for p in sorted(root.rglob('*')):
        if p.is_symlink(): raise ValueError(f'Symlink not permitted in snapshot/package: {p}')
        if p.is_file(): result[p.relative_to(root).as_posix()]=sha(p)
    return result
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def state(root): return read(Path(root)/'state.json')
def save(root,s):
    if s.get('phase')!='ready' or s.get('status') not in ['MOCK_PUBLICATION_PACKAGE_READY','GENERIC_ACADEMIC_BUILD_READY','PUBLICATION_PACKAGE_READY']:
        for name in ['MOCK_PUBLICATION_PACKAGE_READY','GENERIC_ACADEMIC_BUILD_READY','PUBLICATION_PACKAGE_READY']:
            (Path(root)/(name+'.json')).unlink(missing_ok=True)
    s['updated_at']=now();write(Path(root)/'state.json',s)
def frozen(root):
    r=Path(root);s=state(r)
    if files(r/'canonical')!=s['canonical_hashes']: raise ValueError('CONTENT_REVISION_REQUIRED: frozen Stage 3 inputs changed')
    return s

def init(root,handoff,test_only=False):
    r=Path(root);h=Path(handoff)
    if r.exists(): raise ValueError('Use a new build directory; resume existing state instead')
    for f in ['reviewed_manuscript.md','references.bib']:
        if not (h/f).is_file(): raise ValueError('Missing Stage 3 input: '+f)
    if (h/'readiness.json').exists():
        ready=read(h/'readiness.json')
        test_only=test_only or bool(ready.get('test_only'))
        if ready.get('status')!='REVIEWED_MANUSCRIPT_READY': raise ValueError('Stage 3 not ready')
    elif not (h/'REVIEWED_MANUSCRIPT_READY.md').exists() and not test_only:
        raise ValueError('Stage 3 readiness evidence required')
    if any(h.glob('MOCK*')): test_only=True
    files(h) # reject symlinks before copying
    if (h/'checksums.json').exists():
        checks=read(h/'checksums.json')
        if not isinstance(checks,dict) or not all(isinstance(v,str) for v in checks.values()): raise ValueError('Unsupported checksum schema: document and validate an adapter before intake')
        if isinstance(checks,dict):
            for f,v in checks.items():
                p=(h/f).resolve()
                if not p.is_relative_to(h.resolve()) or not p.is_file() or sha(p)!=v: raise ValueError('Handoff checksum mismatch: '+f)
    r.mkdir(parents=True)
    shutil.copytree(h,r/'canonical')
    for d in ['compliance','template','source','pdf','submission_assets','evidence']: (r/d).mkdir()
    s={'schema_version':1,'project':r.name,'target_journal':None,'article_type':None,'template_source':None,'template_version':None,'guideline_date':None,'phase':PHASES[0],'status':'BUILD_IN_PROGRESS','build_version':now(),'content_freeze':now(),'mode':'UNRESOLVED','variants':['full'],'test_only':test_only,'canonical_hashes':files(r/'canonical'),'blockers':[],'author_decisions':[],'builds':{},'main_status':'PENDING','si_status':'PENDING','reference_status':'PENDING','figure_status':'PENDING','table_status':'PENDING','pdf_qa_status':'PENDING','content_integrity_status':'PENDING','package_status':'PENDING'}
    save(r,s)
    profile={k:{'value':'UNKNOWN','required':True,'source':None} for k in FIELDS}
    write(r/'compliance/profile.json',profile)
    return s

def profile(root,generic=False):
    r=Path(root);s=frozen(r)
    if generic:
        p={k:{'value':'NOT_APPLICABLE','required':False,'source':'generic mode, no journal compliance claim'} for k in FIELDS}
        for k,v in {'journal':'GENERIC_ACADEMIC_BUILD','template':'academic-paper','anonymity':'full','reference_style':'natbib/plainnat','supplementary':'separate PDF'}.items(): p[k]['value']=v
        write(r/'compliance/profile.json',p);s.update(mode='GENERIC_ACADEMIC_BUILD',target_journal=None,variants=['full'])
    else:
        p=read(r/'compliance/profile.json')
        missing=[k for k in FIELDS if k not in p or (p[k].get('required',True) and p[k].get('value') in [None,'','UNKNOWN'])]
        if missing: raise ValueError('Mandatory UNKNOWN: '+','.join(missing))
        evidence=read(r/'compliance/guideline_sources.json')
        if not evidence or any(not e.get('url','').startswith('https://') or not e.get('retrieved_at') or not e.get('official_verified') for e in evidence): raise ValueError('Current official source evidence required')
        if not s['test_only'] and any(e.get('mock') for e in evidence): raise ValueError('MOCK guidelines cannot authorize real submission')
        for e in evidence:
            q=(r/'compliance'/e['snapshot']).resolve()
            if not q.is_relative_to((r/'compliance').resolve()) or not q.is_file() or sha(q)!=e['sha256']: raise ValueError('Guideline snapshot changed')
        s.update(mode='JOURNAL_BUILD',target_journal=p['journal']['value'],article_type=p['article_type']['value'],guideline_date=max(e['retrieved_at'] for e in evidence))
        s['variants']={'full':['full'],'anonymous':['anonymous'],'both':['full','anonymous']}.get(p['anonymity']['value'],[])
        if not s['variants']: raise ValueError('AUTHOR_INPUT_REQUIRED: resolve anonymity as full/anonymous/both')
    s['profile_hash']=sha(r/'compliance/profile.json');s['phase']='compliance_profile';save(r,s)
    return s

def safe_extract(archive,target):
    target=Path(target);target.mkdir(parents=True,exist_ok=False)
    with zipfile.ZipFile(archive) as z:
        if sum(i.file_size for i in z.infolist())>500_000_000: raise ValueError('Archive exceeds 500 MB; inspect deliberately')
        for i in z.infolist():
            p=(target/i.filename).resolve()
            if not p.is_relative_to(target.resolve()) or '\\' in i.filename or (i.external_attr>>16)&0o170000==0o120000: raise ValueError('Unsafe ZIP member '+i.filename)
        z.extractall(target)

def template(root,path=None,kind='user',url=None,version=None):
    r=Path(root);s=frozen(r)
    if kind=='generic':
        if s['mode']!='GENERIC_ACADEMIC_BUILD': raise ValueError('Generic template must be deliberately selected for a journal')
        path=EXECUTOR/'assets/templates/academic-paper.tex'
    if kind not in ['user','official','generic']: raise ValueError('Invalid template source')
    if not path: raise ValueError('TEMPLATE_REQUIRED: obtain uploaded or official template first')
    existing=s.get('template_source')
    if existing and existing['kind']=='user' and kind!='user': raise ValueError('Consequential template replacement: preserve user priority')
    dest=r/'template'/('revision-'+str(len(list((r/'template').iterdir()))+1))
    p=Path(path)
    if p.suffix.lower()=='.zip': safe_extract(p,dest)
    elif p.is_dir(): files(p);shutil.copytree(p,dest)
    else: dest.mkdir();shutil.copy2(p,dest/p.name)
    inventory=files(dest)
    if not any(n.endswith('.tex') for n in inventory): raise ValueError('TEMPLATE_REQUIRED: no sample/main .tex')
    s.update(template_source={'kind':kind,'url':url,'path':dest.relative_to(r).as_posix(),'sha256':inventory,'retrieved_at':now()},template_version=version or 'UNKNOWN',phase='template_validation')
    save(r,s);write(r/'compliance/template_inventory.json',s['template_source']);return s['template_source']

# Deterministic conservative content signals, with human semantic/PDF review required.
def ast(path,fmt):
    return json.loads(subprocess.check_output(['pandoc',str(path),'-f',fmt,'-t','json'],text=True))
def signals(path,fmt):
    a=ast(path,fmt);words=[];math=[];cites=[];headings=[]
    def textnode(x):
        if isinstance(x,dict):
            if x.get('t')=='Str': return x['c']
            if x.get('t') in ['Space','SoftBreak','LineBreak']: return ' '
            return textnode(x.get('c',[]))
        if isinstance(x,list): return ''.join(textnode(v) for v in x)
        return ''
    def walk(x):
        if isinstance(x,dict):
            t=x.get('t');c=x.get('c')
            if t=='Str': words.extend(re.findall(r'\w+(?:[.−-]\w+)*',c.casefold()))
            if t=='Math': math.append(re.sub(r'\s+','',c[1]))
            if t=='Cite':
                cites.extend(v['citationId'] for v in c[0]);return
            if t=='Header': headings.append(textnode(c[2]).casefold())
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(a['blocks'])
    return {'words':words,'math':math,'cites':cites,'headings':headings}
def integrity(canonical,tex):
    a=signals(canonical,'markdown');b=signals(tex,'latex')
    # Citation display syntax differs between readers; compare citation ids separately.
    ac=collections.Counter(a['words']);bc=collections.Counter(b['words'])
    missing=dict(ac-bc)
    missing_math=list((collections.Counter(a['math'])-collections.Counter(b['math'])).elements())
    missing_cites=list((collections.Counter(a['cites'])-collections.Counter(b['cites'])).elements())
    missing_headings=[x for x in a['headings'] if x not in b['headings']]
    return {'status':'PASS' if not any([missing,missing_math,missing_cites,missing_headings]) else 'CONTENT_REVISION_REQUIRED','missing_tokens':missing,'missing_equations':missing_math,'missing_citations':missing_cites,'missing_headings':missing_headings,'limitation':'Conservative omission signal; added/changed meaning, order, rendered math and captions need mapped semantic review. Do not waive numeric/equation differences without evidence.'}

def source_check(directory):
    d=Path(directory);issues=[];allfiles=files(d)
    for n in allfiles:
        p=d/n
        if p.suffix in ['.tex','.bib','.cls','.sty','.bst']:
            t=p.read_text(errors='replace')
            if re.search(r'(?:\{\s*|=\s*)(?:/|[A-Za-z]:[\\/]|~/)',t): issues.append('absolute path: '+n)
            if p.suffix=='.tex':
                for v in re.findall(r'\\(?:includegraphics|input|include)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}',t):
                    if '\\' in v or '#' in v: continue # dynamic paths require mapping audit
                    q=p.parent/v
                    if not any(x.is_file() for x in [q,*[Path(str(q)+s) for s in ['.tex','.pdf','.png','.jpg','.jpeg','.eps']]]): issues.append('missing asset: '+n+': '+v)
    return issues

def convert(input,output):
    cmd=['bash',str(EXECUTOR/'scripts/convert_document.sh'),str(Path(input).resolve()),str(Path(output).resolve()),'--no-standalone','--natbib']
    subprocess.run(cmd,check=True);return cmd

def compile_one(directory,entry,engine,evidence):
    directory=Path(directory).resolve();ep=(directory/entry).resolve()
    if not ep.is_relative_to(directory) or not ep.is_file(): raise ValueError('Invalid entrypoint')
    issues=source_check(directory)
    if issues: raise ValueError('; '.join(issues))
    ev=Path(evidence);ev.mkdir(parents=True,exist_ok=True)
    cmd=['bash',str(EXECUTOR/'scripts/compile_latex.sh'),str(ep),'--strict','--engine',engine,'--preview','--preview-dir',str((ev/'preview').resolve())]
    result=subprocess.run(cmd,cwd=directory,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (ev/'compile.txt').write_text(result.stdout)
    write(ev/'command.json',{'command':cmd,'exit_code':result.returncode,'executor_sha256':sha(EXECUTOR/'scripts/compile_latex.sh'),'at':now()})
    if result.returncode: raise ValueError('BUILD_FAILED: inspect '+str(ev/'compile.txt'))
    pdf=ep.with_suffix('.pdf')
    if not pdf.exists(): raise ValueError('BUILD_FAILED: PDF missing')
    subprocess.run(['pdftotext','-layout',str(pdf),str(ev/'extracted.txt')],check=True)
    subprocess.run(['pdfinfo',str(pdf)],stdout=(ev/'pdfinfo.txt').open('w'),check=True)
    pages=sorted((ev/'preview').glob('*.png'))
    if not pages: raise ValueError('No preview pages')
    return {'entry':entry,'engine':engine,'pdf_sha256':sha(pdf),'pages':{p.name:sha(p) for p in pages},'at':now()}

def build(root,entry='main.tex',engine='pdflatex'):
    r=Path(root);s=frozen(r);tag=Path(entry).with_suffix('').as_posix().replace('/','__')
    # build source in separate directory: diagnostics never enter source package
    work=r/'evidence'/('build-'+tag)
    if work.exists(): shutil.rmtree(work)
    shutil.copytree(r/'source',work/'source')
    try: b=compile_one(work/'source',entry,engine,work)
    except Exception:
        s['status']='BUILD_FAILED';save(r,s);raise
    target=r/'pdf'/Path(entry).with_suffix('.pdf');target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(work/'source'/Path(entry).with_suffix('.pdf'),target)
    b['source_hash']=digest(files(r/'source'));b['evidence']=work.relative_to(r).as_posix();b['pdf']=target.relative_to(r).as_posix()
    s['builds'][entry]=b;s['main_status' if entry.endswith('main.tex') else 'si_status']='BUILT';s.update(phase='compile_repair',status='BUILD_IN_PROGRESS');save(r,s);return b

def fingerprint(root):
    r=Path(root);s=frozen(r)
    return digest({'canonical':s['canonical_hashes'],'source':files(r/'source'),'template':files(r/'template'),'profile':files(r/'compliance'),'pdf':files(r/'pdf'),'assets':files(r/'submission_assets'),'builds':s['builds'],'variants':s['variants'],'mode':s['mode']})

def attest(root,category,report):
    r=Path(root);s=frozen(r)
    if category not in AUDITS: raise ValueError('Unknown audit')
    report=Path(report);v=read(report)
    if v.get('status')!='PASS' or not v.get('observations') or not v.get('reviewer'): raise ValueError('Audit needs PASS, actual reviewer and observations')
    if category=='visual':
        expected={b['pdf']:sorted(b['pages']) for b in s['builds'].values()}
        if not expected or v.get('inspected_pages')!=expected: raise ValueError('Inspect every current PDF page')
    if category=='content':
        pairs=v.get('pairs',[])
        if not pairs: raise ValueError('Content audit must name canonical/TeX pairs')
        for pair in pairs:
            a=(r/'canonical'/pair['canonical']).resolve();b=(r/'source'/pair['tex']).resolve()
            if not a.is_relative_to((r/'canonical').resolve()) or not b.is_relative_to((r/'source').resolve()): raise ValueError('Invalid integrity pair')
            result=integrity(a,b)
            if result['status']!='PASS': raise ValueError(json.dumps(result))
        if not v.get('pdf_semantic_checked'): raise ValueError('Compare extracted PDF, rendered equations, captions and numeric locks')
    evidence=r/'evidence'/'audits';evidence.mkdir(exist_ok=True)
    v['fingerprint']=fingerprint(r);v['at']=now();write(evidence/(category+'.json'),v)
    return v

ALLOWED={'.tex','.bib','.cls','.sty','.bst','.pdf','.png','.jpg','.jpeg','.eps','.tif','.tiff','.svg','.csv','.txt','.md','.latex','.bbx','.cbx','.lbx','.cfg','.def','.clo','.bbl','.ist','.fd'}
def package(root):
    r=Path(root);s=frozen(r);issues=source_check(r/'source')
    if issues: raise ValueError('; '.join(issues))
    inventory=files(r/'source')
    if not inventory: raise ValueError('Empty source')
    for n in inventory:
        p=Path(n)
        if p.suffix.lower() not in ALLOWED or any(x.startswith('.') or x.lower() in ['test','tests','cache','preview','previews','debug','old'] for x in p.parts): raise ValueError('Non-deliverable source member: '+n)
    for e,b in s['builds'].items():
        if b['source_hash']!=digest(inventory): raise ValueError('Rebuild all PDFs after source changes')
    if not s['builds']: raise ValueError('No successful builds')
    plan=read(r/'compliance/build_plan.json')
    if set(plan.get('entries',[]))!=set(s['builds']): raise ValueError('All declared main/SI/variant entrypoints must be built')
    if plan.get('variants')!=s['variants']: raise ValueError('Variant plan mismatch')
    declared=set(plan.get('source_files',[]))
    if declared!=set(inventory): raise ValueError('Source inventory differs from reviewed build plan (unused/missing files)')
    archive=r/'submission_source.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for n in inventory: z.write(r/'source'/n,n)
        z.writestr('SOURCE_MANIFEST.json',json.dumps(inventory,indent=2))
    clean=[]
    with tempfile.TemporaryDirectory(prefix='publication-clean-') as tmp:
        source=Path(tmp)/'source';safe_extract(archive,source)
        for e,b in s['builds'].items():
            ev=r/'evidence'/'clean'/e.replace('/','__')
            clean.append(compile_one(source,e,b['engine'],ev))
    receipt={'sha256':sha(archive),'source_hash':digest(inventory),'fingerprint':fingerprint(r),'clean_builds':clean,'at':now()}
    write(r/'evidence/package.json',receipt);return receipt

def finalize(root):
    r=Path(root);s=frozen(r);fp=fingerprint(r);problems=[]
    if s['mode'] not in ['GENERIC_ACADEMIC_BUILD','JOURNAL_BUILD']: problems.append('unresolved build mode')
    if not s.get('template_source'): problems.append('template missing')
    elif files(r/s['template_source']['path'])!=s['template_source']['sha256']: problems.append('template core changed')
    if s.get('template_source'):
        template_dir=r/s['template_source']['path']
        for name,original_hash in s['template_source']['sha256'].items():
            if Path(name).suffix in ['.cls','.sty','.bst']:
                for copied in (r/'source').rglob(Path(name).name):
                    if sha(copied)!=original_hash: problems.append('publisher core modified: '+str(copied.relative_to(r)))
    if sha(r/'compliance/profile.json')!=s.get('profile_hash'): problems.append('profile changed: revalidate')
    for name in AUDITS:
        p=r/'evidence/audits'/(name+'.json')
        if not p.exists() or read(p).get('fingerprint')!=fp: problems.append('missing/stale '+name+' audit')
    p=r/'evidence/package.json'
    if not p.exists(): problems.append('clean package missing')
    else:
        receipt=read(p)
        if receipt['fingerprint']!=fp or not (r/'submission_source.zip').exists() or receipt['sha256']!=sha(r/'submission_source.zip'): problems.append('stale/tampered clean package')
    for e,b in s['builds'].items():
        if b['source_hash']!=digest(files(r/'source')) or not (r/b['pdf']).is_file() or sha(r/b['pdf'])!=b['pdf_sha256']: problems.append('stale build '+e)
    if s.get('blockers'): problems.extend(s['blockers'])
    if any(d.get('status')=='PENDING' for d in s['author_decisions']): problems.append('pending consequential choice')
    if problems:
        s['status']='BLOCKED';save(r,s);raise ValueError('; '.join(problems))
    marker='MOCK_PUBLICATION_PACKAGE_READY' if s['test_only'] else ('GENERIC_ACADEMIC_BUILD_READY' if s['mode']=='GENERIC_ACADEMIC_BUILD' else 'PUBLICATION_PACKAGE_READY')
    s.update(status=marker,phase='ready',main_status='PASS',si_status='PASS',reference_status='PASS',figure_status='PASS',table_status='PASS',pdf_qa_status='PASS',content_integrity_status='PASS',package_status='PASS');save(r,s)
    write(r/(marker+'.json'),{'status':marker,'test_only':s['test_only'],'mode':s['mode'],'fingerprint':fp,'package_sha256':sha(r/'submission_source.zip'),'at':now()})
    return s

def raster(path,width_mm,min_dpi):
    from PIL import Image
    with Image.open(path) as im: pixels=im.width
    effective=pixels/(width_mm/25.4)
    return {'effective_dpi':effective,'status':'PASS' if effective>=min_dpi else 'SOURCE_REEXPORT_REQUIRED','note':'Metadata DPI and interpolation do not create detail. Re-export vector/data at required resolution.'}
def anonymous(paths,identities):
    found=[]
    for p in map(Path,paths):
        if p.suffix=='.pdf': t=subprocess.check_output(['pdftotext',str(p),'-'],text=True)+subprocess.check_output(['pdfinfo',str(p)],text=True)
        else: t=p.read_text(errors='replace')
        for identity in identities:
            if identity.casefold() in t.casefold(): found.append({'file':str(p),'identity':identity})
    return {'status':'PASS' if not found else 'AUTHOR_INPUT_REQUIRED','leaks':found}
def decision(kind,alternatives=1,material=False):
    return 'AUTHOR_DECISION_REQUIRED' if _coord.decision(alternatives,material)=='ASK' else 'AUTO'

def content_limit(root,actual,maximum,kind='words'):
    r=Path(root);s=frozen(r)
    if actual>maximum:
        s['status']='CONTENT_REVISION_REQUIRED'
        message=f'{kind}: {actual} exceeds {maximum}; assess Stage 3 content revision without deleting text'
        if message not in s['blockers']: s['blockers'].append(message)
        save(r,s)
        return {'status':s['status'],'issue':message}
    return {'status':'PASS'}


def current_status(root):
    r=Path(root);s=frozen(r)
    if s.get('phase')=='ready':
        marker=r/(s['status']+'.json')
        if not marker.is_file() or read(marker).get('fingerprint')!=fingerprint(r) or not (r/'submission_source.zip').is_file() or read(marker).get('package_sha256')!=sha(r/'submission_source.zip'):
            s.update(status='BUILD_IN_PROGRESS',phase='final_compliance');save(r,s)
    return s

def main():
    p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='command',required=True)
    q=sp.add_parser('init');q.add_argument('root');q.add_argument('handoff');q.add_argument('--test-only',action='store_true')
    q=sp.add_parser('profile');q.add_argument('root');q.add_argument('--generic',action='store_true')
    q=sp.add_parser('template');q.add_argument('root');q.add_argument('--path');q.add_argument('--kind',choices=['user','official','generic'],default='user');q.add_argument('--url');q.add_argument('--version')
    q=sp.add_parser('convert');q.add_argument('input');q.add_argument('output')
    q=sp.add_parser('integrity');q.add_argument('canonical');q.add_argument('tex')
    q=sp.add_parser('build');q.add_argument('root');q.add_argument('--entry',default='main.tex');q.add_argument('--engine',default='pdflatex',choices=['pdflatex','xelatex','lualatex'])
    q=sp.add_parser('attest');q.add_argument('root');q.add_argument('category',choices=AUDITS);q.add_argument('report')
    for c in ['package','finalize','status']:
        q=sp.add_parser(c);q.add_argument('root')
    q=sp.add_parser('content_limit');q.add_argument('root');q.add_argument('actual',type=int);q.add_argument('maximum',type=int);q.add_argument('--kind',default='words')
    q=sp.add_parser('raster');q.add_argument('path');q.add_argument('width_mm',type=float);q.add_argument('min_dpi',type=float)
    q=sp.add_parser('anonymous');q.add_argument('paths',nargs='+');q.add_argument('--identities',nargs='+',required=True)
    args=vars(p.parse_args());cmd=args.pop('command')
    try:
        if 'root' in args and cmd!='init':_coord.enter(args['root'],'publication_build',cmd=='finalize')
        result=(current_status(args['root']) if cmd=='status' else globals()[cmd](**args))
        if cmd=='init':_coord.enter(args['root'],'publication_build')
        if cmd=='finalize':_coord.completed(args['root'],'publication_build',Path(args['root'])/(result['status']+'.json'),{'publication_package':Path(args['root'])/'submission_source.zip'})
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,FileNotFoundError,subprocess.CalledProcessError) as exc: p.exit(1,str(exc)+'\n')
if __name__=='__main__': main()
