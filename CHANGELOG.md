# Changelog

## 0.1.0 — 2026-10-10 — local release candidate preparation

- Extracted the used Human Insight Reading workflow into a self-contained portable Skill, preserving Chapter Map, cumulative question budget, sessions, source policy, Claim Audit and correction history.
- Removed private roots, vault dependencies, linked template folders and real learning records from the distribution; original project remains unchanged.
- Added three teaching preferences, four provenance labels and risk-proportionate audit routing; clarified that correcting a definition does not always require another question.
- Retained current book index / historical session separation, page/edition distinctions and pause/Next continuity; added portable book asset and optional no-overwrite initialization/read-only recovery helper.
- Adapted original evaluation bookkeeping and 20 cases with original synthetic fixtures; added A–J acceptance cases and deterministic package/state/tally tests.
- Prepared English/Chinese instructions, provenance and test/rights release gates, and a MIT candidate license.
- Clarified reading alongside a reader-supplied original book, using the same edition, preparing ebooks (including a conditional mention of Z-Library) and supporting paper-book passages; no provider dependency or automatic download added.
- No public repository, publication, push, original-book upload, automatic reminders or cloud services introduced. Legacy test scores are not new-version results.

### Alpha acceptance work

- Preserved three independent forward/semantic-review rounds: 27/30, 28/30 and 30/30. Initial failures and a source-limited test input were not erased or regraded into passes.
- Clarified continuation invitations, error-log recovery, source-limited closing, theoretical-mechanism status, reflowable EPUB pagination and per-note source-path checks.
- Corrected V01-F's rubric locator to match its actual fixture and supplied original synthetic content for L02's requested grounded takeaway. The grading criteria were not relaxed to hide failed answers.
- Added a Windows junction fallback for older Path APIs; 23 deterministic tests now report 22 passed and one OS-limited symlink skip. Native Python 3.10 was not executed.
- Actual local CLI tests exercised discovery, continuous co-reading, direct explanation, fatigue, saved discussion vs reading, fresh-thread recovery and saved exhausted-question-budget recovery. Independent trace review passed within those scopes.
- Retained UTF-8 harness failures, console-capture recovery, no-match query exits and the final-review quota interruption. They are separated from reading-assistant behavior failures.
- Current final-run note/source paths resolve; one unchanged archive snapshot needs original-location restoration for its relative link. No global filesystem/no-error guarantee is claimed.
- Prepared an alpha package with completed local checks; owner licensing/attribution and publishing authorization remain pending.

### GitHub publication

- Owner authorized public distribution of the prepared MIT alpha under VanillaArana/deep-reading.
- Added repository/download links and clone-based installation instructions; only the curated source package is published.
- Release label: v0.1.0-alpha. Previous failed test runs and current validation limits remain documented.
