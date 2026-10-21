"""Run the shipped entrypoint, including paths with spaces, without live MCP."""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins/loki-bootstrap/skills/operar-loki/scripts/loki_local.py"
)


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, timeout=60
    )


def test_entrypoint_selftest_runs_all_portable_engines_without_oauth(tmp_path):
    result = run("doctor", tmp_path / "diagnostico privado")
    assert result.returncode == 0, result.stderr
    receipt = json.loads(result.stdout)
    assert receipt["status"] == "local_readers_ready"
    assert receipt["oauth"] == "existing_harness_connection_untouched"
    assert (tmp_path / "diagnostico privado/pdf/manifest.json").exists()


def test_cli_read_then_csv_request_keeps_interpretation_in_harness(tmp_path):
    source = tmp_path / "leitura mascarada.csv"
    source.write_text("campo;valor\nzero;0\n", encoding="utf-8")
    read = run("read", source, tmp_path / "leitura local")
    assert read.returncode == 0, read.stderr
    assert json.loads(read.stdout)["status"] == "requires_harness_review"
    prepared = run(
        "csv-request",
        source,
        tmp_path / "pedido privado",
        "--destination",
        "case",
        "--target",
        "SYNTHETIC-1",
    )
    assert prepared.returncode == 0, prepared.stderr
    request = json.loads((tmp_path / "pedido privado/request.json").read_text())
    assert request["state"] == "prepared_not_sent"
    assert request["tool"] == "anexar_documento_conteudo"


def test_inventory_covers_each_file_and_reports_unsupported_without_reading_symlinks(tmp_path):
    sources = tmp_path / "originais"
    sources.mkdir()
    (sources / "texto.txt").write_text("sintetico")
    (sources / "desconhecido.bin").write_bytes(b"synthetic")
    result = run("inventory", sources, tmp_path / "inventario")
    assert result.returncode == 0, result.stderr
    data = json.loads((tmp_path / "inventario/inventory.json").read_text())
    assert len(data["files"]) == 2
    by_name = {item["relative_path"]: item for item in data["files"]}
    assert by_name["texto.txt"]["status"] == "pending_harness_reading"
    assert by_name["desconhecido.bin"]["status"] == "unsupported_format"


def test_error_never_echoes_private_document_contents(tmp_path):
    source = tmp_path / "dado.csv"
    source.write_bytes(b"%PDF-1.7 PRIVATE_SYNTHETIC_MARKER")
    result = run(
        "csv-request",
        source,
        tmp_path / "pedido",
        "--destination",
        "case",
        "--target",
        "SYNTHETIC-1",
    )
    assert result.returncode == 1
    assert "PRIVATE_SYNTHETIC_MARKER" not in result.stdout + result.stderr
    assert not (tmp_path / "pedido/request.json").exists()


def test_local_runtime_does_not_access_network_or_client_auth_stores(tmp_path):
    code = """
import sys,runpy
from pathlib import Path
blocked = [str(Path.home()/p) for p in [
    ".codex/auth.json", ".codex/config.toml", ".claude.json", ".claude/.credentials.json"
]]
def audit(event,args):
    if event in {"socket.connect", "socket.getaddrinfo"}:
        raise AssertionError("network_access_forbidden")
    if event == "open" and str(args[0]) in blocked:
        raise AssertionError("client_credentials_forbidden")
sys.addaudithook(audit)
sys.path.insert(0,str(Path(sys.argv[1]).parent))
sys.argv=[sys.argv[1],"doctor",sys.argv[2]]
runpy.run_path(sys.argv[0],run_name="__main__")
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(SCRIPT), str(tmp_path / "offline")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "local_readers_ready"
