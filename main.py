from typing import List
from langchain_openai import ChatOpenAI
from datetime import datetime
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage, AIMessage, ChatMessage
from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_structured_chat_agent
from wikipedia import summary
from langchain_redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import os
def get_current_time(*args, **kwargs):
    """Returns the current time in HH:MM AM/PM format
    """
    now = datetime.now()
    return now.strftime("%I:%M %p")

def search_wikipedia(query:str):
    """_summary_

    Args:
        query (str): _description_
    """
    try:
        return summary(query, sentences=2)
    except Exception as e:
        return "I couldn't find any information of that"

def tools_generator()->List[Tool]:
    return [Tool(name="Time",
              description="useful when you need to get the current time",
              func=get_current_time)]


def get_redis(session_id:str)->BaseChatMessageHistory:
    REDIS_URL= os.getenv("REDIS_URL")
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL, ttl=3600)


if __name__ == "__main__":
    tools = tools_generator()
    prompt = hub.pull("hwchase17/structured-chat-agent")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    history = get_redis("xxxxxx")
    memory = ConversationBufferMemory(chat_memory=history, memory_key="chat_history", return_messages=True)
    agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools,
                                                         verbose=True, handle_parsing_errors=True, memory=memory)
    
    initial_message = "Eres un asistente virtual que habla español y responderás en ese idiomasu\n "
    history.add_message(message=SystemMessage(content=initial_message))
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = agent_executor.invoke({"input": user_input})
        bot_message = response.get("output")
        print(f"Bot: {bot_message}")
    history.clear()

