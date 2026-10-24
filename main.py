from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router.router import api_router
from api.lifespan.lifespan import lifespan
import uvicorn

app = FastAPI(lifespan=lifespan,title="DeepAgent")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8080,reload=True)
























