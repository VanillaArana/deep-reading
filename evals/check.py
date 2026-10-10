"""Adapted from the original prepare/answer/review/summarize bookkeeping.

Does not run a model, grade semantic correctness, or touch reader notes.
Python 3.10+, standard library only.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def cases():
    rows = load(ROOT / "cases.json")["cases"]
    ids = [row["id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate case ID")
    for row in rows:
        if not row["input"].strip() or not row["must"] or not row["hard_fail"]:
            raise ValueError("Incomplete case")
        for name in row["materials"]:
            path = (ROOT / name).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                raise ValueError("Fixture is missing or escapes eval directory")
    return rows


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def prepare(output):
    inputs = [{"id": c["id"], "input": c["input"], "materials": [
        {"path": n, "text": (ROOT / n).read_text(encoding="utf-8")} for n in c["materials"]
    ]} for c in cases()]
    write_new(output, {"protocol": "Use the skill. Answer before reading rubrics. Never edit real reader data.", "cases": inputs})
    return {"prepared": len(inputs), "rubrics_exported": False}


def summarize(answer_path, review_path):
    answers = load(answer_path)["answers"]
    reviews = load(review_path)["reviews"]
    am = {x["id"]: x for x in answers}
    rm = {x["id"]: x for x in reviews}
    rows = cases()
    ids = {c["id"] for c in rows}
    if len(am) != len(answers) or len(rm) != len(reviews):
        raise ValueError("Duplicate answers/reviews")
    if not set(am) <= ids or not set(rm) <= ids:
        raise ValueError("Unknown case ID")
    for answer in answers:
        if not isinstance(answer.get("answer"), str) or not answer["answer"].strip():
            raise ValueError("Blank or invalid answer")
    result = []
    for case in rows:
        cid = case["id"]
        status = "not_reviewed"
        if cid in am and cid in rm:
            review = rm[cid]
            criteria = review.get("criteria")
            hard = review.get("hard_fail")
            if not isinstance(criteria, list) or len(criteria) != len(case["must"]) or any(type(v) is not bool for v in criteria):
                raise ValueError("Incomplete or non-boolean criteria")
            if type(hard) is not bool or not isinstance(review.get("evidence"), str) or not review["evidence"].strip():
                raise ValueError("Review needs a boolean hard_fail and concrete evidence")
            status = "pass" if all(criteria) and not hard else "fail"
        result.append({"id": cid, "status": status})
    return {"answers": len(am), "reviewed": sum(x["status"] != "not_reviewed" for x in result),
            "passed": sum(x["status"] == "pass" for x in result),
            "failed": sum(x["status"] == "fail" for x in result),
            "not_reviewed": sum(x["status"] == "not_reviewed" for x in result), "cases": result,
            "scope": "This run and supplied semantic reviews only; not a general accuracy estimate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("--output", required=True)
    summ = commands.add_parser("summarize")
    summ.add_argument("--answers", required=True)
    summ.add_argument("--reviews", required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.output) if args.command == "prepare" else summarize(args.answers, args.reviews)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Eval bookkeeping failed: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
