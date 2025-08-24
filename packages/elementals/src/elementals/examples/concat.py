from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from configfuncs.loader import load_config


class ConcatFunction(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        cfg = load_config().get("Concat", {})
        name = cfg.get("name", "Concat")
        desc = cfg.get("description", "Receives two texts and returns them along with their concatenation.")
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
        t1 = params.params.get("text1")
        t2 = params.params.get("text2")
        if t1 is None or t2 is None:
            return {
                "status": "error",
                "error": {"code": "missing_param", "message": "Both 'text1' and 'text2' must be provided."},
                "data": None,
                "meta": (params.meta.model_dump() if params.meta else None),
            }
        concat = f"{t1}{t2}"
        return {
            "status": "success",
            "data": {"text1": t1, "text2": t2, "concat": concat},
            "meta": (params.meta.model_dump() if params.meta else None),
        }
