import sys
import types
import importlib


def import_analyze_with_fake_llmchain(reply_text: str):
    # Create a fake llama object with invoke method
    class DummyLlama:
        def invoke(self, prompt):
            class DummyResponse:
                def __init__(self, content):
                    self.content = content
            return DummyResponse(reply_text)
    
    fake_agents = types.ModuleType("agents")
    setattr(fake_agents, "llama", DummyLlama())
    sys.modules["app.utils.agents"] = fake_agents

    # Fresh import of module under test
    if "app.graph.nodes.analyze" in sys.modules:
        del sys.modules["app.graph.nodes.analyze"]
    analyze_mod = importlib.import_module("app.graph.nodes.analyze")
    return analyze_mod


def test_analyze_node_sets_analysis_text():
    analyze_mod = import_analyze_with_fake_llmchain("analysis-ok")
    state = {"ticker": "AAPL", "summary": "sum"}
    out = analyze_mod.analyze_node(state)
    assert out["analysis"] == "analysis-ok"


