from typing import List
from infrastructure.cache.chat_history_redis import get_redis
from langchain_core.messages import AIMessage
from domain.log.logger import get_logger
from fastapi import FastAPI
from wikipedia import summary
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel

app = FastAPI()


def get_current_time(*args, **kwargs):
    """Returns the current time in HH:MM AM/PM format
    """
    now = datetime.now()
    return now.strftime("%I:%M %p")


def search_wikipedia(query: str):
    """_summary_

    Args:
        query (str): _description_
    """
    try:
        return summary(query, sentences=2)
    except Exception as e:
        return "I couldn't find any information of that"


def tools_generator() -> List[Tool]:
    return [Tool(name="Time",
                 description="useful when you need to get the current time",
                 func=get_current_time)]


tools = tools_generator()
prompt = hub.pull("hwchase17/structured-chat-agent")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)


class AgentRequest(BaseModel):
    session_id: str
    content: str

@app.post("/invoke")
async def root(request: AgentRequest):
    history = get_redis(session_id=request.session_id)
    memory = ConversationBufferMemory(
        chat_memory=history, memory_key="chat_history", return_messages=True)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools,
                                                        handle_parsing_errors=True, memory=memory)
    response = agent_executor.invoke({"input": request.content})
    bot_message = response.get("output")
    return {"response": bot_message, "session_id": request.session_id}
