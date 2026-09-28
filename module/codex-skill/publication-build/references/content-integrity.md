# Content Integrity

Compare canonical Markdown → mapped generated LaTeX → extracted PDF plus rendered math.
Use Pandoc AST signals to avoid naive markup diff. The helper checks missing text tokens,
heading strings, citation keys and normalized math. It is conservative: reorderings, extra
claims, synonyms, PDF glyph ambiguity and template macro parsing require manual semantic QA.
Do not waive a failed signal just to pass; inspect mapping and fix conversions. Unsupported
custom macros can be checked with a documented expanded audit copy tied to exact source hashes,
then implement an evidence-backed adapter instead of bypassing final gates.
Lock percentages, sample sizes, p-values, CI, model parameters, counts, errors and experiment
IDs to Stage 3 numeric_trace/data records. 92.6→92.4 blocks. Check equation terms/signs/subscripts/
superscripts and crossrefs; lost equation blocks. Compare every paragraph, title, abstract,
section, caption, reference and SI link, including separate figure/table sources. No factual
polish or scientific additions. content audit includes canonical/tex pairs and pdf_semantic_checked.
Machine PASS alone never establishes equivalence; observations explain actual semantic comparison.
