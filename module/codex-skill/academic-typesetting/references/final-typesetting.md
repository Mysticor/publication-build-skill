# Final typesetting workflow

Apply this workflow to existing content, including requests for `.tex` alone.
The agent performs conversion, error repair and visual review; the compile helper
is a build/validation tool, not a substitute for those agent steps.

## 1. Inventory and preserve

Identify the current manuscript using the conversation and project files. If
multiple plausible manuscripts remain, ask which one; do not silently pick an
unrelated draft. Read the entire source and inventory headings, paragraphs,
figures/captions, tables/notes, equations, footnotes, citations, bibliography and
appendices. Preserve their meaning, order, hierarchy and content. Do not invent
missing bibliographic fields, author information or figure captions.

Keep sources and original templates untouched. Use an existing project layout
when present. Otherwise use source/, figures/, template/, references/ and output/
only as useful; do not move existing files to impose this structure. Generate into
output/ (or the project's build/dist convention), with relative asset paths and
all necessary resources. Build there so auxiliary files do not pollute source.

## 2. Select and respect the template

Read supplied template instructions, example .tex, .cls, .sty, .bst and engine
requirements first. User/official templates are the highest layout authority:
Elsevier, IEEE, Springer, MDPI, university, company and custom templates all apply.
Retain documentclass/options, publisher core files, page size, margins, body size,
line spacing, columns, bibliography style and heading format. Copy required files
without modifying them, and compare hashes before delivery. Insert content using
the template's author, abstract, keywords, body and bibliography interfaces.

Resolve conflicts through content insertion, escaping, environment correctness,
paths, tables, equations, citations, package compatibility and front matter.
Never beautify an official layout or silently substitute a generic class. If the
actual template must change, explain the concrete conflict and request a decision.
Do not use automatic microtype/float/PDF-A injection on the official template.

Without a supplied template, choose a layout appropriate to the requested document type. The bundled academic-paper.tex is an optional article starting point; report/thesis/presentation/poster templates are available for those formats. There is no fixed page quota. Preserve real content and remove all sample metadata. Choose the engine according to the template and actual font needs; verify font availability.

## 3. Convert content

Reuse scripts/convert_document.sh for Pandoc-supported formats (check Pandoc
first). A publisher .tex sample is not a Pandoc template: generate a body fragment
with --no-standalone and insert it into the supplied LaTeX interfaces. For DOCX,
extract embedded media to output assets with Pandoc --extract-media, inspect
captions/notes and equations, and compare against the original; conversion is not
proof of fidelity. For TXT choose an explicit parser and preserve paragraph text.
For PDF/scans use the original PDF conversion resources; flag unreadable source
rather than fabricate. Respect existing LaTeX project includes and build rules.

Keep headings, lists, inline/display math, equation/align environments, figures,
table notes, footnotes, labels, citations, bibliography and appendix structure.
Use stable conventional LaTeX. Preserve mathematical symbols, units, numeric
values and technical meanings. Use existing images with correct aspect ratio;
add appropriate figure/caption/label wiring when supported by source/template.
Do not invent cross-reference targets. Prefer booktabs and wrapping columns when
the template permits; constrain tables/images to column or page width as required.
Do not arbitrarily scale body text or alter margins to hide overflow.

Use --natbib or --biblatex as appropriate when retaining citation keys. Do not
apply --citeproc and then also expect BibTeX to resolve those citations. Inspect
bibliography and figure/table/equation references against the source inventory.

## 4. Build the exact deliverable and repair

Preflight engine, latexmk, bibliography backend if used, pdftoppm and required
packages/fonts. Pandoc is needed for its conversion route, not for existing .tex.
Do not install/change the system without authorization. Report exact missing
required versus optional dependencies with OS-appropriate installation advice.
Run Python helpers via `python` on this machine.

Default command (use absolute paths for source and previews):

```bash
bash <skill_path>/scripts/compile_latex.sh /absolute/output/main.tex \
  --strict --engine xelatex --preview --preview-dir /absolute/output/preview
```

Choose pdflatex/lualatex instead when required. `--strict` uses existing latexmk,
retains logs/auxiliaries and rejects compiler errors, missing glyphs, unresolved
references/citations and missing bibliography output. Do not combine it with
--auto-fix/--pdfa/--clean: they could validate a different temporary source or
remove evidence. Apply needed fixes to the actual generated deliverable instead.
A successful exit is necessary, but content and visual checks remain mandatory.

If latexmk is unavailable and installation is not authorized, use the existing
manual backend with --keep-aux, inspect the actual final log yourself, and run
engine → BibTeX/Biber (if needed) → engine → engine until stable. Repeat additional
index/glossary passes when required. This fallback has the same delivery gates;
legacy script exit status alone is insufficient.

On failure read real .log/.blg and compiler output, fix generated content, rebuild.
Handle undefined commands, missing math delimiters/unbalanced braces, missing
files/packages, image paths, citation/bibliography problems, CJK/fonts, table/math
environments. Continue while project-local corrections are possible. If progress
is blocked by unavailable external dependencies, missing user assets or an
unresolved template constraint, report the exact blocker and preserve diagnostics;
do not claim completion. Never send raw errors as the only response.

Check final .log for undefined citations/references, missing characters, duplicate
labels and rerun requests. Confirm .bbl and rendered bibliography actually contain
the intended entries. Verify figure/table/equation numbering and absence of `??`.
Harmless Underfull warnings do not require mechanical elimination.

## 5. Visual and content acceptance

Reuse --preview or scripts/pdf_to_images.sh. Open the rendered image of every page
with the available image-viewing tool (contact sheets may assist navigation but
do not replace legibility checks). Merely producing PNGs is not visual review.
Inspect clipped/overflowing text, oversized/truncated tables, distorted/overflowing
images, captions and notes, missing CJK glyphs, fonts, equations, orphan headings,
abnormal blank areas, misplaced floats, pagination and section progression.
Investigate Overfull warnings for actual visual impact. Fix generated layout
within template rules → compile → render → inspect again after each layout change.
Compare extracted PDF text and source inventory for omissions; text extraction
alone cannot verify layout. Confirm sources and official core files are unchanged.

## 6. Deliver

- LaTeX request: verified .tex plus .bib, assets and required template/build files.
  PDF is still built and visually inspected internally; it need not be primary.
- PDF request: final PDF; keep matching .tex, .bib and all resources.
- LaTeX + PDF request: both plus every required resource.

Keep diagnostics/previews in a clearly marked build area; include the engine and
reproducible build command. Never deliver a stale PDF from a failed build as final.
A concise report states validation and any unresolved limits. Users need only say
“调用 academic-typesetting，把当前文章生成 LaTeX/PDF” or specify their template.
