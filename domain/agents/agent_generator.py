from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_structured_chat_agent

from domain.agents.tools_generator import tools_generator

def create_agent():
    tools = tools_generator()
    prompt = hub.pull("hwchase17/structured-chat-agent")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)
    return agent