# Architecture Design

## 1. Project Overview
### 1.1 Project Name
- Linux Web Dashboard

### 1.2 Goal
- Linux 내부 동작 이해
- /proc 파싱
- FastAPI로 REST API 경험
- 배울게 많았으면 하는 프로젝트 경험

### 1.3 Objectives
- CPU/Mem/Network/Disk 수치 정보 수집
- Fast API 설계
- Docker 배포
- 무엇을 배운 프로젝트 였는지?
- 이력서에 어떻게 적을 지

## 2. System Scope
### 2.1 In Scope
- /proc/stat, /proc/meminfo 파싱
- /metrics/* API
- systemd 등록
- Docker
- 그 외 간단한 기능

### 2.2 Out of Scope
- DB
- 프론트엔드 멋있게
- 멀티 서버
- 로그인/인증
- 고급 기능

## 3. High-Level Architecture
### 3.1 Components
- Parser Layer
- Service Layer
- API Layer
- Schema Layer
- Optional Alert Layer

### 3.2 Data Flow
- Client가 /metrics/memory request
- route handler가 service 호출
- service가 parser 호출
- parser가 /proc/meminfo 수집
- service가 usage 계산
- schema에 맞게 JSON 변환

## 4. Directory Structure
각 역할(표로)
- api/routes/
- services/
- parsers/
- schemas/
- core/

## 5. Layer Responsibilities
### 5.1 Parser Layer
- /proc 파일 읽기
- raw text parsing ?
- structured data 반환 ?

### 5.2 Service Layer
- 보통 service에서 usage 계산 왜?
- parser 호출
- business logic 처리
- API에서 쓰기 좋은 형태로 가공
- facade랑 같은건가?

### 5.3 API Layer
- endpoint 정의
- request 처리
- response 반환
- HTTP 에러 처리

### 5.4 Schema Layer
- response model 정의
- 응답 형식 통일
- validaion

## 6. Metric Collection Design
### 6.1 CPU Metrics
- source: /proce/stat
- single read로는 usage 계산 불가 왜?
- two-sample delta 필요

### 6.2 Memory Metrics
- source: /proc/meminfo
- MemTotal, MemAvailable
- userd = total - available

``` bash
free -h

#               total        used        free      shared  buff/cache   available
# Mem:           3936        1087         252         130        2596        2427
# Swap:             0           0           0
```
- total: 응용 프로그램에서 사용할 수 있는 총 메모리 양. 응용 프로그램이 application인가
- used: 사용된 메모리(total - available - buffer/cache)
- free: 사용 가능한 메모리/사용하지 않은 메모리
- shared: ?
- buff/cache: 커널 버퍼와 페이지 캐시 및 슬래브에서 사용되는 결합된 메모리. 애플리케이션이 필요할 경우 언제든지 회수 가능? 이해 안됨. 
- available: 스왑 없이 새 응용 프로그램을 시작하는 데 사용할 수 있는 메모리의 예상값

### 6.3 Network Metrics
- source: /proc/net/dev
- interface 별 rx/tx bytes, packets 뭐여 이게
- loopback 포함 여부

### 6.4 Disk Metrics
- source: /proc/diskstats
- read/write count, sectors
- 어떤 device만 보여줄지? sda, nvme0n1, partition이 각각 뭔디


## 7. Error Handling Strategy
- /proc 파일 읽기 실패 시
- Linux 외 환경
- parsing format이 틀릴 때
- API에 어떤 에러로 보여줄지

## 8. Deployment Architecture
> 실행 환경 설명

### 8.1 Local Development
- windows
- vscode
- python
- linux(virtual box)

### 8.2 systemd Service
- 이게 뭔지 모름
- 백그라운드 서비스로 등록 가능?
- 부팅 시 자동 실행?

### 8.3 Docker Deployment
- 컨테이너로 실행
- linux 환경에서 동작 보장?

## 9. Design Principles
- psutil 사용 안함 왜?
- parsing / service / api 분리 이게 뭔데
- 하향식? 상향십? top down protocol? 이런거 
- 문서 기록 잘하기

## 10. Future Extensions