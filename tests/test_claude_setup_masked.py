"""Execute the published setup commands with failing local-only tools."""

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

GUIDE = Path(__file__).resolve().parents[1] / "docs/DAILY_OPERATOR_UPDATES.md"


@pytest.mark.skipif(shutil.which("bash") is None, reason="Bash is required")
@pytest.mark.parametrize("platform", ["Mac", "Linux"])
@pytest.mark.parametrize("failure", ["configure", "run", "none"])
def test_setup_registers_only_after_configure_and_run_succeed(
    tmp_path: Path, platform: str, failure: str
) -> None:
    blocks = re.findall(r"```bash\n(.*?)```", GUIDE.read_text(), re.S)
    block = next(
        x
        for x in blocks
        if "git clone" in x
        and (
            ("launchctl bootstrap" in x) if platform == "Mac" else ("systemctl --user enable" in x)
        )
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    scripts = {
        "git": "exit 0\n",
        "claude": "exit 0\n",
        "uv": 'if [ "$1" = venv ]; then mkdir -p "$4/bin"; cp "$FAKE_PYTHON" "$4/bin/python"; fi\n',
        "fake-python": 'if [ "$2" = "$FAIL_ACTION" ]; then exit 1; fi\n'
        'touch "$HOME/Library/Application Support/Loki-Claude-Updates/'
        'com.themindops.loki-updates.plist" 2>/dev/null\n'
        'touch "$HOME/.local/share/loki-claude-updates/loki-claude-update.service" 2>/dev/null\n'
        'touch "$HOME/.local/share/loki-claude-updates/loki-claude-update.timer" 2>/dev/null\n'
        "exit 0\n",
        "launchctl": 'if [ "$1" = bootstrap ]; then touch "$REGISTERED"; fi\n',
        "systemctl": 'if [ "$2" = enable ]; then touch "$REGISTERED"; fi\n',
    }
    for name, content in scripts.items():
        path = bin_dir / name
        path.write_text("#!/bin/sh\n" + content)
        path.chmod(0o700)
    marker = tmp_path / "registered"
    env = dict(
        os.environ,
        HOME=str(tmp_path),
        PATH=str(bin_dir) + os.pathsep + os.defpath,
        FAKE_PYTHON=str(bin_dir / "fake-python"),
        FAIL_ACTION=failure,
        REGISTERED=str(marker),
    )
    result = subprocess.run(["bash", "-c", block], env=env, capture_output=True, timeout=10)
    assert marker.exists() == (failure == "none")
    assert (result.returncode == 0) == (failure == "none")


def powershell_probe(failure: str) -> str:
    block = next(
        x
        for x in re.findall(r"```powershell\n(.*?)```", GUIDE.read_text(), re.S)
        if "schtasks /Create" in x
    )
    action = failure if failure != "none" else "configure"
    start = next(
        line
        for line in block.splitlines()
        if line.startswith("& $lokiPython") and " " + action + " " in line
    )
    block = block[block.index(start) :]
    code = "0" if failure == "none" else "1"
    return (
        "$global:registered=$false\n$caught=$false\n"
        "function Invoke-SyntheticPython { $global:LASTEXITCODE=" + code + " }\n"
        "function schtasks { $global:registered=$true; $global:LASTEXITCODE=0 }\n"
        "function Get-ScheduledTaskInfo {}\n"
        "function Get-Command { [PSCustomObject]@{Source='/synthetic/claude.exe'} }\n"
        "$lokiRoot='/synthetic'\n$lokiPython='Invoke-SyntheticPython'\ntry {\n"
        + block
        + "\n} catch { $caught=$true }\n"
        + (
            "if (-not $registered -or $caught)"
            if failure == "none"
            else "if ($registered -or -not $caught)"
        )
        + " { throw 'Incorrect setup registration gate' }\nWrite-Output 'PASS setup gate'\n"
    )


@pytest.mark.skipif(shutil.which("pwsh") is None, reason="PowerShell is required")
@pytest.mark.parametrize("failure", ["configure", "run", "none"])
def test_windows_registration_gate(tmp_path: Path, failure: str) -> None:
    script = tmp_path / "setup_masked.ps1"
    script.write_text(powershell_probe(failure), encoding="utf-8-sig")
    subprocess.run(["pwsh", "-NoProfile", "-File", str(script)], check=True, capture_output=True)


@pytest.mark.skipif(shutil.which("bash") is None, reason="Bash is required")
def test_mac_disable_does_not_reload_at_next_login(tmp_path: Path) -> None:
    block = next(
        x
        for x in re.findall(r"```bash\n(.*?)```", GUIDE.read_text(), re.S)
        if x.startswith("launchctl bootout")
    )
    plist = tmp_path / "Library/LaunchAgents/com.themindops.loki-updates.plist"
    plist.parent.mkdir(parents=True)
    plist.write_text("synthetic")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    command = bin_dir / "launchctl"
    command.write_text("#!/bin/sh\nexit 0\n")
    command.chmod(0o700)
    subprocess.run(
        ["bash", "-c", block],
        check=True,
        capture_output=True,
        env=dict(os.environ, HOME=str(tmp_path), PATH=str(bin_dir) + os.pathsep + os.defpath),
    )
    assert not plist.exists()
