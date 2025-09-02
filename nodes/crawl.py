from state import StockState
from agents import gemini
from monitoring import instrument


@instrument("crawl")
def crawl_node(state: StockState) -> StockState:
    ticker = state["ticker"]

    if ticker == "UNKNOWN":
        state["summary"] = "❌ Could not infer a valid ticker from your input."
        return state

    tool_descriptions = (
        "Available tools:\n"
        "1. tavily_tool(ticker) -> fetch latest stock news from web\n"
        "2. yahoo_finance_tool(ticker) -> fetch fundamental stock metrics\n"
        "3. finnhub_tool(ticker) -> fetch company news and financial metrics\n"
        "4. newsapi_tool(ticker) -> fetch latest news headlines from NewsAPI\n"
    )

    prompt = f"""
    You are an intelligent stock research agent.

    Task: Gather relevant information for ticker {ticker}.
    Use the tools as needed:
    {tool_descriptions}

    Output a concise, plain-text summary for investors.
    """
    summary = gemini.invoke(prompt)
    state["summary"] = summary.content
    return state


