from ..graph.state import StockState
from ..graph.nodes.infer import infer_ticker_node
from ..graph.nodes.crawl import crawl_node
from ..graph.nodes.analyze import analyze_node
from ..graph.nodes.recommend import recommend_node, highlight_recommendation
from ..utils.portfolio import (
    extract_portfolio_allocations,
    plot_portfolio_pie,
    extract_portfolio_section,
    format_portfolio,
    plot_price_history,
)
from ..observability.monitoring import start_metrics_server
from langgraph.graph import StateGraph
import gradio as gr
import markdown
import os
import shutil
import subprocess
from pathlib import Path
from config import START_LOCAL_MONITORING
# try:
#     from dotenv import load_dotenv  # type: ignore
#     load_dotenv()
# except Exception:
#     pass


def build_graph():
    graph_builder = StateGraph(StockState)
    graph_builder.add_node("infer_ticker", infer_ticker_node)
    graph_builder.add_node("crawl", crawl_node)
    graph_builder.add_node("analyze", analyze_node)
    graph_builder.add_node("recommend", recommend_node)
    graph_builder.set_entry_point("infer_ticker")
    graph_builder.add_edge("infer_ticker", "crawl")
    graph_builder.add_edge("crawl", "analyze")
    graph_builder.add_edge("analyze", "recommend")
    return graph_builder.compile()


def analyze_query_streaming(user_query: str):
    state = {"user_input": user_query.strip()}
    state = infer_ticker_node(state)
    inferred_ticker = state.get("ticker", "").upper() if state.get("ticker") else ""
    inferred_html = f"<details open><summary><b>Inferred Ticker</b></summary><p>{inferred_ticker or '—'}</p></details>"
    yield inferred_html, "", "", None, None, ""

    state = crawl_node(state)
    summary_html = f"<details open><summary><b>Summary</b></summary>{markdown.markdown(state['summary'])}</details>"
    yield inferred_html, summary_html, "", None, None, ""

    state = analyze_node(state)
    analysis_html = f"<details open><summary><b>Analysis</b></summary>{markdown.markdown(state['analysis'])}</details>"
    yield inferred_html, summary_html, analysis_html, None, None, ""

    state = recommend_node(state)
    recommendations_html = f"<details open><summary><b>Recommendations</b></summary>{highlight_recommendation(markdown.markdown(state['recommendations']))}</details>"

    portfolio_text = extract_portfolio_section(state['recommendations'])
    portfolio_html = format_portfolio(portfolio_text)
    portfolio_chart = plot_portfolio_pie(state['recommendations'])
    price_chart = plot_price_history(state["ticker"])  # inferred ticker

    yield inferred_html, summary_html, analysis_html, price_chart, portfolio_chart, portfolio_html


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


def _maybe_start_local_monitoring():
    if START_LOCAL_MONITORING != "1":
        return
    try:
        project_root = Path(__file__).resolve().parents[2]
        prom_cfg = project_root / "monitoring" / "prometheus.local.yml"
        prom_bin = shutil.which("prometheus")
        if prom_bin and prom_cfg.exists():
            subprocess.Popen([prom_bin, f"--config.file={str(prom_cfg)}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    try:
        brew = shutil.which("brew")
        if brew:
            subprocess.Popen([brew, "services", "start", "grafana"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            grafana_bin = shutil.which("grafana-server")
            if grafana_bin:
                subprocess.Popen([grafana_bin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main():
    try:
        start_metrics_server(9100)
    except Exception:
        pass
    _maybe_start_local_monitoring()
    iface.launch(server_name="0.0.0.0", server_port=7860)





