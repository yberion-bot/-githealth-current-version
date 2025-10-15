import datetime
class TelemetryExporter:
    def __init__(self):
        self.registry = {}
    def record_task(self, task):
        tid = task.get('trace_id', None)
        if not tid:
            return
        self.registry[tid] = {
            'latency': task.get('metrics', {}).get('latency_ms', 0),
            'tokens': task.get('metrics', {}).get('token_usage', 0),
            'errors': task.get('metrics', {}).get('errors', 0),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
    def snapshot(self, task):
        tid = task.get('trace_id')
        return self.registry.get(tid, {})
    def export_prometheus(self):
        lines = []
        for tid, d in self.registry.items():
            lines.append(f'yb_task_latency{{trace_id="{tid}"}} {d["latency"]}')
            lines.append(f'yb_token_usage{{trace_id="{tid}"}} {d["tokens"]}')
        return "\n".join(lines)
