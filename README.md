# Linux Web Dashboard

> Linux `/proc` filesystem 기반 시스템 메트릭 수집 백엔드 프로젝트

## Overview
Linux 시스템의 CPU, memory, network, disk 메트릭을 `/proc` 파일시스템에서 직접 파싱하여 수집하고, 이를 FastAPI 기반 REST API로 제공하는 백엔드 프로젝트입니다.

이 프로젝트는 Linux 내부 동작, `/proc` 기반 메트릭 수집 방식, FastAPI API 설계, 그리고 Linux 실행 환경(Ubuntu VM)에서의 개발 흐름을 학습하기 위해 시작했습니다.

## Goals
- Linux 시스템이 메트릭 정보를 어떻게 제공하는지 이해
- `/proc` 파일을 직접 파싱하는 방식 학습
- FastAPI 기반 REST API 설계 및 구현
- Docker / systemd 같은 Linux 실행 환경 학습
- 문서화와 기록을 통한 학습 과정 정리

## Tech Stack
- Python 3.x
- FastAPI
- Pydantic
- Linux `/proc` filesystem
- Uvicorn
- Ubuntu 24.04 VM
- VSCode Remote SSH

## Current Features
- [x] `GET /health`
- [x] `GET /metrics/cpu`
- [x] `GET /metrics/memory`
- [x] `GET /metrics/network`
- [x] `GET /metrics/disk`

## API Endpoints
- `GET /health`
- `GET /metrics/cpu`
- `GET /metrics/memory`
- `GET /metrics/network`
- `GET /metrics/disk`

## Architecture
The backend is organized with a layered structure:

- **Parser Layer**
  - Reads and parses raw data from `/proc`
- **Service Layer**
  - Calculates metrics and prepares response data
- **API Layer**
  - Exposes FastAPI endpoints
- **Schema Layer**
  - Defines response models with Pydantic

## Metric Sources
- CPU: `/proc/stat`
- Memory: `/proc/meminfo`
- Network: `/proc/net/dev`
- Disk: `/proc/diskstats`

## Development Environment
- Windows host
- Ubuntu 24.04 VM
- VSCode Remote SSH
- Python virtual environment created inside Ubuntu VM

## Project Documents
- `docs/architecture.md`
- `docs/api-spec.md`
- `docs/dev-log.md`
- `docs/decision-log.md`
- `docs/troubleshooting.md`

## How to Run

### 1. Move to backend
```bash
cd backend
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install fastapi "uvicorn[standard]"
```

### 4. Run server
```bash
uvicorn app.main:app --reload
```

### 5. Test endpoints
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/metrics/memory
curl http://127.0.0.1:8000/metrics/network
curl http://127.0.0.1:8000/metrics/cpu
curl http://127.0.0.1:8000/metrics/disk
```

## Current Status
- Core REST API endpoints implemented
- Memory, network, CPU, and disk metric parsing completed
- Documentation for architecture and API specification completed
- Initial validation against `/proc` files completed

## Future Work
- Dockerize the backend
- Learn and apply systemd service setup
- Add CLI dashboard with `rich`
- Consider simple frontend or visualization layer later
- Add optional alerting / filtering / rate-based metrics in future versions