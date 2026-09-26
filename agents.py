from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.schema import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

#model setup
llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

#1st agent
def build_search_agent():
    return create_agent(
        llm=llm,
        tools=[web_search, scrape_url],
        system_message=SystemMessage(content="You are a helpful research assistant. You have access to the following tools: web_search and scrape_url. Use them to gather information and provide accurate answers."),
        #human_message=HumanMessage(content="Please use the tools to find information on the given topic."),
        #output_parser=StrOutputParser(),
    )

#2nd agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        #system_message=SystemMessage(content="You are a helpful research assistant. You have access to the following tool: scrape_url. Use it to gather information and provide accurate answers."),
       #human_message=HumanMessage(content="Please use the tool to find information on the given topic
    )
#writer chain
writer_prompt =  ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain=writer_prompt | llm |StrOutputParser()

#critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
