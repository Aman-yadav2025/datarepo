from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional
from database import  Base
from sqlalchemy.orm import Session
import schemas,model
from database import engine,SessionLocal

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return {'data':'fuck you'}

@app.get('/about/static')
def stats():
    return {'data':'testing'}

@app.get('/about/{id}')
def about(id: int,blogs:Optional[str] =None, posted:Optional[str]=None):
    return {'name':id}

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    
    # 4. Convert the Pydantic schema (request) into a SQLAlchemy model
    new_blog = model.Blog(title=request.title, body=request.body)
    
    # 5. Add it to the database, save (commit), and refresh to get the new ID
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    # Return the newly created blog from the database
    return new_blog

@app.get('/blog')
def all(db:Session = Depends(get_db)):
    blog = db.query(model.Blog).all()
    return blog

@app.get('/blog/{id}', status_code=200)
def blog_id(id :int,response : Response,db:Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with the id {id} is not available"
        )
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    
    # 1. Find the blog post in the database
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    
    # 2. Check if it actually exists; if not, throw a 404 error
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} not found"
        )
    
    # 3. If it does exist, delete it and commit the change
    blog.delete(synchronize_session=False)
    db.commit()
    
    # 4. Return a proper 204 response (no dictionary!)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id: int , request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id )

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"fuck you blog {id} isn't there"
        )
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    
    return {'response':"updated"}

