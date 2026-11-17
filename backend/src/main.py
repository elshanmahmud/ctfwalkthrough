from datetime import datetime
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException

from .models import PostCreate, PostResponse

app = FastAPI(title="CTF Walkthrough", version="1.0.0")

localdb: List[Dict[str, Any]] = []
id_counter = 0


@app.get("/")
def read_root():
  return {"message": "backend is live"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts():
  return localdb


@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):  # Fixed function name from get_posts
  global id_counter

  for i in localdb:
    if i["slug"] == post.slug:
      raise HTTPException(status_code=400, detail="Slug already exists")

  new_post = {
      "id": str(id_counter),
      "title": post.title,
      "summary": post.summary,
      "slug": post.slug,
      "content": post.content,
      "created_at": datetime.utcnow()
  }

  localdb.append(new_post)
  id_counter += 1

  return new_post