from __future__ import annotations

from typing import Any, Mapping, Sequence
from ..params import ElementalParams


def _get_attr_or_key(obj: Any, key: str) -> Any:
    """Get obj[key] or getattr(obj, key) if possible; return KeyError on miss.

    Supports Pydantic models and plain dict-like objects.
    """
    # Dict-like
    if isinstance(obj, Mapping) and key in obj:
        return obj[key]
    # Pydantic BaseModel or any object with attribute
    if hasattr(obj, key):
        return getattr(obj, key)
    raise KeyError(key)


def _resolve_path(root: Any, path: str) -> Any:
    """Resolve a dotted/bracket path like 'params.items[0].id' from root.

    - Dots navigate attributes/keys.
    - Brackets [index] access list indices.
    Returns None if any step is missing/out-of-range.
    """
    cur = root
    token = ""
    i = 0
    while i < len(path):
        ch = path[i]
        if ch == ".":
            if token:
                try:
                    cur = _get_attr_or_key(cur, token)
                except KeyError:
                    return None
                token = ""
            i += 1
            continue
        if ch == "[":
            # commit prior token first
            if token:
                try:
                    cur = _get_attr_or_key(cur, token)
                except KeyError:
                    return None
                token = ""
            # parse index until ]
            j = path.find("]", i + 1)
            if j == -1:
                return None
            idx_str = path[i + 1 : j].strip()
            try:
                idx = int(idx_str)
            except ValueError:
                return None
            if isinstance(cur, Sequence) and not isinstance(cur, (str, bytes, bytearray)):
                if 0 <= idx < len(cur):
                    cur = cur[idx]
                else:
                    return None
            else:
                return None
            i = j + 1
            continue
        token += ch
        i += 1
    # commit remaining token
    if token:
        try:
            cur = _get_attr_or_key(cur, token)
        except KeyError:
            return None
    return cur


def resolve_path(params: ElementalParams, path: str) -> Any:
    """Resolve a path starting at ElementalParams; path can start with top fields.

    Examples:
    - 'params.a'
    - 'savepoint.step'
    - 'meta.timestamp'
    - 'params.items[0].id'
    If the string starts with '$', that prefix is ignored (convenience in templates).
    Returns None if not found.
    """
    if path.startswith("$"):
        path = path[1:]
    return _resolve_path(params, path)


def render_template(params: ElementalParams, template: Any) -> Any:
    """Render a nested template by replacing '$path' strings with resolved values.

    - Dicts: recurse into values
    - Lists/Tuples: recurse into items, return same type
    - Strings: if start with '$', resolve path; otherwise keep literal
    - Others: returned as-is
    """
    if isinstance(template, dict):
        return {k: render_template(params, v) for k, v in template.items()}
    if isinstance(template, list):
        return [render_template(params, v) for v in template]
    if isinstance(template, tuple):
        return tuple(render_template(params, v) for v in template)
    if isinstance(template, str) and template.startswith("$"):
        return resolve_path(params, template)
    return template
