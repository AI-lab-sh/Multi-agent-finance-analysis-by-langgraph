import re
from io import BytesIO
from typing import Dict

import matplotlib.pyplot as plt
from PIL import Image
import yfinance as yf
import pandas as pd
import matplotlib.dates as mdates
import markdown


def extract_portfolio_allocations(text: str) -> Dict[str, float]:
    allocations: Dict[str, float] = {}
    pattern = r"(\d+\.?\d*)(?:-(\d+\.?\d*))?%.*?(?:of|to)\s+(\w+)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    for low, high, ticker in matches:
        if high:
            amount = (float(low) + float(high)) / 2
        else:
            amount = float(low)
        allocations[ticker.upper()] = amount
    return allocations


def plot_portfolio_pie(recommendations_text: str):
    allocations = extract_portfolio_allocations(recommendations_text)
    if not allocations:
        return None
    labels = list(allocations.keys())
    sizes = list(allocations.values())

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Portfolio Allocation")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return Image.open(buf)


def extract_portfolio_section(text: str) -> str:
    pattern = r"(?:Suggested Portfolio Allocation.*?)(?:\n\n|$)"
    match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)
    return ""


def format_portfolio(portfolio_text: str) -> str:
    html_text = markdown.markdown(portfolio_text)
    return (
        "<div style='background:#f5f5f5; padding:10px; border-radius:6px; "
        "font-family:monospace;'>" + html_text + "</div>"
    )


def plot_price_history(ticker: str):
    data = yf.download(ticker, period="1mo", interval="1d")
    if data is None or getattr(data, "empty", True):
        return None

    data.index = pd.to_datetime(data.index)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data.index, data["Close"], label="Close Price", color="blue")
    ax.set_title(f"{ticker} Price History (1 Month)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
    fig.autofmt_xdate()
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)


