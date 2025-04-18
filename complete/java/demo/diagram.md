# SNS API 서비스 다이어그램

## 전체 시스템 구조

```
+--------------------------------------------+
|                FastAPI 애플리케이션          |
+--------------------------------------------+
| - title: "Simple SNS API"                  |
| - CORS 미들웨어 추가                         |
| - API 라우터 설정 (/api)                    |
+--------------------------------------------+
               |
               | 사용
               v
+--------------------------------------------+
|                데이터베이스                  |
+--------------------------------------------+
| - SQLite                                   |
| - 테이블: posts, comments, likes           |
+--------------------------------------------+
               |
               | 포함
               v
+--------------------------------------------+
|                데이터 모델                   |
+--------------------------------------------+
|          |           |           |         |
|          v           v           v         |
+----------+    +------+    +------+         |
|   Post   |    |Comment|    | Like |         |
+----------+    +------+    +------+         |
+--------------------------------------------+
               |
               | 구현
               v
+--------------------------------------------+
|                 API 엔드포인트              |
+--------------------------------------------+
| 포스트 관련:                                |
| - GET /api/posts                          |
| - POST /api/posts                         |
| - GET /api/posts/{postId}                 |
| - PATCH /api/posts/{postId}               |
| - DELETE /api/posts/{postId}              |
|                                            |
| 댓글 관련:                                  |
| - GET /api/posts/{postId}/comments        |
| - POST /api/posts/{postId}/comments       |
| - GET /api/posts/{postId}/comments/{id}   |
| - PATCH /api/posts/{postId}/comments/{id} |
| - DELETE /api/posts/{postId}/comments/{id}|
|                                            |
| 좋아요 관련:                                |
| - POST /api/posts/{postId}/likes          |
| - DELETE /api/posts/{postId}/likes        |
+--------------------------------------------+
```

## 데이터 모델 상세 다이어그램

```
+----------------+       +----------------+       +----------------+
|     Post       |       |    Comment     |       |      Like      |
+----------------+       +----------------+       +----------------+
| id: int        |       | id: int        |       | postId: int    |
| userName: str  |       | postId: int    |       | userName: str  |
| content: str   |       | userName: str  |       |                |
| createdAt: str |       | content: str   |       |                |
| updatedAt: str |       | createdAt: str |       |                |
| likeCount: int |       | updatedAt: str |       |                |
| commentCount:int|       |                |       |                |
+----------------+       +----------------+       +----------------+
        |                        |                        |
        | 1                      | *                      | *
        v                        v                        v
+----------------+       +----------------+       +----------------+
|   PostCreate   |       | CommentCreate  |       |   LikeBase    |
+----------------+       +----------------+       +----------------+
| userName: str  |       | userName: str  |       | userName: str  |
| content: str   |       | content: str   |       |                |
+----------------+       +----------------+       +----------------+
        |                        |
        v                        v
+----------------+       +----------------+
|   PostUpdate   |       | CommentUpdate  |
+----------------+       +----------------+
| content: str   |       | content: str   |
+----------------+       +----------------+
```

## 데이터베이스 스키마 다이어그램

```
+----------------+       +----------------+       +----------------+
|     posts      |       |    comments    |       |     likes      |
+----------------+       +----------------+       +----------------+
| id             |       | id             |       | postId         |
| userName       |       | postId         |       | userName       |
| content        |       | userName       |       +----------------+
| createdAt      |       | content        |              ^
| updatedAt      |       | createdAt      |              |
| likeCount      |       | updatedAt      |              |
| commentCount   |       +----------------+              |
+----------------+              ^                        |
        ^                       |                        |
        |                       +------------------------+
        |                       |                        |
        +-----------------------+------------------------+
                       외래 키 관계
```

## API 흐름 다이어그램

```
클라이언트 → HTTP 요청 → FastAPI 애플리케이션 → API 라우터 → 비즈니스 로직 → 
SQLite 데이터베이스 → 결과 → Pydantic 모델 변환 → JSON 응답 → 클라이언트
```

## API 엔드포인트 설명

1. **포스트 관련 API**
   - `GET /api/posts`: 모든 포스트 목록 조회
   - `POST /api/posts`: 새 포스트 작성
   - `GET /api/posts/{postId}`: 특정 포스트 조회
   - `PATCH /api/posts/{postId}`: 특정 포스트 수정
   - `DELETE /api/posts/{postId}`: 특정 포스트 삭제

2. **댓글 관련 API**
   - `GET /api/posts/{postId}/comments`: 특정 포스트의 댓글 목록 조회
   - `POST /api/posts/{postId}/comments`: 특정 포스트에 댓글 작성
   - `GET /api/posts/{postId}/comments/{commentId}`: 특정 댓글 조회
   - `PATCH /api/posts/{postId}/comments/{commentId}`: 특정 댓글 수정
   - `DELETE /api/posts/{postId}/comments/{commentId}`: 특정 댓글 삭제

3. **좋아요 관련 API**
   - `POST /api/posts/{postId}/likes`: 특정 포스트에 좋아요 추가
   - `DELETE /api/posts/{postId}/likes`: 특정 포스트의 좋아요 취소
