from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from configfuncs.loader import load_config

class MultiplyFunction(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        cfg = load_config().get("Multiply", {})
        # Map YAML values to enum instances with sensible defaults
        name = cfg.get("name", "Multiply")
        desc = cfg.get("description", "Receives two numbers and returns them along with their multiplication.")
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
        a = params.params.get("a")
        b = params.params.get("b")
        if a is None or b is None:
            return {
                "status": "error",
                "error": {"code": "missing_param", "message": "Both 'a' and 'b' must be provided."},
                "data": None,
                "meta": (params.meta.model_dump() if params.meta else None),
            }
        result = a * b
        return {
            "status": "success",
            "data": {"a": a, "b": b, "product": result},
            "meta": (params.meta.model_dump() if params.meta else None),
        }
