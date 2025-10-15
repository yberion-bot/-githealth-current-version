from src.mirror.adaptive_balancer import AdaptiveTaskBalancer
def test_routing_scores():
    bal = AdaptiveTaskBalancer()
    task = {"requirements":{"priority":"high","latency_p95_ms":300}}
    routing = bal.create_routing(task, ["Coder","Scribe","Architect"])
    assert isinstance(routing, list)
