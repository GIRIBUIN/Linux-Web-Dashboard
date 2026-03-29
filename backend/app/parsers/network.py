"""
Linux Web Dashboard - Network Info Parser
/proc/net/dev 파일을 파싱하여 네트워크 인터페이스별로 수신 및 송신된 바이트 수를 추출하는 모듈입니다.
"""


def parse_network_info(
    net_dev_path: str = "/proc/net/dev",
) -> list[dict[str, int | str]]:
    """
    /proc/net/dev 파일을 파싱하여 네트워크 인터페이스별로 수신 및 송신된 바이트 수를 추출합니다.
    Args:
        net_dev_path (str): /proc/net/dev 파일의 경로 (기본값: "/proc/net/dev")
    Returns:
        list[dict[str, int | str]]: 네트워크 인터페이스별로 수신 및 송신된 바이트 수를 포함하는 딕셔너리의 리스트
    """
    interfaces: list[dict[str, int | str]] = []

    with open(net_dev_path, "r") as f:
        lines = f.readlines()[2:]  # 첫 두줄은 헤더

    for line in lines:
        if ":" not in line:
            continue

        parts = line.split(":", 1)
        interface_name = parts[0].strip()
        fields = parts[1].strip().split()
        if len(fields) < 16:
            continue

        interfaces.append(
            {
                "interface": interface_name,
                "rx_bytes": int(fields[0]),
                "rx_packets": int(fields[1]),
                "tx_bytes": int(fields[8]),
                "tx_packets": int(fields[9]),
            }
        )

    return interfaces


if __name__ == "__main__":
    network_info = parse_network_info()
    print("[Test] Network Info:", network_info)
