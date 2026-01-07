"""
Usage examples:
    python scripts/clean_math_code.py content/posts --ext .md --ext .mdx
    python scripts/clean_math_code.py content/posts/AI/PPO.md --in-place --backup .bak
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Sequence, Tuple

DEFAULT_EXTS = {".md", ".markdown", ".mdx"}

INLINE_MATH_PATTERN = re.compile(
    r"\{\{<[ \t]*math[ \t]*>\}\}[ \t]*(\$[^\r\n]*?\$)[ \t]*\{\{<[ \t]*/[ \t]*math[ \t]*>\}\}"
)


def normalize_exts(exts: Sequence[str] | None) -> set[str]:
    if not exts:
        return set(DEFAULT_EXTS)
    normalized = set()
    for ext in exts:
        ext = ext.strip()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        normalized.add(ext.lower())
    return normalized


def collect_files(paths: Sequence[str], allowed_exts: set[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()

    def add_file(p: Path) -> None:
        if p.is_file() and (not allowed_exts or p.suffix.lower() in allowed_exts):
            if p not in seen:
                seen.add(p)
                files.append(p)

    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for item in path.rglob("*"):
                add_file(item)
        else:
            add_file(path)
    return files


def transform_text(text: str) -> Tuple[str, int]:
    return INLINE_MATH_PATTERN.subn(r"\1", text)


def read_text_preserve_newlines(path: Path) -> str:
    with path.open(encoding="utf-8", errors="surrogateescape", newline="") as f:
        return f.read()


def write_atomic(path: Path, content: str) -> None:
    tmp_fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8", newline="") as tmp_file:
            tmp_file.write(content)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            try:
                os.remove(tmp_name)
            except OSError:
                pass


def backup_file(path: Path, extension: str) -> Path:
    backup_path = path.with_name(path.name + extension)
    shutil.copy2(path, backup_path)
    return backup_path


def process_file(path: Path, in_place: bool, backup_ext: str | None) -> int:
    original = read_text_preserve_newlines(path)
    transformed, count = transform_text(original)
    if count and in_place:
        if backup_ext:
            backup_file(path, backup_ext)
        write_atomic(path, transformed)
    return count


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove Hugo math shortcodes wrapping single-line inline math."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Input files or directories to process.",
    )
    parser.add_argument(
        "--ext",
        action="append",
        dest="exts",
        help="File extension to include (e.g. .md). Can be provided multiple times.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Rewrite files in place (default is dry-run).",
    )
    parser.add_argument(
        "--backup",
        metavar="EXT",
        help="Backup extension to use before modifying files (e.g. .bak).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    exts = normalize_exts(args.exts)
    files = collect_files(args.paths, exts)

    if not files:
        print("No matching files found.", file=sys.stderr)
        return 1

    total_files_changed = 0
    total_replacements = 0

    for file_path in files:
        count = process_file(file_path, args.in_place, args.backup)
        if count:
            total_files_changed += 1
            total_replacements += count
            action = "updated" if args.in_place else "would update"
            print(f"{file_path} - {action} with {count} replacement(s)")

    summary_action = "Updated" if args.in_place else "Dry-run:"
    print(
        f"{summary_action} {total_files_changed} file(s); "
        f"{total_replacements} replacement(s) in total."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
