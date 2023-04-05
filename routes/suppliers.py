from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Suppliers
from schemas.supplier_schema import SupplierSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

suppliers = APIRouter()

@suppliers.get("/api/suppliers", response_model=List[SupplierSchema])
def get_suppliers(db:Session = Depends(get_db)):
    result = db.query(Suppliers).all()
    return result

@suppliers.post("/api/suppliers", status_code=HTTP_201_CREATED)
def add_supplier(supplier: SupplierSchema, db:Session = Depends(get_db)):
    new_supplier = Suppliers(name = supplier.name, rut = supplier.rut, city_address = supplier.city_address)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    content = str(new_supplier.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@suppliers.get("/api/suppliers/{supplier_id}", response_model=SupplierSchema)
def get_supplier(supplier_id: int, db:Session = Depends(get_db)):
    return db.query(Suppliers).filter(Suppliers.id == supplier_id).first()

@suppliers.put("/api/suppliers/{supplier_id}", response_model=SupplierSchema)
def update_supplier(data_update: SupplierSchema, supplier_id: int, db:Session = Depends(get_db)):
    db_supplier = get_supplier(supplier_id, db=db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_supplier, key, value)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@suppliers.delete("/api/suppliers/{supplier_id}", status_code=HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db:Session = Depends(get_db)):
    db_supplier = get_supplier(supplier_id, db=db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_supplier)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
