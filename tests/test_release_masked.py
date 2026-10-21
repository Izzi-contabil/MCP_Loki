"""Synthetic release fixtures; no credentials, network, or deployment."""

from __future__ import annotations

import base64
import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "promote.py"


def release_module() -> Any:
    assert SCRIPT.is_file(), "release promotion script must exist"
    spec = importlib.util.spec_from_file_location("release_promote", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def wheel_masked(tmp_path: Path, extra: dict[str, bytes] | None = None) -> Path:
    source = ROOT / "src" / "mcp_loki_updates"
    assert source.is_dir(), "provider package must exist before release validation"
    members = {
        path.relative_to(ROOT / "src").as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }
    info = "mcp_loki_updates-0.1.1.dist-info/"
    members[info + "METADATA"] = (
        b"Metadata-Version: 2.3\nName: mcp-loki-updates\nVersion: 0.1.1\nRequires-Python: >=3.11\n"
    )
    members[info + "WHEEL"] = b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    members.update(extra or {})
    if info + "RECORD" not in members:
        record = io.StringIO(newline="")
        writer = csv.writer(record, lineterminator="\n")
        for name, data in sorted(members.items()):
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
            writer.writerow((name, "sha256=" + digest, len(data)))
        writer.writerow((info + "RECORD", "", ""))
        members[info + "RECORD"] = record.getvalue().encode()
    wheel = tmp_path / "mcp_loki_updates-0.1.1-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return wheel


def loki_masked(tmp_path: Path) -> Path:
    root = tmp_path / "loki-masked"
    (root / "src" / "loki").mkdir(parents=True)
    (root / "pyproject.toml").write_text('[project]\nname = "project-loki"\n', encoding="utf-8")
    return root


def test_promotion_copies_exact_bytes_and_records_honest_source(tmp_path: Path) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path)
    loki = loki_masked(tmp_path)
    result = module.promote(wheel, loki)
    target = loki / "vendor" / wheel.name
    assert target.read_bytes() == wheel.read_bytes()
    proof = json.loads(target.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    assert proof["wheel_sha256"] == hashlib.sha256(wheel.read_bytes()).hexdigest()
    assert proof["provider_validation"] == "ok"
    assert isinstance(proof["source"]["dirty"], bool)
    assert "head" in proof["source"] and "tree" in proof["source"]
    assert proof["source"]["package_sha256"]
    assert proof["deployment_performed"] is False
    assert result["wheel"] == str(target)
    assert module.promote(wheel, loki)["wheel"] == str(target)


@pytest.mark.parametrize("name", ["../escape.py", "/escape.py", "evil.py", "mcp_loki_updates/.env"])
def test_refuses_members_outside_distribution_allowlist(tmp_path: Path, name: str) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path, {name: b"synthetic"})
    loki = loki_masked(tmp_path)
    with pytest.raises(module.ReleaseRefused, match="wheel_member_not_allowed"):
        module.promote(wheel, loki)
    assert not (loki / "vendor").exists()


def test_refuses_wheel_different_from_source_and_preserves_existing(tmp_path: Path) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path, {"mcp_loki_updates/__init__.py": b"# altered fixture\n"})
    loki = loki_masked(tmp_path)
    with pytest.raises(module.ReleaseRefused, match="wheel_source_mismatch"):
        module.promote(wheel, loki)
    wheel = wheel_masked(tmp_path)
    vendor = loki / "vendor"
    vendor.mkdir()
    target = vendor / wheel.name
    target.write_bytes(b"existing-release-masked")
    with pytest.raises(module.ReleaseRefused, match="existing_release_differs"):
        module.promote(wheel, loki)
    assert target.read_bytes() == b"existing-release-masked"


def test_refuses_duplicate_zip_member_and_symlink(tmp_path: Path) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path)
    with zipfile.ZipFile(wheel, "a") as archive:
        with pytest.warns(UserWarning, match="Duplicate name"):
            archive.writestr("mcp_loki_updates/__init__.py", b"duplicate")
    with pytest.raises(module.ReleaseRefused, match="duplicate_wheel_member"):
        module.promote(wheel, loki_masked(tmp_path))
    wheel = wheel_masked(tmp_path)
    with zipfile.ZipFile(wheel, "a") as archive:
        member = zipfile.ZipInfo("mcp_loki_updates/link.py")
        member.create_system = 3
        member.external_attr = 0o120777 << 16
        archive.writestr(member, b"elsewhere")
    with pytest.raises(module.ReleaseRefused, match="wheel_links_not_allowed"):
        module.promote(wheel, tmp_path / "unused")


