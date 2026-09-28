# Latex

Read ../academic-typesetting/SKILL.md and ../academic-typesetting/references/final-typesetting.md
relative to this skill’s resolved project directory; these are internal executor resources,
not a separately installed skill. Reuse its
convert_document.sh --no-standalone --natbib (or --biblatex per template) for supported
formats. Insert the body into actual sample interfaces; publisher tex is not a Pandoc template.
The wrapper `publicationctl.py convert` forwards to that existing converter, and build forwards
to compile_latex.sh --strict --engine ... --preview. No duplicated compiler/log parser.
Prefer mandated engine, else pdfLaTeX English / XeLaTeX CJK. Check installed fonts/packages.
No auto dependency installation. Preserve literal math and citation keys; no citeproc plus BibTeX.
Build .tex even if PDF not requested. Strict uses latexmk and validates references/glyphs.
Read real .log/.blg after failure, repair generated integration, rebuild until stable. Keep
failed command/output as evidence before next retry (build replaces the entry's working folder).
Handle missing files, undefined macros, math/braces, tables, fonts, citation passes and floats.
Do not use --auto-fix/--pdfa/--clean with strict or alter publisher cores to hide errors.
Build all main/SI/anonymous entrypoints after all source changes. Keep source-only files in
source/; wrapper compiles isolated copies in evidence/ and copies successful PDF to pdf/.
