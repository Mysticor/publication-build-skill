---
name: publication-build
description: >-
  科研论文第四阶段：将 Stage 3 审后定稿按当前期刊要求生成官方模板 LaTeX、
  已验证 PDF 和可独立编译的投稿源码包。用于第四阶段出版构建、继续 publication-build、
  匿名版、更换投稿期刊，以及普通 Markdown/DOCX 转 LaTeX/PDF 排版；不改科学内容。
---
# Publication Build

## Project coordination contract 1.1 (incremental)
Before local work, run `scripts/projectctl.py open PROJECT_ROOT` and read
[the shared contract](../../../workflow-contract/README.md). This is the authoritative
cross-stage rule for manifest, canonical ownership, staleness, AUTO decisions and optional
Humanizer; it supersedes older routine-approval wording below and in specialist references.
Use the existing intended study root, not the Skills tooling repository. No manifest means
automatic legacy recovery, not restarting Stage 1. Preserve all current working directories.
Register stable result/claim/asset IDs and evidenced dependencies; consume upstream revisions
when selecting inputs. Record owner changes, inspect targeted impact and revalidate affected
objects before publishing. Local CLI init/finalization hooks synchronize the shared contract;
when working through imported helper functions, explicitly run projectctl open/consume/publish.
Gate labels are retained checkpoints, not mandatory user questions: use `projectctl.py
auto-gate STAGE_DIR --gate A --record decisions/auto-a.yaml` for evidence-backed AUTO cases.
Never label an automatic decision as user consent. Consequential alternatives or major
commitments still require actual decisions. Missing necessary scientific facts remain blockers.


Choose the mode from the request. For ordinary file typesetting/conversion, read the
internal executor's `references/final-typesetting.md` and perform that workflow directly;
do not require Stage 3 handoff, journal compliance or a submission package. For Stage 4
publication builds read `references/workflow.md`, then the active phase references.
The internal executor lives at `../academic-typesetting/` relative to this skill's resolved
project directory (an adapted latex-document-skill executor). Read its files directly;
it is no longer a separately installed skill. Never resolve it through ~/.codex/skills.
This skill supplies publication orchestration, never a second LaTeX engine.

## Invariants
- AUTO BY DEFAULT, CONFIRM ONLY CONSEQUENTIAL CHOICES. Resolve routine compliant
  technical choices automatically. No compulsory approval Gate; “第四阶段定稿”
  authorizes the remaining checks. Read `references/decision-policy.md` for exceptions.
- Keep actual research data and frozen Stage 3 reviewed_manuscript.md authoritative.
  Earlier drafts/blueprints cannot replace reviewed claims. main.tex is a build target.
  Scientific changes → CONTENT_REVISION_REQUIRED, return Stage 3; no reviewer/polisher calls.
- User template has priority, checked against current official requirements. A real
  conflict needs a concise consequential choice. Never silently switch publisher class.
- Preserve original figures, data, equations and numbers. Technical re-export is allowed;
  scientific figure redesign, invented details and new graphical abstracts need routing.
- Without a journal, use GENERIC_ACADEMIC_BUILD and choose an appropriate layout
  from the user’s document type and requirements. The bundled academic-paper template is
  an optional article starting point, not a fixed personal default or journal-ready claim.
- Actual compile → repair → recompile → all-page visual QA → semantic integrity →
  clean source-package compile are required, including requests for .tex alone.
- Never mark readiness on rendering or exit status alone. MOCK and generic readiness
  have distinct markers. Missing facts, source assets or mandatory rules remain blockers.

## Execute and resume
On this machine use `python3`.
Locate this skill by its loaded path. Source lives in the project's
`module/codex-skill/publication-build`; the installed skill directory is a symlink.

```text
publicationctl.py init /project/publication /project/PUBLICATION_HANDOFF
publicationctl.py status /project/publication
publicationctl.py profile /project/publication --generic
publicationctl.py template /project/publication --kind generic
publicationctl.py convert /project/publication/canonical/reviewed_manuscript.md /tmp/body.tex
publicationctl.py build /project/publication --entry main.tex --engine pdflatex
publicationctl.py attest /project/publication content /tmp/content-report.json
publicationctl.py package /project/publication
publicationctl.py finalize /project/publication
```
These helpers are deterministic guards, not autonomous scientific or visual reviewers.
Insert converted body into the selected real template using academic-typesetting.
Resolve full paper + captions/tables/SI through explicit mapping; body conversion alone
must not discard separate Stage 3 assets. Profile, reports and decisions require real evidence.
`attest` must follow actual inspection; never populate PASS to make finalize succeed.

## Phase routing
0 intake → [intake](references/intake.md), [handoff](references/handoff.md)
1 guideline refresh → [guidelines](references/guidelines.md)
2 template → [template](references/template.md), [generic](references/generic.md)
3 compliance profile → [guidelines](references/guidelines.md)
4 mapping → [mapping](references/mapping.md)
5–6 generation/build/repair → [latex](references/latex.md)
7 assets/references/SI → [figures](references/figure.md), [tables](references/table.md),
[bibliography](references/bibliography.md), [supplementary](references/supplementary.md),
[anonymous](references/anonymous.md)
8 visual QA → [PDF QA](references/pdf-qa.md)
9 integrity → [content](references/content-integrity.md)
10 source → [clean build](references/clean-build.md), [package](references/package.md)
11–12 final checks → [readiness](references/readiness.md)

A journal change creates a new build directory/version from the same frozen Markdown;
retain the previous build. Never transform the old publisher-specific .tex into a new journal.
