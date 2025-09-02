from ..state import StockState, validate_ticker
from ...utils.agents import gemini
import re
import yfinance as yf
from ...utils.tools import tavily_tool
from ...observability.monitoring import instrument


@instrument("infer")
def infer_ticker_node(state: StockState) -> StockState:
    user_input = state.get("user_input", "").strip()

    if user_input.isalpha() and len(user_input) <= 5:
        if validate_ticker(user_input):
            state["ticker"] = user_input.upper()
            return state

    prompt = (
        f"""
You are an intelligent financial assistant.
The user entered: "{user_input}"
Your task: Infer the correct stock ticker symbol.

Rules:
- If this is already a valid ticker (e.g., TSLA, AAPL), return it directly.
- If it is a company name or misspelled ticker, return the most relevant ticker symbol.
- Only return the ticker symbol, nothing else.
"""
    )
    response = gemini.invoke(prompt)
    inferred_ticker = response.content.strip().upper()

    try:
        test_data = yf.download(inferred_ticker, period="5d", interval="1d")
    except Exception:
        test_data = None

    if test_data is None or getattr(test_data, "empty", True):
        try:
            updated = tavily_tool(f"current stock ticker symbol for {inferred_ticker}")
            match = re.search(r"\b[A-Z]{1,5}\b", updated)
            if match:
                inferred_ticker = match.group(0).upper()
        except Exception:
            pass

    if not validate_ticker(inferred_ticker):
        state["ticker"] = "UNKNOWN"
    else:
        state["ticker"] = inferred_ticker

    return state


