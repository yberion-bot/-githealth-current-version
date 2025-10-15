from src.mirror.infinity_protocol import InfinityProtocolController
def test_auto_deactivate():
    c = InfinityProtocolController(max_cycles=2)
    c.activate()
    r1 = c.tick()
    r2 = c.tick()
    assert r2.get("deactivate") is True
    assert c.active is False
