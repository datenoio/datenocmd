"""Serialization helpers for CLI output."""

from __future__ import annotations

import json
from typing import Any

import yaml


def to_plain(obj: Any) -> Any:
    """
    Convert SDK/Pydantic models to plain Python types suitable for JSON/YAML.
    Prevents YAML from emitting !!python/object tags.
    """
    if obj is None:
        return None

    # Pydantic v2
    model_dump = getattr(obj, "model_dump", None)
    if callable(model_dump):
        return to_plain(model_dump(mode="python", exclude_none=True))

    # Pydantic v1 fallback
    dict_method = getattr(obj, "dict", None)
    if callable(dict_method):
        return to_plain(dict_method(exclude_none=True))

    if isinstance(obj, dict):
        return {str(k): to_plain(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [to_plain(x) for x in obj]

    if isinstance(obj, (str, int, float, bool)):
        return obj

    return str(obj)


def render_output(data: Any, out_format: str) -> str:
    fmt = (out_format or "yaml").strip().lower()
    payload = to_plain(data)

    if fmt == "json":
        return json.dumps(payload, indent=4, ensure_ascii=False, default=str)

    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
