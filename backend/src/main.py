from datetime import datetime
from typing import Any, Dict, List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session 

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

@app.get("/post/{slug}", response_model=PostResponse)
def get_post_by_slug(slug:str,db: Session = Depends(get_db)):
  post = db.query(Post).filter(Post.slug == slug).first()
  if not post:
    raise HTTPException(404,"No post found with that slug")
  return post

# @app.get("/search", response_model=List[PostResponse])
@app.get("/search")
def search_post(q:str,db: Session = Depends(get_db)):
  posts = db.query(Post).filter(or_(
              Post.title.ilike(q),
              Post.summary.ilike(q),
          )).all()
  return posts



@app.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
  new_post = Post(
      title=post.title,
      summary=post.summary,
      slug=post.slug,
      content=post.content,
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@app.delete("/posts/{postid}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(postid:int,db:Session=Depends(get_db)) -> None:
  post = db.query(Post).filter(Post.id==postid).first()
  if not post:
    raise HTTPException(404,"No post found with that ID")
  db.delete(post)
  db.commit()
  return None