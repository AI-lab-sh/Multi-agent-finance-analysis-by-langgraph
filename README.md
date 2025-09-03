# 🏦 Multi-Agent Financial Intelligence Platform (LangGraph Version)
This project implements a modern multi-agent financial intelligence platform using **LangGraph**, open-source LLMs, and market data tools. It processes natural language investment queries, handles spelling errors and company names if ticker symbols are incorrect, extracts the most recent ticker symbols using search tools like Tavily, scrapes market and qualitative data from sources such as Yahoo Finance and news sites, performs in-depth analysis, and delivers structured, actionable recommendations, including price charts and portfolio allocation suggestions.  
The system integrates crawler scripts, multiple LLM-driven agents, and external APIs to deliver high-quality insights for investors, analysts, and automated trading tools.

## 📊 System Architecture
![System Architecture Diagram](assets/diagram.png)

## 📊 Data Flow
The workflow proceeds in stages:

1. **User Query**

   * Can be a **natural language query**, e.g., "invest in renewable energy" or "Apple company".
   * Can also be a **ticker symbol**, e.g., `AAPL`, `TSLA`.
   * The query is sent to the **Ticker Inference Agent** to extract the relevant ticker symbol.

2. **Ticker Inference Agent**

   * If the user input is a valid ticker, it returns the ticker.
   * If the input is a company name or a **misspelled ticker**, it infers the most relevant ticker symbol.
   * If the input is an **old/outdated ticker symbol**, it finds the current updated symbol (e.g., `FB` → `META`).
   * This guarantees that all downstream agents use the correct ticker symbol.

3. **Crawler Agent**

   * Fetches data from multiple sources:

     * Yahoo Finance
     * Finnhub
     * Tavily
     * NewsAPI
   * Produces raw summaries, financial metrics, and news content for the selected ticker.

4. **Analysis Agent (Groq LLaMA)**

   * Performs quantitative and qualitative analysis on the crawled data.
   * Produces stock outlook summaries.

5. **Recommender Agent**

   * Generates actionable investment guidance:

     * Buy / Hold / Sell recommendations
     * Portfolio allocation suggestions
     * Risk management strategies

---

## 🌟 Key Features

* **Ticker Handling**: Automatically corrects old or misspelled tickers using LLM reasoning + search tools.
* **Portfolio Awareness**: Extracts portfolio allocation suggestions and visualizes them.
* **Streaming Output**: Each node's results are displayed progressively in the frontend.
* **Integration of Quantitative & Qualitative Data**: Combines financial metrics with market news and insights.
* **Graph-Oriented Orchestration**: Uses **LangGraph** and **LangChain** to define and manage the workflow between agents efficiently.
* **Robust Error Handling & Logging**: Detects missing or outdated data.
* **User-Friendly Interface**: Simple Gradio interface with charts and formatted Markdown output.

---

## 📈 Technology Stack

* **Python 3.10+**
* **LangGraph**: Modern graph-based orchestration of agents
* **LangChain**: For prompt chaining and agent workflows
* **LLM APIs**: Gemini-2.0-Flash, Groq LLaMA 3.1 8B
* **Market Data**: Yahoo Finance, Tavily
* **Visualization**: Matplotlib, Markdown formatting in frontend
* **Web Interface**: Gradio
* **Monitoring**: Prometheus metrics

## 📦 Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Key dependencies include:
- `langgraph` - Agent orchestration
- `langchain` - LLM integration framework
- `gradio` - Web interface
- `yfinance` - Stock market data
- `tavily-python` - Web search
- `prometheus-client` - Metrics collection

---


## 🚀 Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file (keys as needed):

```text
GEMINI_API_KEY=your_gemini_key
FINNHUB_API_KEY=your_finnhub_key
NEWSAPI_KEY=your_newsapi_key
```

3. Run the app:

```bash
python run_app.py
```

This starts the UI at `http://localhost:7860` and monitoring at `http://localhost:9100/metrics`.

Optional: Auto-start local Prometheus/Grafana by adding to `.env`:

```text
START_LOCAL_MONITORING=1
```
If available on your system, Prometheus runs at `http://localhost:9090` and Grafana at `http://localhost:3000`.

---

## 📈 Monitoring

Monitoring starts automatically with `python run_app.py`. Metrics are exposed at `http://localhost:9100/metrics`. To optionally auto-start Prometheus/Grafana, see the Setup notes above.

LLM tracing (LangSmith):
- Enable deep tracing of prompts/tokens/costs by setting env vars:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_langsmith_key
export LANGCHAIN_PROJECT=lang_graph
```

Errors (optional):
- Add Sentry for exception tracking:
  - `pip install sentry-sdk`
  - `sentry_sdk.init(dsn="https://<dsn>", traces_sample_rate=0.2)`

---

## ✅ Automated Tests

We use pytest with mocks to keep tests fast and offline.

- Install pytest (once per environment):

```bash
pip install pytest
```

- Run all tests from the project root:

```bash
pytest -q
```

What's covered:
- `tests/test_nodes_infer.py`: unit tests for `nodes/infer.py` with external calls (LLMs, yfinance, Tavily) stubbed via `monkeypatch`.
- `tests/test_utils.py`: parsing and extraction helpers in `utils.py`.
- `tests/test_nodes_crawl.py`, `tests/test_nodes_analyze.py`, `tests/test_nodes_recommend.py`: unit tests for other nodes and helpers.
- `tests/test_integration_graph.py`: integration test that runs the full LangGraph pipeline with all external calls mocked.

Notes on mocking:
- External/networked dependencies are replaced with lightweight fakes so tests are deterministic and run without internet/API keys.
- Prefer one behavior/assertion per test. Keep tests small and focused.

Run only integration tests:

```bash
pytest -q -k integration
```

CI:
- GitHub Actions workflow in `.github/workflows/tests.yml` runs `pytest` on every push/PR.


## 🔮 Future Enhancements

* Backtesting of recommended portfolios
* Expanded data sources (Bloomberg, TradingView)
* Options / derivatives support
* Interactive dashboards with portfolio simulation and risk modeling

---