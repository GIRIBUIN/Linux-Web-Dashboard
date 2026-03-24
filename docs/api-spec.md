# API Specification

## 1. Overview
### 1.1 Base URL
- Local development 기준 `http://localhost:8000`이다.

### 1.2 Response Format
- API 응답 형식은 JSON으로 통일한다.

### 1.3 API Goals
- Linux `/proc` 기반 메트릭을 단순하고 일관된 형태로 제공한다.
- 각 endpoint가 명확한 역할을 갖도록 설계한다.

## 2. Common Response Policy
### 2.1 Success Response
- 성공 시 적절한 HTTP status code와 JSON body를 반환한다.
- metric endpoint는 요청한 메트릭 데이터를 JSON 형식으로 반환한다.

### 2.2 Error Response
- 실패 시 HTTP error status code와 오류 메시지를 포함한 JSON 응답을 반환한다.

```json
{
    "detail": "error message"
}
```
## 3. Endpoints
### 3.1 GET /health
- Description: 서버가 정상적으로 실행 중인지 확인하는 health check endpoint
- Method: `GET`
- Request Body: 없음
- Query parameters: 없음
- Success Response: `200 OK`

```json
{
    "status": "ok"
}
```

### 3.2 GET /metrics/cpu
- Description: `/proc/stat` 기반으로 계산한 CPU usage 메트릭을 반환하는 endpoint
- Method: `GET`
- Request Body: 없음
- Query Parameters: 없음
- Success Response: `200 OK`

```json
{
  "usage_percent": 12.3,
  "raw": {
    "user": 12345,
    "system": 1234,
    "idle": 12345
  }
}
```

### 3.3 GET /metrics/memory
- Description: `/proc/meminfo` 기반 memory usage 메트릭을 반환하는 endpoint
- Method: `GET`
- Request Body: 없음
- Query Parameters: 없음
- Success Response: `200 OK`
 
 ```json
{
    "total_kb": 1234567,
    "available_kb": 1234567,
    "used_kb": 1234567,
    "usage_percent": 12.34
}
```

### 3.4 GET /metrics/network
- Description: `/proc/net/dev` 기반 네트워크 인터페이스별 송수신 메트릭을 반환하는 endpoint
- Method: `GET`
- Request Body: 없음
- Query Parameters: 없음
- Success Response: `200 OK`

```json
{
  "interfaces": [
    {
      "name": "eth0",
      "rx_bytes": 123456,
      "tx_bytes": 123456,
      "rx_packets": 1234,
      "tx_packets": 123
    }
  ]
}
```

### 3.5 GET /metrics/disk
- Description: `/proc/diskstats` 기반 디스크 I/O 메트릭을 반환하는 endpoint
- Method: `GET`
- Request Body: 없음
- Query Parameters: 없음
- Success Response: `200 OK`

```json
{
  "devices": [
    {
      "name": "sda",
      "reads_completed": 123456,
      "writes_completed": 234567,
      "sectors_read": 1234567,
      "sectors_written": 2345678
    }
  ]
}
```

## 4. Request / Response Schema
### 4.1 Health Response
- 서버 상태 확인용 응답 schema

```json
{
    "status": "ok"
}
```

Fields:
- `status`: 서버 상태 문자열

### 4.2 CPU Metrics Response
- `/proc/stat` 기반으로 계산한 CPU 메트릭 응답 schema

```json
{
  "usage_percent": 12.3,
  "raw": {
    "user": 12345,
    "system": 1234,
    "idle": 12345
  }
}
```

Fields:
- `usage_percent`: CPU usage percentage
- `raw.user`: user mode cumulative CPU time
- `raw.system`: system mode cumulative CPU time
- `raw.idle`: idle cumulative CPU time

Notes:
- `usage_percent`는 two-sample delta 계산 결과이다.
- `raw.user`, `raw.system`, `raw.idle` 값은 `/proc/stat`의 누적 counter를 기반으로 한다.

### 4.3 Memory Metrics Response
- `/proc/meminfo` 기반 memory usage 응답 schema

 ```json
{
    "total_kb": 1234567,
    "available_kb": 1234567,
    "used_kb": 1234567,
    "usage_percent": 12.34
}
```

Fields:
- `total_kb`: total memory size in KB
- `available_kb`: estimated available memory in KB
- `used_kb`: used memory in KB
- `usage_percent`: memory usage percentage

Notes:
- `used_kb`는 `total_kb - available_kb`로 계산한다.
- `MemFree` 대신 `MemAvailable`을 기준으로 사용한다.

### 4.4 Network Metrics Response
- `/proc/net/dev` 기반 네트워크 메트릭 응답 schema

```json
{
  "interfaces": [
    {
      "name": "eth0",
      "rx_bytes": 123456,
      "tx_bytes": 123456,
      "rx_packets": 1234,
      "tx_packets": 123
    }
  ]
}
```

Fields:
- `interfaces`: network interface metric list
- `name`: interface name
- `rx_bytes`: received bytes
- `tx_bytes`: transmitted bytes
- `rx_packets`: received packets
- `tx_packets`: transmitted packets

### 4.5 Disk Metrics Response
- `/proc/diskstats` 기반 디스크 I/O 메트릭 응답 schema

```json
{
  "devices": [
    {
      "name": "sda",
      "reads_completed": 157698,
      "writes_completed": 345678,
      "sectors_read": 1234567,
      "sectors_written": 2345678
    }
  ]
}
```

