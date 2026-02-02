"""
Dateno CLI compatibility wrapper.

This module keeps the legacy entrypoint working while the CLI
is implemented in `dateno_cmd.cli`.
"""

from __future__ import annotations

from dateno_cmd.cli import app, main

__all__ = ["app", "main"]


if __name__ == "__main__":
    main()
