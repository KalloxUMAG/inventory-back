from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Rooms
from schemas.room_schema import RoomSchema
from typing import List

from config.database import get_db
from sqlalchemy.orm import Session

from routes.units import get_unit

rooms = APIRouter()

@rooms.get("/api/rooms", response_model=List[RoomSchema])
def get_rooms(db:Session = Depends(get_db)):
    result = db.query(Rooms).all()
    return result

@rooms.post("/api/rooms", status_code=HTTP_201_CREATED)
def add_room(room: RoomSchema, db:Session = Depends(get_db)):
    db_unit = get_unit(room.unit_id, db=db)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_room = Rooms(name = room.name, unit_id = room.unit_id)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    content = str(new_room.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@rooms.get("/api/room/{room_id}", response_model=RoomSchema)
def get_room(room_id: int, db:Session = Depends(get_db)):
    return db.query(Rooms).filter(Rooms.id == room_id).first()

@rooms.get("/api/rooms/{unit_id}", response_model=List[RoomSchema])
def get_rooms_unit(unit_id: int, db:Session = Depends(get_db)):
    return db.query(Rooms).filter(Rooms.unit_id == unit_id).all()

@rooms.put("/api/rooms/{room_id}", response_model=RoomSchema)
def update_room(data_update: RoomSchema, room_id: int, db:Session = Depends(get_db)):
    db_room = get_room(room_id, db=db)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@rooms.delete("/api/rooms/{room_id}", status_code=HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db:Session = Depends(get_db)):
    db_room = get_room(room_id, db=db)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_room)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)