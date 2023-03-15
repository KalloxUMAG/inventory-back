from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Suppliers
from schemas.supplier_schema import SupplierSchema
from typing import List

suppliers = APIRouter()

@suppliers.get("/api/suppliers", response_model=List[SupplierSchema])
def get_suppliers():
    result = get_session().query(Suppliers).all()
    return result

@suppliers.post("/api/suppliers", status_code=HTTP_201_CREATED)
def add_supplier(supplier: SupplierSchema):
    new_supplier = Suppliers(name = supplier.name, rut = supplier.rut, city_address = supplier.city_address)
    session = get_session()
    session.add(new_supplier)
    session.commit()
    content = str(new_supplier.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@suppliers.get("/api/suppliers/{supplier_id}", response_model=SupplierSchema)
def get_supplier(supplier_id: int):
    return get_session().query(Suppliers).filter(Suppliers.id == supplier_id).first()

@suppliers.put("/api/suppliers/{supplier_id}", response_model=SupplierSchema)
def update_supplier(data_update: SupplierSchema, supplier_id: int):
    db_supplier = get_supplier(supplier_id)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_supplier, key, value)
    session = get_session()
    session.add(db_supplier)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier

@suppliers.delete("/api/suppliers/{supplier_id}", status_code=HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int):
    db_supplier = get_supplier(supplier_id)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_supplier)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
