# publication-build
Stage 4: frozen reviewed manuscript → current journal compliance → official template →
existing academic-typesetting executor → compile/repair → all-page visual and content QA →
clean-build submission archive. Scientific revisions return to Stage 3.
User templates take precedence subject to explicit material conflicts. No journal means a
separately labelled generic build; layout follows the request, with no fixed page target.
Invoke `$publication-build` with a PUBLICATION_HANDOFF, resume with “continue publication-build”,
or request final Stage 4 checks. See SKILL.md for phases, CLI and maintained references.
Source is under module/codex-skill/publication-build with a ~/.codex/skills symlink.
Tests are MOCK fixtures; current publisher requirements must be fetched for each real build.
