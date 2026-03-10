from fastapi import FastAPI, Depends, status, HTTPException
from typing import Optional,List
from database import get_db
from sqlalchemy.orm import Session
import schemas,model,hashing
from database import engine
from routers import blog,users


app = FastAPI()
#model is my table while schemas contains info that is to be sent to the database ie structure of the info that is send
model.Base.metadata.create_all(bind=engine) #establish the connect

#import blogs function form routers/bolg.py
app.include_router(blog.router)
#import users function form routers/users.py
app.include_router(users.router)

@app.get('/')
def index():
    return {'data':'indo'}

@app.get('/about/static')
def stats():
    return {'data':'testing'}

@app.get('/about/{id}')
def about(id: int,blogs:Optional[str] =None, posted:Optional[str]=None):
    return {'name':id}


