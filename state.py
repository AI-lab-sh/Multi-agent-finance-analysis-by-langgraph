from typing import TypedDict
import yfinance as yf


class StockState(TypedDict):
    user_input: str
    ticker: str
    summary: str
    analysis: str
    recommendations: str


def validate_ticker(ticker: str) -> str:
    try:
        data = yf.Ticker(ticker).info
        if data and "symbol" in data:
            return ticker.upper()
    except Exception:
        pass
    return ""


