from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
import schemas,database,model
from sqlalchemy.orm import Session


router = APIRouter()

@router.get('/blog',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowModel],tags=['blogs'])
def all(db:Session = Depends(database.get_db)):
    blog = db.query(model.Blog).all()
    return blog

@router.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs']) #schemas is used to create the json that is send to the server
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    
    # 4. Convert the Pydantic schema (request) into a SQLAlchemy model
    new_blog = model.Blog(title=request.title, body=request.body,user_id=1)
    
    # 5. Add it to the database, save (commit), and refresh to get the new ID
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    # Return the newly created blog from the database
    return new_blog


@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowModel,tags=['blogs'])
def blog_id(id :int,response : Response,db:Session = Depends(database.get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with the id {id} is not available"
        )
    return blog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete_blog(id: int, db: Session = Depends(database.get_db)):
    
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

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id: int , request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id )

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} doesnot exists"
        )
    blog.update(request.dict(exclude={'published'}), synchronize_session=False)
    db.commit()
    
    return {'response':"updated"}
