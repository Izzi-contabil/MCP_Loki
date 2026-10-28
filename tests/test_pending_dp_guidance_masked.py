"""Real snapshot validation for additive DP guides; host grants remain external."""

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider, InstructionsUnavailable

LEGACY_DOMAINS = (
    "geral",
    "admissao",
    "rescisao",
    "ferias",
    "decimo_terceiro",
    "afastamento",
    "documentos",
    "aprovacoes",
)
NEW_DOMAINS = (
    "alteracao_cadastral",
    "ocorrencia",
    "adiantamento",
    "aviso_ferias",
    "aviso_rescisao",
)
PROCESS_TYPES = (
    "admissao",
    "folha_mensal",
    "rescisao",
    "ferias",
    "decimo_terceiro",
    "afastamento",
    "transferencia",
    "fechamento",
    "informe_rendimentos",
    "estagio",
    "autonomo",
    "pro_labore",
    "distribuicao_lucros",
    *NEW_DOMAINS,
)


def test_additive_guides_declare_single_process_and_consultation() -> None:
    provider = InstructionsProvider()
    assert provider.domains() == (*LEGACY_DOMAINS, *NEW_DOMAINS)
    for process in NEW_DOMAINS:
        guide = provider.get(process)
        assert guide["version"] == "2.0.2"
        assert guide["permissions"] == {"capabilities": ["consultar"], "processes": [process]}
        assert "get_dp_capabilities" in guide["instructions"]
        assert "get_process_contract" in guide["instructions"]
        assert f"dados_{process}" in guide["instructions"]


def _snapshot_with_processes(tmp_path: Path, processes: list[str]) -> Path:
    import mcp_loki_updates

    root = tmp_path / "snapshot"
    shutil.copytree(Path(mcp_loki_updates.__file__).parent / "data", root)
    metadata_path = root / "domains" / "documentos.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["permissions"]["processes"] = processes
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    release_path = root / "release.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["domains"]["documentos"]["metadata_sha256"] = hashlib.sha256(
        metadata_path.read_bytes()
    ).hexdigest()
    release_path.write_text(json.dumps(release), encoding="utf-8")
    return root


def test_process_allowlist_accepts_all_host_processes_independent_of_domains(
    tmp_path: Path,
) -> None:
    provider = InstructionsProvider(_snapshot_with_processes(tmp_path, list(PROCESS_TYPES)))
    assert provider.get("documentos")["permissions"]["processes"] == list(PROCESS_TYPES)


@pytest.mark.parametrize("process", ["geral", "documentos", "aprovacoes", "all", "../ocorrencia"])
def test_non_process_domain_cannot_be_used_as_process_scope(tmp_path: Path, process: str) -> None:
    with pytest.raises(InstructionsUnavailable, match="instructions_snapshot_unavailable"):
        InstructionsProvider(_snapshot_with_processes(tmp_path, [process]))


def test_operational_guide_delivery_preserves_factual_and_financial_limits() -> None:
    provider = InstructionsProvider()
    for process in ("afastamento", *NEW_DOMAINS):
        text = provider.get(process)["instructions"]
        assert "receive_case_data" in text
        assert "get_process_contract" in text
    for process in ("alteracao_cadastral", "ocorrencia"):
        text = provider.get(process)["instructions"]
        assert "JSON" in text and "sem PDF" in text
        assert "supports_apply=false" in text
    advance = provider.get("adiantamento")["instructions"]
    for literal in ("advance-v1", "AdvancePolicy", "None", "pending", "centavos", "pagamento"):
        assert literal in advance
    assert provider.check_version("2.0.0", "2.0.0")["compatible"] is True
    assert provider.check_version()["compatible"] is None


def test_new_process_access_uses_existing_admin_browser_and_preserves_legacy_tool_vocabulary() -> (
    None
):
    guide = InstructionsProvider().get("aprovacoes")
    assert guide["version"] == "2.0.2"
    text = guide["instructions"]
    for literal in ("preparar_autorizacao", "13 processos", "/admin", *NEW_DOMAINS):
        assert literal in text
    assert "não envie os cinco novos" in text
