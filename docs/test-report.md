# V0.1 test status and release gates

Date: 2026-10-10. This is an alpha candidate with completed local checks, not a guarantee of correctness or learning outcomes.

## Reproduce deterministic checks

From the repository root, Python 3.10+ (no packages):

```sh
python -B -m unittest discover -s tests -v
```

The suite checks no-overwrite initialization, unrelated-note preservation, invalid IDs and escaping links, package data isolation, Unicode/spaced directories, missing records, file-based recovery in a separate process, archive exclusion, read-only recovery and strict eval coverage/failure bookkeeping. Symlink testing may be skipped where the OS disallows creating symlinks; a skip is never counted as a pass. These tests validate concrete storage/bookkeeping outcomes, not wording or teaching judgment.

Executed on Windows with Python 3.12. Results: **23 tests, 22 passed, 1 skipped, 0 failures/errors**. The skip was actual symbolic-link creation, which this OS did not permit. Real Windows directory-junction checks passed both with the native API and with that API disabled to exercise the older-runtime fallback. This is not a native Python 3.10 test. The fallback uses documented [Windows lstat reparse tags](https://docs.python.org/3.10/library/os.html#os.stat_result) and [mount-point constants](https://docs.python.org/3.10/library/stat.html). Skill-creator `quick_validate.py` reported **Skill is valid**; final validation is repeated during packaging. Its private PyYAML validation dependency is not redistributed.

The relocated-install test copied only the skill into a different temporary `.agents/skills/deep-reading` path, then initialized and recovered its own reader library successfully. This proves resource paths/helper portability under the local runtime, not that Codex selected/invoked the installed skill.

The original project's structural validator was also run: 20 original cases still structurally valid, 120 valid links, 14 original books preserved, 47 old inventory files retained, original user quotations preserved, three schema checks, one canonical skill and backup ZIP CRC passed. These are preservation/structure results, not a rerun of the original behavioral suite.

30 behavior inputs were exported without rubrics. Behavioral answers were frozen before separate semantic review; they are not inferred from unit-test results.

## Actual forward and independent semantic reviews

| Run | Cases passed | Failed all-criteria checks | Hard failures | Outcome |
|---|---|---|---|---|
| Initial | 27/30 | S02, L02, V01-I | 0 | Continuation invitation/error-log omissions; L02 also lacked material for the requested takeaway |
| Second | 28/30 | P02, S01 | 0 | Missing theory-status and dynamic-pagination explanations; A/H source-path defects additionally noted |
| Final | **30/30** | None | **0** | **97/97 must criteria met; 43 hard-fail conditions checked without triggering** |

Each run used a fresh forward agent and a different source-grounded reviewer. A batch shares one forward context while separating case material/state; it is not 30 independently fresh conversations. Exact tested/reviewer model and reasoning settings were unavailable and remain unknown. Inputs, actual answers, hashes, operation records, reviews and failures are retained privately; no raw paths, account context or old conversations are distributed.

V01-F's planned-end locator was corrected against its fixture before grading. L02's first score remains failed with a source-limitation flag; subsequent input adds original synthetic passage and reader expression without relaxing the closing criterion. Later scores cannot be described as identical-input measurements. Earlier answers/reviews were not rewritten.

The final reviewer inspected A/H/J files and backups: A remains planned-only; H retains erroneous wording/history and updates both dependencies; J retains the exact KEEP_ME fixture and a matching refusal log. Current source-path fields/local links resolve. File-state checks cannot prove every operation order, independent J pre-state/exit-code evidence, or no side effects across the entire host.

## Actual local CLI co-reading and fresh-thread recovery

Independent review of closed traces and immutable snapshots passed within these exercised scopes:

- Local `.agents/skills/deep-reading` catalog discovery and actual SKILL/reference loading.
- Five successful original-version turns: onboarding, reader feedback, direct explanation, fatigue stop/save and completely fresh-thread recovery.
- Two successful first-revision turns: fresh recovery and true-resume closing save. New explanation stays discussion; actual reading/mastery is not advanced.
- Three successful first-revision budget-probe turns: recover supplied count2, issue one actual third check, save it as unanswered/count3, and recover in a fresh thread without a fourth check. The prior two questions are explicitly synthetic supplied history, not two executed prior turns.

Ten model executions succeeded. Session-first/index-second writes, distinct backups, verification and source/skill preservation are visible in traces. No-write turns are not credited with persistence. The main interrupted session keeps its ID, actual stop, preferences, questions and Next. CLI version was 0.162.0-alpha.17.2; exact model/settings were not reported.

Version scope matters: live CLI scenarios ran against the original and first narrow revision, with their actual hashes retained separately. The final version adds theory/pagination/source-path explanations and the helper compatibility correction; it has its own full30 forward/review run and deterministic tests. Do not relabel all live runs as executions of the final identical files.

## Acceptance coverage A–J

| Test | Prepared coverage | Semantic/model status |
|---|---|---|
| A first use | V01-A and bootstrap tests | Final response/files passed; live onboarding also exercised |
| B priorities | V01-B, L01, L04 | Final semantic review passed on supplied synthetic arguments |
| C over-questioning | V01-C, L01–L03 | Final review passed; live exhausted-budget recovery also exercised |
| D direct explanation | V01-D | Final review and actual direct-explanation turn passed |
| E uncertainty | V01-E, R01/R02/S01 | Final review passed; no invented page/text/reference |
| F recovery | V01-F and fresh-process file test | Final fixture review and genuine fresh-thread CLI recovery passed within stated versions |
| G edition differences | V01-G, S01 | Final source-limited review passed; no real two-edition book extraction test |
| H user correction | V01-H and audit rules | Final response/files/dependencies passed; archive-link caveat below |
| I no Obsidian | V01-I and stdlib Markdown helper | Final review passed; actual workflow used plain Markdown/CLI with no Obsidian calls |
| J data safety | V01-J and preservation/containment tests | Final refusal/files passed; does not prove whole-host absence of side effects |

30 inputs/rubrics are available in [evaluation instructions](../evals/README.md). Unit-test tally data are not model answers. Historic mother-project results were inspected separately: original16 had two failures/two targeted retests, later four were a separate run; those scores are never substituted for the three new forward runs.

## Preserved infrastructure events and artifact limitation

- First CLI launch failed from invalid UTF-8 stdin before model execution; it was retained, runner encoding corrected, then actual execution succeeded.
- Console capture/encoding and instrumentation recovery are recorded. Resulting files alone are not independent proof of every reconstructed event.
- Some verification queries returned exit1 because `rg` found no error-log filename; preceding read/verification output is distinguished from a failed save.
- The final independent reviewer hit an account usage limit before finishing. Review resumed against the same frozen answer/metadata/trace hashes; no answers were regenerated.
- One H `archive/book` snapshot retains an original-location relative concept link that cannot resolve from the archive directory. Its original bytes were preserved. Interpret references from the original note directory or inspect an isolated original-layout copy, preserving current notes. A layout-preserving archive also works. Current final-run notes and source paths resolve; archives are never current progress.

## Known limits

- Instruction compliance, Chapter Map judgment and mastery judgments depend on the host model; no deterministic guarantees.
- Source access and independent evidence may be unavailable; correct behavior is scoped uncertainty.
- The state helper creates initial files and reads saved state; subsequent session saving remains the agent's Markdown editing workflow. It does not schedule reviews or parse text into learning claims.
- Multi-file saving is not transactional. The session-first sequence permits recovery; failed initialization may leave a partial new directory, with explicit error reporting and no overwrite.
- Path checks reject links/junctions and traversal at operation time; they are not a security sandbox against a separate process changing paths concurrently.
- Tests executed locally use Windows/bundled Python and original synthetic source/reader data. Native macOS/Linux, native Python3.10, other hosts, real EPUB/PDF extraction across editions and longitudinal learning outcomes are unverified.
- Exact model/settings were unknown, and one forward context handles the30 cases per run. The reviewed real CLI trajectories cover specific versions/branches, not every final-version behavior.

## Before public release

- [x] Execute actual A–J/regression responses and independent source-grounded reviews; preserve failed earlier runs, input differences and hashes.
- [x] Exercise actual local co-reading, direct explanation, early stop/save and fresh-thread file recovery using synthetic reader data.
- [x] Verify local installed discovery; retain exact version/branch evidence and limits.
- [x] Owner authorized publication of the prepared MIT package with its contributor notice. No license is granted over readers' books/notes; publication authorization is not a separate legal certification of all possible rights.
- [x] Check this local alpha's source manifest and packaging scope for private paths, data and unintended file types. Repeat for each later release; no scan proves every possible disclosure absent.
- [x] Explicit owner authorization obtained for GitHub publication under VanillaArana. Public repository: https://github.com/VanillaArana/deep-reading. This publication covers only the curated package.
- [ ] Before presenting this as stable, complete a real-reader trial. Broader platform/file-format validation is future work.

## Suggested V0.2

Use observed behavior first: refine priorities/budget from real fatigue and understanding feedback; make fresh-chat recovery and partial-save repair easier; add focused regressions for confirmed errors. Consider a small optional review queue only after demonstrated demand. Plugin distribution, broader host support and larger registries are later adaptations, not V0.1 prerequisites.
