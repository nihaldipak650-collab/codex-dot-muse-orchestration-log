"""Verify current-main public file bytes; --update refreshes the manifest using Git."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import subprocess
import sys

MANIFEST = "PUBLIC_FILE_HASHES.sha256"


def safe_path(root, name):
    relative = PurePosixPath(name)
    if not name or "\\" in name or ":" in name or relative.is_absolute() or ".." in relative.parts:
        raise ValueError("unsafe manifest path")
    path = root.joinpath(*relative.parts)
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        raise ValueError("path escapes repository")
    if name == MANIFEST or ".git" in relative.parts:
        raise ValueError("reserved manifest path")
    return path


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def update(root):
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, check=True, capture_output=True,
    )
    names = sorted(set(result.stdout.decode("utf-8").rstrip("\0").split("\0")))
    lines = []
    for name in names:
        if not name or name == MANIFEST:
            continue
        path = safe_path(root, name)
        lines.append(f"{digest(path)}  {name}\n")
    with (root / MANIFEST).open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("".join(lines))
    print(f"Updated {len(lines)} file hashes. Review the file list before committing.")


def verify(root):
    lines = (root / MANIFEST).read_text(encoding="utf-8").splitlines()
    seen, errors = set(), []
    for number, line in enumerate(lines, 1):
        try:
            expected, name = line.split("  ", 1)
            if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
                raise ValueError("invalid SHA-256")
            if name in seen:
                raise ValueError("duplicate path")
            seen.add(name)
            if digest(safe_path(root, name)) != expected:
                raise ValueError("hash mismatch")
        except (ValueError, OSError) as error:
            errors.append(f"Line {number}: {error}")
    if not lines:
        errors.append("Empty manifest")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(seen)} listed files match. This does not verify research claims or unlisted files.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="write hashes of Git-listed public files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        if args.update:
            update(root)
        return verify(root)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
