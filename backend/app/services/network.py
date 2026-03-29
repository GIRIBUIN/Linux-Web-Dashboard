"""
Linux Web Dashboard - Network Service
네트워크 관련 메트릭을 수집하는 서비스 모듈입니다.
"""

from app.parsers.network import parse_network_info


def get_network_metrics() -> dict[str, list[dict[str, int | str]]]:
    interfaces = parse_network_info()

    return {"interfaces": interfaces}


if __name__ == "__main__":
    print("[Test] Network Metrics:", get_network_metrics())
