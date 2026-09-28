"""Real isolated MOCK acceptance build. Run with Python 3.11+; never touch Stage 3."""
import sys, shutil, json, tempfile, subprocess, re, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import publicationctl as c
from PIL import Image
BASE=Path(sys.argv[1]).resolve();BASE.mkdir(parents=True,exist_ok=True)
H=Path(__file__).resolve().parents[4]/'test-fixtures/handoff'
results=[]
def ok(name,cond):
    if not cond: raise AssertionError(name)
    results.append({'test':name,'status':'PASS'});print('PASS',name,flush=True)
def reject(name,fn):
    try: fn()
    except (ValueError,subprocess.CalledProcessError) as e: ok(name,True);return str(e)
    raise AssertionError('Expected rejection: '+name)
# Whole Stage 3 input preserved; separate equation fixture is explicitly MOCK and frozen too.
h=BASE/'MOCK-input';shutil.copytree(H,h)
(h/'mock_equation.md').write_text('# MOCK math lock\n\nThe locked fixture value is 92.6 percent.\n\n$$x_i^2 + y = 3$$\n')
checks=c.files(h);checks.pop('checksums.json',None);c.write(h/'checksums.json',checks)
r=BASE/'MOCK-generic';c.init(r,h);ok('A: Stage 3 intake and mock propagation',c.state(r)['test_only'])
c.profile(r,generic=True);c.template(r,kind='generic')
ok('D/E: explicitly selected generic article template, no page quota',c.state(r)['mode']=='GENERIC_ACADEMIC_BUILD' and 'academic-paper.tex' in c.state(r)['template_source']['sha256'])
# Uploaded template validation accepts real TeX structure; no copyrighted publisher content.
u=BASE/'MOCK-upload';u.mkdir();(u/'main.tex').write_text('\\documentclass{mock}\n\\begin{document}MOCK\\end{document}\n')
(u/'mock.cls').write_text('\\NeedsTeXFormat{LaTeX2e}\n\\ProvidesClass{mock}\n\\LoadClass{article}\n');(u/'mock.sty').write_text('% MOCK local style\n');(u/'mock.bst').write_text('% MOCK inventory only, not executable bibliography style\n')
z=BASE/'MOCK-template.zip'
with zipfile.ZipFile(z,'w') as f:
 for p in u.iterdir(): f.write(p,p.name)
