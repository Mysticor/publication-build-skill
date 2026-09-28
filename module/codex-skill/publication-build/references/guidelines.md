# Guidelines

At each new journal build, browse the journal/publisher official author instructions,
article-type requirements and submission page. Prefer current primary sources. Save each
retrieved source in compliance/ with URL, retrieval UTC, version/date if available,
official_verified reasoning, snapshot path and SHA256 in guideline_sources.json.
Record actual successful retrieval; login/unavailable pages remain UNKNOWN. Do not use a
blog or old cached rules as proof of current requirements. Refresh when resuming stale builds
or switching journal; record why the material is still current.
Fill profile.json from templates and generate journal_profile.md for the reader. Each field
has value, required and source. NOT_REQUIRED, NOT_APPLICABLE and UNKNOWN are distinct.
Required UNKNOWN prevents readiness. Use field-specific citations/limits, not universal DPI.
Include journal/publisher/article/manuscript type/scope/template/anonymity/title page;
abstract/keywords/main words/pages; references; figures format/resolution/size/color;
tables; SI; graphical abstract/highlights; data/code; conflicts/funding/CRediT/ethics/AI;
source requirements and upload layout. Source record mock:true only in tests.
Extra assets: AVAILABLE, REQUIRED, OPTIONAL, MISSING or AUTHOR_INPUT_REQUIRED. Format
known Stage 3 facts. Never invent authors, contributions, funding numbers or declarations.
Missing scientific graphical abstract → AUTHOR_DECISION_REQUIRED, Stage 2/nature-figure.
Significant content/word/page/figure limit conflict → CONTENT_REVISION_REQUIRED, not deleting
text or reducing margins. Minor legitimate float/layout repairs remain automatic.
