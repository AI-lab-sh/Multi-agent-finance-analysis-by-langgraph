import sys
import types
import importlib
import pandas as pd


class DummyResponse:
    def __init__(self, content: str):
        self.content = content


def import_infer_with_fakes(gemini_reply: str):
    # Inject a fake agents module BEFORE importing nodes.infer
    fake_agents = types.ModuleType("agents")
    setattr(fake_agents, "gemini", types.SimpleNamespace(invoke=lambda _: DummyResponse(gemini_reply)))
    setattr(fake_agents, "llama", object())
    sys.modules["agents"] = fake_agents

    # Fresh import of module under test
    if "nodes.infer" in sys.modules:
        del sys.modules["nodes.infer"]
    return importlib.import_module("nodes.infer")


def test_infer_ticker_node_happy_path(monkeypatch):
    infer_mod = import_infer_with_fakes("AAPL")

    # Mock yfinance.download → non-empty dataframe
    df = pd.DataFrame({"Close": [100.0]})
    monkeypatch.setattr(infer_mod.yf, "download", lambda *a, **k: df, raising=True)

    # Mock validate_ticker → valid
    monkeypatch.setattr(infer_mod, "validate_ticker", lambda t: t, raising=True)

    state = {"user_input": "Apple"}
    out = infer_mod.infer_ticker_node(state)
    assert out["ticker"] == "AAPL"


def test_infer_ticker_node_invalid_then_unknown(monkeypatch):
    infer_mod = import_infer_with_fakes("BAD")

    # yfinance returns empty-like
    class Empty:
        empty = True

    monkeypatch.setattr(infer_mod.yf, "download", lambda *a, **k: Empty(), raising=True)
    # tavily_tool raises (simulating HTTP error)
    def raise_err(*_args, **_kwargs):
        raise Exception("net")

    monkeypatch.setattr(infer_mod, "tavily_tool", raise_err, raising=True)
    # validator says invalid
    monkeypatch.setattr(infer_mod, "validate_ticker", lambda *_: "", raising=True)

    state = {"user_input": "Some Co"}
    out = infer_mod.infer_ticker_node(state)
    assert out["ticker"] == "UNKNOWN"


