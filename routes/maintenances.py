from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Maintenances
from schemas.maintenance_schema import MaintenanceSchema, MaintenanceFromEquipment
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

from routes.equipments import get_equipment_exist

maintenances = APIRouter()

@maintenances.get("/api/maintenances", response_model=List[MaintenanceSchema])
def get_maintenances(db:Session = Depends(get_db)):
    result = db.query(Maintenances).all()
    return result

@maintenances.post("/api/maintenances", status_code=HTTP_201_CREATED)
def add_maintenances(maintenance: MaintenanceSchema, db:Session = Depends(get_db)):
    db_equipment = get_equipment_exist(maintenance.equiptment_id, db=db)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_maintenance = Maintenances(date=maintenance.date, observations=maintenance.observations, maintenance_type=maintenance.maintenance_type, equiptment_id = maintenance.equiptment_id)
    db.add(new_maintenance)
    db.commit()
    db.refresh(new_maintenance)
    return Response(status_code=HTTP_201_CREATED)

@maintenances.get("/api/maintenance/{maintenance_id}", response_model=MaintenanceSchema)
def get_maintenance(maintenance_id: int, db:Session = Depends(get_db)):
    return db.query(Maintenances).filter(Maintenances.id == maintenance_id).first()

@maintenances.get("/api/maintenances/{equipment_id}", response_model=List[MaintenanceFromEquipment])
def get_maintenances_equipment(equipment_id: int, db:Session = Depends(get_db)):
    return db.query(Maintenances.id, Maintenances.date, Maintenances.maintenance_type, Maintenances.observations).filter(Maintenances.equiptment_id == equipment_id).all()

@maintenances.put("/api/maintenances/{maintenance_id}", response_model=MaintenanceSchema)
def update_maintenance(data_update: MaintenanceSchema, maintenance_id: int, db:Session = Depends(get_db)):
    db_maintenance = get_maintenance(maintenance_id, db=db)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_maintenance, key, value)
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@maintenances.delete("/api/maintenances/{maintenance_id}", status_code=HTTP_204_NO_CONTENT)
def delete_maintenance(maintenance_id: int, db:Session = Depends(get_db)):
    db_maintenance = get_maintenance(maintenance_id, db=db)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_maintenance)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)