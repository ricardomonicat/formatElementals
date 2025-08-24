from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Meta(BaseModel):
    call_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    config: Dict[str, Any] = {}

class ProcessInfo(BaseModel):
    process_id: str
    version: int = 1
    run_id: Optional[str] = None
    source_system: Optional[str] = None

class Environment(BaseModel):
    name: str = "dev"
    debug: bool = False
    region: Optional[str] = None
    max_retries: int = 0

class ElementalParams(BaseModel):
    params: Dict[str, Any] = {}
    savepoint: Dict[str, Any] = {}
    process: Optional[ProcessInfo] = None
    environment: Optional[Environment] = None
    meta: Optional[Meta] = None
