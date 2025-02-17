from typing import List, Dict, Any
from dataclasses import dataclass, field 


@dataclass
class EmailState:
    emails: List[Dict[str, Any]] = field(default_factory=list)
    history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    current_email: Dict[str, Any] = field(default_factory=dict)

