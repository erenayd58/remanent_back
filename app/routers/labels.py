
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..models import Remanent
from ..services.label import render_label_png

router = APIRouter(prefix="/labels", tags=["labels"])

@router.post("/{rem_id}")
def generate_label(rem_id: str, session: Session = Depends(get_session)):
    rem = session.get(Remanent, rem_id)
    if not rem:
        raise HTTPException(status_code=404, detail="Not found")
    out = render_label_png(rem.id, rem.material, rem.thickness_mm, rem.width_mm, rem.height_mm, rem.location_code)
    return {"label_path": out}
