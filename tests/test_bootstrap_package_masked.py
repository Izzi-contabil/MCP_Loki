"""The shared native plugin ships readers without replacing the OAuth connection."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_marketplace_has_complete_offline_plugin_and_stable_bootstrap() -> None:
    catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    assert catalog["name"] == "loki-equipe"
    assert catalog["plugins"] == [
        {"name": "loki-orientacoes", "source": "./plugins/loki-bootstrap"}
    ]
    plugin = ROOT / "plugins/loki-bootstrap"
    manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert set(manifest) == {"name", "version", "description"}
    assert manifest["name"] == "loki-orientacoes"
    assert manifest["version"] == "2.2.0"
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
        "skills/investigar-regras-dp/SKILL.md",
        "skills/investigar-regras-dp/references/QUALIFICACAO.md",
        "skills/registrar-problema-loki/SKILL.md",
        "skills/registrar-problema-loki/references/relato.json",
        "skills/operar-loki/SKILL.md",
        "skills/operar-loki/references/WORKFLOWS.md",
        "skills/operar-loki/references/ESOCIAL.md",
        "skills/operar-loki/references/ROUTINES.md",
        "skills/operar-loki/references/COMPARATIVE_TESTING.md",
        "skills/operar-loki/scripts/loki_local.py",
        "skills/operar-loki/scripts/loki_local.py.lock",
        "skills/operar-loki/scripts/loki_readers/__init__.py",
        "skills/operar-loki/scripts/loki_readers/private.py",
        "skills/operar-loki/scripts/loki_readers/readers.py",
        "skills/operar-loki/scripts/loki_readers/exchange.py",
        "skills/operar-loki/scripts/loki_readers/workspace.py",
    }


def test_feedback_skill_is_discoverable_and_uses_existing_authenticated_action() -> None:
    plugin = ROOT / "plugins/loki-bootstrap"
    skill = (plugin / "skills/registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    example = json.loads(
        (plugin / "skills/registrar-problema-loki/references/relato.json").read_text(
            encoding="utf-8"
        )
    )
    bootstrap = (plugin / "SKILL.md").read_text(encoding="utf-8")
    operator = (plugin / "skills/operar-loki/SKILL.md").read_text(encoding="utf-8")
    assert "registrar-problema-loki" in bootstrap
    assert "registrar-problema-loki" in operator
    assert "registrar_problema" in skill
    assert "meu_acesso" in skill
    assert "runtime.json" not in skill
    assert example["schema_version"] == "loki.feedback/1"
    assert example["kind"] == "ajuste"
    assert example["severity"] == "baixa"
    assert "TESTE" in example["summary"]
    assert not any("webhook" in name or "token" in name for name in example)


def test_investigation_is_reachable_and_all_its_markdown_links_resolve() -> None:
    plugin = ROOT / "plugins/loki-bootstrap"
    skill = plugin / "skills/investigar-regras-dp/SKILL.md"
    for entry in (
        plugin / "skills/operar-loki/SKILL.md",
        plugin / "skills/operar-loki/references/ROUTINES.md",
    ):
        targets = {
            (entry.parent / link).resolve()
            for link in re.findall(r"\]\(([^)]+\.md)\)", entry.read_text(encoding="utf-8"))
        }
        assert skill.resolve() in targets
    for entry in (skill, skill.parent / "references/QUALIFICACAO.md"):
        for link in re.findall(r"\]\(([^)]+\.md)\)", entry.read_text(encoding="utf-8")):
            assert (entry.parent / link).is_file(), (entry, link)
    assert skill.parent.name == "investigar-regras-dp"
