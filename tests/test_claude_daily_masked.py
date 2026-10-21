"""The native profile updates a declarative plugin, never the MCP identity."""

import importlib.util
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]


def module() -> Any:
    spec = importlib.util.spec_from_file_location("claude_daily", ROOT / "scripts/claude_daily.py")
    assert spec and spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_marketplace_has_only_declarative_bootstrap() -> None:
    catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert catalog["name"] == "loki-equipe"
    assert catalog["plugins"] == [
        {"name": "loki-orientacoes", "source": "./plugins/loki-bootstrap"}
    ]
    plugin = ROOT / "plugins/loki-bootstrap"
    manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
    assert set(manifest) == {"name", "version", "description"}
    assert manifest["name"] == "loki-orientacoes"
    assert (plugin / "skills/loki-bootstrap/SKILL.md").read_bytes() == (
        plugin / "SKILL.md"
    ).read_bytes()
    assert {str(p.relative_to(plugin)) for p in plugin.rglob("*") if p.is_file()} == {
        ".claude-plugin/plugin.json",
        "SKILL.md",
        "README.md",
        "skills/loki-bootstrap/SKILL.md",
    }


def test_native_update_preserves_oauth_and_is_daily(tmp_path: Path) -> None:
    daily = module()
    credentials = tmp_path / ".claude/.credentials.json"
    credentials.parent.mkdir()
    credentials.write_text("synthetic-oauth-keep-exactly")
    config = tmp_path / ".claude.json"
    config.write_text("synthetic-existing-mcp-configuration")
    calls: list[list[str]] = []

    def run(args: list[str]) -> None:
        calls.append(args)

    state = tmp_path / "daily"
    now = datetime(2026, 10, 21, 9, 59, tzinfo=UTC)
    assert (
        daily.update(state, Path("/synthetic/claude"), now=now, run=run)["status"]
        == "aguardando_07h"
    )
    now = datetime(2026, 10, 21, 10, 0, tzinfo=UTC)
    assert (
        daily.update(state, Path("/synthetic/claude"), now=now, run=run)["status"] == "atualizado"
    )
    assert calls == [
        ["/synthetic/claude", "plugin", "marketplace", "update", "loki-equipe"],
        [
            "/synthetic/claude",
            "plugin",
            "update",
            "loki-orientacoes@loki-equipe",
            "--scope",
            "user",
        ],
    ]
    assert (
        daily.update(state, Path("/synthetic/claude"), now=now, run=run)["status"]
        == "ja_consultado_hoje"
    )
    assert len(calls) == 2
    assert credentials.read_text() == "synthetic-oauth-keep-exactly"
    assert config.read_text() == "synthetic-existing-mcp-configuration"
    assert (
        daily.update(state, Path("/synthetic/claude"), now=now, run=run, force=True)["status"]
        == "atualizado"
    )


def test_failure_is_visible_sanitized_and_can_retry_manually(tmp_path: Path) -> None:
    daily = module()

    def fail(args: list[str]) -> None:
        raise RuntimeError("synthetic-private-output")

    now = datetime(2026, 10, 21, 14, tzinfo=UTC)
    result = daily.update(tmp_path, Path("/claude"), now=now, run=fail)
    assert result["status"] == "falha_consultar_claude"
    assert "synthetic-private-output" not in (tmp_path / "status.json").read_text()
    assert (
        daily.update(tmp_path, Path("/claude"), now=now, run=fail)["status"] == "ja_consultado_hoje"
    )
    assert (
        daily.update(tmp_path, Path("/claude"), now=now, run=lambda _: None, force=True)["status"]
        == "atualizado"
    )


def test_concurrent_tick_cannot_mutate_plugin(tmp_path: Path) -> None:
    daily = module()
    calls: list[list[str]] = []
    with daily.lock(tmp_path):
        result = daily.update(tmp_path, Path("/claude"), run=calls.append, force=True)
    assert result["status"] == "ocupado"
    assert not calls


def test_configure_keeps_stable_launcher_and_absolute_custom_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    daily = module()
    executable = tmp_path / "versioned-claude"
    executable.write_text("synthetic")
    launcher = tmp_path / "claude"
    launcher.symlink_to(executable)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "custom-profile")
    root = tmp_path / "daily"
    daily.configure(root, launcher, platform="linux")
    config = json.loads((root / "config.json").read_text())
    assert config["claude"] == str(launcher)
    assert config["claude_config_dir"] == str(tmp_path / "custom-profile")


def test_default_profile_cannot_inherit_a_different_scheduler_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    daily = module()
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    daily.configure(tmp_path, Path("/claude"), platform="linux")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/synthetic/unexpected-profile")

    def update(*args: Any, **kwargs: Any) -> dict[str, str]:
        assert os.environ.get("CLAUDE_CONFIG_DIR") is None
        return {"status": "atualizado"}

    monkeypatch.setattr(daily, "update", update)
    monkeypatch.setattr(sys, "argv", ["claude_daily.py", "run", "--root", str(tmp_path)])
    assert daily.main() == 0


@pytest.mark.parametrize("platform", ["darwin", "linux", "win32"])
def test_scheduler_uses_stable_absolute_runner_and_no_credentials(
    tmp_path: Path, platform: str
) -> None:
    daily = module()
    root = tmp_path / "café with spaces"
    paths = daily.configure(root, Path("/absolute/claude"), platform=platform)
    text = "\n".join(
        p.read_text(encoding="utf-16" if platform == "win32" else "utf-8") for p in paths
    )
    assert "claude_daily.py" in text
    assert "secret" not in text.lower() and "password" not in text.lower()
    assert (root / "claude_daily.py").read_bytes() == (
        ROOT / "scripts/claude_daily.py"
    ).read_bytes()
    if platform == "darwin":
        import plistlib

        plist = plistlib.loads(paths[0].read_bytes())
        assert plist["StartInterval"] == 60 and plist["RunAtLoad"] is True
        assert plist["ProgramArguments"][-1] == str(root.resolve())
    elif platform == "linux":
        assert "OnUnitActiveSec=60s" in text and "OnBootSec=60s" in text
        assert '"' + str(root.resolve()) + '"' in text
    else:
        import xml.etree.ElementTree as ET

        tree = ET.fromstring(paths[0].read_bytes())
        ns = {"t": "http://schemas.microsoft.com/windows/2004/02/mit/task"}
        assert tree.find(".//t:Interval", ns).text == "PT1M"
        assert tree.find(".//t:LogonType", ns).text == "InteractiveToken"
        assert tree.find(".//t:MultipleInstancesPolicy", ns).text == "IgnoreNew"
