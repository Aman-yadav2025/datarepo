from sqlalchemy import Column, Integer,String,Boolean,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

#creating table

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True,index = True)
    password = Column(String)
    blogs = relationship("Blog", back_populates="creator") #search for creator in the Blog class


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    published = Column(Boolean, default=False)
    user_id = Column(Integer,ForeignKey('users.id')) #search for the user_id in the table of users
    creator = relationship("User", back_populates="blogs")



    