"""Validate and copy a built wheel for local Loki review; never deploy or change auth."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import stat
import subprocess
import tempfile
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "mcp_loki_updates"
VERSION = "0.2.1"
WHEEL_NAME = f"{PACKAGE}-{VERSION}-py3-none-any.whl"
INFO = f"{PACKAGE}-{VERSION}.dist-info/"
MAX_WHEEL_BYTES = 8 * 1024 * 1024
MAX_MEMBER_BYTES = 1024 * 1024


class ReleaseRefused(ValueError):
    """A review artifact failed an explicit release check."""


def _linked(path: Path) -> bool:
    if not path.exists() and not path.is_symlink():
        return False
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def _allowed(name: str) -> bool:
    path = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or path.is_absolute()
        or any(part in {"", ".", ".."} or ":" in part for part in name.split("/"))
    ):
        return False
    if name.startswith(PACKAGE + "/"):
        return path.suffix in {".py", ".json", ".md"} or path.name == "py.typed"
    return name in {INFO + leaf for leaf in ("METADATA", "WHEEL", "RECORD", "top_level.txt")}


def _source_files() -> dict[str, bytes]:
    package = ROOT / "src" / PACKAGE
    files: dict[str, bytes] = {}
    for path in package.rglob("*"):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if _linked(path):
            raise ReleaseRefused("source_links_not_allowed")
        if path.is_file():
            name = path.relative_to(ROOT / "src").as_posix()
            if not _allowed(name):
                raise ReleaseRefused("source_member_not_allowed")
            files[name] = path.read_bytes()
    if not files:
        raise ReleaseRefused("source_package_missing")
    return files


def validate_wheel(wheel: Path) -> tuple[bytes, dict[str, str]]:
    """Read only allowlisted bytes; validate data using the trusted source provider."""
    from mcp_loki_updates import InstructionsProvider, InstructionsUnavailable

    if wheel.name != WHEEL_NAME or _linked(wheel) or not wheel.is_file():
        raise ReleaseRefused("wheel_name_or_path_invalid")
    if wheel.stat().st_size > MAX_WHEEL_BYTES:
        raise ReleaseRefused("wheel_size_exceeded")
    contents = wheel.read_bytes()
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise ReleaseRefused("duplicate_wheel_member")
            if any(stat.S_ISLNK(info.external_attr >> 16) for info in infos):
                raise ReleaseRefused("wheel_links_not_allowed")
            if not all(_allowed(name) for name in names):
                raise ReleaseRefused("wheel_member_not_allowed")
            if (
                any(info.file_size > MAX_MEMBER_BYTES for info in infos)
                or sum(info.file_size for info in infos) > MAX_WHEEL_BYTES
            ):
                raise ReleaseRefused("wheel_size_exceeded")
            required = {INFO + leaf for leaf in ("METADATA", "WHEEL", "RECORD")}
            if not required.issubset(names):
                raise ReleaseRefused("wheel_metadata_missing")
            files = {name: archive.read(name) for name in names}
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise ReleaseRefused("wheel_archive_invalid") from exc
    metadata = BytesParser().parsebytes(files[INFO + "METADATA"])
    if metadata.get_all("Name") != ["mcp-loki-updates"] or metadata.get_all("Version") != [VERSION]:
        raise ReleaseRefused("wheel_identity_invalid")
    if metadata.get_all("Requires-Dist") is not None or metadata.get_all("Requires-Python") != [
        ">=3.11"
    ]:
        raise ReleaseRefused("wheel_dependency_contract_invalid")
    wheel_metadata = BytesParser().parsebytes(files[INFO + "WHEEL"])
    if (
        wheel_metadata.get_all("Tag") != ["py3-none-any"]
        or wheel_metadata.get("Root-Is-Purelib") != "true"
    ):
        raise ReleaseRefused("wheel_tag_invalid")
    try:
        rows = list(csv.reader(io.StringIO(files[INFO + "RECORD"].decode("utf-8")), strict=True))
        if any(len(row) != 3 for row in rows):
            raise ReleaseRefused("wheel_record_invalid")
        records = {row[0]: (row[1], row[2]) for row in rows}
        if len(records) != len(rows) or records.keys() != files.keys():
            raise ReleaseRefused("wheel_record_invalid")
        for name, data in files.items():
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
            expected = ("", "") if name == INFO + "RECORD" else ("sha256=" + digest, str(len(data)))
            if records[name] != expected:
                raise ReleaseRefused("wheel_record_invalid")
    except (UnicodeError, csv.Error) as exc:
        raise ReleaseRefused("wheel_record_invalid") from exc
    source = _source_files()
    package_files = {name: data for name, data in files.items() if name.startswith(PACKAGE + "/")}
    if package_files != source:
        raise ReleaseRefused("wheel_source_mismatch")
    with tempfile.TemporaryDirectory(prefix="mcp-loki-release-") as temporary:
        data_root = Path(temporary)
        for name, data in package_files.items():
            prefix = PACKAGE + "/data/"
            if name.startswith(prefix):
                target = data_root / name.removeprefix(prefix)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        try:
            healthy = InstructionsProvider(data_root).health()["status"] == "ok"
        except InstructionsUnavailable as exc:
            raise ReleaseRefused("provider_data_invalid") from exc
        if not healthy:
            raise ReleaseRefused("provider_data_invalid")
    return contents, {
        name: hashlib.sha256(data).hexdigest() for name, data in sorted(package_files.items())
    }


def _git(*arguments: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *arguments], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def provenance(contents: bytes, hashes: dict[str, str]) -> dict[str, Any]:
    status = _git("status", "--porcelain=v1", "--untracked-files=normal")
    if status is None:
        raise ReleaseRefused("source_git_repository_required")
    head = _git("rev-parse", "--verify", "HEAD")
    return {
        "schema_version": "mcp-loki.release-provenance/1",
        "package": "mcp-loki-updates",
        "version": VERSION,
        "wheel_sha256": hashlib.sha256(contents).hexdigest(),
        "provider_validation": "ok",
        "source": {
            "repository": "MCP_Loki",
            "head": head,
            "tree": _git("rev-parse", "HEAD^{tree}") if head else None,
            "has_head": head is not None,
            "dirty": bool(status) or head is None,
            "package_sha256": hashlib.sha256(
                json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest(),
            "package_files": hashes,
        },
        "deployment_performed": False,
        "dependency_lock_updated": False,
        "authentication_changed": False,
    }


def _validate_existing_provenance(path: Path, expected: dict[str, Any]) -> None:
    """Validate artifact invariants while preserving the original Git observation."""
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise ReleaseRefused("existing_provenance_invalid") from exc
    if not isinstance(existing, dict) or existing.keys() != expected.keys():
        raise ReleaseRefused("existing_provenance_invalid")
    for field in (
        "schema_version",
        "package",
        "version",
        "wheel_sha256",
        "provider_validation",
    ):
        if existing[field] != expected[field]:
            raise ReleaseRefused("existing_provenance_invalid")
    for field in ("deployment_performed", "dependency_lock_updated", "authentication_changed"):
        if existing[field] is not False:
            raise ReleaseRefused("existing_provenance_invalid")
    source = existing["source"]
    expected_source = expected["source"]
    if not isinstance(source, dict) or source.keys() != expected_source.keys():
        raise ReleaseRefused("existing_provenance_invalid")
    for field in ("repository", "package_sha256", "package_files"):
        if source[field] != expected_source[field]:
            raise ReleaseRefused("existing_provenance_invalid")
    if type(source["dirty"]) is not bool or type(source["has_head"]) is not bool:
        raise ReleaseRefused("existing_provenance_invalid")
    if source["has_head"]:
        if any(
            not isinstance(source[field], str)
            or re.fullmatch(r"[0-9a-f]{40}", source[field]) is None
            for field in ("head", "tree")
        ):
            raise ReleaseRefused("existing_provenance_invalid")
    elif source["head"] is not None or source["tree"] is not None or source["dirty"] is not True:
        raise ReleaseRefused("existing_provenance_invalid")


def promote(wheel: Path, loki_path: Path) -> dict[str, str]:
    contents, hashes = validate_wheel(wheel.absolute())
    proof = provenance(contents, hashes)
    root = loki_path.absolute()
    if (
        _linked(root)
        or not (root / "src" / "loki").is_dir()
        or not (root / "pyproject.toml").is_file()
    ):
        raise ReleaseRefused("loki_checkout_required")
    vendor = root / "vendor"
    if _linked(vendor):
        raise ReleaseRefused("vendor_links_not_allowed")
    vendor.mkdir(exist_ok=True)
    target = vendor / WHEEL_NAME
    proof_path = target.with_suffix(".provenance.json")
    if _linked(target) or _linked(proof_path):
        raise ReleaseRefused("release_links_not_allowed")
    if proof_path.exists():
        _validate_existing_provenance(proof_path, proof)
    if target.exists():
        if target.read_bytes() != contents:
            raise ReleaseRefused("existing_release_differs")
    else:
        with target.open("xb") as output:
            output.write(contents)
    # An idempotent retry preserves the first provenance for these exact bytes.
    if not proof_path.exists():
        with proof_path.open("x", encoding="utf-8", newline="\n") as output:
            json.dump(proof, output, ensure_ascii=False, indent=2)
            output.write("\n")
    return {"wheel": str(target), "provenance": str(proof_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wheel", required=True, type=Path, help="Existing wheel built by uv build"
    )
    parser.add_argument(
        "--loki-path", required=True, type=Path, help="Explicit target Loki checkout"
    )
    arguments = parser.parse_args()
    try:
        result = promote(arguments.wheel, arguments.loki_path)
    except (ReleaseRefused, OSError, ValueError) as exc:
        parser.exit(1, f"Promotion refused ({type(exc).__name__}): {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Review wheel/provenance, then pin the local dependency and update Loki's uv.lock.")
    print("No deployment, authentication change, or dependency lock update was performed.")


if __name__ == "__main__":
    main()
