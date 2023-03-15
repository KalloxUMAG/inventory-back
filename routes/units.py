from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Units
from schemas.unit_schema import UnitSchema
from typing import List

from routes.buildings import get_building

units = APIRouter()

@units.get("/api/units", response_model=List[UnitSchema])
def get_units():
    result = get_session().query(Units).all()
    return result

@units.post("/api/units", status_code=HTTP_201_CREATED)
def add_unit(unit: UnitSchema):
    db_building = get_building(unit.building_id)
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_unit = Units(name = unit.name, building_id = unit.building_id)
    session = get_session()
    session.add(new_unit)
    session.commit()
    content = str(new_unit.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@units.get("/api/unit/{unit_id}", response_model=UnitSchema)
def get_unit(unit_id: int):
    return get_session().query(Units).filter(Units.id == unit_id).first()

@units.get("/api/units/{building_id}", response_model=List[UnitSchema])
def get_units_building(building_id: int):
    return get_session().query(Units).filter(Units.building_id == building_id).all()

@units.put("/api/units/{unit_id}", response_model=UnitSchema)
def update_unit(data_update: UnitSchema, unit_id: int):
    db_unit = get_unit(unit_id)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_unit, key, value)
    session = get_session()
    session.add(db_unit)
    session.commit()
    session.refresh(db_unit)
    return db_unit

@units.delete("/api/units/{unit_id}", status_code=HTTP_204_NO_CONTENT)
def delete_unit(unit_id: int):
    db_unit = get_unit(unit_id)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_unit)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)