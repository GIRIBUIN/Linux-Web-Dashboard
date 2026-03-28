"""
Linux Web Dashboard - Memory Service
parsers/memory.py 모듈을 호출해서 user_kb, usage_percent를 계산하는 서비스 모듈입니다.
"""
from app.parsers.memory import parse_memory_info

def get_memory_metrics() -> dict[str, float | int]:
    """
    Memory Metrics를 계산하여 반환합니다.

    Returns:
        dict[str, float | int]: {"total_kb": int, "available_kb": int, "used_kb": int, "usage_percent": float} 형태의 딕셔너리
    """
    memory_info = parse_memory_info()

    total_kb = memory_info["total_kb"]
    available_kb = memory_info["available_kb"]
    used_kb = total_kb - available_kb
    usage_percent = (used_kb / total_kb) * 100 if total_kb > 0 else 0.0

    return {
        "total_kb": total_kb,
        "available_kb": available_kb,
        "used_kb": used_kb,
        "usage_percent": round(usage_percent, 2),
    }

if __name__ == "__main__":
    memory_metrics = get_memory_metrics()
    print("[Test] Memory Metrics:", memory_metrics)