"""SDK helper utilities."""

from __future__ import annotations


def call_sdk_flexible(fn, **kwargs):
    """
    На случай несовпадения имени параметра в SDK (бывает между версиями).
    Пробуем разные варианты, чтобы не стопориться.
    """
    try:
        return fn(**kwargs)
    except TypeError:
        alt_maps = [
            {"body": "request"},
            {"body": "query"},
            {"entry_id": "id"},
        ]
        for m in alt_maps:
            alt = dict(kwargs)
            changed = False
            for src, dst in m.items():
                if src in alt and dst not in alt:
                    alt[dst] = alt.pop(src)
                    changed = True
            if not changed:
                continue
            try:
                return fn(**alt)
            except TypeError:
                continue
        raise
