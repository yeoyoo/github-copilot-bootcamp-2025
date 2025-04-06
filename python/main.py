import sqlite3
import datetime
from fastapi import FastAPI, Request, HTTPException, status, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Simple SNS API",
    description="간단한 SQLite + FastAPI 예시 (클래스/함수 최소화)",
    version="1.0.0"
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# API 라우터 설정
api_router = APIRouter(prefix="/api")

@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
def startup():
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 테이블
    c.execute("""
    CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      userName TEXT NOT NULL,
      content TEXT NOT NULL,
      createdAt TEXT NOT NULL,
      updatedAt TEXT NOT NULL,
      likeCount INTEGER NOT NULL,
      commentCount INTEGER NOT NULL
    )
    """)

    # 댓글 테이블
    c.execute("""
    CREATE TABLE IF NOT EXISTS comments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      postId INTEGER NOT NULL,
      userName TEXT NOT NULL,
      content TEXT NOT NULL,
      createdAt TEXT NOT NULL,
      updatedAt TEXT NOT NULL
    )
    """)

    # 좋아요 테이블
    c.execute("""
    CREATE TABLE IF NOT EXISTS likes (
      postId INTEGER NOT NULL,
      userName TEXT NOT NULL,
      PRIMARY KEY (postId, userName)
    )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------
# (1) 모든 포스트 목록 조회 (GET /api/posts)
# ------------------------------------------------
@api_router.get("/posts", operation_id="getPosts")
def get_posts():
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id ASC")
    rows = c.fetchall()
    col = [desc[0] for desc in c.description]
    conn.close()

    # 튜플을 딕셔너리로 변환해서 반환
    return [dict(zip(col, row)) for row in rows]


# ------------------------------------------------
# (2) 새 포스트 작성 (POST /api/posts)
# ------------------------------------------------
@api_router.post("/posts", status_code=status.HTTP_201_CREATED, operation_id="createPost")
async def create_post(request: Request):
    body = await request.json()
    userName = body.get("userName")
    content = body.get("content")
    if not userName or not content:
        raise HTTPException(status_code=400, detail="userName, content가 필요합니다.")

    now = datetime.datetime.utcnow().isoformat() + "Z"
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO posts (userName, content, createdAt, updatedAt, likeCount, commentCount)
        VALUES (?, ?, ?, ?, 0, 0)
    """, (userName, content, now, now))
    post_id = c.lastrowid
    conn.commit()

    # 삽입 후 해당 포스트 정보를 다시 SELECT
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = c.fetchone()
    col = [desc[0] for desc in c.description]
    conn.close()

    return dict(zip(col, row))


# ------------------------------------------------
# (3) 특정 포스트 조회 (GET /api/posts/{postId})
# ------------------------------------------------
@api_router.get("/posts/{postId}", operation_id="getPost")
def get_post(postId: int):
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    row = c.fetchone()
    col = [desc[0] for desc in c.description] if c.description else []
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")
    return dict(zip(col, row))


# ------------------------------------------------
# (4) 특정 포스트 수정 (PATCH /api/posts/{postId})
# ------------------------------------------------
@api_router.patch("/posts/{postId}", operation_id="updatePost")
async def update_post(postId: int, request: Request):
    body = await request.json()
    new_content = body.get("content")
    if new_content is None:
        raise HTTPException(status_code=400, detail="수정할 content가 없습니다.")

    # 기존 포스트 확인
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    old = c.fetchone()
    if not old:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        UPDATE posts
        SET content = ?, updatedAt = ?
        WHERE id = ?
    """, (new_content, now, postId))
    conn.commit()

    # 수정된 내용 다시 SELECT
    c.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    row = c.fetchone()
    col = [desc[0] for desc in c.description]
    conn.close()

    return dict(zip(col, row))


# ------------------------------------------------
# (5) 특정 포스트 삭제 (DELETE /api/posts/{postId})
# ------------------------------------------------
@api_router.delete("/posts/{postId}", status_code=status.HTTP_204_NO_CONTENT, operation_id="deletePost")
def delete_post(postId: int):
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()
    c.execute("SELECT id FROM posts WHERE id = ?", (postId,))
    post = c.fetchone()
    if not post:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    # 해당 포스트 연관된 댓글, 좋아요, 그리고 포스트 자체 삭제
    c.execute("DELETE FROM comments WHERE postId = ?", (postId,))
    c.execute("DELETE FROM likes WHERE postId = ?", (postId,))
    c.execute("DELETE FROM posts WHERE id = ?", (postId,))
    conn.commit()
    conn.close()
    return


# ------------------------------------------------
# (6) 특정 포스트의 댓글 목록 조회 (GET /api/posts/{postId}/comments)
# ------------------------------------------------
@api_router.get("/posts/{postId}/comments", operation_id="getComments")
def get_comments(postId: int):
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 존재 확인
    c.execute("SELECT id FROM posts WHERE id = ?", (postId,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    c.execute("SELECT * FROM comments WHERE postId = ? ORDER BY id ASC", (postId,))
    rows = c.fetchall()
    col = [desc[0] for desc in c.description]
    conn.close()

    return [dict(zip(col, row)) for row in rows]


# ------------------------------------------------
# (7) 특정 포스트에 댓글 작성 (POST /api/posts/{postId}/comments)
# ------------------------------------------------
@api_router.post("/posts/{postId}/comments", status_code=status.HTTP_201_CREATED, operation_id="createComment")
async def create_comment(postId: int, request: Request):
    body = await request.json()
    userName = body.get("userName")
    content = body.get("content")
    if not userName or not content:
        raise HTTPException(status_code=400, detail="userName, content가 필요합니다.")

    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 존재 확인
    c.execute("SELECT id FROM posts WHERE id = ?", (postId,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        INSERT INTO comments (postId, userName, content, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?)
    """, (postId, userName, content, now, now))

    # 댓글 카운트 갱신
    c.execute("""
        UPDATE posts
        SET commentCount = commentCount + 1,
            updatedAt = ?
        WHERE id = ?
    """, (now, postId))
    conn.commit()

    comment_id = c.lastrowid
    c.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    row = c.fetchone()
    col = [desc[0] for desc in c.description]
    conn.close()

    return dict(zip(col, row))


