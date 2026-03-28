"""
Linux Web Dashboard - Memory Schema
Pydantic 모델을 사용하여 memory metrics 정보를 표현하는 스키마를 정의하는 모듈입니다.
"""
from pydantic import BaseModel

class MemoryResponse(BaseModel):
    """
    Memory metrics response schema.
      - total_kb: 총 메모리 용량 (KB)
      - available_kb: 사용 가능한 메모리 용량 (KB)
      - used_kb: 사용 중인 메모리 용량 (KB)
      - usage_percent: 메모리 사용률 (%)
    """
    total_kb: int
    available_kb: int
    used_kb: int
    usage_percent: float