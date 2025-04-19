# 컨테이너 오케스트레이션

## 시작하기

1. Docker Desktop 이 현재 동작중인지 확인합니다.

    ```bash
    docker info
    ```

1. 아래 명령어를 실행시켜 준비된 컨테이너 앱을 실행시킵니다.

    ```bash
    docker compose up -d
    ```

1. 웹 브라우저를 열고 `http://localhost:3000`으로 접속하여 웹사이트가 제대로 동작하는지 확인합니다.

1. 아래 명령어를 실행시켜 컨테이너 앱을 삭제합니다.

```bash
docker compose down --rmi all
```
