# Decision Log

> 중요한 기술적 결정과 그 이유를 기록합니다.
> 무엇을 선택했는지보다, 왜 그렇게 선택했는지에 집중합니다.

---

## Writing Rule

다음 경우에 작성:
- 여러 기술적 선택지 중 하나를 결정했을 때
- 프로젝트 범위를 확정하거나 축소했을 때
- 아키텍처나 구현 방향을 변경했을 때
- 의도적으로 어떤 trade-off를 받아들였을 때

좋은 기록은 아래 질문에 답할 수 있어야 함:
- 무엇을 결정했는가?
- 왜 그렇게 결정했는가?
- 다른 대안은 무엇이 있었는가?
- 어떤 trade-off를 감수했는가?
- 이 결정이 어떤 영향을 주는가?

---

## Template

## Decision: [short title]

- **Date:** YYYY-MM-DD
- **Status:** Proposed / Accepted / Replaced / Deprecated

### Context
What problem or situation led to this decision?

### Decision
What was chosen?

### Alternatives Considered
- Option A:
- Option B:
- Option C:

### Reason
Why was this option chosen?

### Trade-offs
What was gained and what was sacrificed?

### Impact
What changes because of this decision?

---

## Entries
---
## Decision: `psutil` 대신 `/proc` 직접 파싱 사용

- **Date:** 2026-03-24
- **Status:** Accepted

### Context
이 프로젝트의 목표는 단순히 시스템 메트릭을 보여주는 것이 아니라, Linux가 메트릭 정보를 어떻게 제공하는지 직접 이해하는 것이다.

### Decision
고수준 시스템 라이브러리인 `psutil` 대신 Linux `/proc` filesystem을 직접 파싱하는 방식으로 구현한다.

### Alternatives Considered
- `psutil`
- `top`, `free`, `vmstat` 같은 shell command 활용
- `/proc` 직접 파싱

### Reason
Linux 기반 백엔드/인프라 직무와 연결되는 설명 포인트를 만들 수 있다.

### Trade-offs
- 장점:
  - Linux 내부 동작 이해에 도움이 됨
  - 메트릭 수집 과정을 직접 구현할 수 있음
- 단점:
  - 구현 복잡도가 높아짐
  - parsing과 validation을 직접 처리해야 함

### Impact
parser 모듈을 직접 구현해야 하며, 각 메트릭 계산 방식도 문서와 코드로 명확히 정리해야 한다.

---

## Decision: parser / service / API / schema layer 분리

- **Date:** 2026-03-24
- **Status:** Accepted

### Context
이 프로젝트는 `/proc` 파일 읽기, 메트릭 계산, HTTP 응답 처리, 응답 형식 정의를 모두 포함한다. 기능이 늘어나면 각 책임이 섞일 가능성이 있다.

### Decision
backend 구조를 parser, service, API, schema layer로 분리한다.

### Alternatives Considered
- 모든 로직을 FastAPI route 내부에 작성
- parsing과 calculation을 하나의 모듈에 함께 작성
- parser / service / API / schema로 분리

### Reason
각 layer가 담당하는 책임을 분리하면 코드가 더 읽기 쉬워지고, 수정이나 확장이 쉬워진다.

### Trade-offs
- 장점:
  - 역할이 명확해짐
  - 테스트와 유지보수가 쉬워짐
  - 나중에 기능이 늘어나도 구조가 덜 무너짐
- 단점:
  - 파일/폴더 수가 늘어남
  - 초기에 구조 잡는 시간이 더 필요함

### Impact
- parser는 `/proc` 파일 읽기와 parsing만 담당
- service는 metric calculation 담당
- API는 HTTP 처리 담당
- schema는 request/response model 정의 담당

---

## Decision: CPU usage는 two-sample delta 방식 사용

- **Date:** 2026-03-24
- **Status:** Accepted

### Context
`/proc/stat`의 CPU 값은 현재 퍼센트가 아니라 부팅 이후 누적 counter이다. 따라서 한 번 읽는 것만으로는 현재 usage percentage를 구할 수 없다.

### Decision
CPU usage는 `/proc/stat`를 짧은 간격으로 두 번 읽고 delta를 계산하는 방식으로 구현한다.

### Alternatives Considered
- `/proc/stat` single read 사용
- 외부 라이브러리에 계산 위임
- two-sample delta calculation 사용

### Reason
single read는 누적값만 제공하므로 현재 usage percentage 계산에 적합하지 않다. 두 시점 차이를 사용해야 실제 사용률에 가까운 값을 얻을 수 있다.

