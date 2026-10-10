# Deep Reading · V0.1 alpha

**AI should make you a better reader, not read in your place.**

[中文说明](README.zh-CN.md) · [Provenance and reuse](docs/provenance.md) · [Tests and release checks](docs/test-report.md)

[GitHub repository](https://github.com/VanillaArana/deep-reading) · [Download source ZIP](https://github.com/VanillaArana/deep-reading/archive/refs/heads/main.zip)

Deep Reading is a Codex-first Agent Skill for reading books and essays with a source-grounded tutor and a lightweight learning manager. It is extracted from an existing, used co-reading workflow, preserving its Chapter Map, cumulative question budget, Reading Session, Evidence Policy and Claim Audit mechanisms.

It is useful for readers of nonfiction, psychology, humanities and difficult arguments who want explanations, critical discussion and continuity across chats. Literary/philosophical readings use textual interpretation without forcing empirical evidence grades.

## What V0.1 provides

- A/B/C/D priorities based on the argument and reading goal; partial text produces a provisional local map.
- Guided-first, balanced (default) and explanation-first teaching. “Just explain” works immediately. At most three unsolicited understanding checks per session by default; fewer when already understood.
- Clear text/explanation/external/unverified provenance, scoped evidence checks and correction history.
- Flexible long plans and concrete next-session boundaries, including early stops and fatigue.
- Separate records for reading, discussion, demonstrated understanding and source audit.
- Reader-owned Markdown files and file-based recovery. Optional Obsidian compatibility; no database or service.

These are instructions executed by the host agent, not a deterministic reading engine. An optional Python helper creates empty state safely and reads saved files; it does not judge comprehension or verify facts.

## Read alongside the original book

**Read the book yourself, then use Deep Reading to discuss it.** After a subsection, bring your understanding or questions. Giving the reader and the agent access to the same edition makes it easier to locate difficult passages, check the author's wording and resume accurately.

Prepare an ebook you are entitled to use, obtained from a publisher, library or public-domain collection. If you use Z-Library or another source, confirm the particular file's usage rights and edition. Keep the book in your own reading directory and tell Codex its location and the range you want to discuss. The skill includes no books and does not download them.

Prefer EPUB or PDF with extractable text. Check author, translator, edition and contents before starting; readable file structure does not establish that the text is complete or error-free. OCR of scanned pages can be wrong, so verify exact quotations against the page image. Paper books work too: supply the passage and edition information.

The usual flow is **prepare the book → check the edition → read → share your understanding or question → discuss against the text → save progress and Next Session**.

## Install in Codex

Download the source ZIP above and extract it, or clone the repository:

```sh
git clone https://github.com/VanillaArana/deep-reading.git
cd deep-reading
```

The installable folder is `skills/deep-reading`, not this whole repository. Copy it into either your reading workspace's `.agents/skills/deep-reading` or your personal `~/.agents/skills/deep-reading`. Do not overwrite an existing skill without comparing it first.

PowerShell example from this repository root, using a chosen existing reading workspace:

```powershell
$readingWorkspace = Read-Host 'Reading workspace directory'
$skillDestination = Join-Path $readingWorkspace '.agents/skills/deep-reading'
if (Test-Path -LiteralPath $skillDestination) { throw 'Existing skill: compare before replacing' }
New-Item -ItemType Directory -Path (Split-Path $skillDestination) -Force | Out-Null
Copy-Item -LiteralPath './skills/deep-reading' -Destination $skillDestination -Recurse
```

On macOS/Linux, from this repository root (choose your destination first):

```sh
reading_workspace='/your/reading-workspace'
skill_destination="$reading_workspace/.agents/skills/deep-reading"
if [ -e "$skill_destination" ]; then
  printf '%s\n' 'Existing skill: compare before replacing'
else
  mkdir -p "$reading_workspace/.agents/skills"
  cp -R skills/deep-reading "$skill_destination"
fi
```

Invoke `$deep-reading` in Codex and supply your source material. If discovery has not refreshed, restart Codex. Current discovery locations, required metadata and progressive loading were checked against [official Codex documentation](https://learn.chatgpt.com/docs/build-skills) and the [Agent Skills specification](https://agentskills.io/specification) on 2026-10-10. The root is a source distribution; V0.1 does not require a marketplace plugin.

## First session

Example request:

> Use $deep-reading. Here is my book's title, known edition, contents and the first subsection. My goal is to understand the argument. Use balanced teaching, about 20 minutes, and save notes in my separate reading directory.

Provide only available metadata; unknown ISBN/pages can remain unknown. The agent reads supplied materials, proposes a manageable range, helps with your questions and saves actual progress plus a concrete Next Session. It should not generate an unseen book's summary or ask a long initialization questionnaire. Existing records/layouts take priority over fresh templates.

See the [original synthetic co-reading example](examples/demo-session.md). Its dialogue and book are invented, and it never changes real learning records.

## Save and resume

Use a directory outside this source repository and installed skill:

```text
your-reading-library/book-id/book.md
your-reading-library/book-id/sessions/S001.md
```

The book index owns current progress, proposed long plan, open/review questions and Next. Session notes retain actual source range, reader wording, discussion and history. Concepts and an error log are created only when useful. Save permission applies to your chosen reader directory, not unrelated files. Dated distinct backups protect substantive edits. A partial save is reported and recoverable from the session note; multi-file saving is not transactional.

Next chat:

> Use $deep-reading and resume from this book index. Read its latest actual session and relevant error history before proposing the next range.

If saving is declined or unavailable, the agent returns a copyable state block and says it was not saved. A file cannot be assumed from a chat response.

Optional helper, Python 3.10+ and no packages, run from this repository root:

```sh
python skills/deep-reading/scripts/reading_state.py init --root /your/reading-library --book-id sample-book
python skills/deep-reading/scripts/reading_state.py resume --root /your/reading-library --book-id sample-book
```

`init` rejects existing book directories and package locations; it creates no completed session. `resume` reads the index, linked session records and optional error log, without writing. Links must stay within that book. It rejects symlinks/junctions and missing linked records. In an installed copy, use the helper's installed path. Manual template copying remains fully supported.

## FAQ and limits

**Do I need Obsidian, Python or an API key?** No for reading and ordinary Markdown notes. Python is optional for helpers/tests. Codex access is supplied by your own host/account.

**Can I skip questions?** Yes. Ask for direct explanation, change preferences, pause, deepen a secondary topic or change the plan.

**Does an ISBN unlock the book?** No. Supply accessible text or an authorized local file. No automatic downloads. Printed, PDF-file and reader-dynamic pages are distinct and edition-specific.

**Are claims now guaranteed correct?** No. Provenance tags, evidence labels and audits expose support/limits; they do not eliminate hallucinations. Claim audit and reader understanding are separate.

**Are reminders automatic?** No. Review items are saved for reader-initiated sessions. No accounts, background jobs, syncing, vector database or GUI is included.

**What has been tested?** [The test report](docs/test-report.md) records 23 deterministic tests (22 passed, one skipped), three frozen behavioral runs with independent model review (27/30, 28/30, then 30/30), and actual local CLI co-reading, stop/save and fresh-thread recovery. Earlier failures remain recorded. These synthetic tests do not establish universal accuracy or real-reader learning outcomes; model settings were unreported. Other hosts and native macOS/Linux execution remain unverified.

**Why can a backup contain a broken relative link?** An unchanged standalone snapshot retains paths relative to its original note location. Interpret its references from that original directory, or inspect it in an isolated copy of the original layout; preserve current notes. It is never current progress. Use an archive preserving the original folder layout when navigable backups matter.

## License and release preparation

[MIT](LICENSE) covers this package's project material, not readers' books or notes. This repository distributes an early alpha; local technical/behavioral checks and their limits are recorded in the [release checklist](docs/test-report.md). No original book, private note, account configuration or historical conversation is included. A real-reader trial is recommended before presenting it as a stable release.
