from typing import TypedDict
from langgraph.graph import StateGraph
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agents import gemini, llama
from tools import tavily_tool, yahoo_finance_tool, finnhub_tool, newsapi_tool
import yfinance as yf

# -----------------------------
# Define graph state
# -----------------------------
class StockState(TypedDict):
    user_input: str          # raw user query (company name or ticker)
    ticker: str              # inferred + validated ticker
    summary: str
    analysis: str
    recommendations: str

# -----------------------------
# Helper: validate ticker with yfinance
# -----------------------------
def validate_ticker(ticker: str) -> str:
    try:
        data = yf.Ticker(ticker).info
        if data and "symbol" in data:
            return ticker.upper()
    except Exception:
        pass
    return ""  # invalid ticker

# -----------------------------
# Node 0: Ticker inference
# -----------------------------
# -----------------------------
# Node 0: Ticker inference
# -----------------------------
def infer_ticker_node(state: StockState) -> StockState:
    """
    Use Gemini to infer the most relevant ticker symbol from user input.
    If the ticker is old/delisted, use Tavily to search for the updated ticker.
    """
    user_input = state.get("user_input", "").strip()

    # Step 1: Ask Gemini to normalize the input to a ticker
    prompt = f"""
You are an intelligent financial assistant.
The user entered: "{user_input}"
Your task: Infer the correct stock ticker symbol.

Rules:
- If this is already a valid ticker (e.g., TSLA, AAPL), return it directly.
- If it is a company name or misspelled ticker, return the most relevant ticker symbol.
- Only return the ticker symbol, nothing else.
"""
    response = gemini.invoke(prompt)
    inferred_ticker = response.content.strip().upper()

    # Step 2: Check if Yahoo Finance has data for this ticker
    import yfinance as yf
    try:
        test_data = yf.download(inferred_ticker, period="5d", interval="1d")
    except Exception:
        test_data = None

    if test_data is None or test_data.empty:
        # Step 3: Use Tavily to find updated ticker
        tavily_prompt = f"""
The stock ticker "{inferred_ticker}" seems invalid or delisted.
Search the web and return ONLY the current valid ticker symbol that replaced it,
if available. Example: "FB" -> "META".
If no replacement exists, return the original input unchanged.
"""
        try:
            updated_ticker = tavily_tool(f"current stock ticker symbol for {inferred_ticker}")
            # Extract clean ticker from response (LLMs sometimes return sentences)
            import re
            match = re.search(r"\b[A-Z]{1,5}\b", updated_ticker)
            if match:
                inferred_ticker = match.group(0).upper()
        except Exception:
            pass  # fallback to inferred_ticker

    state["ticker"] = inferred_ticker
    return state

    """
    Use Gemini to infer the most relevant ticker symbol from user input.
    Fallback: try yfinance to validate.
    """
    user_input = state.get("user_input", "").strip()

    # If user already typed a valid ticker, keep it
    if user_input.isalpha() and len(user_input) <= 5:
        if validate_ticker(user_input):
            state["ticker"] = user_input.upper()
            return state

    # Otherwise, ask Gemini
    prompt = f"""
    You are an intelligent financial assistant.
    The user entered: "{user_input}"

    Task: Infer the correct US stock ticker.
    - If it's already a valid ticker, return it.
    - If it's a company name or misspelling, return the correct ticker.
    - Reply with ONLY the ticker symbol (e.g. AAPL, TSLA, MSFT).
    """
    response = gemini.invoke(prompt)
    inferred = response.content.strip().upper()

    # Validate with yfinance
    if not validate_ticker(inferred):
        state["ticker"] = "UNKNOWN"
    else:
        state["ticker"] = inferred

    return state

# -----------------------------
# Node A: Crawl data
# -----------------------------
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

# -----------------------------
# Node B: Analysis (LLaMA)
# -----------------------------
def analyze_node(state: StockState) -> StockState:
    if state["ticker"] == "UNKNOWN":
        state["analysis"] = "No analysis possible without a valid ticker."
        return state

    prompt = PromptTemplate(
        template=(
            "Analyze the stock outlook for {ticker} based on this summary:\n\n"
            "{summary}\n\n"
            "Discuss:\n"
            "- Market sentiment\n"
            "- Growth potential\n"
            "- Key risks"
        ),
        input_variables=["ticker", "summary"]
    )
    chain = LLMChain(llm=llama, prompt=prompt)
    analysis = chain.run(ticker=state["ticker"], summary=state["summary"])
    state["analysis"] = analysis
    return state

# -----------------------------
# Node C: Recommender
# -----------------------------
def recommend_node(state: StockState) -> StockState:
    if state["ticker"] == "UNKNOWN":
        state["recommendations"] = "No recommendations possible without a valid ticker."
        return state

    prompt = PromptTemplate(
        template=(
            "You are a financial advisor. Based on this analysis:\n\n"
            "{analysis}\n\n"
            "Provide actionable recommendations:\n"
            "1. Buy / Hold / Sell guidance for {ticker}\n"
            "2. Suggested portfolio allocation (e.g. 5-10% allocation of {ticker})\n"
            "3. Risk management strategies"
        ),
        input_variables=["analysis", "ticker"]
    )
    chain = LLMChain(llm=llama, prompt=prompt)
    recommendations = chain.run(ticker=state["ticker"], analysis=state["analysis"])
    state["recommendations"] = recommendations
    return state

# -----------------------------
# Build LangGraph
# -----------------------------
graph_builder = StateGraph(StockState)
graph_builder.add_node("infer_ticker", infer_ticker_node)
graph_builder.add_node("crawl", crawl_node)
graph_builder.add_node("analyze", analyze_node)
graph_builder.add_node("recommend", recommend_node)

graph_builder.set_entry_point("infer_ticker")
graph_builder.add_edge("infer_ticker", "crawl")
graph_builder.add_edge("crawl", "analyze")
graph_builder.add_edge("analyze", "recommend")

graph = graph_builder.compile()

# -----------------------------
# Demo run
# -----------------------------
if __name__ == "__main__":
    user_query = "apple company"  # test input
    initial_state = {"user_input": user_query}
    result = graph.invoke(initial_state)

    print("Inferred Ticker:", result.get("ticker", ""))
    print("\n=== SUMMARY (Gemini) ===")
    print(result.get("summary", ""))
    print("\n=== ANALYSIS (LLaMA) ===")
    print(result.get("analysis", ""))
    print("\n=== RECOMMENDATIONS ===")
    print(result.get("recommendations", ""))
