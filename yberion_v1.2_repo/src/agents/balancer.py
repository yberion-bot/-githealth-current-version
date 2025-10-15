from ..yberion_nexus import SubAgent
from typing import Dict, Any
class Balancer(SubAgent):
    def handle(self, task: Dict[str, Any]) -> Dict[str, Any]:
        draft = task.get("draft", "")
        tone_flag = "neutral"
        if any(word in draft.lower() for word in ["fail", "error", "problem"]):
            tone_flag = "caution"
        return {"agent": self.name, "confidence": 0.9, "explanations": f"tone {tone_flag}", "payload": {"tone": tone_flag}}
