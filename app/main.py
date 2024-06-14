from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class BlogPost(BaseModel):
    id: int
    title: str
    content: str

blog_posts: List[BlogPost] = []

# Configure logging
logging.basicConfig(filename='/app/logs/app.log', level=logging.WARNING, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.post('/blog', status_code=201)
async def create_blog_post(post: BlogPost):
    blog_posts.append(post)
    logging.warning(f'Blog post created: {post}')
    return {'status': 'success'}

@app.get('/blog', response_model=List[BlogPost])
async def get_blog_posts():
    logging.warning(f'reading all blogs')
    return blog_posts

@app.get('/blog/{id}', response_model=BlogPost)
async def get_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            logging.warning(f'reading blog {id}')
            return post
    raise HTTPException(status_code=404, detail='Post not found')

@app.delete('/blog/{id}', status_code=200)
async def delete_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            logging.warning(f'Blog post deleted: {post}')
            return {'status': 'success'}
    raise HTTPException(status_code=404, detail='Post not found')

@app.put('/blog/{id}', status_code=200)
async def update_blog_post(id: int, updated_post: BlogPost):
    for post in blog_posts:
        if post.id == id:
            post.title = updated_post.title
            post.content = updated_post.content
            logging.warning(f'Blog post updated: {post}')
            return {'status': 'success'}
    raise HTTPException(status_code=404, detail='Post not found')

@app.get('/generate-warning')
async def generate_warning():
    logging.warning('This is a test warning log')
    return {'status': 'Warning log generated'}