from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from agents import (
    build_reader_agent,
    build_search_agent,
    critic_chain,
    writer_chain,
)

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
)


# 1. Search agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a web research agent. Search for reliable sources "
            "using the web_search tool. Summarize relevant findings "
            "and preserve the source URLs. Do not invent sources."
        ),
    )


# 2. Webpage reader agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a webpage research agent. Use the scrape_url tool "
            "to read the supplied URLs. Extract relevant facts, dates, "
            "and evidence. Preserve source URLs and identify inaccessible "
            "pages instead of inventing their contents."
        ),
    )


# 3. Research report writer
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured, "
        "factual, insightful, and professional reports. Distinguish "
        "verified facts from uncertainty."
    ),
    (
        "human",
        """Write a research report on the topic below.

Topic: {topic}

Research gathered:
{research}

Use this structure:
1. Introduction
2. Key Findings (at least 3 well-explained points)
3. Conclusion
4. Sources (list the source URLs supplied in the research)

Do not invent facts, quotations, statistics, or URLs.
If evidence is insufficient or conflicting, state that clearly."""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# 4. Research critic
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a rigorous, constructive research critic. Evaluate "
        "accuracy, evidence, source quality, completeness, and clarity."
    ),
    (
        "human",
        """Review the research report below.

Report:
{report}

Use this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
