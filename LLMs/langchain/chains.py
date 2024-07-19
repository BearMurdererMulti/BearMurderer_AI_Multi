from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

MODEL = "gpt-4o"
# MODEL = "gpt-4-1106-preview"


def define_llm_chain(key, prompt):
    llm = ChatOpenAI(model=MODEL, openai_api_key=key)
    return LLMChain(
        prompt=prompt,
        llm=llm,
        verbose=True,
    )