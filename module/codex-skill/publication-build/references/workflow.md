> Coordination update 1.1: [project contract](project-coordination.md) takes precedence for routine AUTO decisions, freshness and optional specialist routing. Gate labels remain checkpoints.

# Workflow

The 13 phases are intake, guideline_refresh, template_validation, compliance_profile,
publication_mapping, latex_generation, compile_repair, reference_display_si_qa,
pdf_visual_qa, content_integrity, source_package, final_compliance, ready.
Persist publication/state.json after each phase with project, target_journal, article_type,
template_source/version, guideline_date, phase, status, build_version, content_freeze,
variants, main/SI/reference/figure/table/visual/content/package status, blockers,
author_decisions and updated_at. Helper stores hashes and build receipts; add human-readable
phase status fields as work progresses. Resume status plus artifacts, do not restart.
Input corrections create a new freeze/build; never edit canonical in place.
Complete routine work automatically; meaningful unresolved choices remain pending.
This is orchestration for a capable agent, not a one-command universal publisher converter.
