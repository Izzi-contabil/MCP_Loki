"""The shared native plugin remains declarative and preserves the stable skill."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
