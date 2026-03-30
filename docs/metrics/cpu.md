# System CPU Metrics

리눅스 시스템의 `/proc/stat`를 파싱하여 CPU 사용률을 계산합니다.

## 1. 데이터 흐름 (Data Flow)
1. **Parser** (`parsers/cpu.py`): `/proc/stat` 파일의 첫 번째 `cpu` 라인에서 CPU time counter 값을 읽어옴.
2. **Service** (`services/cpu.py`): 두 번 읽은 CPU counter 값의 차이(delta)를 계산하여 `usage_percent`를 구함.
3. **Route** (`api/routes/cpu.py`): FastAPI 엔드포인트를 통해 JSON 형태로 반환.

## 2. 계산 방식 (Calculation Idea)
CPU usage는 `/proc/stat`의 누적 counter를 한 번 읽는 것만으로는 계산할 수 없습니다.  
따라서 짧은 시간 간격으로 두 번 읽은 뒤, total time과 idle time의 차이를 이용해 사용률을 계산합니다.

- `total = user + nice + system + idle + iowait + irq + softirq + steal`
- `idle_all = idle + iowait`
- `total_delta = total_t2 - total_t1`
- `idle_delta = idle_t2 - idle_t1`
- `usage_percent = (total_delta - idle_delta) / total_delta * 100`

## 3. 실행 및 테스트 (How to Run)

### CLI 실행 (Unit Test)
반드시 `backend` 위치에서 모듈 모드로 실행해야 합니다.

```bash
cd backend
python3 -m app.services.cpu
```

### API 서버 실행 및 확인
```bash
uvicorn app.main:app --reload
```

#### Curl 테스트 결과
```bash
curl -s http://127.0.0.1:8000/metrics/cpu | jq
{
  "usage_percent": 1.93,
  "raw": {
    "user": 19469,
    "system": 17844,
    "idle": 2257408
  }
}
```
