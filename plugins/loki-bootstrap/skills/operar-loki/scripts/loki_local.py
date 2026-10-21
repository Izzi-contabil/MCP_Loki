# /// script
# requires-python = ">=3.11,<3.12"
# dependencies = [
#   "pypdf==6.14.2", "pypdfium2==5.12.1", "pillow==12.3.0",
#   "openpyxl==3.1.5", "xlrd==2.0.2", "defusedxml==0.7.1", "jsonschema==4.25.1",
#   "rfc3339-validator==0.1.4",
# ]
# ///
"""Run through uv --locked --script; all business/MCP calls belong to the harness."""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

# The native plugin cache is immutable working code, not an output directory.
sys.dont_write_bytecode = True

from loki_readers.exchange import (  # noqa: E402
    csv_request,
    render_records,
    save_receipt,
    source_csv,
    validate_parameters,
)
from loki_readers.private import (  # noqa: E402
    ReadError,
    checked_bytes,
    private_directory,
    strict_json,
    write_bytes,
    write_json,
)
from loki_readers.readers import MAX_BYTES, read_document  # noqa: E402
from loki_readers.workspace import doctor, inventory  # noqa: E402


def load(path: Path) -> Any:
    return strict_json(checked_bytes(path, MAX_BYTES).decode("utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    read = commands.add_parser("read", help="Prepare local text/tables/images for the harness")
    read.add_argument("source", type=Path)
    read.add_argument("output", type=Path)
    read.add_argument("--encoding", default="utf-8-sig")
    read.add_argument("--pages")
    read.add_argument("--expected-sha256")
    digest = commands.add_parser("hash", help="Verify source bytes before preparing a request")
    digest.add_argument("source", type=Path)
    digest.add_argument("--expected-sha256")
    for name in ("inventory", "source-csv", "render-csv", "csv-request", "parameters"):
        command = commands.add_parser(name)
        command.add_argument("source", type=Path)
        command.add_argument("output", type=Path)
        if name == "render-csv":
            command.add_argument("--contract", type=Path, required=True)
        if name == "parameters":
            command.add_argument("--schema", type=Path, required=True)
            command.add_argument("--schema-pointer", default="")
        if name == "csv-request":
            command.add_argument(
                "--destination",
                choices=("case", "onboarding-source", "onboarding-csv"),
                required=True,
            )
            command.add_argument("--target", required=True)
            command.add_argument("--reference", default="")
            command.add_argument("--revision", type=int, default=1)
    diagnostic = commands.add_parser("doctor")
    diagnostic.add_argument("output", type=Path)
    receipt = commands.add_parser("receipt")
    receipt.add_argument("request", type=Path)
    receipt.add_argument("response", type=Path)
    receipt.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "read":
            result = read_document(
                args.source,
                args.output,
                args.encoding,
                pages=args.pages,
                expected_sha256=args.expected_sha256,
            )
            print(
                json.dumps(
                    {
                        "manifest": str(args.output.absolute() / "manifest.json"),
                        "sha256": result["source"]["sha256"],
                        "units": len(result["units"]),
                        "status": result["status"],
                    }
                )
            )
        elif args.command == "hash":
            print(
                json.dumps(
                    {
                        "sha256": hashlib.sha256(
                            checked_bytes(args.source, MAX_BYTES, args.expected_sha256)
                        ).hexdigest()
                    }
                )
            )
        elif args.command == "doctor":
            print(json.dumps(doctor(args.output)))
        elif args.command == "inventory":
            result = inventory(args.source, args.output)
            print(
                json.dumps(
                    {
                        "inventory": str(args.output.absolute() / "inventory.json"),
                        "files": len(result["files"]),
                        "status": result["status"],
                    }
                )
            )
        elif args.command == "receipt":
            print(json.dumps(save_receipt(args.request, args.response, args.output)))
        elif args.command in {"render-csv", "source-csv"}:
            data = load(args.source)
            if args.command == "render-csv":
                contract = load(args.contract)
                content = render_records(data, contract.get("batch_csv", contract))
            else:
                content = source_csv(data)
            output = private_directory(args.output)
            write_bytes(output / "reading.csv", content)
            write_json(output / "local-provenance.json", data)
            print(
                json.dumps(
                    {
                        "csv": str(output / "reading.csv"),
                        "content_hash": hashlib.sha256(content).hexdigest(),
                        "status": "prepared_not_sent",
                    }
                )
            )
        elif args.command == "csv-request":
            request = csv_request(
                args.source,
                args.destination,
                args.target,
                reference=args.reference,
                revision=args.revision,
            )
            output = private_directory(args.output)
            write_json(output / "request.json", request)
            print(
                json.dumps(
                    {
                        "request": str(output / "request.json"),
                        "tool": request["tool"],
                        "content_hash": request["content_hash"],
                        "status": request["state"],
                    }
                )
            )
        elif args.command == "parameters":
            schema = load(args.schema)
            if args.schema_pointer:
                if not args.schema_pointer.startswith("/"):
                    raise ReadError("invalid_schema_pointer")
                for key in args.schema_pointer[1:].split("/"):
                    schema = schema[key.replace("~1", "/").replace("~0", "~")]
            data = validate_parameters(load(args.source), schema)
            output = private_directory(args.output)
            write_json(output / "parameters.json", data)
            print(
                json.dumps(
                    {"parameters": str(output / "parameters.json"), "status": "validated_not_sent"}
                )
            )
        return 0
    except Exception as error:
        code = str(error) if isinstance(error, ReadError) else "local_operation_failed"
        print(json.dumps({"error": code}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
