from pydantic import BaseModel
from typing import Optional

class SupplierSchema(BaseModel):
        id: Optional[int]
        name: str
        rut: Optional[str]
        city_address: Optional[str]

        class Config:
                orm_mode = True