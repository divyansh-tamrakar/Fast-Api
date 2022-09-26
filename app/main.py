from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

posts_data = [{'title': 'title of post1', 'content': 'content of post 1', 'id': 1},
              {'title': 'title of post2', 'content': 'content of post 2', 'id': 2},
              {'title': 'best footballer in the world', 'content': 'CR7', 'id': 3}]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FASTAPI-Project',
                                user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\n\n----------------------database connection successful----------------------\n\n")
        break
    except Exception as e:
        print("Connection to database failed")
        print(e)
        time.sleep(2)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
