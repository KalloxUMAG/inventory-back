from pydantic import BaseModel
from typing import Optional

class SupplierContactSchema(BaseModel):
        id: Optional[int]
        name: str
        position: Optional[str]
        phone: Optional[str]
        email: Optional[str]
        supplier_id: int

        class Config:
                orm_mode = True