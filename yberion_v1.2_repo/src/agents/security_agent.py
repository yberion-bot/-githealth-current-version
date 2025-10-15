from ..yberion_nexus import SubAgent
from typing import Dict, Any
import re
INJECTION_PATTERNS = [
    r"\brm -rf\b",
    r"\bexec\b",
    r"\bshutdown\b",
    r"\\x[0-9a-fA-F]{2}",
    r"```.*?```"
]
class SecurityAgent(SubAgent):
    def handle(self, task: Dict[str, Any]) -> Dict[str, Any]:
        suspect = []
        text_fields = []
        for k in ["draft", "spec"]:
            v = task.get(k)
            if isinstance(v, str):
                text_fields.append(v)
            elif isinstance(v, dict):
                text_fields.append(str(v))
        joined = " ".join(text_fields)
        for pat in INJECTION_PATTERNS:
            if re.search(pat, joined, flags=re.IGNORECASE | re.DOTALL):
                suspect.append(f"pattern:{pat}")
        urls = re.findall(r"https?://\S+", joined)
        if len(urls) > 5:
            suspect.append("many_urls")
        actions = []
        if suspect:
            actions.append({"action":"quarantine","reason":"suspicious_patterns","details":suspect})
        else:
            actions.append({"action":"clear","reason":"no_detected_issues"})
        return {"agent": self.name, "confidence": 0.95 if not suspect else 0.6,
                "explanations": f"security audit run, suspect_count={len(suspect)}",
                "payload": {"security": actions}}
