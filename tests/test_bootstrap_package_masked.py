"""The shared native plugin ships readers without replacing the OAuth connection."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_marketplace_has_complete_offline_plugin_and_stable_bootstrap() -> None:
    catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert catalog["name"] == "loki-equipe"
    assert catalog["plugins"] == [
        {"name": "loki-orientacoes", "source": "./plugins/loki-bootstrap"}
    ]
    plugin = ROOT / "plugins/loki-bootstrap"
    manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
    assert set(manifest) == {"name", "version", "description"}
    assert manifest["name"] == "loki-orientacoes"
    assert manifest["version"] == "1.1.0"
    assert (plugin / "skills/loki-bootstrap/SKILL.md").read_bytes() == (
        plugin / "SKILL.md"
    ).read_bytes()
    assert {
        p.relative_to(plugin).as_posix()
        for p in plugin.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    } == {
        ".claude-plugin/plugin.json",
        "SKILL.md",
        "README.md",
        "skills/loki-bootstrap/SKILL.md",
        "skills/operar-loki/SKILL.md",
        "skills/operar-loki/references/WORKFLOWS.md",
        "skills/operar-loki/scripts/loki_local.py",
        "skills/operar-loki/scripts/loki_local.py.lock",
        "skills/operar-loki/scripts/loki_readers/__init__.py",
        "skills/operar-loki/scripts/loki_readers/private.py",
        "skills/operar-loki/scripts/loki_readers/readers.py",
        "skills/operar-loki/scripts/loki_readers/exchange.py",
        "skills/operar-loki/scripts/loki_readers/workspace.py",
    }
