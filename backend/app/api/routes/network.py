"""
Linux Web Dashboard - Network Routes
네트워크 관련 API 엔드포인트를 정의하는 모듈입니다.
"""
from fastapi import APIRouter

from app.schemas.network import NetworkResponse
from app.services.network import get_network_metrics

router = APIRouter()


@router.get("/metrics/network", response_model=NetworkResponse)
def read_network_metrics() -> NetworkResponse:
    data = get_network_metrics()
    return NetworkResponse(**data)