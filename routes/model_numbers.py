from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Model_numbers
from schemas.model_number_schema import ModelNumberSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

from routes.models import get_model

model_numbers = APIRouter()

@model_numbers.get("/api/model_numbers", response_model=List[ModelNumberSchema])
def get_model_numbers(db:Session = Depends(get_db)):
    result = db.query(Model_numbers).all()
    return result

@model_numbers.post("/api/model_numbers", status_code=HTTP_201_CREATED)
def add_model_number(model_number: ModelNumberSchema, db:Session = Depends(get_db)):
    db_model = get_model(model_number.model_id, db=db)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_model_number = Model_numbers(number = model_number.number, model_id = model_number.model_id)
    db.add(new_model_number)
    db.commit()
    db.refresh(new_model_number)
    content = str(new_model_number.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@model_numbers.get("/api/model_number/{model_number_id}", response_model=ModelNumberSchema)
def get_model_number(model_number_id: int, db:Session = Depends(get_db)):
    return db.query(Model_numbers).filter(Model_numbers.id == model_number_id).first()

@model_numbers.get("/api/model_numbers/{model_id}", response_model=List[ModelNumberSchema])
def get_model_numbers_model(model_id: int, db:Session = Depends(get_db)):
    return db.query(Model_numbers).filter(Model_numbers.model_id == model_id).all()

@model_numbers.put("/api/model_numbers/{model_number_id}", response_model=ModelNumberSchema)
def update_model_number(data_update: ModelNumberSchema, model_number_id: int, db:Session = Depends(get_db)):
    db_model_number = get_model_number(model_number_id, db=db)
    if not db_model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_model_number, key, value)
    db.add(db_model_number)
    db.commit()
    db.refresh(db_model_number)
    return db_model_number

@model_numbers.delete("/api/model_numbers/{model_number_id}", status_code=HTTP_204_NO_CONTENT)
def delete_model_number(model_number_id: int, db:Session = Depends(get_db)):
    db_model_number = get_model_number(model_number_id, db=db)
    if not db_model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_model_number)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
