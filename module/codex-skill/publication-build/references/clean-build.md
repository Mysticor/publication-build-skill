# Clean Build

Create source ZIP with only required main/SI/variant tex, bib, licensed class/style/bst,
used figures/tables and explicit build/readme files. No logs/aux/previews/cache/debug/old/unused/
tests or system TeX package copies. Inventory includes source SHA256 and exact build commands.
Use relative paths (including bibliographies and transitive inputs). source_check is a basic
guard; inspect dynamic TeX paths and source manifest manually as part of submission audit.
`package` ZIPs source, extracts into an independent temporary directory and runs the same
academic-typesetting strict executor for every entrypoint. A clean build must succeed without
hidden original-working-directory assets. System toolchain/packages are declared dependencies,
not vendored. Receipt binds ZIP/source/current QA inputs. Ensure package contains all roots;
building only main while SI exists is not acceptable.

Before packaging create compliance/build_plan.json: entries (all .tex roots), variants
(full/anonymous as selected), source_files (exact reviewed relative file inventory).
The helper rejects unbuilt roots and undeclared/unused source files. Include SOURCE_MANIFEST
and an engine/build-command README; do not include a generated main.pdf among source figures.
