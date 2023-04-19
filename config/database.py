from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, scoped_session

username = "kallox"
password = "uv7p11I2zJFAWVhDThJGUsWCp3Lx7mOy"
database = "inventory_nkgu"
ip = "localhost"
port = 5432

database_render = "postgresql://postgres:okBAG6RHetD0JzVdfjXR@containers-us-west-129.railway.app:7821/railway"

DATABASE_URL = database_render

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
#Session = scoped_session(session_factory)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#def get_session(): 
    #return Session
