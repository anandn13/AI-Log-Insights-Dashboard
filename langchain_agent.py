from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


PROMPT = """
You are a helpful log analysis assistant.
Given the following logs:
{logs}

1) Provide a concise summary (2-4 sentences).
2) List up to 10 unique error/warning patterns and suggest root causes and one mitigation each.
3) Provide suggested search queries to find similar issues.

Output as JSON with keys: summary, issues (list of {pattern, count, suggestion}).
"""


def analyze_logs_with_llm(log_texts: str, openai_api_key: str=None):
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    template = PromptTemplate(input_variables=["logs"], template=PROMPT)
    chain = LLMChain(llm=llm, prompt=template)
    out = chain.run({"logs": log_texts})
    return out


