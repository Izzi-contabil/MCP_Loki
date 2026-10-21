"""Daily native Claude plugin refresh. Never reads or provisions MCP/OAuth."""

from __future__ import annotations

import argparse
import contextlib
import csv
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

MARKETPLACE = "loki-equipe"
PLUGIN = "loki-orientacoes@loki-equipe"


@contextlib.contextmanager
def lock(root: Path) -> Iterator[None]:
    root.mkdir(parents=True, mode=0o700, exist_ok=True)
    with (root / "update.lock").open("a+b") as handle:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            handle.write(b"0")
            handle.flush()
            handle.seek(0)
            try:
                cast(Any, msvcrt).locking(handle.fileno(), cast(Any, msvcrt).LK_NBLCK, 1)
            except OSError as exc:
                raise BlockingIOError from exc
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                cast(Any, msvcrt).locking(handle.fileno(), cast(Any, msvcrt).LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def save(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(".pending")
    temporary.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def invoke(args: list[str]) -> None:
    subprocess.run(
        args,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=300,
    )


def update(
    root: Path,
    claude: Path,
    *,
    now: datetime | None = None,
    run: Callable[[list[str]], None] = invoke,
    force: bool = False,
) -> dict[str, Any]:
    now = now or datetime.now(UTC)
    local = now.astimezone(ZoneInfo("America/Sao_Paulo"))
    today = local.date().isoformat()
    try:
        with lock(root):
            state = root / "status.json"
            previous = json.loads(state.read_text(encoding="utf-8")) if state.exists() else {}
            if not force and local.hour < 7:
                return {"status": "aguardando_07h"}
            if not force and previous.get("dia_brasilia") == today:
                return {"status": "ja_consultado_hoje"}
            result = {
                "status": "iniciado",
                "dia_brasilia": today,
                "horario_utc": now.isoformat(),
                "plugin": PLUGIN,
            }
            # Record the attempt first: network failures never cause one retry/minute.
            save(state, result)
            try:
                run([str(claude), "plugin", "marketplace", "update", MARKETPLACE])
                run([str(claude), "plugin", "update", PLUGIN, "--scope", "user"])
            except Exception:
                result["status"] = "falha_consultar_claude"
            else:
                result["status"] = "atualizado"
            save(state, result)
            return result
    except BlockingIOError:
        return {"status": "ocupado"}


def unit_quote(value: str) -> str:
    return (
        '"'
        + value.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%").replace("$", "$$")
        + '"'
    )


def configure(root: Path, claude: Path, *, platform: str = sys.platform) -> list[Path]:
    root = root.expanduser().resolve()
    claude = claude.expanduser().absolute()  # Keep the stable Claude launcher symlink.
    python = str(Path(sys.executable).absolute())  # Preserve venv; resolve() loses tzdata.
    for value in (str(root), str(claude), python):
        if any(ord(char) < 32 for char in value):
            raise ValueError("caminho_invalido")
    ZoneInfo("America/Sao_Paulo")  # Fail during setup if Windows lacks tzdata.
    root.mkdir(parents=True, mode=0o700, exist_ok=True)
    driver = root / "claude_daily.py"
    if driver.resolve() != Path(__file__).resolve():
        shutil.copyfile(__file__, driver)
    custom_profile = os.environ.get("CLAUDE_CONFIG_DIR")
    save(
        root / "config.json",
        {
            "claude": str(claude),
            "path": os.environ.get("PATH", ""),
            "claude_config_dir": (
                str(Path(custom_profile).expanduser().absolute()) if custom_profile else None
            ),
        },
    )
    argv = [python, str(driver), "tick", "--root", str(root)]
    if platform == "darwin":
        path = root / "com.themindops.loki-updates.plist"
        path.write_bytes(
            plistlib.dumps(
                {
                    "Label": "com.themindops.loki-updates",
                    "ProgramArguments": argv,
                    "StartInterval": 60,
                    "RunAtLoad": True,
                    "ProcessType": "Background",
                }
            )
        )
        return [path]
    if platform == "linux":
        service, timer = root / "loki-claude-update.service", root / "loki-claude-update.timer"
        service.write_text(
            "[Unit]\nDescription=Atualização Loki no Claude Code\n[Service]\nType=oneshot\n"
            + "ExecStart="
            + " ".join(unit_quote(x) for x in argv)
            + "\n",
            encoding="utf-8",
        )
        timer.write_text(
            "[Unit]\nDescription=Consulta diária Loki às 07h de Brasília\n[Timer]\n"
            "OnBootSec=60s\nOnUnitActiveSec=60s\nAccuracySec=1s\n"
            "[Install]\nWantedBy=timers.target\n",
            encoding="utf-8",
        )
        return [service, timer]
    if platform != "win32":
        raise ValueError("plataforma_nao_suportada")
    ns = "http://schemas.microsoft.com/windows/2004/02/mit/task"
    ET.register_namespace("", ns)

    def element(parent: ET.Element, tag: str, text: str | None = None, **attrs: str) -> ET.Element:
        node = ET.SubElement(parent, "{" + ns + "}" + tag, attrs)
        node.text = text
        return node

    task = ET.Element("{" + ns + "}Task", {"version": "1.2"})
    triggers = element(task, "Triggers")
    trigger = element(triggers, "CalendarTrigger")
    repeat = element(trigger, "Repetition")
    element(repeat, "Interval", "PT1M")
    element(repeat, "Duration", "P1D")
    element(repeat, "StopAtDurationEnd", "false")
    element(trigger, "StartBoundary", "2026-01-01T00:00:00Z")
    element(element(trigger, "ScheduleByDay"), "DaysInterval", "1")
    element(element(triggers, "LogonTrigger"), "Enabled", "true")
    principal = element(element(task, "Principals"), "Principal", id="Operator")
    # The SID is ASCII even when whoami's account name uses an OEM code page.
    raw_identity = subprocess.check_output(["whoami", "/user", "/fo", "csv", "/nh"])
    identities = list(csv.reader(raw_identity.decode("latin-1").splitlines()))
    if len(identities) != 1 or len(identities[0]) != 2:
        raise ValueError("identidade_windows_invalida")
    identity = identities[0][1]
    if not re.fullmatch(r"S-1-\d+(?:-\d+)+", identity):
        raise ValueError("identidade_windows_invalida")
    element(principal, "UserId", identity)
    element(principal, "LogonType", "InteractiveToken")
    element(principal, "RunLevel", "LeastPrivilege")
    settings = element(task, "Settings")
    element(settings, "MultipleInstancesPolicy", "IgnoreNew")
    element(settings, "DisallowStartIfOnBatteries", "false")
    element(settings, "StopIfGoingOnBatteries", "false")
    element(settings, "StartWhenAvailable", "true")
    element(settings, "ExecutionTimeLimit", "PT15M")
    action = element(element(task, "Actions", Context="Operator"), "Exec")
    # pythonw prevents a console flashing for the lightweight minute tick.
    pythonw = Path(python).with_name("pythonw.exe")
    element(action, "Command", str(pythonw) if pythonw.exists() else python)
    element(action, "Arguments", subprocess.list2cmdline(argv[1:]))
    path = root / "loki-claude-update.xml"
    path.write_bytes(ET.tostring(task, encoding="utf-16", xml_declaration=True))
    return [path]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["configure", "tick", "run", "status"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--claude", type=Path)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if args.action == "configure":
        binary = args.claude or (Path(found) if (found := shutil.which("claude")) else None)
        if binary is None or not binary.is_file():
            parser.error("informe --claude com o executável nativo do Claude Code")
        print(json.dumps([str(p) for p in configure(root, binary)], ensure_ascii=False))
        return 0
    if args.action == "status":
        print(
            (root / "status.json").read_text(encoding="utf-8")
            if (root / "status.json").exists()
            else '{"status":"ainda_nao_executado"}'
        )
        return 0
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    os.environ["PATH"] = config["path"]
    if config.get("claude_config_dir"):
        os.environ["CLAUDE_CONFIG_DIR"] = config["claude_config_dir"]
    else:
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
    result = update(root, Path(config["claude"]), force=args.action == "run")
    if args.action == "run":
        print(json.dumps(result, ensure_ascii=False))
    return 1 if result["status"] == "falha_consultar_claude" else 0


if __name__ == "__main__":
    raise SystemExit(main())
