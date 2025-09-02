import sys
import types
import importlib


def import_analyze_with_fake_llmchain(reply_text: str):
    # Fake agents.llama not actually used directly, but ensure import safety
    fake_agents = types.ModuleType("agents")
    setattr(fake_agents, "llama", object())
    sys.modules["agents"] = fake_agents

    # Patch LLMChain in module namespace after import
    if "nodes.analyze" in sys.modules:
        del sys.modules["nodes.analyze"]
    analyze_mod = importlib.import_module("nodes.analyze")

    class DummyChain:
        def __init__(self, *args, **kwargs):
            pass
        def run(self, **kwargs):
            return reply_text

    analyze_mod.LLMChain = DummyChain
    return analyze_mod


def test_analyze_node_sets_analysis_text():
    analyze_mod = import_analyze_with_fake_llmchain("analysis-ok")
    state = {"ticker": "AAPL", "summary": "sum"}
    out = analyze_mod.analyze_node(state)
    assert out["analysis"] == "analysis-ok"


