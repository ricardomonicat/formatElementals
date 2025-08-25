#!/usr/bin/env python
"""
Scaffold a new YAML-driven ElementalFunction and its test.

Usage (from repo root):
  venv/Scripts/python scripts/scaffold_function.py --name Sum --description "Sum two numbers"

This will:
  - Append an entry to packages/configfuncs/src/configfuncs/configFunctions.yaml
  - Create packages/elementals/src/elementals/examples/sum.py
  - Create packages/elementals/tests/test_sum.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = REPO_ROOT.parent / "customerfunctions" / "configFunctions.yaml"
EXAMPLES_DIR = REPO_ROOT / "packages" / "elementals" / "src" / "elementals" / "examples"
TESTS_DIR = REPO_ROOT / "packages" / "elementals" / "tests"


def to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_pascal(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name.strip())
    return "".join(p.capitalize() for p in parts if p)


def load_yaml() -> Dict:
    if YAML_PATH.exists():
        with YAML_PATH.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                raise ValueError("configFunctions.yaml must contain a mapping at the top level")
            return data
    return {}


def save_yaml(data: Dict) -> None:
    YAML_PATH.parent.mkdir(parents=True, exist_ok=True)
    with YAML_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=True, allow_unicode=True)


TEMPLATE_MODULE = """from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from configfuncs.loader import load_config


class {ClassName}Function(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        cfg = load_config().get("{ConfigName}", {{}})
        name = cfg.get("name", "{DefaultName}")
        desc = cfg.get("description", "{DefaultDesc}")
        role = RoleInProcess(cfg.get("role", RoleInProcess.BUSINESS_ACTION.value))
        sync = SyncType(cfg.get("sync", SyncType.SYNC.value))
        resource = ResourceType(cfg.get("resource_type", ResourceType.CPU.value))
        duration = DurationClass(cfg.get("duration", DurationClass.SHORT.value))

        super().__init__(FunctionCharacteristics(
            name=name,
            description=desc,
            role=role,
            sync=sync,
            resource_type=resource,
            duration=duration,
        ))

    def run(self, params: ElementalParams) -> Dict[str, Any]:
        # TODO: implement logic; for now return a not_implemented error
        return {{
            "status": "error",
            "error": {{"code": "not_implemented", "message": "Function not implemented yet"}},
            "data": None,
            "meta": (params.meta.model_dump() if params.meta else None),
        }}
"""


TEMPLATE_TEST = """from elementals.params import ElementalParams
from elementals.examples.{module_name} import {ClassName}Function


def test_{module_name}_scaffold_runs_and_returns_dict():
    fn = {ClassName}Function()
    out = fn.run(ElementalParams(params={{}}))
    assert isinstance(out, dict)
    assert out.get("status") in ("success", "error")
"""


def main() -> None:
    p = argparse.ArgumentParser(description="Scaffold a new YAML-driven ElementalFunction")
    p.add_argument("--name", required=True, help="Function name (e.g., Sum or sum)")
    p.add_argument("--description", required=True, help="Human description")
    p.add_argument("--module", help="Module name override (default derived from name)")
    p.add_argument("--class-name", dest="class_name", help="Class name override (default <PascalName>Function)")
    p.add_argument("--force", action="store_true", help="Overwrite existing files if present")
    args = p.parse_args()

    cfg_name = to_pascal(args.name)
    module_name = to_snake(args.name)
    class_name = args.class_name or to_pascal(args.name)

    # 1) Update YAML
    data = load_yaml()
    if cfg_name in data:
        # keep existing and only ensure required keys exist
        entry = data[cfg_name] or {}
    else:
        entry = {}
    entry.update({
        "name": cfg_name,
        "description": args.description,
        "module": f"elementals.examples.{module_name}",
        "class": f"{class_name}Function",
        "enabled": True,
        "role": "business_action",
        "sync": "sync",
        "resource_type": "cpu",
        "duration": "short",
    })
    data[cfg_name] = entry
    save_yaml(data)

    # 2) Create module file
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    module_path = EXAMPLES_DIR / f"{module_name}.py"
    if module_path.exists() and not args.force:
        print(f"[skip] Module exists: {module_path}")
    else:
        content = TEMPLATE_MODULE.format(
            ClassName=class_name,
            ConfigName=cfg_name,
            DefaultName=cfg_name,
            DefaultDesc=args.description,
        )
        module_path.write_text(content, encoding="utf-8")
        print(f"[write] {module_path}")

    # 3) Create test file
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    test_path = TESTS_DIR / f"test_{module_name}.py"
    if test_path.exists() and not args.force:
        print(f"[skip] Test exists: {test_path}")
    else:
        tcontent = TEMPLATE_TEST.format(module_name=module_name, ClassName=class_name)
        test_path.write_text(tcontent, encoding="utf-8")
        print(f"[write] {test_path}")

    print("\nScaffold complete. Next:")
    print(" - Implement the run() method in the generated module")
    print(" - Run tests: venv\\Scripts\\pytest packages/elementals/tests/test_{}.py -q".format(module_name))


if __name__ == "__main__":
    main()
