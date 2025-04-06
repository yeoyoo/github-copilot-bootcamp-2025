# Python 앱 완성본

## 시작하기

### 환경설정 방법

1. 터미널을 실행합니다.
2. 아래 명령어를 순서대로 실행합니다.

```
git clone https://github.com/devrel-kr/github-copilot-bootcamp-2025.git
cd github-copilot-bootcamp-2025
cd python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 실행 방법

1. 터미널에서 아래 명령어를 수행합니다.

```
uvicorn main:app --reload
```

2. 아래와 같은 로그가 출력이 되면 정상적으로 실행이 된 것입니다.

```
INFO:     Will watch for changes in these directories: ['/???/github-copilot-bootcamp-2025/python']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [85427] using StatReload
INFO:     Started server process [85430]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 사용해보기

