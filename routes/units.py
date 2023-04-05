from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Units, Buildings
from schemas.unit_schema import UnitSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

units = APIRouter()

@units.get("/api/units", response_model=List[UnitSchema])
def get_units(db:Session = Depends(get_db)):
    result = db.query(Units).all()
    return result

@units.post("/api/units", status_code=HTTP_201_CREATED)
def add_unit(unit: UnitSchema, db:Session = Depends(get_db)):
    db_building = db.query(Buildings).filter(Buildings.id == unit.building_id).first()
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_unit = Units(name = unit.name, building_id = unit.building_id)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    content = str(new_unit.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@units.get("/api/unit/{unit_id}", response_model=UnitSchema)
def get_unit(unit_id: int, db:Session = Depends(get_db)):
    return db.query(Units).filter(Units.id == unit_id).first()

@units.get("/api/units/{building_id}", response_model=List[UnitSchema])
def get_units_building(building_id: int, db:Session = Depends(get_db)):
    return db.query(Units).filter(Units.building_id == building_id).all()

@units.put("/api/units/{unit_id}", response_model=UnitSchema)
def update_unit(data_update: UnitSchema, unit_id: int, db:Session = Depends(get_db)):
    db_unit = db.query(Units).filter(Units.id == unit_id).first()
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_unit, key, value)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

@units.delete("/api/units/{unit_id}", status_code=HTTP_204_NO_CONTENT)
def delete_unit(unit_id: int, db:Session = Depends(get_db)):
    db_unit = db.query(Units).filter(Units.id == unit_id).first()
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_unit)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)