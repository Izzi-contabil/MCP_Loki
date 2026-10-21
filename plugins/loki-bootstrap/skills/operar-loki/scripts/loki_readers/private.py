"""Exclusive private outputs on POSIX and Windows; never read credential stores."""

import csv
import io
import json
import math
import os
import stat
import subprocess
from pathlib import Path
from typing import Any


class ReadError(ValueError):
    """Stable error code, never include document content in a diagnostic."""


PLUGIN_ROOT = Path(__file__).resolve().parents[4]


def private_directory(output: Path) -> Path:
    output = output.absolute()
    for parent in (output, *output.parents):
        if parent.is_symlink() or (
            os.name == "nt"
            and parent.exists()
            and getattr(parent.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
        ):
            raise ReadError("unsafe_output_symlink")
    output = output.resolve()
    plugin_root = PLUGIN_ROOT.resolve()
    if output == plugin_root or plugin_root in output.parents:
        raise ReadError("output_inside_plugin_cache")
    if output.exists():
        raise ReadError("output_exists")
    missing = [path for path in reversed(output.parents) if not path.exists()]
    for parent in missing:
        parent.mkdir(mode=0o700)
    output.mkdir(mode=0o700)
    if os.name == "nt":
        # chmod does not protect a Windows directory: replace inherited ACLs.
        result = subprocess.run(
            ["whoami", "/user", "/fo", "csv", "/nh"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
        sid = next(csv.reader(io.StringIO(result.stdout)))[1].strip()
        if not sid.startswith("S-1-") or any(c not in "S-0123456789" for c in sid):
            raise ReadError("private_acl_failed")
        subprocess.run(
            [
                "icacls",
                str(output),
                "/inheritance:r",
                "/grant:r",
                f"*{sid}:(OI)(CI)F",
                "*S-1-5-18:(OI)(CI)F",
            ],
            capture_output=True,
            check=True,
            timeout=15,
        )
    return output


def write_bytes(path: Path, content: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(content)


def write_json(path: Path, value: Any) -> None:
    write_bytes(
        path,
        (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8"),
    )


def strict_json(content: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ReadError("duplicate_json_key")
            result[key] = value
        return result

    def constant(_: str) -> None:
        raise ReadError("invalid_json_number")

    def finite(raw: str) -> float:
        value = float(raw)
        if not math.isfinite(value):
            raise ReadError("invalid_json_number")
        return value

    return json.loads(content, object_pairs_hook=pairs, parse_constant=constant, parse_float=finite)


def checked_bytes(source: Path, maximum: int, expected: str | None = None) -> bytes:
    if source.is_symlink() or not source.is_file():
        raise ReadError("source_not_regular_file")
    if source.stat().st_size > maximum:
        raise ReadError("size_limit")
    with source.open("rb") as stream:
        content = stream.read(maximum + 1)
    if not content or len(content) > maximum:
        raise ReadError("size_limit_or_empty")
    if expected is not None:
        import hashlib

        if hashlib.sha256(content).hexdigest() != expected:
            raise ReadError("source_hash_changed")
    return content
