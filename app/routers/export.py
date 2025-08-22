
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select
from ..db import get_session
from ..models import Remanent, Location
import csv
import io
from datetime import date

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/remanents.csv")
def export_remanents_csv(session: Session = Depends(get_session)):
    # Query join Remanent with Location for a richer CSV
    rems = session.exec(select(Remanent)).all()
    # Build CSV in-memory
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id","material","thickness_mm","width_mm","height_mm","location_code","created_at"])
    for r in rems:
        writer.writerow([r.id, r.material, r.thickness_mm, r.width_mm, r.height_mm, r.location_code, r.created_at])
    content = buf.getvalue()
    headers = {
        "Content-Disposition": f'attachment; filename="remanents_{date.today().isoformat()}.csv"'
    }
    return Response(content, media_type="text/csv", headers=headers)
