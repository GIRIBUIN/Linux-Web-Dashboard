"""
Linux Web Dashboard - CPU Schema
Pydantic 모델을 사용하여 CPU metrics 정보를 표현하는 스키마를 정의하는 모듈입니다.
"""

from pydantic import BaseModel


class CpuRawResponse(BaseModel):
    user: int
    system: int
    idle: int


class CpuResponse(BaseModel):
    usage_percent: float
    raw: CpuRawResponse
