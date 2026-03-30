"""
Linux Web Dashboard - CPU Info Parser
/proc/stat 파일을 파싱하여 CPU 사용률 정보를 추출하는 모듈입니다
"""


def parse_cpu_info(stat_path: str = "/proc/stat") -> dict[str, int]:
    """
    /proc/stat 파일을 읽어서 CPU 사용률 정보를 추출합니다.

    Args:
        stat_path (str): /proc/stat 파일의 경로 (기본값: "/proc/stat")
    Returns:
        dict[str, int]: {"user": int, "nice": int, "system": int, "idle": int, "iowait": int, "irq": int, "softirq": int, "steal": int, "guest": int, "guest_nice": int} 형태의 딕셔너리
    """

    cpu_info: dict[str, int] = {}

    with open(stat_path, "r") as f:
        line = f.readline().strip()
        parts = line.split()
        if not parts or parts[0] != "cpu":
            raise ValueError("Invalid /proc/stat format: missing 'cpu' line")
        cpu_info = {
            "user": int(parts[1]),
            "nice": int(parts[2]),
            "system": int(parts[3]),
            "idle": int(parts[4]),
            "iowait": int(parts[5]),
            "irq": int(parts[6]),
            "softirq": int(parts[7]),
            "steal": int(parts[8]),
            "guest": int(parts[9]),
            "guest_nice": int(parts[10]),
        }
    return cpu_info


if __name__ == "__main__":
    cpu_info = parse_cpu_info()
    print("[Test] CPU Info:", cpu_info)
