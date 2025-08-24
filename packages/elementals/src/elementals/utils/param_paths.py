from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, Tuple, Union
from pydantic import BaseModel

from ..params import ElementalParams


PathLike = str


def _is_path_expr(value: Any) -> bool:
    """Return True if value is a string path expression like "$params.a[0]"."""
    return isinstance(value, str) and value.strip().startswith("$")


def _tokenize(path: str) -> List[Union[str, int]]:
    """Tokenize a dotted/bracket path like "params.a[0].b" -> ["params", "a", 0, "b"]."""
    raw = path.lstrip("$").strip()
    if not raw:
        return []
    tokens: List[Union[str, int]] = []
    # split on '.' first, then extract bracketed indices
    for part in raw.split('.'):
        if not part:
            continue
        buf = ""
        i = 0
        while i < len(part):
            ch = part[i]
            if ch == '[':
                # flush accumulated buf as a key token
                if buf:
                    tokens.append(buf)
                    buf = ""
                # find closing ']'
                j = part.find(']', i + 1)
                if j == -1:
                    # unmatched bracket, treat rest as text
                    buf += part[i:]
                    break
                idx_text = part[i + 1:j].strip()
                # try parse int index, else treat as key
                if idx_text.isdigit() or (idx_text.startswith('-') and idx_text[1:].isdigit()):
                    tokens.append(int(idx_text))
                else:
                    tokens.append(idx_text)
                i = j + 1
                continue
            else:
                buf += ch
                i += 1
        if buf:
            tokens.append(buf)
    return tokens


_MISSING = object()


def _get_child(obj: Any, key: Union[str, int]) -> Any:
    """Get next child by key or index from dict/list/BaseModel/obj attributes.

    Returns _MISSING if the path cannot be resolved at this step.
    """
    if obj is None:
        return _MISSING
    # pydantic model: prefer attribute access
    if isinstance(obj, BaseModel):
        # model_dump for non-leaf is handled by caller; here we traverse
        try:
            if isinstance(key, int):
                # cannot index a model
                return _MISSING
            return getattr(obj, key)
        except AttributeError:
            data = obj.model_dump()  # fallback to dict
            return data.get(key, _MISSING)
    # dict-like
    if isinstance(obj, dict):
        return obj.get(key, _MISSING)
    # list/tuple
    if isinstance(obj, (list, tuple)):
        if isinstance(key, int) and -len(obj) <= key < len(obj):
            return obj[key]
        return _MISSING
    # generic object: try attribute then item access
    if isinstance(key, int):
        try:
            return obj[key]  # type: ignore[index]
        except Exception:
            return _MISSING
    try:
        return getattr(obj, key)
    except Exception:
        return _MISSING


def resolve_path(params: ElementalParams, path: PathLike, *, default: Any = _MISSING, dump_models: bool = True) -> Any:
    """Resolve a "$"-prefixed path against ElementalParams.

    Examples:
    - "$params.a" -> params.params["a"]
    - "$savepoint.items[1].val" -> params.savepoint["items"][1]["val"]
    - "$process.process_id" -> params.process.process_id

    If the path cannot be resolved, returns `default` if provided, else raises KeyError.
    If dump_models is True and the resolved value is a BaseModel, returns model_dump().
    """
    if not _is_path_expr(path):
        raise ValueError("Path expressions must start with '$'")
    current: Any = params
    for token in _tokenize(path):
        current = _get_child(current, token)
        if current is _MISSING:
            if default is _MISSING:
                raise KeyError(f"Path not found: {path}")
            return default
    if dump_models and isinstance(current, BaseModel):
        return current.model_dump()
    return current


def resolve_template(template: Any, params: ElementalParams, *, on_missing: str = "none", dump_models: bool = True) -> Any:
    """Resolve all "$"-prefixed string paths inside a nested template structure.

    - template may be a dict, list/tuple, or primitive.
    - strings starting with "$" are treated as ElementalParams paths and replaced with their values.
    - on_missing controls behavior for unresolved paths:
        - "none": replace with None
        - "keep": keep the original string path
        - "error": raise KeyError
    - dump_models: if a resolved value is a BaseModel, return model_dump().
    """
    def _resolve(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: _resolve(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_resolve(v) for v in value]
        if isinstance(value, tuple):
            return tuple(_resolve(v) for v in value)
        if _is_path_expr(value):
            if on_missing == "keep":
                default = value
            elif on_missing == "none":
                default = None
            elif on_missing == "error":
                default = _MISSING
            else:
                raise ValueError("on_missing must be one of: none, keep, error")
            try:
                return resolve_path(params, value, default=default, dump_models=dump_models)
            except KeyError:
                # only occurs when on_missing == "error"
                raise
        return value

    return _resolve(template)


def apply_path_map(path_map: Dict[str, Any], params: ElementalParams, *, on_missing: str = "none", dump_models: bool = True) -> Dict[str, Any]:
    """Alias for resolve_template when you know the root is a dict.

    Useful for mapping a flat or nested dict of output fields to ElementalParams paths.
    """
    result = resolve_template(path_map, params, on_missing=on_missing, dump_models=dump_models)
    if not isinstance(result, dict):
        raise TypeError("path_map must resolve to a dict")
    return result
