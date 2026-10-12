#!/usr/bin/env python3
"""Build a deterministic ZIP from explicitly approved release files."""
from __future__ import annotations

import argparse
import hashlib
import io
import os
import stat
import sys
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile, ZipInfo

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PACKAGE_ROOT.parent / f"{PACKAGE_ROOT.name}.zip"
RELEASE_MANIFEST = "release-manifest.txt"
EXCLUDED_DIRECTORIES = {".git", ".pytest_cache", "__pycache__", ".venv", "venv"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _source_files(source_root: Path) -> tuple[Path, list[tuple[Path, Path]]]:
    root = Path(source_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Source root is not a directory: {root}")
    manifest_path = root / RELEASE_MANIFEST
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError(f"Required release manifest is missing or not a regular file: {manifest_path}")

    files: list[tuple[Path, Path]] = []
    seen: set[str] = set()
    for line_number, raw_line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), start=1):
        entry = raw_line.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry != raw_line or "\\" in entry or "\x00" in entry:
            raise ValueError(f"Invalid release-manifest entry on line {line_number}: {raw_line!r}")
        relative = PurePosixPath(entry)
        if (
            relative.is_absolute()
            or relative.as_posix() != entry
            or any(part in {"", ".", ".."} for part in relative.parts)
        ):
            raise ValueError(f"Unsafe release-manifest path on line {line_number}: {entry!r}")
        if entry == RELEASE_MANIFEST:
            raise ValueError(f"{RELEASE_MANIFEST} is included automatically and must not list itself")
        if entry in seen:
            raise ValueError(f"Duplicate release-manifest path on line {line_number}: {entry!r}")
        seen.add(entry)
        if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
            raise ValueError(f"Release manifest includes a generated directory: {entry!r}")
        if PurePosixPath(entry).suffix.lower() in EXCLUDED_SUFFIXES:
            raise ValueError(f"Release manifest includes a compiled file: {entry!r}")

        path = root
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise ValueError(f"Refusing to archive a symlink: {path}")
        try:
            resolved = path.resolve(strict=True)
        except FileNotFoundError as exc:
            raise ValueError(f"Release-manifest file does not exist: {entry!r}") from exc
        if not _is_within(resolved, root):
            raise ValueError(f"Release-manifest path resolves outside the source root: {entry!r}")
        if not path.is_file():
            raise ValueError(f"Release-manifest path is not a regular file: {entry!r}")
        files.append((path, relative))

    files.append((manifest_path, PurePosixPath(RELEASE_MANIFEST)))
    files.sort(key=lambda item: item[1].as_posix())
    return root, files


def build_archive_bytes(source_root: Path = PACKAGE_ROOT) -> tuple[bytes, int]:
    """Return normalized ZIP bytes and the number of included regular files.

    The output is byte-reproducible with the same Python and zlib implementation.
    Cross-version compression streams are not guaranteed to be identical.
    """
    root, files = _source_files(source_root)
    buffer = io.BytesIO()
    with ZipFile(
        buffer,
        mode="w",
        compression=ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        root_info = ZipInfo(f"{root.name}/", FIXED_TIMESTAMP)
        root_info.external_attr = (stat.S_IFDIR | 0o755) << 16
        root_info.compress_type = ZIP_DEFLATED
        archive.writestr(root_info, b"")
        for path, relative in files:
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"Unsafe archive path: {relative}")
            name = f"{root.name}/{relative.as_posix()}"
            info = ZipInfo(name, FIXED_TIMESTAMP)
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return buffer.getvalue(), len(files)


def write_archive(
    destination: Path,
    source_root: Path = PACKAGE_ROOT,
    *,
    verify_reproducible: bool = False,
) -> tuple[int, str]:
    """Atomically write a source ZIP, optionally comparing two fresh builds."""
    root = Path(source_root).expanduser().resolve()
    target = Path(destination).expanduser().resolve()
    if _is_within(target, root):
        raise ValueError("Archive output must be outside the source tree")

    payload, file_count = build_archive_bytes(root)
    if verify_reproducible:
        repeated, repeated_count = build_archive_bytes(root)
        if file_count != repeated_count or payload != repeated:
            raise RuntimeError("Two source archive builds were not byte-identical")

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

    with ZipFile(target, "r") as archive:
        corrupt_entry = archive.testzip()
        if corrupt_entry is not None:
            raise BadZipFile(f"Archive verification failed at {corrupt_entry}")
    return file_count, hashlib.sha256(payload).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Destination outside the source tree (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--verify-reproducible",
        action="store_true",
        help="Build twice and require identical ZIP bytes before writing",
    )
    args = parser.parse_args(argv)
    try:
        file_count, digest = write_archive(
            args.output,
            verify_reproducible=args.verify_reproducible,
        )
    except (BadZipFile, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {file_count} files to {args.output.expanduser().resolve()}")
    print(f"SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