def test_cli_requires_explicit_destination_and_existing_wheel() -> None:
    release_module()
    command = subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False
    )
    assert command.returncode == 2
    assert "--loki-path" in command.stderr and "--wheel" in command.stderr


@pytest.mark.parametrize(
    ("member", "contents", "reason"),
    [
        (
            "METADATA",
            b"Metadata-Version: 2.3\nName: other-package\nVersion: 0.1.1\n",
            "wheel_identity_invalid",
        ),
        (
            "WHEEL",
            b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: cp311-win_amd64\n",
            "wheel_tag_invalid",
        ),
    ],
)
def test_refuses_incorrect_distribution_identity(
    tmp_path: Path, member: str, contents: bytes, reason: str
) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path, {"mcp_loki_updates-0.1.1.dist-info/" + member: contents})
    with pytest.raises(module.ReleaseRefused, match=reason):
        module.promote(wheel, loki_masked(tmp_path))


def test_provider_validates_data_even_when_wheel_matches_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = release_module()
    source = module._source_files()
    member = "mcp_loki_updates/data/domains/geral.md"
    source[member] = b"# Modified synthetic content with stale metadata\n"
    monkeypatch.setattr(module, "_source_files", lambda: source)
    wheel = wheel_masked(tmp_path, {member: source[member]})
    loki = loki_masked(tmp_path)
    with pytest.raises(module.ReleaseRefused, match="provider_data_invalid"):
        module.promote(wheel, loki)
    assert not (loki / "vendor").exists()


def test_refuses_record_with_unlisted_or_forged_content(tmp_path: Path) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path, {"mcp_loki_updates-0.1.1.dist-info/RECORD": b"../other,,\n"})
    with pytest.raises(module.ReleaseRefused, match="wheel_record_invalid"):
        module.promote(wheel, loki_masked(tmp_path))


@pytest.mark.parametrize(
    "requirements",
    [
        b"Requires-Python: >=3.11\nRequires-Dist: synthetic-unreviewed-package\n",
        b"Requires-Python: >=3.8\n",
        b"Requires-Python: >=3.14\n",
        b"",
    ],
)
def test_refuses_unreviewed_dependency_or_python_contract(
    tmp_path: Path, requirements: bytes
) -> None:
    module = release_module()
    metadata = b"Metadata-Version: 2.3\nName: mcp-loki-updates\nVersion: 0.1.1\n" + requirements
    wheel = wheel_masked(tmp_path, {"mcp_loki_updates-0.1.1.dist-info/METADATA": metadata})
    with pytest.raises(module.ReleaseRefused, match="wheel_dependency_contract_invalid"):
        module.promote(wheel, loki_masked(tmp_path))


@pytest.mark.parametrize(
    "corruption", ["digest_only", "package_hash", "source_hash", "source_type"]
)
def test_retry_refuses_incomplete_or_inconsistent_provenance(
    tmp_path: Path, corruption: str
) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path)
    loki = loki_masked(tmp_path)
    module.promote(wheel, loki)
    target = loki / "vendor" / wheel.name
    proof_path = target.with_suffix(".provenance.json")
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    if corruption == "digest_only":
        proof = {"wheel_sha256": proof["wheel_sha256"]}
    elif corruption == "package_hash":
        proof["source"]["package_sha256"] = "0" * 64
    elif corruption == "source_hash":
        proof["source"]["package_files"]["mcp_loki_updates/__init__.py"] = "0" * 64
    else:
        proof["source"]["dirty"] = "true"
    proof_path.write_text(json.dumps(proof), encoding="utf-8")
    corrupt_bytes = proof_path.read_bytes()
    with pytest.raises(module.ReleaseRefused, match="existing_provenance_invalid"):
        module.promote(wheel, loki)
    assert target.read_bytes() == wheel.read_bytes()
    assert proof_path.read_bytes() == corrupt_bytes


def test_retry_preserves_complete_original_git_observation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = release_module()
    wheel = wheel_masked(tmp_path)
    loki = loki_masked(tmp_path)
    module.promote(wheel, loki)
    proof_path = (loki / "vendor" / wheel.name).with_suffix(".provenance.json")
    original = proof_path.read_bytes()
    newer_git = {
        ("status", "--porcelain=v1", "--untracked-files=normal"): "",
        ("rev-parse", "--verify", "HEAD"): "a" * 40,
        ("rev-parse", "HEAD^{tree}"): "b" * 40,
    }
    monkeypatch.setattr(module, "_git", lambda *args: newer_git[args])
    module.promote(wheel, loki)
    assert proof_path.read_bytes() == original
