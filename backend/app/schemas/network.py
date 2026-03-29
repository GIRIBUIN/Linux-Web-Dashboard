"""
Linux Web Dashboard - Network Schema
Pydantic 모델을 사용하여 network metrics 정보를 표현하는 스키마를 정의하는 모듈입니다.
"""

from pydantic import BaseModel


class NetworkInterfaceResponse(BaseModel):
    interface: str
    rx_bytes: int
    tx_bytes: int
    rx_packets: int
    tx_packets: int


class NetworkResponse(BaseModel):
    interfaces: list[NetworkInterfaceResponse]