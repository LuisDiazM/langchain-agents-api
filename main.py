from fastapi import FastAPI
from infrastructure.web.routes.routes import routers

app = FastAPI()
app.include_router(routers)
