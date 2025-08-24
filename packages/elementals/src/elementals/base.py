from dataclasses import dataclass
from typing import Any, Dict, Generic, Type, TypeVar
from pydantic import BaseModel
from .enums import RoleInProcess, SyncType, ResourceType, DurationClass
from .params import ElementalParams
from .responses import ElementalResponse

TOut = TypeVar("TOut")

@dataclass(frozen=True)
class FunctionCharacteristics:
    name: str
    description: str
    role: RoleInProcess
    sync: SyncType = SyncType.SYNC
    resource_type: ResourceType = ResourceType.CPU
    duration: DurationClass = DurationClass.SHORT

class ElementalFunction(Generic[TOut]):
    """Base class for all elemental functions."""
    characteristics: FunctionCharacteristics
    ResponseModel: Type[ElementalResponse[TOut]] = ElementalResponse

    def __init__(self, characteristics: FunctionCharacteristics):
        self.characteristics = characteristics

    def run(self, params: ElementalParams) -> Dict[str, Any]:
        """Override in subclasses to return a plain dict in ElementalResponse shape."""
        raise NotImplementedError("Subclasses must implement `run` to return a dict.")

    def run_dict(self, params: ElementalParams) -> Dict[str, Any]:
        """Execute and return a plain dict conforming to ElementalResponse schema.

        This preserves the existing run() contract while providing a standardized
        dict payload that callers can serialize or inspect without Pydantic models.
        """
        result = self.run(params)
        # If a Pydantic model is returned by legacy implementations, convert to dict.
        if isinstance(result, BaseModel):
            return result.model_dump()
        if isinstance(result, dict):
            return result
        raise TypeError(f"run() must return a dict, got: {type(result)!r}")
