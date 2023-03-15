from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Projects
from schemas.project_schema import ProjectSchema
from typing import List

projects = APIRouter()

@projects.get("/api/projects", response_model=List[ProjectSchema])
def get_projects():
    result = get_session().query(Projects).all()
    return result

@projects.post("/api/projects", status_code=HTTP_201_CREATED)
def add_project(project: ProjectSchema):
    new_project = Projects(name = project.name, start_date = project.start_date, end_date = project.end_date)
    session = get_session()
    session.add(new_project)
    session.commit()
    content = str(new_project.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@projects.get("/api/projects/{project_id}", response_model=ProjectSchema)
def get_project(project_id: int):
    return get_session().query(Projects).filter(Projects.id == project_id).first()

@projects.put("/api/projects/{project_id}", response_model=ProjectSchema)
def update_project(data_update: ProjectSchema, project_id: int):
    db_project = get_project(project_id)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    session = get_session()
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@projects.delete("/api/projects/{project_id}", status_code=HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    db_project = get_project(project_id)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_project)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)