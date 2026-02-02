"""I/O helpers for CLI commands."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Optional

import typer


def write_or_print(rendered: str, output: Optional[str]) -> None:
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
        print(f"Results saved to {output}")
    else:
        print(rendered)


def write_csv(headers: Iterable[str], rows: Iterable[Iterable[object]], output: str) -> None:
    with open(output, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(list(headers))
        writer.writerows(list(rows))
    print(f"Results saved to {output}")


def load_json_arg(value: str) -> object:
    """
    Load JSON from:
      - inline string: '{"a":1}'
      - file reference: '@path/to/file.json'
    """
    if not value:
        raise typer.BadParameter("Empty JSON input")

    raw = value.strip()
    if raw.startswith("@"):
        p = Path(raw[1:]).expanduser()
        if not p.exists():
            raise typer.BadParameter(f"JSON file not found: {p}")
        raw = p.read_text(encoding="utf-8").strip()

    try:
        import json

        return json.loads(raw)
    except Exception as e:
        raise typer.BadParameter(f"Invalid JSON: {e}") from e
