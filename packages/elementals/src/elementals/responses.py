from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class ErrorItem(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ElementalResponse(BaseModel, Generic[T]):
    status: str = Field(..., description="success | error")
    data: Optional[T] = None
    error: Optional[ErrorItem] = None
    meta: Optional[Dict[str, Any]] = None
