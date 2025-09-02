from ..state import StockState
from ...utils.agents import gemini
from ...observability.monitoring import instrument


@instrument("crawl")
def crawl_node(state: StockState) -> StockState:
    ticker = state.get("ticker", "")
    if not ticker or ticker == "UNKNOWN":
        state["summary"] = "Unable to determine ticker symbol."
        return state

    prompt = f"""
Analyze the stock {ticker} and provide a comprehensive summary including:
- Current market performance
- Key financial metrics
- Recent news and developments
- Risk factors
- Growth potential

Focus on actionable insights for investors.
"""

    response = gemini.invoke(prompt)
    state["summary"] = response.content
    return state
