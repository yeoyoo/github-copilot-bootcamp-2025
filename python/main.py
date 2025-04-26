import sqlite3
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect("sns.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userName TEXT NOT NULL,
            content TEXT NOT NULL,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL,
            likeCount INTEGER DEFAULT 0,
            commentCount INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            postId INTEGER NOT NULL,
            userName TEXT NOT NULL,
            content TEXT NOT NULL,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL,
            FOREIGN KEY (postId) REFERENCES posts (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            postId INTEGER NOT NULL,
            userName TEXT NOT NULL,
            FOREIGN KEY (postId) REFERENCES posts (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Models
class Post(BaseModel):
    id: int
    userName: str
    content: str
    createdAt: datetime
    updatedAt: datetime
    likeCount: int
    commentCount: int

class CreatePostRequest(BaseModel):
    userName: str
    content: str

class UpdatePostRequest(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    postId: int
    userName: str
    content: str
    createdAt: datetime
    updatedAt: datetime

class CreateCommentRequest(BaseModel):
    userName: str
    content: str

class UpdateCommentRequest(BaseModel):
    content: str

class LikeRequest(BaseModel):
    userName: str

# Endpoints
@app.get("/api/posts", response_model=List[Post])
def get_posts():
    conn = sqlite3.connect("sns.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    conn.close()
    return [Post(id=row[0], userName=row[1], content=row[2], createdAt=row[3], updatedAt=row[4], likeCount=row[5], commentCount=row[6]) for row in rows]

@app.post("/api/posts", response_model=Post, status_code=201)
def create_post(request: CreatePostRequest):
    conn = sqlite3.connect("sns.db")
    cursor = conn.cursor()
    created_at = updated_at = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO posts (userName, content, createdAt, updatedAt) VALUES (?, ?, ?, ?)",
        (request.userName, request.content, created_at, updated_at)
    )
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return Post(id=post_id, userName=request.userName, content=request.content, createdAt=created_at, updatedAt=updated_at, likeCount=0, commentCount=0)

@app.get("/api/posts/{postId}", response_model=Post)
def get_post(postId: int = Path(...)):
    conn = sqlite3.connect("sns.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(id=row[0], userName=row[1], content=row[2], createdAt=row[3], updatedAt=row[4], likeCount=row[5], commentCount=row[6])

@app.patch("/api/posts/{postId}", response_model=Post)
def update_post(postId: int, request: UpdatePostRequest):
    conn = sqlite3.connect("sns.db")
    cursor = conn.cursor()
    updated_at = datetime.utcnow().isoformat()
    cursor.execute("UPDATE posts SET content = ?, updatedAt = ? WHERE id = ?", (request.content, updated_at, postId))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    row = cursor.fetchone()
    conn.close()
    return Post(id=row[0], userName=row[1], content=row[2], createdAt=row[3], updatedAt=row[4], likeCount=row[5], commentCount=row[6])

@app.delete("/api/posts/{postId}", status_code=204)
def delete_post(postId: int):
    conn = sqlite3.connect("sns.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (postId,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    conn.close()