from fastapi import FastAPI

from app.api.routes.cpu import router as cpu_router
from app.api.routes.health import router as health_router
from app.api.routes.memory import router as memory_router
from app.api.routes.network import router as network_router

app = FastAPI(title="Linux Web Dashboard API", version="1.0.0")


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Linux Web Dashboard API!",
    }


app.include_router(health_router)
app.include_router(memory_router)
app.include_router(network_router)
app.include_router(cpu_router)
