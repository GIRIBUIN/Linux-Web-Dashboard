# Development Log

> 의미 있는 진행 사항만 기록합니다.
> 사소한 작업은 생략합니다.
> 구현 진척, 배운 점, 막힌 부분, 다음 작업 위주로 작성합니다.

---

## Writing Rule

다음 경우에 작성:
- 의미 있는 기능 개발을 시작하거나 완료했을 때
- 새로운 기술이나 개념을 학습했을 때
- 작업을 막는 문제나 이슈가 발생했을 때
- 설계 방향이나 구현 방향이 바뀌었을 때

다음 내용은 굳이 작성하지 않아도 됨:
- 아주 작은 리팩토링
- 단순 오타 수정
- 학습 가치가 없는 작은 수정

---

## Template

### YYYY-MM-DD

#### Summary
- 

#### What I did
- 

#### What I learned
- 

#### Issues / Blockers
- 

#### Next step
- 

---

## Logs

### 2026-03-23

#### Summary
- project documentation setup

#### What I did
- Created core documentation files under `docs/`
- Defined the purpose of each document
- Decided to write design documents before implementation

#### Next step
- Define the initial API scope
- Write architecture overview

### 2026-03-24

#### Summary
- Completed first draft of architecture.md
- Started api-spec.md for core endpoints

#### What I did
- Project goal, scope, and layer structure 정리
- Wrote data flow from client request to `/proc` parsing
- Added endpoint drafts for `/health` and `/metrics/*`

#### What I learned
- `/proc/stat` uses cumulative counters, so CPU usage needs delta calculation
- `MemAvailable` is more practical than `MemFree`

#### Issues / Blockers
- layer를 왜 나누는지 설명하는 게 어려웠음
  - 역할 구분은 이해했지만, 분리 이유를 문장으로 정리하는 게 쉽지 않았음
  - Solution: 각 layer의 책임과 분리 이유를 따로 적으면서 정리함

- 데이터 플로우와 다이어그램 표현이 헷갈렸음
  - Schema의 위치와 역할을 runtime flow 기준으로 어떻게 표현할지 혼란이 있었음
  - Solution: Schema는 별도 실행 노드가 아니라 API layer 내부 적용 단계로 정리함

#### Next step
- Write decision log entries
- Start implementing `GET /health`
- Implement `/metrics/memory`