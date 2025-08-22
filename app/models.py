
from typing import Optional
from sqlmodel import SQLModel, Field

class Location(SQLModel, table=True):
    code: str = Field(primary_key=True, index=True)  # e.g., S-B2-03-04
    zone: str
    rack: str
    row: str
    bin: str

class Remanent(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)      # REM-YYYY-MM-XXX
    material: str                                      # GLV, AISI304
    thickness_mm: float
    width_mm: float
    height_mm: float
    location_code: str = Field(foreign_key="location.code")
    created_at: str                                     # ISO date
