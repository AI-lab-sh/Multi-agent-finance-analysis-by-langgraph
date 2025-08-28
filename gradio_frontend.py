import gradio as gr
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import re
import yfinance as yf
import markdown
import matplotlib.dates as mdates
import pandas as pd

# Import the node functions from main.py (now including infer_ticker_node)
from main import infer_ticker_node, crawl_node, analyze_node, recommend_node

# ----------------------------
# Helper functions
# ----------------------------
def highlight_recommendation(html_text):
    lc = html_text.lower()
    if "buy" in lc:
        return f"<span style='color:white; background-color:green; padding:2px 6px; border-radius:4px;'>BUY</span> {html_text}"
    elif "sell" in lc:
        return f"<span style='color:white; background-color:red; padding:2px 6px; border-radius:4px;'>SELL</span> {html_text}"
    elif "hold" in lc:
        return f"<span style='color:black; background-color:yellow; padding:2px 6px; border-radius:4px;'>HOLD</span> {html_text}"
    else:
        return html_text

def format_portfolio(portfolio_text):
    # Convert Markdown to HTML before wrapping
    html_text = markdown.markdown(portfolio_text)
    return f"<div style='background:#f5f5f5; padding:10px; border-radius:6px; font-family:monospace;'>{html_text}</div>"

def plot_price_history(ticker):
    data = yf.download(ticker, period="1mo", interval="1d")
    if data.empty:
        return None

    data.index = pd.to_datetime(data.index)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data.index, data["Close"], label="Close Price", color="blue")
    ax.set_title(f"{ticker} Price History (1 Month)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()

    # Improve date tick readability
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
    fig.autofmt_xdate()
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# ----------------------------
# Extract allocations from descriptive text
# ----------------------------
def extract_portfolio_allocations(text):
    allocations = {}
    # Match "5-10% allocation of AAPL" or "10% allocation to TSLA"
    pattern = r"(\d+\.?\d*)(?:-(\d+\.?\d*))?%.*?(?:of|to)\s+(\w+)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    for low, high, ticker in matches:
        if high:
            amount = (float(low) + float(high)) / 2  # take average of range
        else:
            amount = float(low)
        allocations[ticker.upper()] = amount
    return allocations

def plot_portfolio_pie(recommendations_text):
    allocations = extract_portfolio_allocations(recommendations_text)
    if not allocations:
        return None
    labels = list(allocations.keys())
    sizes = list(allocations.values())

    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Portfolio Allocation")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return Image.open(buf)

def extract_portfolio_section(text):
    """
    Extract only the portfolio allocation section from recommendations.
    """
    pattern = r"(?:Suggested Portfolio Allocation.*?)(?:\n\n|$)"
    match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)
    return ""

# ----------------------------
# Streaming Gradio function with inference
# ----------------------------
# ----------------------------
# Streaming Gradio function with inference
# ----------------------------
def analyze_query_streaming(user_query: str):
    # Start with user_input; ticker will be inferred by the first node
    state = {"user_input": user_query.strip()}

    # Node 0: Infer Ticker
    state = infer_ticker_node(state)
    inferred_ticker = state.get("ticker", "").upper() if state.get("ticker") else ""
    inferred_html = f"<details open><summary><b>Inferred Ticker</b></summary><p>{inferred_ticker or '—'}</p></details>"
    # First yield: only inferred ticker
    yield inferred_html, "", "", None, None, ""

    # Node A: Crawl
    state = crawl_node(state)
    summary_html = f"<details open><summary><b>Summary</b></summary>{markdown.markdown(state['summary'])}</details>"
    # Second yield: inferred + summary
    yield inferred_html, summary_html, "", None, None, ""

    # Node B: Analyze
    state = analyze_node(state)
    analysis_html = f"<details open><summary><b>Analysis</b></summary>{markdown.markdown(state['analysis'])}</details>"
    # Third yield: inferred + summary + analysis
    yield inferred_html, summary_html, analysis_html, None, None, ""

    # Node C: Recommend
    state = recommend_node(state)
    recommendations_html = f"<details open><summary><b>Recommendations</b></summary>{highlight_recommendation(markdown.markdown(state['recommendations']))}</details>"

    # Extract portfolio allocation section only
    portfolio_text = extract_portfolio_section(state['recommendations'])
    portfolio_html = format_portfolio(portfolio_text)
    portfolio_chart = plot_portfolio_pie(state['recommendations'])

    # ✅ Always use the inferred ticker for price history (no fallback to user_query)
    price_chart = plot_price_history(state["ticker"])

    # Final yield: all panels filled
    yield inferred_html, summary_html, analysis_html, price_chart, portfolio_chart, portfolio_html

    # Start with user_input; ticker will be inferred by the first node
    state = {"user_input": user_query.strip()}

    # Node 0: Infer Ticker
    state = infer_ticker_node(state)
    inferred_ticker = state.get("ticker", "").upper() if state.get("ticker") else ""
    inferred_html = f"<details open><summary><b>Inferred Ticker</b></summary><p>{inferred_ticker or '—'}</p></details>"
    # First yield: only inferred ticker
    yield inferred_html, "", "", None, None, ""

    # Node A: Crawl
    state = crawl_node(state)
    summary_html = f"<details open><summary><b>Summary</b></summary>{markdown.markdown(state['summary'])}</details>"
    # Second yield: inferred + summary
    yield inferred_html, summary_html, "", None, None, ""

    # Node B: Analyze
    state = analyze_node(state)
    analysis_html = f"<details open><summary><b>Analysis</b></summary>{markdown.markdown(state['analysis'])}</details>"
    # Third yield: inferred + summary + analysis
    yield inferred_html, summary_html, analysis_html, None, None, ""

    # Node C: Recommend
    state = recommend_node(state)
    recommendations_html = f"<details open><summary><b>Recommendations</b></summary>{highlight_recommendation(markdown.markdown(state['recommendations']))}</details>"

    # Extract portfolio allocation section only
    portfolio_text = extract_portfolio_section(state['recommendations'])
    portfolio_html = format_portfolio(portfolio_text)
    portfolio_chart = plot_portfolio_pie(state['recommendations'])

    # Price history chart for the inferred ticker
    price_chart = plot_price_history(inferred_ticker or user_query.strip().upper())

    # Final yield: all panels filled
    yield inferred_html, summary_html, analysis_html, price_chart, portfolio_chart, portfolio_html

# ----------------------------
# Gradio interface
# ----------------------------
iface = gr.Interface(
    fn=analyze_query_streaming,
    inputs=gr.Textbox(label="Enter Company Name or Ticker", placeholder="e.g. Apple, AAPL, or aaplee"),
    outputs=[
        gr.HTML(label="Inferred Ticker"),
        gr.HTML(label="Summary"),
        gr.HTML(label="Analysis"),
        gr.Image(label="Price History"),
        gr.Image(label="Portfolio Allocation"),
        gr.HTML(label="Portfolio Details")
    ],
    title="Stock Analyzer (Streaming Outputs + Ticker Inference)",
    description="Type a company name or a misspelled ticker. The app infers the ticker, crawls data, analyzes it, and recommends actions."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
