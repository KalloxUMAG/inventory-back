from pydantic import BaseModel
from typing import Optional

class StageSchema(BaseModel):
    id: Optional[int]
    name: str
    project_id: Optional[int]

    class Config:
        orm_mode = True