t=BASE/'MOCK-template-intake';c.init(t,h);c.profile(t,generic=True);inventory=c.template(t,z)
ok('B: ZIP inventories tex/cls/sty/bst',len(inventory['sha256'])==4)
reject('C: user template cannot be silently replaced',lambda:c.template(t,kind='generic'))
bad=BASE/'unsafe.zip'
with zipfile.ZipFile(bad,'w') as f:f.writestr('../escape.txt','no')
reject('ZIP traversal rejected',lambda:c.safe_extract(bad,BASE/'unsafe-extract'))
# Mock official profile used only for profile route testing.
p=c.read(t/'compliance/profile.json')
for field in p: p[field]={'value':'NOT_REQUIRED','required':False,'source':'MOCK official fixture'}
p['journal']['value']='MOCK JOURNAL';p['anonymity']['value']='anonymous';p['article_type']['value']='MOCK test'
c.write(t/'compliance/profile.json',p);(t/'compliance/MOCK-guidelines.txt').write_text('MOCK ONLY. No actual journal rules.')
c.write(t/'compliance/guideline_sources.json',[{'url':'https://example.org/MOCK','retrieved_at':c.now(),'official_verified':'MOCK ONLY; not real authority','snapshot':'MOCK-guidelines.txt','sha256':c.sha(t/'compliance/MOCK-guidelines.txt'),'mock':True}])
c.profile(t);ok('A: MOCK journal profile isolated',c.state(t)['target_journal']=='MOCK JOURNAL')
p['funding']={'value':'UNKNOWN','required':True,'source':None};c.write(t/'compliance/profile.json',p)
reject('mandatory UNKNOWN blocks',lambda:c.profile(t))
# Real executor conversion and insertion into generated copy of actual default template.
src=r/'source';preamble=(c.EXECUTOR/'assets/templates/academic-paper.tex').read_text().split('% DOCUMENT METADATA')[0]
preamble=preamble.replace('\\usepackage{amssymb}','% newtxmath already defines these symbols; integration compatibility fix')
preamble=preamble.replace('pdfauthor={Author One, Author Two}','pdfauthor={MOCK Fixture Author}').replace('pdftitle={Paper Title: A Study of Something Important}','pdftitle={MOCK source-traceable arithmetic}').replace('pdfsubject={Computer Science}','pdfsubject={Software acceptance fixture}').replace('pdfkeywords={keyword one, keyword two, keyword three}','pdfkeywords={MOCK}')
preamble=preamble.replace('\\usepackage{amsthm}', '').replace('\\usepackage{newtxmath}', '\\usepackage{amsthm}\n\\usepackage{newtxmath}')
preamble+='\n\\usepackage{longtable}\n\\providecommand{\\tightlist}{}\n'
c.convert(r/'canonical/reviewed_manuscript.md',BASE/'body.tex')
body=(BASE/'body.tex').read_text();body=body.replace('\\section{MOCK:', '\\section*{MOCK:',1)
# Use librsvg solely for lossless vector format adaptation, never imagegen.
(src/'figures').mkdir();subprocess.run(['rsvg-convert','-f','pdf','-o',str(src/'figures/Figure_01.pdf'),str(r/'canonical/figures/final/Figure_01.svg')],check=True)
c.convert(r/'canonical/figures/final/Figure_01_caption.md',BASE/'figure-caption.tex')
c.convert(r/'canonical/tables/final/Table_01.md',BASE/'table.tex')
c.convert(r/'canonical/tables/final/Table_01_caption.md',BASE/'table-caption.tex')
figcap=(BASE/'figure-caption.tex').read_text();table=(BASE/'table.tex').read_text().replace('\\def\\LTcaptype{none}', '').replace('\\begin{longtable}[]{@{}ll@{}}','\\begin{tabular}{ll}').replace('\\end{longtable}','\\end{tabular}').replace('\\endhead','').replace('\\endlastfoot','').replace('\\endfirsthead','').replace('\\endfoot','');tabcap=(BASE/'table-caption.tex').read_text()
table=table.replace('\\bottomrule\\noalign{}','').replace('\\end{tabular}','\\bottomrule\n\\end{tabular}')
# Actual full table + original captions appended unchanged for audit.
assets='\n\\begin{figure}[htbp]\n\\centering\\includegraphics[width=0.85\\linewidth]{figures/Figure_01.pdf}\n\\caption{'+figcap.strip()+'}\n\\end{figure}\n'+table+'\n'+tabcap
shutil.copy2(r/'canonical/references.bib',src/'references.bib')
main=preamble+'\n\\begin{document}\n'+body+assets+'\n\\bibliographystyle{plainnat}\n\\bibliography{references}\n\\end{document}\n'
(src/'main.tex').write_text(main)
c.convert(r/'canonical/reviewed_supplementary.md',BASE/'si-body.tex')
(src/'supplementary.tex').write_text(preamble+'\n\\begin{document}\n'+(BASE/'si-body.tex').read_text()+'\n\\end{document}\n')
# Technical visual mapping: title is not a numbered parent section; avoid duplicate captions.
main=main.replace('\\subsection{','\\section{').replace('\\section{Abstract}','\\section*{Abstract}').replace('\\caption{Figure 1.','\\caption*{Figure 1.')
start=main.index('{ % do not increment counter');end=main.index('\\bibliographystyle')
old=main[start:end];a0=old.index('\\begin{tabular}');b0=old.index('\\end{tabular}')+len('\\end{tabular}')
main=main[:start]+'\\begin{table}[htbp]\n\\centering\n'+old[a0:b0]+'\n\\caption*{'+old[old.index('Table 1.'):].strip()+'}\n\\end{table}\n'+main[end:]
(src/'main.tex').write_text(main)
(src/'supplementary.tex').write_text((src/'supplementary.tex').read_text().replace('\\section{MOCK','\\section*{MOCK'))
# Audit auxiliary equation fixture converted by the same executor, not part of manuscript.
c.convert(r/'canonical/mock_equation.md',BASE/'equation.tex')
eq=(BASE/'equation.tex').read_text();ok('M/N baseline equation conversion',c.integrity(r/'canonical/mock_equation.md',BASE/'equation.tex')['status']=='PASS')
(BASE/'badnumeric.tex').write_text(eq.replace('92.6','92.4'));ok('M: numeric change detected',c.integrity(r/'canonical/mock_equation.md',BASE/'badnumeric.tex')['status']!='PASS')
(BASE/'badmath.tex').write_text(re.sub(r'\\\[.*?\\\]','',eq,flags=re.S));ok('N: lost equation detected',c.integrity(r/'canonical/mock_equation.md',BASE/'badmath.tex')['status']!='PASS')
(src/'main.tex').write_text(main.replace('\\end{document}','\\UndefinedMockCommand\n\\end{document}'))
reject('G: real compiler failure captured',lambda:c.build(r));shutil.copytree(r/'evidence/build-main',BASE/'G-failed-build')
(src/'main.tex').write_text(main)
try:c.build(r)
except Exception: print((r/'evidence/build-main/compile.txt').read_text()[-6000:]);raise
c.build(r,'supplementary.tex');ok('F/G: real converter + strict compilation after repair',True)
ok('H: missing figure blocked',bool(c.source_check(src))==False)
fig=src/'figures/Figure_01.pdf';backup=fig.read_bytes();fig.unlink();reject('H: actual missing figure prevents build',lambda:c.build(r));fig.write_bytes(backup)
(src/'absolute.tex').write_text('\\input{/nonexistent/hidden.tex}')
ok('O: absolute source path detected',any('absolute' in x for x in c.source_check(src)));(src/'absolute.tex').unlink()
img=BASE/'lowres.png';Image.new('RGB',(300,100),'white').save(img)
ok('I: insufficient true raster resolution detected',c.raster(img,25.4,600)['status']=='SOURCE_REEXPORT_REQUIRED')
ok('J: original vector remains unchanged',c.sha(r/'canonical/figures/final/Figure_01.svg')==c.sha(H/'figures/final/Figure_01.svg'))
ok('K: technical auto and consequential choices',c.decision('dpi')=='AUTO' and c.decision('legend')=='AUTO' and c.decision('grayscale',2,True)=='AUTHOR_DECISION_REQUIRED' and c.decision('template_conflict',2,True)=='AUTHOR_DECISION_REQUIRED')
(src/'main.tex').write_text(main.replace('mock_source','missing_mock_key'));reject('L: unresolved bibliography fails strict build',lambda:c.build(r));shutil.copytree(r/'evidence/build-main',BASE/'L-failed-citation');(src/'main.tex').write_text(main)
c.build(r);c.build(r,'supplementary.tex')
ok('Q: full-only build creates no anonymous duplicate',c.state(r)['variants']==['full'] and not (src/'anonymous').exists())
ok('V: full reviewed text survives AST conversion',c.integrity(r/'canonical/reviewed_manuscript.md',src/'main.tex')['status']=='PASS')
# Real independent anonymous test: one anonymous PDF, no fake both requirement.
a=BASE/'MOCK-anonymous';c.init(a,h);c.profile(a,generic=True);c.template(a,kind='generic')
s=c.state(a);s['variants']=['anonymous'];c.save(a,s)
shutil.copytree(src,a/'source',dirs_exist_ok=True)
(a/'source/main.tex').write_text(main.replace('pdfauthor={MOCK Fixture Author}','pdfauthor={}'))
(a/'source/supplementary.tex').write_text((src/'supplementary.tex').read_text().replace('pdfauthor={MOCK Fixture Author}','pdfauthor={}'))
c.build(a);c.build(a,'supplementary.tex')
scan=c.anonymous([a/'pdf/main.pdf',a/'pdf/supplementary.pdf',a/'source/main.tex',a/'source/supplementary.tex'],['MOCK Fixture Author'])
ok('P: actual anonymous main/SI text and metadata',scan['status']=='PASS')
ok('P: identity leak in full PDF is detectable',c.anonymous([r/'pdf/main.pdf'],['MOCK Fixture Author'])['status']!='PASS')
c.write(BASE/'results.json',results)
c.write(BASE/'build-roots.json',[str(r),str(a)])
print('READY FOR ACTUAL ALL-PAGE INSPECTION:',r,a,flush=True)
