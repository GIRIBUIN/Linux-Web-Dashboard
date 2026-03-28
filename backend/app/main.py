from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.memory import router as memory_router

app = FastAPI(title="Linux Web Dashboard API", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Linux Web Dashboard API!"
    }

app.include_router(health_router)
app.include_router(memory_router)