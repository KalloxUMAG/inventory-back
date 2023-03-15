from config.database import Base, engine, get_db
from models.models import *
import sqlalchemy

def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

create_tables()

print(sqlalchemy.__version__)