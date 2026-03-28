# System Memory Metrics

리눅스 시스템의 `/proc/meminfo`를 파싱하여 가용 메모리 및 사용률을 계산합니다.

## 1. 데이터 흐름 (Data Flow)
1. **Parser** (`parsers/memory.py`): `/proc/meminfo` 파일에서 `MemTotal`, `MemAvailable` 값을 읽어옴.
2. **Service** (`services/memory.py`): 읽어온 값을 이용해 `used_kb` 및 `usage_percent` 계산.
3. **Route** (`api/routes/health.py`): FastAPI 엔드포인트를 통해 JSON 형태로 반환.



## 2. 실행 및 테스트 (How to Run)

### CLI 실행 (Unit Test)
반드시 `backend` 위치에서 모듈 모드로 실행해야 합니다.

```bash
cd backend
python3 -m app.services.memory
```

### API 서버 실행 및 확인
```bash
uvicorn app.main:app --reload
```

#### Curl 테스트 결과
```bash
curl -s http://127.0.0.1:8000/metrics/memory | jq
{
  "total_kb": 12245760,
  "available_kb": 9153032,
  "used_kb": 3092728,
  "usage_percent": 25.26
}
```
