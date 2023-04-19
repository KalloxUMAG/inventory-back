from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Projects
from schemas.project_schema import ProjectSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

projects = APIRouter()

@projects.get("/api/projects", response_model=List[ProjectSchema])
def get_projects(db:Session = Depends(get_db)):
    result = db.query(Projects).all()
    return result

@projects.post("/api/projects", status_code=HTTP_201_CREATED)
def add_project(project: ProjectSchema, db:Session = Depends(get_db)):
    new_project = Projects(name = project.name, owner_id=project.owner_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    content = str(new_project.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@projects.get("/api/projects/{project_id}", response_model=ProjectSchema)
def get_project(project_id: int, db:Session = Depends(get_db)):
    return db.query(Projects).filter(Projects.id == project_id).first()

@projects.put("/api/projects/{project_id}", response_model=ProjectSchema)
def update_project(data_update: ProjectSchema, project_id: int, db:Session = Depends(get_db)):
    db_project = get_project(project_id, db=db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@projects.delete("/api/projects/{project_id}", status_code=HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db:Session = Depends(get_db)):
    db_project = get_project(project_id, db=db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_project)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)