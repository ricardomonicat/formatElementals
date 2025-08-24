from typing import Any, Dict
from ..base import ElementalFunction, FunctionCharacteristics
from ..enums import RoleInProcess, SyncType, ResourceType, DurationClass
from ..params import ElementalParams
from ..responses import ElementalResponse

class MultiplyFunction(ElementalFunction[Dict[str, Any]]):
    def __init__(self):
        super().__init__(FunctionCharacteristics(
            name="Multiply",
            description="Receives two numbers and returns them along with their multiplication.",
            role=RoleInProcess.BUSINESS_ACTION,
            sync=SyncType.SYNC,
            resource_type=ResourceType.CPU,
            duration=DurationClass.SHORT,
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