### Trade-offs
- 장점:
  - Linux 메트릭 의미와 맞는 계산 방식
  - 보다 정확한 CPU usage 산출 가능
- 단점:
  - 두 번 읽어야 하므로 구현이 memory보다 복잡함
  - sampling interval 고려가 필요함

### Impact
CPU metric은 별도 계산 로직이 필요하고, service layer에서 sampling과 delta 계산을 담당하게 된다.

---

## Decision: memory usage는 `MemFree` 대신 `MemAvailable` 사용

- **Date:** 2026-03-24
- **Status:** Accepted

### Context
Linux는 남는 메모리를 buffer/cache로 활용하므로, `MemFree`만 보면 실제 사용 가능한 메모리를 정확히 설명하기 어렵다.

### Decision
memory usage 계산에는 `MemTotal`과 `MemAvailable`을 사용한다.

### Alternatives Considered
- `MemTotal` + `MemFree`
- `MemTotal` + `MemAvailable`

### Reason
`MemAvailable`은 새 프로그램이 사용할 수 있을 것으로 예상되는 메모리 양을 더 잘 반영한다. `MemFree`만 기준으로 보면 메모리가 과도하게 사용된 것처럼 보일 수 있다.

### Trade-offs
- 장점:
  - 실제 Linux 메모리 동작과 더 잘 맞음
  - 사용자 입장에서 더 현실적인 usage 제공 가능
- 단점:
  - cache/buffer 개념을 추가로 이해해야 함

### Impact
memory metric은 아래 계산식을 기준으로 구현한다.
- `used_kb = total_kb - available_kb`
- `usage_percent = used_kb / total_kb * 100`

---

## Decision: network와 disk는 초기 버전에서 raw counter 우선 노출

- **Date:** 2026-03-24
- **Status:** Accepted

### Context
network와 disk는 raw counter를 그대로 보여줄 수도 있고, bytes/sec, reads/sec 같은 rate 기반 값으로 계산해서 보여줄 수도 있다.

### Decision
초기 버전에서는 network와 disk metric을 raw counter 중심으로 제공한다.

### Alternatives Considered
- rate 기반 metric만 제공
- raw counter만 먼저 제공
- raw counter와 rate를 둘 다 첫 버전에 포함

### Reason
초기 버전에서는 `/proc`가 제공하는 원본 데이터에 가깝게 보여주는 것이 더 단순하고 구현/문서화가 쉽다.

### Trade-offs
- 장점:
  - 구현이 단순함
  - `/proc` source data와 직접 연결되어 이해하기 쉬움
  - 초기 복잡도를 줄일 수 있음
- 단점:
  - 클라이언트 입장에서 바로 직관적인 값은 아닐 수 있음
  - rate 기반 정보는 추가 계산이 필요함

### Impact
`/metrics/network`와 `/metrics/disk`는 초기 버전에서 raw counter를 반환하고, rate 기반 endpoint는 추후 확장 기능으로 고려한다.

---
## Decision: Expose only main disk devices in the initial version

- **Date:** 2026-03-30
- **Status:** Accepted

### Context
`/proc/diskstats`에는 `loop*`, `ram*`, `sr*` 같은 가상/임시 디바이스와 `sda1`, `nvme0n1p1` 같은 파티션 엔트리가 포함되어 있다. 모든 엔트리를 보여주기보다는 주요 디스크 장치만 보여주는 것으로 결정했다. 

### Decision
`sda`, `nvme` 등의 주요 디스크 장치만 `/metrics/disk`에서 반환한다. `loop*`, `ram*`, `sr*`와 파티션 엔트리는 초기 버전에서 제외한다.

### Alternatives Considered
- 모든 엔트리를 보여주기
- 메인 디스크 장치만 보여주기
- 메인 장치와 파티션을 별도로 보여주기

### Reason
초기 버전에서는 디스크 엔드포인트를 단순하고 설명하기 쉽게 유지하는 것이 목표다.

### Trade-offs
- 장점:
  - response 구조가 단순해진다.
  - 설명과 검증이 더 쉬워진다.
  - 초기 학습 중심 버전에 더 적합하다.
- 단점:
  - partition-level visibility가 제공되지 않는다.
  - 일부 디바이스 정보가 의도적으로 생략된다.

### Impact
디스크 parser는 `loop*`, `ram*`, `sr*`와 파티션 엔트리를 필터링한다. `/metrics/disk` 엔드포인트는 현재 환경에서 주요 디스크 장치만 반환한다.
`/metrics/disk` 엔드포인트는 현재 환경에서 주요 디스크 장치만 반환한다.