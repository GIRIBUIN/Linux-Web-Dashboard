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
            "user": int(parts[1]),  # user mode: user가 CPU를 사용한 시간
            "nice": int(
                parts[2]
            ),  # nice mode: nice 프로세스가 CPU를 사용한 시간. nice 프로세스는 우선순위가 낮은 프로세스
            "system": int(parts[3]),  # system mode: 시스템 프로세스가 CPU를 사용한 시간
            "idle": int(parts[4]),  # idle mode: CPU가 유휴 상태에 소모한 시간
            "iowait": int(parts[5]),  # iowait mode: I/O 대기 중인 시간
            "irq": int(
                parts[6]
            ),  # irq mode: 하드웨어 인터럽트 처리 시간. 예를 들어, 키보드나 마우스 입력과 같은 하드웨어 이벤트가 발생했을 때 CPU가 이를 처리하는 시간
            "softirq": int(
                parts[7]
            ),  # softirq mode: 소프트웨어 인터럽트 처리 시간. 예를 들어, 네트워크 패킷 처리와 같은 소프트웨어 이벤트가 발생했을 때 CPU가 이를 처리하는 시간
            "steal": int(
                parts[8]
            ),  # steal mode: 가상화 환경에서 다른 가상 머신이 CPU를 사용한 시간
            "guest": int(parts[9]),  # guest mode: 가상 머신이 CPU를 사용한 시간
            "guest_nice": int(
                parts[10]
            ),  # guest_nice mode: nice 프로세스가 가상 머신에서 CPU를 사용한 시간
        }
    return cpu_info


if __name__ == "__main__":
    cpu_info = parse_cpu_info()
    print("[Test] CPU Info:", cpu_info)
