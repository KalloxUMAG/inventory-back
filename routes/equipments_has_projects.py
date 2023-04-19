from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Equipments_has_Projects, Projects, Stages, Equipments, Project_owners
from schemas.equipment_has_project_schema import EquipmentHasProjectSchema, EquipmentHasProjectsSchema, ProjectHasEquipmentsSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

from routes.equipments import get_equipment_exist
from routes.projects import get_project
from routes.stages import get_stage

equipments_projects = APIRouter()

@equipments_projects.get("/api/equipments_projects", response_model=List[EquipmentHasProjectSchema])
def get_equipments_has_projects(db:Session = Depends(get_db)):
    result = db.query(Equipments_has_Projects).all()
    return result

@equipments_projects.post("/api/equipments_projects", status_code=HTTP_201_CREATED)
def add_equipment_has_project(equipment_has_project: EquipmentHasProjectSchema, db:Session = Depends(get_db)):
    db_equipment = get_equipment_exist(equipment_has_project.equipment_id, db=db)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_project = get_project(equipment_has_project.project_id, db=db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment_has_project.stage_id != None:
        db_stage = get_stage(equipment_has_project.stage_id, db=db)
        if not db_stage:
            return Response(status_code=HTTP_404_NOT_FOUND)
    new_equipment_has_project = Equipments_has_Projects(equipment_id=equipment_has_project.equipment_id, project_id = equipment_has_project.project_id, stage_id = equipment_has_project.stage_id)
    db.add(new_equipment_has_project)
    db.commit()
    db.refresh(new_equipment_has_project)
    return Response(status_code=HTTP_201_CREATED)

@equipments_projects.get("/api/equipments_project/{project_id}", response_model=List[ProjectHasEquipmentsSchema])
def get_project_equipments(project_id: int, db:Session = Depends(get_db)):
    return db.query(Equipments_has_Projects, Equipments.name.label('equipment_name'), Stages.name.label('stage_name')).outerjoin(
        Equipments, Equipments.id == Equipments_has_Projects.equipment_id).outerjoin(Stages, Stages.id == Equipments_has_Projects.stage_id
        ).filter(Equipments_has_Projects.project_id == project_id).all()

@equipments_projects.get("/api/equipment_projects/{equipment_id}", response_model=EquipmentHasProjectsSchema)
def get_equipment_projects(equipment_id: int, db:Session = Depends(get_db)):
    result = db.query(Equipments_has_Projects.project_id.label('id'), Equipments_has_Projects.stage_id, Projects.name.label('project_name'), Stages.name.label('stage_name'), Project_owners.name.label('project_owner')).outerjoin(
        Stages, Stages.id == Equipments_has_Projects.stage_id).outerjoin(Projects, Projects.id == Equipments_has_Projects.project_id).outerjoin(Project_owners, Project_owners.id == Projects.id
        ).filter(Equipments_has_Projects.equipment_id == equipment_id).first()
    
    if not result:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return result
