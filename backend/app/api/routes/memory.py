"""
Linux Web Dashboard - Memory Route
메모리 관련 API 엔드포인트를 정의하는 모듈입니다.
"""
from fastapi import APIRouter

from app.schemas.memory import MemoryResponse
from app.services.memory import get_memory_metrics

router = APIRouter()


@router.get("/metrics/memory", response_model=MemoryResponse)
def read_memory_metrics() -> MemoryResponse:
    data = get_memory_metrics()
    return MemoryResponse(**data)
