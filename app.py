from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.database import Base, engine
from routes.equipments import equipments
from routes.equipments_has_projects import equipments_projects
from routes.buildings import buildings
from routes.units import units
from routes.rooms import rooms
from routes.suppliers import suppliers
from routes.supplier_contact import suppliers_contacts
from routes.brands import brands
from routes.models import models
from routes.model_numbers import model_numbers
from routes.maintenances import maintenances
from routes.invoices import invoices
from routes.projects import projects
from routes.stages import stages

def create_tables():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
create_tables()
app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

routes = [buildings, brands, equipments, equipments_projects, invoices, maintenances, models, model_numbers, units, projects, rooms, stages, suppliers, suppliers_contacts]

for route in routes:
        app.include_router(route)