"""Repository controls protect reviewed bytes and exclude local private state."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_state_is_ignored_but_instruction_sources_are_not() -> None:
    private = [
        ".env",
        ".env.production",
        ".venv/private",
        "var/private",
        "outputs/private",
        "clientes/private",
        "src/mcp_loki_updates/__pycache__/private.pyc",
    ]
    result = subprocess.run(
        ["git", "check-ignore", "--", *private],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert set(result.stdout.splitlines()) == set(private)
    source = subprocess.run(
        ["git", "check-ignore", "--", "src/mcp_loki_updates/data/domains/geral.md"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert source.returncode == 1 and not source.stdout


def test_git_preserves_hashed_instruction_bytes_on_windows_checkout() -> None:
    result = subprocess.run(
        [
            "git",
            "check-attr",
            "eol",
            "--",
            "src/mcp_loki_updates/data/domains/geral.md",
            "src/mcp_loki_updates/data/domains/geral.json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout.count(": eol: lf") == 2


def test_instruction_snapshot_from_git_index_is_valid(tmp_path: Path) -> None:
    from mcp_loki_updates import InstructionsProvider

    data = "src/mcp_loki_updates/data/"
    files = subprocess.run(
        ["git", "ls-files", "--", data],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert data + "release.json" in files
    assert data + "domains/geral.json" in files
    for name in files:
        content = subprocess.run(
            ["git", "show", ":" + name],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        target = tmp_path / name.removeprefix(data)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    assert InstructionsProvider(tmp_path).health()["status"] == "ok"
