import sys
import types
import pandas as pd

import app.graph.nodes.infer as infer_mod
import app.graph.nodes.crawl as crawl_mod
import app.graph.nodes.analyze as analyze_mod
import app.graph.nodes.recommend as recommend_mod
import app.ui.gradio_app as app


class DummyResponse:
    def __init__(self, content: str):
        self.content = content


def test_full_graph_flow(monkeypatch):
    # Create fake agents module with proper mocks
    fake_agents = types.ModuleType("agents")
    
    # Mock gemini
    class DummyGemini:
        def invoke(self, prompt):
            if "infer the correct stock ticker" in prompt.lower():
                return DummyResponse("AAPL")
            elif "analyze the stock" in prompt.lower():
                return DummyResponse("SUMMARY")
            else:
                return DummyResponse("DEFAULT")
    fake_agents.gemini = DummyGemini()
    
    # Mock llama
    class DummyLlama:
        def invoke(self, prompt):
            if "provide specific investment recommendations" in prompt.lower():
                return DummyResponse("RECOMMENDATIONS")
            elif "provide a detailed financial analysis" in prompt.lower():
                return DummyResponse("ANALYSIS")
            else:
                return DummyResponse("DEFAULT")
    fake_agents.llama = DummyLlama()
    
    # Inject fake agents BEFORE importing modules
    sys.modules["app.utils.agents"] = fake_agents
    
    # Re-import modules to use the fake agents
    import importlib
    if "app.graph.nodes.infer" in sys.modules:
        del sys.modules["app.graph.nodes.infer"]
    if "app.graph.nodes.crawl" in sys.modules:
        del sys.modules["app.graph.nodes.crawl"]
    if "app.graph.nodes.analyze" in sys.modules:
        del sys.modules["app.graph.nodes.analyze"]
    if "app.graph.nodes.recommend" in sys.modules:
        del sys.modules["app.graph.nodes.recommend"]
    
    # Re-import with fake agents
    infer_mod = importlib.import_module("app.graph.nodes.infer")
    crawl_mod = importlib.import_module("app.graph.nodes.crawl")
    analyze_mod = importlib.import_module("app.graph.nodes.analyze")
    recommend_mod = importlib.import_module("app.graph.nodes.recommend")
    
    # Re-import app.ui.gradio_app to use the new modules
    if "app.ui.gradio_app" in sys.modules:
        del sys.modules["app.ui.gradio_app"]
    app = importlib.import_module("app.ui.gradio_app")
    
    # Mock yfinance and validation
    monkeypatch.setattr(infer_mod.yf, "download", lambda *_, **__: pd.DataFrame({"Close": [1.0]}), raising=True)
    monkeypatch.setattr(infer_mod, "validate_ticker", lambda t: t if t.upper() == "AAPL" else "", raising=True)

    graph = app.build_graph()
    result = graph.invoke({"user_input": "Apple"})

    assert result["ticker"] == "AAPL"
    assert result["summary"] == "SUMMARY"
    assert result["analysis"] == "ANALYSIS"
    assert result["recommendations"] == "RECOMMENDATIONS"


