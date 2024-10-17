from fastapi import APIRouter
from infrastructure.web.routes.invoke_agents.invoke_agents_route import invoke_route
routers = APIRouter()

routers.include_router(invoke_route)
