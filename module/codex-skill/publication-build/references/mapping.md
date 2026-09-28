# Mapping

Before generation write publication_mapping.md (and machine-readable mapping if useful).
Map every title/author/affiliation/abstract/keyword/section/paragraph/figure/caption/table/
footnote/equation/citation/reference/SI item to exact source and destination. Preserve section
hierarchy and numbering semantics; layout wrapper numbering changes need explicit crossrefs.
Stage 3 often keeps figure captions and tables outside reviewed_manuscript.md; join these
from manuscript_asset_manifest.csv by IDs, hashes and final paths. Keep duplicate source
content out of output while proving every intended item appears once. Identify main/SI placement
from reviewed source and official rules; scientific relocation needs Stage 3 if meaning changes.
Record asset conversions with original/derived hashes, physical sizes and generator commands.
Missing referenced asset blocks; never invent a replacement graphic or measurement.
