from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, scoped_session

username = "kallox"
password = "uv7p11I2zJFAWVhDThJGUsWCp3Lx7mOy"
database = "inventory_nkgu"
ip = "localhost"
port = 5432

database_render = "postgres://kallox:uv7p11I2zJFAWVhDThJGUsWCp3Lx7mOy@dpg-cg8t5b64dad531tt9a30-a.oregon-postgres.render.com/inventory_nkgu"

DATABASE_URL = database_render
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

class Base(DeclarativeBase):
    pass


def get_session(): 
    return Session
