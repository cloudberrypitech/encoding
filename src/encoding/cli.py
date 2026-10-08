"""Command-line interface for encoding."""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path
from typing import BinaryIO, TextIO


def _open_input(filename: str) -> BinaryIO:
    return sys.stdin.buffer if filename == "-" else open(filename, "rb")


def _open_output(filename: str) -> BinaryIO:
    return sys.stdout.buffer if filename == "-" else open(filename, "wb")


def _default_output(source: str, operation: str) -> str:
    if source == "-":
        return "-"
    path = Path(source)
    if operation == "encode":
        return str(path.with_name(path.name + ".b64"))
    if path.name.endswith(".b64"):
        return str(path.with_name(path.name[:-4]))
    return str(path.with_name(path.name + ".decoded"))


def encode_file(source: str, destination: str) -> None:
    with _open_input(source) as input_file:
        data = input_file.read()
    encoded = base64.b64encode(data)
    with _open_output(destination) as output_file:
        output_file.write(encoded)


def decode_file(source: str, destination: str) -> None:
    with _open_input(source) as input_file:
        data = input_file.read()
    decoded = base64.b64decode(data, validate=True)
    with _open_output(destination) as output_file:
        output_file.write(decoded)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="encoding",
        description="Encode and decode files using Base64.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("encode", "decode"):
        sub = subparsers.add_parser(
            command,
            help=f"Base64-{command} a file.",
        )
        sub.add_argument(
            "input",
            metavar="INPUT",
            help="Input file, or '-' for standard input.",
        )
        sub.add_argument(
            "-o",
            "--output",
            metavar="OUTPUT",
            help="Output file, or '-' for standard output.",
        )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    output = args.output or _default_output(args.input, args.command)

    try:
        if args.command == "encode":
            encode_file(args.input, output)
        else:
            decode_file(args.input, output)
    except FileNotFoundError as exc:
        print(f"encoding: file not found: {exc.filename}", file=sys.stderr)
        return 2
    except PermissionError as exc:
        print(f"encoding: permission denied: {exc.filename}", file=sys.stderr)
        return 2
    except (ValueError, base64.binascii.Error):
        print("encoding: input is not valid Base64", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"encoding: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
