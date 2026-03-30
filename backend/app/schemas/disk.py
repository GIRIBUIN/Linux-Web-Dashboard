"""
Linux Web Dashboard - Disk Schemas
Pydantic 모델을 사용하여 disk metrics 정보를 표현하는 스키마를 정의하는 모듈입니다.
"""

from pydantic import BaseModel


class DiskDeviceResponse(BaseModel):
    device: str
    reads_completed: int
    writes_completed: int
    sectors_read: int
    sectors_written: int


class DiskResponse(BaseModel):
    devices: list[DiskDeviceResponse]
