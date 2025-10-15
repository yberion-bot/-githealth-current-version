import time, uuid
from typing import List, Dict, Any
class MasterKey:
    def __init__(self):
        self._store: Dict[str, Dict[str,Any]] = {}
    def issue(self, agent_name: str, scopes: List[str], ttl_s: int = 300) -> str:
        token = f"{agent_name}:{uuid.uuid4().hex}"
        self._store[token] = {"agent":agent_name, "scopes":scopes, "expiry": int(time.time()) + ttl_s}
        return token
    def validate(self, token: str, scope: str) -> bool:
        info = self._store.get(token)
        if not info:
            return False
        if int(time.time()) > info["expiry"]:
            return False
        return scope in info["scopes"]
