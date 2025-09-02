from state import StockState
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agents import llama
from monitoring import instrument


def highlight_recommendation(html_text: str) -> str:
    lc = html_text.lower()
    if "buy" in lc:
        return f"<span style='color:white; background-color:green; padding:2px 6px; border-radius:4px;'>BUY</span> {html_text}"
    elif "sell" in lc:
        return f"<span style='color:white; background-color:red; padding:2px 6px; border-radius:4px;'>SELL</span> {html_text}"
    elif "hold" in lc:
        return f"<span style='color:black; background-color:yellow; padding:2px 6px; border-radius:4px;'>HOLD</span> {html_text}"
    else:
        return html_text


@instrument("recommend")
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
        input_variables=["analysis", "ticker"],
    )
    chain = LLMChain(llm=llama, prompt=prompt)
    recommendations = chain.run(ticker=state["ticker"], analysis=state["analysis"])
    state["recommendations"] = recommendations
    return state