Fields:
- `devices`: disk device metric list
- `name`: device name
- `reads_completed`: completed read operations
- `writes_completed`: completed write operations
- `sectors_read`: sectors read
- `sectors_written`: sectors written

## 5. Status Codes
- `200 OK`: 요청이 정상적으로 처리되었을 때 반환한다.
- `400 Bad Request`: 잘못된 요청 형식이나 지원하지 않는 parameter가 전달된 경우 사용할 수 있다.
- `404 Not Found`: 존재하지 않는 endpoint에 접근한 경우 반환될 수 있다.
- `500 Internal Server Error`: `/proc` 파일 읽기 실패, parsing 실패, 내부 계산 오류 등 서버 내부 문제 발생 시 반환한다.
- `503 Service Unavailable`: 지원하지 않는 실행 환경이거나, 일시적으로 메트릭 수집이 불가능한 경우 고려할 수 있다.

## 6. Error Handling
### 6.1 Standard Error Format
- 에러 응답은 JSON 형식으로 통일한다.
- FastAPI 기본 스타일에 맞춰 `detail` 필드를 사용한다.
- 내부 디버깅용 상세 정보는 로그에 남기고, API 응답에는 필요한 수준만 노출한다.

```json
{
  "detail": "error message"
}
```

Fields:
- `detail`: 오류 원인을 설명하는 메시지

### 6.2 Typical Error Cases
- `/proc` 파일이 존재하지 않거나 읽을 수 없는 경우
- Linux 이외의 환경에서 실행된 경우
- `/proc` 파일 형식이 예상과 달라 parsing에 실패한 경우
- CPU usage 계산 시 두 시점 샘플링 과정에서 오류가 발생한 경우
- 지원하지 않는 resource나 잘못된 endpoint 요청이 들어온 경우

- `500 Internal Server Error`
  - `/proc/meminfo` read failed
  - failed to parse `/proc/stat`
  - disk metric calculation failed

- `503 Service Unavailable`
  - unsupported platform: Linux `/proc` is required

- `404 Not Found`
  - requested endpoint does not exist


## 7. Testing Plan
### 7.1 Manual Testing
- 각 endpoint를 직접 호출하여 응답 형식과 값을 확인한다.
- `/health`, `/metrics/cpu`, `/metrics/memory`, `/metrics/network`, `/metrics/disk`를 중심으로 테스트한다.
- Linux 환경에서 `/proc` 파일 값을 직접 확인한 뒤, API 응답과 비교하여 파싱 및 계산 결과가 올바른지 검증한다.

Manual test checklist:
- [ ] `GET /health`가 `200 OK`와 정상 JSON을 반환하는지 확인
- [ ] `GET /metrics/memory`가 `MemTotal`, `MemAvailable` 기반 계산 결과를 올바르게 반환하는지 확인
- [ ] `GET /metrics/cpu`가 비정상적인 음수 값이나 100% 초과 값을 반환하지 않는지 확인
- [ ] `GET /metrics/network`가 인터페이스별 값을 정상적으로 반환하는지 확인
- [ ] `GET /metrics/disk`가 디스크 장치별 값을 정상적으로 반환하는지 확인
- [ ] Linux 이외 환경 또는 `/proc` 읽기 실패 상황에서 적절한 에러 응답이 반환되는지 확인

### 7.2 Swagger / ReDoc
- FastAPI가 제공하는 Swagger UI와 ReDoc을 사용하여 endpoint 문서와 응답 구조를 확인한다.
- Swagger UI는 `/docs`, ReDoc은 `/redoc` 경로에서 확인한다.
- 각 endpoint의 request/response schema가 의도한 형태와 일치하는지 검토한다.

Testing points:
- endpoint 목록이 올바르게 노출되는지 확인
- response model이 의도한 필드명과 타입으로 표시되는지 확인
- example response와 실제 응답 구조가 크게 어긋나지 않는지 확인
- API 문서가 초기 설계 문서와 일관되는지 확인

### 7.3 curl Examples
- CLI 환경에서 빠르게 endpoint 동작을 확인하기 위해 `curl` 명령을 사용한다.

```bash
curl http://localhost:8000/health
```

```bash
curl http://localhost:8000/metrics/cpu
```

```bash
curl http://localhost:8000/metrics/memory
```

```bash
curl http://localhost:8000/metrics/network
```

```bash
curl http://localhost:8000/metrics/disk
```

## 8. Future API Extensions
- 특정 인터페이스나 디스크 장치만 조회할 수 있도록 Query Parameter 기반 filtering을 추가할 수 있다.
- 현재 raw counter 중심 응답 외에, bytes/sec, reads/sec 같은 rate 기반 메트릭 endpoint를 추가할 수 있다.
- threshold 설정 및 경고 상태를 조회하는 API를 추가할 수 있다.
- 메트릭 이력을 조회할 수 있는 history endpoint를 확장 기능으로 고려할 수 있다.
- 추후 필요하다면 Prometheus exporter 형태나 외부 모니터링 도구 연동용 endpoint를 추가할 수 있다.

Possible extensions:
- `GET /metrics/network?interface=eth0`
- `GET /metrics/disk?device=sda`
- `GET /metrics/cpu/rate`
- `GET /alerts`
- `GET /metrics/history`