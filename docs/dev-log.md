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

---

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
- Implement `GET /health`
- Implement `/metrics/memory`

### 2026-03-24

#### Summary
- Remote development environment setup on Ubuntu VM

#### What I did
- Installed **VSCode Remote-SSH** to develop on the Linux environment.
- Configured **VirtualBox Port Forwarding** (Host:2222 -> Guest:22).
- Successfully established an SSH connection to the Ubuntu VM.
- Synchronized source code from Windows to the Linux environment.
- Created a new **Python virtual environment (venv)** on Linux.

#### What I learned
- **Kernel Dependency**: Reconfirmed that `/proc` is a Linux-specific feature, making the Linux environment mandatory.
- **NAT Networking**: Understood why the host cannot directly access the guest IP (`10.0.2.15`) without port forwarding.
- **Remote Workflow**: Experienced the separation of the editor (Windows) and the execution environment (Linux).

#### Issues / Blockers
- **Connection Failure to 10.0.2.15**
  - **Symptoms**: VSCode failed to connect to the internal NAT IP of the VM.
  - **Cause**: The NAT network model blocks inbound traffic from the host by default.
  - **Resolution**: Implemented port forwarding in VirtualBox settings to map `127.0.0.1:2222` to the guest's port 22.

#### Next step
- Implement `GET /health`
- Implement `/metrics/memory`

---

### 2026-03-25

#### Summary
- Set up the Ubuntu VM development environment
- Implemented and tested the first FastAPI endpoint: `GET /health`

#### What I did
- Cloned the repository in Ubuntu VM and switched to the `dev` branch
- Created a virtual environment in `backend/`
- Installed `fastapi` and `uvicorn[standard]`
- Wrote the first FastAPI app and confirmed `/health` works

#### What I learned
- This project should be developed and tested in Linux because it depends on `/proc`
- `uvicorn app.main:app --reload` should be run from `backend/` based on the current import path

#### Issues / Blockers
- Windows Python version and VSCode interpreter setting were confusing at first
  - Solution: decided to use Ubuntu Python as the actual runtime environment

#### Next step
- Organize `/health` route structure
- Implement `/metrics/memory`

---
### 2026-03-29

#### Summary
- Implemented and verified the `/metrics/memory` endpoint

#### What I did
- Created `parsers/memory.py`, `services/memory.py`, `schemas/memory.py`, and `api/routes/memory.py`
- Parsed `MemTotal` and `MemAvailable` from `/proc/meminfo`
- Calculated `used_kb` and `usage_percent` in the service layer
- Registered the memory router in `main.py`
- Tested `/metrics/memory` with `curl` and `jq`
- Compared API response with `/proc/meminfo` values

#### What I learned
- Parser should focus on reading and parsing raw values, while calculation logic should stay in the service layer
- `MemAvailable` changes slightly over time, so small differences between API output and manual `grep` results are normal
- `jq` makes JSON response checking much easier in the terminal

#### Issues / Blockers
- I first put both parsing and calculation logic into the parser
  - Solution: moved `used_kb` and `usage_percent` calculation into the service layer to match the architecture design

- API response and manual `/proc/meminfo` values did not match exactly
  - Solution: confirmed that the difference came from time gap between API call and manual check, and verified that the calculation logic itself was correct

#### Next step
- Start implementing network metrics next
---
### 2026-03-29

#### Summary
- Implemented and verified the `/metrics/network` endpoint

#### What I did
- Created `parsers/network.py`, `services/network.py`, `schemas/network.py`, and `api/routes/network.py`
- Parsed interface metrics from `/proc/net/dev`
- Extracted `rx_bytes`, `tx_bytes`, `rx_packets`, and `tx_packets`
- Registered the network router in `main.py`
- Tested `/metrics/network` with `curl` and `jq`
- Compared API response with `/proc/net/dev` values

#### What I learned
- `/proc/net/dev` provides cumulative counters for each network interface
- Small differences between API output and manual checks are normal because network values keep changing
- The network endpoint can be implemented cleanly with the same parser → service → schema → route structure used for memory

#### Issues / Blockers
- At first, I was unsure whether the API response should use `name` or `interface` as the field name
  - Solution: used `interface` consistently across parser, service, schema, and route

- API response and `/proc/net/dev` values did not match exactly
  - Solution: confirmed that the values are cumulative counters and change continuously, so small differences between checks are expected

#### Next step
- Start implementing `/metrics/cpu`