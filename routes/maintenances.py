from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Maintenances
from schemas.maintenance_schema import MaintenanceSchema, MaintenanceFromEquipment
from typing import List

from routes.equipments import get_equipment_exist

maintenances = APIRouter()

@maintenances.get("/api/maintenances", response_model=List[MaintenanceSchema])
def get_maintenances():
    result = get_session().query(Maintenances).all()
    return result

@maintenances.post("/api/maintenances", status_code=HTTP_201_CREATED)
def add_maintenances(maintenance: MaintenanceSchema):
    db_equipment = get_equipment_exist(maintenance.equiptment_id)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_maintenance = Maintenances(date=maintenance.date, observations=maintenance.observations, maintenance_type=maintenance.maintenance_type, equiptment_id = maintenance.equiptment_id)
    session = get_session()
    session.add(new_maintenance)
    session.commit()
    return Response(status_code=HTTP_201_CREATED)

@maintenances.get("/api/maintenance/{maintenance_id}", response_model=MaintenanceSchema)
def get_maintenance(maintenance_id: int):
    return get_session().query(Maintenances).filter(Maintenances.id == maintenance_id).first()

@maintenances.get("/api/maintenances/{equipment_id}", response_model=List[MaintenanceFromEquipment])
def get_maintenances_equipment(equipment_id: int):
    return get_session().query(Maintenances.id, Maintenances.date, Maintenances.maintenance_type, Maintenances.observations).filter(Maintenances.equiptment_id == equipment_id).all()

@maintenances.put("/api/maintenances/{maintenance_id}", response_model=MaintenanceSchema)
def update_maintenance(data_update: MaintenanceSchema, maintenance_id: int):
    db_maintenance = get_maintenance(maintenance_id)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_maintenance, key, value)
    session = get_session()
    session.add(db_maintenance)
    session.commit()
    session.refresh(db_maintenance)
    return db_maintenance

@maintenances.delete("/api/maintenances/{maintenance_id}", status_code=HTTP_204_NO_CONTENT)
def delete_maintenance(maintenance_id: int):
    db_maintenance = get_maintenance(maintenance_id)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_maintenance)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)