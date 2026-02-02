"""Search response helpers."""

from __future__ import annotations

from typing import Any


def extract_hits_list(data_dict: Any) -> list[dict]:
    """
    Extract list of hits from various SDK response shapes.
    Supports:
      - {"hits": {"hits": [ ... ]}}
      - {"hits": [ ... ]}
      - {"data": [ ... ]}
      - {"results": [ ... ]}
      - {"items": [ ... ]}
    """
    if not isinstance(data_dict, dict):
        return []

    hits = data_dict.get("hits")
    if isinstance(hits, dict):
        hh = hits.get("hits")
        if isinstance(hh, list):
            return [x for x in hh if isinstance(x, dict)]
        if isinstance(hh, dict) and isinstance(hh.get("hits"), list):
            return [x for x in hh["hits"] if isinstance(x, dict)]
    if isinstance(hits, list):
        return [x for x in hits if isinstance(x, dict)]

    data = data_dict.get("data")
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    for key in ("results", "items"):
        v = data_dict.get(key)
        if isinstance(v, list):
            return [x for x in v if isinstance(x, dict)]

    return []


def extract_doc_from_item(item: dict) -> dict:
    """
    Turn an item from hits/data into a flat document dict suitable for FlatDict.
    """
    if "_source" in item and isinstance(item["_source"], dict):
        return item["_source"]

    if "document" in item and isinstance(item["document"], dict):
        return item["document"]

    if "dataset" in item or "source" in item:
        return item

    return item
