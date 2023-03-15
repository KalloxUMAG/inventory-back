from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProjectSchema(BaseModel):
    id: Optional[int]
    name: str
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        orm_mode = True