# ------------------------------------------------
# (8) 특정 댓글 조회 (GET /api/posts/{postId}/comments/{commentId})
# ------------------------------------------------
@api_router.get("/posts/{postId}/comments/{commentId}", operation_id="getComment")
def get_comment(postId: int, commentId: int):
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 존재
    c.execute("SELECT id FROM posts WHERE id = ?", (postId,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    # 해당 댓글
    c.execute("SELECT * FROM comments WHERE id = ?", (commentId,))
    row = c.fetchone()
    col = [desc[0] for desc in c.description] if c.description else []
    if not row or row[1] != postId:
        conn.close()
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    conn.close()

    return dict(zip(col, row))


# ------------------------------------------------
# (9) 특정 댓글 수정 (PATCH /api/posts/{postId}/comments/{commentId})
# ------------------------------------------------
@api_router.patch("/posts/{postId}/comments/{commentId}", operation_id="updateComment")
async def update_comment(postId: int, commentId: int, request: Request):
    body = await request.json()
    new_content = body.get("content")
    if new_content is None:
        raise HTTPException(status_code=400, detail="수정할 content가 필요합니다.")

    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 확인
    c.execute("SELECT id FROM posts WHERE id = ?", (postId,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    # 댓글 확인
    c.execute("SELECT * FROM comments WHERE id = ?", (commentId,))
    row = c.fetchone()
    if not row or row[1] != postId:
        conn.close()
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        UPDATE comments
        SET content = ?, updatedAt = ?
        WHERE id = ?
    """, (new_content, now, commentId))
    conn.commit()

    c.execute("SELECT * FROM comments WHERE id = ?", (commentId,))
    updated = c.fetchone()
    col = [desc[0] for desc in c.description]
    conn.close()

    return dict(zip(col, updated))


# ------------------------------------------------
# (10) 특정 댓글 삭제 (DELETE /api/posts/{postId}/comments/{commentId})
# ------------------------------------------------
@api_router.delete("/posts/{postId}/comments/{commentId}", status_code=status.HTTP_204_NO_CONTENT, operation_id="deleteComment")
def delete_comment(postId: int, commentId: int):
    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 확인
    c.execute("SELECT id FROM posts WHERE id = ?", (postId,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    # 댓글 확인
    c.execute("SELECT * FROM comments WHERE id = ?", (commentId,))
    row = c.fetchone()
    if not row or row[1] != postId:
        conn.close()
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

    # 댓글 삭제
    c.execute("DELETE FROM comments WHERE id = ?", (commentId,))

    # commentCount 재계산
    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        UPDATE posts
        SET commentCount = (SELECT COUNT(*) FROM comments WHERE postId = ?),
            updatedAt = ?
        WHERE id = ?
    """, (postId, now, postId))

    conn.commit()
    conn.close()
    return


# ------------------------------------------------
# (11) 특정 포스트에 좋아요 (POST /api/posts/{postId}/likes)
# ------------------------------------------------
@api_router.post("/posts/{postId}/likes", status_code=status.HTTP_201_CREATED, operation_id="likePost")
async def like_post(postId: int, request: Request):
    body = await request.json()
    userName = body.get("userName")
    if not userName:
        raise HTTPException(status_code=400, detail="userName이 필요합니다.")

    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 확인
    c.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    post = c.fetchone()
    if not post:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    # 이미 좋아요 눌렀는지 확인
    c.execute("SELECT * FROM likes WHERE postId = ? AND userName = ?", (postId, userName))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="이미 좋아요를 눌렀습니다.")

    # 좋아요 추가
    c.execute("INSERT INTO likes (postId, userName) VALUES (?, ?)", (postId, userName))

    # likeCount +1
    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        UPDATE posts
        SET likeCount = likeCount + 1,
            updatedAt = ?
        WHERE id = ?
    """, (now, postId))

    conn.commit()
    conn.close()

    return {"message": "좋아요 성공"}


# ------------------------------------------------
# (12) 특정 포스트의 좋아요 취소 (DELETE /api/posts/{postId}/likes)
# ------------------------------------------------
@api_router.delete("/posts/{postId}/likes", status_code=status.HTTP_204_NO_CONTENT, operation_id="unlikePost")
async def unlike_post(postId: int, request: Request):
    body = await request.json()
    userName = body.get("userName")
    if not userName:
        raise HTTPException(status_code=400, detail="userName이 필요합니다.")

    conn = sqlite3.connect("sns.db")
    c = conn.cursor()

    # 포스트 확인
    c.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    post = c.fetchone()
    if not post:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다.")

    # 좋아요 존재 여부 확인
    c.execute("SELECT * FROM likes WHERE postId = ? AND userName = ?", (postId, userName))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="좋아요 정보가 없습니다.")

    # 좋아요 삭제
    c.execute("DELETE FROM likes WHERE postId = ? AND userName = ?", (postId, userName))

    # likeCount -1
    now = datetime.datetime.utcnow().isoformat() + "Z"
    c.execute("""
        UPDATE posts
        SET likeCount = likeCount - 1,
            updatedAt = ?
        WHERE id = ?
    """, (now, postId))

    conn.commit()
    conn.close()
    return

# API 라우터 등록
app.include_router(api_router)
