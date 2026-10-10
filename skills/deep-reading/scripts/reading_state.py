"""Optional Markdown bootstrap and read-only recovery; Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat

SKILL = Path(__file__).resolve().parents[1]
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))}


def is_junction(path: Path) -> bool:
    check = getattr(path, "is_junction", None)
    if callable(check):
        return check()
    if os.name != "nt":
        return False
    # Path.is_junction arrived in Python 3.12; Windows lstat tags exist in 3.8+.
    try:
        tag = getattr(path.lstat(), "st_reparse_tag", 0)
    except FileNotFoundError:
        return False
    return tag == stat.IO_REPARSE_TAG_MOUNT_POINT


def checked_root(value: str) -> Path:
    path = Path(os.path.abspath(value))
    for part in (path, *path.parents):
        if part.is_symlink() or is_junction(part):
            raise ValueError("Reader root must not traverse symlinks or junctions")
    root = path.resolve()
    forbidden = [SKILL]
    distribution = SKILL.parents[1]
    if (distribution / "docs/provenance.md").is_file():
        forbidden.append(distribution)
    if any(root == p or p in root.parents for p in forbidden):
        raise ValueError("Choose a reader directory outside the distributable package")
    return root


def book_path(root: Path, book_id: str) -> Path:
    if not ID.fullmatch(book_id) or len(book_id) > 64 or book_id in RESERVED:
        raise ValueError("book-id must be a non-reserved lowercase slug, maximum 64 characters")
    book = root / book_id
    checked_root(str(book))
    return book


def init_book(root: Path, book_id: str) -> dict:
    book = book_path(root, book_id)
    root.mkdir(parents=True, exist_ok=True)
    book.mkdir(exist_ok=False)  # Never reuse or overwrite an existing book directory.
    (book / "sessions").mkdir()
    (book / "book.md").write_text(
        (SKILL / "assets/templates/book.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    return {"created": str(book), "files": ["book.md"], "reading_recorded": False,
            "note": "Fill only verified identity and actual reader feedback; no session started."}


def read_checked(book: Path, relative: str) -> str:
    path = book / relative
    # Reject traversal, symlinks and directory junctions before accessing text.
    checked_root(str(path))
    if not path.resolve().is_relative_to(book.resolve()):
        raise ValueError("A state link escaped its book directory")
    return path.read_text(encoding="utf-8-sig")


def resume_book(root: Path, book_id: str) -> dict:
    book = book_path(root, book_id)
    index = read_checked(book, "book.md")
    records = {}
    for relative in dict.fromkeys(re.findall(r"\[[^\]]*\]\((sessions/[^)]+\.md)\)", index)):
        records[relative] = read_checked(book, relative)
    errors = read_checked(book, "AI-ERROR-LOG.md") if (book / "AI-ERROR-LOG.md").exists() else None
    return {"book_id": book_id, "canonical_index": index, "linked_sessions": records,
            "error_log": errors, "warning": None if records else "No linked actual session; do not infer progress.",
            "scope": "File recovery only; no interpretation, source verification or mastery inference."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "resume"])
    parser.add_argument("--root", required=True, help="Reader-owned Markdown library, outside the package")
    parser.add_argument("--book-id", required=True)
    args = parser.parse_args()
    try:
        root = checked_root(args.root)
        result = (init_book if args.command == "init" else resume_book)(root, args.book_id)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"State operation failed: {exc}\nCheck for partial initialization before retrying; existing files were not overwritten.\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
