from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from ..responses import ElementalResponse
from configfuncs.loader import load_config

class EchoFunction(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        cfg = load_config().get("Echo", {})
        name = cfg.get("name", "Echo")
        desc = cfg.get("description", "Echoes input parameters.")
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
        return {
            "status": "success",
            "data": {"echo": params.params, "savepoint": params.savepoint},
            "meta": (params.meta.model_dump() if params.meta else None),
        }

if __name__ == "__main__":
    fn = EchoFunction()
    resp = fn.run(ElementalParams(params={"msg": "hello"}))
    import json
    print(json.dumps(resp, indent=2))
