"""
Linux Web Dashboard - Disk API Route
Disk 관련 API 엔드포인트를 정의하는 모듈입니다.
"""

from fastapi import APIRouter

from app.schemas.disk import DiskResponse
from app.services.disk import get_disk_metrics

router = APIRouter()


@router.get("/metrics/disk", response_model=DiskResponse)
def read_disk_metrics() -> DiskResponse:
    data = get_disk_metrics()
    return DiskResponse(**data)
