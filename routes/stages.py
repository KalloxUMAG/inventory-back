from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Stages
from schemas.stage_schema import StageSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

from routes.projects import get_project

stages = APIRouter()

@stages.get("/api/stages", response_model=List[StageSchema])
def get_stages(db:Session = Depends(get_db)):
    result = db.query(Stages).all()
    return result

@stages.post("/api/stages", status_code=HTTP_201_CREATED)
def add_stage(stage: StageSchema, db:Session = Depends(get_db)):
    db_project = get_project(stage.project_id, db=db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_stage = Stages(name = stage.name, project_id = stage.project_id)
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    content = str(new_stage.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@stages.get("/api/stage/{stage_id}", response_model=StageSchema)
def get_stage(stage_id: int, db:Session = Depends(get_db)):
    return db.query(Stages).filter(Stages.id == stage_id).first()

@stages.get("/api/stages/{project_id}", response_model=List[StageSchema])
def get_stages_project(project_id: int, db:Session = Depends(get_db)):
    return db.query(Stages).filter(Stages.project_id == project_id).all()

@stages.put("/api/stages/{stage_id}", response_model=StageSchema)
def update_stage(data_update: StageSchema, stage_id: int, db:Session = Depends(get_db)):
    db_stage = get_stage(stage_id, db=db)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    if data_update.project_id != None:
        db_project = get_project(data_update.project_id, db=db)
        if not db_project:
            return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_stage, key, value)
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

@stages.delete("/api/stages/{stage_id}", status_code=HTTP_204_NO_CONTENT)
def delete_stage(stage_id: int, db:Session = Depends(get_db)):
    db_stage = get_stage(stage_id, db=db)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_stage)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)