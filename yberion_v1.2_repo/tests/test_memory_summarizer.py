from src.mirror.memory_summarizer import MemorySummarizer
def test_checkpoint_creation():
    ms = MemorySummarizer(checkpoint_interval=2)
    msgs = ["hello world","second","third"]
    r1 = ms.ingest_and_maybe_checkpoint(msgs[:1])
    assert r1["checkpoint_created"] is False
    r2 = ms.ingest_and_maybe_checkpoint(msgs)
    assert isinstance(ms.list_checkpoints(), list)
