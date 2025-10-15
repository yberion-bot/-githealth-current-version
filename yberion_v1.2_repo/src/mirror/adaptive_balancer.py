from typing import Dict, List, Any
class AdaptiveTaskBalancer:
    def __init__(self):
        self.priority_map = {"critical": 100, "high": 75, "medium": 50, "low": 25}
    def score_agent_priority(self, task: Dict[str,Any], agent_name: str) -> float:
        base = self.priority_map.get(task.get("requirements", {}).get("priority", "medium"), 50)
        latency_need = task.get("requirements", {}).get("latency_p95_ms", 1000)
        latency_score = max(0, (2000 - latency_need) / 20)
        agent_boost = 0
        if agent_name.lower() in ["coder", "architect"]:
            agent_boost = 15
        return base + latency_score + agent_boost
    def create_routing(self, task: Dict[str,Any], candidate_agents: List[str]) -> List[Dict]:
        scored = []
        for a in candidate_agents:
            s = self.score_agent_priority(task, a)
            scored.append((a, s))
        scored.sort(key=lambda x: -x[1])
        routing = [{"agent": a, "score": s} for a,s in scored]
        return routing
