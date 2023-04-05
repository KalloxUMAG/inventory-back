from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
#from config.database import get_session
from models.models import Buildings
from schemas.building_schema import BuildingSchema
from typing import List

from fastapi import Depends
from config.database import get_db
from sqlalchemy.orm import Session

buildings = APIRouter()

@buildings.get("/api/buildings", response_model=List[BuildingSchema])
def get_buildings(db:Session = Depends(get_db)):
    result = db.query(Buildings).all()
    return result


@buildings.post("/api/buildings", status_code=HTTP_201_CREATED)
def add_building(building: BuildingSchema, db:Session = Depends(get_db)):
    new_building = Buildings(name=building.name)
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    content = str(new_building.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@buildings.get("/api/buildings/{building_id}", response_model=BuildingSchema)
def get_building(building_id: int, db:Session = Depends(get_db)):
    return db.query(Buildings).filter(Buildings.id == building_id).first()

@buildings.put("/api/buildings/{building_id}", response_model=BuildingSchema)
def update_building(data_update: BuildingSchema, building_id: int, db:Session = Depends(get_db)):
    db_building = db.query(Buildings).filter(Buildings.id == building_id).first()
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_building, key, value)
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

@buildings.delete("/api/buildings/{building_id}", status_code=HTTP_204_NO_CONTENT)
def delete_building(building_id: int, db:Session = Depends(get_db)):
    db_building = db.query(Buildings).filter(Buildings.id == building_id).first()
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_building)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
