from typing import List, Dict
import datetime, hashlib
class MemorySummarizer:
    def __init__(self, checkpoint_interval: int = 5):
        self.checkpoint_interval = checkpoint_interval
        self.task_count = 0
        self.checkpoints: List[Dict] = []
    def summarize_conversation(self, messages: List[str]) -> str:
        if not messages:
            return ""
        first = messages[0]
        last = messages[-1]
        tokens = " ".join(messages).split()
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        top_tokens = sorted(freq.items(), key=lambda x: -x[1])[:5]
        top = " ".join([t for t,_ in top_tokens])
        summary = f"CHKPT {datetime.datetime.utcnow().isoformat()} | first: {first[:80]} | last: {last[:80]} | top: {top}"
        return summary
    def ingest_and_maybe_checkpoint(self, messages: List[str]) -> Dict:
        self.task_count += 1
        result = {"checkpoint_created": False, "summary": None}
        if self.task_count % self.checkpoint_interval == 0:
            summary = self.summarize_conversation(messages)
            ckid = hashlib.sha1(summary.encode()).hexdigest()[:8]
            checkpoint = {"id": ckid, "summary": summary, "created_at": datetime.datetime.utcnow().isoformat()}
            self.checkpoints.append(checkpoint)
            result["checkpoint_created"] = True
            result["summary"] = summary
        return result
    def list_checkpoints(self) -> List[Dict]:
        return list(self.checkpoints)
