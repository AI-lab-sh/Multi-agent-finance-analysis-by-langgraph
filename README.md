# 🏦 Multi-Agent Financial Intelligence Platform (LangGraph Version)
This project implements a modern multi-agent financial intelligence platform using **LangGraph**, open-source LLMs, and market data tools. It processes natural language investment queries, handles spelling errors and company names if ticker symbols are incorrect, extracts the most recent ticker symbols using search tools like Tavily, scrapes market and qualitative data from sources such as Yahoo Finance and news sites, performs in-depth analysis, and delivers structured, actionable recommendations, including price charts and portfolio allocation suggestions.  
The system integrates crawler scripts, multiple LLM-driven agents, and external APIs to deliver high-quality insights for investors, analysts, and automated trading tools.
<<<<<<< HEAD
=======



>>>>>>> 5c3035d (add monitoring and tests)
## 📊 System Architecture
![System Architecture Diagram](assets/diagram.png)
<<<<<<< HEAD
=======



>>>>>>> 5c3035d (add monitoring and tests)
## 📊 Data Flow
The workflow proceeds in stages:
<<<<<<< HEAD
1. **User Query**  
   * Can be a **natural language query**, e.g., "TESLA" or "Apple company".  
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
## 🌟 Key Features
* **Ticker Handling**: Automatically corrects old or misspelled tickers using LLM reasoning + search tools.  
* **Portfolio Awareness**: Extracts portfolio allocation suggestions and visualizes them.  
* **Streaming Output**: Each node’s results are displayed progressively in the frontend.  
* **Integration of Quantitative & Qualitative Data**: Combines financial metrics with market news and insights.  
* **Graph-Oriented Orchestration**: Uses **LangGraph** and **LangChain** to define and manage the workflow between agents efficiently.  
* **Robust Error Handling & Logging**: Detects missing or outdated data.  
* **User-Friendly Interface**: Simple Gradio interface with charts and formatted Markdown output.
## 📈 Technology Stack
* **Python 3.10+**  
* **LangGraph**: Modern graph-based orchestration of agents  
* **LangChain**: For prompt chaining and agent workflows  
* **LLM APIs**: Gemini-2.0-Flash, Groq LLaMA 3.1 8B  
* **Market Data**: Yahoo Finance, Finnhub, Tavily, NewsAPI  
* **Visualization**: Matplotlib, Recharts, Markdown formatting in frontend
## 🔮 Future Enhancements
* Backtesting of recommended portfolios  
* Expanded data sources (Bloomberg, TradingView)  
* Options / derivatives support  
* Interactive dashboards with portfolio simulation and risk modeling
## 🛠 How to Use
1. Clone the repository and navigate to the project folder:
   ```bash
   git clone https://github.com/AI-lab-sh/Multi-agent-finance-analysis-by-langgraph
   cd lang-graph
   ```
2. Create a `.env` file and copy your API key values for all required services (Gemini, Finnhub, NewsAPI, etc.):
   ```text
   GEMINI_API_KEY=your_gemini_key
   FINNHUB_API_KEY=your_finnhub_key
   NEWSAPI_KEY=your_newsapi_key
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the Gradio frontend:
   ```bash
   python gradio_frontend.py
   ```
5. Open your browser at `http://127.0.0.1:7860` to start entering queries.
=======

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
* **Streaming Output**: Each node’s results are displayed progressively in the frontend.
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
* **Market Data**: Yahoo Finance, Finnhub, Tavily, NewsAPI
* **Visualization**: Matplotlib, Recharts, Markdown formatting in frontend

---

## 🔮 Future Enhancements

* Backtesting of recommended portfolios
* Expanded data sources (Bloomberg, TradingView)
* Options / derivatives support
* Interactive dashboards with portfolio simulation and risk modeling

---

## 🛠 How to Use

1. Clone the repository and navigate to the project folder:

```bash
git clone <repository-url>
cd <project-folder>
```

2. Create a `.env` file and copy your API key values for all required services (Gemini, Finnhub, NewsAPI, etc.):

```text
GEMINI_API_KEY=your_gemini_key
FINNHUB_API_KEY=your_finnhub_key
NEWSAPI_KEY=your_newsapi_key
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Launch the Gradio frontend:

```bash
python gradio_frontend.py
```

5. Open your browser at `http://127.0.0.1:7860` to start entering queries.

---

## 📈 Monitoring

Conventional metrics (Prometheus):
- Metrics server starts at `:9100` when launching Gradio.
- Exposed metrics:
  - `node_calls_total{node}`
  - `node_errors_total{node}`
  - `node_latency_seconds_bucket{node}` (histogram)
- Scrape with Prometheus and visualize in Grafana.

Local Prometheus + Grafana (no Docker):

1) Prometheus config
- Use `monitoring/prometheus.local.yml` as your config:
```bash
prometheus --config.file=monitoring/prometheus.local.yml
# UI: http://localhost:9090
```

2) Run the app (metrics on :9100)
```bash
python gradio_frontend.py
```

3) Grafana
- Start Grafana (e.g., Homebrew on macOS):
```bash
brew services start grafana
# UI: http://localhost:3000  (admin/admin)
```
- Add Prometheus datasource pointing to `http://localhost:9090`
- Optional: import the sample dashboard in `monitoring/grafana.dashboard.json`

Auto-start (optional):
- The app can try to start Prometheus and Grafana for you when it launches.
- Requirements: `prometheus` in PATH, and either `brew services` (macOS) or `grafana-server` in PATH.
- Steps:
  1) Create a `.env` file in the project root with:
     ```
     START_LOCAL_MONITORING=1
     ```
  2) Run the app:
     ```bash
     python gradio_frontend.py
     ```
  3) Open:
     - App UI: `http://localhost:7860`
     - Metrics (raw): `http://localhost:9100/metrics`
     - Prometheus: `http://localhost:9090`
     - Grafana: `http://localhost:3000`

Troubleshooting:
- If `9090/3000` don’t open automatically, start Prometheus/Grafana manually as shown above.
- Ensure `.env` is being loaded; we call `load_dotenv()` in `gradio_frontend.py`.

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

What’s covered:
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

---

## 📁 Project Structure (refactored)

```
lang_graph/
  agents.py            # LLM clients
  state.py             # shared StockState and validation helpers
  nodes/
    infer.py           # ticker inference node
    crawl.py           # data gathering node
    analyze.py         # analysis node
    recommend.py       # recommendations + highlight helper
  utils.py             # portfolio parsing/plot helpers
  monitoring.py        # Prometheus counters/histograms and instrumentation
  gradio_frontend.py   # UI entrypoint
  tests/
    test_nodes_infer.py
    test_utils.py
```
>>>>>>> 5c3035d (add monitoring and tests)
