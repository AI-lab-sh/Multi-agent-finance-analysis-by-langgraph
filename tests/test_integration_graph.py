import pandas as pd

import nodes.infer as infer_mod
import nodes.crawl as crawl_mod
import nodes.analyze as analyze_mod
import nodes.recommend as recommend_mod
import gradio_frontend as app


class DummyResponse:
    def __init__(self, content: str):
        self.content = content


def test_full_graph_flow(monkeypatch):
    # Infer: mock LLM + yfinance + validator
    monkeypatch.setattr(infer_mod.gemini, "invoke", lambda *_: DummyResponse("AAPL"), raising=True)
    monkeypatch.setattr(infer_mod.yf, "download", lambda *_, **__: pd.DataFrame({"Close": [1.0]}), raising=True)
    monkeypatch.setattr(infer_mod, "validate_ticker", lambda t: t, raising=True)
    # Crawl: mock LLM to return summary
    monkeypatch.setattr(crawl_mod.gemini, "invoke", lambda *_: DummyResponse("SUMMARY"), raising=True)
    # Analyze: mock chain to return analysis
    class DummyChain:
        def __init__(self, *args, **kwargs):
            pass
        def run(self, **kwargs):
            return "ANALYSIS"
    monkeypatch.setattr(analyze_mod, "LLMChain", DummyChain, raising=True)
    # Recommend: mock chain to return recs
    class DummyChain2:
        def __init__(self, *args, **kwargs):
            pass
        def run(self, **kwargs):
            return "RECOMMENDATIONS"
    monkeypatch.setattr(recommend_mod, "LLMChain", DummyChain2, raising=True)

    graph = app.build_graph()
    result = graph.invoke({"user_input": "Apple"})

    assert result["ticker"] == "AAPL"
    assert result["summary"] == "SUMMARY"
    assert result["analysis"] == "ANALYSIS"
    assert result["recommendations"] == "RECOMMENDATIONS"


