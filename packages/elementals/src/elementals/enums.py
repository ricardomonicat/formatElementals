from enum import Enum

class RoleInProcess(str, Enum):
    BUSINESS_ACTION = "business_action"
    RETRY_ANALYSIS = "retry_analysis"
    SPECIAL_PARAM_VALIDATION = "special_param_validation"
    BUSINESS_RULE_VALIDATION = "business_rule_validation"
    COMPLETE_INCOMPLETE_ACTION = "complete_incomplete_action"
    ROLLBACK = "rollback"
    REBUILD_RESPONSE = "rebuild_response"

class SyncType(str, Enum):
    SYNC = "sync"
    ASYNC = "async"

class ResourceType(str, Enum):
    CPU = "cpu"
    IO = "io"
    NETWORK = "network"
    EXTERNAL_API = "external_api"

class DurationClass(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
