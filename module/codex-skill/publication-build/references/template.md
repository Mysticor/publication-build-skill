# Template

Priority: user specified/uploaded > current journal official > official publisher generic >
explicit document type > academic-paper. Check compatibility, not merely provenance.
ZIP: safely extract, inventory README/sample/main .tex/documentclass/.cls/.sty/.bst/.bib/
figures. `template` accepts ZIP, directory or tex and archives a fresh revision with hashes.
Read dependencies and license; acquire journal files only at runtime. No publisher files
are bundled in this skill. URL: use browser/web to locate official journal/publisher download;
official publisher-maintained Overleaf/GitHub next. Download the actual file, verify contents,
record final URL/date/version/hash and authority reasoning, then pass --path and --url.
A landing page is not a downloaded template. Never run downloaded setup scripts automatically.
When user input has multiple .tex files, identify the actual sample/main from README.
Preserve class, options, fonts, margins, columns, headings and bibliography style. Compare
copied .cls/.sty/.bst hashes with acquired originals. Compatibility repairs belong in generated
integration files. User obsolete template vs mandatory newer official template is consequential:
present actual conflict and choices; do not silently replace. Required unavailable template
→ TEMPLATE_REQUIRED. Optional official template absent → implement documented guidelines,
record evidence and layout verification, do not call it the official class.
