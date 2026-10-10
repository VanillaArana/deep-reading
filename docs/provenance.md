# Audit, provenance and reuse

This public report intentionally contains no original reader paths, notes, books or historic answer files. A detailed private audit and preservation inventory remain with the project owner outside this distribution.

## Findings from the actual source project

1. **Implemented and used:** a canonical co-reading skill; Chapter Map and A/B/C/D rules; cumulative question budget; active session and Next state in a book index; actual reader expressions in chapter notes; eight claim types, E5–H, source cards, Claim Audit and real error entries; Markdown recovery; 20-case offline evaluation bookkeeping with retained historic failures.
2. **Implemented with defects:** fixed private paths, vault-specific links, filesystem junctions for discovery/templates, machine-specific validation, duplicated old/current progress descriptions and no explicit three-mode preference field.
3. **Designed only:** deployed multi-role agents, continuous backup/Git, automatic reminders and longitudinal learning-effect measurement. These are not claimed as working source capabilities or added to V0.1.
4. **Duplication/conflict:** old optional questions could look mandatory; subsection budgets could be mis-added; a prior correction rubric required a follow-up even when a later budget rule made it unnecessary; redundant progress areas could disagree. V0.1 uses one current index and meaningful checks only.
5. **Private binding:** a personal library/reading route, real feedback, edition anchors, book copies, machine paths and backup snapshots. All excluded.
6. **Retained strengths:** source-grounded priority, modest questions, stop rights, edition/page boundaries, attribution versus truth, archive exclusion, actual/planned distinction and audit history.
7. **Release work:** portable assets/state, public-data isolation, synthetic fixtures, current skill structure and fresh behavioral acceptance. Local behavioral runs and live CLI recovery now have independent reviews; rights/attribution confirmation and broader user/platform validation remain. See test report for exact versions, failures and coverage limits.

The inspected source did not have a standalone CLAIM-REGISTRY or PROJECT-CHANGELOG, nor a discovered project license. Claims actually lived inline and in audits; absence of a registry did not mean absence of claim tracking. The source roots were not Git repositories, so a separate distribution directory was used. No old file was deprecated, deleted or overwritten.

## File-level derivation

| Source mechanism | V0.1 artifact | Change and rationale |
|---|---|---|
| Main Human Insight Reading SKILL | `skills/deep-reading/SKILL.md` | Preserve routing and session decisions; remove private root; add mode/preferences and portable storage boundary |
| reading-session reference and book index | `references/reading-session.md`, book template | Preserve map/budget/pause/Next and single current source; generalize onboarding and long plan |
| evidence-policy reference | `references/evidence-policy.md` | Keep types, levels, actual source access; add four visible provenance labels and risk-proportionate audit |
| psychology-policy reference | `references/psychology-policy.md` | Keep causal/individual limits, alternatives and theory boundaries; conditionally load for applicable genres |
| System/Claim-Audit and error mechanism | `references/claim-audit.md` | Preserve exact-wording and three-color audit; move instructions into self-contained skill, reader logs stay private |
| note-schema and two existing core templates | `references/note-schema.md`, session/concept assets | Preserve light metadata and actual user wording; portable relative links, real packaged assets instead of junctions |
| Existing Markdown state design | `scripts/reading_state.py`, book template | New optional bootstrap/read-only helper, no semantic automation; retains index/session split |
| Existing eval prepare/summarize | `evals/check.py` | Adapt same hidden-rubric export and all-criteria/no-hard-fail counting; remove personal vault validation; strengthen invalid-input handling |
| Existing 20 eval cases | `evals/cases.json`, original synthetic fixtures | Keep categories/IDs and regressions; replace published excerpt, relax mandatory post-correction check, add V01-A–J |
| New packaging/storage tests and requested docs | `tests`, README pair, test report, changelog, license | Deterministic verification and usable distribution, with behavior limitations explicit |

Paths beginning references/assets/scripts above are relative to the installable skill. No existing migration/updater was rerun. No source reading data migrated. Generic templates are English; the skill responds and writes in the reader's chosen language without maintaining conflicting template copies.

## Licensing decision

MIT was selected as a simple permissive candidate for a small instruction/script package, using the [OSI MIT text](https://opensource.org/license/mit). The source audit found no existing license or third-party code notice in the material selected for adaptation. That does not establish all rights; before release the owner must review authorship/attribution, the prepared contributor notice and permission to license these derived project instructions. This LICENSE does not grant rights over readers' books, external studies or private data.

No third-party runtime code or dependency is bundled. Optional helpers/tests use Python's standard library. The local skill-creator validator and its dependency were used only for checks and are not redistributed. All public book/demo/source fixtures here are newly authored synthetic material, not copied copyrighted excerpts.

## Compatibility basis

Checked on 2026-10-10: [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for name/description, discovery under `.agents/skills`, optional UI metadata and progressive loading; [Agent Skills specification](https://agentskills.io/specification) for frontmatter and relative resource layout. Cross-host compatibility beyond Codex has not been demonstrated. The current source package has no marketplace/connector requirement.
