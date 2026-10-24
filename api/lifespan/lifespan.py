from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.client_management.mysql_client import mysql_client_management
from app.client_management.tavily_client import tavily_client_management
from api.monitor.monitor import manager
import asyncio


@asynccontextmanager
async def lifespan(app:FastAPI):

    loop = asyncio.get_running_loop()
    manager.set_loop(loop)
    print(f"[Server] WebSocket Manager bound to loop:{id(loop)}")

    yield

    mysql_client_management.close()
    tavily_client_management.close()





