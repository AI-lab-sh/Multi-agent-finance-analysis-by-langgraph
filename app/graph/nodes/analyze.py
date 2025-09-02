from ..state import StockState
from ...utils.agents import llama
from ...observability.monitoring import instrument


@instrument("analyze")
def analyze_node(state: StockState) -> StockState:
    ticker = state.get("ticker", "")
    summary = state.get("summary", "")
    
    if not ticker or ticker == "UNKNOWN" or not summary:
        state["analysis"] = "Insufficient data for analysis."
        return state

    prompt = f"""
Based on the following summary for {ticker}, provide a detailed financial analysis:

{summary}

Please analyze:
1. Financial health and stability
2. Market position and competitive advantages
3. Growth prospects and risks
4. Valuation metrics
5. Investment thesis

Provide specific insights and recommendations.
"""

    response = llama.invoke(prompt)
    state["analysis"] = response.content
    return state
