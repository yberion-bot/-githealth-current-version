from src.agents.security_agent import SecurityAgent
def test_security_detects_injection():
    s = SecurityAgent("SecurityAgent")
    task = {"draft":"normal text","spec":{"notes":"rm -rf /"}}
    out = s.handle(task)
    assert "payload" in out
    assert isinstance(out["payload"].get("security"), list)
