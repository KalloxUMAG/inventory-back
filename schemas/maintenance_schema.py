from pydantic import BaseModel
from typing import Optional
from datetime import date

class MaintenanceSchema(BaseModel):
    id: Optional[int]
    date: date
    observations: Optional[str]
    maintenance_type: int
    equiptment_id: Optional[int]

    class Config:
        orm_mode = True

class MaintenanceFromEquipment(BaseModel):
    id: int
    date: date
    observations: Optional[str]
    maintenance_type: int

    class Config:
        orm_mode = True