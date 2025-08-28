import yfinance as yf
import finnhub
from tavily import TavilyClient
from langchain.tools import tool
from config import TAVILY_API_KEY, FINNHUB_API_KEY

# ----------------------
# Tavily tool
# ----------------------
tavily = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def tavily_tool(ticker: str) -> str:
    """Fetch latest stock news from Tavily for the given ticker symbol."""
    results = tavily.search(f"{ticker} stock news", max_results=5)
    return "\n".join([r["content"] for r in results["results"]])

# ----------------------
# Yahoo Finance tool
# ----------------------
@tool
def yahoo_finance_tool(ticker: str) -> str:
    """Fetch stock fundamental metrics from Yahoo Finance for the given ticker."""
    stock = yf.Ticker(ticker)
    info = stock.info
    summary = {
        "currentPrice": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "dividendYield": info.get("dividendYield"),
        "sector": info.get("sector"),
    }
    return str(summary)

# ----------------------
# Finnhub tool
# ----------------------
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

@tool
def finnhub_tool(ticker: str) -> str:
    """Fetch company news and financial metrics from Finnhub for the given ticker."""
    # Latest company news
    news = finnhub_client.company_news(ticker, _from="2024-01-01", to="2024-12-31")
    news_text = [f"{n['datetime']} - {n['headline']}: {n['summary']}" for n in news[:5]]

    # Company metrics
    metrics = finnhub_client.company_basic_financials(ticker, "all")

    return f"News: {news_text}\nMetrics: {metrics.get('metric', {})}"

import requests
from langchain.tools import tool
from config import NEWS_API_KEY

# ----------------------
# NewsAPI tool
# ----------------------
@tool
def newsapi_tool(ticker: str) -> str:
    """Fetch latest news headlines and summaries from NewsAPI for the given ticker."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "apiKey": NEWS_API_KEY,
        "pageSize": 5,
        "sortBy": "publishedAt",
        "language": "en"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    articles = data.get("articles", [])
    news_text = [f"{a['publishedAt']} - {a['title']}: {a['description']}" for a in articles]
    
    return "\n".join(news_text)

