# Portable Markdown state

Adapted from the original book index/current progress, chapter notes/history and light metadata. Retain an existing reader layout; do not bulk-migrate a vault. Generic relative Markdown links work in ordinary editors and optionally Obsidian.

## Smallest new library

```text
reader-owned-root/
  book-id/
    book.md                 Canonical current state and long plan
    sessions/               Actual session notes; retain history
    concepts/               Only when reusable knowledge is ready
    AI-ERROR-LOG.md          Actual errors; create on demand
    archive/                Dated distinct backups; never current state
```

Use the bundled book/session/concept templates as working prompts, not a requirement to fill every field. Store reader content outside the public package. Keep UTF-8. Link only existing files; for a proposed session use plain text until its note exists. Prefer stable title/anchor locations to unverified page percentages. The helper optionally initializes this layout; manual copying works without Python.

Resolve relative references from the directory of the note containing them, including frontmatter source-path strings, not from the book index or workspace root. After saving, check file targets for each changed note. A path valid in book.md may be wrong in sessions/S001.md; do not copy it unchanged without recalculating. Source-card IDs such as S1 are not file paths. Keep a verified plain address when a clickable target cannot be established.

## What the book index must recover

Known title/author/edition/ISBN and their verification basis; actual accessible text and contents; learning goal/preference/time; proposed long plan; current reading location and date of actual report (different from date read if unknown); read/discussed/demonstrated-understanding separately; current Session ID/state/planned range/actual stop/cumulative question count; latest actual session link; important unresolved/review items; concrete proposed Next Session.

The session records actual date or unknown, edition/access scope, planned vs actual range, reader's verbatim expression distinct from AI's interpretation, discussion/corrections, claims/sources only as needed, question count and closing/Next. User paraphrases must be labeled, not wrapped in quotation marks as their verbatim wording. Do not fill in understanding on their behalf. The absence of a field never implies completion or certainty.

On recovery, read the canonical index, linked/latest formal session, relevant map and prior error log. Archives cannot reset progress. If dated session evidence and the index conflict, explain the conflict and recover the last supported state; do not automatically choose the furthest position. Never advance to proposed Next if the active/paused unit is incomplete. No authoritative state: ask for minimal actual position, not a fabricated restart.

## Light metadata for reusable notes

```yaml
type: reading # or concept
status: draft
claim_type: []
evidence_level: not_assessed
confidence: unassessed
source: []
controversy: not_assessed
ai_inference: null
last_verified: null
audit_status: not_run
```

This comes from the original schema; index/archives/raw notes do not need these fields. Evidence is per claim in the body: `ID | statement/type | level and reason | source/locator | boundaries/alternatives | audit`. A document-level value cannot upgrade every claim. Confidence is unassessed/low/medium/high with scoped reasons, never an invented percentage. Controversy is not_assessed/disputed/none_identified, where none_identified does not mean none exists. Adding unverified important content invalidates an earlier blanket audit pass. Reader confirmation is separate from scientific checking.

## Saving and failure recovery

Save only within the selected, authorized reader directory. Back up before substantive edits with distinct dated names; preserve all reader wording and historical outcomes. Write the actual session first, then update book.md/current progress, then reopen both. This sequence permits index recovery from session history after a partial save, but is not an atomic multi-file transaction. If interrupted, report what succeeded and what remains. Never claim persistence from a chat output alone.

If the reader declines saving or access is unavailable, output a compact copyable block with edition, actual position, Session status/count, understanding evidence, open/review items and Next boundaries. Mark “not saved.” Recovery can use that block later, but cannot assume a file exists.
