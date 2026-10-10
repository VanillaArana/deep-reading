"""Deterministic packaging, state and evaluation tests; no model execution."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/deep-reading"
HELPER = SKILL / "scripts/reading_state.py"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


state = module("reading_state", HELPER)
evals = module("eval_check", ROOT / "evals/check.py")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="reading-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "读者 library"
        self.book = self.root / "sample-book"

    def init(self):
        return state.init_book(state.checked_root(str(self.root)), "sample-book")

    def test_initialization_records_no_reading(self):
        result = self.init()
        self.assertFalse(result["reading_recorded"])
        self.assertEqual(list(self.book.glob("*.md")), [self.book / "book.md"])
        self.assertEqual(list((self.book / "sessions").iterdir()), [])

    def test_duplicate_initialization_preserves_all_content(self):
        self.init()
        index = self.book / "book.md"
        index.write_text("KEEP_ME\n", encoding="utf-8")
        old = digest(index)
        with self.assertRaises(FileExistsError):
            self.init()
        self.assertEqual(digest(index), old)

    def test_existing_unrelated_notes_untouched(self):
        self.root.mkdir(parents=True)
        note = self.root / "existing-note.md"
        note.write_text("unrelated", encoding="utf-8")
        old = digest(note)
        self.init()
        self.assertEqual(digest(note), old)

    def test_invalid_ids_do_not_escape(self):
        for book_id in ("../escape", "..", "UPPER", "x/y", "a--b", "con", "com1", "x" * 65):
            with self.subTest(book_id=book_id), self.assertRaises(ValueError):
                state.init_book(self.root, book_id)
        self.assertFalse(self.root.exists())

    def test_reader_data_cannot_be_initialized_in_package(self):
        for root in (ROOT, SKILL, SKILL / "reader-data"):
            with self.assertRaises(ValueError):
                state.checked_root(str(root))

    def test_missing_index_does_not_create_state(self):
        with self.assertRaises(FileNotFoundError):
            state.resume_book(self.root, "sample-book")
        self.assertFalse(self.root.exists())

    def test_relocated_install_works_with_own_reader_library(self):
        installed = Path(self.temp.name) / "another workspace/.agents/skills/deep-reading"
        shutil.copytree(SKILL, installed)
        cmd = [sys.executable, "-X", "utf8", "-B", str(installed / "scripts/reading_state.py")]
        args = ["--root", str(self.root), "--book-id", "sample-book"]
        created = subprocess.run(cmd + ["init"] + args, capture_output=True, encoding="utf-8", check=True)
        self.assertFalse(json.loads(created.stdout)["reading_recorded"])
        restored = subprocess.run(cmd + ["resume"] + args, capture_output=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(restored.stdout)["canonical_index"], (self.book / "book.md").read_text(encoding="utf-8"))

    def test_fresh_process_recovery_and_no_writes(self):
        # A subprocess initializes; files emulate actual saved notes; another
        # subprocess recovers without shared conversation or in-process state.
        base = [sys.executable, "-X", "utf8", "-B", str(HELPER)]
        args = ["--root", str(self.root), "--book-id", "sample-book"]
        first = subprocess.run(base + ["init"] + args, check=True, capture_output=True, encoding="utf-8")
        self.assertFalse(json.loads(first.stdout)["reading_recorded"])
        fixture = ROOT / "evals/fixtures/recovery"
        (self.book / "book.md").write_bytes((fixture / "book.md").read_bytes())
        (self.book / "sessions/S001.md").write_bytes((fixture / "sessions/S001.md").read_bytes())
        (self.book / "AI-ERROR-LOG.md").write_text("Actual synthetic correction: attempted is not effective.", encoding="utf-8")
        # An archive with conflicting advanced progress must not be loaded.
        (self.book / "archive").mkdir()
        (self.book / "archive/book.md").write_text("ALL MASTERED", encoding="utf-8")
        before = {str(p): digest(p) for p in self.book.rglob("*.md")}
        recovered = subprocess.run(base + ["resume"] + args, check=True, capture_output=True, encoding="utf-8")
        result = json.loads(recovered.stdout)
        self.assertEqual(result["canonical_index"], (fixture / "book.md").read_text(encoding="utf-8"))
        self.assertEqual(result["linked_sessions"]["sessions/S001.md"], (fixture / "sessions/S001.md").read_text(encoding="utf-8"))
        self.assertIn("attempted is not effective", result["error_log"])
        self.assertNotIn("ALL MASTERED", json.dumps(result))
        self.assertEqual(before, {str(p): digest(p) for p in self.book.rglob("*.md")})

    def test_recovery_without_session_does_not_infer_progress(self):
        self.init()
        result = state.resume_book(self.root, "sample-book")
        self.assertEqual(result["linked_sessions"], {})
        self.assertTrue(result["warning"])

    def test_missing_linked_record_is_error(self):
        self.init()
        (self.book / "book.md").write_text("[S009](sessions/S009.md)", encoding="utf-8")
        with self.assertRaises(FileNotFoundError):
            state.resume_book(self.root, "sample-book")

    def test_traversal_in_link_is_rejected(self):
        self.init()
        outside = self.root / "secret.md"
        outside.write_text("outside", encoding="utf-8")
        (self.book / "book.md").write_text("[escape](sessions/../../secret.md)", encoding="utf-8")
        with self.assertRaises(ValueError):
            state.resume_book(self.root, "sample-book")

    def test_symlink_is_rejected_when_supported(self):
        self.init()
        outside = self.root / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        link = self.book / "sessions/link.md"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("OS does not permit symlink creation")
        (self.book / "book.md").write_text("[link](sessions/link.md)", encoding="utf-8")
        with self.assertRaises(ValueError):
            state.resume_book(self.root, "sample-book")

    @unittest.skipUnless(os.name == "nt", "Windows directory junction test")
    def test_windows_junction_is_rejected(self):
        self.init()
        target = self.root / "other-book"
        target.mkdir()
        (target / "record.md").write_text("outside book", encoding="utf-8")
        link = self.book / "sessions/redirect"
        # Only creates a junction under this test's isolated temporary root.
        script = "New-Item -ItemType Junction -Path $env:READING_TEST_LINK -Target $env:READING_TEST_TARGET | Out-Null"
        env = dict(os.environ, READING_TEST_LINK=str(link), READING_TEST_TARGET=str(target))
        result = subprocess.run(["powershell", "-NoProfile", "-Command", script], env=env, capture_output=True)
        if result.returncode != 0 or not getattr(link, "is_junction", lambda: False)():
            self.skipTest("OS could not create a test directory junction")
        (self.book / "book.md").write_text("[redirect](sessions/redirect/record.md)", encoding="utf-8")
        with self.assertRaises(ValueError):
            state.resume_book(self.root, "sample-book")
        self.assertTrue((target / "record.md").exists())

    @unittest.skipUnless(os.name == "nt", "Windows older-path-API compatibility test")
    def test_windows_junction_rejected_without_path_junction_api(self):
        self.init()
        target = self.root / "other-book"
        target.mkdir()
        (target / "record.md").write_text("outside book", encoding="utf-8")
        link = self.book / "sessions/redirect"
        script = "New-Item -ItemType Junction -Path $env:READING_TEST_LINK -Target $env:READING_TEST_TARGET | Out-Null"
        env = dict(os.environ, READING_TEST_LINK=str(link), READING_TEST_TARGET=str(target))
        result = subprocess.run(["powershell", "-NoProfile", "-Command", script], env=env, capture_output=True)
        if result.returncode != 0 or not state.is_junction(link):
            self.skipTest("OS could not create a test directory junction")
        (self.book / "book.md").write_text("[redirect](sessions/redirect/record.md)", encoding="utf-8")
        # Exercise the older API branch against a real junction, not fake tags.
        with mock.patch.object(Path, "is_junction", None, create=True):
            with self.assertRaises(ValueError):
                state.resume_book(self.root, "sample-book")
        self.assertTrue((target / "record.md").exists())


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.answers = self.root / "answers.json"
        self.reviews = self.root / "reviews.json"

    def write(self, answers, reviews):
        self.answers.write_text(json.dumps({"answers": answers}), encoding="utf-8")
        self.reviews.write_text(json.dumps({"reviews": reviews}), encoding="utf-8")

    def test_export_has_no_rubrics_or_private_material(self):
        target = self.root / "inputs.json"
        result = evals.prepare(target)
        self.assertEqual(result["prepared"], 30)
        inputs = json.loads(target.read_text(encoding="utf-8"))["cases"]
        self.assertTrue(all(set(c) == {"id", "input", "materials"} for c in inputs))
        self.assertTrue(all(set(m) == {"path", "text"} for c in inputs for m in c["materials"]))
        with self.assertRaises(FileExistsError):
            evals.prepare(target)

    def test_unanswered_cases_are_not_passes(self):
        self.write([], [])
        result = evals.summarize(self.answers, self.reviews)
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["not_reviewed"], 30)

    def test_hard_failure_overrides_all_criteria(self):
        self.write([{"id": "B01", "answer": "Synthetic bookkeeping answer"}],
                   [{"id": "B01", "criteria": [True] * 3, "hard_fail": True, "evidence": "Synthetic bookkeeping review"}])
        result = evals.summarize(self.answers, self.reviews)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["not_reviewed"], 29)

    def test_partial_and_pass_are_tallied_separately(self):
        self.write([{"id": "B01", "answer": "synthetic"}, {"id": "B02", "answer": "synthetic"}],
                   [{"id": "B01", "criteria": [True] * 3, "hard_fail": False, "evidence": "synthetic tally test"}])
        result = evals.summarize(self.answers, self.reviews)
        self.assertEqual((result["passed"], result["reviewed"], result["not_reviewed"]), (1, 1, 29))

    def test_invalid_reviews_are_rejected(self):
        for criteria, hard in (([True], False), ([1, 1, 1], False), ([True] * 3, "false")):
            self.write([{"id": "B01", "answer": "synthetic"}],
                       [{"id": "B01", "criteria": criteria, "hard_fail": hard, "evidence": "synthetic"}])
            with self.assertRaises(ValueError):
                evals.summarize(self.answers, self.reviews)

    def test_duplicate_unknown_and_empty_answers_rejected(self):
        for answers in ([{"id": "B01", "answer": "x"}] * 2,
                        [{"id": "unknown", "answer": "x"}], [{"id": "B01", "answer": " "}]):
            self.write(answers, [])
            with self.assertRaises(ValueError):
                evals.summarize(self.answers, self.reviews)


class PackageTests(unittest.TestCase):
    def test_local_markdown_links_exist_and_stay_in_package(self):
        for doc in ROOT.rglob("*.md"):
            text = re.sub(r"```.*?```", "", doc.read_text(encoding="utf-8"), flags=re.S)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                path = (doc.parent / target.split("#")[0]).resolve()
                self.assertTrue(path.is_relative_to(ROOT), (doc, target))
                self.assertTrue(path.is_file(), (doc, target))

    def test_no_books_links_or_personal_absolute_paths(self):
        blocked = {".pdf", ".epub", ".mobi", ".azw3", ".lnk", ".zip", ".env"}
        for path in ROOT.rglob("*"):
            self.assertFalse(path.is_symlink() or getattr(path, "is_junction", lambda: False)(), path)
            self.assertNotIn(path.suffix.lower(), blocked, path)
            if path.suffix in {".md", ".json", ".yaml", ".py"}:
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"\b[A-Za-z]:[\\/][\w\u4e00-\u9fff]", text), path)
                self.assertIsNone(re.search(r"sk-[A-Za-z0-9]{20,}", text), path)

    def test_acceptance_cases_and_legacy_ids_present(self):
        ids = {c["id"] for c in evals.cases()}
        self.assertTrue({"V01-" + letter for letter in "ABCDEFGHIJ"} <= ids)
        self.assertTrue({"B01", "B02", "S01", "S02", "L01", "L02", "L03", "L04"} <= ids)
        self.assertEqual(len(ids), 30)


if __name__ == "__main__":
    unittest.main(verbosity=2)
