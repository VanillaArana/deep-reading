# Behavioral evaluation

30 cases: 20 adapted from the original suite and 10 V0.1 acceptance cases A–J. The copyright book excerpt has been replaced with original synthetic text. No historic answers or reader records are distributed. Original B01's mandatory example test was relaxed to respect the later cumulative budget; this is a deliberate rubric change, not score equivalence.

Run from the repository root with Python 3.10+:

```sh
python evals/check.py prepare --output /your/private-test-run/inputs.json
python evals/check.py summarize --answers /your/private-test-run/answers.json --reviews /your/private-test-run/reviews.json
```

1. Use a fresh chat/test workspace. Provide the installed skill and exported inputs, not cases.json, rubrics, prior conclusions or intended answers. Confine writes to synthetic test directories; no real notes, books or account files.
2. Save actual responses as `{"answers":[{"id":"B01","answer":"actual response"}]}`. Do not fabricate answers from rubrics.
3. Only after answering, have a human or authorized independent reviewer inspect `cases.json` and the supplied sources. Save `{"reviews":[{"id":"B01","criteria":[true,true,true],"hard_fail":false,"evidence":"concrete answer excerpts and reasoning"}]}`. Every must needs a boolean; any hard failure fails the case. Word matching is not semantic grading.
4. Record date, model/reasoning setting (unknown when unavailable), skill/reference hashes, actual access conditions, inputs/answers, reviewer identity and failure repairs. Preserve original failures. Partial coverage is not all-pass.

V01-A/H/J require observing actual temporary-file outcomes as well as responses. V01-F's fixture tests recovery reasoning; the full F acceptance test additionally starts a new chat with only saved files after a preceding actual simulated session. Tool-level fresh-process recovery is automated separately and does not prove new-chat behavior. Check I without Obsidian, and G with each edition identified independently.

The script only exports inputs and tallies supplied semantic reviews. It does not execute or judge a model. Automated bookkeeping tests use invented responses to exercise counting; those are not model eval results. Never convert results into overall accuracy or learning-effect percentages. Current execution status is in [test report](../docs/test-report.md).

The recorded alpha preparation has three actual frozen forward batches, each followed by a separate model reviewer: 27/30, 28/30 and 30/30. Each batch shares one tested-agent context while treating scenarios and state files separately; it is not 30 independently fresh chats. Live CLI traces separately check genuine fresh-thread recovery. Exact model/reasoning settings were not reported. Raw traces and full reviews remain in the owner's private test workspace, outside this distribution.

V01-F's original rubric misnamed its planned endpoint; the locator was corrected against the fixture before grading. L02 initially requested a substantive closing takeaway with no passage or reader expression; after retaining that first failure, its input gained original synthetic passage/reader material. Keep input/rubric/skill hashes when comparing results: version labels alone do not establish identical test conditions.
