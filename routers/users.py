from fastapi import APIRouter,Depends,HTTPException,status
import schemas,model,database,hashing
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post('/user',tags=['users'])
def add_user(request:schemas.User,db: Session = Depends(database.get_db)):
    new_user = model.User(name = request.name, email = request.email, password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user',response_model=List[schemas.ShowUser],tags=['users'])
def all_user(db: Session = Depends(database.get_db)):
    info = db.query(model.User).all()
    return info

@router.get('/user/{id}',response_model=schemas.ShowUser,tags=['users'])
def user_id(id:int, db:Session= Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} doesnot exists"
        )
    return user