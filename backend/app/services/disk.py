"""
Linux Web Dashboard - Disk Service
디스크 메트릭을 수집하는 서비스 모듈입니다.
"""

from app.parsers.disk import parse_disk_info


def get_disk_metrics() -> dict[str, list[dict[str, int | str]]]:
    devices = parse_disk_info()
    return {"devices": devices}


if __name__ == "__main__":
    print("[Test] Disk Metrics:", get_disk_metrics())
