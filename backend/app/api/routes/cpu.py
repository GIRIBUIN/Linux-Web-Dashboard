"""
Linux Web Dashboard - CPU Route
CPU 관련 API 엔드포인트를 정의하는 모듈입니다.
"""

from fastapi import APIRouter

from app.schemas.cpu import CpuResponse
from app.services.cpu import get_cpu_metrics

router = APIRouter()


@router.get("/metrics/cpu", response_model=CpuResponse)
def read_cpu_metrics() -> CpuResponse:
    data = get_cpu_metrics()
    return CpuResponse(**data)
