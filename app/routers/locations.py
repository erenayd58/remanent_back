
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models import Location
from ..schemas import LocationCreate, LocationRead

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("", response_model=LocationRead)
def create_location(payload: LocationCreate, session: Session = Depends(get_session)):
    loc = session.get(Location, payload.code)
    if loc:
        return loc
    loc = Location(**payload.dict())
    session.add(loc)
    session.commit()
    session.refresh(loc)
    return loc

@router.get("", response_model=list[LocationRead])
def list_locations(session: Session = Depends(get_session)):
    res = session.exec(select(Location)).all()
    return res
