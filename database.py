import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This line loads the hidden variables from your .env file
load_dotenv()

# This grabs the specific URL string
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
#cretae the engine 
engine = create_engine(SQLALCHEMY_DATABASE_URL) #used for connection
#create a session
SessionLocal = sessionmaker(bind = engine, autoflush=False,autocommit=False) 
#create the base
Base = declarative_base()