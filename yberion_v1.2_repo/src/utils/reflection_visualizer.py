from typing import List, Dict
import json, datetime
def build_reflection_timeline(reflection_logs: List[Dict]) -> str:
    lines = []
    for entry in reflection_logs:
        t = entry.get("time", datetime.datetime.utcnow().isoformat())
        s = entry.get("summary", "")
        lines.append(f"{t} | {s}")
    return "\n".join(lines)
def export_reflection_json(reflection_logs: List[Dict]) -> str:
    return json.dumps({"reflections": reflection_logs}, indent=2)
