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
    def _with_id(doc: dict) -> dict:
        if doc.get("id") is not None:
            return doc
        hit_id = item.get("id")
        if hit_id is None:
            hit_id = item.get("_id")
        if hit_id is None:
            return doc
        if doc is item:
            doc["id"] = hit_id
            return doc
        merged = dict(doc)
        merged["id"] = hit_id
        return merged

    if "_source" in item and isinstance(item["_source"], dict):
        return _with_id(item["_source"])

    source = item.get("source")
    if isinstance(source, dict):
        # Pydantic SearchQueryResponse.Hit uses `source` for ES `_source`.
        if "dataset" in source or "source" in source or "resources" in source:
            return _with_id(source)

    if "document" in item and isinstance(item["document"], dict):
        return _with_id(item["document"])

    if "dataset" in item or "source" in item:
        return _with_id(item)

    return _with_id(item)
