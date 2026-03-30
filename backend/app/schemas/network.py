"""
Linux Web Dashboard - Network Schema
Pydantic 모델을 사용하여 network metrics 정보를 표현하는 스키마를 정의하는 모듈입니다.
"""

from pydantic import BaseModel


class NetworkInterfaceResponse(BaseModel):
    """
    interface: 네트워크 인터페이스 이름
    rx_bytes: 수신된 바이트 수
    tx_bytes: 전송된 바이트 수
    rx_packets: 수신된 패킷 수
    tx_packets: 전송된 패킷 수
    """

    interface: str
    rx_bytes: int
    tx_bytes: int
    rx_packets: int
    tx_packets: int


class NetworkResponse(BaseModel):
    """
    interfaces: 네트워크 인터페이스 목록
    """

    interfaces: list[NetworkInterfaceResponse]
