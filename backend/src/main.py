from datetime import datetime
from typing import Any, Dict, List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session  # <--- Fixed import

from .database import Base, engine, get_db
from .models import Post
from .schemas import PostCreate, PostResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CTF Walkthrough", version="1.0.0")


@app.get("/")
def read_root():
  return {"message": "backend is live"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(Post).all()
  return posts


@app.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
  new_post = Post(  # Avoid shadowing variable names (don't name the variable 'post' if parameter is 'post')
      title=post.title,
      summary=post.summary,
      slug=post.slug,
      content=post.content,
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post