# 🏦 Multi-Agent Financial Intelligence Platform (LangGraph Version)

This project implements a modern multi-agent financial intelligence platform using **LangGraph**, open-source LLMs, and market data tools. It processes natural language investment queries, handles spelling errors and company names if ticker symbols are incorrect, extracts the most recent ticker symbols using search tools like Tavily, scrapes market and qualitative data from sources such as Yahoo Finance and news sites, performs in-depth analysis, and delivers structured, actionable recommendations, including price charts and portfolio allocation suggestions.

The system integrates crawler scripts, multiple LLM-driven agents, and external APIs to deliver high-quality insights for investors, analysts, and automated trading tools.

## 📊 System Architecture

![System Architecture Diagram](assets/diagram.png)

## 📊 Data Flow

The workflow is carried out in the following stages:

1. **User Query**

   - The input can be a **natural language query**, e.g., "invest in renewable energy" or "Apple company."
   - Alternatively, it can be a **ticker symbol**, e.g., `AAPL`, `TSLA`.
   - The query is sent to the **Ticker Inference Agent**, which extracts the relevant ticker symbol.

2. **Ticker Inference Agent**

   - If the input is a valid ticker, it directly returns the ticker.
   - If the input is a company name or a **misspelled ticker**, it infers the most relevant ticker symbol.
   - If the input contains an **outdated ticker symbol**, it finds and returns the current symbol (e.g., `FB` → `META`).
   - This ensures that all downstream agents use the correct ticker symbol.

3. **Crawler Agent**

   - Fetches data from multiple sources, including:
     - Yahoo Finance
     - Finnhub
     - Tavily
     - NewsAPI
   - It generates raw summaries, financial metrics, and news content for the selected ticker.

4. **Analysis Agent (Groq LLaMA)**

   - Performs both quantitative and qualitative analysis on the crawled data.
   - Provides stock outlook summaries based on the collected data.

5. **Recommender Agent**

   - Generates actionable investment guidance, such as:
     - Buy / Hold / Sell recommendations
     - Portfolio allocation suggestions
     - Risk management strategies

---

## 🌟 Key Features

- **Ticker Handling**: Automatically corrects outdated or misspelled tickers using LLM reasoning and search tools.
- **Portfolio Awareness**: Extracts portfolio allocation suggestions and visualizes them for the user.
- **Streaming Output**: Results from each node are displayed progressively in the frontend.
- **Integration of Quantitative & Qualitative Data**: Combines financial metrics with market news and insights.
- **Graph-Oriented Orchestration**: Uses **LangGraph** and **LangChain** to efficiently manage workflows between agents.
- **Robust Error Handling & Logging**: Detects missing or outdated data and logs it accordingly.
- **User-Friendly Interface**: Features a simple Gradio interface, including charts and Markdown-formatted output.

---

## 📈 Technology Stack

- **Python 3.10+**
- **LangGraph**: Modern, graph-based orchestration of agents
- **LangChain**: For prompt chaining and agent workflows
- **LLM APIs**: Gemini-2.0-Flash, Groq LLaMA 3.1 8B
- **Market Data**: Yahoo Finance, Finnhub, Tavily, NewsAPI
- **Visualization**: Matplotlib, Recharts, Markdown formatting in the frontend

---

## 🔮 Future Enhancements

- Backtesting of recommended portfolios
- Expanded data sources (Bloomberg, TradingView)
- Support for options and derivatives
- Interactive dashboards with portfolio simulation and risk modeling

---

## 🛠 How to Use

1. Clone the repository and navigate to the project folder:

   ```bash
   git clone https://github.com/AI-lab-sh/Multi-agent-finance-analysis-by-langgraph
   cd lang-graph
