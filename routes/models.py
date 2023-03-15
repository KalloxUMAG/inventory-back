from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Models
from schemas.model_schema import ModelSchema
from typing import List

models = APIRouter()

@models.get("/api/models", response_model=List[ModelSchema])
def get_models():
    result = get_session().query(Models).all()
    return result

@models.post("/api/models", status_code=HTTP_201_CREATED)
def add_model(model: ModelSchema):
    new_model = Models(model = model.model, brand = model.brand, product_number = model.product_number)
    session = get_session()
    session.add(new_model)
    session.commit()
    content = str(new_model.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@models.get("/api/models/{model_id}", response_model=ModelSchema)
def get_model(model_id: int):
    return get_session().query(Models).filter(Models.id == model_id).first()

@models.put("/api/models/{model_id}", response_model=ModelSchema)
def update_model(data_update: ModelSchema, model_id: int):
    db_model = get_model(model_id)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_model, key, value)
    session = get_session()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    return db_model

@models.delete("/api/models/{model_id}", status_code=HTTP_204_NO_CONTENT)
def delete_model(model_id: int):
    db_model = get_model(model_id)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_model)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
