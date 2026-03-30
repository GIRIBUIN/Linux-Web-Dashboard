"""
Linux Web Dashboard - Memory Info Parser
/proc/meminfo 파일을 파싱하여 Total Memory와 Available Memory 정보를 추출하는 모듈입니다.
"""


def parse_memory_info(meminfo_path: str = "/proc/meminfo") -> dict[str, int]:
    """
    /proc/meminfo 파일을 읽어서 Total Memory와 Available Memory 정보를 추출합니다.

    Args:
        meminfo_path (str): /proc/meminfo 파일의 경로 (기본값: "/proc/meminfo")

    Returns:
        dict[str, int]: {"total_kb": int, "available_kb": int} 형태의 딕셔너리
    """
    meminfo: dict[str, str] = {}

    with open(meminfo_path, "r") as f:
        for line in f:
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                meminfo[key] = value

    total_kb = int(meminfo.get("MemTotal", "0 kB").split()[0])
    available_kb = int(meminfo.get("MemAvailable", "0 kB").split()[0])

    return {
        "total_kb": total_kb,
        "available_kb": available_kb,
    }


if __name__ == "__main__":
    memory_info = parse_memory_info()
    print("[Test] Memory Info:", memory_info)
