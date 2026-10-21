"""Consumer boundary tests: corrupt input cannot replace a validated snapshot."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

DOMAINS = (
    "geral",
    "admissao",
    "rescisao",
    "ferias",
    "decimo_terceiro",
    "afastamento",
    "documentos",
    "aprovacoes",
)


def provider_type() -> Any:
    from mcp_loki_updates import InstructionsProvider

    return InstructionsProvider


@pytest.fixture
def snapshot(tmp_path: Path) -> Path:
    """Copy packaged inputs so tests exercise the real decoder and filesystem."""
    import mcp_loki_updates

    source = Path(mcp_loki_updates.__file__).parent / "data"
    shutil.copytree(source, tmp_path / "snapshot")
    return tmp_path / "snapshot"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def reseal(root: Path, domain: str) -> None:
    """Model a reviewed publisher producing a new consistent release manifest."""
    release = json.loads((root / "release.json").read_text(encoding="utf-8"))
    for extension, key in (("json", "metadata_sha256"), ("md", "content_sha256")):
        content = (root / "domains" / f"{domain}.{extension}").read_bytes()
        release["domains"][domain][key] = hashlib.sha256(content).hexdigest()
    write_json(root / "release.json", release)


def test_packaged_provider_exposes_eight_safe_domains_and_defensive_copies() -> None:
    provider = provider_type()()
    assert provider.domains() == DOMAINS
    value = provider.get("admissao")
    assert value["dominio"] == "admissao"
    assert value["version"] == "1.2.1"
    assert value["updated_at"] == "2026-10-21"
    assert value["instructions"].strip()
    assert value["permissions"] == {"capabilities": ["consultar"], "processes": ["admissao"]}
    value["permissions"]["capabilities"].clear()
    assert provider.get("admissao")["permissions"]["capabilities"] == ["consultar"]
    assert provider.get("geral")["permissions"] == {"capabilities": [], "processes": []}
    assert provider.get("documentos")["permissions"]["processes"] == []
    assert provider.get("aprovacoes")["permissions"]["capabilities"] == ["decidir_chat"]


@pytest.mark.parametrize("domain", ["../geral", "GERAL", "", "unknown", "geral.md"])
def test_rejects_domain_outside_allowlist(domain: str) -> None:
    from mcp_loki_updates import InvalidDomain

    with pytest.raises(InvalidDomain, match="invalid_domain"):
        provider_type()().get(domain)


def test_reload_is_atomic_and_retains_last_good_snapshot(snapshot: Path) -> None:
    provider = provider_type()(snapshot)
    original = provider.get("admissao")
    (snapshot / "domains" / "admissao.md").write_text("TEXTO NÃO SELADO", encoding="utf-8")
    assert provider.reload() is False
    assert provider.get("admissao") == original
    assert provider.health()["status"] == "degraded"
    assert provider.health()["error_code"] == "instructions_snapshot_invalid"
    reseal(snapshot, "admissao")
    assert provider.reload() is True
    assert provider.get("admissao")["instructions"] == "TEXTO NÃO SELADO"
    assert provider.health()["status"] == "ok"
    assert provider.health()["error_code"] is None


def test_unavailable_initial_snapshot_has_sanitized_error(tmp_path: Path) -> None:
    from mcp_loki_updates import InstructionsUnavailable

    private_root = tmp_path / "private-client-name"
    with pytest.raises(InstructionsUnavailable) as caught:
        provider_type()(private_root)
    assert str(caught.value) == "instructions_snapshot_unavailable"
    assert caught.value.__cause__ is None


@pytest.mark.parametrize(
    "corruption",
    [
        "unknown_release_key",
        "unknown_domain_key",
        "domain_mismatch",
        "empty_text",
        "oversize",
        "invalid_utf8",
        "invalid_version",
        "invalid_date",
        "unknown_permission",
        "missing_domain",
        "bad_hash",
        "duplicate_json_key",
        "permission_extra",
        "noncanonical_date",
    ],
)
def test_rejects_invalid_snapshot_even_when_hashes_are_consistent(
    snapshot: Path,
    corruption: str,
) -> None:
    from mcp_loki_updates import InstructionsUnavailable

    release_path = snapshot / "release.json"
    metadata_path = snapshot / "domains" / "admissao.json"
    text_path = snapshot / "domains" / "admissao.md"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if corruption == "unknown_release_key":
        release["root"] = "private-file"
    elif corruption == "unknown_domain_key":
        metadata["path"] = "../../secret"
    elif corruption == "domain_mismatch":
        metadata["dominio"] = "rescisao"
    elif corruption == "empty_text":
        text_path.write_bytes(b" \n\t")
    elif corruption == "oversize":
        text_path.write_bytes(b"x" * 65537)
    elif corruption == "invalid_utf8":
        text_path.write_bytes(b"\xff")
    elif corruption == "invalid_version":
        metadata["version"] = "01.2.3"
    elif corruption == "invalid_date":
        metadata["updated_at"] = "2026-02-30"
    elif corruption == "noncanonical_date":
        metadata["updated_at"] = "20261019"
    elif corruption == "unknown_permission":
        metadata["permissions"]["capabilities"] = ["all"]
    elif corruption == "missing_domain":
        del release["domains"]["ferias"]
    elif corruption == "bad_hash":
        release["domains"]["ferias"]["content_sha256"] = "0" * 64
    elif corruption == "permission_extra":
        metadata["permissions"]["root"] = True
    write_json(release_path, release)
    write_json(metadata_path, metadata)
    if corruption == "duplicate_json_key":
        metadata_path.write_text('{"dominio":"admissao","dominio":"geral"}', encoding="utf-8")
    reseal(snapshot, "admissao")
    with pytest.raises(InstructionsUnavailable):
        provider_type()(snapshot)


def test_metadata_is_sanitized_and_returns_domain_versions() -> None:
    provider = provider_type()()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.1.3"
    assert metadata["mcp_contract_version"] == "1.0.0"
    assert metadata["versions_by_domain"] == {
        domain: "1.2.1"
        if domain == "admissao"
        else "1.1.1"
        if domain == "documentos"
        else "1.1.0"
        if domain in {"geral", "rescisao"}
        else "1.0.0"
        for domain in DOMAINS
    }
    assert "root" not in metadata
    assert "instructions" not in metadata
    metadata["versions_by_domain"]["admissao"] = "999.0.0"
    assert provider.metadata()["versions_by_domain"]["admissao"] == "1.2.1"


def test_rejects_symlinked_data_file(snapshot: Path, tmp_path: Path) -> None:
    from mcp_loki_updates import InstructionsUnavailable

    content_path = snapshot / "domains" / "admissao.md"
    target = tmp_path / "external.md"
    target.write_bytes(content_path.read_bytes())
    content_path.unlink()
    try:
        content_path.symlink_to(target)
    except OSError:
        pytest.skip("Windows account does not have symlink privilege")
    with pytest.raises(InstructionsUnavailable):
        provider_type()(snapshot)


def test_rejects_mixed_release_during_read(snapshot: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from mcp_loki_updates import InstructionsUnavailable

    original_read = Path.read_bytes
    count = 0

    def racing_read(path: Path) -> bytes:
        nonlocal count
        data = original_read(path)
        if path.name == "release.json":
            count += 1
            if count > 1:
                return data + b" "
        return data

    # Simulate a publisher changing release bytes between the two integrity checks.
    monkeypatch.setattr(Path, "read_bytes", racing_read)
    with pytest.raises(InstructionsUnavailable):
        provider_type()(snapshot)


def test_new_contract_major_cannot_replace_supported_snapshot(snapshot: Path) -> None:
    from mcp_loki_updates import InstructionsUnavailable

    provider = provider_type()(snapshot)
    release_path = snapshot / "release.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["contract_version"] = "2.0.0"
    write_json(release_path, release)
    for domain in DOMAINS:
        path = snapshot / "domains" / f"{domain}.json"
        metadata = json.loads(path.read_text(encoding="utf-8"))
        metadata["compatibility"]["mcp_contract_version"] = "2.0.0"
        write_json(path, metadata)
        reseal(snapshot, domain)
    assert provider.reload() is False
    assert provider.metadata()["mcp_contract_version"] == "1.0.0"
    assert provider.health()["status"] == "degraded"
    with pytest.raises(InstructionsUnavailable):
        provider_type()(snapshot)
