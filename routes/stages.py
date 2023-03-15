from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Stages
from schemas.stage_schema import StageSchema
from typing import List

from routes.projects import get_project

stages = APIRouter()

@stages.get("/api/stages", response_model=List[StageSchema])
def get_stages():
    result = get_session().query(Stages).all()
    return result

@stages.post("/api/stages", status_code=HTTP_201_CREATED)
def add_stage(stage: StageSchema):
    db_project = get_project(stage.project_id)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_stage = Stages(name = stage.name, project_id = stage.project_id)
    session = get_session()
    session.add(new_stage)
    session.commit()
    content = str(new_stage.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@stages.get("/api/stage/{stage_id}", response_model=StageSchema)
def get_stage(stage_id: int):
    return get_session().query(Stages).filter(Stages.id == stage_id).first()

@stages.get("/api/stages/{project_id}", response_model=List[StageSchema])
def get_stages_project(project_id: int):
    return get_session().query(Stages).filter(Stages.project_id == project_id).all()

@stages.put("/api/stages/{stage_id}", response_model=StageSchema)
def update_stage(data_update: StageSchema, stage_id: int):
    db_stage = get_stage(stage_id)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    if data_update.project_id != None:
        db_project = get_project(data_update.project_id)
        if not db_project:
            return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_stage, key, value)
    session = get_session()
    session.add(db_stage)
    session.commit()
    session.refresh(db_stage)
    return db_stage

@stages.delete("/api/stages/{stage_id}", status_code=HTTP_204_NO_CONTENT)
def delete_stage(stage_id: int):
    db_stage = get_stage(stage_id)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_stage)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)