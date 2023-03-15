from pydantic import BaseModel
from typing import Optional

class EquipmentHasProjectSchema(BaseModel):
    equipment_id: int
    project_id: int
    stage_id: Optional[int]

    class Config:
        orm_mode = True

class EquipmentHasProjectsSchema(BaseModel):
    id: int
    project_name: str
    stage_id: Optional[int]
    stage_name: Optional[str]

    class Config:
        orm_mode = True

class ProjectHasEquipmentsSchema(BaseModel):
    equipment_id: int
    equipment_name: str
    stage_id: Optional[int]
    stage_name: Optional[str]

    class Config:
        orm_mode = True