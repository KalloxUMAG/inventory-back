from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Models
from schemas.model_schema import ModelSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

from routes.brands import get_brand

models = APIRouter()

@models.get("/api/models", response_model=List[ModelSchema])
def get_models(db:Session = Depends(get_db)):
    result = db.query(Models).all()
    return result

@models.post("/api/models", status_code=HTTP_201_CREATED)
def add_model(model: ModelSchema, db:Session = Depends(get_db)):
    db_brand = get_brand(model.brand_id, db=db)
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_model = Models(name = model.name, brand_id = model.brand_id)
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    content = str(new_model.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@models.get("/api/model/{model_id}", response_model=ModelSchema)
def get_model(model_id: int, db:Session = Depends(get_db)):
    return db.query(Models).filter(Models.id == model_id).first()

@models.get("/api/models/{brand_id}", response_model=List[ModelSchema])
def get_models_brand(brand_id: int, db:Session = Depends(get_db)):
    return db.query(Models).filter(Models.brand_id == brand_id).all()

@models.put("/api/models/{model_id}", response_model=ModelSchema)
def update_model(data_update: ModelSchema, model_id: int, db:Session = Depends(get_db)):
    db_model = get_model(model_id, db=db)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_model, key, value)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@models.delete("/api/models/{model_id}", status_code=HTTP_204_NO_CONTENT)
def delete_model(model_id: int, db:Session = Depends(get_db)):
    db_model = get_model(model_id, db=db)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_model)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
