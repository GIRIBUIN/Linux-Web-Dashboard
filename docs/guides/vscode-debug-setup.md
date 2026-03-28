# VS Code Python Debugging Setup

패키지 구조(`app/`) 내에서 모듈 간 임포트 에러(`ModuleNotFoundError`) 없이 디버깅하기 위한 설정입니다.

## launch.json 설정
- **path**: `.vscode/launch.json`

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Auto Module (Stable)",
            "type": "debugpy",
            "request": "launch",
            "module": "app.${fileDirnameBasename}.${fileBasenameNoExtension}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/backend",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend"
            },
            "justMyCode": true
        }
    ]
}
```

## 주요 항목 설명

`module`: 파일을 경로로 실행하지 않고 `python -m app.services.memory` 처럼 모듈 방식으로 호출합니다.

`${fileDirnameBasename}`: 현재 폴더명 (예: services)

`${fileBasenameNoExtension}`: 확장자 제외 파일명 (예: memory)

`cwd`: 모든 실행 기준점(Root)을 backend 폴더로 고정합니다.

`PYTHONPATH`: 파이썬이 모듈을 찾을 때 backend 폴더를 최우선으로 탐색하도록 강제합니다.