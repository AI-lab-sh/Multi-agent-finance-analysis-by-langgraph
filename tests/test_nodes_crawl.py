import sys
import types
import importlib


def import_crawl_with_fake_gemini(summary_text: str):
    fake_agents = types.ModuleType("agents")
    class DummyResponse:
        def __init__(self, content: str):
            self.content = content
    setattr(fake_agents, "gemini", types.SimpleNamespace(invoke=lambda *_: DummyResponse(summary_text)))
    sys.modules["agents"] = fake_agents
    if "nodes.crawl" in sys.modules:
        del sys.modules["nodes.crawl"]
    return importlib.import_module("nodes.crawl")


def test_crawl_node_sets_summary():
    crawl_mod = import_crawl_with_fake_gemini("This is a summary")
    state = {"ticker": "AAPL"}
    out = crawl_mod.crawl_node(state)
    assert "summary" in out and out["summary"] == "This is a summary"


