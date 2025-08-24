from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from ..responses import ElementalResponse

class EchoFunction(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        super().__init__(FunctionCharacteristics(
            name="Echo",
            description="Echoes input parameters.",
            role=RoleInProcess.BUSINESS_ACTION,
            sync=SyncType.SYNC,
            resource_type=ResourceType.CPU,
            duration=DurationClass.SHORT,
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
