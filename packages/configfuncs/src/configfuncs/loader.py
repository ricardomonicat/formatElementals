
from importlib import import_module
from pathlib import Path
from typing import Any, Dict
import yaml
import os


def load_config(path: str | Path | None = None) -> Dict[str, Any]:
    """Load the configFunctions.yaml as a dict.

    If path is None, loads from the customerfunctions package directory.
    """
    # Always load configFunctions.yaml from the root of the customerfunctions package (sibling to tasksFormats)
    current = Path(__file__).resolve()
    # Traverse up until we find the workspace root (contains both tasksFormats and customerfunctions)
    for parent in current.parents:
        if (parent / "customerfunctions" / "configFunctions.yaml").exists():
            yaml_path = parent / "customerfunctions" / "configFunctions.yaml"
            break
    else:
        raise FileNotFoundError("configFunctions.yaml not found in any parent directory's customerfunctions folder")
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_callable(entry: Dict[str, Any]):
    """Given an entry with module and class, import and return the class."""
    mod = import_module(entry["classModule"])
    return getattr(mod, entry["class"])  # type: ignore[no-any-return]


def get_function_class(name: str):
    """Return the function class for a given config name (e.g., 'Multiply')."""
    cfg = load_config()
    if name not in cfg:
        raise KeyError(f"Function '{name}' not found in configuration")
    return resolve_callable(cfg[name])


def get_function_instance(name: str):
    """Instantiate the function class defined in config by name."""
    cls = get_function_class(name)
    return cls()  # type: ignore[no-any-return]


def run_function(name: str, *, params: Dict[str, Any] | None = None,
                 savepoint: Dict[str, Any] | None = None,
                 process: Any | None = None,
                 environment: Any | None = None,
                 meta: Any | None = None) -> Dict[str, Any]:
    """Instantiate a configured function by name and run it, returning a dict.

    This imports ElementalParams lazily to avoid hard dependency at import time.
    """
    fn = get_function_instance(name)
    from elementals.params import ElementalParams  # lazy import to avoid cycles
    ep = ElementalParams(
        params=params or {}, savepoint=savepoint or {},
        process=process, environment=environment, meta=meta
    )
    # All functions return dicts in this project
    return fn.run(ep)  # type: ignore[no-any-return]
