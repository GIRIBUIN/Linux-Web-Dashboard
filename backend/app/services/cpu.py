"""
Linux Web Dashboard - CPU Service
CPU 사용량을 계산하는 서비스 모듈입니다.
"""

import time

from app.parsers.cpu import parse_cpu_info


def get_cpu_metrics(interval: float = 1.0) -> dict:
    """
    CPU metrics를 계산하여 반환합니다.

    Args:
        interval (float): CPU 사용량 계산을 위한 시간 간격 (초 단위, 기본값: 1.0)

    Returns:
        dict: {"usage_percent": float, "raw": {...}} 형태의 딕셔너리
    """
    first = parse_cpu_info()
    time.sleep(interval)
    second = parse_cpu_info()

    first_total = (
        first["user"]
        + first["nice"]
        + first["system"]
        + first["idle"]
        + first["iowait"]
        + first["irq"]
        + first["softirq"]
        + first["steal"]
    )

    second_total = (
        second["user"]
        + second["nice"]
        + second["system"]
        + second["idle"]
        + second["iowait"]
        + second["irq"]
        + second["softirq"]
        + second["steal"]
    )

    first_idle = first["idle"] + first["iowait"]
    second_idle = second["idle"] + second["iowait"]

    total_delta = second_total - first_total
    idle_delta = second_idle - first_idle

    if total_delta <= 0:
        usage_percent = 0.0
    else:
        usage_percent = ((total_delta - idle_delta) / total_delta) * 100

    return {
        "usage_percent": round(usage_percent, 2),
        "raw": {
            "user": second["user"],
            "system": second["system"],
            "idle": second["idle"],
        },
    }


if __name__ == "__main__":
    print("[Test] CPU Metrics:", get_cpu_metrics())
