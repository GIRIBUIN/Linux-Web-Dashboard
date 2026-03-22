# Linux Server Monitor

> /proc 파일시스템 기반 시스템 메트릭 수집 에이전트

## Overview
리눅스 서버의 CPU, Memory, Disk 등의 상태를 수집하고,
REST API 형태로 제공하는 백엔드 시스템을 구현한다.

리눅스 내부 동작과 서버 운영 흐름을 이해하기 위해 시작한 프로젝트.

## Tech Stack
- Python 3.x
- FastAPI
- Linux /proc filesystem

## Features
- [ ] CPU / Memory / Disk / Network 수집
- [ ] REST API 노출
- [ ] 제한된 명령 실행
- [ ] 로그 저장
- [ ] Docker 배포

## Progress

### Week 1
- FastAPI 서버 구성
- CPU / Memory API 구현

### Week 2
- Disk / Network API 추가
- 명령 실행 기능 구현

### Week 3
- 로그 저장 기능 추가
- 간단한 UI 연결

### Week 4
- Docker 적용
- README 정리

## Troubleshooting

### 문제 1
- 해결법 1: 