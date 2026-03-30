# System Disk Metrics

리눅스 시스템의 `/proc/diskstats`를 파싱하여 디스크 I/O 관련 raw counter를 수집합니다.

## 1. 데이터 흐름 (Data Flow)
1. **Parser** (`parsers/disk.py`): `/proc/diskstats` 파일에서 디스크 장치별 raw counter를 읽어옴.
2. **Service** (`services/disk.py`): parser 결과를 API 응답 형태로 정리함.
3. **Route** (`api/routes/disk.py`): FastAPI 엔드포인트를 통해 JSON 형태로 반환.

## 2. 설계 기준 (Design Notes)
- 초기 버전에서는 주요 디스크 장치만 노출합니다.
- `loop*`, `ram*`, `sr*`, partition entry는 제외합니다.
- 반환하는 주요 필드는 아래와 같습니다.
  - `reads_completed`
  - `writes_completed`
  - `sectors_read`
  - `sectors_written`

## 3. 실행 및 테스트 (How to Run)

### CLI 실행 (Unit Test)
반드시 `backend` 위치에서 모듈 모드로 실행해야 합니다.

```bash
cd backend
python3 -m app.services.disk
```

### API 서버 실행 및 확인
```bash
uvicorn app.main:app --reload
```

#### Curl 테스트 결과
```bash
curl -s http://127.0.0.1:8000/metrics/disk | jq
{
  "devices": [
    {
      "device": "sda",
      "reads_completed": 20490,
      "writes_completed": 9346,
      "sectors_read": 3571504,
      "sectors_written": 487816
    }
  ]
}
```
