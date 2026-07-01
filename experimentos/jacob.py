from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Text, Optional
from datetime import datetime

app = FastAPI()
posts = []
class Post(BaseModel):
    id: str
    title: str
    author: str
    content: str
    created_at: datetime = datetime.now()
    published_at: Optional[datetime] = None
    published: bool = False
    
@app.get('/')
def read_root():
    return {"message": "Hola, FastAPI!"}
@app.post('/posts')
def create_post(post: Post):
    posts.append(post)
    return post

