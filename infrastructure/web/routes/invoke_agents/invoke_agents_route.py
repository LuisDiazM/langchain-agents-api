from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.web.routes.invoke_agents.models_req_resp import AgentRequest, ChatbotResponse
from infrastructure.cache.chat_history_redis import get_redis
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
import os

from domain.agents.agent_generator import create_agent
from domain.agents.tools_generator import tools_generator

invoke_route = APIRouter(tags=["Interact with agent"])

#Depends fail to inyect
agent = create_agent()
tools = tools_generator()

@invoke_route.post("/invoke")
async def root(request: AgentRequest)->ChatbotResponse:
    try:
        environment = os.getenv("ENV")
        is_debug = True
        if environment.upper() == "PROD":
            is_debug = False
        history = get_redis(session_id=request.session_id)
        memory = ConversationBufferMemory(
            chat_memory=history, memory_key="chat_history", return_messages=True)
        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, 
                                                            tools=tools,
                                                            handle_parsing_errors=True, 
                                                            memory=memory,
                                                            verbose=is_debug)
        response = agent_executor.invoke({"input": request.content})
        bot_message = response.get("output")
        return ChatbotResponse(response=bot_message, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)