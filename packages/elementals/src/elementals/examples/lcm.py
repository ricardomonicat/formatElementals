from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from configfuncs.loader import load_config
import math

class LCMFunction(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        cfg = load_config().get("LCM", {})
        name = cfg.get("name", "LCM")
        desc = cfg.get("description", "Calculate the least common multiple of two numbers")
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
                "error": {"code": "missing_param", "message": "Parameters 'a' and 'b' are required."},
                "data": None,
                "meta": (params.meta.model_dump() if params.meta else None),
            }
        try:
            lcm = abs(a * b) // math.gcd(a, b)
            return {
                "status": "success",
                "data": {"lcm": lcm},
                "meta": (params.meta.model_dump() if params.meta else None),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {"code": "exception", "message": str(e)},
                "data": None,
                "meta": (params.meta.model_dump() if params.meta else None),
            }
