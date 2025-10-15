import time, uuid, threading
from typing import Dict, Any, List
from plugins.masterkey import MasterKey
from mirror.memory_summarizer import MemorySummarizer
from mirror.adaptive_balancer import AdaptiveTaskBalancer
from mirror.infinity_protocol import InfinityProtocolController

def now_ms():
    return int(time.time()*1000)

masterkey = MasterKey()

class SubAgent:
    def __init__(self, name:str):
        self.name = name
        self.token = None
    def set_token(self, token:str):
        self.token = token
    def handle(self, task: Dict[str,Any]) -> Dict[str,Any]:
        raise NotImplementedError()

class NexusOrchestrator:
    def __init__(self, timeout_s=6.0):
        self.agents: Dict[str, SubAgent] = {}
        self.timeout_s = timeout_s
        self.audit_log: List[Dict] = []
        self.memory = MemorySummarizer(checkpoint_interval=5)
        self.balancer = AdaptiveTaskBalancer()
        self.infinity = InfinityProtocolController(max_cycles=3)

    def register(self, agent:SubAgent, scopes:List[str]=None):
        self.agents[agent.name] = agent
        if scopes:
            token = masterkey.issue(agent.name, scopes, ttl_s=600)
            agent.set_token(token)

    def run_task_sync(self, task: Dict[str,Any], agent_order: List[str]=None) -> Dict[str,Any]:
        roles = agent_order or list(self.agents.keys())
        roles = [r['agent'] for r in self.balancer.create_routing(task, roles)]
        responses = {}
        start = now_ms()
        threads = []
        lock = threading.Lock()

        def call_agent(name):
            agent = self.agents[name]
            call_start = now_ms()
            try:
                out = agent.handle(task)
            except Exception as e:
                out = {"agent":name,"confidence":0.0,"explanations":f"exception:{e}","payload":{}}
            call_end = now_ms()
            out.setdefault("_meta", {})["_took_ms"] = call_end - call_start
            with lock:
                responses[name] = out

        for n in roles:
            t = threading.Thread(target=call_agent, args=(n,), daemon=True)
            threads.append(t); t.start()

        deadline = time.time() + self.timeout_s
        for t in threads:
            remaining = deadline - time.time()
            if remaining > 0:
                t.join(remaining)

        end = now_ms()
        trace = {"trace_id": task.get("trace_id", uuid.uuid4().hex), "start": start, "end": end, "duration_ms": end-start}
        self.audit_log.append({"trace": trace, "task": task, "responses": responses})
        agg = self.aggregate_responses(responses)
        msgs = [str(task.get('draft',''))] + [str(res.get('explanations','')) for res in responses.values()]
        self.memory.ingest_and_maybe_checkpoint(msgs)
        inf = self.infinity.tick()
        if inf.get("deactivate"):
            agg['_infinity_deactivated'] = True
        return {"trace": trace, "responses": responses, "aggregate": agg}

    def aggregate_responses(self, responses: Dict[str,Any]) -> Dict[str,Any]:
        artifacts = {}
        provenance = {}
        for name, r in responses.items():
            payload = r.get("payload", {})
            conf = r.get("confidence", 0)
            for k,v in payload.items():
                if isinstance(v, list):
                    artifacts.setdefault(k, []).extend(v)
                elif isinstance(v, dict):
                    artifacts.setdefault(k, {})
                    for subk, subv in v.items():
                        existing = artifacts[k].get(subk)
                        if existing is None:
                            artifacts[k][subk] = subv
                            provenance.setdefault(k, {})[subk] = (name, conf)
                        else:
                            prev_agent, prev_conf = provenance[k][subk]
                            if conf > prev_conf:
                                artifacts[k][subk] = subv
                                provenance[k][subk] = (name, conf)
                else:
                    existing = artifacts.get(k)
                    if existing is None:
                        artifacts[k] = v
                        provenance[k] = (name, conf)
                    else:
                        prev_agent, prev_conf = provenance[k]
                        if conf > prev_conf:
                            artifacts[k] = v
                            provenance[k] = (name, conf)
        code_joined = []
        for name, r in responses.items():
            p = r.get("payload", {})
            if "code" in p:
                header = f"# From {name} (conf={r.get('confidence')})"
                code_joined.append(header + "\n" + p["code"])
        if code_joined:
            artifacts["code_stubs"] = "\n\n".join(code_joined)
        for k in list(artifacts.keys()):
            if isinstance(artifacts[k], list):
                artifacts[k] = list(dict.fromkeys(artifacts[k]))
        return {"artifacts": artifacts, "provenance": provenance}
