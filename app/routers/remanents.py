
import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..db import get_session
from ..models import Remanent, Location
from ..schemas import RemanentCreate, RemanentRead
from ..settings import get_settings

router = APIRouter(prefix="/remanents", tags=["remanents"])
settings = get_settings()

def _passes_threshold(width_mm: float, height_mm: float) -> bool:
    short_edge = min(width_mm, height_mm)
    area_m2 = (width_mm/1000.0) * (height_mm/1000.0)
    return short_edge >= settings.MIN_SHORT_EDGE_MM and area_m2 >= settings.MIN_AREA_M2

@router.post("", response_model=RemanentRead)
def create_remanent(payload: RemanentCreate, session: Session = Depends(get_session)):
    if not session.get(Location, payload.location_code):
        raise HTTPException(status_code=400, detail="Unknown location_code")

    if not _passes_threshold(payload.width_mm, payload.height_mm):
        raise HTTPException(status_code=400, detail="Below threshold (short edge/area)")

    if session.get(Remanent, payload.id):
        raise HTTPException(status_code=409, detail="ID exists")

    rem = Remanent(**payload.dict(), created_at=datetime.date.today().isoformat())
    session.add(rem)
    session.commit()
    session.refresh(rem)
    return rem

@router.get("", response_model=list[RemanentRead])
def find_remanents(material: str, thickness_mm: float,
                   min_width_mm: float = 0, min_height_mm: float = 0,
                   session: Session = Depends(get_session)):
    stmt = select(Remanent).where(
        Remanent.material==material,
        Remanent.thickness_mm==thickness_mm,
        Remanent.width_mm>=min_width_mm,
        Remanent.height_mm>=min_height_mm
    ).order_by(Remanent.width_mm*Remanent.height_mm)
    return session.exec(stmt).all()

@router.get("/{rem_id}", response_model=RemanentRead)
def get_one(rem_id: str, session: Session = Depends(get_session)):
    rem = session.get(Remanent, rem_id)
    if not rem:
        raise HTTPException(status_code=404, detail="Not found")
    return rem
