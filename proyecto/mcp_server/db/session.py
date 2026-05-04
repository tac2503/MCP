from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import sys

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    print("Creando tablas en la base de datos...", file=sys.stderr)
    Base.metadata.create_all(bind=engine)
    
