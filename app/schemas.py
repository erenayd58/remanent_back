
from typing import Optional, List
from pydantic import BaseModel, Field

class LocationCreate(BaseModel):
    code: str
    zone: str
    rack: str
    row: str
    bin: str

class LocationRead(LocationCreate):
    pass

class RemanentCreate(BaseModel):
    id: str
    material: str
    thickness_mm: float
    width_mm: float
    height_mm: float
    location_code: str

class RemanentRead(RemanentCreate):
    created_at: str

class RemanentQuery(BaseModel):
    material: str
    thickness_mm: float
    min_width_mm: float = 0
    min_height_mm: float = 0
