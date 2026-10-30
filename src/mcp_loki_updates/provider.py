"""Validate complete filesystem snapshots before publishing them to readers."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import stat
import threading
from dataclasses import dataclass
from datetime import date
from functools import total_ordering
from pathlib import Path
from typing import Any, cast

PROVIDER_VERSION = "0.3.1"
SUPPORTED_CONTRACT_MAJOR = 2
DOMAINS = (
    "geral",
    "admissao",
    "rescisao",
    "ferias",
    "decimo_terceiro",
    "afastamento",
    "documentos",
    "aprovacoes",
    "alteracao_cadastral",
    "ocorrencia",
    "adiantamento",
    "aviso_ferias",
    "aviso_rescisao",
)
# Process scopes follow the host enum, independently of instruction domains.
PROCESS_TYPES = frozenset(
    {
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
        "alteracao_cadastral",
        "ocorrencia",
        "adiantamento",
        "aviso_ferias",
        "aviso_rescisao",
    }
)
MAX_FILE_BYTES = 65536
_CHANGES = {"backend", "instructions", "compatible_tools", "breaking_contract", "plugin"}
_RELEASE_KEYS = {
    "schema_version",
    "instructions_version",
    "contract_version",
    "plugin_version",
    "minimum_plugin_version",
    "updated_at",
    "domains",
    "changes",
}
_DOMAIN_KEYS = {"dominio", "version", "updated_at", "compatibility", "permissions"}
_COMPATIBILITY_KEYS = {
    "mcp_contract_version",
    "minimum_plugin_version",
    "recommended_plugin_version",
}
_SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


class InstructionsUnavailable(RuntimeError):
    """No complete validated snapshot was available at initialization."""


class InvalidDomain(ValueError):
    """Domain is not in the fixed public allowlist."""


class _InvalidSnapshot(ValueError):
    pass


@total_ordering
@dataclass(frozen=True, eq=False)
class _Version:
    """Strict SemVer 2.0 precedence; build metadata never changes precedence."""

    core: tuple[int, int, int]
    prerelease: tuple[str, ...]

    @classmethod
    def parse(cls, value: Any) -> _Version:
        if not isinstance(value, str) or len(value) > 128:
            raise ValueError("invalid_version")
        match = _SEMVER.fullmatch(value)
        if match is None:
            raise ValueError("invalid_version")
        prerelease = tuple(match[4].split(".")) if match[4] else ()
        if any(part.isdigit() and len(part) > 1 and part.startswith("0") for part in prerelease):
            raise ValueError("invalid_version")
        return cls((int(match[1]), int(match[2]), int(match[3])), prerelease)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Version):
            return NotImplemented
        return self.core == other.core and self.prerelease == other.prerelease

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, _Version):
            return NotImplemented
        if self.core != other.core:
            return self.core < other.core
        if not self.prerelease or not other.prerelease:
            return bool(self.prerelease) and not other.prerelease
        for left, right in zip(self.prerelease, other.prerelease, strict=False):
            if left == right:
                continue
            if left.isdigit() and right.isdigit():
                return int(left) < int(right)
            if left.isdigit() != right.isdigit():
                return left.isdigit()
            return left < right
        return len(self.prerelease) < len(other.prerelease)


def _object(value: Any, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise _InvalidSnapshot
    return cast(dict[str, Any], value)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _InvalidSnapshot
        result[key] = value
    return result


def _json(content: bytes) -> Any:
    return json.loads(content.decode("utf-8"), object_pairs_hook=_pairs)


def _iso_date(value: Any) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise _InvalidSnapshot
    date.fromisoformat(value)


def _strings(value: Any, allowed: set[str] | None = None) -> list[str]:
    if not isinstance(value, list):
        raise _InvalidSnapshot
    if any(not isinstance(item, str) or not item.strip() or len(item) > 2000 for item in value):
        raise _InvalidSnapshot
    if len(set(value)) != len(value) or (allowed is not None and not set(value) <= allowed):
        raise _InvalidSnapshot
    return cast(list[str], value)


def _no_link(path: Path) -> None:
    info = path.lstat()
    # Windows junctions and other reparse points must not become data sources.
    reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & reparse_point:
        raise _InvalidSnapshot


@dataclass(frozen=True)
class _Snapshot:
    release: dict[str, Any]
    domains: dict[str, dict[str, Any]]
    release_sha256: str


class InstructionsProvider:
    """Read reviewed package data, with one atomic last-known-good snapshot.

    ``root`` is a local deployment/test injection point, never an MCP argument.
    All data filenames are fixed by this library. Readers get deep copies and
    cannot modify shared state. Reload failure marks the provider degraded and
    retains the entire prior snapshot; initial failure raises a sanitized error.
    """

    def __init__(self, root: Path | None = None) -> None:
        self._root = root if root is not None else Path(__file__).with_name("data")
        self._lock = threading.RLock()
        self._reload_lock = threading.Lock()
        self._snapshot: _Snapshot | None = None
        self._error: str | None = None
        if not self.reload():
            raise InstructionsUnavailable("instructions_snapshot_unavailable") from None

    def _read(self, relative: str) -> bytes:
        _no_link(self._root)
        parts = Path(relative).parts
        current = self._root
        for part in parts:
            if part in {".", ".."}:
                raise _InvalidSnapshot
            current = current / part
            _no_link(current)
        initial = current.stat()
        if not stat.S_ISREG(initial.st_mode) or initial.st_size > MAX_FILE_BYTES:
            raise _InvalidSnapshot
        content = current.read_bytes()
        final = current.lstat()
        _no_link(current)
        if len(content) > MAX_FILE_BYTES or (
            initial.st_dev,
            initial.st_ino,
            initial.st_mtime_ns,
            initial.st_size,
        ) != (final.st_dev, final.st_ino, final.st_mtime_ns, final.st_size):
            raise _InvalidSnapshot
        return content

    def _load(self) -> _Snapshot:
        original_release = self._read("release.json")
        release = _object(_json(original_release), _RELEASE_KEYS)
        if type(release["schema_version"]) is not int or release["schema_version"] != 1:
            raise _InvalidSnapshot
        for key in (
            "instructions_version",
            "contract_version",
            "plugin_version",
            "minimum_plugin_version",
        ):
            _Version.parse(release[key])
        if _Version.parse(release["contract_version"]).core[0] != SUPPORTED_CONTRACT_MAJOR:
            raise _InvalidSnapshot
        if _Version.parse(release["plugin_version"]) < _Version.parse(
            release["minimum_plugin_version"]
        ):
            raise _InvalidSnapshot
        _iso_date(release["updated_at"])
        domain_hashes = _object(release["domains"], set(DOMAINS))
        changes = _object(release["changes"], _CHANGES)
        for descriptions in changes.values():
            _strings(descriptions)
        domains: dict[str, dict[str, Any]] = {}
        for domain in DOMAINS:
            hashes = _object(domain_hashes[domain], {"metadata_sha256", "content_sha256"})
            metadata_content = self._read(f"domains/{domain}.json")
            text_content = self._read(f"domains/{domain}.md")
            for content, key in (
                (metadata_content, "metadata_sha256"),
                (text_content, "content_sha256"),
            ):
                expected = hashes[key]
                if not isinstance(expected, str) or not re.fullmatch("[0-9a-f]{64}", expected):
                    raise _InvalidSnapshot
                if hashlib.sha256(content).hexdigest() != expected:
                    raise _InvalidSnapshot
            metadata = _object(_json(metadata_content), _DOMAIN_KEYS)
            if metadata["dominio"] != domain:
                raise _InvalidSnapshot
            _Version.parse(metadata["version"])
            _iso_date(metadata["updated_at"])
            compatibility = _object(metadata["compatibility"], _COMPATIBILITY_KEYS)
            for key, release_key in (
                ("mcp_contract_version", "contract_version"),
                ("minimum_plugin_version", "minimum_plugin_version"),
                ("recommended_plugin_version", "plugin_version"),
            ):
                if compatibility[key] != release[release_key]:
                    raise _InvalidSnapshot
            permissions = _object(metadata["permissions"], {"capabilities", "processes"})
            _strings(permissions["capabilities"], {"consultar", "decidir_chat"})
            _strings(permissions["processes"], set(PROCESS_TYPES))
            text = text_content.decode("utf-8")
            if not text.strip():
                raise _InvalidSnapshot
            domains[domain] = {**metadata, "instructions": text}
        if self._read("release.json") != original_release:
            raise _InvalidSnapshot
        return _Snapshot(release, domains, hashlib.sha256(original_release).hexdigest())

    def reload(self) -> bool:
        """Publish only a complete valid snapshot; failures keep the old one."""
        with self._reload_lock:
            try:
                snapshot = self._load()
            except (OSError, ValueError, TypeError, KeyError, RecursionError):
                with self._lock:
                    self._error = "instructions_snapshot_invalid"
                return False
            with self._lock:
                self._snapshot = snapshot
                self._error = None
            return True

    def _current(self) -> _Snapshot:
        if self._snapshot is None:
            raise InstructionsUnavailable("instructions_snapshot_unavailable") from None
        return self._snapshot

    def domains(self) -> tuple[str, ...]:
        """Return the fixed allowlist, independent of caller identity."""
        return DOMAINS

    def get(self, domain: str) -> dict[str, Any]:
        """Return a defensive copy; the host must enforce declared permissions."""
        if domain not in DOMAINS:
            raise InvalidDomain("invalid_domain")
        with self._lock:
            return copy.deepcopy(self._current().domains[domain])

    def _metadata(self, snapshot: _Snapshot) -> dict[str, Any]:
        release = snapshot.release
        return {
            "provider_version": PROVIDER_VERSION,
            "instructions_version": release["instructions_version"],
            "mcp_contract_version": release["contract_version"],
            "minimum_plugin_version": release["minimum_plugin_version"],
            "recommended_plugin_version": release["plugin_version"],
            "updated_at": release["updated_at"],
            "versions_by_domain": {
                name: value["version"] for name, value in snapshot.domains.items()
            },
            "release_sha256": snapshot.release_sha256,
            "changes": copy.deepcopy(release["changes"]),
        }

    def metadata(self) -> dict[str, Any]:
        """Version data only: no filesystem paths, instructions, or caller state."""
        with self._lock:
            return self._metadata(self._current())

    def health(self) -> dict[str, Any]:
        """Expose degraded reloads even when the last valid content is usable."""
        with self._lock:
            snapshot = self._current()
            return {
                "status": "degraded" if self._error else "ok",
                "snapshot_available": True,
                "instructions_version": snapshot.release["instructions_version"],
                "release_sha256": snapshot.release_sha256,
                "error_code": self._error,
            }

    def check_version(
        self,
        client_plugin_version: str | None = None,
        client_contract_version: str | None = None,
    ) -> dict[str, Any]:
        """Report compatibility only from supplied, declared protocol versions.

        Omitted dimensions stay unknown unless another dimension proves an
        incompatibility. Plugins between the declared minimum and recommended versions are
        assessed; newer plugins remain unknown. Earlier major contracts require
        an explicit migration; identity fallback does not restore retired tools.
        Contract clients must share the current major and not
        require a future version. This does not establish installed-client identity,
        tool discovery, or schema synchronization, so refresh remains unknown.
        """
        with self._lock:
            snapshot = self._current()
            result = self._metadata(snapshot)
            release = snapshot.release
            minimum = _Version.parse(release["minimum_plugin_version"])
            current_contract = _Version.parse(release["contract_version"])
            plugin = self._dimension(
                client_plugin_version,
                minimum,
                is_contract=False,
                highest_assessed=_Version.parse(release["plugin_version"]),
            )
            contract = self._dimension(client_contract_version, current_contract, is_contract=True)
            values = (plugin["compatible"], contract["compatible"])
            compatible = False if False in values else (None if None in values else True)
            result.update(
                {
                    "compatible": compatible,
                    "manual_update_required": None if compatible is None else not compatible,
                    "compatibility": {"plugin": plugin, "contract": contract},
                    "refresh_tools_required": None,
                    "tools_refresh_note": (
                        "As ferramentas novas podem exigir atualização da conexão MCP; "
                        "versões declaradas não comprovam descoberta ou sincronização de schemas."
                    ),
                    "compatibility_note": (
                        "Resultado limitado ao protocolo declarado pelo cliente; não comprova "
                        "a versão instalada no ChatGPT nem aprovação operacional."
                    ),
                    "fallback_functions": ["meu_acesso", "get_operator_context"],
                }
            )
            return result

    @staticmethod
    def _dimension(
        value: str | None,
        supported: _Version,
        *,
        is_contract: bool,
        highest_assessed: _Version | None = None,
    ) -> dict[str, Any]:
        if value is None:
            return {"client_version": None, "compatible": None, "reason": "client_version_unknown"}
        try:
            parsed = _Version.parse(value)
        except ValueError:
            return {"client_version": None, "compatible": False, "reason": "invalid_version"}
        if not is_contract and highest_assessed is not None and parsed > highest_assessed:
            return {
                "client_version": value,
                "compatible": None,
                "reason": "client_version_not_assessed",
            }
        compatible = (
            parsed.core[0] == supported.core[0] and parsed <= supported
            if is_contract
            else parsed >= supported
        )
        return {
            "client_version": value,
            "compatible": compatible,
            "reason": "declared_version_supported"
            if compatible
            else "declared_version_unsupported",
        }
