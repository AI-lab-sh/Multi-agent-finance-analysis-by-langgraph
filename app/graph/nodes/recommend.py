from ..state import StockState
from ...utils.agents import llama
from ...observability.monitoring import instrument


@instrument("recommend")
def recommend_node(state: StockState) -> StockState:
    ticker = state.get("ticker", "")
    analysis = state.get("analysis", "")
    
    if not ticker or ticker == "UNKNOWN" or not analysis:
        state["recommendations"] = "Unable to provide recommendations due to insufficient data."
        return state

    prompt = f"""
Based on the analysis for {ticker}, provide specific investment recommendations:

{analysis}

Please provide:
1. Clear buy/hold/sell recommendation with reasoning
2. Target price and time horizon
3. Portfolio allocation percentage
4. Risk management strategies
5. Key factors to monitor

Format the portfolio allocation as a clear section for easy parsing.
"""

    response = llama.invoke(prompt)
    state["recommendations"] = response.content
    return state


def highlight_recommendation(text: str) -> str:
    """Highlight key recommendation words in HTML."""
    highlights = {
        "buy": '<span style="background-color:green;color:white;padding:2px 4px;border-radius:3px;">BUY</span>',
        "sell": '<span style="background-color:red;color:white;padding:2px 4px;border-radius:3px;">SELL</span>', 
        "hold": '<span style="background-color:yellow;color:black;padding:2px 4px;border-radius:3px;">HOLD</span>',
        "strong": '<span style="font-weight:bold;">STRONG</span>',
        "weak": '<span style="color:orange;">WEAK</span>',
        "positive": '<span style="color:green;">POSITIVE</span>',
        "negative": '<span style="color:red;">NEGATIVE</span>'
    }
    
    highlighted = text
    for word, html in highlights.items():
        highlighted = highlighted.replace(word.upper(), html)
    
    return highlighted
