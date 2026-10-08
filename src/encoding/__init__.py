"""Encoding: simple Base64 file encoding and decoding utilities."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

__version__ = "1.0.0"


def encode(filename: PathLike) -> bytes:
    """Return the Base64 representation of *filename* as bytes.

    Base64 is encoding, not encryption. It does not provide confidentiality.
    """
    path = Path(filename)
    return base64.b64encode(path.read_bytes())


def decode(filename: PathLike) -> bytes:
    """Return the decoded bytes stored in a Base64-encoded file."""
    path = Path(filename)
    return base64.b64decode(path.read_bytes(), validate=True)


def encode_bytes(data: bytes) -> bytes:
    """Base64-encode bytes."""
    return base64.b64encode(data)


def decode_bytes(data: bytes) -> bytes:
    """Base64-decode bytes and reject invalid Base64 input."""
    return base64.b64decode(data, validate=True)


__all__ = [
    "encode",
    "decode",
    "encode_bytes",
    "decode_bytes",
    "__version__",
]
