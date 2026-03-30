"""
Linux Web Dashboard - Disk Parser
/proc/diskstats를 파싱하여 디스크 I/O 관련 raw counter를 추출한다.
"""


def parse_disk_info(
    diskstats_path: str = "/proc/diskstats",
) -> list[dict[str, int | str]]:
    devices: list[dict[str, int | str]] = []

    with open(diskstats_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 14:
                continue

            device_name = parts[2]

            # Skip common virtual devices
            """
            loop devices: loop0, loop1, ...
            실제 물리 디스크라기보다, 파일을 디스크처럼 연결해서 사용하는 가상 장치
            - 시스템 내부적으로 마운트 포인터로 사용

            ram devices: ram0, ram1, ...
            실제 물리 디스크가 아니라, 시스템 메모리를 디스크처럼 사용하는 가상 장치
            - 시스템 내부적으로 스왑 공간으로 사용

            sr devices: sr0, sr1, ...
            CD-ROM 드라이브를 나타내는 장치 이름
            - 일반적으로 CD/DVD 드라이브로 사용
            """
            if device_name.startswith(("loop", "ram", "sr")):
                continue

            # Skip partition entries for the initial version
            """
            sdXn: sda1, sda2, ...
            nvmeXnY: nvme0p1, nvme0p2,
            실제 물리 디스크의 파티션을 나타내는 이름
            - sda는 첫 번째 SATA 디스크, sdb는 두 번째 SATA 디스크로 디스크 전체를 나타냄
            """
            if (device_name.startswith("sd") and device_name[-1].isdigit()) or (
                "nvme" in device_name and "p" in device_name
            ):
                continue

            devices.append(
                {
                    "device": device_name,  # 디바이스 이름
                    "reads_completed": int(parts[3]),  # 완료된 읽기 요청 수
                    "writes_completed": int(parts[7]),  # 완료된 쓰기 요청 수
                    "sectors_read": int(parts[5]),  # 읽은 섹터 수
                    "sectors_written": int(parts[9]),  # 쓰인 섹터 수
                }
            )

    return devices


if __name__ == "__main__":
    print("[Test] Disk Info:", parse_disk_info())
