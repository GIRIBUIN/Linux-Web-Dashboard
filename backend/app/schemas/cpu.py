"""
Linux Web Dashboard - CPU Schema
Pydantic 모델을 사용하여 CPU metrics 정보를 표현하는 스키마를 정의하는 모듈입니다.
"""

from pydantic import BaseModel


class CpuRawResponse(BaseModel):
    """
    user: CPU가 사용자 프로세스에 소비한 시간 (ms)
    system: CPU가 시스템 프로세스에 소비한 시간 (ms)
    idle: CPU가 유휴 상태에 소비한 시간 (ms)
    """

    user: int
    system: int
    idle: int


class CpuResponse(BaseModel):
    """
    usage_percent: CPU 사용률 (%)
    raw: 원시 CPU metrics 정보
    """

    usage_percent: float
    raw: CpuRawResponse
