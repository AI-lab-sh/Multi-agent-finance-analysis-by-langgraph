from state import StockState
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agents import llama
from monitoring import instrument


@instrument("analyze")
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
        input_variables=["ticker", "summary"],
    )
    chain = LLMChain(llm=llama, prompt=prompt)
    analysis = chain.run(ticker=state["ticker"], summary=state["summary"])
    state["analysis"] = analysis
    return state


